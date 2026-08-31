# Monitor configuration and state

Read this file when creating, changing, or scheduling a monitor. Keep each monitor under a stable project directory:

```text
.literature-monitor/<monitor-id>/
├── config.json
├── state.json
└── digests/
    └── YYYY-MM-DD.md
```

Use a short filesystem-safe `monitor-id`. Do not put API keys or institutional credentials in these files.

## `config.json`

```json
{
  "schema_version": 3,
  "monitor_id": "example-topic",
  "topic": {
    "statement": "The research direction in one or two precise sentences",
    "include_concepts": ["optional scope concept supplied as part of the research direction"],
    "exclude_concepts": ["optional out-of-scope concept supplied as part of the research direction"],
    "notes": "Optional semantic boundaries that belong to the research direction"
  },
  "content_types": {
    "include": ["research-article", "review-article"],
    "exclude_unless_requested": ["editorial", "news", "correction", "obituary", "letter-to-the-editor", "book-review"]
  },
  "visibility": {
    "definition": "official-public-article-landing-page-visible-to-readers",
    "full_text_access_required": false,
    "paywalled_full_text_allowed": true,
    "index_record_alone_is_insufficient": true
  },
  "journals": [
    {
      "name": "Canonical Journal Title",
      "aliases": ["Accepted title abbreviation"],
      "issn": ["1234-5678"],
      "publisher_url": "https://publisher.example/journal",
      "reader_visibility_surface": {
        "label": "ASAP Articles",
        "url": "https://publisher.example/journal/asap"
      }
    }
  ],
  "schedule": {
    "frequency": "weekly",
    "weekday": "Monday",
    "local_time": "09:00",
    "timezone": "Asia/Shanghai"
  },
  "retrieval": {
    "mode": "reader-visible-first-seen",
    "require_current_reader_visibility": true,
    "scan_all_current_surface_items": true,
    "metadata_lookback_days": 21,
    "metadata_sources_are_verification_only": true,
    "article_types": ["journal-article"],
    "include_pending_verification": true
  },
  "output": {
    "interface_language": "user-conversation-language",
    "preserve_source_article_titles": true,
    "preserve_canonical_journal_names": true,
    "requested_fields": ["title", "journal", "publisher-status", "first-seen-at", "published-online", "doi-or-stable-identifier", "english-abstract", "visibility-source", "abstract-source"],
    "english_abstract_mode": "original-when-permitted-otherwise-faithful-summary-plus-source",
    "include_relevance_note": false,
    "additional_fields": []
  }
}
```

Journal names are an exact whitelist. `aliases` cover metadata variants; `issn` is preferred when known. `reader_visibility_surface` must point to the official public release surface actually used by that journal. A journal-family request is not an exact whitelist until its member journals are enumerated. `full_text_access_required: false` means subscription-only articles still qualify when their official landing pages are publicly visible; turn it on only when the user explicitly requests freely readable full text.

`topic.statement` records the research direction. Optional `include_concepts`, `exclude_concepts`, and `notes` refine that direction's semantic scope; they are not a requirement that every literal term appear. Preserve user-specified scope boundaries. For legacy configurations, continue to interpret those fields as topic scope.

`output.requested_fields` records the user's report-content requirements. Use `additional_fields` for requested fields such as `conclusion`, `methods`, `authors`, or `corresponding-author`; source every added field. `output.interface_language` controls report headings, labels, and explanations. Exact article titles and canonical journal names remain in the source language. For `english-abstract`, use the original when permitted; otherwise use a faithful English summary and link its source.

## `state.json`

Initialize with:

```json
{
  "schema_version": 3,
  "monitor_id": "example-topic",
  "last_completed_run_at": null,
  "journal_scans": {
    "Canonical Journal Title": {
      "surface_label": "ASAP Articles",
      "surface_url": "https://publisher.example/journal/asap",
      "last_successful_scan_at": null,
      "last_scan_candidate_count": null
    }
  },
  "seen": {}
}
```

Store seen records by normalized lowercase DOI when available. Otherwise use a namespaced stable publisher identifier such as `publisher:<journal-id>:<article-id>`; use a normalized title/author/journal fallback only when no persistent identifier exists:

```json
{
  "10.1234/example.1": {
    "title": "Exact title",
    "journal": "Canonical Journal Title",
    "first_seen_at": "2026-08-30T09:00:00+08:00",
    "visibility_source_url": "https://publisher.example/article/1",
    "visibility_status": "ASAP Articles",
    "published_online": "2026-08-28",
    "first_reported_at": "2026-08-30T09:00:00+08:00"
  }
}
```

State rules:

- Update state atomically after a complete digest is written.
- Add only verified main-list records to `seen` by default. Pending records remain eligible for later verification.
- Update `journal_scans.<journal>.last_successful_scan_at` only after that journal's official online surface was successfully enumerated and the digest was written.
- On partial coverage, preserve the previous scan state for every failed or blocked journal. Metadata-only fallback is not a successful publisher-surface scan.
- `last_completed_run_at` records a successfully written digest, even when some journal scans were partial; per-journal timestamps are authoritative for continuity.
- A DOI already in `seen` is not a new paper. Corrections, retractions, or substantial version changes may be reported separately but must not be relabeled as a new article.
- Preserve legacy `first_reported_at` records during schema migration. New records must also store `first_seen_at` and the official visibility URL.

## Automation prompt requirements

The scheduled prompt should contain:

1. the absolute path to this skill;
2. the absolute `config.json` and `state.json` paths;
3. the instruction to scan every configured official reader-visible online surface and use first observation/DOI state rather than a publication-date window;
4. the instruction to write a dated digest and update state only after success;
5. the instruction to surface partial coverage and source failures.

Do not embed raw credentials, notification preferences, or a duplicate copy of the full configuration in the automation prompt.
