"""Guard the actual SSO identity and prevent duplicate-plugin imports."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from validate import ROOT, read_json, validate


class CanonicalBindingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['.agents', 'plugins', 'config', 'schemas']:
            shutil.copytree(ROOT / name, self.root / name)

    def edit(self, name, change):
        path = self.root / name
        value = read_json(path)
        change(value)
        path.write_text(json.dumps(value))

    def test_marketplace_adopts_actual_sso_plugin_instead_of_a_wrapper(self):
        self.assertEqual(validate(self.root)['skills'], 3)
        entry = read_json(self.root / '.agents/plugins/marketplace.json')['plugins'][0]
        self.assertEqual(entry['pluginId'], 'plugin_asdk_app_6afafd3b578c8191a62956239872dd3b')
        self.assertEqual(entry['name'], 'dev-6afafd3b578c8191a62956239872dd3b')
        apps = read_json(self.root / 'plugins/tactical-rmm/.app.json')['apps']
        self.assertEqual(next(iter(apps.values()))['id'], entry['pluginId'].removeprefix('plugin_'))

    def test_missing_plugin_id_would_create_duplicate_and_is_rejected(self):
        self.edit('.agents/plugins/marketplace.json', lambda x: x['plugins'][0].pop('pluginId'))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_old_wrapper_cannot_be_used_as_adoption_target(self):
        self.edit('.agents/plugins/marketplace.json', lambda x: x['plugins'][0].update(pluginId='Plugin_960c953284a0819184889146d979392f'))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_name_must_match_existing_sso_registration(self):
        self.edit('.agents/plugins/marketplace.json', lambda x: x['plugins'][0].update(name='tactical-rmm'))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_personal_or_other_workspace_registration_cannot_be_adopted(self):
        path = 'config/connection.json'
        for field, value in [('scope', 'USER'), ('workspace_id', 'other-workspace')]:
            with self.subTest(field=field):
                original = (self.root / path).read_bytes()
                self.edit(path, lambda x: x['appBindingVerification']['registration'].update({field: value}))
                with self.assertRaises(ValueError):
                    validate(self.root)
                (self.root / path).write_bytes(original)

    def test_binding_cannot_drift_from_registered_app(self):
        self.edit('plugins/tactical-rmm/.app.json', lambda x: next(iter(x['apps'].values())).update(id='asdk_app_OtherSyntheticTest'))
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_portable_root_cannot_hide_native_account_binding(self):
        (self.root / 'plugins/tactical-rmm/plugin.json').write_text('{"name":"tactical-rmm"}')
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_second_marketplace_entry_is_rejected(self):
        self.edit('.agents/plugins/marketplace.json', lambda x: x['plugins'].append(dict(x['plugins'][0])))
        with self.assertRaises(ValueError):
            validate(self.root)


if __name__ == '__main__':
    unittest.main()
