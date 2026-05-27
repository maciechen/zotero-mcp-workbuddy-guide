# 06 · Scite 引用智能

> 在 Zotero 文献检索中集成 Scite 的引用分析和撤稿预警。
> 无需 Scite 付费账号即可使用。

---

## 什么是 Scite？

Scite 是一个学术引用分析平台，能够告诉你一篇论文的引用是**支持性的**（supporting）、**对比性的**（contrasting）还是**提及性的**（mentioning），并标记是否存在**撤稿**或**更正**通知。

---

## 安装

> 🤖 EXEC: `pip install "zotero-mcp-server[scite]"`

---

## 配置

不需要额外配置。安装后，Zotero MCP 工具会自动提供 Scite 相关功能：

- `scite_enrich_item` — 获取单篇论文的 Scite 引用报告
- `scite_check_retractions` — 批量检查文献库中的撤稿与更正
- `scite_enrich_search` — 搜索结果中附带 Scite 引用数据

---

## 使用示例

```
「这篇论文的引用情况如何？有多少支持性引用和反对性引用？」
「检查我 Zotero 文献库中是否有论文被撤稿」
「搜索 Zotero 中关于 ESG 的文献，并报告每篇的 Scite 引用统计」
「给这篇论文添加 Scite 引用报告到 Zotero 笔记中」
```

---

## 功能能力

| 能力 | 说明 |
|------|------|
| 引用计数 | 支持性 / 对比性 / 提及性引用 |
| 撤稿预警 | 标记被撤稿或更正的论文 |
| 批量检查 | 检测整个文献库中的撤稿 |
| 搜索增强 | 搜索结果附带引用统计 |

---

## 注意事项

- Scite 的引用统计基于其自身的数据库，覆盖率因领域而异
- 较新的论文或小众领域的论文可能引用数据较少
- 无需 Scite 账号或 API Key
