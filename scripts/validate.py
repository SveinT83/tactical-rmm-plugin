#!/usr/bin/env python3
"""Validate the package, local paths and repository content without network calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import struct
import sys

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?\Z")
APP_ID = re.compile(r"asdk_app_[A-Za-z0-9]+\Z")
DELETED_APP_ID = "asdk_app_6af232dfb75c81919191e1ab5b5fd9c0"
OAUTH = {"type": "oauth", "client": {"mode": "provided", "clientId": "tactical-chatgpt", "tokenEndpointAuthMethod": "none"}, "baseScopes": ["tactical-rmm"]}
IGNORED = {".git", ".venv", "dist", "build", "node_modules", "__pycache__", ".pytest_cache"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_json(path):
    def unique(pairs):
        result = {}
        for k, v in pairs:
            require(k not in result, f"Duplicate JSON key in {path.name}")
            result[k] = v
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def contained(base, relative):
    require(isinstance(relative, str) and relative.startswith("./"), "Path must start with ./")
    path = base / relative
    require(not any(p.is_symlink() for p in [path, *path.parents] if p != base.parent), "Symlink path")
    require(path.resolve().is_relative_to(base.resolve()), "Path escapes package/root")
    require(path.exists(), f"Missing referenced path: {relative}")
    return path


def source_files(root):
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if d not in IGNORED]
        for d in dirs:
            require(not (Path(directory) / d).is_symlink(), "Repository contains symlink directory")
        for name in files:
            path = Path(directory) / name
            require(not path.is_symlink(), "Repository contains symlink file")
            yield path


def scan_bytes(data, label):
    # Report a filename and rule only, never the matching value or source line.
    patterns = {
        "private-key": rb"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        "jwt": rb"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}",
        "credential-assignment": rb"(?i)[\"']?(?:client_secret|clientSecret|api_key|apiKey|access_token|refresh_token)[\"']?\s*[:=]\s*[\"'][A-Za-z0-9_./+\-=]{16,}[\"']",
        "bearer-value": rb"(?i)\bBearer\s+[A-Za-z0-9_.\-]{24,}",
        "github-token": rb"\bgh[pousr]_[A-Za-z0-9]{30,}",
        "credential-url": rb"https?://[^\s/\"']+:[^\s/@\"']+@",
    }
    for rule, pattern in patterns.items():
        require(not re.search(pattern, data), f"Possible secret ({rule}): {label}")


def scan_repo(root):
    paths = set(source_files(root))
    if (root / ".git").exists():
        # Include tracked ignored files and staged content, too.
        tracked = subprocess.run(["git", "ls-files", "-z"], cwd=root, check=True, capture_output=True).stdout
        for raw in tracked.split(b"\0"):
            if not raw:
                continue
            rel = raw.decode()
            path = root / rel
            require(path.exists() and not path.is_symlink(), "Tracked file missing or symlink")
            paths.add(path)
            staged = subprocess.run(["git", "show", f":{rel}"], cwd=root, check=True, capture_output=True).stdout
            scan_bytes(staged, rel + " (index)")
    for path in paths:
        rel = path.relative_to(root)
        require(not any(part in IGNORED for part in rel.parts), f"Generated/local file tracked: {rel}")
        require(not path.name.startswith((".env", "credentials", "secrets")), f"Sensitive filename: {rel}")
        require(path.name != "auth.json" and path.suffix not in {".pem", ".key", ".p12", ".pfx"}, f"Credential file: {rel}")
        scan_bytes(path.read_bytes(), str(rel))
    return len(paths)


def validate(root=ROOT):
    root = Path(root)
    market = read_json(root / ".agents/plugins/marketplace.json")
    require(market["name"] == "tronder-data-tactical-rmm", "Marketplace identity changed")
    require(len(market["plugins"]) == 1, "Expected exactly one marketplace entry")
    entry = market["plugins"][0]
    require("pluginId" not in entry, "Personal plugin ID must not migrate workspace plugin")
    require(entry["source"]["source"] == "local", "Expected in-repository source")
    package = contained(root, entry["source"]["path"])
    native = not (package / "plugin.json").exists()
    manifest = read_json(package / (".codex-plugin/plugin.json" if native else "plugin.json"))
    if not native:
        jsonschema.Draft202012Validator(read_json(root / "schemas/plugin.schema.json")).validate(manifest)
    require(entry["name"] == manifest["name"] == package.name == "tactical-rmm", "Package names differ")
    require(bool(SEMVER.fullmatch(manifest["version"])), "Invalid semantic version")
    extension = ({"interface": manifest["interface"], "onboardingSkill": manifest["onboardingSkill"]}
                 if native else manifest["extensions"]["com.openai"])
    interface = extension["interface"]
    require(interface["displayName"] == "Tactical RMM", "Unexpected display name")
    require(manifest["author"]["name"] == interface["developerName"] == "Trønder Data", "Publisher differs")
    require(0 < len(interface["shortDescription"]) <= 30, "Subtitle must be 1–30 characters")
    require(interface["category"] == entry["category"] == "Developer Tools", "Category differs")
    require(isinstance(interface["capabilities"], list) and all(isinstance(x, str) and x.strip() for x in interface["capabilities"]), "Invalid capabilities")
    compatibility = read_json(package / ".codex-plugin/plugin.json")
    for k in ["name", "version", "description", "author"]:
        require(compatibility[k] == manifest[k], f"Compatibility mismatch: {k}")
    for k in ["interface", "onboardingSkill"]:
        require(compatibility[k] == extension[k], f"OpenAI overlay mismatch: {k}")
    connection = read_json(root / "config/connection.json")
    auth = OAUTH
    if native:
        require(compatibility.get("apps") == "./.app.json", "Missing native app binding")
        require("mcpServers" not in compatibility, "App binding must not declare a parallel MCP")
        require(not any((package / name).exists() for name in ["mcp.json", ".mcp.json"]), "Raw MCP would mask the registered app")
        apps = read_json(contained(package, compatibility["apps"]))
        require(set(apps) == {"apps"} and set(apps["apps"]) == {"tactical-rmm"}, "Expected one registered Tactical app")
        app = apps["apps"]["tactical-rmm"]
        require(set(app) == {"id", "required"} and app["required"] is True, "App must be required")
        require(isinstance(app["id"], str) and bool(APP_ID.fullmatch(app["id"])) and app["id"] != DELETED_APP_ID, "Invalid or deleted app ID")
        binding = connection["appBindingVerification"]
        require(binding.get("mode") == "registered-app" and binding.get("app_id") == app["id"], "App differs from verified registration")
        receipt = binding.get("registration", {})
        original_apps = receipt.get("app_manifest", {}).get("apps", {})
        require(len(original_apps) == 1, "Expected one original app mapping")
        original = next(iter(original_apps.values()))
        require(set(original) <= {"id", "required"} and original.get("id") == app["id"]
                and original.get("required", True) is True, "App mapping differs from registration receipt")
        require(receipt.get("mcp_url") == connection["mcpUrl"], "Registered app uses the wrong MCP")
        require(receipt.get("scope") == "WORKSPACE" and receipt.get("workspace_id") == "c32d88fa-1324-44b1-9fce-9d7a166164a4", "App is not in the target workspace")
        require(receipt.get("plugin_id") == "plugin_" + app["id"], "Registration identity mismatch")
    else:
        require("apps" not in extension and "apps" not in compatibility and not (package / ".app.json").exists(), "Unverified app dependency")
        mcp = read_json(package / "mcp.json")
        require(set(mcp["mcpServers"]) == {"tactical-rmm"}, "Expected one remote MCP server")
        server = mcp["mcpServers"]["tactical-rmm"]
        require(set(server) == {"type", "url", "extensions"}, "Static auth headers or extra MCP fields are not allowed")
        # The published base schema does not yet admit documented vendor auth.
        transport = json.loads(json.dumps(mcp))
        transport["mcpServers"]["tactical-rmm"].pop("extensions", None)
        jsonschema.Draft202012Validator(read_json(root / "schemas/mcp.schema.json")).validate(transport)
        require(server["type"] == "streamable-http" and server["url"] == connection["mcpUrl"], "Wrong MCP transport or endpoint")
        require(server.get("extensions") == {"com.openai": {"auth": auth}}, "Unexpected OpenAI OAuth configuration")
        legacy = read_json(contained(package, compatibility["mcpServers"]))
        require(legacy == {"mcpServers": {"tactical-rmm": {"url": server["url"], "extensions": server["extensions"]}}}, "Legacy MCP configuration mismatch")
    skills = contained(package, compatibility["skills"])
    skill_paths = sorted(skills.glob("*/SKILL.md"))
    require({p.parent.name for p in skill_paths} == {"tactical-rmm", "tactical-rmm-admin", "tactical-rmm-setup"}, "Expected operational, administration and setup skills")
    onboarding = contained(package, extension["onboardingSkill"])
    require(onboarding in skill_paths and onboarding.parent.name == "tactical-rmm-setup", "Onboarding must reference the packaged setup skill")
    for field in ["logo", "composerIcon"]:
        icon = contained(package, interface[field])
        data = icon.read_bytes()
        require(icon.suffix == ".png" and len(data) >= 24 and data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR", "Invalid PNG icon")
        width, height = struct.unpack(">II", data[16:24])
        require(48 <= width == height <= 4096 and len(data) <= 5 * 1024 * 1024, "Invalid icon size")
        require(hashlib.sha256(data).hexdigest() == "bc5de347720ddf50dadcdecddd0115243515e4e5007fe798f70a990741aae7c2", "Logo differs from verified official source")
    for path in skill_paths:
        raw = path.read_text(encoding="utf-8")
        require(path.stat().st_size <= 1024 * 1024 and raw.startswith("---\n"), "Invalid skill/frontmatter")
        parts = raw.split("---\n", 2)
        require(len(parts) == 3, "Unclosed skill frontmatter")
        front = yaml.safe_load(parts[1])
        require(front["name"] == path.parent.name, "Skill directory/name mismatch")
        require(isinstance(front["description"], str) and front["description"].strip(), "Missing skill description")
        for link in re.findall(r"\]\(([^)]+)\)", parts[2]):
            require("://" not in link and not link.startswith("/"), "Skill reference must stay in package")
            target = path.parent / link
            require(target.resolve().is_relative_to(package.resolve()) and target.is_file(), "Broken/escaping skill reference")
        agent = yaml.safe_load((path.parent / "agents/openai.yaml").read_text())
        require(agent["interface"]["display_name"] == interface["displayName"], "Skill presentation mismatch")
        require(isinstance(agent["policy"]["allow_implicit_invocation"], bool), "Invocation policy must be boolean")
    for path in package.rglob("*"):
        require(not path.is_symlink(), "Package contains symlink")
        require(not any(p in IGNORED for p in path.relative_to(package).parts), "Generated/local file in package")
    require(connection["auth"] == auth, "Connection reference differs from runtime OAuth config")
    require(connection["tokenEndpointAuthMethod"] == auth["client"]["tokenEndpointAuthMethod"], "Token authentication reference differs")
    require(connection["auth"] == {"type": "oauth", "client": {"mode": "provided", "clientId": "tactical-chatgpt", "tokenEndpointAuthMethod": "none"}, "baseScopes": ["tactical-rmm"]}, "OAuth contract changed")
    require(connection["mcpUrl"] == "https://tactical-mcp.tronderdata.no/chatgpt/mcp", "Wrong MCP endpoint")
    require(connection["issuer"] == "https://auth.tronderdata.no/realms/tronderdata", "Wrong issuer")
    require(connection["setupUrl"] == "https://tactical-mcp.tronderdata.no/admin/", "Wrong verified setup URL")
    files = scan_repo(root)
    return {"package": str(package.relative_to(root)), "version": manifest["version"], "skills": len(skill_paths), "scanned_files": files}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        print(json.dumps(validate(), ensure_ascii=False))
    except (ValueError, KeyError, jsonschema.ValidationError, yaml.YAMLError) as error:
        # jsonschema messages may include source values, so suppress full details.
        print(f"Validation failed: {type(error).__name__}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
