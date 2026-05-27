"""Zotero MCP 环境检测脚本

人可手动运行，AI 也可直接执行。
检查 Python版本、zotero-mcp 安装状态、Zotero 本地 API、WorkBuddy 配置。
"""

import subprocess
import sys
import os
import json
import platform

OK = lambda msg: f"  [PASS] {msg}"
FAIL = lambda msg: f"  [FAIL] {msg}"
WARN = lambda msg: f"  [WARN] {msg}"
INFO = lambda msg: f"  [INFO] {msg}"

passed, failed, warnings = 0, 0, 0


def check(name, fn, required=True):
    global passed, failed, warnings
    try:
        ok, msg = fn()
        if ok:
            passed += 1
            print(OK(f"{name}: {msg}"))
        elif required:
            failed += 1
            print(FAIL(f"{name}: {msg}"))
        else:
            warnings += 1
            print(WARN(f"{name}: {msg}"))
        return ok
    except Exception as e:
        if required:
            failed += 1
            print(FAIL(f"{name}: {str(e)}"))
        else:
            warnings += 1
            print(WARN(f"{name}: {str(e)}"))
        return False


def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result.stdout.strip() + result.stderr.strip()


print("=" * 50)
print(f"Zotero MCP 环境检测")
print(f"操作系统: {platform.system()} {platform.release()}")
print(f"Python: {sys.version}")
print("=" * 50)

# 1. Python 版本
def check_python():
    v = sys.version_info
    ok = (v.major, v.minor) >= (3, 10)
    return ok, f"Python {v.major}.{v.minor}.{v.micro} {'✓' if ok else '需要 >= 3.10'}"
check("Python >= 3.10", check_python)

# 2. zotero-mcp-server
def check_zotero_mcp():
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "zotero-mcp-server"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if line.startswith("Version:"):
                    return True, f"已安装 v{line.split(':')[1].strip()}"
            return True, "已安装"
        return False, "未安装，请运行 pip install zotero-mcp-server"
    except Exception:
        return False, "检测失败"
check("zotero-mcp-server", check_zotero_mcp)

# 3. zotero-mcp 命令行工具
def check_cli():
    try:
        result = subprocess.run(
            ["zotero-mcp", "version"],
            capture_output=True, text=True, timeout=10
        )
        out = result.stdout.strip() or result.stderr.strip()
        return True, out
    except FileNotFoundError:
        return False, "zotero-mcp 命令未找到，请确认 Python Scripts 目录在 PATH 中"
    except Exception as e:
        return False, str(e)
check("zotero-mcp CLI", check_cli)

# 4. Zotero 本地 API
def check_zotero_api():
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request("http://localhost:23119/connector/ping")
        resp = urllib.request.urlopen(req, timeout=3)
        return resp.status == 200, f"Zotero 桌面端运行中 (status {resp.status})"
    except urllib.error.URLError:
        return False, "Zotero 桌面端未运行或本地 API 未开启"
    except Exception as e:
        return False, f"检测失败: {e}"
check("Zotero 本地 API", check_zotero_api, required=False)

# 5. WorkBuddy mcp.json
def check_mcp_json():
    mcp_path = os.path.expanduser("~/.workbuddy/mcp.json")
    if os.path.exists(mcp_path):
        try:
            with open(mcp_path, "r", encoding="utf-8") as f:
                content = f.read()
            config = json.loads(content)
            servers = config.get("mcpServers", {})
            if "zotero" in servers:
                zotero = servers["zotero"]
                env = zotero.get("env", {})
                mode_parts = []
                if env.get("ZOTERO_LOCAL") == "true":
                    mode_parts.append("本地")
                if "ZOTERO_API_KEY" in env and env["ZOTERO_API_KEY"] not in ("{{ASK_USER:ZOTERO_API_KEY}}", ""):
                    mode_parts.append("云端")
                disabled = zotero.get("disabled", False)
                mode_str = " + ".join(mode_parts) if mode_parts else "未知模式"
                status_str = " [已禁用]" if disabled else ""
                return True, f"已配置 ({mode_str}){status_str}"
            else:
                return True, "mcp.json 存在但未配置 Zotero"
        except json.JSONDecodeError:
            return False, "mcp.json JSON 格式错误"
    else:
        return True, "mcp.json 尚未创建（配置后将自动生成）"
check("WorkBuddy mcp.json", check_mcp_json, required=False)

# Summary
print("\n" + "=" * 50)
total = passed + failed + warnings
print(f"检测完成: {passed} 通过, {failed} 失败, {warnings} 警告")
print("=" * 50)

if failed > 0:
    print("\n请先解决失败的检查项，然后重新运行本脚本。")
    print("如需帮助，请参阅 docs/01-prerequisites.md 或 docs/07-troubleshooting.md")
    sys.exit(1)
else:
    print("\n环境就绪！可以继续配置 Zotero MCP。")
    sys.exit(0)
