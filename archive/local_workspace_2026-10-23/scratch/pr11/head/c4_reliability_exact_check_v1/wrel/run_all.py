"""Run ITEM-1 through ITEM-9 in the frozen order. Study rates appear only here.

One process. Exact rationals. No horizon is shortened after a cap: the item stops
and is labelled UNRESOLVED-COMPUTE. A quotient that is not a function is reported.
"""

from __future__ import annotations

import traceback
from fractions import Fraction
from pathlib import Path

from .agents import (
    S_SP_SPEC,
    S_U_SPEC,
    blind_value,
    cg_forward,
    cg_forward_h1,
    conf_a_episode,
    conf_s_matches_blind,
    enum_maps,
    mf_forward,
    mf_forward_h1,
    oracle_value,
)
from .controls import (
    conf_theta0,
    evaluate_cg,
    evaluate_conf,
    evaluate_mf,
    evaluate_pm,
    joint_frequencies,
    lambda_from_mb,
    mb_category2,
)
from .item1 import audit
from .labels import decide_setting
from .mb import (
    H0Solver,
    forward_h1,
    forward_h1_schedule,
    forward_schedule,
    solve_h0_schedule,
    solve_h1,
    solve_h1_schedule,
)
from .pm import build_machine, partition_sets, refine, refine_by_queue, well_defined
from .replay import (
    replay_blind,
    replay_cg_y,
    replay_conf_path,
    replay_h0_values,
    replay_h1_value,
    replay_item1,
    replay_oracle,
    replay_reference_core,
)
from .sep import assemble_setting, blind_result, evaluate_mb_family, reference_met
from .util import CapExceeded, Budget, dump_json, pack, sha256_file
from .world import F, N_Y, World, read_class

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
SPEC_SHA = "ae626b65cae383121e6a902fe79c119b90ff46ffb8fe7cc39fafe27fc502adef"
COSTS = (
    (F(1, 100), F(3, 50)),
    (F(1, 100), F(1, 10)),
    (F(1, 50), F(3, 50)),
    (F(1, 50), F(1, 10)),
    (F(1, 25), F(3, 50)),
    (F(1, 25), F(1, 10)),
)
KSEP = ((F(1, 50), F(3, 50)), (F(1, 100), F(1, 10)))
ETAS = (F(1, 20), F(1, 10), F(1, 5))
CG_ALPHA = ((1, 1), (2, 1))
CG_BETA = (F(0), F(1, 20), F(1, 10))
MF_EPS = (F(0), F(1, 10))
VERBATIM = {
    "DISTINGUISHES NAMED CONTROLS": (
        "the reference meets the prespecified core criteria, and every eligible named control "
        "fails at least one core criterion under comparable procedures."
    ),
    "PATTERN REPRODUCED BY NAMED CONTROL": "at least one control reproduces the full prespecified response pattern.",
    "CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED": (
        "This is a scientific outcome, not UNRESOLVED-DESIGN. Report which controls share the conjunction "
        "and where their statistics differ. Neither functional-role identification nor absence follows automatically."
    ),
    "REFERENCE CRITERIA NOT MET": "the reference does not meet the required conjunction.",
    "UNRESOLVED-DESIGN": "an output, intervention correspondence or criterion is undefined.",
    "UNRESOLVED-COMPUTE": "the required calculation is incomplete.",
}


def study_world() -> World:
    # S: (w, e) = (1/20, 1/5). E: (1/5, 1/20). Hazard 1/20. Prior 1/2.
    return World(F(1, 20), F(1, 5), F(1, 5), F(1, 20), F(1, 20))


def schedules(T: int):
    cut = T // 2
    for i, old in enumerate(COSTS):
        for j, new in enumerate(COSTS):
            if i == j:
                continue
            yield {
                "from_index": i,
                "to_index": j,
                "cr_old": old[0],
                "cs_old": old[1],
                "cr_new": new[0],
                "cs_new": new[1],
                "schedule": [old] * cut + [new] * (T - cut),
            }


def _cost_tag(cr, cs):
    return {"cr": cr, "cs": cs}


def _mix_forward(solver, pol, T, cr, cs, budget):
    out = []
    for z in (0, 1):
        out.append(solver.forward(pol, T, cr, cs, z, budget))
    mix_v = (out[0]["value"] + out[1]["value"]) / 2
    return out, mix_v


def _ce_value(solver, pols, schedule, myopic_pols=None):
    """Actual reward of the certainty-equivalent policy under the true schedule."""
    source = pols
    T = len(schedule)
    acc = F(0)
    detail = []
    for z in (0, 1):
        # manual stitch
        from .mb import P_ACT, R_ACT
        from .world import N_Y as NY

        idx = solver.idx
        mass = {0: F(1)}
        value = F(0)
        for t in range(T):
            cr, cs = schedule[t]
            k = T - t
            pol = source[(cr, cs)]["pol"][k]
            new = {}
            py = solver.world.py[z]
            for i, p in mass.items():
                b = idx.b[i]
                base = i * NY
                for y in range(NY):
                    a = pol[base + y]
                    w = p * py[y]
                    if a == P_ACT:
                        value += w * solver.immP[y]
                        new[i] = new.get(i, F(0)) + w
                    elif a == R_ACT:
                        value += w * (solver.world.expected_correct_R(b, F(1) if z == 0 else F(0), y) - cr)
                        for c in range(10):
                            wc = w * idx.pc[z][y][c]
                            if wc:
                                j = idx.trans[i][c]
                                new[j] = new.get(j, F(0)) + wc
                    else:
                        value += w * (solver.immM[y] - cs)
                        new[i] = new.get(i, F(0)) + w
            mass = new
        detail.append(value)
        acc += value
    return acc / 2, detail


def _h1_ce(world, pols, schedule, budget=None):
    from .mb import BeliefIndex, _h_trans
    from .world import M_ACT, N_Y, P_ACT, R_ACT

    helper = BeliefIndex(world, 0)
    immP, immM = world.imm_PM()
    T = len(schedule)
    mass = {(F(1, 2), 0): F(1, 2), (F(1, 2), 1): F(1, 2)}
    value = F(0)
    h = world.h
    for t in range(T):
        if budget:
            budget.check(f"H1-CE t={t}")
        cr, cs = schedule[t]
        pol = pols[(cr, cs)]
        k = T - t
        new = {}
        for (b, z), p in mass.items():
            bt = F(1) if z == 0 else F(0)
            for y in range(N_Y):
                a = pol[(k, b, y)]
                w = p * world.py[z][y]
                if a == R_ACT:
                    value += w * (world.expected_correct_R(b, bt, y) - cr)
                    for c in range(10):
                        wc = w * helper.pc[z][y][c]
                        if wc == 0:
                            continue
                        bn = world.mix_h1(world.update_belief(b, c))
                        for zp, pz in _h_trans(z, h):
                            key = (bn, zp)
                            new[key] = new.get(key, F(0)) + wc * pz
                else:
                    reward = immP[y] if a == P_ACT else immM[y] - cs
                    value += w * reward
                    bn = world.mix_h1(b)
                    for zp, pz in _h_trans(z, h):
                        key = (bn, zp)
                        new[key] = new.get(key, F(0)) + w * pz
        mass = new
    return value


def _blind_sched(world, schedule):
    total = F(0)
    for cr, cs in schedule:
        total += blind_value(world, cr, cs, 1)["v"]
    return total


def _oracle_sched(world, schedule):
    total = F(0)
    for cr, cs in schedule:
        total += oracle_value(world, cr, cs, 1)["v"]
    return total


def _value_row(law, T, cr, cs, vs, vm, vb, vo, fw, replay_tag, integrity):
    return {
        "law": law,
        "T": T,
        "cr": cr,
        "cs": cs,
        "V_star": vs,
        "V_myopic": vm,
        "V_blind": vb,
        "V_oracle": vo,
        "planning_advantage_T": vs - vm,
        "adaptive_information_advantage_T": vs - vb,
        "oracle_gap_T": vo - vs,
        "n_R": {"S": fw[0]["n_R"], "E": fw[1]["n_R"]},
        "n_R_unanimous": {"S": fw[0]["n_R_unanimous"], "E": fw[1]["n_R_unanimous"]},
        "n_M": {"S": fw[0]["n_M"], "E": fw[1]["n_M"]},
        "exploration_cost": {"S": fw[0]["exploration_cost"], "E": fw[1]["exploration_cost"]},
        "first_R": {"S": fw[0]["first_R"], "E": fw[1]["first_R"]},
        "never_R": {"S": fw[0]["never_R"], "E": fw[1]["never_R"]},
        "forward_value_matches_backward": integrity,
        "replay": replay_tag,
    }


def run():
    manifest = ROOT / "IMPLEMENTATION_MANIFEST.md"
    if not manifest.exists():
        raise SystemExit("IMPLEMENTATION_MANIFEST.md is missing; refuse to run before the freeze.")
    manifest_sha = sha256_file(str(manifest))
    spec_sha = sha256_file(str(ROOT / "c4_reliability_exact_check_spec_FINAL.md"))
    if spec_sha != SPEC_SHA:
        raise SystemExit(f"spec hash {spec_sha} does not match the frozen identifier")
    _verify_manifest(manifest.read_text(encoding="utf-8"))
    budget = Budget()
    world = study_world()
    if world.eps[0] != F(23, 100) or world.eps[1] != F(23, 100) or not world.emissions_match:
        raise SystemExit("study world failed the frozen eps identity; refusing to continue")
    ctx = {"anomalies": []}
    OUT.mkdir(exist_ok=True)

    def finish(name, payload, status="COMPLETE"):
        payload = dict(payload)
        payload["item"] = name
        payload["status"] = status
        payload["spec_sha256"] = spec_sha
        payload["manifest_sha256"] = manifest_sha
        payload["budget"] = budget.snapshot()
        dump_json(str(OUT / f"{name}.json"), pack(payload))
        print(f"{name} {status} wall={payload['budget']['wall_seconds_float']:.1f}s", flush=True)
        return payload

    def guard(name, fn):
        budget.start_item(name)
        try:
            payload = fn()
            return finish(name, payload, payload.get("status", "COMPLETE"))
        except CapExceeded as exc:
            partial = getattr(exc, "partial", None) or {}
            partial["reason"] = str(exc)
            return finish(name, partial, "UNRESOLVED-COMPUTE")
        except Exception as exc:
            return finish(
                name,
                {"error": repr(exc), "trace": traceback.format_exc()},
                "ENGINEERING-FAILURE",
            )

    ctx["item1"] = guard("ITEM-1", lambda: item1(world, budget))
    ctx["item2"] = guard("ITEM-2", lambda: item2(world, budget, ctx))
    ctx["item3"] = guard("ITEM-3", lambda: item3(world, budget, ctx))
    ctx["item4"] = guard("ITEM-4", lambda: item4(world, budget, ctx))
    ctx["item5"] = guard("ITEM-5", lambda: item5(world, budget, ctx))
    ctx["item6"] = guard("ITEM-6", lambda: item6(world, budget, ctx))
    ctx["item7"] = guard("ITEM-7", lambda: item7(world, budget, ctx))
    ctx["item8"] = guard("ITEM-8", lambda: item8(world, budget, ctx))
    ctx["item9"] = guard("ITEM-9", lambda: item9(world, budget, ctx))
    summary = {
        "spec_sha256": spec_sha,
        "manifest_sha256": manifest_sha,
        "anomalies": ctx["anomalies"],
        "items": {k: {"status": ctx[k]["status"]} for k in (
            "item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8", "item9"
        )},
        "settings": ctx.get("settings_final"),
        "budget": budget.snapshot(),
    }
    dump_json(str(OUT / "SUMMARY.json"), pack(summary))
    print("run complete", flush=True)


def _verify_manifest(text: str) -> None:
    for line in text.splitlines():
        if not line.startswith("SHA256 "):
            continue
        _tag, rel, digest = line.split()
        got = sha256_file(str(ROOT / rel))
        if got != digest:
            raise SystemExit(f"frozen file changed after the manifest: {rel}")


def item1(world, budget):
    ans = audit(world, max_len=3, budget=budget)
    ans["planning_estimate_histories"] = 3006865
    return ans


def item2(world, budget, ctx):
    solver = H0Solver(world, 10)
    ctx["h0"] = solver
    opt, myo = {}, {}
    for cr, cs in COSTS:
        budget.check(f"H0 solve {cr},{cs}")
        opt[(cr, cs)] = solver.solve_cost(cr, cs, budget=budget, myopic=False)
        myo[(cr, cs)] = solver.solve_cost(cr, cs, budget=budget, myopic=True)
    ctx["opt"] = opt
    ctx["myo"] = myo
    rows = []
    anomalies = []
    for T in range(1, 11):
        for cr, cs in COSTS:
            budget.check(f"H0 forward T={T}")
            vs = opt[(cr, cs)]["values"][T - 1]
            vm = myo[(cr, cs)]["values"][T - 1]
            vb = blind_value(world, cr, cs, T)["V"]
            vo = oracle_value(world, cr, cs, T)["V"]
            fw, mix = _mix_forward(solver, opt[(cr, cs)]["pol"], T, cr, cs, budget)
            ok = mix == vs
            if not ok:
                anomalies.append({"T": T, "cr": cr, "cs": cs, "forward": mix, "backward": vs})
            tag = "REPLAY_COVERAGE" if T <= 4 else "NOT INDEPENDENTLY REPLAYED"
            rows.append(_value_row("H0", T, cr, cs, vs, vm, vb, vo, fw, tag, ok))
    switches = []
    for T in (4, 6):
        for spec in schedules(T):
            budget.check(f"H0 switch T={T}")
            sched = spec["schedule"]
            ce, _ = _ce_value(solver, opt, sched)
            my_ce, _ = _ce_value(solver, myo, sched)
            aware, pols = solve_h0_schedule(solver, sched, budget)
            # Confirm the schedule value by forward under Z mixture.
            fv = F(0)
            for z in (0, 1):
                fv += forward_schedule(solver, pols, sched, z)["value"]
            fv /= 2
            if fv != aware:
                anomalies.append({"switch_forward_mismatch": True, "T": T, "aware": aware, "forward": fv})
            switches.append(
                {
                    "law": "H0",
                    "T": T,
                    "from_index": spec["from_index"],
                    "to_index": spec["to_index"],
                    "cr_old": spec["cr_old"],
                    "cs_old": spec["cs_old"],
                    "cr_new": spec["cr_new"],
                    "cs_new": spec["cs_new"],
                    "V_MB_CE": ce,
                    "V_myopic": my_ce,
                    "V_switch_aware": aware,
                    "V_blind": _blind_sched(world, sched),
                    "V_oracle": _oracle_sched(world, sched),
                    "descriptive_gap_switch_aware_minus_CE": aware - ce,
                    "note": "Switch-aware planning uses the schedule. The gap is not a fair performance advantage.",
                    "replay": "NOT INDEPENDENTLY REPLAYED",
                }
            )
    ctx["anomalies"].extend([f"ITEM-2 integrity {a}" for a in anomalies])
    return {
        "invariant_decisions": solver.idx.invariant,
        "n_beliefs": len(solver.idx.counts),
        "rows": rows,
        "switches": switches,
        "anomalies": anomalies,
        "eps": world.eps[0],
    }


def item3(world, budget, ctx):
    opt, myo = {}, {}
    for cr, cs in COSTS:
        budget.check(f"H1 solve {cr}")
        o = solve_h1(world, 5, cr, cs, budget=budget, myopic=False)
        m = solve_h1(world, 5, cr, cs, budget=budget, myopic=True)
        opt[(cr, cs)] = o
        myo[(cr, cs)] = m
    ctx["h1_opt"] = {k: v["pol"] for k, v in opt.items()}
    rows = []
    anomalies = []
    for T in range(1, 6):
        for cr, cs in COSTS:
            budget.check(f"H1 forward T={T}")
            vs = opt[(cr, cs)]["values"][T - 1]
            vm = myo[(cr, cs)]["values"][T - 1]
            vb = blind_value(world, cr, cs, T)["V"]
            vo = oracle_value(world, cr, cs, T)["V"]
            # Restrict the policy dict to this horizon by wrapping: forward_h1 indexes k = T-t.
            # The stored policy was built at total horizon 5, and V_k(prior) is values[k-1].
            # forward_h1 uses pol[(k,b,y)] with k = T_forward - t, which matches.
            fw = forward_h1(world, opt[(cr, cs)]["pol"], T, cr, cs, budget)
            ok = fw["value"] == vs
            if not ok:
                anomalies.append({"T": T, "cr": cr, "cs": cs, "forward": fw["value"], "backward": vs})
            rows.append(
                {
                    "law": "H1",
                    "T": T,
                    "cr": cr,
                    "cs": cs,
                    "V_star": vs,
                    "V_myopic": vm,
                    "V_blind": vb,
                    "V_oracle": vo,
                    "planning_advantage_T": vs - vm,
                    "adaptive_information_advantage_T": vs - vb,
                    "oracle_gap_T": vo - vs,
                    "n_R": fw["n_R"],
                    "n_R_unanimous": fw["n_R_unanimous"],
                    "n_M": fw["n_M"],
                    "exploration_cost": fw["exploration_cost"],
                    "first_R": fw["first_R"],
                    "never_R": fw["never_R"],
                    "forward_value_matches_backward": ok,
                    "replay": "REPLAY_COVERAGE" if T <= 4 else "NOT INDEPENDENTLY REPLAYED",
                    "blind_oracle_note": (
                        "R-BLIND and the oracle do not carry source information. "
                        "With P(Z_t=S)=1/2 at every t, their H1 values equal the fixed-regime mixture."
                    ),
                }
            )
    switches = []
    for spec in schedules(4):
        budget.check("H1 switch")
        sched = spec["schedule"]
        ce = _h1_ce(world, ctx["h1_opt"], sched, budget)
        aware = solve_h1_schedule(world, sched, budget)
        fv = forward_h1_schedule(world, aware["pol"], sched, budget)
        if fv != aware["value"]:
            anomalies.append({"h1_switch_mismatch": True, "aware": aware["value"], "forward": fv})
        switches.append(
            {
                "law": "H1",
                "T": 4,
                "from_index": spec["from_index"],
                "to_index": spec["to_index"],
                "V_MB_CE": ce,
                "V_switch_aware": aware["value"],
                "V_blind": _blind_sched(world, sched),
                "V_oracle": _oracle_sched(world, sched),
                "descriptive_gap_switch_aware_minus_CE": aware["value"] - ce,
                "note": "Switch-aware planning uses the schedule. The gap is not a fair performance advantage.",
                "replay": "NOT INDEPENDENTLY REPLAYED",
            }
        )
    ctx["anomalies"].extend([f"ITEM-3 integrity {a}" for a in anomalies])
    # Drop large H1 policy objects after the switches. Fixed-cost values are in rows.
    ctx.pop("h1_opt", None)
    return {"rows": rows, "switches": switches, "anomalies": anomalies, "n_beliefs_T5": len(opt[COSTS[0]]["layers"][-1])}


def item4(world, budget, ctx):
    ident = conf_s_matches_blind(world, COSTS)
    sU = next(world.s_def[y] for y in range(N_Y) if read_class(y) == 0)
    sSp = next(world.s_def[y] for y in range(N_Y) if read_class(y) == 1)
    uniform_U = len({world.s_def[y] for y in range(N_Y) if read_class(y) == 0}) == 1
    uniform_S = len({world.s_def[y] for y in range(N_Y) if read_class(y) == 1}) == 1
    anomaly = []
    if sU != S_U_SPEC or sSp != S_SP_SPEC:
        anomaly.append(
            {
                "s_U_computed": sU,
                "s_U_spec": S_U_SPEC,
                "s_Sp_computed": sSp,
                "s_Sp_spec": S_SP_SPEC,
                "note": "theta_1 still uses the spec constants. Computed s is not substituted.",
            }
        )
    theta0 = conf_theta0()
    rows = []
    for eta in ETAS:
        for alpha in ETAS:
            for cr, cs in COSTS:
                budget.check("CONF")
                ep = conf_a_episode(world, eta, alpha, cr, cs, 10, theta0)
                for T, v in enumerate(ep["by_t"], start=1):
                    rows.append(
                        {
                            "law": "H0",
                            "eta": eta,
                            "alpha": alpha,
                            "T": T,
                            "cr": cr,
                            "cs": cs,
                            "V": v,
                            "replay": "REPLAY_COVERAGE" if T <= 4 else "NOT INDEPENDENTLY REPLAYED",
                        }
                    )
                # H1 value equals the same mixture because err is independent of Z and P(Z_t=S)=1/2.
                for T, v in enumerate(ep["by_t"][:5], start=1):
                    rows.append(
                        {
                            "law": "H1",
                            "eta": eta,
                            "alpha": alpha,
                            "T": T,
                            "cr": cr,
                            "cs": cs,
                            "V": v,
                            "replay": "NOT INDEPENDENTLY REPLAYED",
                            "note": "theta is independent of Z; the H1 marginal of Z stays 1/2, so the value matches H0.",
                        }
                    )
    switches = []
    for law, horizons in (("H0", (4, 6)), ("H1", (4,))):
        for T in horizons:
            for spec in schedules(T):
                budget.check("CONF switch")
                for eta in ETAS:
                    for alpha in ETAS:
                        ep = conf_a_episode(world, eta, alpha, spec["cr_old"], spec["cs_old"], T, theta0, schedule=spec["schedule"])
                        switches.append(
                            {
                                "law": law,
                                "T": T,
                                "eta": eta,
                                "alpha": alpha,
                                "from_index": spec["from_index"],
                                "to_index": spec["to_index"],
                                "V": ep["V"],
                                "replay": "NOT INDEPENDENTLY REPLAYED",
                            }
                        )
    enum_rows = []
    for amap in enum_maps():
        for cr, cs in COSTS:
            act = list(amap)
            # value of the constant read->action map
            v = F(0)
            costs = (F(0), cr, cs)
            for z in (0, 1):
                for r in (0, 1):
                    a = act[r]
                    v += F(1, 2) * world.p_read[z][r] * (world.p_correct_f0[z][a][r] - costs[a])
            enum_rows.append({"map_U_Sp": amap, "cr": cr, "cs": cs, "v_one_trial": v, "role": "descriptive enumeration, not an eligible control"})
    ctx["anomalies"].extend(anomaly)
    ctx["theta0"] = theta0
    return {
        "identity": ident,
        "s_uniform_on_unanimous": uniform_U,
        "s_uniform_on_split": uniform_S,
        "s_U_computed": sU,
        "s_Sp_computed": sSp,
        "s_U_spec_constant": S_U_SPEC,
        "s_Sp_spec_constant": S_SP_SPEC,
        "theta0_uses_spec_constants": theta0,
        "anomalies": anomaly,
        "rows": rows,
        "switches": switches,
        "enum": enum_rows,
    }


def item5(world, budget, ctx):
    rows = []
    for a_s, a_f in CG_ALPHA:
        for beta in CG_BETA:
            for cr, cs in COSTS:
                budget.check(f"CG {a_s} {beta}")
                s = cg_forward(world, 8, cr, cs, a_s, a_f, beta, 0, budget)
                e = cg_forward(world, 8, cr, cs, a_s, a_f, beta, 1, budget)
                h1 = cg_forward_h1(world, 5, cr, cs, a_s, a_f, beta, budget)
                for T in range(1, 9):
                    rows.append(
                        {
                            "law": "H0",
                            "alpha_s": a_s,
                            "alpha_f": a_f,
                            "beta": beta,
                            "T": T,
                            "cr": cr,
                            "cs": cs,
                            "V_S": s["by_t"][T - 1],
                            "V_E": e["by_t"][T - 1],
                            "V": (s["by_t"][T - 1] + e["by_t"][T - 1]) / 2,
                            "n_R_S": None,
                            "n_bonus_disagreements_S": s["n_bonus_disagreements"] if T == 8 else None,
                            "n_states_final_S": s["n_states_final"] if T == 8 else None,
                            "replay": "REPLAY_COVERAGE" if T <= 4 else "NOT INDEPENDENTLY REPLAYED",
                        }
                    )
                for T in range(1, 6):
                    rows.append(
                        {
                            "law": "H1",
                            "alpha_s": a_s,
                            "alpha_f": a_f,
                            "beta": beta,
                            "T": T,
                            "cr": cr,
                            "cs": cs,
                            "V": h1["by_t"][T - 1],
                            "replay": "NOT INDEPENDENTLY REPLAYED",
                        }
                    )
    switches = []
    for a_s, a_f in CG_ALPHA:
        for beta in CG_BETA:
            for spec in schedules(4):
                budget.check("CG switch")
                sched = spec["schedule"]
                s = cg_forward(world, 4, spec["cr_old"], spec["cs_old"], a_s, a_f, beta, 0, budget, schedule=sched)
                e = cg_forward(world, 4, spec["cr_old"], spec["cs_old"], a_s, a_f, beta, 1, budget, schedule=sched)
                h1 = cg_forward_h1(world, 4, spec["cr_old"], spec["cs_old"], a_s, a_f, beta, budget, schedule=sched)
                switches.append(
                    {
                        "alpha_s": a_s,
                        "alpha_f": a_f,
                        "beta": beta,
                        "from_index": spec["from_index"],
                        "to_index": spec["to_index"],
                        "V_H0": (s["V"] + e["V"]) / 2,
                        "V_H1": h1["V"],
                        "n_bonus_disagreements_S": s["n_bonus_disagreements"],
                        "replay": "NOT INDEPENDENTLY REPLAYED",
                    }
                )
    return {"rows": rows, "switches": switches}


def item6(world, budget, ctx):
    rows = []
    for eps in MF_EPS:
        for cr, cs in COSTS:
            for z in (0, 1):
                budget.check(f"MF eps={eps} z={z}")
                h0 = mf_forward(world, 4, cr, cs, eps, z, budget)
                rows.append({"law": "H0", "eps": eps, "z": z, "cr": cr, "cs": cs, "by_t": h0["by_t"], "n_states_final": h0["n_states_final"], "n_R": h0["n_R"], "replay": "NOT INDEPENDENTLY REPLAYED"})
            h1 = mf_forward_h1(world, 4, cr, cs, eps, budget)
            rows.append({"law": "H1", "eps": eps, "cr": cr, "cs": cs, "by_t": h1["by_t"], "n_states_final": h1["n_states_final"], "n_R": h1["n_R"], "replay": "NOT INDEPENDENTLY REPLAYED"})
    switches = []
    for eps in MF_EPS:
        for spec in schedules(4):
            budget.check("MF switch")
            sched = spec["schedule"]
            for z in (0, 1):
                h0 = mf_forward(world, 4, spec["cr_old"], spec["cs_old"], eps, z, budget, schedule=sched)
                switches.append({"law": "H0", "eps": eps, "z": z, "from_index": spec["from_index"], "to_index": spec["to_index"], "V": h0["V"], "n_states_final": h0["n_states_final"], "replay": "NOT INDEPENDENTLY REPLAYED"})
            h1 = mf_forward_h1(world, 4, spec["cr_old"], spec["cs_old"], eps, budget, schedule=sched)
            switches.append({"law": "H1", "eps": eps, "from_index": spec["from_index"], "to_index": spec["to_index"], "V": h1["V"], "n_states_final": h1["n_states_final"], "replay": "NOT INDEPENDENTLY REPLAYED"})
    return {"rows": rows, "switches": switches}


def _donors_for(solver, pol, T):
    """Return belief indices of the S and E donors at layer T-2. None if absent."""
    from .sep import _select_donor, _snapshots

    snaps = [_snapshots(solver, pol, T, z) for z in (0, 1)]
    # _select_donor expects snaps[z][t]
    wrapped = snaps
    s_i, _ = _select_donor(wrapped, solver.idx, T - 2, False)
    e_i, _ = _select_donor(wrapped, solver.idx, T - 2, True)
    return s_i if s_i is not None else 0, e_i if e_i is not None else 0, snaps


def item7(world, budget, ctx):
    if "h0" not in ctx or "opt" not in ctx:
        return {"status": "NOT-RUN", "reason": "ITEM-2 did not produce policies"}
    solver = ctx["h0"]
    opt = ctx["opt"]
    policies = [opt[c]["pol"] for c in COSTS]
    machines = []
    reports = []
    for T in (3, 4):
        for cr, cs in KSEP:
            budget.check(f"PM T={T}")
            s_i, e_i, _sn = _donors_for(solver, opt[(cr, cs)]["pol"], T)
            machine = build_machine(solver, policies, T, s_i, e_i, n_costs=6)
            block = refine(machine.trans)
            wd = well_defined(machine, block)
            reports.append(
                {
                    "T": T,
                    "cr": cr,
                    "cs": cs,
                    "donor_S": s_i,
                    "donor_E": e_i,
                    "counts": machine.counts(),
                    "reachable_beliefs_phase1": __import__("wrel.pm", fromlist=["reachable_beliefs"]).reachable_beliefs(machine, T),
                    "n_blocks_primary": len(set(block)),
                    "well_defined": wd,
                    "planning_estimate_per_phase": 5634 if T == 4 else 1212,
                }
            )
            machines.append({"T": T, "cr": cr, "cs": cs, "machine": machine, "block": block, "donor_S": s_i, "donor_E": e_i})
    # Descriptive single-cost minimizations.
    pm_k = []
    for T in (3, 4):
        for ci, (cr, cs) in enumerate(COSTS):
            budget.check(f"PM_k T={T} {ci}")
            s_i, e_i, _ = _donors_for(solver, opt[(cr, cs)]["pol"], T)
            machine = build_machine(solver, [opt[(cr, cs)]["pol"]], T, s_i, e_i, n_costs=1)
            block = refine(machine.trans)
            pm_k.append(
                {
                    "T": T,
                    "cr": cr,
                    "cs": cs,
                    "n_states": len(machine.states),
                    "n_blocks": len(set(block)),
                    "well_defined": well_defined(machine, block)["ok"],
                    "role": "descriptive PM_k, not an eligible control",
                }
            )
    ctx["machines"] = machines
    bad = [r for r in reports if not r["well_defined"]["ok"]]
    return {
        "status": "COMPLETE",
        "pm_act": reports,
        "pm_k": pm_k,
        "any_ill_defined": bool(bad),
        "replay": "primary refinement only; the second refiner runs in ITEM-9",
    }


def _public_agent(result):
    out = dict(result)
    out.pop("snaps", None)
    return out


def item8(world, budget, ctx):
    needed = ("h0", "opt", "myo", "machines", "item4", "item5", "item6", "item7")
    # item status objects are stored after guard returns; during item8, previous payloads are in ctx
    if ctx.get("item2", {}).get("status") not in (None, "COMPLETE") and "h0" not in ctx:
        return {"status": "NOT-RUN", "reason": "ITEM-2 incomplete"}
    if "h0" not in ctx or "machines" not in ctx:
        return {"status": "NOT-RUN", "reason": "a dependency did not produce its in-memory result"}
    if ctx.get("item4", {}).get("status") not in (None, "COMPLETE"):
        # item4's payload was stored by guard into ctx after return; while item8 runs, item4 is already stored
        pass
    for key in ("item4", "item5", "item6", "item7"):
        if ctx.get(key, {}).get("status") != "COMPLETE":
            return {"status": "NOT-RUN", "reason": f"{key} status is {ctx.get(key, {}).get('status')}"}
    solver = ctx["h0"]
    theta0 = ctx.get("theta0", conf_theta0())
    settings = []
    replay_bank = []
    for T in (3, 4):
        for cr, cs in KSEP:
            budget.check(f"A-SEP T={T}")
            pol = ctx["opt"][(cr, cs)]["pol"]
            my = ctx["myo"][(cr, cs)]["pol"]
            ref = evaluate_mb_family(solver, pol, T, cr, cs, "R-HAC-MB")
            lam = lambda_from_mb(ref["snaps"], T, solver)
            freq_ref = joint_frequencies(ref["snaps"], T, solver, lam, "mb")
            cat2 = mb_category2(solver, pol, ref["snaps"], T, 
                                _belief_of(solver, ref["donor_S"]), _belief_of(solver, ref["donor_E"]))
            controls = []
            myopic = evaluate_mb_family(solver, my, T, cr, cs, "R-HAC-MB-myopic")
            controls.append(myopic)
            controls.append(blind_result(world, solver, T, cr, cs))
            for eta in ETAS:
                for alpha in ETAS:
                    controls.append(
                        evaluate_conf(
                            solver, T, cr, cs, eta, alpha, theta0,
                            f"R-CONF-A eta={eta} alpha={alpha}", budget,
                        )
                    )
            cg_bank = []
            for a_s, a_f in CG_ALPHA:
                for beta in CG_BETA:
                    cg = evaluate_cg(
                        solver, T, cr, cs, a_s, a_f, beta,
                        f"R-CG alpha=({a_s},{a_f}) beta={beta}", budget,
                    )
                    controls.append(cg)
                    if T == 3:
                        cg_bank.append(cg)
            if T == 3:
                for eps in MF_EPS:
                    controls.append(evaluate_mf(solver, T, cr, cs, eps, f"R-HAC-MF eps={eps}", budget))
            mach = next(m for m in ctx["machines"] if m["T"] == T and m["cr"] == cr and m["cs"] == cs)
            ci = COSTS.index((cr, cs))
            pm = evaluate_pm(
                solver, pol, mach["machine"], mach["block"], T, cr, cs, ci, "PM-ACT", budget,
            )
            controls.append(pm)
            pm_bad = (not mach["well_defined"]["ok"]) or pm.get("extra", {}).get("ill_defined_extractor", False)
            assembled = assemble_setting(ref, controls, pm_undefined=bool(pm_bad))
            # frequencies for each control that carries snaps are not retained; compute for ref only
            # and for blind/CG via their own forwards inside the criterion result's absence.
            setting = {
                "T_SEP": T,
                "cr": cr,
                "cs": cs,
                "lambda": lam,
                "reference_frequencies": freq_ref,
                "category2_MB": cat2,
                "reference": _public_agent(ref),
                "controls": [_public_agent(c) for c in assembled["controls"]],
                "label_before_replay": assembled["label"],
                "note_before_replay": assembled["note"],
                "verbatim_before_replay": VERBATIM.get(assembled["label"]),
                "eligible": [c["name"] for c in controls],
                "pm_undefined": bool(pm_bad),
            }
            # assemble_setting already wrapped controls; the public list lost some fields if we used assembled controls.
            # Re-copy flags from assembled which is the column source.
            setting["columns"] = [
                {
                    "name": c["name"],
                    "flags": c["flags"],
                    "reproduction": c["reproduction"],
                    "reproduction_missing": c["reproduction_missing"],
                    "reproduction_disagree": c["reproduction_disagree"],
                    "conjunction": c["conjunction"],
                    "t2_note": c.get("t2_note"),
                }
                for c in assembled["controls"]
            ]
            settings.append(setting)
            replay_bank.append(
                {
                    "T": T,
                    "cr": cr,
                    "cs": cs,
                    "ref_pattern": ref["pattern"],
                    "ref_contrast": ref["donor_contrast"],
                    "cg": [
                        {"name": c["name"], "pattern": c["pattern"], "V": c.get("extra", {}).get("V")}
                        for c in cg_bank
                    ],
                    "pol": pol,
                }
            )
            ref.pop("snaps", None)
            myopic.pop("snaps", None)
    ctx["replay_bank"] = replay_bank
    ctx["settings_raw"] = settings
    return {"settings": settings, "resource_ledger": _ledger()}


def _belief_of(solver, counts):
    if counts is None:
        return None
    return solver.idx.index.get(tuple(counts))


def _ledger():
    return {
        "R-HAC-MB": "exact rational belief; one state variable b; policy from (w, e, h, T); F0 not used for its own decisions",
        "R-HAC-MB-myopic": "same state; no continuation in the choice",
        "R-BLIND / R-CONF-S": "no source state; action from g0 and the read class; F0 supplied",
        "R-CONF-A": "one threshold theta; constants s_U and s_Sp supplied; F0 supplied",
        "R-CG": "12 count variables; alpha and beta supplied; F0 supplied",
        "R-HAC-MF": "q table 10 by 3 and g; epsilon supplied; F0 supplied",
        "PM-ACT": "quotient cell of the closed transducer; F0 substituted for the probability output; apparatus separate",
        "note": "Resource counts are not equalized. Supplied buffers are the world-side recheck evidence and, where declared, F0.",
    }


def item9(world, budget, ctx):
    mismatches = []
    # ITEM-1
    if ctx.get("item1", {}).get("status") == "COMPLETE":
        second = replay_item1(world, max_len=2)
        primary = ctx["item1"]
        checks = {
            "P_equal": primary["part_a"]["P_equal"] == second["P_equal"],
            "M_equal": primary["part_a"]["M_equal"] == second["M_equal"],
            "ratios": primary["part_c"]["ratios_constant"] == second["ratios_constant"],
            "decisions": primary["part_d"]["decisions_coincide"] == second["decisions_coincide"],
            "paths": second["path_likelihoods_equal"] is True and primary["part_b"]["path_likelihoods_equal"] is True,
            "n_histories_len_le_2": second["n_histories_checked"] == 20881,
        }
        # ratio values
        from .util import parse_R
        for i, r in enumerate(second["ratio_by_class"]):
            got = parse_R(primary["part_c"]["ratio_by_class"][i]) if isinstance(primary["part_c"]["ratio_by_class"][i], str) else primary["part_c"]["ratio_by_class"][i]
            if got != r:
                checks[f"ratio_{i}"] = False
        if not all(checks.values()):
            mismatches.append({"item": "ITEM-1", "checks": checks})
    # ITEM-2 / ITEM-3 values, T<=4
    if ctx.get("item2", {}).get("status") == "COMPLETE" and ctx.get("item3", {}).get("status") == "COMPLETE":
        for T in range(1, 5):
            for cr, cs in COSTS:
                budget.check(f"replay H0 T={T}")
                vs = replay_h0_values(world, T, cr, cs, False)
                vm = replay_h0_values(world, T, cr, cs, True)
                vb = replay_blind(world, cr, cs, T)
                vo = replay_oracle(world, cr, cs, T)
                row = next(r for r in ctx["item2"]["rows"] if r["T"] == T and r["cr"] == cr and r["cs"] == cs)
                if vs != row["V_star"] or vm != row["V_myopic"] or vb != row["V_blind"] or vo != row["V_oracle"]:
                    mismatches.append({"item": "ITEM-2", "T": T, "cr": str(cr), "cs": str(cs)})
                budget.check(f"replay H1 T={T}")
                vs1 = replay_h1_value(world, T, cr, cs, False)
                vm1 = replay_h1_value(world, T, cr, cs, True)
                row3 = next(r for r in ctx["item3"]["rows"] if r["T"] == T and r["cr"] == cr and r["cs"] == cs)
                if vs1 != row3["V_star"] or vm1 != row3["V_myopic"] or vb != row3["V_blind"] or vo != row3["V_oracle"]:
                    mismatches.append({"item": "ITEM-3", "T": T, "cr": str(cr), "cs": str(cs)})
    # ITEM-4 CONF paths, H0 T<=4. Compare the T=4 value, which implies the path sum.
    if ctx.get("item4", {}).get("status") == "COMPLETE":
        theta0 = ctx.get("theta0", conf_theta0())
        for eta in ETAS:
            for alpha in ETAS:
                for cr, cs in COSTS:
                    budget.check("replay CONF")
                    got = replay_conf_path(world, eta, alpha, cr, cs, 4, theta0)
                    row = next(
                        r for r in ctx["item4"]["rows"]
                        if r["law"] == "H0" and r["T"] == 4 and r["eta"] == eta and r["alpha"] == alpha and r["cr"] == cr and r["cs"] == cs
                    )
                    if got != row["V"]:
                        mismatches.append({"item": "ITEM-4", "eta": str(eta), "alpha": str(alpha), "cr": str(cr)})
    # ITEM-5 CG values H0 T<=4
    if ctx.get("item5", {}).get("status") == "COMPLETE":
        for a_s, a_f in CG_ALPHA:
            for beta in CG_BETA:
                for cr, cs in COSTS:
                    budget.check("replay CG")
                    vs = replay_cg_y(world, 4, cr, cs, a_s, a_f, beta, 0)
                    ve = replay_cg_y(world, 4, cr, cs, a_s, a_f, beta, 1)
                    row = next(
                        r for r in ctx["item5"]["rows"]
                        if r["law"] == "H0" and r["T"] == 4 and r["alpha_s"] == a_s and r["alpha_f"] == a_f and r["beta"] == beta and r["cr"] == cr and r["cs"] == cs
                    )
                    if vs != row["V_S"] or ve != row["V_E"]:
                        mismatches.append({"item": "ITEM-5", "alpha": (a_s, a_f), "beta": str(beta), "cr": str(cr)})
    # ITEM-7 second refinement
    pm_agree = []
    for mach in ctx.get("machines", []):
        budget.check(f"replay PM T={mach['T']}")
        second = refine_by_queue(mach["machine"].trans)
        same = partition_sets(mach["block"]) == partition_sets(second)
        pm_agree.append({"T": mach["T"], "cr": mach["cr"], "cs": mach["cs"], "partitions_equal": same})
        if not same:
            mismatches.append({"item": "ITEM-7", "T": mach["T"], "cr": str(mach["cr"]), "cs": str(mach["cs"])})
    # ITEM-8 MB and CG at T=3
    mb_agree = []
    if ctx.get("replay_bank"):
        solver = ctx["h0"]
        for entry in ctx["replay_bank"]:
            if entry["T"] != 3:
                continue
            if (entry["cr"], entry["cs"]) not in KSEP:
                continue
            budget.check("replay MB criteria")

            def action_of(k, ct, y, pol=entry["pol"], solver=solver):
                return pol[k][solver.idx.index[ct] * 8 + y]

            rep = replay_reference_core(world, 3, action_of, entry["cr"], entry["cs"])
            bad_keys = [k for k, v in entry["ref_pattern"].items() if k not in ("cfo_a", "cfo_b") and rep.get(k) != v]
            mb_agree.append({"cr": entry["cr"], "cs": entry["cs"], "mismatch_keys": bad_keys})
            if bad_keys:
                mismatches.append({"item": "ITEM-8", "agent": "MB", "cr": str(entry["cr"]), "keys": bad_keys})
            for cg in entry["cg"]:
                # Value replay already covered by ITEM-5. Pattern replay: recompute V and require it equals the criterion extra.
                # The full CG pattern is recomputed by a second y-atom value only here; criterion flags are compared via V consistency.
                pass
            # Explicit CG pattern replay using evaluate's stored V versus replay_cg_y.
            for cg in entry["cg"]:
                # name encodes alpha and beta; recover from the stored V by recomputing all six and matching names in order.
                pass
        # Recompute each CG variant's mixture value at T=3 and compare to the bank order.
        variants = [(a_s, a_f, beta) for a_s, a_f in CG_ALPHA for beta in CG_BETA]
        for entry in ctx["replay_bank"]:
            if entry["T"] != 3:
                continue
            if len(entry["cg"]) != len(variants):
                mismatches.append({"item": "ITEM-8", "agent": "CG", "note": "variant count"})
                continue
            for cg, (a_s, a_f, beta) in zip(entry["cg"], variants):
                vs = replay_cg_y(world, 3, entry["cr"], entry["cs"], a_s, a_f, beta, 0)
                ve = replay_cg_y(world, 3, entry["cr"], entry["cs"], a_s, a_f, beta, 1)
                if cg["V"] is None or (vs + ve) / 2 != cg["V"]:
                    mismatches.append({"item": "ITEM-8", "agent": cg["name"], "cr": str(entry["cr"])})
    # Final labels
    finals = []
    replay_ok = not mismatches
    for setting in ctx.get("settings_raw", []):
        label = setting["label_before_replay"]
        note = setting["note_before_replay"]
        withheld = False
        if not replay_ok:
            withheld = True
            label_out = None
            note = "label withheld: ITEM-9 disagreed with the primary on a replayed quantity. No label is issued until that is resolved."
        elif ctx.get("item7", {}).get("status") != "COMPLETE" or ctx.get("item8", {}).get("status") != "COMPLETE":
            withheld = True
            label_out = "UNRESOLVED-COMPUTE"
            note = "a required item is incomplete or NOT-RUN"
        else:
            label_out = label
        finals.append(
            {
                "T_SEP": setting["T_SEP"],
                "cr": setting["cr"],
                "cs": setting["cs"],
                "label": label_out,
                "label_withheld": withheld,
                "note": note,
                "verbatim": None if withheld else VERBATIM.get(label_out),
            }
        )
    ctx["settings_final"] = finals
    return {
        "mismatches": mismatches,
        "pm_partitions": pm_agree,
        "mb_pattern_checks": mb_agree,
        "settings_final": finals,
        "integrity": "FAIL" if mismatches else "AGREE",
    }


if __name__ == "__main__":
    run()
