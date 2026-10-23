"""Toy checks. Rates, costs, and the hazard are not study quantities.

World: S=(1/7, 1/9), E=(1/9, 1/7), h=1/6, costs (1/8, 1/3).
Horizons in this file are at most 3, except an optional timing probe
that is not a study-rate run.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from wrel.mb import H0Solver, forward_h1, solve_h1
from wrel.world import F, M_ACT, N_Y, P_ACT, R_ACT, World


def world():
    return World(F(1, 7), F(1, 9), F(1, 9), F(1, 7), F(1, 6))


def test_latent_matches_closed_form():
    w = world()
    assert w.emissions_match
    for z in (0, 1):
        for y in range(N_Y):
            for x in (0, 1):
                assert w.latent_p_default(z, y, x) == w.Ldef[z][y][x]
    # read marginals agree and sum to 1
    for z in (0, 1):
        assert sum(w.py[z]) == 1
        assert w.p_read[z][0] + w.p_read[z][1] == 1
        assert w.p_read[0] == w.p_read[1]


def test_h0_forward_matches_backward():
    w = world()
    cr, cs = F(1, 8), F(1, 3)
    sol = H0Solver(w, 3)
    opt = sol.solve_cost(cr, cs, myopic=False)
    myo = sol.solve_cost(cr, cs, myopic=True)
    for T in (1, 2, 3):
        acc = F(0)
        for z in (0, 1):
            fw = sol.forward(opt["pol"], T, cr, cs, z)
            acc += F(1, 2) * fw["value"]
        assert acc == opt["values"][T - 1], (T, acc, opt["values"][T - 1])
        acc_m = F(0)
        for z in (0, 1):
            fw = sol.forward(myo["pol"], T, cr, cs, z)
            acc_m += F(1, 2) * fw["value"]
        assert acc_m == myo["values"][T - 1], (T, acc_m, myo["values"][T - 1])
        # first-recheck probabilities sum with never to 1
        fw = sol.forward(opt["pol"], T, cr, cs, 0)
        assert sum(fw["first_R"], F(0)) + fw["never_R"] == 1


def test_h1_forward_matches_backward():
    w = world()
    cr, cs = F(1, 8), F(1, 3)
    for T, myopic in ((1, False), (2, False), (2, True), (3, False)):
        ans = solve_h1(w, T, cr, cs, myopic=myopic)
        # Rebuild a policy-only object for forward. solve_h1 returns pol.
        fw = forward_h1(w, ans["pol"], T, cr, cs)
        assert fw["value"] == ans["values"][T - 1], (T, myopic, fw["value"], ans["values"][T - 1])
        assert sum(fw["first_R"], F(0)) + fw["never_R"] == 1


def test_blind_one_trial_enumerates():
    w = world()
    cr, cs = F(1, 8), F(1, 3)
    # Pick P on unanimous and the g0 argmax on split, ties P>R>M.
    def choose(r):
        best_a, best_q = P_ACT, None
        costs = (F(0), cr, cs)
        for a in (P_ACT, R_ACT, M_ACT):
            q = w.g0[a][r] - costs[a]
            if best_q is None or q > best_q:
                best_q, best_a = q, a
        return best_a

    def action_of_y(y):
        return choose(0 if y in (0, N_Y - 1) else 1)

    def dec_of(a, y, obs):
        if a == P_ACT:
            return w.d_def[y]
        if a == R_ACT:
            return w.d_recheck(F(1, 2), y, obs)
        return w.d_resample(F(1, 2), y, obs)

    vS = w.one_trial_value(0, action_of_y, dec_of, cr, cs)
    vE = w.one_trial_value(1, action_of_y, dec_of, cr, cs)
    # g0 mixture value
    v = F(0)
    for r, pr in ((0, w.p_read[0][0]), (1, w.p_read[0][1])):
        a = choose(r)
        # correctness under the half-half prior equals g0
        v += pr * (w.g0[a][r] - (F(0), cr, cs)[a])
    assert v == F(1, 2) * (vS + vE)


def test_label_order():
    from wrel.labels import decide_setting

    ref_pass = {"C-REF": "PASS", "C-T2": "PASS", "C-SEL": "PASS", "C-FO": "PASS", "rescue": "PASS"}
    fail = dict(ref_pass)
    fail["C-REF"] = "FAIL"
    assert decide_setting(False, fail, [])[0] == "REFERENCE CRITERIA NOT MET"
    controls = [
        {
            "name": "A",
            "flags": fail,
            "reproduction": "NO",
            "conjunction": "FAILS",
        }
    ]
    assert decide_setting(True, ref_pass, controls)[0] == "DISTINGUISHES NAMED CONTROLS"
    controls[0]["reproduction"] = "YES"
    controls[0]["conjunction"] = "ATTAINED"
    controls[0]["flags"] = dict(ref_pass)
    assert decide_setting(True, ref_pass, controls)[0] == "PATTERN REPRODUCED BY NAMED CONTROL"
    controls[0]["reproduction"] = "NO"
    assert decide_setting(True, ref_pass, controls)[0].startswith("CORE CRITERIA SHARED")
    blind = {
        "name": "BLIND",
        "flags": {
            "C-REF": "FAIL",
            "C-T2": "PASS",
            "C-SEL": "NOT APPLICABLE",
            "C-FO": "PASS",
            "rescue": "NOT APPLICABLE",
        },
        "reproduction": "UNRESOLVED",
        "conjunction": "FAILS",
    }
    # A failure plus an unresolved reproduction and no YES reproduction is UNRESOLVED-DESIGN.
    assert decide_setting(True, ref_pass, [blind])[0] == "UNRESOLVED-DESIGN"
    blind["reproduction"] = "NO"
    assert decide_setting(True, ref_pass, [blind])[0] == "DISTINGUISHES NAMED CONTROLS"
    stateless = {
        "name": "S",
        "flags": {
            "C-REF": "PASS",
            "C-T2": "PASS",
            "C-SEL": "NOT APPLICABLE",
            "C-FO": "PASS",
            "rescue": "PASS",
        },
        "reproduction": "NO",
        "conjunction": "UNRESOLVED",
    }
    assert decide_setting(True, ref_pass, [stateless])[0] == "UNRESOLVED-DESIGN"


def test_y_atoms_and_controls():
    from wrel.agents import cg_forward, conf_a_episode
    from wrel.controls import conf_theta0, evaluate_cg, evaluate_conf, evaluate_mf
    from wrel.sep import blind_result, evaluate_mb_family

    w = world()
    for z in (0, 1):
        for y in range(N_Y):
            for a in range(3):
                s = sum((atom[3] for atom in w.y_atoms()[z][y][a]), F(0))
                assert s == 1, (z, y, a, s)
    cr, cs = F(1, 8), F(1, 3)
    sol = H0Solver(w, 3)
    opt = sol.solve_cost(cr, cs)
    mb = evaluate_mb_family(sol, opt["pol"], 3, cr, cs, "MB")
    assert mb["pattern"]["E_err_agent"] == 0
    blind = blind_result(w, sol, 3, cr, cs)
    assert blind["pattern"]["delta_R"] == 0
    assert blind["pattern"]["delta_M"] == 0
    assert blind["flags"]["C-SEL"] == "NOT APPLICABLE"
    cg = evaluate_cg(sol, 2, cr, cs, 1, 1, F(0), "CG", None)
    direct = cg_forward(w, 2, cr, cs, 1, 1, F(0), 0)
    direct_e = cg_forward(w, 2, cr, cs, 1, 1, F(0), 1)
    assert cg["extra"]["V_S"] == direct["V"]
    assert cg["extra"]["V_E"] == direct_e["V"]
    th = conf_theta0()
    cf = evaluate_conf(sol, 2, cr, cs, F(1, 10), F(1, 10), th, "CONF", None)
    ep = conf_a_episode(w, F(1, 10), F(1, 10), cr, cs, 2, th)
    assert cf["extra"]["V_S"] == ep["V_S"]
    assert cf["extra"]["V_E"] == ep["V_E"]
    mf = evaluate_mf(sol, 2, cr, cs, F(0), "MF", None)
    assert mf["extra"]["V_S"] == mf["extra"]["V_S"]
    assert mf["flags"]["C-FO"] == "PASS"


def test_replay_matches_primary_on_toy():
    from wrel.agents import blind_value, cg_forward, conf_a_episode, oracle_value
    from wrel.controls import conf_theta0
    from wrel.item1 import audit
    from wrel.replay import (
        replay_blind,
        replay_cg_y,
        replay_conf_path,
        replay_h0_values,
        replay_h1_value,
        replay_item1,
        replay_oracle,
        replay_reference_core,
    )

    w = world()
    cr, cs = F(1, 8), F(1, 3)
    sol = H0Solver(w, 3)
    for myopic in (False, True):
        ans = sol.solve_cost(cr, cs, myopic=myopic)
        assert replay_h0_values(w, 3, cr, cs, myopic=myopic) == ans["values"][2]
        assert replay_h1_value(w, 2, cr, cs, myopic=myopic) == solve_h1_value(w, cr, cs, myopic)
    assert replay_blind(w, cr, cs, 3) == blind_value(w, cr, cs, 3)["V"]
    assert replay_oracle(w, cr, cs, 2) == oracle_value(w, cr, cs, 2)["V"]
    assert replay_cg_y(w, 2, cr, cs, 1, 1, F(0), 0) == cg_forward(w, 2, cr, cs, 1, 1, F(0), 0)["V"]
    th = conf_theta0()
    assert replay_conf_path(w, F(1, 5), F(1, 5), cr, cs, 3, th) == conf_a_episode(w, F(1, 5), F(1, 5), cr, cs, 3, th)["V"]
    primary = audit(w, max_len=1)
    second = replay_item1(w, max_len=1)
    assert primary["part_a"]["P_equal"] == second["P_equal"]
    assert primary["part_a"]["M_equal"] == second["M_equal"]
    assert primary["part_c"]["ratios_constant"] == second["ratios_constant"]
    assert primary["part_d"]["decisions_coincide"] == second["decisions_coincide"]
    assert primary["part_b"]["path_likelihoods_equal"] == second["path_likelihoods_equal"]
    assert second["n_histories_checked"] == 145  # 1 + 144
    # Forced RECHECK is not an optimal study policy. It exercises donor contrast on toy rates.
    from wrel.sep import evaluate_mb_family
    from wrel.world import N_Y, R_ACT

    sol = H0Solver(w, 3)
    opt = sol.solve_cost(cr, cs)
    pol = [None]
    for k in range(1, 4):
        ba = bytearray(opt["pol"][k])
        if k >= 2:
            for i in range(len(sol.idx.counts)):
                for y in range(N_Y):
                    ba[i * 8 + y] = R_ACT
        pol.append(ba)
    mb = evaluate_mb_family(sol, pol, 3, cr, cs, "forced")
    assert mb["donor_contrast"]

    def action_of(k, ct, y, pol=pol, sol=sol):
        return pol[k][sol.idx.index[ct] * 8 + y]

    rep = replay_reference_core(w, 3, action_of, cr, cs)
    for key, val in mb["pattern"].items():
        if key in ("cfo_a", "cfo_b"):
            continue
        assert rep[key] == val, key


def solve_h1_value(w, cr, cs, myopic):
    from wrel.mb import solve_h1

    return solve_h1(w, 2, cr, cs, myopic=myopic)["values"][1]


def test_pm_toy_closure():
    from wrel.pm import build_machine, partition_sets, refine, refine_by_queue, well_defined

    w = world()
    cr, cs = F(1, 11), F(1, 4)
    sol = H0Solver(w, 3)
    opt = sol.solve_cost(cr, cs)
    # Donors are belief indices. 0,0 is a legal closure input and is not a study quantity.
    machine = build_machine(sol, [opt["pol"]], 3, 0, 0, n_costs=1)
    b1 = refine(machine.trans)
    b2 = refine_by_queue(machine.trans)
    assert partition_sets(b1) == partition_sets(b2)
    assert well_defined(machine, b1)["ok"]


if __name__ == "__main__":
    t0 = time.perf_counter()
    test_latent_matches_closed_form()
    test_blind_one_trial_enumerates()
    test_h0_forward_matches_backward()
    test_h1_forward_matches_backward()
    test_label_order()
    test_y_atoms_and_controls()
    test_replay_matches_primary_on_toy()
    test_pm_toy_closure()
    print(f"toy tests passed in {time.perf_counter() - t0:.2f}s")
