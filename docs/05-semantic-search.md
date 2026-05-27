# 05 · 语义搜索配置

> 语义搜索启用以自然语言进行跨文献相似度搜索，无需精确匹配关键词。
> 例如：「找跟这篇论文方法论最相似的研究」——AI 会通过向量相似度找到最相关内容。

---

## 工作原理

```
zotero-mcp
  │
  ├── ChromaDB（向量数据库）
  │    存储所有文献的向量嵌入
  │
  └── Embedding Model（嵌入模型）
       └── 默认: all-MiniLM-L6-v2（本地运行，无需 API Key）
       └── 可选: OpenAI text-embedding-3-small
       └── 可选: Google Gemini embedding-001
```

---

## 安装

> 🤖 EXEC: `pip install "zotero-mcp-server[semantic]"`

这会安装 ChromaDB 和 sentence-transformers（用于本地嵌入模型）。

---

## 构建语义搜索数据库

安装后需要构建向量数据库：

> 🤖 EXEC: `zotero-mcp update-db`

可选参数：

| 命令 | 说明 |
|------|------|
| `zotero-mcp update-db` | 仅元数据（快速） |
| `zotero-mcp update-db --fulltext` | 含全文提取（较慢，更全面） |
| `zotero-mcp update-db --force-rebuild` | 强制完全重建 |
| `zotero-mcp db-status` | 查看数据库状态 |

> 🤖 ASK: 「语义搜索数据库需要构建。建议运行以下命令（可能需要几分钟）：
>   `zotero-mcp update-db --fulltext`
>   是否现在构建？如果文献量大，建议稍后在终端手动运行。」

---

## 嵌入模型选择

### 选项 1: 本地模型（默认，推荐）

无需任何 API Key，完全本地运行。

**环境变量：**
```json
"ZOTERO_EMBEDDING_MODEL": "default"
```

### 选项 2: OpenAI 嵌入

> 需要 OpenAI API Key:
> 🤖 ASK: 「请提供您的 OpenAI API Key（或以 OPENAI_API_KEY 环境变量的形式设置）。」

```json
"ZOTERO_EMBEDDING_MODEL": "openai",
"OPENAI_API_KEY": "sk-...",
"OPENAI_EMBEDDING_MODEL": "text-embedding-3-small"
```

如需自定义 API 端点（如 Azure OpenAI）：
```json
"OPENAI_BASE_URL": "https://your-endpoint.openai.azure.com/"
```

### 选项 3: Gemini 嵌入

```json
"ZOTERO_EMBEDDING_MODEL": "gemini",
"GEMINI_API_KEY": "...",
"GEMINI_EMBEDDING_MODEL": "gemini-embedding-001"
```

---

## 配置示例

包含语义搜索的 mcp.json：

```json
{
  "mcpServers": {
    "zotero": {
      "command": "zotero-mcp",
      "args": [],
      "env": {
        "ZOTERO_LOCAL": "true",
        "ZOTERO_EMBEDDING_MODEL": "default"
      },
      "disabled": false
    }
  }
}
```

---

## 使用示例

配置完成后：

```
「基于我的 Zotero 文献库，找与这篇论文方法论最相似的 5 篇研究」
「查找我的文献库中讨论数字化转型对企业绩效影响的论文」
「给我一个关于供应链韧性的文献综述，基于语义最相关的 10 篇论文」
```

---

## 注意事项

- 默认嵌入模型（all-MiniLM-L6-v2）首次运行时会自动下载
- 文献库越大，`update-db` 耗时越长
- 向量数据库文件存储在 Zotero 数据目录中
- 新增文献后建议定期运行 `zotero-mcp update-db` 更新索引
