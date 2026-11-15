import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

import jsonschema

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate import ROOT, scan_bytes, scan_repo, validate
from build import build


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in [".agents", "plugins", "config", "schemas"]:
            shutil.copytree(ROOT / name, self.root / name)

    def edit_json(self, path, change):
        target = self.root / path
        value = json.loads(target.read_text())
        change(value)
        target.write_text(json.dumps(value, ensure_ascii=False))

    def test_valid_package(self):
        self.assertEqual(validate(self.root)["skills"], 3)

    def test_missing_onboarding_skill_is_rejected(self):
        (self.root / "plugins/tactical-rmm/skills/tactical-rmm-setup/SKILL.md").unlink()
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_unverified_logo_is_rejected(self):
        (self.root / "plugins/tactical-rmm/assets/tactical-rmm.png").write_bytes(b"invalid image")
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_overlay_version_drift_is_rejected(self):
        self.edit_json("plugins/tactical-rmm/.codex-plugin/plugin.json", lambda x: x.update(version="2.0.0"))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_marketplace_cannot_escape_repo(self):
        self.edit_json(".agents/plugins/marketplace.json", lambda x: x["plugins"][0]["source"].update(path="./../"))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_plugin_id_cannot_be_used_as_app_id(self):
        self.edit_json("plugins/tactical-rmm/.app.json", lambda x: x["apps"]["tactical-rmm"].update(id="plugin_" + x["apps"]["tactical-rmm"]["id"]))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_duplicate_connection_is_rejected(self):
        (self.root / "plugins/tactical-rmm/mcp.json").write_text("{}")
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_broken_skill_reference_is_rejected(self):
        (self.root / "plugins/tactical-rmm/skills/tactical-rmm/references/connection.md").unlink()
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_symlink_is_rejected(self):
        (self.root / "plugins/tactical-rmm/extra.md").symlink_to(ROOT / "README.md")
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_secret_scan_never_echoes_value(self):
        value = "sensitive" * 5
        payload = json.dumps({"client_" + "secret": value}).encode()
        with self.assertRaises(ValueError) as context:
            scan_bytes(payload, "fixture.json")
        self.assertNotIn(value, str(context.exception))

    def test_staged_secret_is_checked_even_if_working_copy_clean(self):
        subprocess.run(["git", "init", "-q", self.root], check=True, capture_output=True)
        path = self.root / "example.json"
        path.write_text(json.dumps({"access_" + "token": "synthetic" * 5}))
        subprocess.run(["git", "add", "example.json"], cwd=self.root, check=True, capture_output=True)
        path.write_text("{}")
        with self.assertRaises(ValueError) as context:
            scan_repo(self.root)
        self.assertIn("index", str(context.exception))

    def test_archive_has_exactly_one_plugin_and_is_repeatable(self):
        with contextlib.redirect_stdout(io.StringIO()):
            archive = build(self.root)
            first = archive.read_bytes()
            build(self.root)
        self.assertEqual(first, archive.read_bytes())
        with zipfile.ZipFile(archive) as z:
            names = z.namelist()
            self.assertTrue(all(n.startswith("tactical-rmm/") for n in names))
            self.assertIn("tactical-rmm/.app.json", names)
            self.assertIn("tactical-rmm/.codex-plugin/plugin.json", names)
            self.assertIn("tactical-rmm/skills/tactical-rmm/SKILL.md", names)
            self.assertIn("tactical-rmm/skills/tactical-rmm-admin/SKILL.md", names)
            self.assertIn("tactical-rmm/skills/tactical-rmm-setup/SKILL.md", names)
            self.assertIn("tactical-rmm/assets/tactical-rmm.png", names)
            self.assertIn("tactical-rmm/docs/MCP-ADMIN-CONTRACT.md", names)
            self.assertFalse(any("marketplace" in n for n in names))


class ObservedCommandSchemaTests(unittest.TestCase):
    """Check actual search-result requirements without executing a command."""
    @classmethod
    def setUpClass(cls):
        snapshot = json.loads((ROOT / "docs/evidence/endpoint-samples.json").read_text())
        cls.schema = snapshot["command"]["params_schema"]
        cls.validator = jsonschema.Draft202012Validator(cls.schema)

    def sample(self):
        return {"agent_id": "synthetic-test-agent", "cmd": "hostname", "shell": "custom", "custom_shell": "/bin/bash", "timeout": 15, "run_as_user": False}

    def test_both_explicit_context_choices_match_schema(self):
        for context in [True, False]:
            sample = self.sample()
            sample["run_as_user"] = context
            self.validator.validate(sample)

    def test_context_cannot_be_missing_or_a_string(self):
        missing = self.sample()
        del missing["run_as_user"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validator.validate(missing)
        invalid = self.sample()
        invalid["run_as_user"] = "false"
        with self.assertRaises(jsonschema.ValidationError):
            self.validator.validate(invalid)

    def test_custom_shell_path_is_required(self):
        sample = self.sample()
        del sample["custom_shell"]
        with self.assertRaises(jsonschema.ValidationError):
            self.validator.validate(sample)

    def test_timeout_and_target_are_validated(self):
        for key, value in [("timeout", 0), ("timeout", 1.5), ("agent_id", " "), ("cmd", "")]:
            sample = self.sample()
            sample[key] = value
            with self.subTest(field=key), self.assertRaises(jsonschema.ValidationError):
                self.validator.validate(sample)


if __name__ == "__main__":
    unittest.main()
