---
name: literature-monitor-skills
description: Monitor when scholarly articles first become visible to readers on official journal or publisher surfaces—such as ASAP, Online First, Early View, Advance Articles, FirstView, Early Access, Articles in Press, or Latest Articles—and report newly observed relevant work with verified titles, persistent identifiers, and source-grounded abstract summaries. Works for user-specified STEM/SCI, social-science, arts, and humanities journals. Use for recurring target-journal alerts or a 本周最新论文/期刊周报, not broad reviews without a journal whitelist.
---

# Literature-monitor-skills

Track a research direction inside an exact journal whitelist and produce a reproducible digest. The monitored event is **an article entering the reader-visible literature**, not a database assigning it a publication date. The primary source is each journal's official public release surface or article page. This applies equally to scientific, technical, medical, social-science, arts, and humanities journals.

In this skill, **reader-visible** means that an ordinary reader can publicly discover and open the official article landing page and see enough bibliographic identity to establish the work (normally title plus author or persistent identifier). Full text may still require subscription or purchase. Open-access/full-text availability is a separate optional filter and must not be inferred from reader visibility.

## Select the mode

- **Set up** when the user provides or changes a direction, journals, schedule, strict time window, or report-content requirements. Read [references/intake-and-onboarding.md](references/intake-and-onboarding.md) and [references/config-and-state.md](references/config-and-state.md), create or update the monitor bundle, then run an initial retrieval unless the user asks not to.
- **Run now** when the user asks for this week's papers or supplies a case to test. Read [references/retrieval-protocol.md](references/retrieval-protocol.md) and execute one cycle. A persistent config is helpful but not required for a one-off test.
- **Scheduled run** when an existing automation invokes the skill. Read [references/config-and-state.md](references/config-and-state.md) and [references/retrieval-protocol.md](references/retrieval-protocol.md), use the named config and state paths, and do not ask routine questions unless execution cannot continue safely.

## Intake contract

Normal recurring setup requires exactly five user decisions:

1. **Research direction** — the topic, question, or field to monitor;
2. **Target journals** — an explicit journal whitelist;
3. **Schedule** — frequency, day, time, and timezone;
4. **Strict time window** — either a rolling number of calendar days or an explicit inclusive start/end date, in a stated timezone;
5. **Report-content requirements** — the information to provide for each article, such as title, DOI, English abstract, conclusion, methods, authors, publication date, or links.

Accept the five decisions in one natural-language message or guide the user through only the missing items. Do not ask again for information already supplied. The research direction controls semantic screening; any useful inclusion or exclusion boundaries belong in that direction's scope. The strict time window controls date eligibility. Report-content requirements control what the digest displays, not which papers qualify. Do not activate a strict monitor without an explicit time window. Unless the user changes the defaults, include research articles and reviews and exclude editorials, news, corrections, obituaries, letters to the editor, and book reviews.

If timezone is omitted, use the user's current timezone. If a weekly schedule omits day or time, assume Monday 09:00, state the assumption, and make it easy to change. Do not silently expand a title such as `Nature` into the full Nature Portfolio. Resolve ambiguous titles, aliases, print/online ISSNs, and the journal's official reader-visible release surface before claiming coverage. Use [references/publisher-surface-taxonomy.md](references/publisher-surface-taxonomy.md) for routing; visible publisher wording controls over the examples.

## Non-negotiable meaning of “latest within the requested window”

- A paper is eligible only when it is visible to readers on the official publisher surface configured for that journal: **ASAP Articles**, **Early View**, **First Release**, **Articles in Press**, or **Latest Articles**. A DOI/index record without current publisher visibility is not sufficient for the main list.
- Equivalent labels—including **Online First**, **OnlineFirst**, **Advance Articles**, **FirstView**, **Early Access**, **Latest**, and publisher-specific variants—have the same meaning when the official journal uses them.
- A paper must have an official publisher-displayed online-availability date inside the configured strict time window. For `last N calendar days`, calculate inclusive local dates from the scan date minus `N - 1` days through the scan date, using the configured timezone. For an explicit range, both start and end dates are inclusive. Crossref dates cannot substitute for a missing official date.
- Within that strict window, the weekly/new-item boundary is **first observed by this monitor** and DOI/stable-identifier deduplication. On the first scan, report only currently visible relevant papers whose official date is inside the window; do not backfill older visible items. On later scans, report only in-window items whose stable identity has not previously been recorded.
- Scan every currently listed research article on the relevant surface, following pagination or load-more controls. Do not stop at a seven-day metadata date filter.
- Record the publisher's online date and use it as a strict eligibility condition when a time window is configured. Never use Crossref deposit, created, updated, indexed, issue-assignment, or metadata-only online dates as proof that a reader could see the paper or as a substitute for the required official date.
- Crossref, PubMed/Europe PMC, OpenAlex, and search engines are candidate-discovery or verification fallbacks. If the official surface cannot be checked, mark that journal **partial/unverified coverage** and do not claim it had zero new ASAP articles.
- Never require a DOI when a discipline or journal legitimately uses another persistent identifier or stable official article URL. Prefer DOI; otherwise record the publisher article identifier/URL and use it for deduplication.

## Run one monitoring cycle

1. Load the configuration and state. Freeze the scan start time and show the previous successful publisher-surface scan time for each journal.
2. Open each configured `reader_visibility_surface.url` (accept legacy `online_surface`) and enumerate every currently visible in-scope scholarly article, following pagination/load-more controls. Capture the surface label, source URL, scan time, title, article URL, DOI or other persistent identifier when present, and the official displayed online-availability date/status.
3. Follow [references/retrieval-protocol.md](references/retrieval-protocol.md). Treat journals independently so a blocked publisher does not become a false zero for that journal.
4. Require exact journal identity using the official surface, canonical title, aliases, or ISSN. Exclude accepted manuscripts that have no public official landing page and exclude content types outside the saved configuration. A publicly visible accepted manuscript or version-of-record page may qualify when the journal itself presents it in the configured release surface.
5. Before a candidate reaches the main list, enforce the configured strict time window using its official publisher-displayed online date. Put a visible candidate with a missing, incomplete, or out-of-range official date in a separately labeled date-unverified/excluded section; do not use a metadata date to make it eligible. Then fetch an official or structured abstract when needed to screen the research direction, and collect each requested report field. Do not rely on title keywords alone.
6. Deduplicate against `state.json` by normalized DOI, then by another persistent publisher identifier, then by normalized title plus first author plus journal. Absence of a DOI is not a reason to discard a legitimate humanities or social-science article when its official identity and visibility are verified.
7. Verify each main-list identifier and ground every requested abstract, conclusion, or other content field in an official or structured scholarly source. Record both the visibility-source URL and the source URL for the requested content. Some humanities journals provide no abstract; in that case report `No abstract supplied by the journal` when an abstract was requested and, only if requested, provide a clearly labeled synopsis grounded in accessible article text—not an invented abstract. If a requested conclusion is unavailable from accessible authoritative text, say so rather than infer it.
8. Write the digest. Only after the digest succeeds, add verified reported records to `seen` with `first_seen_at`, and update `journal_scans.<journal>` only for journals whose official online surface was successfully inspected. A partial run must preserve failed journals' previous scan state.

The bundled stdlib-only [scripts/crossref_recent.py](scripts/crossref_recent.py) is a secondary metadata and DOI-verification helper. It is not sufficient to claim ASAP/Early View completeness or reader visibility.

## Output contract

Start every report with:

- scan time and timezone;
- strict time window, inclusive calculated start/end dates, and the official-date rule used;
- exact journals requested;
- per-journal official online surface, previous/current scan time, and any failures;
- number of newly observed, verified, relevant papers.

Use the user's conversation language for report headings, section headings, field labels, coverage explanations, audit notes, source notes, and conclusions. For a Chinese-language report, write all of those surrounding elements in Chinese. Keep article titles and canonical journal names in the publisher's original language (normally English for the target journals), and keep requested English abstracts and article summaries in English. Preserve publisher-surface labels such as `ASAP Articles` or `Early View` exactly as shown by the publisher. By default, include title, journal, publisher status, first observation time, online date when available, DOI/stable identifier, English abstract, and source links. Add or omit article-level fields according to the user's report-content requirements. The example below uses Chinese surrounding labels; localize them for users speaking another language. For each verified paper, output:

```markdown
### N. Exact article title
- 期刊：Canonical journal title
- 出版商状态：ASAP Articles / Early View / First Release / Articles in Press / Latest Articles
- 首次观察时间：ISO-8601 timestamp
- 官网首次在线日期：YYYY-MM-DD（only when the publisher displays or verifies it）
- DOI: https://doi.org/10.xxxx/xxxxx
- 英文摘要：Original English abstract when permitted; otherwise a faithful English summary grounded only in the verified abstract, with its source link
- 可见性来源：Official publisher URL
- 摘要来源：Publisher/PubMed/Europe PMC/OpenAlex URL
```

Keep these sections separate when applicable:

- **Pending verification** — reader-visible item with missing/unresolved DOI or abstract;
- **Excluded after screening** — optional compact audit trail with exclusion reason.

When no new verified paper qualifies, say exactly that and still report every publisher surface, coverage failure, and date-unverified candidate. Never convert a failed/blocked official-surface scan into a definitive “no new ASAP papers” claim.

## Recurring automation

When the user asks for weekly delivery and the product provides a scheduling/automation tool, create a recurring automation only after saving the monitor configuration. Prefer a heartbeat attached to the current task. The automation prompt must name this skill, the absolute config/state paths, and instruct the run to search, verify, write the digest, and update state only on success. Keep notification preferences out of the prompt. If scheduling is unavailable, provide the exact saved config and a manual run command without claiming that monitoring is active.

## Stop conditions

- If every primary source fails, produce a failed-run report and preserve state.
- If one or more official online surfaces are uncovered, label the digest **partial coverage** and identify them; metadata-only fallback does not upgrade that journal to complete ASAP coverage.
- If journal identity is ambiguous, ask one focused question instead of searching a guessed family.
- Never invent a DOI, abstract, publication date, journal match, or claim of completeness.
