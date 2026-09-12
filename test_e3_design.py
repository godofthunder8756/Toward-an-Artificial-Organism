"""Read-only verifier tests using only self-created external temporary fixtures.

No original freeze/data file is copied, changed or repaired. subprocesses use
-B; imports have no verification side effects. Filesystem snapshots assert
that both successful and failed verification leave fixture contents untouched.
"""

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import importlib
import io
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import verify_e3_design as verifier


class TestDesignVerifier(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="e3-design-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.payload = self.root / "input.txt"
        self.payload.write_bytes(b"independent engineering fixture\n")
        self.manifest = self.root / "design.json"
        self.data = {
            "kind": "engineering_only_design_freeze",
            "external_preregistration": False,
            "implementation_present_at_snapshot": False,
            "engineering_execution_requires_implementation_validation": True,
            "final_target_draws_permitted": False,
            "confirmatory_h2_permitted": False,
            "files": {"input.txt": self.entry(self.payload.read_bytes())},
        }
        self.write_manifest()

    @staticmethod
    def entry(content):
        return {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}

    def write_manifest(self):
        self.manifest.write_text(json.dumps(self.data), encoding="utf-8")

    def snapshot(self):
        result = {}
        for path in self.root.rglob("*"):
            name = path.relative_to(self.root).as_posix()
            if path.is_symlink():
                result[name] = ("link", str(path.readlink()))
            elif path.is_file():
                info = path.stat()
                result[name] = ("file", path.read_bytes(), info.st_mtime_ns, info.st_mode)
            else:
                result[name] = ("directory",)
        return result

    def audit(self, expected, fragment=None, manifest=None):
        before = self.snapshot()
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = verifier.verify(self.root, self.manifest.name if manifest is None else manifest)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")
        self.assertIs(result["ok"], expected)
        self.assertIsInstance(result["failures"], list)
        if fragment is not None:
            self.assertIn(fragment, " ".join(result["failures"]))
        # An ordinary caller can serialize the returned result without conversion.
        self.assertEqual(json.loads(json.dumps(result)), result)
        return result

    def test_minimal_valid_fixture_no_hardcoded_23(self):
        result = self.audit(True)
        self.assertEqual(result["file_count"], 1)
        self.assertEqual(result["files_checked"], 1)
        self.assertEqual(result["failures"], [])
        self.audit(True, manifest=self.manifest)
        self.audit(True, manifest=Path(self.manifest.name))

    def test_all_entries_including_empty_nested_and_binary_files(self):
        nested = self.root / "nested"
        nested.mkdir()
        for name, content in (("nested/zero", b""), ("nested/binary", bytes(range(256)))):
            (self.root / name).write_bytes(content)
            self.data["files"][name] = self.entry(content)
        self.write_manifest()
        result = self.audit(True)
        self.assertEqual(result["files_checked"], 3)
        (nested / "binary").write_bytes(bytes(reversed(range(256))))
        result = self.audit(False, "sha256 mismatch")
        self.assertEqual(result["files_checked"], 3)
        self.assertFalse(any("bytes mismatch" in failure for failure in result["failures"]))

    def test_modified_size_missing_file_and_directory_are_failures(self):
        self.payload.write_bytes(b"short")
        result = self.audit(False, "bytes mismatch")
        self.assertTrue(any("sha256 mismatch" in failure for failure in result["failures"]))
        self.payload.unlink()
        self.audit(False)
        self.payload.mkdir()
        self.audit(False, "not a regular file")

    def test_nonempty_file_map_and_top_level_object_required(self):
        for files in (None, [], {}, "files", 23):
            self.data["files"] = files
            self.write_manifest()
            self.audit(False, "nonempty JSON object")
        for top in ([], None, 0, "manifest"):
            self.manifest.write_text(json.dumps(top), encoding="utf-8")
            self.audit(False, "JSON object")

    def test_exact_kind_and_strict_boolean_permissions(self):
        for kind in ("engineering_only", "final", "engineering_only_design_freeze ", None, False):
            self.data["kind"] = kind
            self.write_manifest()
            self.audit(False, "kind must be")
        self.data["kind"] = "engineering_only_design_freeze"
        expected = {
            "external_preregistration": False,
            "implementation_present_at_snapshot": False,
            "engineering_execution_requires_implementation_validation": True,
            "final_target_draws_permitted": False,
            "confirmatory_h2_permitted": False,
        }
        for field, value in expected.items():
            for bad in (not value, 0, 1, 0.0, 1.0, "false", "true", None, [], {}):
                self.data[field] = bad
                self.write_manifest()
                self.audit(False, field)
            del self.data[field]
            self.write_manifest()
            self.audit(False, field)
            self.data[field] = value
        self.write_manifest()
        self.audit(True)

    def test_entry_keys_size_integer_and_lowercase_sha256(self):
        entry = self.entry(self.payload.read_bytes())
        for bad in (None, [], "entry", 1, {}, {"bytes": 1}, {**entry, "other": 0}):
            self.data["files"]["input.txt"] = bad
            self.write_manifest()
            self.audit(False, "exactly bytes and sha256")
        for bad in (True, False, -1, 1.0, "1", None, [], {}):
            self.data["files"]["input.txt"] = {**entry, "bytes": bad}
            self.write_manifest()
            self.audit(False, "nonnegative JSON integer")
        for bad in (True, 1, None, [], "", "a" * 63, "a" * 65,
                    "g" * 64, "A" * 64, "a" * 64 + "\n"):
            self.data["files"]["input.txt"] = {**entry, "sha256": bad}
            self.write_manifest()
            self.audit(False, "lowercase hexadecimal")

    def test_json_duplicates_rejected_at_every_depth(self):
        entry_json = json.dumps(self.data["files"]["input.txt"])
        original = json.dumps(self.data)
        fixtures = (
            original[:-1] + ', "kind": "engineering_only_design_freeze"}',
            original[:-1] + ', "final_target_draws_permitted": false}',
            original.replace('"input.txt": ' + entry_json,
                             '"input.txt": ' + entry_json + ', "input.txt": ' + entry_json),
            original.replace(entry_json, entry_json[:-1] + ', "bytes": 1}'),
            original[:-1] + ', "extra": {"same": 1, "same": 2}}',
        )
        for raw in fixtures:
            self.manifest.write_text(raw, encoding="utf-8")
            self.audit(False, "duplicate JSON key")

    def test_invalid_json_utf8_and_nonstandard_constants(self):
        for raw in (b"{", b"", b"\xff", b"{} {}", b'{"bad": NaN}',
                    b'{"bad": Infinity}', b'{"bad": -Infinity}'):
            self.manifest.write_bytes(raw)
            self.audit(False)
        self.manifest.unlink()
        self.audit(False)

    def test_paths_cannot_escape_or_use_noncanonical_aliases(self):
        entry = self.entry(self.payload.read_bytes())
        for name in ("../outside", "/input.txt", "//server/share", "C:/input.txt",
                     "C:input.txt", "input.txt:stream", "..\\outside", "nested\\file",
                     "./input.txt", "nested/../input.txt", "nested//file", "input.txt/",
                     "", "input.txt\x00", "input.txt.", "input.txt "):
            self.data["files"] = {name: entry}
            self.write_manifest()
            self.audit(False)
        self.data["files"] = {"input.txt": entry}
        self.write_manifest()
        for name in ("../design.json", "./design.json", "nested/../design.json",
                     "C:design.json", "design.json:stream"):
            self.audit(False, manifest=name)
        # An outside manifest is never read, even if its contents are valid.
        with tempfile.TemporaryDirectory(prefix="e3-outside-") as outside:
            external = Path(outside) / "design.json"
            external.write_bytes(self.manifest.read_bytes())
            self.audit(False, manifest=external)

    def make_link(self, link, target, directory=False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError) as error:
            self.skipTest(f"OS does not permit symlink fixtures: {error}")

    def test_file_symlink_inside_workspace_is_rejected(self):
        link = self.root / "alias"
        self.make_link(link, self.payload)
        self.data["files"] = {"alias": self.entry(self.payload.read_bytes())}
        self.write_manifest()
        self.audit(False, "symlink")

    def test_directory_symlink_and_outside_target_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix="e3-link-target-") as outside:
            target = Path(outside) / "input.txt"
            target.write_bytes(self.payload.read_bytes())
            self.make_link(self.root / "linked", Path(outside), directory=True)
            self.data["files"] = {"linked/input.txt": self.entry(target.read_bytes())}
            self.write_manifest()
            self.audit(False, "symlink")
            (self.root / "linked").unlink()

    def test_dangling_link_and_manifest_link_are_rejected(self):
        link = self.root / "dangling"
        self.make_link(link, self.root / "absent")
        self.data["files"] = {"dangling": self.entry(b"")}
        self.write_manifest()
        self.audit(False, "symlink")
        manifest_link = self.root / "manifest-link.json"
        self.make_link(manifest_link, self.manifest)
        self.audit(False, "symlink", manifest=manifest_link.name)

    def test_root_symlink_is_not_silently_resolved(self):
        actual = self.root / "actual"
        actual.mkdir()
        self.make_link(self.root / "alias", actual, directory=True)
        before = self.snapshot()
        result = verifier.verify(self.root / "alias", "design.json")
        self.assertIs(result["ok"], False)
        self.assertIn("symlink", " ".join(result["failures"]))
        self.assertEqual(self.snapshot(), before)

    def test_link_and_reparse_metadata_rejection_without_os_link_privilege(self):
        # Deterministic checks supplement, rather than replace, real-link tests.
        nested = self.root / "nested"
        nested.mkdir()
        child = nested / "child"
        child.write_bytes(b"child")
        self.data["files"]["nested/child"] = self.entry(b"child")
        self.write_manifest()
        real_lstat = Path.lstat
        before = self.snapshot()
        for blocked in (self.root, self.manifest, self.payload, nested):
            for mode, attributes in ((stat.S_IFLNK | 0o777, 0),
                                     (stat.S_IFREG | 0o600, stat.FILE_ATTRIBUTE_REPARSE_POINT)):
                def fake_lstat(path, *, target=blocked, st_mode=mode, flags=attributes):
                    if path == target:
                        return SimpleNamespace(st_mode=st_mode, st_file_attributes=flags)
                    return real_lstat(path)

                with patch.object(Path, "lstat", fake_lstat):
                    result = verifier.verify(self.root, self.manifest.name)
                self.assertIs(result["ok"], False)
                self.assertIn("symlink or reparse point", " ".join(result["failures"]))
                self.assertEqual(self.snapshot(), before)

    def test_twenty_three_entries_all_checked_and_failures_accumulate(self):
        for index in range(22):
            name = f"fixture-{index}.txt"
            content = f"fixture {index}".encode("ascii")
            (self.root / name).write_bytes(content)
            self.data["files"][name] = self.entry(content)
        self.write_manifest()
        result = self.audit(True)
        self.assertEqual((result["file_count"], result["files_checked"]), (23, 23))
        (self.root / "fixture-0.txt").unlink()
        (self.root / "fixture-1.txt").write_bytes(b"tampered")
        result = self.audit(False)
        self.assertEqual((result["file_count"], result["files_checked"]), (23, 22))
        self.assertTrue(any("fixture-0.txt" in error for error in result["failures"]))
        self.assertTrue(any("fixture-1.txt" in error for error in result["failures"]))

    def test_io_errors_are_results_and_do_not_fix_anything(self):
        before = self.snapshot()
        with patch.object(Path, "open", side_effect=PermissionError("fixture access denied")):
            result = verifier.verify(self.root, self.manifest.name)
        self.assertIs(result["ok"], False)
        self.assertIn("access denied", " ".join(result["failures"]))
        self.assertEqual(self.snapshot(), before)
        self.audit(True)
        result = verifier.verify(self.root / "missing", self.manifest.name)
        self.assertIs(result["ok"], False)

    def test_main_json_stdout_exit_zero_or_one_and_no_sidecars(self):
        cases = ((["--root", str(self.root), "--manifest", self.manifest.name], 0),
                 (["--root", str(self.root), "--manifest", "missing.json"], 1),
                 (["--unknown"], 1), (["--root"], 1), (["--help"], 1))
        for arguments, expected_status in cases:
            before = self.snapshot()
            stdout, stderr = io.StringIO(), io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                status = verifier.main(arguments)
            self.assertEqual(status, expected_status)
            self.assertIs(json.loads(stdout.getvalue())["ok"], expected_status == 0)
            self.assertEqual(stderr.getvalue(), "")
            self.assertEqual(len(stdout.getvalue().splitlines()), 1)
            self.assertEqual(self.snapshot(), before)

    def test_cli_subprocess_and_import_guard_with_bytecode_disabled(self):
        script = str(Path(verifier.__file__).resolve())
        for contents, expected in ((self.manifest.read_bytes(), 0), (b"{bad", 1)):
            self.manifest.write_bytes(contents)
            before = self.snapshot()
            process = subprocess.run(
                [sys.executable, "-B", script, "--root", str(self.root),
                 "--manifest", self.manifest.name],
                cwd=self.root, capture_output=True, text=True, check=False,
            )
            self.assertEqual(process.returncode, expected)
            self.assertIs(json.loads(process.stdout)["ok"], expected == 0)
            self.assertEqual(process.stderr, "")
            self.assertEqual(self.snapshot(), before)
        stdout, stderr = io.StringIO(), io.StringIO()
        # Reload exercises module top-level code; no manifest should be opened.
        with patch.object(Path, "open", side_effect=AssertionError("import attempted I/O")):
            with redirect_stdout(stdout), redirect_stderr(stderr):
                importlib.reload(verifier)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "")


if __name__ == "__main__":
    unittest.main()