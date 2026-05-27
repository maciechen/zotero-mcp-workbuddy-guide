# 03 · 云端模式配置

> 云端模式通过 Zotero Web API 进行通信。
> 优势：不需要运行 Zotero 桌面端，可远程访问。
> 要求：Zotero API Key + Library ID。

---

## 工作原理

```
WorkBuddy
  │  MCP Protocol (stdio)
  ▼
zotero-mcp server
  │  HTTPS (api.zotero.org)
  ▼
Zotero Web API
  │
  ├── 文献元数据
  ├── 标签与集合
  ├── 附件（需 WebDAV）
  └── 群组文献库
```

---

## 配置步骤

### Step 1: 获取 Zotero API Key

> 🤖 ASK: 「云端模式需要 Zotero API Key。请按以下步骤操作：

>   1. 访问 https://www.zotero.org/settings/keys
>      （需登录 Zotero 账号）
>   2. 点击 **'Create New Private Key'**
>   3. 根据需要勾选权限：
>      - **Allow library access**（必需）
>      - Allow notes access（如需读写笔记）
>      - Allow write access（如需添加/修改文献）
>   4. 点击 **'Save Key'**
>   5. 复制生成的 API Key（格式：一串字母+数字）

>   在同一页面顶部可以看到您的 **User ID**（纯数字）。

>   请将 API Key 和 User ID 提供给我。」

### Step 2: 安装 zotero-mcp-server

> 🤖 CHECK: 确认已安装: `pip show zotero-mcp-server`
> 如果未安装: 🤖 EXEC: `pip install zotero-mcp-server`

### Step 3: 配置 WorkBuddy

> 🤖 READ: `configs/workbuddy-cloud.json`

> 模板中包含 `{{ASK_USER:ZOTERO_API_KEY}}` 和 `{{ASK_USER:ZOTERO_LIBRARY_ID}}` 占位符。
> 请将 Step 1 中用户提供的值替换这些占位符。

> 🤖 EXEC: 将以下内容中的占位符替换为实际值：

```json
{
  "zotero": {
    "command": "zotero-mcp",
    "args": [],
    "env": {
      "ZOTERO_API_KEY": "替换为实际的 API Key",
      "ZOTERO_LIBRARY_ID": "替换为实际的 User ID",
      "ZOTERO_LIBRARY_TYPE": "user"
    },
    "disabled": false
  }
}
```

> 🤖 EXEC: 检查 ~/.workbuddy/mcp.json 是否存在

**如果文件已存在：**
> 🤖 EXEC: 读取现有内容 → 将替换后的 zotero 条目追加到 mcpServers 对象中 → 保留已有配置

**如果文件不存在：**
> 🤖 EXEC: 创建新文件，写入替换后的完整配置

> 🤖 EXEC: 写入文件 ~/.workbuddy/mcp.json

> ⚠️ **安全提醒（必须对用户说）**：
> 「API Key 已写入 mcp.json。该文件仅存储在您的本地计算机上，不会被上传。
> 请勿将含 API Key 的配置文件分享给他人或提交到公开仓库。」

### Step 4: 可选 · WebDAV 附件下载

> 如果用户需要直接通过 WorkBuddy 下载论文附件：
> 🤖 ASK: 「是否需要配置 WebDAV 以支持直接下载 PDF 附件？
>   如果不需要，跳过此步骤。」

**如果需要：**

```json
{
  "zotero": {
    "command": "zotero-mcp",
    "args": [],
    "env": {
      "ZOTERO_API_KEY": "...",
      "ZOTERO_LIBRARY_ID": "...",
      "ZOTERO_LIBRARY_TYPE": "user",
      "ZOTERO_WEBDAV_URL": "https://your-webdav-server.com/zotero/",
      "ZOTERO_WEBDAV_USERNAME": "your-username",
      "ZOTERO_WEBDAV_PASSWORD": "your-password"
    },
    "disabled": false
  }
}
```

### Step 5: 验证配置

> 🤖 ASK: 「配置已写入 ~/.workbuddy/mcp.json。请执行以下操作：
>
>   1. **重启 WorkBuddy** 使配置生效
>   2. 重启后对我说：**「测试 Zotero 连接」**
>
>   我会尝试搜索您的文献库来验证连接。」

> 用户说「测试 Zotero 连接」后:
> 🤖 EXEC: 尝试调用 Zotero MCP 工具获取用户文献库信息
> 如果成功: 报告连接正常 + 文献库概况
> 如果失败: 跳转至 docs/07-troubleshooting.md

---

## 功能能力

| 能力 | 云端模式 |
|------|:---:|
| 关键词搜索文献 | ✓ |
| 语义搜索文献 | 需额外配置（见 docs/05） |
| 读取文献元数据 | ✓ |
| 获取 PDF 全文 | ✗（仅元数据） |
| 提取 PDF 批注 | 有限支持 |
| 按标签/集合浏览 | ✓ |
| 创建/管理笔记 | ✓ |
| 写入标签 | ✓ |
| 修改元数据 | ✓ |
| 通过 DOI 添加文献 | ✓ |
| 群组文献库 | ✓ |
| 附件下载 | 需配置 WebDAV |
| Scite 引用统计 | 需额外配置（见 docs/06） |

---

## 使用示例

配置完成后，在 WorkBuddy 中尝试：

```
「列出我的 Zotero 群组库中最近添加的文献」
「搜索 Zotero 中与 ESG 投资相关的论文」
「给我的文献添加标签：重要论文」
```

---

## 环境变量

| 变量 | 值 | 必需 |
|------|-----|:---:|
| `ZOTERO_API_KEY` | 从 zotero.org 获取 | 是 |
| `ZOTERO_LIBRARY_ID` | User ID 或 Group ID | 是 |
| `ZOTERO_LIBRARY_TYPE` | `user` 或 `group` | 是 |
| `ZOTERO_WEBDAV_URL` | WebDAV 服务器地址 | 否 |
| `ZOTERO_WEBDAV_USERNAME` | WebDAV 用户名 | 否 |
| `ZOTERO_WEBDAV_PASSWORD` | WebDAV 密码 | 否 |

---

## 群组库配置

> 如果用户提到群组库：
> 🤖 ASK: 「请提供群组 ID（在 zotero.org 群组页面 URL 中可见）。」

将环境变量调整为：
```json
"ZOTERO_LIBRARY_ID": "群组ID",
"ZOTERO_LIBRARY_TYPE": "group"
```
