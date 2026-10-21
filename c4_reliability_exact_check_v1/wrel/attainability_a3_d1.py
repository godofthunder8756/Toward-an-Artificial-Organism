"""Addendum A3 Deviation D1. Verification block only.

Plumbing fix for the blind per-state joint. Does not edit a frozen module and
does not call evaluate_mb_family, blind_result, evaluate_conf, evaluate_cg,
evaluate_mf, or evaluate_pm. One invocation. No retry.
"""

from __future__ import annotations

import hashlib
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
    A2_KEYS,
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
OUT = ROOT / "outputs" / "attainability_A3_D1"
MANIFEST_A3 = ROOT / "ADDENDUM_A3_MANIFEST.md"
MANIFEST_D1 = ROOT / "ADDENDUM_A3_D1_MANIFEST.md"
PRIMARY_COMMIT = "7e153d1648dfa5babe080b028a0c1609682c5a69"
FROZEN_RUNNER_SHA = "12c719bebafcda83ffcaaf67cfc3ae33ea997603424fa547d255c3c6ef78ba8a"
APPROVAL_SHA = "47fd381e1fdf98b40914b117e5bf24412316a7aba56240fcce273b78e872bd62"
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
    "RESULTS_A3_D1.sha256",
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


class D1Clock(Clock):
    """A3 caps with the wall time the crashed verification block already used."""

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
        d1_wall = time.perf_counter() - self.t0
        return {
            "d1_wall_seconds_float": d1_wall,
            "prior_a3_wall_seconds_float": self.prior_total,
            "prior_verification_wall_seconds_float": self.prior_verify,
            "cumulative_a3_wall_seconds_float": self.prior_total + d1_wall,
            "cumulative_verification_wall_seconds_float": self.prior_verify + d1_wall,
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


def _check_manifest_file(path: Path, clock: D1Clock) -> None:
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


def _load_primary(clock: D1Clock) -> dict:
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
    summary = json.loads((PRIMARY / "SUMMARY.json").read_text(encoding="utf-8"))
    t4 = json.loads((PRIMARY / "TSEP-4.json").read_text(encoding="utf-8"))
    prior_total = summary["clock"]["cumulative_wall_seconds_float"]
    prior_t4 = t4["clock_evaluation"]["cumulative_wall_seconds_float"]
    prior_verify = prior_total - prior_t4
    if not (0 < prior_verify < BLOCK_LIMIT) or prior_total > WALL_LIMIT:
        raise Stop("integrity", "stored A3 clock is outside the recorded caps")
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


def _add_table(states: dict, name: str, table: dict) -> None:
    states[name] = {
        "n_rows": table["n_rows"],
        "n_action_equal": table["n_action_equal"],
        "n_action_unequal": table["n_action_unequal"],
        "n_transition_equal": table["n_transition_equal"],
        "n_transition_unequal": table["n_transition_unequal"],
        "rows": table["rows"],
        "unequal_transitions": table["unequal_transitions"],
    }


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
    record["state_summary"] = _summary_of(states)
    _write(f"TSEP-{T}-states.json", {"T_SEP": T, "partial": True, "controls": states})
    _write(f"TSEP-{T}-replay.json", record)
    raise Stop("integrity", where)


def verify_horizon(world, T: int, held: dict, stored: dict, theta0, clock: D1Clock, settings_out: list) -> dict:
    solver = held["solver"]
    ref_pol = held["study_pol"]
    names = [row[1] for row in roster(T)]
    record = {
        "T_SEP": T,
        "compared_to_commit": PRIMARY_COMMIT,
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
    diffs = _diff_keys(ref["public"], stored["reference"], A2_KEYS)
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
            _add_table(states, name, table)
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

            _add_table(states, name, state_table(solver, ref_pol, T, snaps, lambda content: list(content), cdist))
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

            _add_table(states, name, state_table(solver, ref_pol, T, snaps, _content_mf, mdist))
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
    for key, value in stored_extra.items():
        _diff_packed(replay_extra.get(key), value, f"extra.{key}", pdiffs)
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
    )
    if pdiffs:
        _stop_replay(record, states, T, f"T_SEP={T} PM-ACT replay disagrees")

    issued = assemble_setting(
        _unpack(stored["reference"]),
        [
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
            for col in stored["columns"]
        ],
        incomplete=False,
        pm_undefined=bool(stored["pm_undefined"]),
    )
    record["formal_label"] = issued["label"]
    record["formal_note"] = issued["note"]
    record["clause"] = clause_of(issued["note"])
    record["verified"] = True
    record["state_summary"] = _summary_of(states)
    record["all_agreed"] = all(item["agreed"] for item in record["configurations"])
    _write(f"TSEP-{T}-states.json", {"T_SEP": T, "partial": False, "controls": states})
    _write(f"TSEP-{T}-replay.json", record)
    return record


def _results_text(state: dict) -> str:
    lines = [
        "# RESULTS A3 D1",
        "",
        "Additive verification record for Addendum A3 Deviation D1. Primary files at `7e153d1` are unchanged.",
        "",
        f"Binding approval: `c4_reliability_APPROVAL_ADDENDUM_A3_D1.md`, sha256 `{APPROVAL_SHA}`.",
        "",
        f"Code commit at process start: `{state['head']}`.",
        "",
        "The blind joint walks each regime and stores content `None`. `replay_blind` returns the deciding statistics before that joint is built, and `decide_setting` does not read the joint. The nesting correction is not a criterion change.",
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
        lines.append("")
        lines.append("| Configuration | Agreed | Failures |")
        lines.append("| --- | --- | --- |")
        for cfg in item.get("configurations") or []:
            fails = cfg.get("failures") or []
            shown = ", ".join(fails[:12]) if fails else "—"
            if len(fails) > 12:
                shown += f" (+{len(fails) - 12} more)"
            lines.append(f"| {cfg['name']} | {cfg['agreed']} | {shown} |")
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
                f"Action mismatches: `{pm.get('action_mismatches')}`."
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
            "taskset -c 0 python3 -u -m wrel.attainability_a3_d1",
            "```",
            "",
        ]
    )
    clock = state.get("clock") or {}
    for key in (
        "d1_wall_seconds_float",
        "prior_a3_wall_seconds_float",
        "prior_verification_wall_seconds_float",
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
    lines.append("The sha256 of this file is `outputs/attainability_A3_D1/RESULTS_A3_D1.sha256`.")
    lines.append("")
    return "\n".join(lines)


def _hash_outputs() -> dict:
    hashes = {}
    for name in OUTPUT_NAMES:
        path = OUT / name
        if path.exists() and name not in ("HASHES.txt", "RESULTS_A3_D1.sha256"):
            hashes[name] = sha256_file(str(path))
    return hashes


def _finalize(state: dict, clock: D1Clock) -> None:
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
    hash_lines = [f"SHA256 outputs/attainability_A3_D1/{name} {digest}" for name, digest in hashes.items()]
    (OUT / "HASHES.txt").write_text("\n".join(hash_lines) + "\n", encoding="utf-8")
    hashes["HASHES.txt"] = sha256_file(str(OUT / "HASHES.txt"))
    state["hashes"] = hashes
    results_path = ROOT / "RESULTS_A3_D1.md"
    results_path.write_text(_results_text(state), encoding="utf-8")
    digest = sha256_file(str(results_path))
    (OUT / "RESULTS_A3_D1.sha256").write_text(f"{digest}  RESULTS_A3_D1.md\n", encoding="utf-8")
    state["results_sha256"] = digest


def _head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO), text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        return f"unavailable ({exc.__class__.__name__})"


def run() -> dict:
    if len(sys.argv) != 1:
        raise SystemExit("this module takes no arguments")
    if (ROOT / "RESULTS_A3_D1.md").exists() or any((OUT / name).exists() for name in OUTPUT_NAMES):
        raise SystemExit("refusing a second invocation; an Addendum A3 D1 output already exists")
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
        preload = D1Clock(0.0, 0.0)
        _check_manifest_file(MANIFEST_A3, preload)
        _check_manifest_file(MANIFEST_D1, preload)
        loaded = _load_primary(preload)
        pre_elapsed = time.perf_counter() - pre_t0
        clock = D1Clock(loaded["prior_total"], loaded["prior_verify"])
        clock.t0 -= pre_elapsed
        clock.verify_t0 -= pre_elapsed
        clock.stage_t0 -= pre_elapsed
        state["prior"] = {"total": loaded["prior_total"], "verification": loaded["prior_verify"]}
        clock.check("priors")
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
                f"T_SEP={horizon} verified={setting['verified']} formal={setting['formal_label']} clause={setting['clause']}",
                flush=True,
            )
            del obj
    except (Cap, Stop) as exc:
        state["stop"] = {"kind": exc.kind, "where": exc.where}
        print(f"stop {exc.kind}: {exc.where}", flush=True)
    except Exception as exc:
        state["deviation"] = f"{exc.__class__.__name__}: {exc}"
        state["traceback"] = traceback.format_exc()
        print(state["traceback"], flush=True)
    finally:
        if clock is None:
            clock = D1Clock(0.0, 0.0)
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
