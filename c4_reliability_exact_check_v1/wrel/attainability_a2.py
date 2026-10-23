"""Addendum A2 exploratory reference-attainability check.

One process. R-HAC-MB under H0 at (1/100, 3/50), T_SEP = 3 then 4.
Reuses the frozen solver, world, thresholds, donor rules, and procedures.
Does not modify an earlier file. Takes no arguments and does not retry.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
import traceback
from pathlib import Path

from wrel.labels import conjunction_of
from wrel.mb import H0Solver
from wrel.run_all import study_world
from wrel.sep import MU_REF, MU_RESL, MU_RESa, MU_RESc, MU_SELa, MU_SELc, MU_T2, RHO
from wrel.sep import _advance, assemble_setting, evaluate_mb_family, reference_met
from wrel.util import dump_json, pack, parse_R, read_hwm, read_rss, sha256_file
from wrel.verification_a1 import Index, _mb_advance, forward_mb, reference_case, solve_reference
from wrel.world import ACT_NAME, F, N_Y

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OUT = ROOT / "outputs" / "attainability_A2"
MANIFEST = ROOT / "ADDENDUM_A2_MANIFEST.md"
ITEM2 = ROOT / "outputs" / "ITEM-2.json"
CR = F(1, 100)
CS = F(3, 50)
SETTINGS = (3, 4)
SMOKE_LIMIT = 60.0
WALL_LIMIT = 30 * 60
RSS_LIMIT = 8 * 1024**3
OUTPUT_NAMES = ("smoke.json", "TSEP-3.json", "TSEP-4.json", "SUMMARY.json", "HASHES.txt", "RESULTS_A2.sha256")


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
        self.stage_peak = self.peak

    def begin(self, name: str, limit: float | None = None) -> None:
        self.stage = name
        self.stage_t0 = time.perf_counter()
        self.stage_limit = limit
        self.stage_peak = read_rss()
        self.check("begin")

    def check(self, where: str = "") -> None:
        rss = read_rss()
        if rss > self.peak:
            self.peak = rss
        if rss > self.stage_peak:
            self.stage_peak = rss
        if time.perf_counter() - self.t0 > WALL_LIMIT:
            raise Cap("wall", f"{self.stage}: {where}")
        if self.stage_limit is not None and time.perf_counter() - self.stage_t0 > self.stage_limit:
            raise Cap("smoke-wall", f"{self.stage}: {where}")
        if rss > RSS_LIMIT:
            raise Cap("memory", f"{self.stage}: {where} rss={rss}")

    def stage_snapshot(self) -> dict:
        return {
            "stage": self.stage,
            "stage_wall_seconds_float": time.perf_counter() - self.stage_t0,
            "cumulative_wall_seconds_float": time.perf_counter() - self.t0,
            "stage_peak_rss_bytes_sampled": self.stage_peak,
            "process_hwm_bytes": read_hwm(),
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
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(REPO), text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        return f"unavailable ({exc.__class__.__name__})"


def _check_manifest(clock: Clock) -> None:
    if not MANIFEST.exists():
        raise Stop("integrity", "ADDENDUM_A2_MANIFEST.md is missing")
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
        path = ROOT / rel
        got = sha256_file(str(path))
        if got != digest:
            raise Stop("integrity", f"hash mismatch {rel}")
        clock.check(f"hash {rel}")


def _write(name: str, obj: dict) -> None:
    dump_json(str(OUT / name), pack(obj))


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


def _rows_from_policy(counts_of, action_at, states: set, k: int, horizon_limit: int) -> list:
    rows = []
    for i in states:
        counts = list(counts_of(i))
        if sum(counts) > horizon_limit:
            raise Stop("integrity", f"action state at k={k} is outside the solved horizon")
        for y in range(N_Y):
            rows.append(
                {
                    "k": k,
                    "counts": counts,
                    "y": y,
                    "action": int(action_at(i, y)),
                    "action_name": ACT_NAME[int(action_at(i, y))],
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
    pk2 = pol[2]
    pk1 = pol[1]

    def at(table, i, y):
        return table[i * N_Y + y]

    rows = _rows_from_policy(lambda i: solver.idx.counts[i], lambda i, y: at(pk2, i, y), pert, 2, T - 2)
    rows.extend(_rows_from_policy(lambda i: solver.idx.counts[i], lambda i, y: at(pk1, i, y), repair, 1, T - 1))
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


def run_setting(world, T: int, clock: Clock) -> dict:
    solver = H0Solver(world, T)
    clock.check(f"primary index T={T}")
    solved = solver.solve_cost(CR, CS, budget=clock, myopic=False)
    clock.check(f"primary solved T={T}")
    primary = evaluate_mb_family(solver, solved["pol"], T, CR, CS, "R-HAC-MB")
    clock.check(f"primary criteria T={T}")
    primary_rows = _primary_table(solver, solved["pol"], primary, T)
    primary_entries = _entry_count(solver.idx.sum, solved["pol"], T, False)
    primary_public = _public_case(
        primary, solved["values"][T - 1], primary_entries, solved["invariant"], len(solver.idx.counts)
    )
    primary.pop("snaps", None)
    partial = {
        "T_SEP": T,
        "law": "H0",
        "agent": "R-HAC-MB",
        "cr": CR,
        "cs": CS,
        "status": "PRIMARY-ONLY",
        "primary": primary_public,
        "primary_action_table": primary_rows,
    }
    _write(f"TSEP-{T}.json", partial)
    idx = Index(world, T)
    clock.check(f"replay index T={T}")
    replay_pol, replay_values = solve_reference(world, idx, T, CR, CS, clock)
    clock.check(f"replay solved T={T}")
    replay = reference_case(world, idx, replay_pol, T, CR, CS)
    clock.check(f"replay criteria T={T}")
    replay_rows = _replay_table(world, idx, replay_pol, replay, T)
    clock.check(f"replay actions T={T}")
    replay_entries = _entry_count(idx.sum, replay_pol, T, True)
    replay_public = _public_case(
        replay, replay_values[T - 1], replay_entries, idx.invariant, len(idx.counts)
    )
    stat_diffs = _compare_cases(primary, replay)
    actions = _action_agreement(primary_rows, replay_rows)
    failures = list(stat_diffs)
    if primary_public["V"] != replay_public["V"]:
        failures.append("V")
    if primary_entries != replay_entries:
        failures.append("n_policy_entries")
    if primary_public["n_beliefs"] != replay_public["n_beliefs"]:
        failures.append("n_beliefs")
    if primary_public["invariant_decisions"] != replay_public["invariant_decisions"]:
        failures.append("invariant_decisions")
    if actions["n_disagree"] or actions["n_missing_in_replay"] or actions["n_missing_in_primary"]:
        failures.append("action_table")
    if not _shadow_ok(replay["interventions"]):
        failures.append("repair_equals_shadow")
    for donor_name in ("donor_S", "donor_E"):
        if not _donor_covered(primary_rows, primary[donor_name]) or not _donor_covered(
            replay_rows, replay[donor_name]
        ):
            failures.append(f"{donor_name}_in_action_table")
    agreed = not failures
    assembled = assemble_setting(primary, [], incomplete=not agreed, pm_undefined=False)
    record = {
        "T_SEP": T,
        "law": "H0",
        "agent": "R-HAC-MB",
        "cr": CR,
        "cs": CS,
        "status": "COMPLETE" if agreed else "INTEGRITY-FAIL",
        "agreed": agreed,
        "failures": failures,
        "formal_label": assembled["label"],
        "formal_note": assembled["note"],
        "reference_met": reference_met(primary["flags"]),
        "reference_conjunction": conjunction_of(primary["flags"]),
        "primary": primary_public,
        "replay": replay_public,
        "primary_action_table": primary_rows,
        "replay_action_table": replay_rows,
        "action_agreement": actions,
        "controls_evaluated": [],
        "pm_evaluated": False,
    }
    _write(f"TSEP-{T}.json", record)
    return record


def _fmt(value) -> str:
    if isinstance(value, F):
        return f"{value.numerator}/{value.denominator}"
    if value is None:
        return "—"
    return str(value)


def _mode_line(block, key: str) -> str:
    if not isinstance(block, dict):
        return "—"
    return _fmt(block.get(key))


def _results_text(state: dict) -> str:
    lines = [
        "# RESULTS A2",
        "",
        "Exploratory W-REL reference-attainability check under Addendum A2. Earlier results are unchanged. This file is additive.",
        "",
        "Binding approval: `c4_reliability_APPROVAL_ADDENDUM_A2.md`, sha256 `09c336d4569ec6771c88d97bee424510fab0cd6b5403b24accee1f813fb8b835`, recorded 2026-10-21, 12:19 PM ET. The frozen procedure is `c4_reliability_exact_check_spec_ADDENDUM_A2.md`.",
        "",
        f"Code commit at process start: `{state['head']}`.",
        "",
        "Only R-HAC-MB under H0 at `(c_R, c_S) = (1/100, 3/50)` is evaluated, at `T_SEP = 3` and `T_SEP = 4`. The formal label is the return value of frozen `decide_setting`, called with this reference, an empty control list, and `pm_undefined` false. Eligible named controls and PM-ACT are outside this approval and were not evaluated. This file does not add a label.",
        "",
        "No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested.",
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
                "One invocation: frozen `H0Solver` at T = 1, non-myopic, then `forward` under both regimes.",
                "",
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
    lines.extend(["## Settings", ""])
    if not state["settings"]:
        lines.append("No T_SEP setting was evaluated.")
        lines.append("")
    for setting in state["settings"]:
        flags = setting["primary"]["flags"]
        pattern = setting["primary"]["pattern"]
        lines.extend(
            [
                f"### T_SEP = {setting['T_SEP']}",
                "",
                f"Formal label: **{setting['formal_label']}**.",
                "",
                f"Note: {setting['formal_note']}",
                "",
                f"Reference conjunction (`conjunction_of`): `{setting['reference_conjunction']}`. `reference_met`: `{setting['reference_met']}`.",
                "",
                "| Criterion | Value |",
                "| --- | --- |",
                f"| C-REF | {flags['C-REF']} |",
                f"| C-T2 | {flags['C-T2']} |",
                f"| C-SEL | {flags['C-SEL']} |",
                f"| C-FO | {flags['C-FO']} |",
                f"| rescue | {flags['rescue']} |",
                "",
                f"Status: `{setting['status']}`. Replay and primary agreement: `{setting['agreed']}`.",
                "",
                "#### Deciding statistics",
                "",
                f"- Δ_R = `{_fmt(pattern['delta_R'])}`",
                f"- Δ_M = `{_fmt(pattern['delta_M'])}`",
                f"- E_err(agent) = `{_fmt(pattern['E_err_agent'])}`",
                f"- E_err(baseline) = `{_fmt(pattern['E_err_baseline'])}`",
                f"- C-T2 improvement = `{_fmt(setting['primary']['t2_improvement'])}`",
                f"- C-T2 note = `{setting['primary']['t2_note']}`",
                f"- D_e SWAP-S = `{_fmt(pattern['D_e_S'])}`; D_q SWAP-S = `{_fmt(pattern['D_q_S'])}`",
                f"- D_e SWAP-E = `{_fmt(pattern['D_e_E'])}`; D_q SWAP-E = `{_fmt(pattern['D_q_E'])}`",
                f"- C-FO (a) equal = `{pattern['cfo_a']}`; C-FO (b) equal = `{pattern['cfo_b']}`",
                f"- donor contrast = `{setting['primary']['donor_contrast']}`",
                f"- S-donor counts = `{setting['primary']['donor_S']}`",
                f"- E-donor counts = `{setting['primary']['donor_E']}`",
                f"- empty-belief value = `{_fmt(setting['primary']['V'])}`",
                "",
                "#### Intervention, suspension-control, and rescue components",
                "",
                "| Direction | Mode | D_e | D_q | eA | eB | qA | qB | LA | LB | repair equals shadow |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        interventions = setting["primary"]["interventions"]
        for direction in ("S", "E"):
            modes = None if interventions is None else interventions.get(direction)
            for mode in ("SWAP", "CORRUPT", "SUSPEND"):
                block = None if not isinstance(modes, dict) else modes.get(mode)
                lines.append(
                    "| {direction} | {mode} | {de} | {dq} | {ea} | {eb} | {qa} | {qb} | {la} | {lb} | {shadow} |".format(
                        direction=direction,
                        mode=mode,
                        de=_mode_line(block, "D_e"),
                        dq=_mode_line(block, "D_q"),
                        ea=_mode_line(block, "eA"),
                        eb=_mode_line(block, "eB"),
                        qa=_mode_line(block, "qA"),
                        qb=_mode_line(block, "qB"),
                        la=_mode_line(block, "LA"),
                        lb=_mode_line(block, "LB"),
                        shadow=_mode_line(block, "repair_equals_shadow"),
                    )
                )
        agreement = setting["action_agreement"]
        lines.extend(
            [
                "",
                "#### Replay agreement",
                "",
                f"- Statistic differences: {', '.join(setting['failures']) if setting['failures'] else 'none'}",
                f"- Action rows compared equal: {agreement['n_agree']}",
                f"- Action disagreements: {agreement['n_disagree']}",
                f"- Keys only in the primary table: {agreement['n_missing_in_replay']}",
                f"- Keys only in the replay table: {agreement['n_missing_in_primary']}",
                f"- Primary action-table sha256: `{agreement['primary_sha256']}`",
                f"- Replay action-table sha256: `{agreement['replay_sha256']}`",
                f"- Policy entries: {setting['primary']['n_policy_entries']}",
                "",
                "The per-state action tables are stored in `outputs/attainability_A2/"
                f"TSEP-{setting['T_SEP']}.json`.",
                "",
                f"- Stage wall: {setting['clock']['stage_wall_seconds_float']} seconds",
                f"- Stage sampled peak RSS: {setting['clock']['stage_peak_rss_bytes_sampled']} bytes",
                f"- Process high-water mark at stage end: {setting['clock']['process_hwm_bytes']} bytes",
                "",
            ]
        )
    lines.extend(["## Compute", ""])
    clock = state.get("clock") or {}
    lines.extend(
        [
            "Command, from `c4_reliability_exact_check_v1`:",
            "",
            "```text",
            "taskset -c 0 python3 -u -m wrel.attainability_a2",
            "```",
            "",
            f"- Cumulative wall: {clock.get('cumulative_wall_seconds_float')} seconds",
            f"- Sampled peak RSS: {clock.get('peak_rss_bytes_sampled')} bytes",
            f"- Process high-water mark: {clock.get('process_hwm_bytes')} bytes",
            "- Limits: one CPU process, 30 cumulative minutes, 8 GB resident memory, no GPU.",
            "- Smoke-test stage limit: 60 seconds. Invocations used: "
            f"{state.get('smoke_invocations', 0)}.",
            "",
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
        lines.append(
            f"Approved stop: kind `{state['stop']['kind']}`, where `{state['stop']['where']}`."
        )
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
            "The sha256 of this file is `outputs/attainability_A2/RESULTS_A2.sha256`. It is computed after this file is written.",
            "",
        ]
    )
    return "\n".join(lines)


def _hash_outputs() -> dict:
    hashes = {}
    for name in ("smoke.json", "TSEP-3.json", "TSEP-4.json", "SUMMARY.json"):
        path = OUT / name
        if path.exists():
            hashes[f"outputs/attainability_A2/{name}"] = sha256_file(str(path))
    return hashes


def _write_hashes(hashes: dict) -> None:
    body = "".join(f"SHA256 {name} {digest}\n" for name, digest in hashes.items())
    path = OUT / "HASHES.txt"
    path.write_text(body, encoding="utf-8")
    hashes["outputs/attainability_A2/HASHES.txt"] = sha256_file(str(path))


def _finalize(state: dict, clock: Clock) -> None:
    state["clock"] = clock.snapshot()
    summary = {
        "approval_sha256": "09c336d4569ec6771c88d97bee424510fab0cd6b5403b24accee1f813fb8b835",
        "head": state["head"],
        "cpu_allowed": state.get("cpu"),
        "smoke_ok": None if state.get("smoke") is None else state["smoke"]["ok"],
        "settings": [
            {
                "T_SEP": item["T_SEP"],
                "status": item["status"],
                "formal_label": item["formal_label"],
                "formal_note": item["formal_note"],
                "reference_conjunction": item["reference_conjunction"],
                "reference_met": item["reference_met"],
                "flags": item["primary"]["flags"],
                "agreed": item["agreed"],
                "failures": item["failures"],
                "n_action_agree": item["action_agreement"]["n_agree"],
                "n_action_disagree": item["action_agreement"]["n_disagree"],
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
    results_path = ROOT / "RESULTS_A2.md"
    results_path.write_text(_results_text(state), encoding="utf-8")
    digest = sha256_file(str(results_path))
    (OUT / "RESULTS_A2.sha256").write_text(f"{digest}  RESULTS_A2.md\n", encoding="utf-8")
    state["results_sha256"] = digest


def run() -> dict:
    if len(sys.argv) != 1:
        raise SystemExit("this module takes no arguments")
    if any((OUT / name).exists() for name in OUTPUT_NAMES):
        raise SystemExit("refusing a second invocation; an Addendum A2 output already exists")
    clock = Clock()
    state = {
        "head": _head(),
        "cpu": None,
        "smoke": None,
        "smoke_invocations": 0,
        "settings": [],
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
        _check_manifest(clock)
        clock.begin("smoke", SMOKE_LIMIT)
        world = study_world()
        if world.eps[0] != F(23, 100) or world.eps[1] != F(23, 100) or not world.emissions_match:
            raise Stop("integrity", "frozen world identity failed")
        state["smoke_invocations"] = 1
        smoke = run_smoke(world, clock)
        smoke["clock"] = clock.stage_snapshot()
        state["smoke"] = smoke
        _write("smoke.json", smoke)
        print(
            f"smoke ok={smoke['ok']} wall={smoke['clock']['stage_wall_seconds_float']:.6f}",
            flush=True,
        )
        if not smoke["ok"]:
            raise Stop("integrity", "T=1 smoke test disagreed with the stored case or its forward check")
        for horizon in SETTINGS:
            clock.begin(f"T_SEP={horizon}")
            setting = run_setting(world, horizon, clock)
            setting["clock"] = clock.stage_snapshot()
            _write(f"TSEP-{horizon}.json", setting)
            state["settings"].append(setting)
            print(
                f"T_SEP={horizon} label={setting['formal_label']} agreed={setting['agreed']} "
                f"wall={setting['clock']['stage_wall_seconds_float']:.6f}",
                flush=True,
            )
            if not setting["agreed"]:
                raise Stop("integrity", f"T_SEP={horizon} primary and replay disagree")
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
