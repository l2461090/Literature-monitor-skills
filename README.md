# Literature-monitor-skills

一个以“读者第一次能够在出版社官网看到文章”为标准的期刊监控 skill。它监控 `ASAP Articles`、`Early View`、`First Release`、`Articles in Press`、`Latest Articles` 等官方栏目，而不是仅根据 Crossref 的出版日期生成“最近七天”结果。

## 使用时需要提供的四项信息

```text
研究方向：
目标期刊：
定时任务：
文章内容范围：
```

说明：

1. **研究方向**：需要持续跟踪的领域、问题或主题。
2. **目标期刊**：准确的期刊白名单，不会自动把 `Nature` 扩展为整个 Nature Portfolio。
3. **定时任务**：频率、星期、时间和时区，例如“每周一 09:00，Asia/Shanghai”。
4. **文章内容范围**：论文需要包含的材料、体系、人群、机制、方法、结果或应用，以及需要排除的内容。

示例：

```text
研究方向：Supramolecular chemistry
目标期刊：Nature, Science, Nature Chemistry, Nature Materials, Nature Communications, Chem, Journal of the American Chemical Society, Angewandte Chemie International Edition, Advanced Materials
定时任务：每周一 09:00，Asia/Shanghai
文章内容范围：包含 molecular recognition、host–guest chemistry、self-assembly、supramolecular polymers、macrocycles、molecular cages、mechanically interlocked molecules、dynamic assemblies 和 functional supramolecular materials；排除仅偶然提及 self-assembly、但研究贡献与超分子机制无关的论文。
```

## 默认输出

- 报告标题、栏目、字段、覆盖说明和结论使用用户对话语言。
- 论文标题和期刊名保留出版社原文。
- 有英文摘要时，提供忠实的英文摘要概述和原始摘要链接。
- 若期刊没有摘要，明确写 `No abstract supplied by the journal`。
- 无法完整访问某个官方栏目时标记为部分覆盖，不把它写成“本周没有新论文”。

## 新论文的判定

首次运行会为各期刊当前读者可见栏目建立基线。后续运行以 DOI 或稳定出版社文章标识去重：本监控第一次在官方页面观察到的文章才算本周新增。文章后来从 Early View 进入正式卷期时，不会重复报告。

## 安装

将 `literature-monitor-skills` 文件夹放入 Codex skills 目录，然后使用 `$literature-monitor-skills`，或直接提出“设置目标期刊的每周最新论文监控”。定时运行需要宿主产品提供 recurring automation 或 scheduled task 能力。

## License

MIT License. See [LICENSE](LICENSE).
