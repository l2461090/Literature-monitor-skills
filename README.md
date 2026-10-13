# Literature-monitor-skills

> A scheduled, reader-visible literature monitor for research groups and individual researchers.

面向课题组、研究生、博士后与教师的定时文献监控 skill。它会从你指定期刊的出版社官网发现刚刚上线、读者已经可以找到并打开文章页的相关论文，生成去重的周报，减少逐个打开期刊网页检索的时间。

## 为什么需要它？

许多研究人员每周都要反复查看多个顶刊：有的文章先以 `ASAP Articles`、`Early View`、`First Release`、`Articles in Press` 或 `Latest Articles` 上线，等到正式卷期或数据库日期更新时，往往已经错过了最早可读的窗口。

这个 skill 将这件重复工作变为定时任务：只跟踪你给出的研究方向与期刊白名单，并以出版社官网出现稳定文章页作为“读者可见”的依据，而不是把 Crossref 的在线出版日期或固定七天时间窗当作唯一标准。

## 适合谁？

- **课题组**：建立共享的每周文献雷达，及时发现本领域顶刊的新工作。
- **研究生与博士后**：减少手工刷网页和重复检索，把时间留给阅读与研究。
- **教师、PI 与独立研究者**：按自己的研究方向和目标期刊持续跟踪，不受数据库索引滞后的影响。

## 推荐搭配：用 Codex 做文献监控

推荐将本 skill 与 **Codex** 搭配使用，把研究方向、目标期刊和严格时间范围，变成有来源、可核验的定时文献周报。

- **按方向精准筛选**：围绕你指定的研究主题与期刊检索，结合摘要判断相关性，而不只是匹配标题关键词。
- **真实来源，逐篇核验**：本 skill 要求正式结果具有出版社官网可见性证据，并核对标题、DOI 或稳定标识；每篇附上来源链接，方便回到原文复核。
- **定时追踪，减少重复劳动**：配合 Codex 的定时任务，持续跟踪新上线文章、去重并整理报告，把时间留给阅读与研究。

这里推荐的是“检索 + 核验 + 定时跟踪”的工作方式，并非承诺 AI 永不出错或绝不遗漏。官网受限、日期不明或摘要缺失时，应明确标注，不把未经核验的候选混入正式结果。定时任务的运行条件见 [OpenAI 官方说明](https://learn.chatgpt.com/docs/automations)。

### GPT/Codex 会员开通指南

> [!TIP]
> **GPT/Codex 开通指南 2026：了解 ChatGPT 会员与 Codex 使用方案**
>
> 正规充值平台 **[ai66.org](https://ai66.org)**（平台自述）
>
> ✅ **平台说明支持支付宝/微信**　｜　✅ **可查看套餐与开通教程**
>
> ### 👉 [前往 ai66.org 了解 GPT/Codex 开通方案](https://ai66.org)
>
> **推广说明**：ai66.org 的理念是“世界顶级 AI，国内人人皆可畅享”。通过官方合规支付链路开通会员，不触碰你的账号密码，不留后门。

## 它会做什么？

- 在指定期刊的官方读者可见栏目或文章页中扫描新上线论文，并遍历栏目分页。
- 根据 DOI、稳定出版商文章标识或官方 URL 建立首次观察记录，避免同一篇文章在 Early View 与正式卷期之间重复出现。
- 仅纳入与研究方向相关的文章；任何纳入/排除边界都属于研究方向本身。
- 提供严格检索时间范围：可选“最近 N 个自然日”或明确起止日期；只有出版社官网显示的首次在线日期落在该范围内的文章才会进入主结果。
- 根据你的输出内容要求，生成论文标题、期刊、出版社栏目状态、首次观察时间、官网首次在线日期（若有）、DOI/稳定标识、英文摘要、结论或其他指定字段。
- 官方栏目无法完整访问时，明确标记为 `partial coverage`；不会把扫描失败误报为“没有新论文”。

> **Reader-visible first**：全文可以需要订阅；只要普通读者能在出版社官网发现并打开可识别身份的文章页，即视为可见。

## 60 秒配置

使用时提供以下四项信息：

```text
研究方向：
目标期刊：
定时任务：
严格检索时间范围：
输出内容要求：
```

1. **研究方向**：需要持续跟踪的领域、问题或主题。
2. **目标期刊**：准确的期刊白名单；不会自动把 `Nature` 扩展为整个 Nature Portfolio。
3. **定时任务**：频率、星期、时间和时区，例如“每周一 09:00，Asia/Shanghai”。
4. **严格检索时间范围**：`最近 N 个自然日`或明确起止日期，必须填写。例如“最近 7 个自然日”或“2026-08-25 至 2026-08-31”；两端日期均包含在内。
5. **输出内容要求**：每篇文章需要给出的信息，例如标题、DOI、英文摘要、结论、方法、作者、日期或链接。

示例：

```text
研究方向：Supramolecular chemistry
目标期刊：Nature, Science, Nature Chemistry, Nature Materials, Nature Communications, Chem, Journal of the American Chemical Society, Angewandte Chemie International Edition, Advanced Materials
定时任务：每周一 09:00，Asia/Shanghai
严格检索时间范围：最近 7 个自然日
输出内容要求：标题、DOI、英文原摘要（若复用条件不允许则给忠实英文摘要概述并附原文链接）、官网首次在线日期和可见性来源。
```

## 默认周报

- 中文用户的报告标题、栏目标题、字段名、覆盖/来源说明与结论全部使用中文；论文标题与期刊名保留出版社英文原文，英文摘要与论文概述也保持英文。
- 有英文摘要且复用条件允许时，提供英文原摘要；否则提供忠实的英文摘要概述和原始摘要链接。
- 若期刊没有摘要，明确写 `No abstract supplied by the journal`，不会补写或虚构摘要。
- 首次运行建立基线；后续仅报告本监控首次在官方页面观察到的文章。文章后来进入正式卷期不会重复报告。

## 安装与调用

克隆本仓库后，将它放入你的 AI 助手所使用的 skills 目录。例如，在 Codex 中可放到 `~/.codex/skills/literature-monitor-skills`，随后使用 `$literature-monitor-skills`，或直接提出“设置目标期刊的每周最新论文监控”。

```bash
git clone https://github.com/l2461090/Literature-monitor-skills.git
```

定时运行需要宿主产品提供 recurring automation 或 scheduled task 能力；skill 会在可用时建立监控配置、历史状态与每周 Markdown 周报。

## English summary

Literature-monitor-skills is built for labs and individual researchers who need a reliable weekly view of newly reader-visible papers in a defined field and a defined set of journals. It scans publisher-controlled surfaces such as ASAP Articles and Early View, records the first time a stable article identity is observed, and delivers a deduplicated digest with the original English abstract when the journal supplies one.

To start, provide: **research direction**, **exact target journals**, **schedule (with time zone)**, a **strict time window**, and **report-content requirements**. A strict window is either the last N calendar days or an inclusive date range; a paper must have an official publisher-displayed online date inside it. The research direction determines relevance; report-content requirements specify which fields to deliver. The monitor treats publisher visibility as the evidence for a new paper; metadata indexes cannot replace the official date or visibility evidence.

## License

MIT License. See [LICENSE](LICENSE).
