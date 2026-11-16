#!/usr/bin/env python3
"""Prepare the BookStack-style package after verifying a ChatGPT MCP registration.

The receipt contains public registration metadata copied from the source reader,
not credentials. This command neither registers an OAuth client nor signs in.
It validates a temporary candidate before changing the working tree. Publishing
and browser verification are separate steps.
"""
import argparse
import json
from pathlib import Path
import shutil
import tempfile

from validate import APP_ID, DELETED_APP_ID, ROOT, read_json, require, validate


def bind(receipt, version, root=ROOT):
    root = Path(root)
    validate(root)
    require(set(receipt) == {"plugin_id", "scope", "workspace_id", "mcp_url", "app_manifest"}, "Unexpected registration receipt fields")
    require(receipt["scope"] == "WORKSPACE", "The registered connection must be available in the target workspace")
    require(receipt["workspace_id"] == "c32d88fa-1324-44b1-9fce-9d7a166164a4", "Wrong workspace")
    require(receipt["mcp_url"] == "https://tactical-mcp.tronderdata.no/chatgpt/mcp", "Wrong MCP endpoint")
    app_manifest = receipt["app_manifest"]
    require(set(app_manifest) == {"apps"} and len(app_manifest["apps"]) == 1, "Expected one registered MCP connection")
    app = next(iter(app_manifest["apps"].values()))
    require(set(app) == {"id", "required"} and app["required"] is True, "Unexpected app mapping")
    app_id = app["id"]
    require(isinstance(app_id, str) and bool(APP_ID.fullmatch(app_id)) and app_id != DELETED_APP_ID, "Invalid or deleted app ID")
    require(receipt["plugin_id"] == "plugin_" + app_id, "Registration and app ID differ")
    current = read_json(root / "plugins/tactical-rmm/.codex-plugin/plugin.json")
    # A stable next patch avoids prerelease precedence mistakes in the helper.
    current_core = tuple(int(x) for x in current["version"].split("-")[0].split("."))
    require(isinstance(version, str) and version.count(".") == 2 and all(x.isdigit() and str(int(x)) == x for x in version.split(".")), "Use a stable three-part version")
    require(tuple(map(int, version.split("."))) > current_core, "Version must advance beyond the current core version")
    with tempfile.TemporaryDirectory(prefix="tactical-native-candidate-") as directory:
        candidate = Path(directory)
        for name in ["plugins", ".agents", "config", "schemas"]:
            shutil.copytree(root / name, candidate / name)
        package = candidate / "plugins/tactical-rmm"
        current["version"] = version
        current.pop("mcpServers", None)
        current["apps"] = "./.app.json"
        current["extensions"] = {"com.openai": {"onboardingSkill": current["onboardingSkill"]}}
        current["interface"]["longDescription"] = "Bruk Tactical RMM gjennom MCP med din personlige Keycloak-innlogging og egne rettigheter. Oppsett, drift og serverstyrt nøkkeladministrasjon."
        writes = {
            "plugins/tactical-rmm/.codex-plugin/plugin.json": current,
            "plugins/tactical-rmm/.app.json": {"apps": {"tactical-rmm": app}},
        }
        connection = read_json(candidate / "config/connection.json")
        connection["appBindingVerification"].update({
            "mode": "registered-app", "status": "awaiting-browser-oauth-test",
            "app_id": app_id, "registration": receipt,
            "note": "Binding prepared from verified registration metadata. Personal SSO and browser access still require testing.",
        })
        writes["config/connection.json"] = connection
        for name, value in writes.items():
            (candidate / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
        deletes = ["plugins/tactical-rmm/" + name for name in ["plugin.json", "mcp.json", ".mcp.json"]]
        for name in deletes:
            (candidate / name).unlink(missing_ok=True)
        url = "https://chatgpt.com/apps/tactical-rmm/" + app_id
        reference = "plugins/tactical-rmm/skills/tactical-rmm-setup/references/setup.md"
        text = (candidate / reference).read_text()
        first = text.index("\n\n")
        next_heading = text.index("\nMCP-endepunkt:", first)
        text = (text[:first] + "\n\nPakken bruker en registrert MCP-tilkobling i ChatGPT, med samme native appformat som BookStack. "
                "Ingen separat MCP-server deklareres i pakken. Bruk denne bekreftede kontolenken: `" + url + "`. "
                "Velg Koble til og fullfør personlig SSO hos Keycloak. Innlogging på API-oppsettsiden alene kobler ikke kontoen til ChatGPT.\n"
                + text[next_heading:])
        (candidate / reference).write_text(text)
        validate(candidate)
        # All rejection paths above leave the real working tree untouched.
        for name in [*writes, reference]:
            shutil.copyfile(candidate / name, root / name)
        for name in deletes:
            (root / name).unlink(missing_ok=True)
    return {"version": version, "app_id": app_id, "connection_url": url, "published": False, "oauth_tested": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True, help="Public metadata verified with Plugin Creator's source reader")
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    print(json.dumps(bind(read_json(args.receipt), args.version)))


if __name__ == "__main__":
    main()
