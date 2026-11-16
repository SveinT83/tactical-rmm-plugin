#!/usr/bin/env python3
"""Read public discovery and MCP metadata only. Never accepts credentials."""
import argparse
from datetime import datetime, timezone
import json
import urllib.error
import urllib.request

from validate import ROOT, read_json, require


def fetch(url, payload=None):
    headers = {"Accept": "application/json, text/event-stream"}
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode()
    request = urllib.request.Request(url, data=data, headers=headers)
    # No Authorization header, environment credential, cookies or token input.
    with urllib.request.urlopen(request, timeout=20) as response:
        text = response.read(1024 * 1024).decode()
        if "text/event-stream" in response.headers.get("Content-Type", ""):
            text = next(line[5:].strip() for line in text.splitlines() if line.startswith("data:") and line[5:].strip())
        return json.loads(text)


def probe():
    config = read_json(ROOT / "config/connection.json")
    resource = fetch(config["protectedResourceMetadataUrl"])
    oidc = fetch(config["oidcConfigurationUrl"])
    require(resource["resource"] == config["mcpUrl"], "Resource mismatch")
    require(config["issuer"] in resource["authorization_servers"], "Authorization server mismatch")
    require("tactical-rmm" in resource["scopes_supported"], "Required resource scope missing")
    require(oidc["issuer"] == config["issuer"], "OIDC issuer mismatch")
    require("S256" in oidc["code_challenge_methods_supported"], "PKCE S256 missing")
    results = {}
    for index, (method, params) in enumerate([
        ("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "tactical-plugin-metadata-probe", "version": "1.0.0"}}),
        ("tools/list", {}),
    ], 1):
        result = fetch(config["mcpUrl"], {"jsonrpc": "2.0", "id": index, "method": method, "params": params})
        require("error" not in result and "result" in result, "MCP metadata request failed")
        results[method] = result["result"]
    tools = results["tools/list"]["tools"]
    baseline_tools = {"tactical-rmm_search", "tactical-rmm_execute"}
    reviewed_tools = set(config.get("reviewedToolNames", baseline_tools))
    tool_names = {t["name"] for t in tools}
    require(baseline_tools <= tool_names, "Baseline tools missing: review integration")
    require(not results["tools/list"].get("nextCursor"), "Paginated catalog: further discovery required")
    for tool in tools:
        schemes = tool.get("_meta", {}).get("securitySchemes", [])
        require(any(s.get("type") == "oauth2" and "tactical-rmm" in s.get("scopes", []) for s in schemes), "OAuth policy changed")
    return {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "kind": "public-metadata-only",
        "resource": resource,
        "oidc": {k: oidc[k] for k in ["issuer", "authorization_endpoint", "token_endpoint", "code_challenge_methods_supported", "token_endpoint_auth_methods_supported", "authorization_response_iss_parameter_supported"] if k in oidc},
        "server": results["initialize"]["serverInfo"],
        "tools": tools,
        "new_tools_requiring_review": sorted(tool_names - reviewed_tools),
        "reviewed_tools_missing_from_catalog": sorted(reviewed_tools - tool_names),
        "oauth_login_tested": False,
        "personal_isolation_tested": False,
        "browser_tested": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true", help="Save sanitized metadata to docs/evidence/public-metadata.json")
    args = parser.parse_args()
    try:
        result = probe()
    except urllib.error.HTTPError as error:
        print(json.dumps({"ok": False, "http_status": error.code, "note": "Metadata access failed; no credentials requested or displayed."}))
        return 1
    except Exception as error:
        print(json.dumps({"ok": False, "error_type": type(error).__name__}))
        return 1
    if args.save:
        dest = ROOT / "docs/evidence/public-metadata.json"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"ok": True, "kind": result["kind"], "tools": [t["name"] for t in result["tools"]], "new_tools_requiring_review": result["new_tools_requiring_review"], "server": result["server"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
