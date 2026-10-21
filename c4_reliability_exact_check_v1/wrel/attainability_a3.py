"""Addendum A3 named-control comparison.

One process. H0 at (1/100, 3/50), T_SEP = 3 then 4, with the roster supplied
in the A3 spec. Reuses frozen modules. Does not modify an earlier file.
Takes no arguments and does not retry.

PM-ACT statistics on a caller-supplied block, and the MF finish on a
caller-supplied occupancy, are filled from the frozen arithmetic at freeze
time (pm_statistics_on_block, mf_finish_on_snaps). They are not calls to
evaluate_pm or evaluate_mf.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
import traceback
from collections import defaultdict
from pathlib import Path

from wrel.agents import _upd, mf_action_probs
from wrel.controls import SPLIT, _Tables, _cfo_mb, _contrast, _ct2, _finish_f0, _flags_from
from wrel.controls import _mf_freeze, _mf_mhat, _mf_thaw, _pack_result, _pattern, _select
from wrel.controls import conf_theta0, evaluate_cg, evaluate_conf, evaluate_mf, evaluate_pm, index_pm
from wrel.labels import CORE, conjunction_of
from wrel.mb import H0Solver
from wrel.pm import build_machine, partition_sets, reachable_beliefs, refine, refine_by_queue, well_defined
from wrel.run_all import CG_ALPHA, CG_BETA, COSTS, ETAS, MF_EPS, _donors_for, study_world
from wrel.sep import MU_REF, MU_RESL, MU_RESa, MU_RESc, MU_SELa, MU_SELc, MU_T2, RHO
from wrel.sep import _advance, _cref, _flag_ref, _flag_t2, _m_f0, _snapshots
from wrel.sep import assemble_setting, blind_result, ct2_from_mixture, evaluate_mb_family, reference_met
from wrel.util import dump_json, pack, parse_R, read_hwm, read_rss, sha256_file
from wrel.verification_a1 import Index, _choose, _mb_advance, cg_case, forward_mb, reference_case, solve_reference
from wrel.world import ACT_NAME, F, M_ACT, N_Y, P_ACT, R_ACT, read_class

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OUT = ROOT / "outputs" / "attainability_A3"
MANIFEST = ROOT / "ADDENDUM_A3_MANIFEST.md"
ITEM2 = ROOT / "outputs" / "ITEM-2.json"
A2 = ROOT / "outputs" / "attainability_A2"
CR = F(1, 100)
CS = F(3, 50)
SETTINGS = (3, 4)
SMOKE_LIMIT = 60.0
BLOCK_LIMIT = 20 * 60
WALL_LIMIT = 60 * 60
RSS_LIMIT = 8 * 1024**3
APPROVAL_SHA = "6efeef0d2ae0123e95939f63d06a803d9cde642997ce735a6b0eb28aa2ea9a2c"
OUTPUT_NAMES = (
    "smoke.json",
    "PM.json",
    "TSEP-3.json",
    "TSEP-3-states.json",
    "TSEP-4.json",
    "TSEP-4-states.json",
    "SUMMARY.json",
    "HASHES.txt",
    "RESULTS_A3.sha256",
)
A2_KEYS = (
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
    "V",
    "n_policy_entries",
    "invariant_decisions",
    "n_beliefs",
    "cfo_detail",
)


class Cap(Exception):
    def __init__(self, kind: str, where: str):
        super().__init__(f"{kind}: {where}")
        self.kind = kind
        self.where = where


class Stop(Exception):
    def __init__(self, kind: str, where: str):
        super().__init__(f"{kind}: {where}")
        self.kind = kind
        self.where = where


class Clock:
    def __init__(self) -> None:
        self.t0 = time.perf_counter()
        self.peak = read_rss()
        self.stage = "start"
        self.stage_t0 = self.t0
        self.stage_limit = None
        self.stage_kind = "none"
        self.stage_peak = self.peak
        self.invocations = []
        self.block_invoke_start = 0
        self.invoke_name = None
        self.invoke_t0 = self.t0
        self.invoke_peak = self.peak

    def begin(self, name: str, limit, kind: str) -> None:
        self.stage = name
        self.stage_t0 = time.perf_counter()
        self.stage_limit = limit
        self.stage_kind = kind
        self.stage_peak = read_rss()
        self.block_invoke_start = len(self.invocations)
        self.check("begin")

    def begin_invoke(self, name: str) -> None:
        self.invoke_name = name
        self.invoke_t0 = time.perf_counter()
        self.invoke_peak = read_rss()
        self.check(name)

    def end_invoke(self) -> dict:
        rss = read_rss()
        if rss > self.invoke_peak:
            self.invoke_peak = rss
        rec = {
            "name": self.invoke_name,
            "stage": self.stage,
            "wall_seconds_float": time.perf_counter() - self.invoke_t0,
            "peak_rss_bytes_sampled": self.invoke_peak,
            "rss_end_bytes": rss,
            "process_hwm_bytes": read_hwm(),
        }
        self.invocations.append(rec)
        self.invoke_name = None
        self.check("end-invoke")
        return rec

    def check(self, where: str = "") -> None:
        rss = read_rss()
        if rss > self.peak:
            self.peak = rss
        if rss > self.stage_peak:
            self.stage_peak = rss
        if self.invoke_name is not None and rss > self.invoke_peak:
            self.invoke_peak = rss
        if time.perf_counter() - self.t0 > WALL_LIMIT:
            raise Cap("wall", f"{self.stage}: {where}")
        if self.stage_limit is not None and time.perf_counter() - self.stage_t0 > self.stage_limit:
            kind = "smoke-wall" if self.stage_kind == "smoke" else "block-wall"
            raise Cap(kind, f"{self.stage}: {where}")
        if rss > RSS_LIMIT:
            raise Cap("memory", f"{self.stage}: {where} rss={rss}")

    def stage_snapshot(self) -> dict:
        return {
            "stage": self.stage,
            "stage_wall_seconds_float": time.perf_counter() - self.stage_t0,
            "cumulative_wall_seconds_float": time.perf_counter() - self.t0,
            "stage_peak_rss_bytes_sampled": self.stage_peak,
            "process_hwm_bytes": read_hwm(),
            "invocations": list(self.invocations[self.block_invoke_start :]),
        }

    def snapshot(self) -> dict:
        return {
            "cumulative_wall_seconds_float": time.perf_counter() - self.t0,
            "peak_rss_bytes_sampled": self.peak,
            "process_hwm_bytes": read_hwm(),
        }


def _cpu_allowed() -> str:
    with open("/proc/self/status", "r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("Cpus_allowed_list:"):
                return line.split(":", 1)[1].strip()
    return ""


def _head() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO), text=True).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        return f"unavailable ({exc.__class__.__name__})"


def _check_manifest(clock: Clock) -> None:
    if not MANIFEST.exists():
        raise Stop("integrity", "ADDENDUM_A3_MANIFEST.md is missing")
    rows = []
    declared = None
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if line.startswith("FILE_COUNT "):
            declared = int(line.split()[1])
        elif line.startswith("SHA256 "):
            _tag, rel, digest = line.split()
            rows.append((rel, digest))
        clock.check("manifest")
    if declared is None or declared != len(rows) or not rows:
        raise Stop("integrity", "manifest file count does not match the hash lines")
    for rel, digest in rows:
        got = sha256_file(str(ROOT / rel))
        if got != digest:
            raise Stop("integrity", f"hash mismatch {rel}")
        clock.check(f"hash {rel}")


def _write(name: str, obj: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dump_json(str(OUT / name), pack(obj))


def _call(clock: Clock, name: str, fn):
    clock.begin_invoke(name)
    try:
        return fn()
    finally:
        clock.end_invoke()


def roster(T: int) -> list:
    """item8 append order at this cost. MF only at T_SEP = 3."""
    rows = [("myopic", "R-HAC-MB-myopic", {})]
    rows.append(("blind", "R-BLIND / R-CONF-S", {}))
    for eta in ETAS:
        for alpha in ETAS:
            rows.append(("conf", f"R-CONF-A eta={eta} alpha={alpha}", {"eta": eta, "alpha": alpha}))
    for a_s, a_f in CG_ALPHA:
        for beta in CG_BETA:
            rows.append(
                (
                    "cg",
                    f"R-CG alpha=({a_s},{a_f}) beta={beta}",
                    {"alpha_s": a_s, "alpha_f": a_f, "beta": beta},
                )
            )
    if T == 3:
        for eps in MF_EPS:
            rows.append(("mf", f"R-HAC-MF eps={eps}", {"eps": eps}))
    rows.append(("pm", "PM-ACT", {}))
    return rows


def clause_of(note: str) -> str:
    """Reading of the frozen decide_setting note. Not a second decision rule."""
    if note == "a required item is incomplete or NOT-RUN":
        return "1"
    if note == "PM-ACT quotient is not well-defined":
        return "2"
    if note.startswith("reference criterion undefined:"):
        return "3"
    if note == "the reference does not meet the required conjunction":
        return "4"
    if note.startswith("reproducing:"):
        return "5"
    if note.startswith("shared conjunction:"):
        return "6"
    if note.startswith("eligible control fails no evaluable core criterion"):
        return "7"
    if note.startswith("no reproduction is YES and some reproduction is UNRESOLVED"):
        return "7"
    if note == "every eligible control fails at least one core criterion":
        return "8"
    if note == "no decision-order clause applied":
        return "9"
    return "unrecognized"


def _deep_diff(got, exp, path: str, out: list) -> None:
    if isinstance(got, F) or isinstance(exp, F):
        if got != exp:
            out.append(path)
        return
    if isinstance(got, dict) and isinstance(exp, dict):
        keys = set(got) | set(exp)
        for key in sorted(keys, key=str):
            nxt = f"{path}.{key}"
            if key not in got or key not in exp:
                out.append(nxt)
            else:
                _deep_diff(got[key], exp[key], nxt, out)
        return
    if isinstance(got, (list, tuple)) and isinstance(exp, (list, tuple)):
        if len(got) != len(exp):
            out.append(path)
            return
        for i, (left, right) in enumerate(zip(got, exp)):
            _deep_diff(left, right, f"{path}[{i}]", out)
        return
    if got != exp:
        out.append(path)


def _diff_packed(got, exp, path: str, out: list) -> None:
    """Compare an in-memory value with an already packed JSON value."""
    packed = pack(got)
    if isinstance(packed, dict) and isinstance(exp, dict):
        keys = set(packed) | set(exp)
        for key in sorted(keys, key=str):
            nxt = f"{path}.{key}"
            if key not in packed or key not in exp:
                out.append(nxt)
            else:
                _diff_packed_ready(packed[key], exp[key], nxt, out)
        return
    _diff_packed_ready(packed, exp, path, out)


def _diff_packed_ready(packed, exp, path: str, out: list) -> None:
    if isinstance(packed, dict) and isinstance(exp, dict):
        keys = set(packed) | set(exp)
        for key in sorted(keys, key=str):
            nxt = f"{path}.{key}"
            if key not in packed or key not in exp:
                out.append(nxt)
            else:
                _diff_packed_ready(packed[key], exp[key], nxt, out)
        return
    if isinstance(packed, list) and isinstance(exp, list):
        if len(packed) != len(exp):
            out.append(path)
            return
        for i, (left, right) in enumerate(zip(packed, exp)):
            _diff_packed_ready(left, right, f"{path}[{i}]", out)
        return
    if packed != exp:
        out.append(path)


def _rows_from_policy(counts_of, action_at, states: set, k: int, horizon_limit: int) -> list:
    rows = []
    for i in states:
        counts = list(counts_of(i))
        if sum(counts) > horizon_limit:
            raise Stop("integrity", f"action state at k={k} is outside the solved horizon")
        for y in range(N_Y):
            action = int(action_at(i, y))
            rows.append(
                {
                    "k": k,
                    "counts": counts,
                    "y": y,
                    "action": action,
                    "action_name": ACT_NAME[action],
                }
            )
    rows.sort(key=lambda row: (row["k"], row["counts"], row["y"]))
    return rows


def _primary_table(solver, pol, result, T: int) -> list:
    snaps = result["snaps"]
    t_star = T - 2
    pert = set()
    for z in (0, 1):
        for i, p in snaps[z][t_star]:
            if p != 0:
                pert.add(i)

    def locate(counts):
        if counts is None:
            return None
        return solver.idx.index[tuple(counts)]

    donors = (locate(result["donor_S"]), locate(result["donor_E"]))
    for donor in donors:
        if donor is not None:
            pert.add(donor)
    repair = set()
    for z, donor in ((1, donors[0]), (0, donors[1])):
        if donor is None:
            continue
        rec = [(i, p) for i, p in snaps[z][t_star] if p != 0]
        for don, clamp in ((donor, False), (donor, True), (None, True)):
            mass_a, mass_b = _advance(rec, don, clamp, z, 2, pol, solver)
            for mass in (mass_a, mass_b):
                for i, p in mass.items():
                    if p != 0:
                        repair.add(i)

    def at(table, i, y):
        return table[i * N_Y + y]

    rows = _rows_from_policy(lambda i: solver.idx.counts[i], lambda i, y: at(pol[2], i, y), pert, 2, T - 2)
    rows.extend(_rows_from_policy(lambda i: solver.idx.counts[i], lambda i, y: at(pol[1], i, y), repair, 1, T - 1))
    return rows


def _replay_table(world, idx, pol, case, T: int) -> list:
    snaps = [forward_mb(world, idx, pol, T, z) for z in (0, 1)]
    t_star = T - 2
    pert = set()
    for z in (0, 1):
        for i, p in snaps[z][t_star]:
            if p != 0:
                pert.add(i)

    def locate(counts):
        if counts is None:
            return None
        return idx.index[tuple(counts)]

    donors = (locate(case["donor_S"]), locate(case["donor_E"]))
    for donor in donors:
        if donor is not None:
            pert.add(donor)
    repair = set()
    for z, donor in ((1, donors[0]), (0, donors[1])):
        if donor is None:
            continue
        rec = [(i, p) for i, p in snaps[z][t_star] if p != 0]
        for don, clamp in ((donor, False), (donor, True), (None, True)):
            mass_a, mass_b = _mb_advance(rec, don, clamp, z, 2, pol, world, idx)
            for mass in (mass_a, mass_b):
                for i, p in mass.items():
                    if p != 0:
                        repair.add(i)

    def at(k, i, y):
        try:
            return pol[k][(i, y)]
        except KeyError as exc:
            raise Stop("integrity", f"replay policy missing k={k} index={i} y={y}") from exc

    rows = _rows_from_policy(lambda i: idx.counts[i], lambda i, y: at(2, i, y), pert, 2, T - 2)
    rows.extend(_rows_from_policy(lambda i: idx.counts[i], lambda i, y: at(1, i, y), repair, 1, T - 1))
    return rows


def _index_table(rows: list) -> dict:
    indexed = {}
    for row in rows:
        key = (row["k"], tuple(row["counts"]), row["y"])
        if key in indexed:
            raise Stop("integrity", "duplicate action-table key")
        indexed[key] = row["action"]
    return indexed


def _table_sha(rows: list) -> str:
    blob = json.dumps(rows, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _shadow_ok(interventions) -> bool:
    if not isinstance(interventions, dict):
        return False
    for direction in ("S", "E"):
        modes = interventions.get(direction)
        if modes is None:
            continue
        if not isinstance(modes, dict):
            return False
        for mode in ("SWAP", "CORRUPT", "SUSPEND"):
            block = modes.get(mode)
            if not isinstance(block, dict) or block.get("repair_equals_shadow") is not True:
                return False
    return True


def _donor_covered(rows: list, donor) -> bool:
    if donor is None:
        return True
    key = tuple(donor)
    return any(row["k"] == 2 and tuple(row["counts"]) == key for row in rows)


def _entry_count(index_sum, pol, T: int, replay: bool) -> int:
    if replay:
        return sum(len(pol[k]) for k in range(1, T + 1))
    total = 0
    for k in range(1, T + 1):
        total += sum(1 for count in index_sum if count <= T - k) * N_Y
    return total


def _public_case(case: dict, value, n_entries: int, invariant: bool, n_beliefs: int) -> dict:
    return {
        "flags": case["flags"],
        "pattern": case["pattern"],
        "t2_note": case["t2_note"],
        "t2_improvement": case["t2_improvement"],
        "per_action_agent": case["per_action_agent"],
        "per_action_baseline": case["per_action_baseline"],
        "cref_counts": case["cref_counts"],
        "donor_S": case["donor_S"],
        "donor_E": case["donor_E"],
        "donor_contrast": case["donor_contrast"],
        "interventions": case["interventions"],
        "V": value,
        "n_policy_entries": n_entries,
        "invariant_decisions": invariant,
        "n_beliefs": n_beliefs,
        "cfo_detail": case.get("cfo_detail"),
    }


def _compare_cases(primary: dict, replay: dict) -> list:
    diffs = []
    for key in (
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
    ):
        _deep_diff(replay[key], primary[key], key, diffs)
    return diffs


def _action_agreement(primary_rows: list, replay_rows: list) -> dict:
    left = _index_table(primary_rows)
    right = _index_table(replay_rows)
    missing_in_replay = []
    missing_in_primary = []
    disagreements = []
    for key in sorted(set(left) | set(right)):
        record = {"k": key[0], "counts": list(key[1]), "y": key[2]}
        if key not in right:
            missing_in_replay.append(record)
        elif key not in left:
            missing_in_primary.append(record)
        elif left[key] != right[key]:
            record["primary"] = left[key]
            record["replay"] = right[key]
            disagreements.append(record)
    n_agree = len(set(left) & set(right)) - len(disagreements)
    return {
        "n_primary_rows": len(primary_rows),
        "n_replay_rows": len(replay_rows),
        "n_agree": n_agree,
        "n_disagree": len(disagreements),
        "n_missing_in_replay": len(missing_in_replay),
        "n_missing_in_primary": len(missing_in_primary),
        "missing_in_replay": missing_in_replay,
        "missing_in_primary": missing_in_primary,
        "disagreements": disagreements,
        "primary_sha256": _table_sha(primary_rows),
        "replay_sha256": _table_sha(replay_rows),
    }


def _smoke_mismatches(backward, forwards, row: dict) -> list:
    mixture = (forwards[0]["value"] + forwards[1]["value"]) / 2
    mismatches = []
    if mixture != backward:
        mismatches.append("forward_mixture_vs_backward")
    if mixture != parse_R(row["V_star"]) or backward != parse_R(row["V_star"]):
        mismatches.append("V_star")
    pairs = (
        ("n_R", "n_R"),
        ("n_R_unanimous", "n_R_unanimous"),
        ("n_M", "n_M"),
        ("exploration_cost", "exploration_cost"),
        ("never_R", "never_R"),
    )
    for z, name in ((0, "S"), (1, "E")):
        for got_key, row_key in pairs:
            if forwards[z][got_key] != parse_R(row[row_key][name]):
                mismatches.append(f"{row_key}.{name}")
        stored_first = [parse_R(item) for item in row["first_R"][name]]
        if list(forwards[z]["first_R"]) != stored_first:
            mismatches.append(f"first_R.{name}")
    return mismatches


def run_smoke(world, clock: Clock) -> dict:
    solver = H0Solver(world, 1)
    clock.check("smoke solver built")
    solved = solver.solve_cost(CR, CS, budget=clock, myopic=False)
    forwards = [solver.forward(solved["pol"], 1, CR, CS, z, clock) for z in (0, 1)]
    clock.check("smoke forward")
    document = json.loads(ITEM2.read_text(encoding="utf-8"))
    row = next(
        item
        for item in document["rows"]
        if item["law"] == "H0" and item["T"] == 1 and item["cr"] == "1/100" and item["cs"] == "3/50"
    )
    backward = solved["values"][0]
    mismatches = _smoke_mismatches(backward, forwards, row)
    return {
        "case": "T=1",
        "law": "H0",
        "agent": "R-HAC-MB",
        "cr": CR,
        "cs": CS,
        "myopic": False,
        "V_backward": backward,
        "V_forward_S": forwards[0]["value"],
        "V_forward_E": forwards[1]["value"],
        "V_forward_mixture": (forwards[0]["value"] + forwards[1]["value"]) / 2,
        "stored_V_star": parse_R(row["V_star"]),
        "n_R": {"S": forwards[0]["n_R"], "E": forwards[1]["n_R"]},
        "n_M": {"S": forwards[0]["n_M"], "E": forwards[1]["n_M"]},
        "mismatches": mismatches,
        "ok": not mismatches,
        "invariant_decisions": solved["invariant"],
    }


def _cost_record(cr, cs) -> dict:
    return {"cr": cr, "cs": cs, "a_sep_setting": (cr, cs) == (CR, CS)}


def build_pm_horizon(world, T: int, clock: Clock) -> tuple:
    """Frozen PM-ACT closure at one horizon. Other COSTS pairs are the input alphabet."""
    solver = H0Solver(world, T)
    clock.check(f"PM index T={T}")
    policies = []
    solved_study = None
    for cr, cs in COSTS:
        solved = _call(
            clock,
            f"PM solve T={T} cr={cr.numerator}/{cr.denominator} cs={cs.numerator}/{cs.denominator}",
            lambda cr=cr, cs=cs: solver.solve_cost(cr, cs, budget=clock, myopic=False),
        )
        policies.append(solved["pol"])
        if (cr, cs) == (CR, CS):
            solved_study = solved
    if solved_study is None:
        raise Stop("integrity", "study cost missing from the PM input alphabet")
    donors = _call(
        clock,
        f"PM donors T={T}",
        lambda: _donors_for(solver, solved_study["pol"], T),
    )
    s_i, e_i, _snaps = donors

    def _close():
        machine = build_machine(solver, policies, T, s_i, e_i, n_costs=6)
        block = refine(machine.trans)
        second = refine_by_queue(machine.trans)
        return machine, block, second

    machine, block, second = _call(clock, f"PM machine T={T}", _close)
    same = partition_sets(block) == partition_sets(second)
    wd = well_defined(machine, block)
    record = {
        "T_SEP": T,
        "cr": CR,
        "cs": CS,
        "n_costs": 6,
        "cost_index": COSTS.index((CR, CS)),
        "input_domain": [_cost_record(cr, cs) for cr, cs in COSTS],
        "input_domain_note": (
            "The five costs other than (1/100, 3/50) are the frozen phase alphabet of PM-ACT. "
            "No A-SEP criterion is evaluated at those costs."
        ),
        "donor_S_index": s_i,
        "donor_E_index": e_i,
        "donor_S_counts": list(solver.idx.counts[s_i]),
        "donor_E_counts": list(solver.idx.counts[e_i]),
        "counts": machine.counts(),
        "n_blocks_primary": len(set(block)),
        "n_blocks_queue": len(set(second)),
        "partition_equal": same,
        "well_defined": wd,
        "reachable_beliefs_phase1": reachable_beliefs(machine, T),
        "pm_k_built": False,
    }
    held = {
        "solver": solver,
        "study_pol": solved_study["pol"],
        "study_values": solved_study["values"],
        "study_invariant": solved_study["invariant"],
        "machine": machine,
        "block": block,
        "block_second": second,
        "donor_S": s_i,
        "donor_E": e_i,
        "well_defined": wd,
    }
    return record, held


def _belief_transition(idx, i: int, y: int, z: int, dist: dict) -> dict:
    out = {}
    counts = idx.counts
    for action, prob in dist.items():
        if prob == 0:
            continue
        if action != R_ACT:
            key = tuple(counts[i])
            out[key] = out.get(key, F(0)) + prob
            continue
        for c in range(10):
            pc = idx.pc[z][y][c]
            if pc == 0:
                continue
            j = idx.trans[i][c]
            if j < 0:
                raise Stop("integrity", "belief transition left the closed count set")
            key = tuple(counts[j])
            out[key] = out.get(key, F(0)) + prob * pc
    return out


def _dist_public(dist: dict) -> list:
    rows = []
    for counts, prob in dist.items():
        rows.append({"counts": list(counts), "prob": prob})
    rows.sort(key=lambda row: row["counts"])
    return rows


def state_table(solver, ref_pol, T: int, snaps, content_of, action_dist_of) -> dict:
    """Positive-mass joint states against the reference policy. snaps[z][t] = (content, i, p)."""
    idx = solver.idx
    rows = []
    unequal = []
    n_action_eq = n_action_ne = n_trans_eq = n_trans_ne = 0
    for z in (0, 1):
        for t, layer in enumerate(snaps[z]):
            k = T - t
            for content, i, p in layer:
                if p == 0:
                    continue
                counts = list(idx.counts[i])
                for y in range(N_Y):
                    dist = action_dist_of(content, y)
                    ref_a = int(ref_pol[k][i * N_Y + y])
                    action_eq = dist.get(ref_a, F(0)) == 1 and all(
                        dist.get(a, F(0)) == 0 for a in range(3) if a != ref_a
                    )
                    left = _belief_transition(idx, i, y, z, dist)
                    right = _belief_transition(idx, i, y, z, {ref_a: F(1)})
                    trans_eq = left == right
                    if action_eq:
                        n_action_eq += 1
                    else:
                        n_action_ne += 1
                    if trans_eq:
                        n_trans_eq += 1
                    else:
                        n_trans_ne += 1
                    if len(dist) == 1 and F(1) in dist.values():
                        shown = int(next(a for a, pr in dist.items() if pr != 0))
                    else:
                        shown = {str(a): dist.get(a, F(0)) for a in range(3)}
                    row = {
                        "z": z,
                        "t": t,
                        "k": k,
                        "belief_counts": counts,
                        "content": content_of(content),
                        "y": y,
                        "control_action": shown,
                        "reference_action": ref_a,
                        "reference_action_name": ACT_NAME[ref_a],
                        "action_equal": action_eq,
                        "transition_equal": trans_eq,
                    }
                    rows.append(row)
                    if not trans_eq:
                        unequal.append(
                            {
                                "z": z,
                                "t": t,
                                "belief_counts": counts,
                                "y": y,
                                "control_next": _dist_public(left),
                                "reference_next": _dist_public(right),
                            }
                        )
    rows.sort(key=lambda row: (row["z"], row["t"], row["belief_counts"], str(row["content"]), row["y"]))
    return {
        "n_rows": len(rows),
        "n_action_equal": n_action_eq,
        "n_action_unequal": n_action_ne,
        "n_transition_equal": n_trans_eq,
        "n_transition_unequal": n_trans_ne,
        "rows": rows,
        "unequal_transitions": unequal,
    }


def _mb_snaps_as_joint(snaps) -> list:
    return [[(None, i, p) for i, p in layer] for layer in snaps]


def _det(action: int) -> dict:
    return {action: F(1)}


def compare_a2(solver, primary_public: dict, action_sha: str, T: int) -> list:
    path = A2 / f"TSEP-{T}.json"
    if not path.exists():
        return ["A2 file missing"]
    stored = json.loads(path.read_text(encoding="utf-8"))
    diffs = []
    for key in A2_KEYS:
        if key not in stored["primary"]:
            diffs.append(f"primary.{key}")
            continue
        _diff_packed(primary_public[key], stored["primary"][key], f"primary.{key}", diffs)
    stored_sha = stored.get("action_agreement", {}).get("primary_sha256")
    if stored_sha != action_sha:
        diffs.append("action_table_sha256")
    if solver is None:
        diffs.append("solver")
    return diffs


def _column_public(assembled_controls) -> list:
    columns = []
    for col in assembled_controls:
        fails = [name for name in CORE if col["flags"].get(name) == "FAIL"]
        columns.append(
            {
                "name": col["name"],
                "flags": col["flags"],
                "reproduction": col["reproduction"],
                "reproduction_missing": col["reproduction_missing"],
                "reproduction_disagree": col["reproduction_disagree"],
                "conjunction": col["conjunction"],
                "separating_core_criteria": fails,
                "t2_note": col.get("t2_note"),
                "donor_contrast": col.get("donor_contrast"),
                "donor_S": col.get("donor_S"),
                "donor_E": col.get("donor_E"),
                "pattern": col.get("pattern"),
                "interventions": col.get("interventions"),
            }
        )
    return columns


def evaluate_horizon(world, T: int, held: dict, theta0, clock: Clock) -> dict:
    solver = held["solver"]
    pol = held["study_pol"]
    names = [row[1] for row in roster(T)]
    if (T == 3 and len(names) != 20) or (T == 4 and len(names) != 18):
        raise Stop("integrity", f"roster length at T_SEP={T} is {len(names)}")
    primary = _call(
        clock,
        f"reference T={T}",
        lambda: evaluate_mb_family(solver, pol, T, CR, CS, "R-HAC-MB"),
    )
    action_rows = _primary_table(solver, pol, primary, T)
    action_sha = _table_sha(action_rows)
    n_entries = _entry_count(solver.idx.sum, pol, T, False)
    primary_public = _public_case(
        primary,
        held["study_values"][T - 1],
        n_entries,
        held["study_invariant"],
        len(solver.idx.counts),
    )
    a2_diffs = compare_a2(solver, primary_public, action_sha, T)
    primary.pop("snaps", None)
    record = {
        "T_SEP": T,
        "law": "H0",
        "cr": CR,
        "cs": CS,
        "status": "PRIMARY-ONLY",
        "roster": names,
        "roster_note": (
            "Eligible controls are supplied from spec FINAL section 4.1 and item8 append order. "
            "KSEP is unchanged. This supply is not a criterion change."
        ),
        "reference_integrity_vs_A2": {"ok": not a2_diffs, "failures": a2_diffs},
        "reference": primary_public,
        "reference_action_table_sha256": action_sha,
        "reference_action_table": action_rows,
        "reference_met": reference_met(primary["flags"]),
        "reference_conjunction": conjunction_of(primary["flags"]),
        "controls_raw_flags": [],
        "columns": [],
        "pm_undefined": None,
        "label_before_replay": None,
        "label_before_replay_note": None,
        "formal_label": None,
        "formal_note": None,
        "clause": None,
        "verified": False,
    }
    _write(f"TSEP-{T}.json", record)
    if a2_diffs:
        record["status"] = "INTEGRITY-FAIL"
        return record
    controls = []
    myopic_pol = _call(
        clock,
        f"myopic solve T={T}",
        lambda: solver.solve_cost(CR, CS, budget=clock, myopic=True),
    )
    myopic = _call(
        clock,
        f"myopic criteria T={T}",
        lambda: evaluate_mb_family(solver, myopic_pol["pol"], T, CR, CS, "R-HAC-MB-myopic"),
    )
    myopic.pop("snaps", None)
    controls.append(myopic)
    blind = _call(clock, f"blind T={T}", lambda: blind_result(world, solver, T, CR, CS))
    controls.append(blind)
    for _kind, name, params in roster(T):
        if _kind == "conf":
            eta, alpha = params["eta"], params["alpha"]
            controls.append(
                _call(
                    clock,
                    name,
                    lambda eta=eta, alpha=alpha, name=name: evaluate_conf(
                        solver, T, CR, CS, eta, alpha, theta0, name, clock
                    ),
                )
            )
        elif _kind == "cg":
            a_s, a_f, beta = params["alpha_s"], params["alpha_f"], params["beta"]
            controls.append(
                _call(
                    clock,
                    name,
                    lambda a_s=a_s, a_f=a_f, beta=beta, name=name: evaluate_cg(
                        solver, T, CR, CS, a_s, a_f, beta, name, clock
                    ),
                )
            )
        elif _kind == "mf":
            eps = params["eps"]
            controls.append(
                _call(
                    clock,
                    name,
                    lambda eps=eps, name=name: evaluate_mf(solver, T, CR, CS, eps, name, clock),
                )
            )
    pm = _call(
        clock,
        f"PM-ACT criteria T={T}",
        lambda: evaluate_pm(
            solver,
            pol,
            held["machine"],
            held["block"],
            T,
            CR,
            CS,
            0,
            "PM-ACT",
            clock,
        ),
    )
    controls.append(pm)
    if [c["name"] for c in controls] != names:
        record["status"] = "INTEGRITY-FAIL"
        record["name_order_ok"] = False
        _write(f"TSEP-{T}.json", record)
        return record
    record["name_order_ok"] = True
    pm_bad = (not held["well_defined"]["ok"]) or bool(pm.get("extra", {}).get("ill_defined_extractor", False))
    assembled = assemble_setting(primary, controls, incomplete=False, pm_undefined=bool(pm_bad))
    record["controls_raw_flags"] = [{"name": c["name"], "flags": c["flags"], "extra": c.get("extra")} for c in controls]
    record["columns"] = _column_public(assembled["controls"])
    record["pm_undefined"] = bool(pm_bad)
    record["pm_extra"] = pm.get("extra")
    record["label_before_replay"] = assembled["label"]
    record["label_before_replay_note"] = assembled["note"]
    record["myopic_pol_values_tail"] = myopic_pol["values"][T - 1]
    record["myopic_invariant"] = myopic_pol["invariant"]
    held["myopic_pol"] = myopic_pol["pol"]
    held["myopic_values"] = myopic_pol["values"]
    held["myopic_invariant"] = myopic_pol["invariant"]
    held["primary_result"] = primary
    held["controls"] = controls
    held["assembled"] = assembled
    held["pm_bad"] = bool(pm_bad)
    _write(f"TSEP-{T}.json", record)
    return record


def solve_myopic(world, idx: Index, T: int, cr, cs, clock: Clock):
    """Index DP. Continuation is omitted from the argmax and added back into the value."""
    immP, immM = world.imm_PM()
    py = world.py[0]
    n = len(idx.counts)
    Vprev = None
    pols = {}
    values = []
    for k in range(1, T + 1):
        clock.check(f"myopic DP k={k}")
        Vk = [F(0)] * n
        pol = {}
        for i in range(n):
            if idx.sum[i] > T - k:
                continue
            b = idx.b[i]
            acc = F(0)
            cont = Vprev[i] if k > 1 and Vprev is not None else F(0)
            for y in range(N_Y):
                ev = idx.cont_R(i, b, y, Vprev) if k > 1 else F(0)
                action, _q = _choose(immP[y], idx.correct_R(b, y) - cr, immM[y] - cs)
                pol[(i, y)] = action
                if action == P_ACT:
                    q = immP[y] + cont
                elif action == R_ACT:
                    q = idx.correct_R(b, y) - cr + ev
                else:
                    q = immM[y] - cs + cont
                acc += py[y] * q
            Vk[i] = acc
        pols[k] = pol
        values.append(Vk[0])
        Vprev = Vk
    return pols, values


def _mb_replay_failures(primary_public, replay_public, primary_rows, replay_rows, replay_interventions) -> list:
    failures = _compare_cases(primary_public, replay_public)
    if primary_public["V"] != replay_public["V"]:
        failures.append("V")
    if primary_public["n_policy_entries"] != replay_public["n_policy_entries"]:
        failures.append("n_policy_entries")
    if primary_public["n_beliefs"] != replay_public["n_beliefs"]:
        failures.append("n_beliefs")
    if primary_public["invariant_decisions"] != replay_public["invariant_decisions"]:
        failures.append("invariant_decisions")
    actions = _action_agreement(primary_rows, replay_rows)
    if actions["n_disagree"] or actions["n_missing_in_replay"] or actions["n_missing_in_primary"]:
        failures.append("action_table")
    if not _shadow_ok(replay_interventions):
        failures.append("repair_equals_shadow")
    for donor_name in ("donor_S", "donor_E"):
        if not _donor_covered(primary_rows, primary_public[donor_name]) or not _donor_covered(
            replay_rows, replay_public[donor_name]
        ):
            failures.append(f"{donor_name}_in_action_table")
    return failures, actions


def replay_reference(world, held, T: int, clock: Clock) -> dict:
    solver = held["solver"]
    idx = Index(world, T)
    pol, values = solve_reference(world, idx, T, CR, CS, clock)
    case = reference_case(world, idx, pol, T, CR, CS)
    rows = _replay_table(world, idx, pol, case, T)
    n_entries = _entry_count(idx.sum, pol, T, True)
    public = _public_case(case, values[T - 1], n_entries, idx.invariant, len(idx.counts))
    primary_rows = _primary_table(solver, held["study_pol"], {"snaps": [_snapshots(solver, held["study_pol"], T, z) for z in (0, 1)], "donor_S": held["primary_result"]["donor_S"], "donor_E": held["primary_result"]["donor_E"]}, T)
    # The evaluation block already stored the primary table. Rebuild only to compare keys.
    # Use the stored primary public, whose action table was hashed against A2.
    return {
        "public": public,
        "rows": rows,
        "case": case,
        "pol": pol,
        "primary_rows_rebuilt": primary_rows,
    }


def replay_myopic(world, held, T: int, clock: Clock) -> dict:
    solver = held["solver"]
    idx = Index(world, T)
    pol, values = solve_myopic(world, idx, T, CR, CS, clock)
    case = reference_case(world, idx, pol, T, CR, CS)
    rows = _replay_table(world, idx, pol, case, T)
    n_entries = _entry_count(idx.sum, pol, T, True)
    public = _public_case(case, values[T - 1], n_entries, idx.invariant, len(idx.counts))
    primary = next(c for c in held["controls"] if c["name"] == "R-HAC-MB-myopic")
    primary_rows = _primary_table(
        solver,
        held["myopic_pol"],
        {
            "snaps": [_snapshots(solver, held["myopic_pol"], T, z) for z in (0, 1)],
            "donor_S": primary["donor_S"],
            "donor_E": primary["donor_E"],
        },
        T,
    )
    return {"public": public, "rows": rows, "primary_rows": primary_rows, "pol": pol}


def _blind_action(world, cr, cs) -> list:
    costs = (F(0), cr, cs)
    actions = []
    for r in (0, 1):
        action, _q = _choose(world.g0[0][r] - costs[0], world.g0[1][r] - costs[1], world.g0[2][r] - costs[2])
        actions.append(action)
    return actions


def replay_blind(world, solver, T: int, clock: Clock) -> dict:
    idx = solver.idx
    act = _blind_action(world, CR, CS)
    n = len(idx.counts)
    ba = bytearray(n * N_Y)
    for i in range(n):
        for y in range(N_Y):
            ba[i * N_Y + y] = act[read_class(y)]
    pol = [None]
    for _k in range(1, T + 1):
        pol.append(ba)
    snaps = [_snapshots(solver, pol, T, z) for z in (0, 1)]
    clock.check(f"blind replay occupancy T={T}")
    raw = _cref(snaps, pol, T, world.py[0])
    dR = raw[0][0] - raw[1][0]
    dM = raw[1][1] - raw[0][1]
    immP, immM = world.imm_PM()

    def base_m(i, y, a):
        m = _m_f0(world, idx.b[i], y, a, immP, immM)
        return world.g0[a][read_class(y)], m

    e_agent, per_a = ct2_from_mixture(snaps, T, world.py[0], base_m)
    t2_flag, imp = _flag_t2(e_agent, e_base := e_agent)
    flags = {
        "C-REF": _flag_ref(dR, dM),
        "C-T2": t2_flag,
        "C-SEL": "NOT APPLICABLE",
        "C-FO": "PASS",
        "rescue": "NOT APPLICABLE",
    }
    pattern = {
        "delta_R": dR,
        "delta_M": dM,
        "E_err_agent": e_agent,
        "E_err_baseline": e_agent,
        "D_e_S": None,
        "D_e_E": None,
        "D_q_S": None,
        "D_q_E": None,
        "cfo_a": True,
        "cfo_b": True,
        "e_A_S": None,
        "e_B_S": None,
        "q_A_S": None,
        "q_B_S": None,
        "e_A_E": None,
        "e_B_E": None,
        "q_A_E": None,
        "q_B_E": None,
    }
    return {
        "name": "R-BLIND / R-CONF-S",
        "flags": flags,
        "pattern": pattern,
        "t2_note": imp if isinstance(imp, str) else None,
        "t2_improvement": None if isinstance(imp, str) else imp,
        "per_action_agent": per_a,
        "donor_contrast": False,
        "interventions": None,
        "action_of_read": act,
    }


def replay_conf(solver, ref_pol, T, cr, cs, eta, alpha, theta0, name, clock: Clock) -> dict:
    """Second occupancy. Deciding statistics then use frozen _finish_f0."""
    tables = _Tables(solver.world, solver)
    world = solver.world
    idx = solver.idx
    err = tables.err
    mass = [{(theta0, 0): F(1)}, {(theta0, 0): F(1)}]

    def bump(th, ebit):
        nxt = th + eta * (ebit - alpha)
        if nxt < 0:
            return F(0)
        if nxt > F(1, 2):
            return F(1, 2)
        return nxt

    def action_of_theta(th, y):
        if world.s_def[y] > th:
            return P_ACT
        r = read_class(y)
        action, _q = _choose(world.g0[0][r], world.g0[1][r] - cr, world.g0[2][r] - cs)
        return action

    snaps = [[], []]
    value = [F(0), F(0)]
    for t in range(T):
        clock.check(f"{name} replay t={t}")
        for z in (0, 1):
            snaps[z].append([(c, i, p) for (c, i), p in mass[z].items() if p != 0])
        new = [{}, {}]
        for z in (0, 1):
            reward = F(0)
            py = tables.py[z]
            ez = err[z]
            for (th, i), p in mass[z].items():
                for y in range(N_Y):
                    a = action_of_theta(th, y)
                    wy = p * py[y]
                    reward += wy * tables.reward(z, y, a, cr, cs)
                    if a == R_ACT:
                        atoms = ez[y][1]
                        for ebit, cid, pc in atoms:
                            w = wy * pc
                            j = idx.trans[i][cid]
                            key = (bump(th, ebit), j)
                            new[z][key] = new[z].get(key, F(0)) + w
                    else:
                        for ebit, pc in ez[y][0]:
                            w = wy * pc
                            key = (bump(th, ebit), i)
                            new[z][key] = new[z].get(key, F(0)) + w
            value[z] += reward
        mass = new

    def mhat(content, y, a):
        return world.g0[a][read_class(y)]

    def mhat_R(content, y):
        return mhat(content, y, R_ACT)

    def action_of(content, y):
        return action_of_theta(content, y)

    def advance(rec, donor, clamp, z, cr_, cs_):
        A, B = {}, {}
        reward = F(0)
        py = tables.py[z]
        ez = err[z]
        for content, i, p in rec:
            ctrl = content if donor is None else donor
            for y in range(N_Y):
                a = action_of_theta(ctrl, y)
                wy = p * py[y]
                reward += wy * tables.reward(z, y, a, cr_, cs_)
                atoms = ez[y][1] if a == R_ACT else tuple((e, None, pc) for e, pc in ez[y][0])
                for ebit, cid, pc in atoms:
                    w = wy * pc
                    j = i if cid is None else idx.trans[i][cid]
                    thA = ctrl if clamp else bump(ctrl, ebit)
                    thB = bump(content, ebit)
                    A[(thA, j)] = A.get((thA, j), F(0)) + w
                    B[(thB, j)] = B.get((thB, j), F(0)) + w
        return A, B, reward

    result = _finish_f0(
        name,
        snaps,
        T,
        tables,
        action_of,
        mhat,
        mhat_R,
        cr,
        cs,
        value,
        lambda th: (th.numerator, th.denominator),
        advance,
        extra_value=value,
    )
    result["state_table"] = state_table(
        solver,
        ref_pol,
        T,
        snaps,
        lambda th: [th.numerator, th.denominator],
        lambda content, y: _det(action_of_theta(content, y)),
    )
    return result


def replay_cg_occupancy(solver, T, cr, cs, alpha_s, alpha_f, beta, clock, name):
    """Count-tuple occupancy for the state table. Statistics come from cg_case."""
    world = solver.world
    idx = solver.idx
    tables = _Tables(world, solver)
    zero = tuple(0 for _ in range(12))
    mass = [{(zero, 0): F(1)}, {(zero, 0): F(1)}]
    from wrel.agents import cg_choose

    snaps = [[], []]
    for t in range(T):
        clock.check(f"{name} occupancy t={t}")
        for z in (0, 1):
            snaps[z].append([(c, i, p) for (c, i), p in mass[z].items() if p != 0])
        new = [{}, {}]
        for z in (0, 1):
            py = world.py[z]
            mv = tables.moves[z]
            for (content, i), p in mass[z].items():
                for y in range(N_Y):
                    a = cg_choose(content, read_class(y), cr, cs, alpha_s, alpha_f, beta)
                    wy = p * py[y]
                    r = read_class(y)
                    slot = a * 2 + r
                    for corr, cid, pc in mv[y][a]:
                        w = wy * pc
                        lst = list(content)
                        if corr:
                            lst[slot] += 1
                        else:
                            lst[6 + slot] += 1
                        j = i if cid < 0 else idx.trans[i][cid]
                        key = (tuple(lst), j)
                        new[z][key] = new[z].get(key, F(0)) + w
        mass = new
    return snaps


def replay_mf_occupancy(solver, T, cr, cs, eps, clock, name):
    """Second MF occupancy. The finish is mf_finish_on_snaps, not evaluate_mf."""
    tables = _Tables(solver.world, solver)
    world = solver.world
    idx = solver.idx
    ya = world.y_atoms()
    empty = _mf_freeze({}, -1)
    mass = [{(empty, 0): F(1)}, {(empty, 0): F(1)}]
    snaps = [[], []]
    value = [F(0), F(0)]
    for t in range(T):
        clock.check(f"{name} replay t={t} n0={len(mass[0])} n1={len(mass[1])}")
        for z in (0, 1):
            snaps[z].append([(c, i, p) for (c, i), p in mass[z].items() if p != 0])
        new = [{}, {}]
        for z in (0, 1):
            reward = F(0)
            py = tables.py[z]
            for (content, i), p in mass[z].items():
                sparse, g = _mf_thaw(content)
                for y in range(N_Y):
                    probs, phi = mf_action_probs(sparse, g, read_class(y), cr, cs, eps)
                    wy = p * py[y]
                    for a, pa in probs.items():
                        if pa == 0:
                            continue
                        slot = phi * 3 + a
                        for corr, cid, agree, pc in ya[z][y][a]:
                            w = wy * pa * pc
                            reward += w * tables.reward(z, y, a, cr, cs)
                            sp2 = _upd(sparse, slot, F(corr))
                            g2 = agree if a == R_ACT else g
                            j = i if cid is None else idx.trans[i][cid]
                            key = (_mf_freeze(sp2, g2), j)
                            new[z][key] = new[z].get(key, F(0)) + w
            value[z] += reward
        mass = new
    return snaps, value


def _content_mf(content):
    g, items = content
    return {"g": g, "q": [list(item) for item in items]}


def donor_beliefs(solver, info, donor, T: int):
    if donor is None:
        return None
    t = T - 2
    counts = []
    for b, cell in info["belief_cell"][t].items():
        if cell == donor:
            counts.append(list(solver.idx.counts[b]))
    counts.sort()
    return counts


def _pm_public(result, signature_s, signature_e) -> dict:
    extra = result.get("extra") or {}
    return {
        "flags": result["flags"],
        "pattern": result["pattern"],
        "t2_note": result["t2_note"],
        "t2_improvement": result["t2_improvement"],
        "per_action_agent": result["per_action_agent"],
        "per_action_baseline": result["per_action_baseline"],
        "donor_signature_S": signature_s,
        "donor_signature_E": signature_e,
        "donor_contrast": result["donor_contrast"],
        "interventions": result["interventions"],
        "action_mismatches": extra.get("action_mismatches"),
        "ill_defined_extractor": extra.get("ill_defined_extractor", False),
        "ill_defined": extra.get("ill_defined", False),
        "decoder_entries": extra.get("decoder_entries"),
    }


def _deciding_diff(primary: dict, replay: dict, keys: tuple) -> list:
    diffs = []
    for key in keys:
        if key not in primary and key not in replay:
            continue
        if key not in primary or key not in replay:
            diffs.append(key)
            continue
        _deep_diff(replay[key], primary[key], key, diffs)
    return diffs


def pm_statistics_on_block(solver, pol, machine, block, T, cr, cs, cost_index, name, budget=None):
    """PM-ACT criteria. Readout is the intact-distribution decoder. No extension rule."""
    tables = _Tables(solver.world, solver)
    info = index_pm(machine, block, T, cost_index)
    if info["ill_defined"]:
        flags = {k: "NOT EVALUABLE [PM quotient map ill-defined]" for k in ("C-REF", "C-T2", "C-SEL", "C-FO", "rescue")}
        pattern = _pattern(None, None, None, None, None, None, False, False)
        extra = {"ill_defined": True, "ill_examples": info["ill_examples"]}
        return _pack_result(name, flags, pattern, None, {}, {}, (None, None), False, None, extra)

    belief_cell = info["belief_cell"]
    action = info["action"]
    # Intact MB snapshots give the visit distribution. PM's action on a reachable
    # belief must equal the cell action.
    from .sep import _snapshots

    snaps_b = [_snapshots(solver, pol, T, z) for z in (0, 1)]
    mismatches = 0
    for z in (0, 1):
        for t in range(T):
            k = T - t
            pk = pol[k]
            for i, p in snaps_b[z][t]:
                if p == 0:
                    continue
                cell = belief_cell[t].get(i)
                if cell is None:
                    mismatches += 1
                    continue
                ay = action.get((t, cell))
                if ay is None:
                    mismatches += 1
                    continue
                base = i * N_Y
                for y in range(N_Y):
                    if ay[y] != pk[base + y]:
                        mismatches += 1
                        break
    # Decoder: E[m_F0 | t, cell, read, a] from intact visits.
    py = tables.py[0]
    dec_num = {}
    dec_den = {}
    for t in range(T):
        for z in (0, 1):
            for i, p in snaps_b[z][t]:
                if p == 0:
                    continue
                cell = belief_cell[t].get(i)
                if cell is None:
                    continue
                b = tables.b[i]
                for y in range(N_Y):
                    r = read_class(y)
                    w = F(1, 2) * p * py[y]
                    for a in (R_ACT, M_ACT):
                        key = (t, cell, r, a)
                        m = tables.m_f0(b, y) if a == R_ACT else tables.immM[y]
                        dec_num[key] = dec_num.get(key, F(0)) + w * m
                        dec_den[key] = dec_den.get(key, F(0)) + w
    decoder = {}
    for key, den in dec_den.items():
        if den != 0:
            decoder[key] = dec_num[key] / den

    def mhat_cell(t, cell, y, a):
        key = (t, cell, read_class(y), a)
        return decoder.get(key)

    # Build PM snaps as (cell, bayes_i, p) by merging beliefs that share a cell.
    snaps = [[], []]
    for z in (0, 1):
        for t in range(T):
            acc = {}
            for i, p in snaps_b[z][t]:
                if p == 0:
                    continue
                cell = belief_cell[t].get(i)
                if cell is None:
                    continue
                key = (cell, i)
                acc[key] = acc.get(key, F(0)) + p
            snaps[z].append([(c, i, p) for (c, i), p in acc.items()])

    def action_of_t(t):
        def action_of(content, y, t=t):
            ay = action.get((t, content))
            if ay is None:
                return P_ACT
            return ay[y]

        return action_of

    # C-REF across trials needs the per-trial action. _cref uses one action_of.
    # Compute directly.
    n = [[F(0), F(0)], [F(0), F(0)]]
    for z in (0, 1):
        for t in range(T):
            aof = action_of_t(t)
            for content, i, p in snaps[z][t]:
                for y in SPLIT:
                    w = p * py[y]
                    a = aof(content, y)
                    if a == R_ACT:
                        n[z][0] += w
                    elif a == M_ACT:
                        n[z][1] += w
    dR = n[0][0] - n[1][0]
    dM = n[1][1] - n[0][1]

    def mhat_of(content_t, y, a):
        # content_t is (t, cell) — we'll call _ct2 with snaps rewritten.
        return None

    # Custom C-T2 because the decoder depends on the trial.
    per_agent = {}
    per_base = {}
    for a in (R_ACT, M_ACT):
        acc_ag = acc_b = F(0)
        ok = True
        for t in range(T):
            num_a = num_b = den = F(0)
            for z in (0, 1):
                for cell, i, p in snaps[z][t]:
                    b = tables.b[i]
                    for y in SPLIT:
                        w = F(1, 2) * p * py[y]
                        den += w
                        mh = mhat_cell(t, cell, y, a)
                        if mh is None:
                            ok = False
                            break
                        m = tables.m_f0(b, y) if a == R_ACT else tables.immM[y]
                        num_a += w * (mh - m) ** 2
                        gb = tables.world.g0[a][read_class(y)]
                        num_b += w * (gb - m) ** 2
                    if not ok:
                        break
                if not ok:
                    break
            if not ok or den == 0:
                ok = False
                break
            acc_ag += num_a / den
            acc_b += num_b / den
        per_agent[a] = None if not ok else acc_ag / T
        per_base[a] = None if not ok else acc_b / T
    if per_agent[R_ACT] is None or per_agent[M_ACT] is None:
        e_agent = None
    else:
        e_agent = (per_agent[R_ACT] + per_agent[M_ACT]) / 2
    if per_base[R_ACT] is None or per_base[M_ACT] is None:
        e_base = None
    else:
        e_base = (per_base[R_ACT] + per_base[M_ACT]) / 2

    # Donors: MB donors passed via max/min b among PM joint states, content = cell.
    t_star = T - 2
    def encode(cell):
        return (cell,)

    dS, dE, _ms, _me = _select(snaps, t_star, tables, encode)
    cS = _contrast(snaps, t_star, 1, dS, dE)
    cE = _contrast(snaps, t_star, 0, dE, dS)
    contrast = bool(cS and cE and dS is not None)

    def cell_mhat_R(t, cell, y):
        return mhat_cell(t, cell, y, R_ACT)

    def stats_at(records, z, t, mhat_fn):
        py_z = tables.py[z]
        num_e = num_q = num_L = den = F(0)
        missing = False
        aof = action_of_t(t)
        for content, i, p in records:
            if p == 0:
                continue
            for y in SPLIT:
                w = p * py_z[y]
                den += w
                if aof(content, y) == R_ACT:
                    num_q += w
                mh = mhat_fn(content, y)
                if mh is None:
                    missing = True
                    break
                m = tables.m_pin(z, y)
                d = mh - m
                num_e += w * d
                num_L += w * (d if d >= 0 else -d)
            if missing:
                break
        if missing or den == 0:
            return None
        return {"e": num_e / den, "q": num_q / den, "L": num_L / den}

    # Advance using machine successors when the cell's action is R/P/M.
    # Intact successor table is keyed by (t, cell, y, a, obs, x).
    # For a donor cell installed into a recipient, the successor of SWAP is the
    # successor of the donor cell. Clamp keeps the donor belief's next-layer cell
    # of the *un-updated* belief. Cells may contain many beliefs; clamping each
    # belief is ill-defined if they part. We detect that and return None stats.
    world = tables.world
    members = defaultdict(list)
    for t in range(T):
        for b, cell in belief_cell[t].items():
            members[(t, cell)].append(b)
    _cell_cache = {}

    def cell_after(t, cell, cid):
        """Cell at t+1 after applying class cid, or None to keep the belief. 'BAD' if not a function."""
        key = (t, cell, cid)
        hit = _cell_cache.get(key)
        if hit is not None:
            return hit
        if t + 1 >= T:
            _cell_cache[key] = "BAD"
            return "BAD"
        nxt = set()
        for b in members[(t, cell)]:
            b2 = b if cid is None else tables.idx.trans[b][cid]
            if b2 is None or b2 < 0:
                _cell_cache[key] = "BAD"
                return "BAD"
            n = belief_cell[t + 1].get(b2)
            if n is None:
                _cell_cache[key] = "BAD"
                return "BAD"
            nxt.add(n)
            if len(nxt) > 1:
                _cell_cache[key] = "BAD"
                return "BAD"
        if len(nxt) != 1:
            _cell_cache[key] = "BAD"
            return "BAD"
        val = next(iter(nxt))
        _cell_cache[key] = val
        return val

    def advance_pm(rec, donor_cell, clamp, z):
        """A/B masses at t_star+1. Shadow applies the taken action to the pre-perturbation cell.

        A clamped controller keeps its belief. A free controller applies the class update.
        Returns (None, None) when a cell's image is not a single cell.
        """
        A, B = {}, {}
        t = t_star
        py_z = tables.py[z]
        for cell, i, p in rec:
            ctrl = cell if donor_cell is None else donor_cell
            for y in range(N_Y):
                ay = action.get((t, ctrl))
                if ay is None:
                    return None, None
                a = ay[y]
                if a == R_ACT:
                    pairs = []
                    for yp in range(N_Y):
                        for x in (0, 1):
                            ww = F(1, 2) * world.Lre[z][y][yp][x] / py_z[y]
                            if ww != 0:
                                pairs.append((world.cls[y][yp][x], ww))
                else:
                    pairs = [(None, F(1))]
                for cid, pc in pairs:
                    w = p * py_z[y] * pc
                    j = i if cid is None else tables.idx.trans[i][cid]
                    cA = cell_after(t, ctrl, None if clamp or cid is None else cid)
                    cB = cell_after(t, cell, cid)
                    if cA == "BAD" or cB == "BAD":
                        return None, None
                    A[(cA, j)] = A.get((cA, j), F(0)) + w
                    B[(cB, j)] = B.get((cB, j), F(0)) + w
        return A, B

    interventions = {"S": None, "E": None}
    design_gap = False
    if dS is not None and dE is not None:
        for direction, z, donor in (("S", 1, dS), ("E", 0, dE)):
            rec = snaps[z][t_star]
            intact = stats_at(rec, z, t_star, lambda c, y, d=donor: cell_mhat_R(t_star, c, y))
            modes = {}
            for mode in ("SWAP", "CORRUPT", "SUSPEND"):
                if mode == "SUSPEND":
                    now_rec = rec
                    donor_use = None
                    clamp = True
                    mhat_now = lambda c, y: cell_mhat_R(t_star, c, y)
                else:
                    now_rec = [(donor, 0, F(1))]
                    donor_use = donor
                    clamp = mode == "CORRUPT"
                    mhat_now = lambda c, y, d=donor: cell_mhat_R(t_star, d, y)
                now = stats_at(now_rec, z, t_star, mhat_now)
                A, B = advance_pm(rec, donor_use, clamp, z)
                if A is None:
                    design_gap = True
                    modes[mode] = {
                        "D_e": None, "D_q": None, "e_now": None, "q_now": None,
                        "e_intact": None if intact is None else intact["e"],
                        "q_intact": None if intact is None else intact["q"],
                        "eA": None, "eB": None, "qA": None, "qB": None, "LA": None, "LB": None,
                        "repair_equals_shadow": False,
                        "note": "UNRESOLVED-DESIGN [quotient successor not a function]",
                    }
                    continue
                mhat_next = lambda c, y: cell_mhat_R(t_star + 1, c, y)
                stA = stats_at(((c, i, p) for (c, i), p in A.items()), z, t_star + 1, mhat_next)
                stB = stats_at(((c, i, p) for (c, i), p in B.items()), z, t_star + 1, mhat_next)
                de = None if now is None or intact is None else now["e"] - intact["e"]
                dq = None if now is None or intact is None else now["q"] - intact["q"]
                modes[mode] = {
                    "D_e": de,
                    "D_q": dq,
                    "e_now": None if now is None else now["e"],
                    "q_now": None if now is None else now["q"],
                    "e_intact": None if intact is None else intact["e"],
                    "q_intact": None if intact is None else intact["q"],
                    "eA": None if stA is None else stA["e"],
                    "eB": None if stB is None else stB["e"],
                    "qA": None if stA is None else stA["q"],
                    "qB": None if stB is None else stB["q"],
                    "LA": None if stA is None else stA["L"],
                    "LB": None if stB is None else stB["L"],
                    "repair_equals_shadow": True,
                }
            interventions[direction] = modes
    swap_s = None if interventions["S"] is None else interventions["S"]["SWAP"]
    swap_e = None if interventions["E"] is None else interventions["E"]["SWAP"]
    # C-FO: p0 is F0. Decisions equal across beliefs represented at t_star iff A11 on those beliefs.
    beliefs = []
    for z in (0, 1):
        for cell, i, p in snaps[z][t_star]:
            if p != 0:
                beliefs.append(tables.b[i])
    cfo_a, cfo_b = _cfo_mb(world, beliefs)
    cfo = "PASS" if cfo_a == "PASS" and cfo_b == "PASS" else "FAIL"
    if design_gap:
        # an ill-defined successor makes the affected statistics unavailable
        cfo = cfo  # leave C-FO as computed; rescue/sel follow None fields
    usable = contrast and not design_gap
    flags, imp = _flags_from(dR, dM, e_agent, e_base, swap_s, swap_e, cfo, usable)
    if design_gap:
        flags["C-SEL"] = "NOT EVALUABLE [PM quotient successor not a function]"
        flags["rescue"] = "NOT EVALUABLE [PM quotient successor not a function]"
    pattern = _pattern(
        dR, dM, e_agent, e_base,
        swap_s if usable else None,
        swap_e if usable else None,
        cfo_a == "PASS", cfo_b == "PASS",
    )
    extra = {
        "action_mismatches": mismatches,
        "decoder_entries": len(decoder),
        "ill_defined_extractor": info["ill_defined"] or design_gap,
        "reachable": [len(snaps[0][t]) for t in range(T)],
        "zero_support_rule": "A decoder cell with zero intact support is NOT EVALUABLE. No extension rule is applied.",
    }
    return _pack_result(
        name, flags, pattern, imp, per_agent, per_base,
        (dS, dE), contrast and not design_gap, interventions, extra,
    )


def mf_finish_on_snaps(solver, snaps, value, T, cr, cs, eps, name, budget=None):
    """Frozen MF deciding-pattern arithmetic on a caller-supplied occupancy. Not a call to evaluate_mf."""
    tables = _Tables(solver.world, solver)
    world = solver.world
    idx = solver.idx
    ya = world.y_atoms()
    if budget is not None:
        budget.check(name + " finish")

    def mhat(content, y, a):
        return _mf_mhat(content, y, a)

    # Checking probability under ε-greedy is the expected probability of R, not an indicator.
    def cref_mf():
        py = tables.py[0]
        out = []
        for z in (0, 1):
            nR = nM = F(0)
            for t in range(T):
                for content, i, p in snaps[z][t]:
                    if p == 0:
                        continue
                    sparse, g = _mf_thaw(content)
                    for y in SPLIT:
                        w = p * py[y]
                        probs, _ = mf_action_probs(sparse, g, read_class(y), cr, cs, eps)
                        nR += w * probs.get(R_ACT, F(0))
                        nM += w * probs.get(M_ACT, F(0))
            out.append((nR, nM))
        return out

    def stats_mf(records, z):
        py = tables.py[z]
        num_e = num_q = num_L = den = F(0)
        for content, i, p in records:
            if p == 0:
                continue
            sparse, g = _mf_thaw(content)
            for y in SPLIT:
                w = p * py[y]
                den += w
                probs, _ = mf_action_probs(sparse, g, read_class(y), cr, cs, eps)
                num_q += w * probs.get(R_ACT, F(0))
                mh = _mf_mhat(content, y, R_ACT)
                m = tables.m_pin(z, y)
                d = mh - m
                num_e += w * d
                num_L += w * (d if d >= 0 else -d)
        if den == 0:
            return None
        return {"e": num_e / den, "q": num_q / den, "L": num_L / den}

    def advance(rec, donor, clamp, z, cr_, cs_):
        A, B = {}, {}
        reward = F(0)
        py = tables.py[z]
        for content, i, p in rec:
            ctrl = content if donor is None else donor
            sparse, g = _mf_thaw(ctrl)
            base_s, base_g = _mf_thaw(content)
            for y in range(N_Y):
                probs, phi = mf_action_probs(sparse, g, read_class(y), cr_, cs_, eps)
                wy = p * py[y]
                for a, pa in probs.items():
                    if pa == 0:
                        continue
                    slot = phi * 3 + a
                    for corr, cid, agree, pc in ya[z][y][a]:
                        w = wy * pa * pc
                        reward += w * tables.reward(z, y, a, cr_, cs_)
                        j = i if cid is None else idx.trans[i][cid]
                        if clamp:
                            sA = ctrl
                        else:
                            sp2 = _upd(sparse, slot, F(corr))
                            g2 = agree if a == R_ACT else g
                            sA = _mf_freeze(sp2, g2)
                        spB = _upd(base_s, slot, F(corr))
                        gB = agree if a == R_ACT else base_g
                        sB = _mf_freeze(spB, gB)
                        A[(sA, j)] = A.get((sA, j), F(0)) + w
                        B[(sB, j)] = B.get((sB, j), F(0)) + w
        return A, B, reward

    # Custom finish using stats_mf / cref_mf, because q is a probability not an indicator.
    raw = cref_mf()
    dR = raw[0][0] - raw[1][0]
    dM = raw[1][1] - raw[0][1]

    def base_mhat(content, y, a):
        return world.g0[a][read_class(y)]

    e_agent, per_a = _ct2(snaps, T, tables, mhat)
    e_base, per_b = _ct2(snaps, T, tables, base_mhat)
    t_star = T - 2

    def encode(content):
        return content

    dS, dE, _ms, _me = _select(snaps, t_star, tables, encode)
    cS = _contrast(snaps, t_star, 1, dS, dE)
    cE = _contrast(snaps, t_star, 0, dE, dS)
    contrast = bool(cS and cE and dS is not None)
    interventions = {"S": None, "E": None}
    if contrast or (dS is not None and dE is not None):
        for direction, z, donor in (("S", 1, dS), ("E", 0, dE)):
            rec = snaps[z][t_star]
            intact = stats_mf(rec, z)
            modes = {}
            for mode, don, clamp in (("SWAP", donor, False), ("CORRUPT", donor, True), ("SUSPEND", None, True)):
                if mode == "SUSPEND":
                    now = intact
                else:
                    now = stats_mf([(donor, 0, F(1))], z)
                A, B, reward = advance(rec, don, clamp, z, cr, cs)
                stA = stats_mf(((c, i, p) for (c, i), p in A.items()), z)
                stB = stats_mf(((c, i, p) for (c, i), p in B.items()), z)
                de = None if now is None or intact is None else now["e"] - intact["e"]
                dq = None if now is None or intact is None else now["q"] - intact["q"]
                modes[mode] = {
                    "D_e": de,
                    "D_q": dq,
                    "e_now": None if now is None else now["e"],
                    "q_now": None if now is None else now["q"],
                    "e_intact": None if intact is None else intact["e"],
                    "q_intact": None if intact is None else intact["q"],
                    "eA": None if stA is None else stA["e"],
                    "eB": None if stB is None else stB["e"],
                    "qA": None if stA is None else stA["q"],
                    "qB": None if stB is None else stB["q"],
                    "LA": None if stA is None else stA["L"],
                    "LB": None if stB is None else stB["L"],
                    "repair_equals_shadow": True,
                    "reward_perturbed_trial": reward,
                }
            interventions[direction] = modes
    swap_s = None if interventions["S"] is None else interventions["S"]["SWAP"]
    swap_e = None if interventions["E"] is None else interventions["E"]["SWAP"]
    cfo = "PASS"
    flags, imp = _flags_from(dR, dM, e_agent, e_base, swap_s, swap_e, cfo, contrast)
    # Reproduction components of a criterion that is not evaluable stay unavailable.
    pattern = _pattern(
        dR, dM, e_agent, e_base,
        swap_s if contrast else None,
        swap_e if contrast else None,
        True, True,
    )
    extra = {
        "V_S": value[0],
        "V_E": value[1],
        "V": (value[0] + value[1]) / 2,
        "reachable": [len(snaps[0][t]) for t in range(T)],
        "cfo_note": "F0 pre-check probabilities and F0 binary decisions do not depend on (q, g).",
    }
    donors_out = (
        None if dS is None else {"g": dS[0], "n_q_entries": len(dS[1])},
        None if dE is None else {"g": dE[0], "n_q_entries": len(dE[1])},
    )
    return _pack_result(name, flags, pattern, imp, per_a, per_b, donors_out, contrast, interventions, extra)


def _fmt(value) -> str:
    if isinstance(value, F):
        return f"{value.numerator}/{value.denominator}"
    if value is None:
        return "—"
    return str(value)


def _results_text(state: dict) -> str:
    lines = [
        "# RESULTS A3",
        "",
        "Exploratory W-REL named-control comparison under Addendum A3. Earlier results are unchanged. This file is additive.",
        "",
        f"Binding approval: `c4_reliability_APPROVAL_ADDENDUM_A3.md`, sha256 `{APPROVAL_SHA}`, recorded 2026-10-21, 2:45 PM ET. The frozen procedure is `c4_reliability_exact_check_spec_ADDENDUM_A3.md`.",
        "",
        f"Code commit at process start: `{state['head']}`.",
        "",
        "The eligible roster is supplied explicitly at `(c_R, c_S) = (1/100, 3/50)` because that pair is not in frozen `KSEP`. The supply follows spec FINAL section 4.1 and `item8` append order. It is not a criterion change. `KSEP` is unchanged.",
        "",
        "PM-ACT is built with `n_costs=6`. The other five descriptive costs are the frozen input alphabet. No A-SEP criterion is evaluated at those costs. Descriptive `PM_k` is not built. R-CONF-ENUM is not evaluated.",
        "",
        "No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. This file is not an all-controller certificate. A T_SEP = 4 result cannot claim to distinguish R-HAC-MF.",
        "",
        "## Smoke test",
        "",
    ]
    smoke = state.get("smoke")
    if smoke is None:
        lines.append("The T = 1 smoke test did not run.")
    else:
        lines.extend(
            [
                f"- Backward value: `{_fmt(smoke['V_backward'])}`",
                f"- Forward mixture: `{_fmt(smoke['V_forward_mixture'])}`",
                f"- Stored ITEM-2 `V_star`: `{_fmt(smoke['stored_V_star'])}`",
                f"- Mismatches: {', '.join(smoke['mismatches']) if smoke['mismatches'] else 'none'}",
                f"- Integrity: {'AGREE' if smoke['ok'] else 'FAIL'}",
                f"- Stage wall: {smoke['clock']['stage_wall_seconds_float']} seconds",
                f"- Stage sampled peak RSS: {smoke['clock']['stage_peak_rss_bytes_sampled']} bytes",
                f"- Process high-water mark at stage end: {smoke['clock']['process_hwm_bytes']} bytes",
                "",
            ]
        )
    lines.extend(["## PM-ACT closure", ""])
    pm = state.get("pm")
    if not pm:
        lines.append("PM construction did not record a horizon.")
        lines.append("")
    for horizon in pm or []:
        wd = horizon["well_defined"]
        lines.extend(
            [
                f"### T_SEP = {horizon['T_SEP']}",
                "",
                f"- Input domain: six descriptive costs. Study cost index `{horizon['cost_index']}`. A-SEP criteria were not run on the other five.",
                f"- Donor S index `{horizon['donor_S_index']}`, counts `{horizon['donor_S_counts']}`.",
                f"- Donor E index `{horizon['donor_E_index']}`, counts `{horizon['donor_E_counts']}`.",
                f"- States: `{horizon['counts']['n_states']}`. Controller total `{horizon['counts']['controller_total']}`. Apparatus total `{horizon['counts']['apparatus_total']}`.",
                f"- Primary blocks: {horizon['n_blocks_primary']}. Queue-refiner blocks: {horizon['n_blocks_queue']}.",
                f"- Partition equality: `{horizon['partition_equal']}`.",
                f"- `well_defined.ok`: `{wd['ok']}`. Capped bad-symbol count: {wd['n_bad_symbols_capped']}.",
                f"- Reachable phase-1 controller beliefs by trial: `{horizon['reachable_beliefs_phase1']}`.",
                f"- `PM_k` built: `{horizon['pm_k_built']}`.",
                "",
            ]
        )
    lines.extend(["## Settings", ""])
    if not state["settings"]:
        lines.append("No T_SEP setting was evaluated.")
        lines.append("")
    for setting in state["settings"]:
        flags = setting["reference"]["flags"]
        lines.extend(
            [
                f"### T_SEP = {setting['T_SEP']}",
                "",
                f"Reference conjunction: `{setting['reference_conjunction']}`. `reference_met`: `{setting['reference_met']}`.",
                "",
                "| Criterion | Reference |",
                "| --- | --- |",
                f"| C-REF | {flags['C-REF']} |",
                f"| C-T2 | {flags['C-T2']} |",
                f"| C-SEL | {flags['C-SEL']} |",
                f"| C-FO | {flags['C-FO']} |",
                f"| rescue | {flags['rescue']} |",
                "",
                f"Reference integrity against stored A2: `{'AGREE' if setting['reference_integrity_vs_A2']['ok'] else 'FAIL'}`.",
                "",
            ]
        )
        if setting["reference_integrity_vs_A2"]["failures"]:
            lines.append(
                "A2 differences: " + ", ".join(setting["reference_integrity_vs_A2"]["failures"]) + "."
            )
            lines.append("")
        if setting.get("formal_label") is None:
            lines.append("Formal label: not issued.")
        else:
            lines.append(f"Formal label: **{setting['formal_label']}**.")
        lines.append("")
        if setting.get("formal_note"):
            lines.append(f"Note: {setting['formal_note']}")
            lines.append("")
        if setting.get("clause"):
            lines.append(f"Decision-order clause from the frozen note: `{setting['clause']}`.")
            lines.append("")
        if setting.get("label_before_replay"):
            lines.append(
                f"Label before the replay gate: `{setting['label_before_replay']}` ({setting.get('label_before_replay_note')})."
            )
            lines.append("")
        lines.append(f"Status: `{setting['status']}`. `pm_undefined`: `{setting.get('pm_undefined')}`.")
        lines.append("")
        if setting["T_SEP"] == 4:
            lines.append("R-HAC-MF is not eligible at T_SEP = 4. This result cannot claim to distinguish MF.")
            lines.append("")
        lines.extend(
            [
                "| Control | Reproduction | Conjunction | Separating core criteria | Pattern keys outside ρ_REP |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for col in setting.get("columns") or []:
            fails = ", ".join(col["separating_core_criteria"]) if col["separating_core_criteria"] else "—"
            disagree = ", ".join(col["reproduction_disagree"]) if col["reproduction_disagree"] else "—"
            lines.append(
                f"| {col['name']} | {col['reproduction']} | {col['conjunction']} | {fails} | {disagree} |"
            )
        lines.append("")
        replays = setting.get("replays") or {}
        if not replays:
            lines.append("Independent replay: not run.")
        else:
            lines.append("Independent replay:")
            lines.append("")
            for name, info in replays.items():
                failed = ", ".join(info["failures"]) if info["failures"] else "none"
                lines.append(f"- `{name}`: `{'AGREE' if info['agreed'] else 'FAIL'}`; differences: {failed}.")
        lines.append("")
        summary = setting.get("state_summary") or {}
        if summary:
            lines.append("Action and belief-transition comparison against the reference:")
            lines.append("")
            for name, info in summary.items():
                lines.append(
                    f"- `{name}`: action equal {info['n_action_equal']}, unequal {info['n_action_unequal']}; "
                    f"transition equal {info['n_transition_equal']}, unequal {info['n_transition_unequal']}."
                )
            lines.append("")
            lines.append(
                f"Per-state rows are in `outputs/attainability_A3/TSEP-{setting['T_SEP']}-states.json`."
            )
            lines.append("")
    lines.extend(["## Compute", ""])
    clock = state.get("clock") or {}
    lines.extend(
        [
            "Command, from `c4_reliability_exact_check_v1`:",
            "",
            "```text",
            "taskset -c 0 python3 -u -m wrel.attainability_a3",
            "```",
            "",
            f"- Cumulative wall: {clock.get('cumulative_wall_seconds_float')} seconds",
            f"- Sampled peak RSS: {clock.get('peak_rss_bytes_sampled')} bytes",
            f"- Process high-water mark: {clock.get('process_hwm_bytes')} bytes",
            "- Limits: one CPU process, 60 cumulative minutes, 20 minutes inside each named block, 8 GB resident memory, no GPU.",
            "- Smoke-test stage limit: 60 seconds. Invocations used: "
            f"{state.get('smoke_invocations', 0)}.",
            "",
        ]
    )
    for block in state.get("blocks") or []:
        lines.extend(
            [
                f"### Block `{block['stage']}`",
                "",
                f"- Wall: {block['stage_wall_seconds_float']} seconds",
                f"- Sampled peak RSS: {block['stage_peak_rss_bytes_sampled']} bytes",
                f"- Process high-water mark: {block['process_hwm_bytes']} bytes",
                "",
                "| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |",
                "| --- | --- | --- | --- |",
            ]
        )
        for inv in block.get("invocations") or []:
            lines.append(
                f"| {inv['name']} | {inv['wall_seconds_float']} | {inv['peak_rss_bytes_sampled']} | {inv['process_hwm_bytes']} |"
            )
        lines.append("")
    lines.extend(
        [
            "Thresholds read from the frozen `wrel/sep.py` constants:",
            "",
            f"- μ_REF = `{_fmt(MU_REF)}`",
            f"- μ_T2 = `{_fmt(MU_T2)}`",
            f"- μ_SEL,a = `{_fmt(MU_SELa)}`",
            f"- μ_SEL,c = `{_fmt(MU_SELc)}`",
            f"- μ_RES,a = `{_fmt(MU_RESa)}`",
            f"- μ_RES,c = `{_fmt(MU_RESc)}`",
            f"- μ_RES,L = `{_fmt(MU_RESL)}`",
            f"- ρ_REP = `{_fmt(RHO)}`",
            "",
            "## Stop and deviation",
            "",
        ]
    )
    if state.get("stop") is None:
        lines.append("The batch finished inside the approved limits. No approved stop fired.")
    else:
        lines.append(f"Approved stop: kind `{state['stop']['kind']}`, where `{state['stop']['where']}`.")
        lines.append("Partial results are the files written before the stop. No setting was substituted.")
    lines.append("")
    if state.get("deviation"):
        lines.append(f"Deviation: {state['deviation']}")
    else:
        lines.append("Deviation: none.")
    if state.get("traceback"):
        lines.extend(["", "```text", state["traceback"].rstrip(), "```"])
    lines.extend(["", "## Output hashes", ""])
    hashes = state.get("hashes") or {}
    if not hashes:
        lines.append("No output hash was recorded.")
    else:
        for name, digest in hashes.items():
            lines.append(f"- `{name}`: `{digest}`")
    lines.extend(
        [
            "",
            "The sha256 of this file is `outputs/attainability_A3/RESULTS_A3.sha256`. It is computed after this file is written.",
            "",
        ]
    )
    return "\n".join(lines)


def _hash_outputs() -> dict:
    hashes = {}
    for name in OUTPUT_NAMES:
        if name in ("HASHES.txt", "RESULTS_A3.sha256"):
            continue
        path = OUT / name
        if path.exists():
            hashes[f"outputs/attainability_A3/{name}"] = sha256_file(str(path))
    return hashes


def _write_hashes(hashes: dict) -> None:
    body = "".join(f"SHA256 {name} {digest}\n" for name, digest in hashes.items())
    path = OUT / "HASHES.txt"
    path.write_text(body, encoding="utf-8")
    hashes["outputs/attainability_A3/HASHES.txt"] = sha256_file(str(path))


def _finalize(state: dict, clock: Clock) -> None:
    state["clock"] = clock.snapshot()
    summary = {
        "approval_sha256": APPROVAL_SHA,
        "head": state["head"],
        "cpu_allowed": state.get("cpu"),
        "smoke_ok": None if state.get("smoke") is None else state["smoke"]["ok"],
        "pm": [
            {
                "T_SEP": item["T_SEP"],
                "partition_equal": item["partition_equal"],
                "well_defined_ok": item["well_defined"]["ok"],
                "n_states": item["counts"]["n_states"],
            }
            for item in state.get("pm") or []
        ],
        "settings": [
            {
                "T_SEP": item["T_SEP"],
                "status": item["status"],
                "formal_label": item.get("formal_label"),
                "formal_note": item.get("formal_note"),
                "clause": item.get("clause"),
                "reference_conjunction": item.get("reference_conjunction"),
                "pm_undefined": item.get("pm_undefined"),
                "verified": item.get("verified"),
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
    _write_hashes(hashes)
    state["hashes"] = hashes
    results_path = ROOT / "RESULTS_A3.md"
    results_path.write_text(_results_text(state), encoding="utf-8")
    digest = sha256_file(str(results_path))
    (OUT / "RESULTS_A3.sha256").write_text(f"{digest}  RESULTS_A3.md\n", encoding="utf-8")
    state["results_sha256"] = digest


def _verify_horizon(world, T: int, held: dict, record: dict, theta0, clock: Clock) -> dict:
    solver = held["solver"]
    ref_pol = held["study_pol"]
    replays = {}
    states = {}
    primary_ref = record["reference"]

    def add_table(name, table):
        states[name] = {
            "n_rows": table["n_rows"],
            "n_action_equal": table["n_action_equal"],
            "n_action_unequal": table["n_action_unequal"],
            "n_transition_equal": table["n_transition_equal"],
            "n_transition_unequal": table["n_transition_unequal"],
            "rows": table["rows"],
            "unequal_transitions": table["unequal_transitions"],
        }

    ref = _call(clock, f"replay reference T={T}", lambda: replay_reference(world, held, T, clock))
    # Compare replay public to the A2-checked primary public.
    failures, actions = _mb_replay_failures(
        primary_ref, ref["public"], record["reference_action_table"], ref["rows"], ref["case"]["interventions"]
    )
    replays["R-HAC-MB"] = {"agreed": not failures, "failures": failures, "action_agreement": actions}
    if failures:
        record["replays"] = replays
        raise Stop("integrity", f"T_SEP={T} reference replay disagrees")
    ref_snaps = [_snapshots(solver, ref_pol, T, z) for z in (0, 1)]
    mb_joint = []
    for z in (0, 1):
        layers = []
        for t, layer in enumerate(ref_snaps[z]):
            k = T - t
            layers.append([( (i, k), i, p) for i, p in layer])
        mb_joint.append(layers)

    def mb_dist(content, y, pol=ref_pol):
        i, k = content
        return _det(int(pol[k][i * N_Y + y]))

    add_table("R-HAC-MB", state_table(solver, ref_pol, T, mb_joint, lambda content: list(solver.idx.counts[content[0]]), mb_dist))

    my = _call(clock, f"replay myopic T={T}", lambda: replay_myopic(world, held, T, clock))
    my_primary = next(c for c in held["controls"] if c["name"] == "R-HAC-MB-myopic")
    my_public_primary = _public_case(
        my_primary,
        held["myopic_values"][T - 1],
        _entry_count(solver.idx.sum, held["myopic_pol"], T, False),
        held["myopic_invariant"],
        len(solver.idx.counts),
    )
    my_failures, my_actions = _mb_replay_failures(
        my_public_primary, my["public"], my["primary_rows"], my["rows"], my["public"]["interventions"]
    )
    replays["R-HAC-MB-myopic"] = {"agreed": not my_failures, "failures": my_failures, "action_agreement": my_actions}
    if my_failures:
        record["replays"] = replays
        raise Stop("integrity", "T_SEP=%s myopic replay disagrees" % T)
    my_snaps = [_snapshots(solver, held["myopic_pol"], T, z) for z in (0, 1)]
    my_joint = []
    for z in (0, 1):
        layers = []
        for t, layer in enumerate(my_snaps[z]):
            k = T - t
            layers.append([((i, k), i, p) for i, p in layer])
        my_joint.append(layers)

    def my_dist(content, y, pol=held["myopic_pol"]):
        i, k = content
        return _det(int(pol[k][i * N_Y + y]))

    add_table(
        "R-HAC-MB-myopic",
        state_table(solver, ref_pol, T, my_joint, lambda content: list(solver.idx.counts[content[0]]), my_dist),
    )

    blind_primary = next(c for c in held["controls"] if c["name"] == "R-BLIND / R-CONF-S")
    blind = _call(clock, f"replay blind T={T}", lambda: replay_blind(world, solver, T, clock))
    # Attach the study policy comparison, replacing the placeholder table.
    act = blind["action_of_read"]
    blind_pol = [None]
    ba = bytearray(len(solver.idx.counts) * N_Y)
    for i in range(len(solver.idx.counts)):
        for y in range(N_Y):
            ba[i * N_Y + y] = act[read_class(y)]
    for _k in range(T):
        blind_pol.append(ba)
    bsnaps = [_snapshots(solver, blind_pol, T, z) for z in (0, 1)]
    bjoint = _mb_snaps_as_joint(bsnaps)

    def bdist(_content, y, act=act):
        return _det(act[read_class(y)])

    blind_table = state_table(solver, ref_pol, T, bjoint, lambda _c: None, bdist)
    add_table("R-BLIND / R-CONF-S", blind_table)
    blind.pop("state_table", None)
    bdiff = _deciding_diff(
        blind_primary,
        blind,
        ("flags", "pattern", "t2_note", "t2_improvement", "per_action_agent", "donor_contrast", "interventions", "action_of_read"),
    )
    replays["R-BLIND / R-CONF-S"] = {"agreed": not bdiff, "failures": bdiff}
    if bdiff:
        record["replays"] = replays
        raise Stop("integrity", f"T_SEP={T} blind replay disagrees")

    for kind, name, params in roster(T):
        if kind in ("myopic", "blind", "pm"):
            continue
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
            add_table(name, table)
            primary = next(c for c in held["controls"] if c["name"] == name)
            diff = _deciding_diff(
                primary,
                got,
                (
                    "flags",
                    "pattern",
                    "t2_note",
                    "t2_improvement",
                    "per_action_agent",
                    "per_action_baseline",
                    "donor_S",
                    "donor_E",
                    "donor_contrast",
                    "interventions",
                ),
            )
            extra_p = primary.get("extra") or {}
            extra_g = got.get("extra") or {}
            if extra_p.get("V") != extra_g.get("V"):
                diff.append("V")
            replays[name] = {"agreed": not diff, "failures": diff}
            if diff:
                record["replays"] = replays
                _write(f"TSEP-{T}-states.json", states)
                raise Stop("integrity", f"T_SEP={T} {name} replay disagrees")
        elif kind == "cg":
            a_s, a_f, beta = params["alpha_s"], params["alpha_f"], params["beta"]
            got = _call(
                clock,
                f"replay {name}",
                lambda a_s=a_s, a_f=a_f, beta=beta, name=name: cg_case(
                    world, T, CR, CS, a_s, a_f, beta, clock, name
                ),
            )
            snaps = _call(
                clock,
                f"occupancy {name}",
                lambda a_s=a_s, a_f=a_f, beta=beta, name=name: replay_cg_occupancy(
                    solver, T, CR, CS, a_s, a_f, beta, clock, name
                ),
            )
            from wrel.agents import cg_choose

            def cdist(content, y, a_s=a_s, a_f=a_f, beta=beta):
                return _det(cg_choose(content, read_class(y), CR, CS, a_s, a_f, beta))

            add_table(name, state_table(solver, ref_pol, T, snaps, lambda content: list(content), cdist))
            primary = next(c for c in held["controls"] if c["name"] == name)
            diff = _deciding_diff(
                primary,
                got,
                ("flags", "pattern", "t2_note", "donor_S", "donor_E", "donor_contrast", "interventions"),
            )
            replays[name] = {"agreed": not diff, "failures": diff}
            if diff:
                record["replays"] = replays
                _write(f"TSEP-{T}-states.json", states)
                raise Stop("integrity", f"T_SEP={T} {name} replay disagrees")
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

            add_table(name, state_table(solver, ref_pol, T, snaps, _content_mf, mdist))
            primary = next(c for c in held["controls"] if c["name"] == name)
            diff = _deciding_diff(
                primary,
                got,
                (
                    "flags",
                    "pattern",
                    "t2_note",
                    "t2_improvement",
                    "per_action_agent",
                    "per_action_baseline",
                    "donor_S",
                    "donor_E",
                    "donor_contrast",
                    "interventions",
                ),
            )
            replays[name] = {"agreed": not diff, "failures": diff}
            if diff:
                record["replays"] = replays
                _write(f"TSEP-{T}-states.json", states)
                raise Stop("integrity", f"T_SEP={T} {name} replay disagrees")

    pm_primary = next(c for c in held["controls"] if c["name"] == "PM-ACT")
    pm_replay = _call(
        clock,
        f"replay PM-ACT T={T}",
        lambda: pm_statistics_on_block(
            solver, ref_pol, held["machine"], held["block_second"], T, CR, CS, 0, "PM-ACT", clock
        ),
    )
    info_p = index_pm(held["machine"], held["block"], T, 0)
    info_r = index_pm(held["machine"], held["block_second"], T, 0)
    pub_p = _pm_public(
        pm_primary,
        donor_beliefs(solver, info_p, pm_primary.get("donor_S"), T),
        donor_beliefs(solver, info_p, pm_primary.get("donor_E"), T),
    )
    pub_r = _pm_public(
        pm_replay,
        donor_beliefs(solver, info_r, pm_replay.get("donor_S"), T),
        donor_beliefs(solver, info_r, pm_replay.get("donor_E"), T),
    )
    pdiff = _deciding_diff(pub_p, pub_r, tuple(pub_p.keys()))
    replays["PM-ACT"] = {"agreed": not pdiff, "failures": pdiff}
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
            return _det(P_ACT)
        ay = info["action"].get((t, cell))
        if ay is None:
            return _det(P_ACT)
        return _det(int(ay[y]))

    add_table("PM-ACT", state_table(solver, ref_pol, T, pm_joint, lambda content: {"t": content[0], "cell": content[1]}, pdist))
    if pdiff:
        record["replays"] = replays
        record["state_summary"] = {
            name: {k: states[name][k] for k in ("n_rows", "n_action_equal", "n_action_unequal", "n_transition_equal", "n_transition_unequal")}
            for name in states
        }
        _write(f"TSEP-{T}-states.json", states)
        raise Stop("integrity", f"T_SEP={T} PM-ACT replay disagrees")

    record["replays"] = replays
    record["state_summary"] = {
        name: {
            "n_rows": states[name]["n_rows"],
            "n_action_equal": states[name]["n_action_equal"],
            "n_action_unequal": states[name]["n_action_unequal"],
            "n_transition_equal": states[name]["n_transition_equal"],
            "n_transition_unequal": states[name]["n_transition_unequal"],
        }
        for name in states
    }
    _write(f"TSEP-{T}-states.json", {"T_SEP": T, "controls": states})
    record["verified"] = True
    record["status"] = "COMPLETE"
    record["formal_label"] = record["label_before_replay"]
    record["formal_note"] = record["label_before_replay_note"]
    record["clause"] = clause_of(record["formal_note"])
    _write(f"TSEP-{T}.json", record)
    return record


def run() -> dict:
    if len(sys.argv) != 1:
        raise SystemExit("this module takes no arguments")
    if (ROOT / "RESULTS_A3.md").exists() or any((OUT / name).exists() for name in OUTPUT_NAMES):
        raise SystemExit("refusing a second invocation; an Addendum A3 output already exists")
    clock = Clock()
    state = {
        "head": _head(),
        "cpu": None,
        "smoke": None,
        "smoke_invocations": 0,
        "pm": [],
        "settings": [],
        "blocks": [],
        "stop": None,
        "deviation": None,
        "hashes": {},
    }
    finalized = False
    try:
        cpu = _cpu_allowed()
        state["cpu"] = cpu
        if cpu != "0":
            raise Stop("integrity", f"Cpus_allowed_list is {cpu!r}")
        if COSTS[0] != (CR, CS):
            raise Stop("integrity", "study cost is not COSTS index 0")
        clock.begin("manifest", None, "none")
        _check_manifest(clock)
        state["blocks"].append(clock.stage_snapshot())
        clock.begin("smoke", SMOKE_LIMIT, "smoke")
        world = study_world()
        if world.eps[0] != F(23, 100) or world.eps[1] != F(23, 100) or not world.emissions_match:
            raise Stop("integrity", "frozen world identity failed")
        state["smoke_invocations"] = 1
        smoke = _call(clock, "smoke T=1", lambda: run_smoke(world, clock))
        smoke["clock"] = clock.stage_snapshot()
        state["smoke"] = smoke
        _write("smoke.json", smoke)
        print(f"smoke ok={smoke['ok']} wall={smoke['clock']['stage_wall_seconds_float']:.6f}", flush=True)
        if not smoke["ok"]:
            raise Stop("integrity", "T=1 smoke test disagreed with the stored case or its forward check")
        state["blocks"].append(clock.stage_snapshot())
        clock.begin("PM construction", BLOCK_LIMIT, "block")
        held = {}
        for horizon in SETTINGS:
            rec, obj = build_pm_horizon(world, horizon, clock)
            state["pm"].append(rec)
            _write("PM.json", {"horizons": state["pm"]})
            print(
                f"PM T={horizon} equal={rec['partition_equal']} well_defined={rec['well_defined']['ok']} "
                f"states={rec['counts']['n_states']}",
                flush=True,
            )
            if not rec["partition_equal"]:
                raise Stop("integrity", f"PM partitions differ at T_SEP={horizon}")
            held[horizon] = obj
        state["blocks"].append(clock.stage_snapshot())
        theta0 = conf_theta0()
        for horizon in SETTINGS:
            clock.begin(f"T_SEP={horizon} evaluation", BLOCK_LIMIT, "block")
            setting = evaluate_horizon(world, horizon, held[horizon], theta0, clock)
            setting["clock_evaluation"] = clock.stage_snapshot()
            state["settings"].append(setting)
            state["blocks"].append(clock.stage_snapshot())
            _write(f"TSEP-{horizon}.json", setting)
            print(
                f"T_SEP={horizon} primary label_before_replay={setting['label_before_replay']}",
                flush=True,
            )
            if not setting["reference_integrity_vs_A2"]["ok"]:
                raise Stop("integrity", f"T_SEP={horizon} reference primary disagrees with stored A2")
            if not setting.get("name_order_ok", False):
                raise Stop("integrity", f"T_SEP={horizon} control names left item8 order")
        clock.begin("independent verification", BLOCK_LIMIT, "block")
        for setting in state["settings"]:
            horizon = setting["T_SEP"]
            try:
                _verify_horizon(world, horizon, held[horizon], setting, theta0, clock)
            except (Cap, Stop):
                if setting.get("formal_label") is None and setting.get("label_before_replay") is not None:
                    failed = assemble_setting(
                        held[horizon]["primary_result"],
                        held[horizon]["controls"],
                        incomplete=True,
                        pm_undefined=held[horizon]["pm_bad"],
                    )
                    setting["formal_label"] = failed["label"]
                    setting["formal_note"] = failed["note"]
                    setting["clause"] = clause_of(failed["note"])
                    setting["status"] = "INTEGRITY-FAIL"
                    setting["verified"] = False
                    _write(f"TSEP-{horizon}.json", setting)
                raise
            print(
                f"T_SEP={horizon} formal={setting['formal_label']} clause={setting['clause']}",
                flush=True,
            )
        state["blocks"].append(clock.stage_snapshot())
    except (Cap, Stop) as exc:
        state["stop"] = {"kind": exc.kind, "where": exc.where}
        print(f"stop {exc.kind}: {exc.where}", flush=True)
    except Exception as exc:
        state["deviation"] = f"{exc.__class__.__name__}: {exc}"
        state["traceback"] = traceback.format_exc()
        print(state["traceback"], flush=True)
    finally:
        if not finalized:
            try:
                _finalize(state, clock)
                finalized = True
            except Exception as exc:
                print(f"finalize failed: {exc}", flush=True)
    return state


if __name__ == "__main__":
    outcome = run()
    if outcome.get("deviation"):
        raise SystemExit(1)
