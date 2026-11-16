"""Exercise the complete package transition without a real app or credentials."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from bind_app import bind
from build import build
from validate import DELETED_APP_ID, ROOT, read_json, validate


def synthetic_receipt():
    return {
        "plugin_id": "plugin_asdk_app_SyntheticBindingTest",
        "scope": "WORKSPACE",
        "workspace_id": "c32d88fa-1324-44b1-9fce-9d7a166164a4",
        "mcp_url": "https://tactical-mcp.tronderdata.no/chatgpt/mcp",
        "app_manifest": {"apps": {"registered-connection": {
            "id": "asdk_app_SyntheticBindingTest", "required": True,
        }}},
    }


class AppBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in [".agents", "plugins", "config", "schemas"]:
            shutil.copytree(ROOT / name, self.root / name)
        self.package = self.root / "plugins/tactical-rmm"

    def snapshot(self):
        return {p.relative_to(self.root).as_posix(): p.read_bytes()
                for p in self.root.rglob("*") if p.is_file()}

    def test_native_transition_preserves_skills_prompt_assets_and_workspace_plugin(self):
        before = self.snapshot()
        prompt = read_json(self.package / ".codex-plugin/plugin.json")["interface"]["defaultPrompt"]
        result = bind(synthetic_receipt(), "1.3.1", self.root)
        self.assertFalse(result["published"])
        self.assertFalse(result["oauth_tested"])
        self.assertEqual(validate(self.root)["skills"], 3)
        manifest = read_json(self.package / ".codex-plugin/plugin.json")
        self.assertEqual(manifest["apps"], "./.app.json")
        self.assertNotIn("mcpServers", manifest)
        self.assertEqual(manifest["interface"]["defaultPrompt"], prompt)
        after = self.snapshot()
        for name, data in before.items():
            if "/assets/" in name or "/skills/" in name and not name.endswith("references/setup.md"):
                self.assertEqual(after[name], data)
        self.assertEqual(after[".agents/plugins/marketplace.json"], before[".agents/plugins/marketplace.json"])
        connection = read_json(self.root / "config/connection.json")
        self.assertEqual(connection["appBindingVerification"]["workspacePluginId"], "Plugin_960c953284a0819184889146d979392f")
        with contextlib.redirect_stdout(io.StringIO()):
            archive = build(self.root)
        with zipfile.ZipFile(archive) as z:
            self.assertIn("tactical-rmm/.app.json", z.namelist())
            for name in ["plugin.json", "mcp.json", ".mcp.json"]:
                self.assertNotIn("tactical-rmm/" + name, z.namelist())

    def test_wrong_or_unverified_registration_leaves_source_untouched(self):
        for field, value in [("scope", "USER"), ("workspace_id", "other-workspace"),
                             ("mcp_url", "https://example.invalid/mcp"),
                             ("plugin_id", "Plugin_960c953284a0819184889146d979392f")]:
            with self.subTest(field=field):
                before = self.snapshot()
                receipt = synthetic_receipt()
                receipt[field] = value
                with self.assertRaises(ValueError):
                    bind(receipt, "1.3.1", self.root)
                self.assertEqual(self.snapshot(), before)

    def test_deleted_app_cannot_be_bound(self):
        receipt = synthetic_receipt()
        receipt["plugin_id"] = "plugin_" + DELETED_APP_ID
        receipt["app_manifest"]["apps"]["registered-connection"]["id"] = DELETED_APP_ID
        before = self.snapshot()
        with self.assertRaises(ValueError):
            bind(receipt, "1.3.1", self.root)
        self.assertEqual(self.snapshot(), before)

    def test_portable_root_and_parallel_mcp_cannot_mask_native_connection(self):
        before = self.snapshot()
        bind(synthetic_receipt(), "1.3.1", self.root)
        for name in ["plugin.json", "mcp.json", ".mcp.json"]:
            with self.subTest(name=name):
                path = self.package / name
                path.write_bytes(before["plugins/tactical-rmm/" + name])
                with self.assertRaises(ValueError):
                    validate(self.root)
                path.unlink()

    def test_binding_cannot_drift_from_registration_receipt(self):
        bind(synthetic_receipt(), "1.3.1", self.root)
        path = self.package / ".app.json"
        value = read_json(path)
        value["apps"]["tactical-rmm"]["id"] = "asdk_app_OtherSyntheticTest"
        path.write_text(json.dumps(value))
        with self.assertRaises(ValueError):
            validate(self.root)


if __name__ == "__main__":
    unittest.main()
