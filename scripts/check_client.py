#!/usr/bin/env python3
"""Check account wiring with the real client without connecting or reading secrets."""
import json
from pathlib import Path
import selectors
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]


def check():
    process = subprocess.Popen(
        ["codex", "app-server"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, text=True, bufsize=1,
    )
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)

    def call(identifier, method, params):
        process.stdin.write(json.dumps({
            "jsonrpc": "2.0", "id": identifier, "method": method, "params": params,
        }) + "\n")
        process.stdin.flush()
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if not selector.select(timeout=1):
                continue
            line = process.stdout.readline()
            if not line:
                raise RuntimeError("Client stopped before responding")
            response = json.loads(line)
            if response.get("id") != identifier:
                continue
            if "error" in response:
                raise RuntimeError("Client rejected the metadata request")
            return response["result"]
        raise TimeoutError(method)

    try:
        call(1, "initialize", {
            "clientInfo": {"name": "tactical-account-wiring-check", "version": "1.0.0"},
            "capabilities": {"experimentalApi": True},
        })
        process.stdin.write('{"jsonrpc":"2.0","method":"initialized"}\n')
        process.stdin.flush()
        plugin = call(2, "plugin/read", {
            "pluginName": "tactical-rmm",
            "marketplacePath": str(ROOT / ".agents/plugins/marketplace.json"),
        })["plugin"]
        apps = plugin["apps"]
        binding_path = ROOT / "plugins/tactical-rmm/.app.json"
        expected = json.loads(binding_path.read_text())["apps"] if binding_path.exists() else {}
        expected_ids = {app["id"] for app in expected.values() if app.get("required")}
        passed = (
            len(apps) == len(expected_ids) == 1
            and {app["id"] for app in apps} == expected_ids
            and all(isinstance(app.get("installUrl"), str)
                    and app["installUrl"].startswith("https://chatgpt.com/apps/") for app in apps)
            and len(plugin["skills"]) == 3
            and not plugin["mcpServers"]
        )
        print(json.dumps({
            "version": plugin["summary"]["localVersion"],
            "skills": len(plugin["skills"]),
            "registered_apps": len(apps),
            "raw_mcp_servers": len(plugin["mcpServers"]),
            "account_wiring_passed": passed,
            "oauth_login_tested": False,
            "chatgpt_browser_tested": False,
        }))
        return 0 if passed else 1
    finally:
        selector.close()
        process.terminate()
        try:
            process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


if __name__ == "__main__":
    raise SystemExit(check())
