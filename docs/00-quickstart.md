# 00 · 快速开始

> 面向人类：如果你想手动配置，本文档是最快的路径。如果想让 AI 帮你配，只需在 WorkBuddy 中说「配置 Zotero MCP」，AI 会自动读取 `AI_BOOTSTRAP.md` 完成全流程。

---

## 本地模式

```bash
# 1. 安装
pip install zotero-mcp-server

# 2. 确认 Zotero 桌面端正在运行，且已开启本地 API
#    Zotero → Edit → Settings → Advanced
#    → 勾选 "Allow other applications to communicate with Zotero"

# 3. 配置 WorkBuddy
#    将 configs/workbuddy-local.json 的内容
#    写入 ~/.workbuddy/mcp.json

# 4. 重启 WorkBuddy

# 5. 验证
#    在 WorkBuddy 中说：「测试 Zotero 连接」
```

---

## 云端模式

```bash
# 1. 获取 API Key
#    登录 https://www.zotero.org/settings/keys
#    创建新 Key，勾选 "Allow library access"
#    记下 API Key 和 User ID

# 2. 安装
pip install zotero-mcp-server

# 3. 配置 WorkBuddy
#    将 configs/workbuddy-cloud.json 的内容写入 ~/.workbuddy/mcp.json
#    替换 ZOTERO_API_KEY 和 ZOTERO_LIBRARY_ID 为你的值

# 4. 重启 WorkBuddy

# 5. 验证
#    在 WorkBuddy 中说：「测试 Zotero 连接」
```

---

## 我该选哪种？

- **本地模式**适合：你有 Zotero 桌面版，电脑在身边，需要 PDF 全文检索
- **云端模式**适合：你远程办公、不想装/开 Zotero 桌面端、操作群组文献库
- **混合模式**适合：既要本地速度+全文检索，又需要完整的标签/元数据写操作

详细对比见 [README](../README.md#两种模式对比)。
