import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("release", Path(__file__).parents[1] / "scripts/verify_builder_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTests(unittest.TestCase):
    def test_missing_and_escaping_references_fail(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch) / "plugin"
            root.mkdir()
            (Path(scratch) / "outside.md").write_text("outside", encoding="utf-8")
            readme = root / "README.md"
            for link in ("missing.md", "../outside.md", "%2E%2E/outside.md"):
                with self.subTest(link=link):
                    readme.write_text(f"[reference]({link})", encoding="utf-8")
                    with self.assertRaises(ValueError):
                        release.relative_references(root)

    def test_existing_reference_and_external_url(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            (root / "guide.md").write_text("guide", encoding="utf-8")
            (root / "README.md").write_text("[local](guide.md#part) [source](https://example.org) [anchor](#part)", encoding="utf-8")
            self.assertEqual(release.relative_references(root), 1)

    def test_partial_catalog_registration_fails(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            self.write_catalogs(root, [{"name": "starlight-builder-lab"}], [])
            with self.assertRaises(ValueError):
                release.catalogs(root)

    def test_mutable_native_revision_fails(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            portable = {"name": "starlight-builder-lab", "source": {"source": "local", "path": "./plugins/starlight-builder-lab"}}
            native = {"name": "starlight-builder-lab", "source": {"source": "git-subdir", "url": release.REPOSITORY,
                       "path": "plugins/starlight-builder-lab", "sha": "main"}}
            self.write_catalogs(root, [portable], [native])
            with self.assertRaises(ValueError):
                release.catalogs(root)

    def test_end_to_end_preserves_release_boundaries(self):
        result = release.verify()
        self.assertEqual(result["status"], "offline-release-checks-pass")
        self.assertEqual(result["goals_reported"], 6)
        for field in ("host_behavior", "directory_approval", "commerce"):
            self.assertEqual(result[field], "not-proven-by-this-check")

    @staticmethod
    def write_catalogs(root, codex, claude):
        for folder, entries in ((".agents/plugins", codex), (".claude-plugin", claude)):
            (root / folder).mkdir(parents=True)
            (root / folder / "marketplace.json").write_text(json.dumps({"plugins": entries}), encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
