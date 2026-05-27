# 07 · 故障排查

> 本文档用于排查 Zotero MCP 配置后的常见问题。AI 智能体请按问题类型匹配解决方案。

---

## 问题分类

### A. 连接失败

#### A1: Zotero MCP 工具不可用

**症状**：WorkBuddy 中无法调用 Zotero 相关工具

> 🤖 CHECK: 检查 mcp.json 配置是否正确
> 🤖 EXEC: 读取 ~/.workbuddy/mcp.json，确认：
>   1. `mcpServers.zotero` 条目存在
>   2. `command` 路径正确
>   3. `disabled` 不是 `true`
>   4. JSON 语法有效（无多余逗号、引号匹配）

**手动排查：**
1. 确认 WorkBuddy 已重启
2. 检查 MCP 服务器状态面板是否显示绿色
3. 在终端中测试: `zotero-mcp --version` 是否能正常输出

#### A2: 本地模式连接失败

**症状**：`ZOTERO_LOCAL=true` 但无法连接

> 🤖 CHECK: 运行 `curl -s http://localhost:23119/connector/ping`
> 或 PowerShell: `Invoke-WebRequest http://localhost:23119/connector/ping -UseBasicParsing`

**解决方案：**
1. 确认 Zotero 7 桌面端正在运行（不是 Zotero 6）
2. 确认本地 API 已开启: Edit → Settings → Advanced → Allow other applications...
3. 确认端口 23119 未被占用
4. 尝试重启 Zotero

#### A3: 云端模式连接失败

**症状**：有 API Key 但返回认证错误

> 🤖 CHECK: 检查环境变量是否拼写正确
> `ZOTERO_API_KEY`（不是 ZOTERO_APIKEY 或 ZOTERO_KEY）
> `ZOTERO_LIBRARY_ID`（不是 ZOTERO_LIBRARYID）
> `ZOTERO_LIBRARY_TYPE`（不是 ZOTERO_TYPE）

**解决方案：**
1. 确认 API Key 有效（登录 zotero.org/settings/keys 验证）
2. 确认 API Key 权限包含 "Allow library access"
3. 确认 Library ID 正确（User ID 是纯数字）
4. 确认网络可访问 api.zotero.org

---

### B. 配置问题

#### B1: mcp.json 语法错误

**症状**：WorkBuddy 无法识别 MCP 配置，或状态面板显示红色

**常见错误：**
- JSON 最后一项后多了逗号（trailing comma）
- 引号不匹配（使用了中文引号）
- `boolean` 值写成了字符串（`"true"` 而非 `true`）

#### B2: pip install 失败

**症状**：`pip install zotero-mcp-server` 报错

**解决方案：**
```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像（中国用户）
pip install zotero-mcp-server -i https://pypi.tuna.tsinghua.edu.cn/simple

# 确认 Python 版本
python --version  # 需要 >= 3.10
```

#### B3: mcp.json 被覆盖或丢失

**症状**：其他 MCP 服务配置被覆盖

> 🤖 CHECK: 读取 ~/.workbuddy/mcp.json
> 确认 mcpServers 对象中是否包含所有预期的服务

**解决方案：**
- 备份现有配置后再修改
- 使用项目级配置（`<项目>/.workbuddy/mcp.json`）隔离不同项目的 MCP 服务

---

### C. 功能问题

#### C1: PDF 全文/批注无法获取

**症状**：本地模式下仍提示无法访问 PDF 内容

**解决方案：**
1. 确认安装了 PDF 扩展: `pip install "zotero-mcp-server[pdf]"`
2. 确认 PDF 文件存储在 Zotero 数据目录中（非链接文件）
3. 确认是 Zotero 7+（Zotero 6 不支持全文访问）

#### C2: 语义搜索无结果

**症状**：语义搜索查询返回空或无关结果

**解决方案：**
1. 检查数据库是否已构建: `zotero-mcp db-status`
2. 如果未构建: `zotero-mcp update-db`
3. 如果文献量变化大: `zotero-mcp update-db --force-rebuild`

#### C3: 本地模式无法写入标签

**症状**：尝试添加标签时失败

**解释**：本地模式对写操作支持有限。解决方案：
- 切换到混合模式（本地读 + 云端写）
- 或切换到纯云端模式

---

### D. 验证清单

> 🤖 EXEC: 按以下顺序逐项验证：

```
[ ] zotero-mcp --version 正常输出
[ ] ~/.workbuddy/mcp.json JSON 语法有效
[ ] mcpServers.zotero 条目存在且 disabled 不为 true
[ ] [本地/混合] curl localhost:23119 可访问
[ ] [云端/混合] ZOTERO_API_KEY 已设置且有效
[ ] WorkBuddy 已重启
[ ] MCP 服务器状态面板显示绿色
[ ] 能够成功调用 Zotero 工具获取文献库信息
```

---

## 获取帮助

如本文档无法解决你的问题：

1. 查看上游项目 Issue: [54yyyu/zotero-mcp/issues](https://github.com/54yyyu/zotero-mcp/issues)
2. 查阅官方文档: [stevenyuyy.com/zotero-mcp](https://stevenyuyy.com/zotero-mcp/)
3. 检查 Zotero 论坛: [forums.zotero.org](https://forums.zotero.org/)
