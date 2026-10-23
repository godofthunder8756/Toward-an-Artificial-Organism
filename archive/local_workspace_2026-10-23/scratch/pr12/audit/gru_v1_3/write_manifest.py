"""Write the implementation manifest. Run after the code is finished and before any checkpoint load."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from audit.gru_v1_3.replay_map import REPLAY_MAP
from audit.gru_v1_3.run_audit import json_ready

ROOT = Path("/workspace")
CODE_ROOTS = [ROOT / "audit"]
OUT = ROOT / "audit/gru_v1_3/IMPLEMENTATION_MANIFEST.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def code_files():
    found = []
    for root in CODE_ROOTS:
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if "results" in path.parts:
                continue
            if path.name == "IMPLEMENTATION_MANIFEST.json":
                continue
            if path.suffix not in {".py", ".sh"}:
                continue
            found.append(path)
    return sorted(found)


def main():
    files = {str(path.relative_to(ROOT)): sha256(path) for path in code_files()}
    payload = {
        "audit": "GRU hidden-state oracle-accessibility audit spec v1.3",
        "spec_sha256": sha256(ROOT / "review/gru_own_error_audit_spec_v1_3.md"),
        "roster_sha256": sha256(ROOT / "review/gru_own_error_audit_roster_v1.json"),
        "code_files": files,
        "replay_map": json_ready(REPLAY_MAP),
        "zero_variance_rule": REPLAY_MAP["zero_variance_rule"],
        "uniform_weight_r2": REPLAY_MAP["uniform_weight_r2"],
        "notes": {
            "n1": "One zero-variance rule: weighted population variance <= 1e-24.",
            "n2": "Uniform-weight R^2 uses uniform-weight Var(q) and has no floor label.",
            "F4": "Combined 1e-12 tolerance also applies to the e_P reconstruction.",
            "F5": "A checkpoint meets the floor only if C1 and C2 both do; below if either does; otherwise BOUNDARY.",
        },
    }
    text = json.dumps(payload, indent=1) + "\n"
    OUT.write_text(text, encoding="utf-8")
    loaded = json.loads(OUT.read_text(encoding="utf-8"))
    if loaded["replay_map"] != json_ready(REPLAY_MAP):
        raise SystemExit("replay map did not round-trip")
    print(hashlib.sha256(OUT.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
