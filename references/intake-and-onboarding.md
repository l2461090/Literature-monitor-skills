# Intake and onboarding

Read this file when setting up or materially changing a monitor.

## The four required decisions

| Decision | What to collect | How it is used |
|---|---|---|
| Research direction | A topic, research question, or one-to-two-sentence scope statement; include any desired scope boundaries here | Creates the semantic topic rule and retrieval concepts |
| Target journals | Exact journal titles or unambiguous aliases | Creates the fixed journal whitelist and publisher-surface routes |
| Schedule | Frequency, day, local time, and timezone | Creates or updates the recurring task |
| Report-content requirements | The fields to show for each article, such as title, DOI, English abstract, conclusion, methods, authors, dates, or links | Controls the article-level fields in the digest |

The research direction determines whether a paper is relevant. Its scope may include helpful boundaries such as a system, method, application, inclusion, or exclusion. The fourth decision is solely about what the digest should provide for each qualifying article; save it under `output` rather than `topic`.

## Recommended user prompt

When none of the four decisions is known, ask the user to complete this compact template in one message:

```text
研究方向：
目标期刊：
定时任务：
输出内容要求：
```

Equivalent English template:

```text
Research direction:
Target journals:
Schedule:
Report content requirements:
```

Natural-language answers are valid. Do not force the template when the user has already supplied usable information. Ask only for missing or materially ambiguous decisions.

## Defaults and interpretation

- Exact journal titles form a whitelist. A publisher family or phrase such as `Nature journals` must be enumerated before coverage can be claimed.
- When a weekly schedule lacks a day or time, assume Monday at 09:00 in the user's current timezone and explicitly show the assumption.
- Default content types are research articles and review articles. Exclude editorials, news, corrections, obituaries, letters to the editor, and book reviews unless requested.
- Default relevance mode is direct semantic relevance. Put plausible but non-central papers in an adjacent/borderline section rather than silently mixing them into the direct list.
- A research direction may be broad (`all work on supramolecular chemistry`) or constrained (`only host–guest recognition involving macrocycles; exclude biomedical delivery`). Preserve both inclusions and exclusions as topic scope.
- Default report content is title, journal, publisher status, first observation time, online date when available, DOI/stable identifier, English abstract, visibility source, and abstract source. The user may request a conclusion, methods, authors, or other fields in addition to or instead of optional defaults.
- If the user asks to preview the configuration or report format before activation, create a preview and do not create or modify the recurring task until the user confirms.

## Confirmation summary

Before or while saving setup, present the four decisions in a compact summary so mistakes are visible:

```markdown
- 研究方向：...
- 目标期刊：...
- 定时任务：...
- 输出内容要求：...
```

Resolve journal aliases and official reader-visible surfaces during setup. A supplied schedule authorizes creating the requested recurring task unless the user explicitly asks for a preview only.

## Default report language

- Report title, section headings, field labels, coverage explanations, failure/source notes, and conclusions: use the user's conversation language. For Chinese-language users, use Chinese for all of these surrounding elements.
- Exact article title and journal name: preserve the publisher's original wording (normally English for the target journals); do not translate them into Chinese.
- Abstract and article summary: keep in English when the source abstract is English, unless the user explicitly requests another language.
- Publisher surface labels such as `ASAP Articles`, `Early View`, and `First Release`: preserve the publisher wording.
- If no abstract exists, report exactly `No abstract supplied by the journal`.
