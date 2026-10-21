"""ITEM-8 criterion statistics. Thresholds are the spec §4.6 constants."""

from __future__ import annotations

from fractions import Fraction

from .agents import S_SP_SPEC, S_U_SPEC, _tie_max, blind_table, cg_choose
from .labels import conjunction_of, decide_setting
from .world import F, M_ACT, N_Y, P_ACT, R_ACT, read_class

MU_REF = F(1, 100)
MU_T2 = F(1, 2)
MU_SELa = F(1, 100)
MU_SELc = F(1, 100)
MU_RESa = F(1, 100)
MU_RESc = F(1, 100)
MU_RESL = F(1, 100)
RHO = F(1, 1000)
SPLIT = tuple(y for y in range(N_Y) if read_class(y) == 1)
CORE_NAMES = ("C-REF", "C-T2", "C-SEL", "C-FO", "rescue")


def _snapshots(solver, pol, T, z):
    idx = solver.idx
    py = solver.world.py[z]
    mass = {0: F(1)}
    out = []
    for t in range(T):
        k = T - t
        snap = [(i, p) for i, p in mass.items() if p != 0]
        out.append(snap)
        new = {}
        pk = pol[k]
        for i, p in snap:
            base = i * N_Y
            for y in range(N_Y):
                a = pk[base + y]
                w = p * py[y]
                if a != R_ACT:
                    new[i] = new.get(i, F(0)) + w
                else:
                    row = idx.pc[z][y]
                    tr = idx.trans[i]
                    for c in range(10):
                        wc = w * row[c]
                        if wc == 0:
                            continue
                        j = tr[c]
                        new[j] = new.get(j, F(0)) + wc
        mass = new
    return out


def _better(cand, other, minimize_b: bool) -> bool:
    """cand/other = (b, fwd, enc)."""
    if other is None:
        return True
    if cand[0] != other[0]:
        return cand[0] < other[0] if minimize_b else cand[0] > other[0]
    if cand[1] != other[1]:
        return cand[1] > other[1]
    return cand[2] < other[2]


def _select_donor(snaps, idx, t, minimize_b: bool):
    best = None
    best_i = None
    for z in (0, 1):
        for i, p in snaps[z][t]:
            cand = (idx.b[i], F(1, 2) * p, idx.counts[i])
            if _better(cand, best, minimize_b):
                best = cand
                best_i = i
    return best_i, best


def _m_f0(world, b_true, y, a, immP, immM):
    if a == P_ACT:
        return immP[y]
    if a == M_ACT:
        return immM[y]
    return world.expected_correct_R(F(1, 2), b_true, y)


def _m_mb(world, b_pred, b_true, y, a, immP, immM):
    if a == P_ACT:
        return immP[y]
    if a == M_ACT:
        return immM[y]
    return world.expected_correct_R(b_pred, b_true, y)


def _avg(num, den):
    if den == 0:
        return None
    return num / den


def ct2_from_mixture(snaps, T, py, mhat_m):
    """mhat_m(i, y, a, b_true_obs) -> (mhat, m). b_true_obs is the observational posterior.

    Returns per-action squared errors for the agent and the baseline is computed
    by the caller via a second invocation. Here one readout.
    """
    per = {}
    for a in (R_ACT, M_ACT):
        acc = F(0)
        ok = True
        for t in range(T):
            num = F(0)
            den = F(0)
            for z in (0, 1):
                for i, p in snaps[z][t]:
                    for y in SPLIT:
                        w = F(1, 2) * p * py[y]
                        den += w
                        mh, m = mhat_m(i, y, a)
                        num += w * (mh - m) ** 2
            if den == 0:
                ok = False
                break
            acc += num / den
        per[a] = None if not ok else acc / T
    if per[R_ACT] is None or per[M_ACT] is None:
        return None, per
    return (per[R_ACT] + per[M_ACT]) / 2, per


def _cref(snaps, pol, T, py):
    """E[count of R on split | z] and E[count of M on split | z], z=0 and 1."""
    out = []
    for z in (0, 1):
        nR = F(0)
        nM = F(0)
        for t in range(T):
            k = T - t
            pk = pol[k]
            for i, p in snaps[z][t]:
                base = i * N_Y
                for y in SPLIT:
                    w = p * py[y]
                    a = pk[base + y]
                    if a == R_ACT:
                        nR += w
                    elif a == M_ACT:
                        nM += w
        out.append((nR, nM))
    return out


def _split_stats_point(states, z, k, pol, world, immP, immM, mhat_fn):
    """states: iterable of (i, p). Pinned Z. Returns e, q, L for action R, or None if no mass."""
    py = world.py[z]
    point = F(1) if z == 0 else F(0)
    num_e = num_q = num_L = den = F(0)
    pk = pol[k]
    for i, p in states:
        base = i * N_Y
        b = None
        for y in SPLIT:
            w = p * py[y]
            if w == 0:
                continue
            den += w
            a = pk[base + y]
            if a == R_ACT:
                num_q += w
            mh = mhat_fn(i, y)
            m = world.expected_correct_R(b if False else _pred_b(mhat_fn, i, world), point, y)
            # The predictor belief is agent-specific. mhat_fn's closure knows it;
            # m for a Z pin uses the agent's predictor. Pass it via mhat_fn attributes.
            m = mhat_fn.m(i, y, point)
            num_e += w * (mh - m)
            diff = mh - m
            num_L += w * (diff if diff >= 0 else -diff)
    if den == 0:
        return None
    return num_e / den, num_q / den, num_L / den


def _pred_b(fn, i, world):
    return F(1, 2)


class Readout:
    def __init__(self, mhat, m_pinned):
        self.mhat = mhat
        self.m = m_pinned

    def __call__(self, i, y):
        return self.mhat(i, y)


def _stats(states, z, k, pol, world, readout: Readout):
    py = world.py[z]
    point = F(1) if z == 0 else F(0)
    num_e = num_q = num_L = den = F(0)
    pk = pol[k]
    for i, p in states:
        if p == 0:
            continue
        base = i * N_Y
        for y in SPLIT:
            w = p * py[y]
            den += w
            if pk[base + y] == R_ACT:
                num_q += w
            mh = readout.mhat(i, y)
            m = readout.m(i, y, point)
            d = mh - m
            num_e += w * d
            num_L += w * (d if d >= 0 else -d)
    if den == 0:
        return None
    return {"e": num_e / den, "q": num_q / den, "L": num_L / den}


def _advance(recipients, donor, clamp, z, k, pol, solver):
    """recipients (pre_state, p). Controller starts at donor if donor is not None else pre_state.

    Shadow starts at pre_state and always applies the feedback update.
    Returns (A mass dict, B mass dict) at the next trial.
    """
    idx = solver.idx
    py = solver.world.py[z]
    A, B = {}, {}
    pk = pol[k]
    for i, p in recipients:
        ctrl = i if donor is None else donor
        for y in range(N_Y):
            a = pk[ctrl * N_Y + y]
            w = p * py[y]
            if a != R_ACT:
                A[ctrl] = A.get(ctrl, F(0)) + w
                B[i] = B.get(i, F(0)) + w
            else:
                for c in range(10):
                    wc = w * idx.pc[z][y][c]
                    if wc == 0:
                        continue
                    sA = ctrl if clamp else idx.trans[ctrl][c]
                    sB = idx.trans[i][c]
                    A[sA] = A.get(sA, F(0)) + wc
                    B[sB] = B.get(sB, F(0)) + wc
    return A, B


def _flag_ref(dR, dM):
    if dR is None or dM is None:
        return "NOT EVALUABLE [zero-probability event]"
    return "PASS" if dR >= MU_REF and dM >= MU_REF else "FAIL"


def _flag_t2(e_agent, e_base):
    if e_agent is None or e_base is None:
        return "NOT EVALUABLE [zero-probability event]", None
    if e_base == 0:
        return "FAIL", "NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated."
    imp = (e_base - e_agent) / e_base
    return ("PASS" if imp >= MU_T2 else "FAIL"), imp


def _flag_sel(de_s, dq_s, de_e, dq_e, cfo, contrast):
    if not contrast:
        return "NOT EVALUABLE [NO INTERVENTION CONTRAST]"
    if any(v is None for v in (de_s, dq_s, de_e, dq_e)):
        return "NOT EVALUABLE [zero-probability event]"
    ok = (
        de_s >= MU_SELa
        and dq_s >= MU_SELc
        and de_e <= -MU_SELa
        and dq_e <= -MU_SELc
        and cfo == "PASS"
    )
    return "PASS" if ok else "FAIL"


def _flag_rescue(bundle, contrast):
    """bundle[dir] = dict with eA,eB,qA,qB,LA,LB. dir 'S' uses σ=+1, 'E' uses σ=-1."""
    if not contrast:
        return "NOT EVALUABLE [NO INTERVENTION CONTRAST]"
    if bundle is None:
        return "NOT EVALUABLE [zero-probability event]"
    for name, sigma in (("S", 1), ("E", -1)):
        b = bundle[name]
        if any(b[k] is None for k in ("eA", "eB", "qA", "qB", "LA", "LB")):
            return "NOT EVALUABLE [zero-probability event]"
        if sigma * (b["eA"] - b["eB"]) < MU_RESa:
            return "FAIL"
        if sigma * (b["qA"] - b["qB"]) < MU_RESc:
            return "FAIL"
        if b["LA"] - b["LB"] < MU_RESL:
            return "FAIL"
    return "PASS"


def _cfo_mb(world, beliefs):
    """Exact equality of p0 and of decisions across the supplied beliefs. Empty -> PASS."""
    if len(beliefs) <= 1:
        return "PASS", "PASS"
    ref = beliefs[0]
    for b in beliefs[1:]:
        for y in range(N_Y):
            if world.p_recheck(ref, y, 0) and False:
                pass
            p1 = _pdef(world, ref, y)
            p2 = _pdef(world, b, y)
            if p1 != p2:
                return "FAIL", "FAIL"
        for y in range(N_Y):
            for yp in range(N_Y):
                if world.d_recheck(ref, y, yp) != world.d_recheck(b, y, yp):
                    return "FAIL", "FAIL"
            for ypp in range(N_Y):
                if world.d_resample(ref, y, ypp) != world.d_resample(b, y, ypp):
                    return "FAIL", "FAIL"
    return "PASS", "PASS"


def _pdef(world, b, y):
    num = den = F(0)
    for z, bz in ((0, b), (1, 1 - b)):
        for x in (0, 1):
            w = bz * world.pyx[z][y][x]
            den += w
            if x == 1:
                num += w
    return num / den


def evaluate_mb_family(solver, pol, T, cr, cs, name: str):
    """Reference or myopic MB. pol is indexed by remaining horizon."""
    world = solver.world
    idx = solver.idx
    py = world.py[0]
    snaps = [_snapshots(solver, pol, T, z) for z in (0, 1)]
    # C-REF
    raw = _cref(snaps, pol, T, py)
    dR = raw[0][0] - raw[1][0]
    dM = raw[1][1] - raw[0][1]
    # C-T2 observational
    def mh_m(i, y, a):
        b = idx.b[i]
        m = _m_mb(world, b, b, y, a, solver.immP, solver.immM)
        return m, m  # MB readout is the posterior predictive of its own predictor

    def base_m(i, y, a):
        b = idx.b[i]
        m = _m_mb(world, b, b, y, a, solver.immP, solver.immM)
        return world.g0[a][read_class(y)], m

    e_agent, per_agent = ct2_from_mixture(snaps, T, py, mh_m)
    e_base, per_base = ct2_from_mixture(snaps, T, py, base_m)
    # lambda and frequencies use the reference caller's distribution; here we
    # compute this agent's own frequencies against a lambda supplied later.
    t_star = T - 2
    s_i, s_meta = _select_donor(snaps, idx, t_star, False)
    e_i, e_meta = _select_donor(snaps, idx, t_star, True)
    contrast = s_i is not None and s_i != e_i
    # also absent if every E-recipient already equals S-donor, or S-recipient equals E-donor
    def _all_equal(z, donor):
        return all(i == donor for i, p in snaps[z][t_star] if p != 0)

    if contrast and (_all_equal(1, s_i) or _all_equal(0, e_i)):
        contrast = False
    recipients = {0: snaps[0][t_star], 1: snaps[1][t_star]}

    def make_readout(state_i):
        b = idx.b[state_i]

        def mhat(i, y, b=b):
            return _m_mb(world, b, b, y, R_ACT, solver.immP, solver.immM)

        def m(i, y, point, b=b):
            return world.expected_correct_R(b, point, y)

        return Readout(mhat, m)

    # For a distribution of states, mhat depends on each state's own belief.
    def readout_own():
        def mhat(i, y):
            b = idx.b[i]
            return _m_mb(world, b, b, y, R_ACT, solver.immP, solver.immM)

        def m(i, y, point):
            b = idx.b[i]
            return world.expected_correct_R(b, point, y)

        return Readout(mhat, m)

    own = readout_own()
    k_pert = 2  # T - (T-2)
    assert T - (T - 2) == 2
    interventions = {}
    for direction, z, donor in (("S", 1, s_i), ("E", 0, e_i)):
        rec = recipients[z]
        intact = _stats(rec, z, k_pert, pol, world, own)
        modes = {}
        if donor is None:
            modes = None
        else:
            donor_mass = [(donor, F(1))]
            donor_ro = make_readout(donor)
            for mode, don, clamp in (
                ("SWAP", donor, False),
                ("CORRUPT", donor, True),
                ("SUSPEND", None, True),
            ):
                if mode == "SUSPEND":
                    mass_now = rec
                    ro = own
                else:
                    mass_now = donor_mass
                    ro = donor_ro
                now = _stats(mass_now, z, k_pert, pol, world, ro)
                A, B = _advance(rec, don, clamp, z, k_pert, pol, solver)
                # integrity: B is the shadow by construction
                stA = _stats(A.items(), z, 1, pol, world, own if mode == "SUSPEND" else readout_own())
                # After the trial, A states have their own beliefs; readout must be own-belief.
                stA = _stats(A.items(), z, 1, pol, world, own)
                stB = _stats(B.items(), z, 1, pol, world, own)
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
    # C-FO across donor and recipient beliefs that appear
    beliefs = []
    if s_i is not None:
        beliefs.append(idx.b[s_i])
    if e_i is not None:
        beliefs.append(idx.b[e_i])
    for z in (0, 1):
        for i, p in snaps[z][t_star]:
            if p != 0:
                beliefs.append(idx.b[i])
    cfo_a, cfo_b = _cfo_mb(world, beliefs)
    cfo = "PASS" if cfo_a == "PASS" and cfo_b == "PASS" else "FAIL"
    t2_flag, imp = _flag_t2(e_agent, e_base)
    swap_s = None if interventions["S"] is None else interventions["S"]["SWAP"]
    swap_e = None if interventions["E"] is None else interventions["E"]["SWAP"]
    sel = _flag_sel(
        None if swap_s is None else swap_s["D_e"],
        None if swap_s is None else swap_s["D_q"],
        None if swap_e is None else swap_e["D_e"],
        None if swap_e is None else swap_e["D_q"],
        cfo,
        contrast,
    )
    rescue_bundle = None
    if swap_s is not None and swap_e is not None:
        rescue_bundle = {"S": swap_s, "E": swap_e}
    rescue = _flag_rescue(rescue_bundle, contrast)
    flags = {
        "C-REF": _flag_ref(dR, dM),
        "C-T2": t2_flag,
        "C-SEL": sel,
        "C-FO": cfo,
        "rescue": rescue,
    }
    pattern = {
        "delta_R": dR,
        "delta_M": dM,
        "E_err_agent": e_agent,
        "E_err_baseline": e_base,
        "D_e_S": None if swap_s is None else swap_s["D_e"],
        "D_e_E": None if swap_e is None else swap_e["D_e"],
        "D_q_S": None if swap_s is None else swap_s["D_q"],
        "D_q_E": None if swap_e is None else swap_e["D_q"],
        "cfo_a": cfo_a == "PASS",
        "cfo_b": cfo_b == "PASS",
        "e_A_S": None if swap_s is None else swap_s["eA"],
        "e_B_S": None if swap_s is None else swap_s["eB"],
        "q_A_S": None if swap_s is None else swap_s["qA"],
        "q_B_S": None if swap_s is None else swap_s["qB"],
        "e_A_E": None if swap_e is None else swap_e["eA"],
        "e_B_E": None if swap_e is None else swap_e["eB"],
        "q_A_E": None if swap_e is None else swap_e["qA"],
        "q_B_E": None if swap_e is None else swap_e["qB"],
    }
    return {
        "name": name,
        "flags": flags,
        "pattern": pattern,
        "t2_note": imp if isinstance(imp, str) else None,
        "t2_improvement": None if isinstance(imp, str) else imp,
        "per_action_agent": per_agent,
        "per_action_baseline": per_base,
        "cref_counts": raw,
        "donor_S": None if s_i is None else list(idx.counts[s_i]),
        "donor_E": None if e_i is None else list(idx.counts[e_i]),
        "donor_contrast": contrast,
        "interventions": interventions,
        "snaps": snaps,
    }


def compare_pattern(ref, other):
    """Reproduction YES / NO / UNRESOLVED against ρ_REP. Equality flags are exact."""
    missing = []
    disagree = []
    for key, rv in ref.items():
        ov = other.get(key)
        if rv is None or ov is None:
            missing.append(key)
            continue
        if isinstance(rv, bool):
            if rv != ov:
                disagree.append(key)
        else:
            diff = rv - ov
            if diff < 0:
                diff = -diff
            if diff > RHO:
                disagree.append(key)
    if disagree:
        return "NO", missing, disagree
    if missing:
        return "UNRESOLVED", missing, disagree
    return "YES", missing, disagree


def reference_met(flags) -> bool:
    return all(flags[k] == "PASS" for k in CORE_NAMES)


def assemble_setting(ref_result, control_results, incomplete: bool = False, pm_undefined: bool = False):
    ref_flags = ref_result["flags"]
    controls = []
    for c in control_results:
        rep, missing, disagree = compare_pattern(ref_result["pattern"], c["pattern"])
        conj = conjunction_of(c["flags"])
        controls.append(
            {
                "name": c["name"],
                "flags": c["flags"],
                "reproduction": rep,
                "reproduction_missing": missing,
                "reproduction_disagree": disagree,
                "conjunction": conj,
                "pattern": c["pattern"],
                "t2_note": c.get("t2_note"),
                "donor_contrast": c.get("donor_contrast"),
                "interventions": c.get("interventions"),
                "donor_S": c.get("donor_S"),
                "donor_E": c.get("donor_E"),
            }
        )
    label, note = decide_setting(
        reference_met(ref_flags),
        ref_flags,
        controls,
        incomplete=incomplete,
        pm_undefined=pm_undefined,
    )
    return {"label": label, "note": note, "reference": ref_result, "controls": controls}


def blind_result(world, solver, T, cr, cs):
    """Stateless control. C-SEL and rescue are NOT APPLICABLE."""
    act = blind_table(world, cr, cs)
    # Synthesize a policy bytearray that ignores belief: action depends on y via its read.
    # Use belief 0 only for snapshots; the policy is constant across beliefs.
    n = len(solver.idx.counts)
    pol = [None]
    # We only need actions at the beliefs the constant policy reaches, but C-REF
    # uses the same action for every belief. Build pol[k] identically.
    ba = bytearray(n * N_Y)
    for i in range(n):
        for y in range(N_Y):
            ba[i * N_Y + y] = act[read_class(y)]
    for k in range(1, T + 1):
        pol.append(ba)
    snaps = [_snapshots(solver, pol, T, z) for z in (0, 1)]
    raw = _cref(snaps, pol, T, solver.world.py[0])
    dR = raw[0][0] - raw[1][0]
    dM = raw[1][1] - raw[0][1]

    def base_m(i, y, a):
        m = _m_f0(world, solver.idx.b[i], y, a, solver.immP, solver.immM)
        return world.g0[a][read_class(y)], m

    e_agent, per_a = ct2_from_mixture(snaps, T, world.py[0], base_m)
    # readout IS g0, so agent error equals baseline error
    e_base = e_agent
    t2_flag, imp = _flag_t2(e_agent, e_base)
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
        "E_err_baseline": e_base,
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
