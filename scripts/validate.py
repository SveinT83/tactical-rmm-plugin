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
    require(entry["source"]["source"] == "local", "Expected in-repository source")
    package = contained(root, entry["source"]["path"])
    require(package.name == "tactical-rmm", "Unexpected package directory")
    require(not any((package / name).exists() for name in ["plugin.json", "mcp.json", ".mcp.json"]), "Portable components would mask the canonical account binding")
    manifest = read_json(package / ".codex-plugin/plugin.json")
    compatibility = manifest
    connection = read_json(root / "config/connection.json")
    binding = connection["appBindingVerification"]
    receipt = binding["registration"]
    require(receipt.get("scope") == "WORKSPACE" and receipt.get("workspace_id") == "c32d88fa-1324-44b1-9fce-9d7a166164a4", "Registration must belong to the target workspace")
    require(entry.get("pluginId") == receipt.get("plugin_id") == "plugin_asdk_app_6afafd3b578c8191a62956239872dd3b", "Marketplace must adopt the verified SSO plugin")
    require(entry["name"] == manifest["name"] == receipt["name"], "Technical name must match the existing SSO plugin")
    require(binding["workspacePluginId"] == entry["pluginId"], "Canonical workspace plugin identity differs")
    require(bool(SEMVER.fullmatch(manifest["version"])), "Invalid semantic version")
    extension = {"interface": manifest["interface"], "onboardingSkill": manifest["onboardingSkill"]}
    interface = extension["interface"]
    require(interface["displayName"] == "Tactical RMM", "Unexpected display name")
    require(manifest["author"]["name"] == interface["developerName"] == "Trønder Data", "Publisher differs")
    require(0 < len(interface["shortDescription"]) <= 30, "Subtitle must be 1–30 characters")
    require(interface["category"] == entry["category"] == "Developer Tools", "Category differs")
    require(isinstance(interface["capabilities"], list) and all(isinstance(x, str) and x.strip() for x in interface["capabilities"]), "Invalid capabilities")
    require(manifest.get("apps") == "./.app.json", "Missing account binding")
    require("mcpServers" not in manifest, "Canonical SSO plugin cannot declare a parallel MCP")
    apps = read_json(contained(package, manifest["apps"]))
    require(apps == receipt["app_manifest"], "Account binding differs from the actual registration")
    require(set(apps) == {"apps"} and len(apps["apps"]) == 1, "Expected one account binding")
    app = next(iter(apps["apps"].values()))
    require(set(app) <= {"id", "required"} and app.get("required", True) is True, "Account must remain required")
    require("plugin_" + app["id"] == entry["pluginId"] and binding["app_id"] == app["id"], "App and plugin identity differ")
    require(binding["mode"] == "registered-app" and receipt["mcp_url"] == connection["mcpUrl"], "Registered app uses the wrong MCP")
    auth = OAUTH
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
