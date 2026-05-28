# 01 · 前置条件检查

> 本文档列出 Zotero MCP 的所有前置条件。AI 智能体请执行所有 `🤖 CHECK` 指令。
> 人类用户请逐项确认。

---

## 1. Python 环境

> Zotero MCP 是一个 Python 工具包，需要 Python 3.10+

> 🤖 CHECK: 运行 `python --version`
> 期望: 输出版本号 >= 3.10
> 🤖 如果失败: 🤖 ASK 「需要安装 Python 3.10+，请访问 https://www.python.org/downloads/ 下载安装。
>  安装时务必勾选'Add python.exe to PATH'，确保python已被添加进PATH。
>  安装完成后请告诉我，我会继续检测。」

**手动确认：**
```bash
python --version
# 应输出类似: Python 3.14.4
```

---

## 2. zotero-mcp-server 安装

> 🤖 CHECK: 运行 `pip show zotero-mcp-server`
> 期望: 输出版本信息
> 🤖 如果失败: 🤖 EXEC: `pip install zotero-mcp-server`
> 如果安装也失败: 🤖 ASK 「pip 安装失败，请检查网络连接后手动运行：pip install zotero-mcp-server」

**手动确认：**
```bash
pip install zotero-mcp-server
# 安装后验证:
pip show zotero-mcp-server
```

可选扩展（按需安装）：

| 扩展 | 安装命令 | 用途 |
|------|---------|------|
| 语义搜索 | `pip install "zotero-mcp-server[semantic]"` | 向量相似度搜索（需 ChromaDB） |
| PDF 处理 | `pip install "zotero-mcp-server[pdf]"` | PDF 大纲与 EPUB 批注 |
| Scite 引用 | `pip install "zotero-mcp-server[scite]"` | 引用统计与撤稿预警 |
| 全部功能 | `pip install "zotero-mcp-server[all]"` | 一次性安装所有扩展（推荐） |

---

## 3. Zotero 桌面端（仅本地模式 & 混合模式）

> 仅在用户选择本地模式或混合模式时才检查此项

> 🤖 CHECK: 运行 `curl -s http://localhost:23119/connector/ping`
> 如果命令不可用（Windows 无 curl），使用 PowerShell: `Invoke-WebRequest -Uri http://localhost:23119/connector/ping -UseBasicParsing -TimeoutSec 3`
> 期望: 非空响应
> 🤖 如果失败: 🤖 ASK 「请确认以下两项：
>   1. Zotero 7 桌面端是否已启动？
>   2. 是否已开启本地 API？（Zotero → Edit → Settings → Advanced
>      → 勾选'Allow other applications to communicate with Zotero'）
>   请完成后告诉我。」

**手动确认：**
1. 确保 Zotero 7+ 桌面端已启动
2. 打开 `Edit → Settings → Advanced`（编辑 → 设置 → 高级）
3. 勾选 **"Allow other applications to communicate with Zotero"**
4. 验证：浏览器访问 `http://localhost:23119/connector/ping` 应返回 `{}` 或类似响应

---

## 4. Zotero API Key（仅云端模式 & 混合模式）

> 仅在用户选择云端模式或混合模式时才检查此项

> 🤖 ASK: 「云端模式需要 Zotero API Key。请按以下步骤获取：

>   1. 访问 https://www.zotero.org/settings/keys
>   2. 点击 'Create New Private Key'
>   3. 勾选 'Allow library access' 及相关权限
>   4. 点击 'Save Key'
>   5. 复制生成的 API Key（一串字母数字）
>   6. 在同一页面找到您的 User ID（纯数字）

>   请将 API Key 和 User ID 提供给我。」

**手动获取：**
1. 登录 [zotero.org](https://www.zotero.org/)
2. 进入 [Settings → Feeds/API](https://www.zotero.org/settings/keys)
3. 创建新 Key，勾选所需权限
4. 记录 API Key 和 User ID（页面顶部可见）

---

## 5. WorkBuddy

> 🤖 CHECK: 检查 ~/.workbuddy/mcp.json 是否已存在
> 如果存在: 记录现有内容，后续追加 zotero 配置时不覆盖已有 MCP 服务
> 如果不存在: 将在配置步骤中自动创建

**手动确认：**
确认你的 WorkBuddy 已正确安装并可正常使用。

---

## 检查清单

AI 智能体请使用以下清单追踪进度：

```
[ ] Python >= 3.10 已安装
[ ] zotero-mcp-server 已安装
[ ] [本地/混合] Zotero 桌面端运行中，本地 API 已开启
[ ] [云端/混合] Zotero API Key 已获取
[ ] [云端/混合] Zotero User ID 已记录
[ ] WorkBuddy mcp.json 已定位
```

所有项目通过后，进入模式文档继续配置。
