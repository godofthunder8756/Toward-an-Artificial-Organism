"""Addendum A3 Deviation D2. Verification block only.

Replay agreement uses the frozen replay-comparison keys. cfo_detail is reported
and does not gate. Does not edit a frozen module and does not call
evaluate_mb_family, blind_result, evaluate_conf, evaluate_cg, evaluate_mf, or
evaluate_pm. One invocation. No retry.
"""

from __future__ import annotations

import hashlib
import inspect
import json
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

import wrel.attainability_a3 as a3
from wrel.agents import cg_choose, mf_action_probs
from wrel.attainability_a3 import (
    BLOCK_LIMIT,
    CR,
    CS,
    RSS_LIMIT,
    SETTINGS,
    WALL_LIMIT,
    Cap,
    Clock,
    Stop,
    _action_agreement,
    _call,
    _content_mf,
    _cpu_allowed,
    _det,
    _diff_packed,
    _donor_covered,
    _primary_table,
    _shadow_ok,
    _table_sha,
    build_pm_horizon,
    clause_of,
    donor_beliefs,
    mf_finish_on_snaps,
    pm_statistics_on_block,
    replay_blind,
    replay_cg_occupancy,
    replay_conf,
    replay_mf_occupancy,
    replay_myopic,
    replay_reference,
    roster,
    state_table,
)
from wrel.controls import _mf_thaw, conf_theta0, index_pm
from wrel.sep import _snapshots, assemble_setting
from wrel.util import dump_json, pack, parse_R, read_hwm, read_rss, sha256_file
from wrel.verification_a1 import cg_case
from wrel.world import N_Y, read_class
from wrel.run_all import study_world

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PRIMARY = ROOT / "outputs" / "attainability_A3"
D1_SUMMARY = ROOT / "outputs" / "attainability_A3_D1" / "SUMMARY.json"
OUT = ROOT / "outputs" / "attainability_A3_D2"
MANIFEST_A3 = ROOT / "ADDENDUM_A3_MANIFEST.md"
MANIFEST_D1 = ROOT / "ADDENDUM_A3_D1_MANIFEST.md"
MANIFEST_D2 = ROOT / "ADDENDUM_A3_D2_MANIFEST.md"
PRIMARY_COMMIT = "7e153d1648dfa5babe080b028a0c1609682c5a69"
D1_COMMIT = "0c5b308d001ca55402b012cce6655ce9e2317288"
FROZEN_RUNNER_SHA = "12c719bebafcda83ffcaaf67cfc3ae33ea997603424fa547d255c3c6ef78ba8a"
APPROVAL_SHA = "1f7158133243a2a506076bedba3a1ee5147f0004a6b772e6c92f077e6f8b82df"
# Frozen _compare_cases (attainability_a3.py lines 505-521). Not A2_KEYS.
REPLAY_CASE_KEYS = (
    "flags",
    "pattern",
    "t2_note",
    "t2_improvement",
    "per_action_agent",
    "per_action_baseline",
    "cref_counts",
    "donor_S",
    "donor_E",
    "donor_contrast",
    "interventions",
)
# Frozen _mb_replay_failures additions (lines 1022-1042), plus the case keys.
REFERENCE_GATING_KEYS = REPLAY_CASE_KEYS + (
    "V",
    "n_policy_entries",
    "n_beliefs",
    "invariant_decisions",
)
PM_GATING_EXTRA = ("action_mismatches", "ill_defined_extractor", "decoder_entries")
PM_DIAGNOSTIC_EXTRA = ("reachable", "zero_support_rule", "ill_defined")
GATING_CITATION = {
    "replay_case_keys": list(REPLAY_CASE_KEYS),
    "reference_additions": ["V", "n_policy_entries", "n_beliefs", "invariant_decisions", "action_table", "repair_equals_shadow", "donor_in_action_table"],
    "not_gating": ["cfo_detail"],
    "sources": [
        "wrel/attainability_a3.py _compare_cases lines 505-521",
        "wrel/attainability_a3.py _mb_replay_failures lines 1022-1042",
        "wrel/attainability_a3.py _pm_public lines 1365-1382",
        "wrel/attainability_a3.py _verify_horizon deciding-diff tuples",
        "c4_reliability_exact_check_spec_ADDENDUM_A3.md section Independent replay",
        "c4_reliability_exact_check_spec_ADDENDUM_A3_D1.md section What this run does",
    ],
}
PRIMARY_FILES = (
    "RESULTS_A3.md",
    "outputs/attainability_A3/smoke.json",
    "outputs/attainability_A3/PM.json",
    "outputs/attainability_A3/TSEP-3.json",
    "outputs/attainability_A3/TSEP-4.json",
    "outputs/attainability_A3/SUMMARY.json",
    "outputs/attainability_A3/HASHES.txt",
    "outputs/attainability_A3/RESULTS_A3.sha256",
)
OUTPUT_NAMES = (
    "PM-reconstruction.json",
    "TSEP-3-replay.json",
    "TSEP-3-states.json",
    "TSEP-4-replay.json",
    "TSEP-4-states.json",
    "SUMMARY.json",
    "HASHES.txt",
    "RESULTS_A3_D2.sha256",
)
COLUMN_KEYS = (
    "flags",
    "pattern",
    "t2_note",
    "donor_S",
    "donor_E",
    "donor_contrast",
    "interventions",
)
_FRAC = re.compile(r"^-?\d+/\d+$")


class D2Clock(Clock):
    """Caps with the A3 and D1 wall time already charged to the verification block."""

    def __init__(self, prior_total: float, prior_verify: float) -> None:
        super().__init__()
        self.prior_total = prior_total
        self.prior_verify = prior_verify
        self.verify_t0 = self.t0
        self.stage = "independent verification"
        self.stage_kind = "block"
        self.stage_t0 = self.t0

    def check(self, where: str = "") -> None:
        rss = read_rss()
        if rss > self.peak:
            self.peak = rss
        if rss > self.stage_peak:
            self.stage_peak = rss
        if self.invoke_name is not None and rss > self.invoke_peak:
            self.invoke_peak = rss
        now = time.perf_counter()
        if self.prior_total + (now - self.t0) > WALL_LIMIT:
            raise Cap("wall", f"{self.stage}: {where}")
        if self.prior_verify + (now - self.verify_t0) > BLOCK_LIMIT:
            raise Cap("block-wall", f"{self.stage}: {where}")
        if rss > RSS_LIMIT:
            raise Cap("memory", f"{self.stage}: {where} rss={rss}")

    def snapshot(self) -> dict:
        d2_wall = time.perf_counter() - self.t0
        return {
            "d2_wall_seconds_float": d2_wall,
            "prior_wall_through_d1_seconds_float": self.prior_total,
            "prior_verification_through_d1_seconds_float": self.prior_verify,
            "cumulative_a3_wall_seconds_float": self.prior_total + d2_wall,
            "cumulative_verification_wall_seconds_float": self.prior_verify + d2_wall,
            "peak_rss_bytes_sampled": self.peak,
            "process_hwm_bytes": read_hwm(),
        }

    def stage_snapshot(self) -> dict:
        snap = self.snapshot()
        snap["stage"] = self.stage
        snap["invocations"] = list(self.invocations)
        return snap


def joint_both_regimes(snaps) -> list:
    """Per-regime joint for a stateless policy.

    ``snaps[z][t]`` is a list of ``(i, p)``. The frozen helper does that unpack
    for one regime and stores content ``None``. Calling it on the length-2 list
    of horizons is the ValueError at attainability_a3.py:2310. This walks each
    regime first. Content stays ``None``, which the blind action map ignores.
    """
    if len(snaps) != 2:
        raise Stop("integrity", "blind snapshots are not two regimes")
    out = []
    for horizon in snaps:
        layers = []
        for layer in horizon:
            layers.append([(None, i, p) for i, p in layer])
        out.append(layers)
    return out


def _assert_gating_source() -> None:
    """The gating tuple is the frozen _compare_cases tuple, which does not name cfo_detail."""
    src = inspect.getsource(a3._compare_cases)
    for key in REPLAY_CASE_KEYS:
        if f'"{key}"' not in src:
            raise Stop("integrity", f"frozen _compare_cases does not name {key}")
    if "cfo_detail" in src:
        raise Stop("integrity", "frozen _compare_cases names cfo_detail")
    mb = inspect.getsource(a3._mb_replay_failures)
    for key in ("V", "n_policy_entries", "n_beliefs", "invariant_decisions", "action_table", "repair_equals_shadow"):
        if key not in mb:
            raise Stop("integrity", f"frozen _mb_replay_failures does not name {key}")
    if "cfo_detail" in mb:
        raise Stop("integrity", "frozen _mb_replay_failures names cfo_detail")


def _assert_nesting_diagnosis() -> None:
    """Confirm the frozen helper still fails on two horizons and the fix does not."""
    one = [[(7, 1)]]
    both = [one, one]
    try:
        a3._mb_snaps_as_joint(both)
    except ValueError as exc:
        if "not enough values to unpack" not in str(exc):
            raise Stop("integrity", f"unexpected nesting error: {exc}") from exc
    else:
        raise Stop("integrity", "the two-regime call of _mb_snaps_as_joint did not raise")
    if a3._mb_snaps_as_joint(one) != [[(None, 7, 1)]]:
        raise Stop("integrity", "frozen one-regime helper changed")
    if joint_both_regimes(both) != [[[(None, 7, 1)]], [[(None, 7, 1)]]]:
        raise Stop("integrity", "regime walk did not reproduce the one-regime joint")


def _unpack(obj):
    if isinstance(obj, str) and _FRAC.fullmatch(obj):
        return parse_R(obj)
    if isinstance(obj, dict):
        return {key: _unpack(value) for key, value in obj.items()}
    if isinstance(obj, list):
        return [_unpack(value) for value in obj]
    return obj


def _write(name: str, obj: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dump_json(str(OUT / name), pack(obj))


def _git_bytes(commit: str, rel: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{rel}"], cwd=str(REPO))


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _check_manifest_file(path: Path, clock: D2Clock) -> None:
    if not path.exists():
        raise Stop("integrity", f"{path.name} is missing")
    rows = []
    declared = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("FILE_COUNT "):
            declared = int(line.split()[1])
        elif line.startswith("SHA256 "):
            _tag, rel, digest = line.split()
            rows.append((rel, digest))
        clock.check("manifest")
    if declared is None or declared != len(rows) or not rows:
        raise Stop("integrity", f"{path.name} file count does not match the hash lines")
    for rel, digest in rows:
        got = sha256_file(str(ROOT / rel))
        if got != digest:
            raise Stop("integrity", f"hash mismatch {rel}")
        clock.check(f"hash {rel}")


def _load_primary(clock: D2Clock) -> dict:
    if sha256_file(str(ROOT / "wrel" / "attainability_a3.py")) != FROZEN_RUNNER_SHA:
        raise Stop("integrity", "frozen A3 runner hash changed")
    mismatches = []
    for rel in PRIMARY_FILES:
        committed = _sha_bytes(_git_bytes(PRIMARY_COMMIT, f"c4_reliability_exact_check_v1/{rel}"))
        working = sha256_file(str(ROOT / rel))
        if committed != working:
            mismatches.append(rel)
        clock.check(f"primary {rel}")
    if mismatches:
        raise Stop("integrity", "primary files differ from 7e153d1: " + ", ".join(mismatches))
    d1_rel = "outputs/attainability_A3_D1/SUMMARY.json"
    d1_committed = _sha_bytes(_git_bytes(D1_COMMIT, f"c4_reliability_exact_check_v1/{d1_rel}"))
    if d1_committed != sha256_file(str(ROOT / d1_rel)):
        raise Stop("integrity", "D1 summary differs from 0c5b308")
    summary = json.loads((PRIMARY / "SUMMARY.json").read_text(encoding="utf-8"))
    d1 = json.loads(D1_SUMMARY.read_text(encoding="utf-8"))
    prior_total = d1["clock"]["cumulative_a3_wall_seconds_float"]
    prior_verify = d1["clock"]["cumulative_verification_wall_seconds_float"]
    if not (0 < prior_verify < BLOCK_LIMIT) or prior_total > WALL_LIMIT:
        raise Stop("integrity", "stored cumulative clock is outside the recorded caps")
    return {
        "summary": summary,
        "pm": json.loads((PRIMARY / "PM.json").read_text(encoding="utf-8")),
        "settings": {
            3: json.loads((PRIMARY / "TSEP-3.json").read_text(encoding="utf-8")),
            4: json.loads((PRIMARY / "TSEP-4.json").read_text(encoding="utf-8")),
        },
        "prior_total": prior_total,
        "prior_verify": prior_verify,
    }


def _diagnostic(replay_value, stored_value, field: str, note: str):
    diffs = []
    _diff_packed(replay_value, stored_value, field, diffs)
    if not diffs:
        return None
    return {
        "field": field,
        "gating": False,
        "paths": diffs[:20],
        "stored": pack(stored_value),
        "replay": pack(replay_value),
        "note": note,
    }


def _diff_keys(replay: dict, stored: dict, keys: tuple) -> list:
    diffs = []
    for key in keys:
        if key not in stored:
            continue
        if key not in replay:
            diffs.append(key)
            continue
        _diff_packed(replay[key], stored[key], key, diffs)
    return diffs


def _string_note_improvement(replay: dict, stored_column: dict, diffs: list) -> None:
    """A stored string T2 note is the frozen encoding of improvement None."""
    if isinstance(stored_column.get("t2_note"), str) and replay.get("t2_improvement") is not None:
        diffs.append("t2_improvement")


def _unstored(replay: dict, stored_column: dict) -> dict:
    out = {}
    if "t2_improvement" not in stored_column and not isinstance(stored_column.get("t2_note"), str):
        out["t2_improvement"] = replay.get("t2_improvement")
    if "per_action_agent" not in stored_column and "per_action_agent" in replay:
        out["per_action_agent"] = replay.get("per_action_agent")
        out["per_action_baseline"] = replay.get("per_action_baseline")
    return out


def _column(stored: dict, name: str) -> dict:
    matches = [col for col in stored["columns"] if col["name"] == name]
    if len(matches) != 1:
        raise Stop("integrity", f"stored column missing for {name}")
    return matches[0]


def _extra(stored: dict, name: str) -> dict:
    matches = [col for col in stored["controls_raw_flags"] if col["name"] == name]
    if len(matches) != 1:
        raise Stop("integrity", f"stored extra missing for {name}")
    return matches[0].get("extra") or {}


def _agree(name: str, diffs: list, replay: dict, stored_column: dict, extra: dict | None = None) -> dict:
    record = {
        "name": name,
        "agreed": not diffs,
        "failures": diffs,
        "unstored_replay_fields": _unstored(replay, stored_column),
    }
    if extra:
        record.update(extra)
    return record


def _decision_reproduces(stored: dict) -> None:
    ref = _unpack(stored["reference"])
    controls = []
    for col in stored["columns"]:
        controls.append(
            {
                "name": col["name"],
                "flags": col["flags"],
                "pattern": _unpack(col["pattern"]),
                "t2_note": col["t2_note"],
                "donor_contrast": col["donor_contrast"],
                "interventions": _unpack(col["interventions"]),
                "donor_S": col["donor_S"],
                "donor_E": col["donor_E"],
            }
        )
    issued = assemble_setting(ref, controls, incomplete=False, pm_undefined=bool(stored["pm_undefined"]))
    if issued["label"] != stored["label_before_replay"] or issued["note"] != stored["label_before_replay_note"]:
        raise Stop("integrity", f"T_SEP={stored['T_SEP']} stored columns do not reproduce label_before_replay")
    for got, col in zip(issued["controls"], stored["columns"]):
        if got["reproduction"] != col["reproduction"] or got["conjunction"] != col["conjunction"]:
            raise Stop("integrity", f"T_SEP={stored['T_SEP']} {col['name']} reproduction column moved")


def _reference_rows_match(solver, pol, stored: dict) -> None:
    snaps = [_snapshots(solver, pol, stored["T_SEP"], z) for z in (0, 1)]
    rows = _primary_table(
        solver,
        pol,
        {"snaps": snaps, "donor_S": stored["reference"]["donor_S"], "donor_E": stored["reference"]["donor_E"]},
        stored["T_SEP"],
    )
    if _table_sha(rows) != stored["reference_action_table_sha256"]:
        raise Stop("integrity", f"T_SEP={stored['T_SEP']} reconstructed reference action table sha differs")
    if _table_sha(stored["reference_action_table"]) != stored["reference_action_table_sha256"]:
        raise Stop("integrity", f"T_SEP={stored['T_SEP']} stored reference action table sha differs")


def _mb_joint(solver, pol, T: int) -> list:
    snaps = [_snapshots(solver, pol, T, z) for z in (0, 1)]
    joint = []
    for z in (0, 1):
        layers = []
        for t, layer in enumerate(snaps[z]):
            k = T - t
            layers.append([((i, k), i, p) for i, p in layer])
        joint.append(layers)
    return joint


def _add_table(states: dict, name: str, table: dict, clock=None) -> None:
    states[name] = {
        "n_rows": table["n_rows"],
        "n_action_equal": table["n_action_equal"],
        "n_action_unequal": table["n_action_unequal"],
        "n_transition_equal": table["n_transition_equal"],
        "n_transition_unequal": table["n_transition_unequal"],
        "rows": table["rows"],
        "unequal_transitions": table["unequal_transitions"],
    }
    if clock is not None:
        clock.check(f"table {name}")


def _summary_of(states: dict) -> dict:
    return {
        name: {
            "n_rows": states[name]["n_rows"],
            "n_action_equal": states[name]["n_action_equal"],
            "n_action_unequal": states[name]["n_action_unequal"],
            "n_transition_equal": states[name]["n_transition_equal"],
            "n_transition_unequal": states[name]["n_transition_unequal"],
        }
        for name in states
    }


def _stop_replay(record: dict, states: dict, T: int, where: str) -> None:
    record["gating_agreed"] = False
    record["formal_label"] = None
    record["state_summary"] = _summary_of(states)
    _write(f"TSEP-{T}-states.json", {"T_SEP": T, "partial": True, "controls": states})
    _write(f"TSEP-{T}-replay.json", record)
    raise Stop("integrity", where)


def verify_horizon(world, T: int, held: dict, stored: dict, theta0, clock: D2Clock, settings_out: list) -> dict:
    solver = held["solver"]
    ref_pol = held["study_pol"]
    names = [row[1] for row in roster(T)]
    record = {
        "T_SEP": T,
        "compared_to_commit": PRIMARY_COMMIT,
        "gating_key_set": GATING_CITATION,
        "configurations": [],
        "formal_label": None,
        "formal_note": None,
        "clause": None,
        "verified": False,
        "pm_undefined_stored": stored["pm_undefined"],
    }
    settings_out.append(record)
    if stored["roster"] != names:
        raise Stop("integrity", f"T_SEP={T} stored roster is not the frozen roster")
    _decision_reproduces(stored)
    _reference_rows_match(solver, ref_pol, stored)
    states = {}
    held_replay = {
        "solver": solver,
        "study_pol": ref_pol,
        "primary_result": {
            "donor_S": stored["reference"]["donor_S"],
            "donor_E": stored["reference"]["donor_E"],
        },
    }
    ref = _call(clock, f"replay reference T={T}", lambda: replay_reference(world, held_replay, T, clock))
    diffs = _diff_keys(ref["public"], stored["reference"], REFERENCE_GATING_KEYS)
    nongating = []
    detail = _diagnostic(
        ref["public"].get("cfo_detail"),
        stored["reference"].get("cfo_detail"),
        "cfo_detail",
        "Not in frozen _compare_cases or _mb_replay_failures. The stored primary is null because evaluate_mb_family does not emit cfo_detail.",
    )
    if detail is not None:
        nongating.append(detail)
    actions = _action_agreement(stored["reference_action_table"], ref["rows"])
    if actions["n_disagree"] or actions["n_missing_in_replay"] or actions["n_missing_in_primary"]:
        diffs.append("action_table")
    if not _shadow_ok(ref["case"]["interventions"]):
        diffs.append("repair_equals_shadow")
    for donor_name in ("donor_S", "donor_E"):
        if not _donor_covered(stored["reference_action_table"], stored["reference"][donor_name]):
            diffs.append(f"stored_{donor_name}_in_action_table")
        if not _donor_covered(ref["rows"], ref["public"][donor_name]):
            diffs.append(f"replay_{donor_name}_in_action_table")
    record["configurations"].append(
        {
            "name": "R-HAC-MB",
            "agreed": not diffs,
            "failures": diffs,
            "nongating_differences": nongating,
            "action_agreement": {
                "n_agree": actions["n_agree"],
                "n_disagree": actions["n_disagree"],
                "n_missing_in_replay": actions["n_missing_in_replay"],
                "n_missing_in_primary": actions["n_missing_in_primary"],
                "replay_sha256": actions["replay_sha256"],
                "primary_sha256": actions["primary_sha256"],
            },
        }
    )
    if diffs:
        _stop_replay(record, states, T, f"T_SEP={T} reference replay disagrees")
    mb_joint = _mb_joint(solver, ref_pol, T)

    def mb_dist(content, y, pol=ref_pol):
        i, k = content
        return _det(int(pol[k][i * N_Y + y]))

    _add_table(
        states,
        "R-HAC-MB",
        state_table(solver, ref_pol, T, mb_joint, lambda content: list(solver.idx.counts[content[0]]), mb_dist),
        clock,
    )

    solved = _call(
        clock,
        f"myopic policy reconstruct T={T}",
        lambda: solver.solve_cost(CR, CS, budget=clock, myopic=True),
    )
    gate = []
    _diff_packed(solved["values"][T - 1], stored["myopic_pol_values_tail"], "myopic_pol_values_tail", gate)
    if solved["invariant"] != stored["myopic_invariant"]:
        gate.append("myopic_invariant")
    if gate:
        record["configurations"].append(_agree("R-HAC-MB-myopic", gate, {}, _column(stored, "R-HAC-MB-myopic")))
        _stop_replay(record, states, T, f"T_SEP={T} myopic policy reconstruction disagrees with the stored value")
    held_my = {
        "solver": solver,
        "myopic_pol": solved["pol"],
        "myopic_values": solved["values"],
        "myopic_invariant": solved["invariant"],
        "controls": [
            {
                "name": "R-HAC-MB-myopic",
                "donor_S": _column(stored, "R-HAC-MB-myopic")["donor_S"],
                "donor_E": _column(stored, "R-HAC-MB-myopic")["donor_E"],
            }
        ],
    }
    my = _call(clock, f"replay myopic T={T}", lambda: replay_myopic(world, held_my, T, clock))
    my_col = _column(stored, "R-HAC-MB-myopic")
    my_diffs = _diff_keys(my["public"], my_col, COLUMN_KEYS)
    _string_note_improvement(my["public"], my_col, my_diffs)
    _diff_packed(my["public"]["V"], stored["myopic_pol_values_tail"], "V", my_diffs)
    if my["public"]["invariant_decisions"] != stored["myopic_invariant"]:
        my_diffs.append("invariant_decisions")
    if my["public"]["n_beliefs"] != stored["reference"]["n_beliefs"]:
        my_diffs.append("n_beliefs")
    if my["public"]["n_policy_entries"] != stored["reference"]["n_policy_entries"]:
        my_diffs.append("n_policy_entries")
    my_actions = _action_agreement(my["primary_rows"], my["rows"])
    if my_actions["n_disagree"] or my_actions["n_missing_in_replay"] or my_actions["n_missing_in_primary"]:
        my_diffs.append("action_table")
    if not _shadow_ok(my["public"]["interventions"]):
        my_diffs.append("repair_equals_shadow")
    record["configurations"].append(
        _agree(
            "R-HAC-MB-myopic",
            my_diffs,
            my["public"],
            my_col,
            {
                "action_agreement": {
                    "n_agree": my_actions["n_agree"],
                    "n_disagree": my_actions["n_disagree"],
                    "n_missing_in_replay": my_actions["n_missing_in_replay"],
                    "n_missing_in_primary": my_actions["n_missing_in_primary"],
                }
            },
        )
    )
    if my_diffs:
        _stop_replay(record, states, T, f"T_SEP={T} myopic replay disagrees")
    my_joint = _mb_joint(solver, solved["pol"], T)

    def my_dist(content, y, pol=solved["pol"]):
        i, k = content
        return _det(int(pol[k][i * N_Y + y]))

    _add_table(
        states,
        "R-HAC-MB-myopic",
        state_table(solver, ref_pol, T, my_joint, lambda content: list(solver.idx.counts[content[0]]), my_dist),
        clock,
    )

    blind_col = _column(stored, "R-BLIND / R-CONF-S")
    blind = _call(clock, f"replay blind T={T}", lambda: replay_blind(world, solver, T, clock))
    act = blind["action_of_read"]
    blind_pol = [None]
    ba = bytearray(len(solver.idx.counts) * N_Y)
    for i in range(len(solver.idx.counts)):
        for y in range(N_Y):
            ba[i * N_Y + y] = act[read_class(y)]
    for _k in range(T):
        blind_pol.append(ba)
    bsnaps = [_snapshots(solver, blind_pol, T, z) for z in (0, 1)]
    bjoint = joint_both_regimes(bsnaps)

    def bdist(_content, y, act=act):
        return _det(act[read_class(y)])

    _add_table(
        states,
        "R-BLIND / R-CONF-S",
        state_table(solver, ref_pol, T, bjoint, lambda _content: None, bdist),
        clock,
    )
    bdiffs = _diff_keys(blind, blind_col, ("flags", "pattern", "t2_note", "donor_contrast", "interventions"))
    _string_note_improvement(blind, blind_col, bdiffs)
    record["configurations"].append(_agree("R-BLIND / R-CONF-S", bdiffs, blind, blind_col))
    if bdiffs:
        _stop_replay(record, states, T, f"T_SEP={T} blind replay disagrees")

    for kind, name, params in roster(T):
        if kind in ("myopic", "blind", "pm"):
            continue
        primary_col = _column(stored, name)
        if kind == "conf":
            eta, alpha = params["eta"], params["alpha"]
            got = _call(
                clock,
                f"replay {name}",
                lambda eta=eta, alpha=alpha, name=name: replay_conf(
                    solver, ref_pol, T, CR, CS, eta, alpha, theta0, name, clock
                ),
            )
            table = got.pop("state_table")
            _add_table(states, name, table, clock)
            diffs = _diff_keys(got, primary_col, COLUMN_KEYS)
            _string_note_improvement(got, primary_col, diffs)
            stored_extra = _extra(stored, name)
            if "V" in stored_extra:
                _diff_packed((got.get("extra") or {}).get("V"), stored_extra["V"], "extra.V", diffs)
        elif kind == "cg":
            a_s, a_f, beta = params["alpha_s"], params["alpha_f"], params["beta"]
            got = _call(
                clock,
                f"replay {name}",
                lambda a_s=a_s, a_f=a_f, beta=beta, name=name: cg_case(world, T, CR, CS, a_s, a_f, beta, clock, name),
            )
            snaps = _call(
                clock,
                f"occupancy {name}",
                lambda a_s=a_s, a_f=a_f, beta=beta, name=name: replay_cg_occupancy(
                    solver, T, CR, CS, a_s, a_f, beta, clock, name
                ),
            )

            def cdist(content, y, a_s=a_s, a_f=a_f, beta=beta):
                return _det(cg_choose(content, read_class(y), CR, CS, a_s, a_f, beta))

            _add_table(states, name, state_table(solver, ref_pol, T, snaps, lambda content: list(content), cdist), clock)
            diffs = _diff_keys(got, primary_col, ("flags", "pattern", "t2_note", "donor_S", "donor_E", "donor_contrast", "interventions"))
        elif kind == "mf":
            eps = params["eps"]
            snaps, value = _call(
                clock,
                f"replay {name}",
                lambda eps=eps, name=name: replay_mf_occupancy(solver, T, CR, CS, eps, clock, name),
            )
            got = _call(
                clock,
                f"finish {name}",
                lambda snaps=snaps, value=value, eps=eps, name=name: mf_finish_on_snaps(
                    solver, snaps, value, T, CR, CS, eps, name, clock
                ),
            )

            def mdist(content, y, eps=eps):
                sparse, g = _mf_thaw(content)
                probs, _phi = mf_action_probs(sparse, g, read_class(y), CR, CS, eps)
                return probs

            _add_table(states, name, state_table(solver, ref_pol, T, snaps, _content_mf, mdist), clock)
            diffs = _diff_keys(
                got,
                primary_col,
                ("flags", "pattern", "t2_note", "donor_S", "donor_E", "donor_contrast", "interventions"),
            )
        else:
            raise Stop("integrity", f"unknown roster kind {kind}")
        record["configurations"].append(_agree(name, diffs, got, primary_col))
        if diffs:
            _stop_replay(record, states, T, f"T_SEP={T} {name} replay disagrees")

    pm_col = _column(stored, "PM-ACT")
    pm_replay = _call(
        clock,
        f"replay PM-ACT T={T}",
        lambda: pm_statistics_on_block(
            solver, ref_pol, held["machine"], held["block_second"], T, CR, CS, 0, "PM-ACT", clock
        ),
    )
    info_p = index_pm(held["machine"], held["block"], T, 0)
    info_r = index_pm(held["machine"], held["block_second"], T, 0)
    sig_p = (
        donor_beliefs(solver, info_p, pm_col["donor_S"], T),
        donor_beliefs(solver, info_p, pm_col["donor_E"], T),
    )
    sig_r = (
        donor_beliefs(solver, info_r, pm_replay.get("donor_S"), T),
        donor_beliefs(solver, info_r, pm_replay.get("donor_E"), T),
    )
    pdiffs = _diff_keys(pm_replay, pm_col, ("flags", "pattern", "t2_note", "donor_contrast", "interventions"))
    if sig_p != sig_r:
        pdiffs.append("donor_belief_signature")
    stored_extra = stored.get("pm_extra") or {}
    replay_extra = pm_replay.get("extra") or {}
    for key in PM_GATING_EXTRA:
        if key in stored_extra:
            _diff_packed(replay_extra.get(key), stored_extra[key], f"extra.{key}", pdiffs)
    pm_nongating = []
    for key in PM_DIAGNOSTIC_EXTRA:
        if key in stored_extra:
            found = _diagnostic(
                replay_extra.get(key),
                stored_extra[key],
                f"extra.{key}",
                "Not in frozen _pm_public. Reported and not gating.",
            )
            if found is not None:
                pm_nongating.append(found)
    record["configurations"].append(
        _agree(
            "PM-ACT",
            pdiffs,
            pm_replay,
            pm_col,
            {
                "donor_signature_equal": sig_p == sig_r,
                "stored_donor_cells": {"S": pm_col["donor_S"], "E": pm_col["donor_E"]},
                "replay_donor_cells": {"S": pm_replay.get("donor_S"), "E": pm_replay.get("donor_E")},
                "ill_defined_extractor": replay_extra.get("ill_defined_extractor", False),
                "action_mismatches": replay_extra.get("action_mismatches"),
                "rescue": (pm_replay.get("flags") or {}).get("rescue"),
                "nongating_differences": pm_nongating,
            },
        )
    )
    pm_joint = []
    for z in (0, 1):
        snapz = _snapshots(solver, ref_pol, T, z)
        layers = []
        for t, layer in enumerate(snapz):
            rows = []
            for i, p in layer:
                cell = info_p["belief_cell"][t].get(i)
                rows.append(((t, cell), i, p))
            layers.append(rows)
        pm_joint.append(layers)

    def pdist(content, y, info=info_p):
        t, cell = content
        if cell is None:
            return _det(0)
        ay = info["action"].get((t, cell))
        if ay is None:
            return _det(0)
        return _det(int(ay[y]))

    _add_table(
        states,
        "PM-ACT",
        state_table(
            solver,
            ref_pol,
            T,
            pm_joint,
            lambda content: {"t": content[0], "cell": content[1]},
            pdist,
        ),
        clock,
    )
    if pdiffs:
        _stop_replay(record, states, T, f"T_SEP={T} PM-ACT replay disagrees")

    record["gating_agreed"] = all(item["agreed"] for item in record["configurations"])
    record["all_agreed"] = record["gating_agreed"]
    record["formal_label"] = None
    record["formal_note"] = None
    record["clause"] = None
    record["verified"] = False
    record["state_summary"] = _summary_of(states)
    _write(f"TSEP-{T}-states.json", {"T_SEP": T, "partial": False, "controls": states})
    _write(f"TSEP-{T}-replay.json", record)
    return record


def _issue_labels(state: dict, loaded: dict) -> None:
    """Issue both formal labels only after every configuration's gating keys agree."""
    if state.get("stop") or state.get("deviation"):
        return
    if len(state["settings"]) != 2 or not all(item.get("gating_agreed") for item in state["settings"]):
        return
    pending = []
    for item in state["settings"]:
        stored = loaded["settings"][item["T_SEP"]]
        ref = _unpack(stored["reference"])
        controls = []
        for col in stored["columns"]:
            controls.append(
                {
                    "name": col["name"],
                    "flags": col["flags"],
                    "pattern": _unpack(col["pattern"]),
                    "t2_note": col["t2_note"],
                    "donor_contrast": col["donor_contrast"],
                    "interventions": _unpack(col["interventions"]),
                    "donor_S": col["donor_S"],
                    "donor_E": col["donor_E"],
                }
            )
        issued = assemble_setting(ref, controls, incomplete=False, pm_undefined=bool(stored["pm_undefined"]))
        if issued["label"] != stored["label_before_replay"] or issued["note"] != stored["label_before_replay_note"]:
            raise Stop("integrity", f"T_SEP={item['T_SEP']} label issuance does not reproduce label_before_replay")
        pending.append((item, issued))
    for item, issued in pending:
        item["formal_label"] = issued["label"]
        item["formal_note"] = issued["note"]
        item["clause"] = clause_of(issued["note"])
        item["verified"] = True
        _write(f"TSEP-{item['T_SEP']}-replay.json", item)


def _results_text(state: dict) -> str:
    lines = [
        "# RESULTS A3 D2",
        "",
        "Additive verification record for Addendum A3 Deviation D2. Primary files at `7e153d1` and the D1 record are unchanged.",
        "",
        f"Binding approval: `c4_reliability_APPROVAL_ADDENDUM_A3_D2.md`, sha256 `{APPROVAL_SHA}`.",
        "",
        f"Code commit at process start: `{state['head']}`.",
        "",
        "Gating keys are the frozen `_compare_cases` tuple plus the `_mb_replay_failures` additions, restricted to fields the stored primary emits. `cfo_detail` is not in that tuple. It is reported and does not gate. The blind joint walks each regime and stores content `None`. That nesting is not a deciding statistic.",
        "",
        "No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. This file is not an all-controller certificate. A T_SEP = 4 result cannot claim to distinguish R-HAC-MF.",
        "",
        "## Replay agreement",
        "",
    ]
    for item in state["settings"]:
        lines.append(f"### T_SEP = {item['T_SEP']}")
        lines.append("")
        if item.get("formal_label") is None:
            lines.append("Formal label: not issued.")
        else:
            lines.append(f"Formal label: `{item['formal_label']}`.")
            lines.append(f"Note: {item.get('formal_note')}.")
            lines.append(f"Clause: `{item.get('clause')}`.")
        lines.append(f"Gating keys agreed: `{item.get('gating_agreed')}`.")
        lines.append("")
        lines.append("| Configuration | Agreed | Gating failures |")
        lines.append("| --- | --- | --- |")
        for cfg in item.get("configurations") or []:
            fails = cfg.get("failures") or []
            shown = ", ".join(fails[:12]) if fails else "—"
            if len(fails) > 12:
                shown += f" (+{len(fails) - 12} more)"
            lines.append(f"| {cfg['name']} | {cfg['agreed']} | {shown} |")
            for diff in cfg.get("nongating_differences") or []:
                lines.append(f"Non-gating difference `{diff['field']}`: {diff['note']}")
        lines.append("")
        pm = next((cfg for cfg in item.get("configurations") or [] if cfg["name"] == "PM-ACT"), None)
        if pm is not None:
            lines.append(
                f"PM-ACT donor signatures equal: `{pm.get('donor_signature_equal')}`. "
                f"Stored cells S `{pm.get('stored_donor_cells', {}).get('S')}`, "
                f"E `{pm.get('stored_donor_cells', {}).get('E')}`. "
                f"Replay cells S `{pm.get('replay_donor_cells', {}).get('S')}`, "
                f"E `{pm.get('replay_donor_cells', {}).get('E')}`. "
                f"`ill_defined_extractor`: `{pm.get('ill_defined_extractor')}`. "
                f"Action mismatches: `{pm.get('action_mismatches')}`. "
                f"Rescue: `{pm.get('rescue')}`."
            )
            lines.append("")
    if state.get("reconstructions"):
        lines.append("## PM reconstruction")
        lines.append("")
        for item in state["reconstructions"]:
            fails = ", ".join(item.get("failures") or []) or "—"
            lines.append(
                f"- T_SEP = {item['T_SEP']}: matches stored PM.json `{item['matches_stored_PM']}`. Failures: {fails}."
            )
        lines.append("")
    lines.extend(
        [
            "## Compute",
            "",
            "Command, from `c4_reliability_exact_check_v1`:",
            "",
            "```text",
            "taskset -c 0 python3 -u -m wrel.attainability_a3_d2",
            "```",
            "",
        ]
    )
    clock = state.get("clock") or {}
    for key in (
        "d2_wall_seconds_float",
        "prior_wall_through_d1_seconds_float",
        "prior_verification_through_d1_seconds_float",
        "cumulative_a3_wall_seconds_float",
        "cumulative_verification_wall_seconds_float",
        "peak_rss_bytes_sampled",
        "process_hwm_bytes",
    ):
        if key in clock:
            lines.append(f"- {key}: {clock[key]}")
    lines.append("- Limits: verification block 20 minutes cumulative, A3 total 60 minutes cumulative, one CPU, 8 GB, no GPU.")
    lines.append("")
    block = state.get("block") or {}
    invocations = block.get("invocations") or []
    if invocations:
        lines.append("| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |")
        lines.append("| --- | --- | --- | --- |")
        for inv in invocations:
            lines.append(
                f"| {inv['name']} | {inv['wall_seconds_float']} | {inv['peak_rss_bytes_sampled']} | {inv['process_hwm_bytes']} |"
            )
        lines.append("")
    lines.extend(["## Stop and deviation", ""])
    if state.get("stop"):
        lines.append(f"Stop: {state['stop']['kind']} at {state['stop']['where']}.")
    else:
        lines.append("No approved stop fired.")
    if state.get("deviation"):
        lines.append("")
        lines.append(f"Deviation: {state['deviation']}")
        lines.append("")
        lines.append("```text")
        lines.append(state.get("traceback") or "")
        lines.append("```")
    else:
        lines.append("")
        lines.append("No unexpected exception.")
    lines.extend(["", "## Output hashes", ""])
    for name, digest in (state.get("hashes") or {}).items():
        lines.append(f"- `{name}`: `{digest}`")
    lines.append("")
    lines.append("The sha256 of this file is `outputs/attainability_A3_D2/RESULTS_A3_D2.sha256`.")
    lines.append("")
    return "\n".join(lines)


def _hash_outputs() -> dict:
    hashes = {}
    for name in OUTPUT_NAMES:
        path = OUT / name
        if path.exists() and name not in ("HASHES.txt", "RESULTS_A3_D2.sha256"):
            hashes[name] = sha256_file(str(path))
    return hashes


def _finalize(state: dict, clock: D2Clock) -> None:
    state["clock"] = clock.snapshot()
    state["block"] = clock.stage_snapshot()
    summary = {
        "approval_sha256": APPROVAL_SHA,
        "primary_commit": PRIMARY_COMMIT,
        "head": state["head"],
        "cpu_allowed": state.get("cpu"),
        "settings": [
            {
                "T_SEP": item["T_SEP"],
                "gating_agreed": item.get("gating_agreed"),
                "verified": item.get("verified"),
                "formal_label": item.get("formal_label"),
                "formal_note": item.get("formal_note"),
                "clause": item.get("clause"),
                "agreed": [cfg["name"] for cfg in item.get("configurations") or [] if cfg.get("agreed")],
                "disagreed": [cfg["name"] for cfg in item.get("configurations") or [] if not cfg.get("agreed")],
            }
            for item in state["settings"]
        ],
        "stop": state.get("stop"),
        "deviation": state.get("deviation"),
        "clock": state["clock"],
        "gpu": "not used",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    _write("SUMMARY.json", summary)
    hashes = _hash_outputs()
    hash_lines = [f"SHA256 outputs/attainability_A3_D2/{name} {digest}" for name, digest in hashes.items()]
    (OUT / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")
    hashes["HASHES.txt"] = sha256_file(str(OUT / "HASHES.txt"))
    state["hashes"] = hashes
    results_path = ROOT / "RESULTS_A3_D2.md"
    results_path.write_text(_results_text(state), encoding="utf-8")
    digest = sha256_file(str(results_path))
    (OUT / "RESULTS_A3_D2.sha256").write_text(f"{digest}  RESULTS_A3_D2.md\n", encoding="utf-8")
    state["results_sha256"] = digest


def _head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO), text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        return f"unavailable ({exc.__class__.__name__})"


def run() -> dict:
    if len(sys.argv) != 1:
        raise SystemExit("this module takes no arguments")
    if (ROOT / "RESULTS_A3_D2.md").exists() or any((OUT / name).exists() for name in OUTPUT_NAMES):
        raise SystemExit("refusing a second invocation; an Addendum A3 D2 output already exists")
    state = {
        "head": _head(),
        "cpu": None,
        "settings": [],
        "reconstructions": [],
        "stop": None,
        "deviation": None,
        "hashes": {},
    }
    clock = None
    try:
        cpu = _cpu_allowed()
        state["cpu"] = cpu
        if cpu != "0":
            raise Stop("integrity", f"Cpus_allowed_list is {cpu!r}")
        pre_t0 = time.perf_counter()
        preload = D2Clock(0.0, 0.0)
        _check_manifest_file(MANIFEST_A3, preload)
        _check_manifest_file(MANIFEST_D1, preload)
        _check_manifest_file(MANIFEST_D2, preload)
        loaded = _load_primary(preload)
        pre_elapsed = time.perf_counter() - pre_t0
        clock = D2Clock(loaded["prior_total"], loaded["prior_verify"])
        clock.t0 -= pre_elapsed
        clock.verify_t0 -= pre_elapsed
        clock.stage_t0 -= pre_elapsed
        state["prior"] = {"total": loaded["prior_total"], "verification": loaded["prior_verify"]}
        clock.check("priors")
        _assert_gating_source()
        _assert_nesting_diagnosis()
        world = study_world()
        if world.eps[0].numerator != 23 or world.eps[0].denominator != 100:
            raise Stop("integrity", "frozen world identity failed")
        if world.eps[1] != world.eps[0] or not world.emissions_match:
            raise Stop("integrity", "frozen world identity failed")
        theta0 = conf_theta0()
        for horizon in SETTINGS:
            stored = loaded["settings"][horizon]
            rec, obj = build_pm_horizon(world, horizon, clock)
            stored_pm = next(item for item in loaded["pm"]["horizons"] if item["T_SEP"] == horizon)
            diffs = []
            _diff_packed(rec, stored_pm, f"PM.T{horizon}", diffs)
            state["reconstructions"].append({"T_SEP": horizon, "matches_stored_PM": not diffs, "failures": diffs})
            _write("PM-reconstruction.json", {"horizons": state["reconstructions"]})
            print(f"PM reconstruct T={horizon} match={not diffs} failures={len(diffs)}", flush=True)
            if diffs:
                raise Stop("integrity", f"PM reconstruction differs from stored PM.json at T_SEP={horizon}")
            if not rec["partition_equal"]:
                raise Stop("integrity", f"PM partitions differ at T_SEP={horizon}")
            setting = verify_horizon(world, horizon, obj, stored, theta0, clock, state["settings"])
            print(
                f"T_SEP={horizon} gating_agreed={setting.get('gating_agreed')} configs={len(setting.get('configurations') or [])}",
                flush=True,
            )
            del obj
        _issue_labels(state, loaded)
        for setting in state["settings"]:
            print(
                f"T_SEP={setting['T_SEP']} formal={setting.get('formal_label')} clause={setting.get('clause')}",
                flush=True,
            )
    except (Cap, Stop) as exc:
        state["stop"] = {"kind": exc.kind, "where": exc.where}
        print(f"stop {exc.kind}: {exc.where}", flush=True)
    except Exception as exc:
        state["deviation"] = f"{exc.__class__.__name__}: {exc}"
        state["traceback"] = traceback.format_exc()
        print(state["traceback"], flush=True)
    finally:
        if clock is None:
            clock = D2Clock(0.0, 0.0)
        try:
            _finalize(state, clock)
        except Exception as exc:
            print(f"finalize failed: {exc}", flush=True)
            traceback.print_exc()
    return state


if __name__ == "__main__":
    outcome = run()
    if outcome.get("deviation"):
        raise SystemExit(1)
