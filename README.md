# 为你的WorkBuddy接入Zotero MCP · 配置指南

> 基于 [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)（v0.4.1, 3.4k+ stars）
> 专为 WorkBuddy 用户设计 · 一份文档，人机共用

---

## 这是什么？

将 Zotero 文献库接入 WorkBuddy，用自然语言对话完成文献搜索、批注整理、引文管理、文献综述草稿等任务。本仓库提供**完整的中文配置指南**，支持本地模式和云端模式，且设计为 **AI 可自主执行**——你只需一句话，AI 自动完成配置。

---

## 配置方法

### 方式一：交给 AI 自动配置（推荐）

在 WorkBuddy 中说：

> git clone https://github.com/maciechen/zotero-mcp-workbuddy-guide.git 读取这个仓库，帮我配置 Zotero MCP

AI 会自动读取 `AI_BOOTSTRAP.md`，按流程检查环境、安装依赖、写入配置。

### 方式二：手动配置

1. 阅读 [前置条件检查](docs/01-prerequisites.md)
2. 根据你的场景选择对应文档
3. 复制 [configs/](configs/) ，粘贴到 `~/.workbuddy/mcp.json`
访问路径： `WorkBuddy / 连接器 / 自定义连接器 / 配置 MCP`
<img width="647" height="703" alt="image" src="https://github.com/user-attachments/assets/2abb12e9-712a-42ac-95c9-469906b054fa" />

---

## 我该选哪种模式？

| 场景 | 推荐模式 | 文档 |
|------|---------|------|
| 我有 Zotero 桌面版，电脑就在跟前 | **本地模式** | [docs/02-local-mode.md](docs/02-local-mode.md) |
| 我远程办公，不想开 Zotero 桌面端 | **云端模式** | [docs/03-cloud-mode.md](docs/03-cloud-mode.md) |
| 既要本地速度和全文检索，又要完整写权限 | **混合模式** | [docs/04-hybrid-mode.md](docs/04-hybrid-mode.md) |

---

## 两种模式对比

| 对比维度 | 本地模式 | 云端模式 |
|----------|:-------:|:-------:|
| 需要 Zotero 桌面端运行 | 是 | 否 |
| 需要 Zotero API Key | 否 | 是 |
| PDF 全文检索 | 支持 | 不支持 |
| PDF 批注提取 | 完整支持 | 有限支持 |
| 写入标签/元数据 | 部分受限 | 完整支持 |
| 语义搜索 | 可选扩展 | 可选扩展 |
| 适用场景 | 桌面深度研究 | 远程/移动/群组库 |

---

## 项目结构

```
├── AI_BOOTSTRAP.md        ← AI 自动配置的启动入口
├── README.md              ← 你正在看的文件（人类入口）
├── configs/               ← 纯 JSON 配置模板（AI 直接读取写入）
│   ├── workbuddy-local.json
│   ├── workbuddy-cloud.json
│   ├── workbuddy-hybrid.json
│   └── workbuddy-full.json
├── docs/                  ← 双栖文档（人读 + AI 执行）
│   ├── 00-quickstart.md
│   ├── 01-prerequisites.md
│   ├── 02-local-mode.md
│   ├── 03-cloud-mode.md
│   ├── 04-hybrid-mode.md
│   ├── 05-semantic-search.md
│   ├── 06-scite.md
│   └── 07-troubleshooting.md
├── scripts/               ← 环境检测与验证脚本
│   ├── check-env.py
│   └── verify-zotero-mcp.py
├── LICENSE
└── CHANGELOG.md
```

---

## 补充：语义搜索 & Scite 扩展

- [语义搜索配置](docs/05-semantic-search.md)：启用向量相似度搜索，通过自然语言跨所有文献找到最相关的内容
- [Scite 引用智能](docs/06-scite.md)：获取每篇论文的引用统计与撤稿预警

---

## 相关资源

| 资源 | 链接 |
|------|------|
| 上游项目 | [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp) |
| LibGuide | [AI 文献管理](https://ceibs.libguides.com/reference_management/ai) |
| WorkBuddy | [安装指南](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Installation-Win-Guide) |

---

## 文档约定

本文档中的标记符号：

- `🤖 EXEC` — AI 智能体必须执行的操作
- `🤖 CHECK` — AI 智能体必须验证的条件
- `🤖 ASK` — AI 智能体必须向用户提问
- `🤖 DECIDE` — AI 智能体的决策分支点
- `{{ASK_USER:xxx}}` — 需替换为用户提供的值

---

*本仓库基于 [54yyyu/zotero-mcp](https://github.com/54yyyu/zotero-mcp)（MIT License）创建。*
