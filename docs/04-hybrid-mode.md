# 04 · 混合模式配置

> 混合模式 = 本地 API 读取 + Web API 写入。
> 适合既需要本地速度（全文检索、批注提取），又需要完整写操作（标签、元数据修改）的用户。

---

## 工作原理

```
WorkBuddy
  │  MCP Protocol (stdio)
  ▼
zotero-mcp server
  │
  ├── 读取 → Zotero Desktop (localhost:23119) → zotero.sqlite
  │          文献搜索、元数据、PDF全文、批注——速度快
  │
  └── 写入 → Zotero Web API (api.zotero.org)
             标签、元数据修改、添加文献——功能完整
```

---

## 前置条件

混合模式需要**同时满足**本地模式和云端模式的前置条件：

| 条件 | 用途 |
|------|------|
| Zotero 7+ 桌面端运行，本地 API 已开启 | 本地读取 |
| Zotero API Key | 云端写入 |
| Zotero User ID | 云端写入 |

> 请确保 docs/01-prerequisites.md 中所有检查均已通过。

---

## 配置步骤

### Step 1: 环境检测

> 🤖 EXEC: 确认以下两项均已通过：

> 🤖 CHECK: Zotero 桌面端是否运行？
> `curl -s http://localhost:23119/connector/ping`
> 如果失败: 🤖 ASK 「请启动 Zotero 并开启本地 API（Edit → Settings → Advanced → Allow other applications...）」

### Step 2: 获取 API Key

> 如果用户尚未提供 API Key:
> 🤖 ASK: 「混合模式需要 Zotero API Key 用于写操作。请按以下步骤获取：

>   1. 访问 https://www.zotero.org/settings/keys
>   2. 创建新 Key，务必勾选 **Allow write access**
>   3. 复制 API Key 和 User ID 提供给我。」

### Step 3: 配置 WorkBuddy

> 🤖 READ: `configs/workbuddy-hybrid.json`

> 🤖 EXEC: 将模板中 `{{ASK_USER:ZOTERO_API_KEY}}` 和 `{{ASK_USER:ZOTERO_LIBRARY_ID}}` 替换为用户提供的值

> 🤖 EXEC: 写入 ~/.workbuddy/mcp.json（合并/新建）

### Step 4: 验证配置

> 🤖 ASK: 「混合模式配置已写入。请重启 WorkBuddy，然后说'测试 Zotero 连接'。」

> 用户测试后:
> 🤖 EXEC: 尝试读取文献库集合（验证本地）→ 尝试修改一个标签（验证云端写入）
> 两者都成功: 报告混合模式配置正常
> 任一失败: 跳转至 docs/07-troubleshooting.md

---

## 功能能力

| 能力 | 混合模式 |
|------|:---:|
| 关键词搜索文献 | ✓（本地） |
| 语义搜索文献 | 需额外配置 |
| 读取文献元数据 | ✓（本地） |
| 获取 PDF 全文 | ✓（本地） |
| 提取 PDF 批注 | ✓（本地） |
| 按标签/集合浏览 | ✓（本地） |
| 创建/管理笔记 | ✓ |
| 写入标签 | ✓（云端） |
| 修改元数据 | ✓（云端） |
| 通过 DOI 添加文献 | ✓（云端） |
| 群组文献库 | ✓（云端） |

---

## 环境变量

| 变量 | 值 | 必需 |
|------|-----|:---:|
| `ZOTERO_LOCAL` | `true` | 是 |
| `ZOTERO_API_KEY` | Zotero API Key | 是 |
| `ZOTERO_LIBRARY_ID` | User ID 或 Group ID | 是 |
| `ZOTERO_LIBRARY_TYPE` | `user` 或 `group` | 是 |
