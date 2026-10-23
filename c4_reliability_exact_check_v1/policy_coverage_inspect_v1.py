"""Read-only inspection of stored W-REL artifacts for policy action tables.

Does not import wrel. Does not solve, plan, or replay. Does not evaluate
the model. Reports whether already-stored JSON contains an action table
that could be compared at intervention or repair states.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"

FILES = [
    OUTPUTS / "ITEM-1.json",
    OUTPUTS / "ITEM-2.json",
    OUTPUTS / "ITEM-3.json",
    OUTPUTS / "ITEM-4.json",
    OUTPUTS / "ITEM-5.json",
    OUTPUTS / "ITEM-6.json",
    OUTPUTS / "ITEM-7.json",
    OUTPUTS / "ITEM-8.json",
    OUTPUTS / "ITEM-9.json",
    OUTPUTS / "SUMMARY.json",
    OUTPUTS / "deviation_1" / "ITEM-8.json",
    OUTPUTS / "deviation_1" / "ITEM-9.json",
    OUTPUTS / "verification_A1" / "RESULT.json",
    ROOT / "wrel" / "verification_a1.py",
]

NAME_HINTS = ("policy", "action", "pol")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def walk(obj, path, hits, longest):
    if isinstance(obj, dict):
        for k in sorted(obj):
            child = f"{path}.{k}" if path else str(k)
            low = str(k).lower()
            if any(h in low for h in NAME_HINTS):
                hits.append((child, type(obj[k]).__name__, _brief(obj[k])))
            walk(obj[k], child, hits, longest)
        return
    if isinstance(obj, list):
        if obj and all(isinstance(x, int) and not isinstance(x, bool) for x in obj):
            if longest[0] is None or len(obj) > longest[0][0]:
                longest[0] = (len(obj), path, obj[:8])
        # Donor vectors and small records are not descended into element-wise.
        if obj and isinstance(obj[0], (dict, list)):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]", hits, longest)


def _brief(obj) -> str:
    if isinstance(obj, dict):
        return "dict keys=" + ",".join(list(obj)[:12])
    if isinstance(obj, list):
        return f"list len={len(obj)}"
    if isinstance(obj, str):
        return "str " + obj[:80]
    return type(obj).__name__


def reference_shape(doc) -> list[str]:
    lines = []
    for s in doc.get("settings", []):
        if s.get("T_SEP") != 3:
            continue
        ref = s.get("reference", {})
        lines.append(
            f"T_SEP=3 cr={s.get('cr')} cs={s.get('cs')} reference_keys={sorted(ref)}"
        )
        interventions = ref.get("interventions")
        if not isinstance(interventions, dict):
            lines.append("  interventions: absent or not an object")
            continue
        for direction in ("S", "E"):
            block = interventions.get(direction)
            if not isinstance(block, dict):
                lines.append(f"  interventions.{direction}: {type(block).__name__}")
                continue
            lines.append(f"  interventions.{direction} modes={sorted(block)}")
            for mode, rec in block.items():
                if isinstance(rec, dict):
                    lines.append(f"    {mode} fields={sorted(rec)}")
    return lines


def main() -> None:
    print("policy_coverage_inspect_v1")
    print("scope: stored JSON and the locked verification source hash")
    print("computation: none over the model")
    print()
    for path in FILES:
        rel = path.relative_to(ROOT)
        if not path.is_file():
            print(f"MISSING {rel}")
            continue
        print(f"sha256 {rel} {sha256(path)} bytes {path.stat().st_size}")
    print()
    hits = []
    longest = [None]
    for path in FILES:
        if path.suffix != ".json" or not path.is_file():
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        walk(doc, path.relative_to(ROOT).as_posix(), hits, longest)
    print("name hits (key contains policy, action, or pol):")
    if not hits:
        print("  none")
    for child, typ, brief in hits:
        print(f"  {child} :: {typ} :: {brief}")
    print()
    if longest[0] is None:
        print("longest int list: none")
    else:
        n, path, head = longest[0]
        print(f"longest int list: len={n} path={path} head={head}")
    print()
    item8 = json.loads((OUTPUTS / "deviation_1" / "ITEM-8.json").read_text(encoding="utf-8"))
    print("deviation_1/ITEM-8.json reference shape at T_SEP=3:")
    for line in reference_shape(item8):
        print(line)
    print()
    result = json.loads((OUTPUTS / "verification_A1" / "RESULT.json").read_text(encoding="utf-8"))
    print("verification_A1/RESULT.json top keys:", sorted(result))
    print("policy_source:", result.get("policy_source"))
    print("mismatches_len:", len(result.get("mismatches", [])))
    print("invariant_decisions:", result.get("invariant_decisions"))
    for row in result.get("reference", []):
        print(
            "reference row keys:",
            sorted(row),
            "n_policy_entries:",
            row.get("n_policy_entries"),
            "n_mismatches:",
            row.get("n_mismatches"),
        )
    print()
    print("stored_action_table_covering_intervention_or_repair_states: no")


if __name__ == "__main__":
    main()
