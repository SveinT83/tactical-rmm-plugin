#!/usr/bin/env python3
"""Read-only prelaunch checks. No credentials, redirects or mutating tool calls."""
import argparse
from datetime import datetime, timezone
import json
import urllib.error
import urllib.parse
import urllib.request

import jsonschema

from probe import probe
from validate import ROOT, read_json, require, validate

ACCESS_TOOLS = {
    "tactical-rmm_access_users", "tactical-rmm_access_keys",
    "tactical-rmm_access_assign", "tactical-rmm_access_create",
    "tactical-rmm_access_rotate", "tactical-rmm_access_remove",
}
READ_TOOLS = {"tactical-rmm_access_users", "tactical-rmm_access_keys"}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def request_without_identity(url, payload=None, read_login_html=False):
    """Return metadata only; never read a tool-call response body."""
    headers = {"Accept": "application/json, text/event-stream" if payload else "text/html"}
    data = None
    if payload is not None:
        require(not read_login_html, "Tool response bodies must never be read")
        require(payload.get("method") == "tools/call", "Only explicit read-tool probes allowed")
        require(payload["params"]["name"] in READ_TOOLS, "Mutating tool prohibited in this test")
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers)
    opener = urllib.request.build_opener(NoRedirect)
    try:
        response = opener.open(req, timeout=20)
    except urllib.error.HTTPError as error:
        response = error
    try:
        result = {
            "status": response.code,
            "content_type": response.headers.get("Content-Type", ""),
            "bearer_challenge": response.headers.get("WWW-Authenticate", "").lower().startswith("bearer"),
            "resource_metadata_in_challenge": "resource_metadata=" in response.headers.get("WWW-Authenticate", ""),
            "no_store": "no-store" in response.headers.get("Cache-Control", ""),
            "same_origin_referrer_policy": response.headers.get("Referrer-Policy", "") == "same-origin",
        }
        if read_login_html and response.code == 200:
            # An anonymous static login page, never an authenticated browser session.
            html = response.read(256 * 1024).decode("utf-8", errors="replace")
            result["keycloak_login_link_present"] = 'href="/admin/login"' in html
        return result
    finally:
        response.close()


def run():
    package = validate()
    metadata = probe()
    tools = {t["name"]: t for t in metadata["tools"]}
    require(ACCESS_TOOLS <= tools.keys(), "Expected access tools are not deployed")
    for name, tool in tools.items():
        jsonschema.Draft202012Validator.check_schema(tool["inputSchema"])
    for name in ACCESS_TOOLS:
        read_only = tools[name]["annotations"].get("readOnlyHint")
        require(read_only is (name in READ_TOOLS), "Access-tool read/write annotation mismatch")
    checks = [{"name": "package-and-live-catalog", "passed": True}]
    config = read_json(ROOT / "config/connection.json")
    setup = config.get("setupUrl")
    require(setup == "https://tactical-mcp.tronderdata.no/admin/", "Setup URL must be source-verified before this test")
    page = request_without_identity(setup, read_login_html=True)
    checks.append({"name": "anonymous-setup-signin-page", "passed": page["status"] == 200 and page.get("keycloak_login_link_present") is True and page["no_store"], "observed": page})
    for index, name in enumerate(sorted(READ_TOOLS), 1):
        result = request_without_identity(config["mcpUrl"], {
            "jsonrpc": "2.0", "id": index, "method": "tools/call",
            "params": {"name": name, "arguments": {}},
        })
        checks.append({"name": name + "-requires-oauth", "passed": result["status"] == 401 and result["bearer_challenge"] and result["resource_metadata_in_challenge"], "observed": result})
    internal = request_without_identity("https://tactical-mcp.tronderdata.no/admin/api/tools")
    checks.append({"name": "internal-admin-backend-not-public", "passed": internal["status"] in {403, 404}, "observed": internal})
    # These constraints are documented and enforced by the server, but not all
    # are encoded in its published input schemas. Do not mistake schema-only
    # acceptance for valid runtime parameters.
    notes = [
        "access_assign describes key_id as required but does not list it in required; enforce it before calls.",
        "access_remove mode=revoke conditionally requires key_id in documentation/server validation.",
        "idempotency_key length and expiration bounds are documented runtime requirements, not complete input-schema constraints.",
        "No authenticated user mapping, role isolation, key lifecycle or ChatGPT browser flow was tested by this script.",
    ]
    return metadata, {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "kind": "prelaunch-readonly-without-identity",
        "package": package,
        "server": metadata["server"],
        "checks": checks,
        "all_automated_checks_passed": all(c["passed"] for c in checks),
        "authenticated_checks_passed": False,
        "authenticated_tool_available_in_this_chat": False,
        "key_mutations_performed": False,
        "customer_machine_actions_performed": False,
        "customer_data_retrieved": False,
        "launch_approved": False,
        "limitations": notes,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    try:
        metadata, report = run()
    except Exception as error:
        print(json.dumps({"passed": False, "error_type": type(error).__name__}))
        return 1
    if args.save:
        directory = ROOT / "docs/evidence"
        (directory / "prelaunch-readonly.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        (directory / "public-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"passed": report["all_automated_checks_passed"], "checks": len(report["checks"]), "server": report["server"], "authenticated_checks_passed": False, "launch_approved": False}, ensure_ascii=False))
    return 0 if report["all_automated_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
