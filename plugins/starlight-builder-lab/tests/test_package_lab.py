"""Behavior checks: preservation, package integrity and honest release boundaries."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

MODULE = Path(__file__).parents[1] / "scripts/package_lab.py"
SPEC = importlib.util.spec_from_file_location("package_lab", MODULE)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


def spec():
    return {"name": "example-workflow", "version": "0.1.0",
            "description": "Create an inspectable research brief.", "author": "Example publisher",
            "license": "LicenseRef-Example", "license_text": "Example test license text.",
            "skills": [{"name": "research-brief", "description": "Use when preparing a cited brief.",
                        "instructions": "Use supplied sources. Mark unavailable evidence unknown."}]}


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.package = self.base / "package"

    def build(self):
        return lab.scaffold(spec(), self.package)

    def test_generate_validate_and_zip_roundtrip(self):
        self.build()
        result = lab.check(self.package)
        self.assertEqual(result["skills"], 1)
        self.assertEqual(result["hostTests"], "not-run")
        zip_path = self.base / "first.zip"
        result = lab.pack(self.package, zip_path)
        with zipfile.ZipFile(zip_path) as archive:
            self.assertIn("plugin.json", archive.namelist())
            self.assertEqual(json.loads(archive.read("plugin.json"))["name"], "example-workflow")
            archive.extractall(self.base / "unpacked")
        self.assertEqual(lab.check(self.base / "unpacked")["status"], "structural-pass")
        second = lab.pack(self.package, self.base / "second.zip")
        self.assertEqual(result["sha256"], second["sha256"])
        self.assertEqual(result["sha256"], "11cf5adb7781594369ab2ce16066893ae191fa4d3ca1ea7d8970b93db2eea8b5")

    def test_invalid_spec_does_not_create_output(self):
        invalid = spec()
        invalid["skills"].append(copy.deepcopy(invalid["skills"][0]))
        with self.assertRaises(ValueError):
            lab.scaffold(invalid, self.package)
        self.assertFalse(self.package.exists())

    def test_names_cannot_escape_package(self):
        for name in ("../escape", "a/b", "A-name", "CON:", "con", "lpt1"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                value = spec()
                value["skills"][0]["name"] = name
                lab.scaffold(value, self.package)
        self.assertFalse(self.package.exists())

    def test_scaffold_and_zip_preserve_existing_work(self):
        self.build()
        sentinel = (self.package / "plugin.json").read_bytes()
        with self.assertRaises(ValueError):
            lab.scaffold(spec(), self.package)
        self.assertEqual(sentinel, (self.package / "plugin.json").read_bytes())
        zip_path = self.base / "existing.zip"
        zip_path.write_bytes(b"existing buyer work")
        with self.assertRaises(ValueError):
            lab.pack(self.package, zip_path)
        self.assertEqual(zip_path.read_bytes(), b"existing buyer work")

    def test_zip_cannot_be_written_inside_source(self):
        self.build()
        with self.assertRaises(ValueError):
            lab.pack(self.package, self.package / "output.zip")

    def test_secret_and_environment_files_block_packaging(self):
        self.build()
        (self.package / ".env.production").write_text("not a secret", encoding="utf-8")
        with self.assertRaises(ValueError):
            lab.pack(self.package, self.base / "bad.zip")
        self.assertFalse((self.base / "bad.zip").exists())

    def test_failed_zip_write_removes_only_the_new_output(self):
        self.build()
        output = self.base / "failed.zip"
        with patch.object(zipfile.ZipFile, "writestr", side_effect=OSError("Simulated write failure")):
            with self.assertRaises(OSError):
                lab.pack(self.package, output)
        self.assertFalse(output.exists())
        self.assertEqual(lab.check(self.package)["skills"], 1)

    def test_private_key_and_personal_path_detection(self):
        examples = [prefix + "a" * 32 for prefix in ("sk-", "polar_" + "oat_", "sk_" + "live_", "whsec_", "ghp_")]
        examples.append("/".join(["C:", "Users", "sample", "private"]))
        examples.append("Sources:\n" + "/".join(["", "Users", "sample", "private"]))
        for content in examples:
            value = spec()
            value["skills"][0]["instructions"] = content
            with self.subTest(content=content[:6]), self.assertRaises(ValueError):
                lab.scaffold(value, self.package)
        self.assertFalse(self.package.exists())

    def test_public_url_does_not_look_like_a_personal_path(self):
        value = spec()
        value["skills"][0]["instructions"] = "Read https://example.org/home/about/ when requested."
        lab.scaffold(value, self.package)
        self.assertEqual(lab.check(self.package)["status"], "structural-pass")

    def test_unquoted_frontmatter_is_accepted(self):
        self.build()
        path = self.package / "skills/research-brief/SKILL.md"
        path.write_text("---\nname: research-brief\ndescription: Prepare a cited brief.\n---\n\nUse supplied sources.\n", encoding="utf-8")
        self.assertEqual(lab.check(self.package)["skills"], 1)

    def test_newlines_do_not_change_zip_bytes(self):
        self.build()
        first = lab.pack(self.package, self.base / "lf.zip")
        for path in lab.package_files(self.package):
            text = path.read_text(encoding="utf-8")
            path.write_bytes(text.replace("\n", "\r\n").encode("utf-8"))
        second = lab.pack(self.package, self.base / "crlf.zip")
        self.assertEqual(first["sha256"], second["sha256"])

    def test_missing_parent_is_preserved(self):
        with self.assertRaises(ValueError):
            lab.scaffold(spec(), self.base / "missing/package")
        self.assertFalse((self.base / "missing").exists())

    @unittest.skipUnless(os.name == "nt", "Windows junction behavior")
    def test_windows_junction_does_not_import_external_directory(self):
        self.build()
        external = self.base / "outside"
        external.mkdir()
        (external / "secret.md").write_text("external data", encoding="utf-8")
        junction = self.package / "references"
        result = subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(external)], capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        with self.assertRaises(ValueError):
            lab.pack(self.package, self.base / "junction.zip")
        self.assertFalse((self.base / "junction.zip").exists())
        self.assertEqual((external / "secret.md").read_text(encoding="utf-8"), "external data")

    def test_native_manifest_drift_blocks_package(self):
        self.build()
        path = self.package / ".claude-plugin/plugin.json"
        value = lab.read_json(path)
        value["version"] = "2.0.0"
        lab.write_json(path, value)
        with self.assertRaises(ValueError):
            lab.check(self.package)

    def test_nested_skill_blocks_package(self):
        self.build()
        nested = self.package / "skills/research-brief/nested"
        nested.mkdir()
        (nested / "SKILL.md").write_text("unexpected", encoding="utf-8")
        with self.assertRaises(ValueError):
            lab.check(self.package)

    def test_symlink_cannot_import_external_file(self):
        self.build()
        external = self.base / "outside.md"
        external.write_text("outside", encoding="utf-8")
        try:
            (self.package / "references").mkdir()
            (self.package / "references/external.md").symlink_to(external)
        except OSError:
            self.skipTest("Symlink permission unavailable on this host")
        with self.assertRaises(ValueError):
            lab.check(self.package)


if __name__ == "__main__":
    unittest.main()
