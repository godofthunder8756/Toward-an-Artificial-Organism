"""Additive check that PR #10 artifacts are unchanged by the v1 errata.

Compares the working tree with commit 5f6446f, the Stage 2 results commit.
New errata files are not part of that tree. This test does not train.
"""

from __future__ import annotations

import hashlib
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RESULTS_COMMIT = "5f6446f29b74d837b4e16057f02b408e5eb56bac"
ORIGINAL_MANIFEST_SHA = "17a6ff525261e43d951ae07546717c496bca20cc06e43478cb72e3a70aca2e4d"
CORRECTED_MANIFEST_SHA = "5b533f6ed372bbef18508aeff809a2dafe93fd9ee9b791e573058a0dd1dffb2a"
ORIGINAL_TREE = "1349a6786e92d81ba194d866d48dd88304961b5acda900fc5cadc3c52998f7f9"
CORRECTED_TREE = "d00ff89b5c4be698a690c0c472a6bbdf00c1a0279af5d82a4a8c907d22696ee4"
PROTOCOL_SHA = "eca2121c5972138580ebd8ababb1cd40879a4c20404e925e129becd7e778ea40"


def _git_bytes(spec: str) -> bytes:
    return subprocess.check_output(["git", "show", spec], cwd=ROOT)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _commit_paths(commit: str) -> list[str]:
    raw = subprocess.check_output(["git", "ls-tree", "-r", "-z", commit], cwd=ROOT)
    paths = []
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        _meta, path = entry.split(b"\t", 1)
        paths.append(path.decode("utf-8"))
    return paths


class OriginalArtifactHashTests(unittest.TestCase):
    def test_every_results_commit_file_is_unchanged(self):
        paths = _commit_paths(RESULTS_COMMIT)
        self.assertGreater(len(paths), 8000)
        diff = subprocess.run(
            ["git", "diff", "--name-only", "--ignore-submodules=all", RESULTS_COMMIT],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(diff.stdout, "")
        study = [
            path
            for path in paths
            if path.startswith("frozen_recurrent_compensation")
            or path.startswith("test_frozen_recurrent_compensation.py")
            or path.startswith("FROZEN_RECURRENT_COMPENSATION_")
        ]
        self.assertGreater(len(study), 60)
        changed = []
        for path in study:
            recorded = _sha256(_git_bytes("%s:%s" % (RESULTS_COMMIT, path)))
            if _sha256((ROOT / path).read_bytes()) != recorded:
                changed.append(path)
        self.assertEqual(changed, [])

    def test_stage0_provenance_copies(self):
        original = (ROOT / "results_v1_errata" / "STAGE0_MANIFEST_original_0fed34e").read_bytes()
        corrected = (ROOT / "results_v1_errata" / "STAGE0_MANIFEST_corrected_fd720ee").read_bytes()
        self.assertEqual(_sha256(original), ORIGINAL_MANIFEST_SHA)
        self.assertEqual(_sha256(corrected), CORRECTED_MANIFEST_SHA)
        self.assertEqual(
            original,
            _git_bytes("0fed34ebad4bee2b794ce1324ec286ae0a2c68ab:frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json"),
        )
        self.assertEqual(
            corrected,
            _git_bytes("fd720ee78ae7d60b7db425baca55bc1fca7af6b9:frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json"),
        )
        self.assertIn(ORIGINAL_TREE, original.decode("utf-8"))
        self.assertIn(CORRECTED_TREE, corrected.decode("utf-8"))
        live = (ROOT / "frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json").read_bytes()
        self.assertEqual(live, corrected)

    def test_protocol_and_results_files_keep_their_hashes(self):
        protocol = (ROOT / "frozen_recurrent_compensation_protocol_FINAL.md").read_bytes()
        self.assertEqual(_sha256(protocol), PROTOCOL_SHA)
        results_md = ROOT / "frozen_recurrent_compensation_results_v1/stage2/RESULTS.md"
        results_json = ROOT / "frozen_recurrent_compensation_results_v1/stage2/results.json"
        self.assertEqual(results_md.read_bytes(), _git_bytes("%s:%s" % (RESULTS_COMMIT, results_md.relative_to(ROOT).as_posix())))
        self.assertEqual(results_json.read_bytes(), _git_bytes("%s:%s" % (RESULTS_COMMIT, results_json.relative_to(ROOT).as_posix())))


if __name__ == "__main__":
    unittest.main()
