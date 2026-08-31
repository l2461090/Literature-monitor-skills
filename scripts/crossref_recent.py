#!/usr/bin/env python3
"""Fetch recent Crossref journal-article metadata with exact journal/date filtering.

This is a deterministic fallback for candidate discovery. It does not prove
exhaustive coverage and does not invent or synthesize missing abstracts.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import http.client
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Iterable


CROSSREF_WORKS_URL = "https://api.crossref.org/works"


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    doi = html.unescape(str(value)).strip()
    doi = re.sub(r"^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)", "", doi, flags=re.I)
    doi = doi.split("?", 1)[0].split("#", 1)[0].strip().rstrip(".,;:)]}")
    doi = doi.lower()
    return doi if re.match(r"^10\.\d{4,9}/\S+$", doi) else None


def normalize_text(value: str | None) -> str:
    text = unicodedata.normalize("NFKC", value or "").casefold()
    text = text.replace("&", " and ")
    text = re.sub(r"[^\w]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def normalize_issn(value: str | None) -> str:
    return re.sub(r"[^0-9xX]", "", value or "").upper()


def strip_markup(value: str | None) -> str | None:
    if not value:
        return None
    text = re.sub(r"<[^>]+>", " ", html.unescape(value))
    text = " ".join(text.split())
    return text or None


def date_from_crossref(item: dict[str, Any]) -> tuple[str | None, str | None, str | None]:
    for key in ("published-online", "published", "issued", "published-print"):
        parts = ((item.get(key) or {}).get("date-parts") or [[]])[0]
        if not parts:
            continue
        precision = {1: "year", 2: "month"}.get(len(parts), "day")
        if len(parts) < 3:
            return None, key, precision
        try:
            parsed = dt.date(int(parts[0]), int(parts[1]), int(parts[2]))
        except (TypeError, ValueError):
            continue
        return parsed.isoformat(), key, precision
    return None, None, None


def journal_matches(item: dict[str, Any], journal: dict[str, Any]) -> bool:
    requested_issns = {normalize_issn(x) for x in journal.get("issn", []) if x}
    item_issns = {normalize_issn(x) for x in item.get("ISSN", []) if x}
    if requested_issns and requested_issns.intersection(item_issns):
        return True

    accepted_titles = {normalize_text(journal.get("name"))}
    accepted_titles.update(normalize_text(x) for x in journal.get("aliases", []) if x)
    accepted_titles.discard("")
    item_titles = {normalize_text(x) for x in item.get("container-title", []) if x}
    return bool(accepted_titles.intersection(item_titles))


def author_names(item: dict[str, Any]) -> list[str]:
    names: list[str] = []
    for author in item.get("author", []) or []:
        name = " ".join(x for x in (author.get("given"), author.get("family")) if x)
        if name:
            names.append(name)
    return names


def item_to_record(item: dict[str, Any], requested_journal: str) -> dict[str, Any]:
    publication_date, date_source, date_precision = date_from_crossref(item)
    titles = item.get("title") or []
    journals = item.get("container-title") or []
    abstract = strip_markup(item.get("abstract"))
    doi = normalize_doi(item.get("DOI"))
    return {
        "title": strip_markup(titles[0]) if titles else None,
        "doi": doi,
        "doi_url": f"https://doi.org/{doi}" if doi else None,
        "journal": strip_markup(journals[0]) if journals else None,
        "requested_journal": requested_journal,
        "publication_date": publication_date,
        "publication_date_source": date_source,
        "publication_date_precision": date_precision,
        "type": item.get("type"),
        "authors": author_names(item),
        "abstract": abstract,
        "abstract_source": "Crossref" if abstract else None,
        "url": item.get("URL"),
        "source": "Crossref",
    }


def record_score(record: dict[str, Any]) -> tuple[int, int, int]:
    return (
        1 if record.get("doi") else 0,
        1 if record.get("abstract") else 0,
        1 if record.get("publication_date_source") == "published-online" else 0,
    )


def deduplicate(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}
    for record in records:
        doi = record.get("doi")
        if doi:
            key = f"doi:{doi}"
        else:
            first_author = (record.get("authors") or [""])[0]
            key = "fallback:" + "|".join(
                (normalize_text(record.get("title")), normalize_text(first_author))
            )
        previous = selected.get(key)
        if previous is None or record_score(record) > record_score(previous):
            selected[key] = record
    return sorted(
        selected.values(),
        key=lambda x: (x.get("publication_date") or "", x.get("title") or ""),
        reverse=True,
    )


def parse_journal_spec(value: str) -> dict[str, Any]:
    # CLI form: Canonical title|Alias one,Alias two|ISSN one,ISSN two
    parts = value.split("|", 2)
    return {
        "name": parts[0].strip(),
        "aliases": [x.strip() for x in parts[1].split(",") if x.strip()] if len(parts) > 1 else [],
        "issn": [x.strip() for x in parts[2].split(",") if x.strip()] if len(parts) > 2 else [],
    }


def load_journals(config_path: str | None, cli_journals: list[str]) -> tuple[list[dict[str, Any]], str | None]:
    mailto = None
    journals = [parse_journal_spec(value) for value in cli_journals]
    if config_path:
        config = json.loads(Path(config_path).read_text(encoding="utf-8"))
        configured = config.get("journals") or []
        journals.extend(
            {"name": x, "aliases": [], "issn": []} if isinstance(x, str) else x
            for x in configured
        )
        mailto = config.get("contact", {}).get("mailto")
    if not journals:
        raise ValueError("provide --journal or a config containing journals")
    for journal in journals:
        if not journal.get("name"):
            raise ValueError("every journal must have a canonical name")
        journal.setdefault("aliases", [])
        journal.setdefault("issn", [])
    return journals, mailto


def fetch_json(url: str, user_agent: str, timeout: int, retries: int = 2) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "application/json"})
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read())
        except (
            urllib.error.URLError,
            TimeoutError,
            http.client.IncompleteRead,
            http.client.RemoteDisconnected,
            json.JSONDecodeError,
        ) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(2**attempt)
    raise urllib.error.URLError(f"Crossref response failed after {retries + 1} attempts: {last_error}")


def crossref_url(
    journal: dict[str, Any], from_date: str, until_date: str, rows: int, offset: int, mailto: str | None
) -> str:
    filters = [f"from-pub-date:{from_date}", f"until-pub-date:{until_date}", "type:journal-article"]
    configured_issns = [str(x).strip() for x in journal.get("issn", []) if str(x).strip()]
    if configured_issns:
        # Crossref's container-title query is fuzzy. An ISSN filter narrows the
        # API result set before local exact matching and prevents similarly
        # named journals from consuming the pagination budget.
        filters.append(f"issn:{configured_issns[0]}")
    params: dict[str, str | int] = {
        "filter": ",".join(filters),
        "rows": rows,
        "offset": offset,
        "sort": "published",
        "order": "desc",
        "query.container-title": journal["name"],
    }
    if mailto:
        params["mailto"] = mailto
    return CROSSREF_WORKS_URL + "?" + urllib.parse.urlencode(params)


def fetch_journal(
    journal: dict[str, Any],
    from_date: str,
    until_date: str,
    rows: int,
    limit: int,
    mailto: str | None,
    timeout: int,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    user_agent = "literature-monitor-skills/1.0"
    if mailto:
        user_agent += f" (mailto:{mailto})"
    accepted: list[dict[str, Any]] = []
    fetched = 0
    offset = 0
    total_results: int | None = None

    while fetched < limit:
        page_rows = min(rows, limit - fetched)
        payload = fetch_json(crossref_url(journal, from_date, until_date, page_rows, offset, mailto), user_agent, timeout)
        message = payload.get("message") or {}
        items = message.get("items") or []
        if total_results is None:
            total_results = int(message.get("total-results") or 0)
        if not items:
            break
        fetched += len(items)
        offset += len(items)
        for item in items:
            if journal_matches(item, journal):
                record = item_to_record(item, journal["name"])
                record_date = record.get("publication_date")
                if record_date is None or from_date <= record_date <= until_date:
                    accepted.append(record)
        if len(items) < page_rows:
            break

    coverage = {
        "journal": journal["name"],
        "source": "Crossref",
        "query_total_results": total_results,
        "records_fetched": fetched,
        "records_exact_match": len(accepted),
        "truncated": bool(total_results is not None and fetched < total_results),
    }
    return accepted, coverage


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="Path to monitor config.json")
    parser.add_argument(
        "--journal",
        action="append",
        default=[],
        help="Journal spec: Canonical title|Alias one,Alias two|ISSN one,ISSN two",
    )
    parser.add_argument("--from-date", required=True, help="Discovery start date, YYYY-MM-DD")
    parser.add_argument("--until-date", required=True, help="Discovery end date, YYYY-MM-DD")
    parser.add_argument("--mailto", help="Contact email for the Crossref polite pool")
    parser.add_argument("--rows", type=int, default=100, help="Crossref page size (1-1000)")
    parser.add_argument("--limit", type=int, default=500, help="Maximum records fetched per journal")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--output", help="Write JSON here instead of stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        start = parse_date(args.from_date)
        end = parse_date(args.until_date)
        if end < start:
            raise ValueError("--until-date must not be earlier than --from-date")
        if not 1 <= args.rows <= 1000:
            raise ValueError("--rows must be between 1 and 1000")
        if args.limit < 1:
            raise ValueError("--limit must be positive")
        journals, config_mailto = load_journals(args.config, args.journal)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2

    mailto = args.mailto or config_mailto
    all_records: list[dict[str, Any]] = []
    coverage: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    for journal in journals:
        try:
            records, journal_coverage = fetch_journal(
                journal,
                args.from_date,
                args.until_date,
                args.rows,
                args.limit,
                mailto,
                args.timeout,
            )
            all_records.extend(records)
            coverage.append(journal_coverage)
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            errors.append({"journal": journal["name"], "source": "Crossref", "error": str(exc)})

    result = {
        "source": "Crossref",
        "queried_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "discovery_window": {"from": args.from_date, "until": args.until_date},
        "coverage": coverage,
        "records": deduplicate(all_records),
        "errors": errors,
        "limitations": [
            "Crossref is a metadata fallback, not proof of exhaustive journal coverage.",
            "Missing abstracts must be obtained from a publisher or another structured scholarly source.",
            "Publication dates require publisher confirmation when weekly inclusion is material.",
        ],
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(encoded, encoding="utf-8")
    else:
        sys.stdout.write(encoded)

    if errors and not coverage:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
