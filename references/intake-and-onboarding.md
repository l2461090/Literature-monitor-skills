# Intake and onboarding

Read this file when setting up or materially changing a monitor.

## The four required decisions

| Decision | What to collect | How it is used |
|---|---|---|
| Research direction | A topic, research question, or one-to-two-sentence scope statement | Creates the semantic topic rule and retrieval concepts |
| Target journals | Exact journal titles or unambiguous aliases | Creates the fixed journal whitelist and publisher-surface routes |
| Schedule | Frequency, day, local time, and timezone | Creates or updates the recurring task |
| Article-content requirements | Required or preferred systems, materials, populations, mechanisms, methods, outcomes, applications, and explicit exclusions | Controls abstract-level relevance screening |

The fourth decision describes what a qualifying article must substantively contain. It is not the same as choosing report columns. Translate it into `topic.include_concepts`, `topic.exclude_concepts`, and `topic.notes` without requiring literal keyword matches.

## Recommended user prompt

When none of the four decisions is known, ask the user to complete this compact template in one message:

```text
研究方向：
目标期刊：
定时任务：
文章内容范围：
```

Equivalent English template:

```text
Research direction:
Target journals:
Schedule:
Article content scope:
```

Natural-language answers are valid. Do not force the template when the user has already supplied usable information. Ask only for missing or materially ambiguous decisions.

## Defaults and interpretation

- Exact journal titles form a whitelist. A publisher family or phrase such as `Nature journals` must be enumerated before coverage can be claimed.
- When a weekly schedule lacks a day or time, assume Monday at 09:00 in the user's current timezone and explicitly show the assumption.
- Default content types are research articles and review articles. Exclude editorials, news, corrections, obituaries, letters to the editor, and book reviews unless requested.
- Default relevance mode is direct semantic relevance. Put plausible but non-central papers in an adjacent/borderline section rather than silently mixing them into the direct list.
- A content request may be broad (`all work on supramolecular chemistry`) or constrained (`only host–guest recognition involving macrocycles; exclude biomedical delivery`). Preserve both inclusions and exclusions.
- If the user asks to preview the configuration or report format before activation, create a preview and do not create or modify the recurring task until the user confirms.

## Confirmation summary

Before or while saving setup, present the four decisions in a compact summary so mistakes are visible:

```markdown
- 研究方向：...
- 目标期刊：...
- 定时任务：...
- 文章内容范围：...
```

Resolve journal aliases and official reader-visible surfaces during setup. A supplied schedule authorizes creating the requested recurring task unless the user explicitly asks for a preview only.

## Default report language

- Report title, section headings, field labels, coverage explanations, failure notes, and conclusions: use the user's conversation language.
- Exact article title: preserve the publisher's source title.
- Journal name: preserve the canonical source name.
- Abstract summary: English when an English abstract is available, unless the user explicitly requests another language.
- Publisher surface labels such as `ASAP Articles`, `Early View`, and `First Release`: preserve the publisher wording.
- If no abstract exists, report exactly `No abstract supplied by the journal`.
