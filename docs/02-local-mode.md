# 02 · 本地模式配置

> 本地模式通过 Zotero 桌面端的本地 HTTP API 进行通信。
> 优势：速度快、无需网络、支持 PDF 全文检索和批注提取。
> 要求：Zotero 7+ 桌面端必须运行。

---

## 工作原理

```
WorkBuddy
  │  MCP Protocol (stdio)
  ▼
zotero-mcp server
  │  HTTP (localhost:23119)
  ▼
Zotero Desktop (zotero.sqlite)
  │
  ├── 文献元数据
  ├── PDF 全文
  ├── 批注与笔记
  └── 标签与集合
```

---

## 配置步骤

### Step 1: 环境检测

> 已完成 docs/01-prerequisites.md 中的所有检查？继续。
> 如果尚未完成，🤖 EXEC: 退回 docs/01-prerequisites.md 完成检查。

### Step 2: 安装 zotero-mcp-server

> 🤖 CHECK: 确认已安装: `pip show zotero-mcp-server`
> 如果未安装: 🤖 EXEC: `pip install zotero-mcp-server`

推荐同时安装 PDF 处理扩展（用于批注提取和 PDF 大纲）：

> 🤖 ASK: 「建议安装 PDF 处理扩展以支持批注和 PDF 大纲提取，是否安装？
>  如果不需要，可以跳过。」
> 如果用户同意: 🤖 EXEC: `pip install "zotero-mcp-server[pdf]"`

### Step 3: 配置 WorkBuddy

> 🤖 READ: `configs/workbuddy-local.json`

> 🤖 EXEC: 检查 ~/.workbuddy/mcp.json 是否存在

**如果文件已存在：**
> 🤖 EXEC: 读取现有内容 → 将 configs/workbuddy-local.json 中 zotero 条目
> 追加到 mcpServers 对象中 → 保留已有 MCP 服务配置

**如果文件不存在：**
> 🤖 EXEC: 创建新文件，内容如下：

```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": [],
      "env": {
        "ZOTERO_LOCAL": "true"
      },
      "disabled": false
    }
  }
}
```

> 🤖 EXEC: 写入文件 ~/.workbuddy/mcp.json

### Step 4: 验证配置

> 🤖 ASK: 「配置已写入 ~/.workbuddy/mcp.json。请执行以下操作：
>
>   1. **重启 WorkBuddy** 使配置生效
>   2. 重启后对我说：**「测试 Zotero 连接」**
>
>   我会尝试搜索您的文献库来验证连接。」

> 用户说「测试 Zotero 连接」后:
> 🤖 EXEC: 尝试调用 Zotero MCP 工具来获取用户文献库中的集合信息
> 如果成功: 报告连接正常 + 文献库概况
> 如果失败: 跳转至 docs/07-troubleshooting.md

---

## 功能能力

| 能力 | 本地模式 |
|------|:---:|
| 关键词搜索文献 | ✓ |
| 语义搜索文献 | 需额外配置（见 docs/05） |
| 读取文献元数据 | ✓ |
| 获取 PDF 全文 | ✓ |
| 提取 PDF 批注 | ✓（需 [pdf] 扩展） |
| PDF 大纲提取 | ✓（需 [pdf] 扩展） |
| 按标签/集合浏览 | ✓ |
| 创建/管理笔记 | ✓ |
| 写入标签 | ✗（需混合模式） |
| 修改元数据 | ✗（需混合模式） |
| 通过 DOI 添加文献 | 部分支持 |
| Scite 引用统计 | 需额外配置（见 docs/06） |

---

## 使用示例

配置完成后，在 WorkBuddy 中尝试：

```
「搜索我的 Zotero 中与数字化转型相关的文献」
「列出我最近一周添加的文献」
「提取这篇论文的 PDF 批注并整理成笔记」
「在我的 Zotero 中搜索标签为 ESG 的文献，生成综述草稿」
```

---

## 环境变量

| 变量 | 值 | 必需 |
|------|-----|:---:|
| `ZOTERO_LOCAL` | `true` | 是 |
| `ZOTERO_DB_PATH` | 自定义 zotero.sqlite 路径 | 否 |
