"""Download-to-source behavior, unsafe archives, preservation and update failure."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import warnings
import zipfile

MODULE = Path(__file__).parents[1] / "scripts/package_lab.py"
SPEC = importlib.util.spec_from_file_location("restore_lab", MODULE)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)
EXAMPLE = Path(__file__).parents[1] / "examples/research-brief.json"


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="builder-restore-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.package = self.base / "source"
        lab.scaffold(lab.read_json(EXAMPLE), self.package)
        self.archive = self.base / "release.zip"
        self.release = lab.pack(self.package, self.archive)

    def rewrite(self, entries, compression=zipfile.ZIP_STORED):
        archive = self.base / "custom.zip"
        with warnings.catch_warnings(), zipfile.ZipFile(archive, "w", compression=compression) as writer:
            warnings.simplefilter("ignore", UserWarning)
            for name, content in entries:
                writer.writestr(name, content)
        return archive, hashlib.sha256(archive.read_bytes()).hexdigest()

    def entries(self):
        with zipfile.ZipFile(self.archive) as archive:
            return [(entry.filename, archive.read(entry)) for entry in archive.infolist()]

    def test_cli_restore_preserves_complete_license_and_reproducible_package(self):
        restored = self.base / "restored"
        run = subprocess.run([sys.executable, "-B", str(MODULE), "restore", str(self.archive), str(restored), "--sha256", self.release["sha256"]], capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["status"], "restored-structural-pass")
        self.assertEqual(result["installation"], "not-performed")
        self.assertEqual(result["publisherIdentity"], "not-verified-by-checksum")
        self.assertEqual((restored / "LICENSE").read_bytes(), (self.package / "LICENSE").read_bytes())
        for name, sha in result["files_sha256"].items():
            self.assertEqual(hashlib.sha256((restored / name).read_bytes()).hexdigest(), sha)
        self.assertEqual(lab.pack(restored, self.base / "repacked.zip")["sha256"], self.release["sha256"])

    def test_update_never_replaces_prior_empty_or_edited_versions(self):
        target = self.base / "version-one"
        lab.restore(self.archive, target, self.release["sha256"])
        edited = target / "README.md"
        edited.write_bytes(b"Exact customer edit\r\n")
        for existing in (target, self.base / "empty"):
            existing.mkdir(exist_ok=True)
            with self.assertRaisesRegex(ValueError, "already exists"):
                lab.restore(self.archive, existing, self.release["sha256"])
        lab.restore(self.archive, self.base / "version-two", self.release["sha256"])
        self.assertEqual(edited.read_bytes(), b"Exact customer edit\r\n")

    def test_bad_hash_and_invalid_contract_refuse_before_output(self):
        target = self.base / "refused"
        for checksum in ("0" * 64, "x" * 64, "short"):
            with self.assertRaises(ValueError):
                lab.restore(self.archive, target, checksum)
            self.assertFalse(target.exists())
        archive, checksum = self.rewrite([(name, data) for name, data in self.entries() if name != "LICENSE"])
        with self.assertRaisesRegex(ValueError, "LICENSE"):
            lab.restore(archive, target, checksum)
        self.assertFalse(target.exists())

    def test_paths_duplicates_case_and_file_directory_conflicts_refuse_before_output(self):
        names = ["../escape.md", "/absolute.md", "a\\b.md", "aux.md", "a:b.md", "folder//file.md", "trailing."]
        variants = [[(name, b"unsafe")] for name in names]
        variants += [[("README.md", b"duplicate")], [("readme.md", b"collision")], [("references", b"file"), ("references/item.md", b"conflict")], [("references/A.md", b"a"), ("References/b.md", b"b")]]
        for additional in variants:
            with self.subTest(entries=[str(v[0]) for v in additional]):
                archive, checksum = self.rewrite(self.entries() + additional)
                target = self.base / "refused"
                with self.assertRaises(ValueError):
                    lab.restore(archive, target, checksum)
                self.assertFalse(target.exists())
                self.assertFalse((self.base / "escape.md").exists())

    def test_link_special_and_directory_payload_refuse_before_output(self):
        for mode, name, content in [(stat.S_IFLNK | 0o777, "references/link.md", b"../README.md"), (stat.S_IFIFO | 0o600, "references/fifo.txt", b""), (stat.S_IFDIR | 0o755, "references/", b"hidden data")]:
            entry = zipfile.ZipInfo(name); entry.create_system = 3; entry.external_attr = mode << 16
            archive, checksum = self.rewrite(self.entries() + [(entry, content)])
            with self.assertRaises(ValueError):
                lab.restore(archive, self.base / "refused", checksum)
            self.assertFalse((self.base / "refused").exists())

    def test_invalid_utf8_secret_and_crc_damage_refuse_before_output(self):
        for content in (b"\xc3\x28", b"sk-proj-" + b"A" * 40):
            archive, checksum = self.rewrite(self.entries() + [("references/bad.txt", content)])
            with self.assertRaises(ValueError):
                lab.restore(archive, self.base / "refused", checksum)
            self.assertFalse((self.base / "refused").exists())
        raw = bytearray(self.archive.read_bytes())
        # Change one stored byte without changing the ZIP's CRC, then supply the correct archive hash.
        name_size, extra_size = struct.unpack_from("<HH", raw, 26)
        raw[30 + name_size + extra_size] ^= 1
        damaged = self.base / "crc.zip"; damaged.write_bytes(raw)
        result = subprocess.run([sys.executable, "-B", str(MODULE), "restore", str(damaged), str(self.base / "refused"), "--sha256", hashlib.sha256(raw).hexdigest()], capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stderr)["status"], "fail")
        self.assertFalse((self.base / "refused").exists())

    def test_bounded_expansion_entry_count_and_archive_size(self):
        archive, checksum = self.rewrite(self.entries() + [("references/large.txt", b"a" * (lab.MAX_MEMBER + 1))], zipfile.ZIP_DEFLATED)
        with self.assertRaises(ValueError):
            lab.restore(archive, self.base / "refused", checksum)
        archive, checksum = self.rewrite(self.entries() + [(f"references/{i}.txt", b"x") for i in range(lab.MAX_ENTRIES)])
        with self.assertRaises(ValueError):
            lab.restore(archive, self.base / "refused", checksum)
        with patch.object(lab, "MAX_RESTORED", 1), self.assertRaises(ValueError):
            lab.restore(self.archive, self.base / "refused", self.release["sha256"])
        with patch.object(lab, "MAX_ARCHIVE", 1), self.assertRaises(ValueError):
            lab.restore(self.archive, self.base / "refused", self.release["sha256"])
        self.assertFalse((self.base / "refused").exists())

    def test_deflated_text_node_source_and_explicit_directory_entries(self):
        directory = zipfile.ZipInfo("scripts/"); directory.external_attr = (stat.S_IFDIR | 0o755) << 16
        archive, checksum = self.rewrite(self.entries() + [(directory, b""), ("scripts/local.mjs", b"// Inspectable Node fixture; never executed during restore.\n")], zipfile.ZIP_DEFLATED)
        restored = self.base / "restored"
        result = lab.restore(archive, restored, checksum)
        self.assertIn("scripts/local.mjs", result["files_sha256"])
        self.assertEqual((restored / "scripts/local.mjs").read_bytes(), b"// Inspectable Node fixture; never executed during restore.\n")

    def test_partial_write_is_preserved_and_fresh_retry_succeeds(self):
        target = self.base / "partial"
        original = Path.open
        def fail_second(path, *args, **kwargs):
            if path == target / ".claude-plugin/plugin.json":
                raise OSError("Injected session-owned write failure")
            return original(path, *args, **kwargs)
        with patch.object(Path, "open", fail_second), self.assertRaisesRegex(ValueError, "preserve the partial"):
            lab.restore(self.archive, target, self.release["sha256"])
        before = {str(path.relative_to(target)): path.read_bytes() for path in target.rglob("*") if path.is_file()}
        self.assertTrue(target.is_dir())
        with self.assertRaises(ValueError):
            lab.restore(self.archive, target, self.release["sha256"])
        lab.restore(self.archive, self.base / "fresh-retry", self.release["sha256"])
        self.assertEqual(before, {str(path.relative_to(target)): path.read_bytes() for path in target.rglob("*") if path.is_file()})

    def test_linked_output_parent_is_refused(self):
        real = self.base / "real"; real.mkdir()
        alias = self.base / "alias"
        try:
            alias.symlink_to(real, target_is_directory=True)
        except OSError:
            self.skipTest("Host cannot create directory links")
        with self.assertRaisesRegex(ValueError, "ordinary"):
            lab.restore(self.archive, alias / "escaped", self.release["sha256"])
        self.assertFalse((real / "escaped").exists())


if __name__ == "__main__":
    unittest.main()
