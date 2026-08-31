# Retrieval and verification protocol

Read this file for every monitoring run.

## Source routing

Use the official publisher online-release surface as the discovery authority and, for every reported paper, an abstract-bearing publisher or structured scholarly source. Structured APIs are preferred for verification, but they cannot replace the official surface for proving current reader visibility.

| Need | Primary | Secondary | Last resort |
|---|---|---|---|
| Current reader-visible discovery | Publisher ASAP/Early View/First Release/Articles in Press/Latest Articles surface | Official publisher feed/API | Carefully scoped web search that resolves back to the publisher page |
| Biomedical coverage | PubMed/Europe PMC | Crossref; publisher | Semantic Scholar |
| Cross-disciplinary metadata | Crossref | OpenAlex | Semantic Scholar |
| DOI verification | DOI resolver; Crossref | PubMed/Europe PMC | Publisher article page |
| Abstract | Publisher; PubMed/Europe PMC | OpenAlex | Semantic Scholar |

Scopus, Web of Science, and ScienceDirect may improve coverage when authenticated access is available. Treat Google Scholar as discovery-only because its results and dates are unstable.

## Completeness strategy

For each journal independently:

1. open the configured official online surface and record its publisher-specific status label;
2. enumerate all currently visible research-article candidates, following pagination/load-more controls until the surface is exhausted;
3. capture title, article URL, DOI when shown, displayed online date/status, and observation timestamp;
4. exact-filter journal identity and article type;
5. merge metadata only to resolve DOI/authors/abstract, never to infer reader visibility;
6. deduplicate against `seen` by DOI, holding unresolved DOI records as pending;
7. fetch abstracts for new plausible candidates and screen semantic relevance;
8. record the successful surface scan independently for that journal.

Do not use only `topic + journal` search queries when an all-articles feed or API is available. Topic queries can miss relevant papers whose titles use different terminology.

## Exact journal matching

Accept a record only when at least one condition holds:

- its ISSN/eISSN equals a configured ISSN; or
- its normalized container title equals the canonical journal name or an explicit alias; or
- the official publisher page proves the journal identity.

Do not use fuzzy matching to turn similarly named journals into whitelist matches. Record unresolved variants and request an alias update.

## Reader visibility and strict time window

The main-list eligibility proof is a current official journal/publisher article listing or article page reachable from the configured reader-visibility surface. Store that URL as `visibility_source_url` and the run timestamp as `first_seen_at`. Public visibility of the landing page is sufficient unless the user separately requires open/full-text access.

Reader visibility and date eligibility are separate requirements. In strict mode, a candidate must be reader-visible on the official publisher surface *and* have an official publisher-displayed online-availability date within the configured window. For a rolling `N`-day window, use inclusive local calendar dates from the scan date minus `N - 1` through the scan date. For a fixed range, both configured endpoints are inclusive.

Date evidence priority:

1. publisher `Published online` / online-availability date on the official surface or official article page;
2. no fallback for strict-date eligibility.

Crossref, PubMed/Europe PMC, OpenAlex, or search-engine dates may be recorded for reconciliation only. Reject created/indexed/deposited dates, print/issue dates, and metadata-only online dates as strict-date evidence. Month-only or year-only official dates are incomplete: retain them as metadata but list the item as date-unverified rather than including it in the main list.

## Identifier and deduplication

Normalize DOI by removing `doi:`, `https://doi.org/`, URL parameters, surrounding whitespace, and trailing punctuation; then lowercase it. The DOI is the preferred deduplication key, but some humanities and social-science journals legitimately rely on stable publisher identifiers or URLs.

If DOI is absent, use a verified stable publisher identifier. If neither exists, use normalized title plus first author plus journal. Do not invent a DOI from URL patterns, and do not exclude an otherwise verified reader-visible article solely because its discipline does not assign DOIs.

When sources disagree, prefer publisher/Crossref DOI metadata, then PubMed/Europe PMC. Report unresolved conflicts.

## Abstract handling

- Use an abstract only when the source explicitly associates it with the verified DOI/title.
- Strip JATS/HTML tags without changing scientific meaning.
- Default output is a faithful English summary when an English source abstract is available. Preserve population, intervention/material, method, principal result, and stated conclusion when present. Use the user's conversation language for surrounding labels and explanations.
- Do not add effect sizes, mechanisms, significance, or limitations absent from the source.
- If the user asks for the original abstract, provide only what the source and applicable quotation limits permit; otherwise link to the source and provide a faithful summary.
- An abstract inferred from the full text, highlights, graphical abstract, or press release must be labeled as a summary of that material, not the article abstract.
- When the journal supplies no abstract, state `No abstract supplied by the journal`. A synopsis derived from accessible article text is optional and must be labeled as a synopsis, never as the original abstract.

## Relevance screen

Classify after reading the title and abstract:

- **Include**: directly addresses the configured direction, population/material/system, mechanism, method, or outcome.
- **Borderline**: adjacent and plausibly useful; include only if the user configured broad sensitivity, otherwise place in the audit trail.
- **Exclude**: merely shares generic terminology or violates an explicit exclusion.

Do not rank by journal prestige—the whitelist already encodes venue preference.

## Coverage status

- **Complete enough for reporting**: every journal's configured official online surface was successfully enumerated, and each main item has verified DOI, visibility URL, first-observed time, and abstract source.
- **Partial coverage**: one or more official online surfaces failed or could not be exhausted. Name affected journals and sources; successful Crossref or index queries do not turn that journal into complete ASAP coverage.
- **Failed run**: no acceptable discovery source succeeded. Preserve state and do not claim zero results.

Record query times and source URLs/API names in the digest so the next run is auditable.
