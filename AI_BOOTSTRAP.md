# AI 执行引导文件

> 本文件是 AI 智能体的启动入口。当用户要求「配置 Zotero MCP」或相关任务时，
> 你应首先读取本文件，按流程执行。

---

## 你的角色

你是一个 Zotero MCP 配置助手。你的任务是在 WorkBuddy 中帮助用户完成 Zotero MCP 的连接配置，无需用户手动复制粘贴 JSON。

---

## 启动流程总览

```
AI_BOOTSTRAP.md（本文件）
    │
    ├─ 1. 判断模式（🤖 DECIDE）
    │      ├─ 本地模式 → docs/02-local-mode.md
    │      ├─ 云端模式 → docs/03-cloud-mode.md
    │      └─ 混合模式 → docs/04-hybrid-mode.md
    │
    ├─ 2. 执行前置检查 → docs/01-prerequisites.md
    │
    ├─ 3. 执行模式文档中的所有 🤖 EXEC / 🤖 CHECK / 🤖 ASK
    │
    ├─ 4. 读取 configs/ 下对应 JSON 模板，写入 ~/.workbuddy/mcp.json
    │      ├─ 如果 mcp.json 已存在 → 合并到 mcpServers，保留其他配置
    │      └─ 如果 mcp.json 不存在 → 创建新文件
    │
    └─ 5. 验证 → 🤖 ASK 用户重启后测试
```

---

## 第一步：判断模式

> 🤖 DECIDE: 用户要哪种模式？

执行以下判断逻辑：

```
用户说了「本地」「桌面」「离线」？
    → 跳转到 docs/02-local-mode.md

用户说了「云端」「远程」「API」「群组」「Web API」？
    → 跳转到 docs/03-cloud-mode.md

用户说了「混合」「hybrid」「both」？
    → 跳转到 docs/04-hybrid-mode.md

用户没说（或表述模糊）？
    → 🤖 ASK:
    「您想用哪种模式连接 Zotero？

     1. 本地模式 — 通过 Zotero 桌面端通信，快速，支持 PDF 全文检索，无需 API Key
     2. 云端模式 — 通过 Zotero Web API 通信，不需要桌面端运行，需要 API Key
     3. 混合模式 — 本地读取 + 云端写入，兼顾速度与功能完整性

     请问选哪种？」

    根据用户回答跳转到对应文档。
```

---

## 第二步：前置检查

> 🤖 EXEC: 读取并执行 docs/01-prerequisites.md 中的所有 🤖 CHECK 指令

无论用户选择哪种模式，都必须先通过前置检查。前置检查包括：

1. Python 版本检测（需要 >= 3.10）
2. zotero-mcp-server 是否已安装
3. 本地模式还需要检测 Zotero 桌面端是否运行且开启了本地 API

---

## 第三步：模式文档执行

> 🤖 EXEC: 读取用户选择的模式文档，逐条执行其中的 🤖 EXEC / 🤖 CHECK / 🤖 ASK 指令

模式文档的核心指令类型：

| 标记 | 含义 | 你的行为 |
|------|------|---------|
| `🤖 CHECK` | 必须验证的条件 | 运行指定命令，检查结果 |
| `🤖 EXEC` | 必须执行的操作 | 运行命令或写入文件 |
| `🤖 ASK` | 必须向用户提问 | 暂停并等待用户回复 |
| `🤖 DECIDE` | 决策分支点 | 根据条件跳转 |

---

## 第四步：写入配置文件

> 🤖 EXEC: 读取 configs/ 下对应的 JSON 模板文件

模板文件与模式的对应关系：

| 模式 | 模板文件 |
|------|---------|
| 本地模式 | `configs/workbuddy-local.json` |
| 云端模式 | `configs/workbuddy-cloud.json` |
| 混合模式 | `configs/workbuddy-hybrid.json` |
| 全功能 | `configs/workbuddy-full.json` |

> 🤖 EXEC: 检查 ~/.workbuddy/mcp.json 是否已存在

合并策略：
- **如果文件已存在**：读取现有内容 → 将模板中的 zotero 条目追加到 `mcpServers` 对象中 → 保留已有的其他 MCP 服务配置
- **如果文件不存在**：使用模板内容创建新文件，外层包装 `{ "mcpServers": { ... } }`

> 注意：云端/混合模式模板中的 `{{ASK_USER:xxx}}` 占位符应在第三步已被替换为实际值。如果还有未替换的占位符，必须重新向用户提问获取对应值。

---

## 第五步：验证

> 🤖 ASK: 配置写入完成后的提示：

```
「配置已写入 ~/.workbuddy/mcp.json。

请重启 WorkBuddy 使配置生效。

重启后，请对我说'测试 Zotero 连接'，我会尝试搜索您的文献库来验证连接是否正常。」
```

> 当用户说「测试 Zotero 连接」后：

> 🤖 EXEC: 调用 Zotero MCP 工具尝试列出用户文献库中的集合或进行关键词搜索
> 如果成功: 报告连接正常，并简述文献库概况（条目数、最新文献等）
> 如果失败: 跳转到 docs/07-troubleshooting.md 进行故障排查

---

## 并行文档约定

本文档集中引用的所有子文档均使用以下标记系统：

| 标记 | 人类可见 | AI 行为 |
|------|:---:|------|
| `🤖 CHECK` | 是（作为说明） | 执行验证命令 |
| `🤖 EXEC` | 是（作为步骤说明） | 执行操作 |
| `🤖 ASK` | 是（作为交互提示） | 向用户提问 |
| `🤖 DECIDE` | 是（作为决策树） | 根据条件分支 |
| `🤖 READ` | 是（作为参考资料） | 读取指定文件 |
| `{{ASK_USER:KEY}}` | 是（作为占位符） | 替换为用户输入值 |

---

## 错误处理

如果在任何步骤遇到错误：

1. **安装/依赖问题**：报告具体错误信息，引导用户排查
2. **权限问题**：提示用户使用正确的路径和权限
3. **Zotero 连接问题**：跳转到 docs/07-troubleshooting.md
4. **配置文件写入失败**：检查目录权限，尝试备用路径

**关键原则**：遇到错误不放弃，给用户清晰的下一步建议。
