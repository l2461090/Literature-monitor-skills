# Reader-visible release surfaces

Read this file during setup when resolving how a journal exposes newly available articles. These are routing examples, not a closed publisher whitelist. The wording and behavior visible on the official journal site are authoritative.

## Common labels

| Publisher or platform pattern | Common reader-visible label |
|---|---|
| American Chemical Society | ASAP Articles |
| Wiley | Early View |
| Springer Nature | Online First, Latest research articles, Advance online publication |
| Elsevier / Cell Press | Articles in Press, Latest articles |
| AAAS | First Release, Latest research |
| Oxford Academic | Advance Articles, Latest |
| Cambridge University Press | FirstView |
| Taylor & Francis | Latest Articles, Latest issue online |
| SAGE | OnlineFirst |
| IEEE | Early Access |
| BMJ and related platforms | Online First, Latest |
| Project MUSE / humanities platforms | Latest issue, Forthcoming when full article pages are public |
| JSTOR-hosted journal content | Latest issue/article page; verify the journal's own release status |

## Resolution rules

1. Start from the official journal home page and locate the earliest public article stream used by that journal.
2. Prefer a dedicated early-release stream over a formal issue table of contents when both exist.
3. Confirm that list entries lead to public official article landing pages. A page may be paywalled at full text and still be reader-visible.
4. Do not count a manuscript-management status, author-only accepted-paper notice, search snippet, Crossref deposit, repository preprint, or indexing record as official reader visibility.
5. When no dedicated early-release stream exists, use the journal's official Latest Articles or current issue surface and record that limitation.
6. Save the exact label and URL in configuration. If the publisher redesigns the site or redirects to a different surface, re-resolve it rather than silently falling back to date metadata.

## First-run and recurring behavior

- First run: establish a baseline from every in-scope article currently listed on the official release surface. If the surface exposes a trustworthy `first available online` date, an optional initial horizon may be applied; otherwise scan the entire current surface.
- Later runs: compare stable identifiers and official URLs with `seen`. An item is new when it is reader-visible now and was not recorded in a previous successful scan.
- If an article moves from early release into an issue without changing DOI/identifier, it is not new again.
- If the early-release and issue versions use different identifiers, verify version relationships before reporting a second time.
