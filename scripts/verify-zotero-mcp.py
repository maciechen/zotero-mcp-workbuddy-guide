"""Zotero MCP 配置验证脚本

配置完成后运行此脚本，验证 MCP 配置是否正常工作。
"""

import json
import os
import subprocess
import sys

print("=" * 50)
print("Zotero MCP 配置验证")
print("=" * 50)

def error(msg):
    print(f"\n  [错误] {msg}")
    return False

def ok(msg):
    print(f"  [OK] {msg}")
    return True

# 1. 检查 mcp.json
mcp_path = os.path.expanduser("~/.workbuddy/mcp.json")
if not os.path.exists(mcp_path):
    error(f"mcp.json 未找到: {mcp_path}")
    sys.exit(1)

with open(mcp_path, "r", encoding="utf-8") as f:
    try:
        config = json.loads(f.read())
    except json.JSONDecodeError as e:
        error(f"mcp.json JSON 格式错误: {e}")
        sys.exit(1)

servers = config.get("mcpServers", {})
if "zotero" not in servers:
    error("mcp.json 中未找到 zotero 配置")
    sys.exit(1)

zotero = servers["zotero"]
ok(f"已找到 zotero 配置")

# 2. 检查模式
env = zotero.get("env", {})
is_local = env.get("ZOTERO_LOCAL") == "true"
has_api_key = "ZOTERO_API_KEY" in env and env["ZOTERO_API_KEY"] not in ("{{ASK_USER:ZOTERO_API_KEY}}", "")

if is_local and has_api_key:
    ok("模式: 混合模式（本地 + 云端）")
elif is_local:
    ok("模式: 本地模式")
elif has_api_key:
    ok("模式: 云端模式")
else:
    error("未识别到有效配置模式")

# 3. 检查 disabled 状态
if zotero.get("disabled", False):
    error("Zotero MCP 配置已被禁用（\"disabled\": true）")

# 4. 检查 mcp.json 语法
json_str = json.dumps(config, indent=2, ensure_ascii=False)
ok(f"mcp.json 语法有效 ({len(json_str)} bytes)")

# 5. 检查 zotero-mcp 可执行
try:
    result = subprocess.run(
        ["zotero-mcp", "version"],
        capture_output=True, text=True, timeout=10
    )
    version = (result.stdout + result.stderr).strip()
    ok(f"zotero-mcp 可用: {version}")
except FileNotFoundError:
    error("zotero-mcp 命令不可用，请确认已安装")

# 6. 本地模式额外检查
if is_local:
    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:23119/connector/ping")
        resp = urllib.request.urlopen(req, timeout=3)
        ok("Zotero 桌面端已连接")
    except Exception:
        error("Zotero 桌面端未连接！请确认 Zotero 7+ 正在运行且本地 API 已开启")

# 7. 云端模式检查
if has_api_key:
    api_key = env["ZOTERO_API_KEY"]
    masked = api_key[:4] + "****" + api_key[-4:] if len(api_key) > 8 else "***"
    ok(f"API Key 已设置: {masked}")
    ok(f"Library ID: {env.get('ZOTERO_LIBRARY_ID', '未设置')}")
    ok(f"Library Type: {env.get('ZOTERO_LIBRARY_TYPE', '未设置')}")

print("\n" + "=" * 50)
print("验证完成！")
print("\n下一步：重启 WorkBuddy，然后在对话中说「测试 Zotero 连接」")
print("=" * 50)
