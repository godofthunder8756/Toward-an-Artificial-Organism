"""N2 v2: exact reference checks for spec v2 at costs (1/100, 3/50), phi=1/4, kappa=1/4.
Worlds: PRIMARY kappa_0 = 1/16 (C-K0, PROPOSED); DIAGNOSTIC kappa_0 = 0 (v1 world) with the v2
target on R, declared in PRE_RUN_FREEZE_v2.txt before running, to separate target-definition
effects from kappa_0. Reference = R-HIST (exact Bayes on received history R). Oracle o = clean
world-model Bayes averaged over world samples given R. No learner, no network, no training."""
import json, sys, time, math, itertools
from fractions import Fraction as Fr
from acq_model_v2 import *

SMOKE = "--smoke" in sys.argv; t0 = time.time()
S = str; fl = float
E1 = {"lo": [1, 1, 2, 3, 5, 12], "hi": [2, 3, 4, 4, 5, 6]}
def enum(y, Y, N): t = E1[N]; return t[y] if Y == 1 else t[5 - y]
out = {"mode": "SMOKE" if SMOKE else "PRIMARY", "costs": {"R": "1/100", "S": "3/50"}, "phi": "1/4", "kappa": "1/4", "worlds": {}}

def run_world(name, kappa0):
    M = graded_model(kappa0); R = Ref(M, kmax=1 if SMOKE else KMAX); W = {"kappa0": S(kappa0)}
    kmaxd = 1 if SMOKE else KMAX
    def qnum(rec, y, F):
        if F == 1: return 76 if rec == y else 4
        if kappa0 == Fr(1, 16): return 91 if rec == y else 1
        if kappa0 == 0: return 96 if rec == y else 0
        raise ValueError("unsupported kappa0")
    # ---- (a) profitability, both readings
    dec_states = [r for r in received_histories(6, kmaxd - 1)]
    acts = {r: R.act(r) for r in dec_states}
    st1 = {}
    for r in dec_states:
        if len(r[1]) == 1:
            qs = R.Q(r); st1[f"{r[0]},y~={r[1][0][1]+1}"] = {"Q": {a: S(v) for a, v in qs.items()}, "act": acts[r],
                "gain_R": fl(qs["R"] - qs["P"]), "gain_S": fl(qs["S"] - qs["P"])}
    W["stage1_received"] = st1
    pw = {}
    for N in CUES:
        for y in range(6):
            pr = {a: sum(M["q"](x, y, F) * (PHI if F else 1 - PHI) for F in (0, 1) for x in range(6) if acts[(N, (("F", x),))] == a) for a in ("R", "S")}
            pw[f"{N},y1={y+1}"] = {"P(first=RECHECK)": S(pr["R"]), "P(first=RESAMPLE)": S(pr["S"])}
    W["stage1_world_first_action"] = pw
    cnt = {}
    for r, a in acts.items():
        k = len(r[1]); cnt.setdefault(k, {"P": 0, "R": 0, "S": 0}); cnt[k][a] += 1
    W["optimal_action_counts_by_stage"] = cnt
    rate = {"R": Fr(0), "S": Fr(0)}; vopt = Fr(0); vpred = Fr(0)
    for N in CUES:
        for y1 in range(6):
            root = (N, (("F", y1),)); p0 = mass_R(R, root)
            vopt += p0 * R.V(root); vpred += p0 * R.assess(root)
            stack = [(root, p0)]
            while stack:
                node, p = stack.pop(); a = R.act(node)
                if a == "P": continue
                rate[a] += p
                for _, n2, pn in R.next_probs(node, a):
                    if pn: stack.append((n2, p * pn))
    W["optimal_policy"] = {"E[#RECHECK]": S(rate["R"]), "E[#RESAMPLE]": S(rate["S"]), "value_optimal": S(vopt), "value_always_predict": S(vpred),
                           "floats": {"E[#R]": fl(rate["R"]), "E[#S]": fl(rate["S"]), "v_opt": fl(vopt), "v_pred": fl(vpred), "gain": fl(vopt - vpred)}}
    s1R = any(a == "R" for r, a in acts.items() if len(r[1]) == 1); s1S = any(a == "S" for r, a in acts.items() if len(r[1]) == 1)
    anyR = any(a == "R" for a in acts.values()); anyS = any(a == "S" for a in acts.values())
    W["12_4a"] = {"stage1_reading": {"RECHECK": s1R, "RESAMPLE": s1S, "holds": s1R and s1S},
                  "some_decision_stage_reading": {"RECHECK": anyR and rate["R"] > 0, "RESAMPLE": anyS and rate["S"] > 0, "holds": anyR and anyS and rate["R"] > 0 and rate["S"] > 0}}
    print(name, "12.4a", W["12_4a"], "policy", W["optimal_policy"]["floats"])
    # ---- (b)(c) contrast on R, stage 2 after RECHECK (R-HIST as the learner: m = o^R)
    def oR(r):
        z = sum(R.joint(r).values())
        vals = [R.assess(r)]
        for t in ("R", "S"):
            tot = Fr(0)
            for x in range(6):
                r2 = (r[0], r[1] + ((t, x),)); tot += R.joint(r2)[R.decision(r2)]
            vals.append(tot / z)
        return vals
    cls = {}
    for r in received_histories(6, 1):
        if len(r[1]) != 2 or r[1][1][0] != "R": continue
        c = "CON" if r[1][0][1] == r[1][1][1] else "DIS"; m = mass_R(R, r); mv = oR(r)
        for sp in ("E" if split_E_R(r) else "I", "ALL"):
            d = cls.setdefault((sp, c), {"w": Fr(0), "m": [Fr(0)] * 3, "q": Fr(0), "pF": Fr(0), "vec": {}, "n": 0})
            d["w"] += m; d["n"] += 1
            for a in range(3): d["m"][a] += m * mv[a]
            d["q"] += m * (0 if R.act(r) == "P" else 1) if not SMOKE else 0
            d["pF"] += m * R.pF1(r)
            for kk, x in R.posterior_vec(r).items(): d["vec"][kk] = d["vec"].get(kk, 0) + m * x
    cm = {}
    for (sp, c), d in sorted(cls.items()):
        cm[f"{sp}/{c}"] = {"states": d["n"], "mass": S(d["w"]), "mean_m_P": S(d["m"][0] / d["w"]), "mean_m_R": S(d["m"][1] / d["w"]),
                           "mean_m_S": S(d["m"][2] / d["w"]), "checking_rate": S(d["q"] / d["w"]), "mean_P(F=1|R)": S(d["pF"] / d["w"]),
                           "floats": [fl(d["m"][0] / d["w"]), fl(d["q"] / d["w"]), fl(d["pF"] / d["w"])]}
    W["class_means_stage2_after_RECHECK_on_R"] = cm
    con = {}
    for sp in ("E", "I", "ALL"):
        a, b = cls[(sp, "CON")], cls[(sp, "DIS")]
        diff = a["m"][0] / a["w"] - b["m"][0] / b["w"]
        va = {k: x / a["w"] for k, x in a["vec"].items()}; vb = {k: x / b["w"] for k, x in b["vec"].items()}
        con[sp] = {"mbar_P_CON_minus_DIS": S(diff), "float": fl(diff), "B1_resolved_nonzero": diff != 0, "meets_mu_contrast_1/100": abs(diff) >= Fr(1, 100),
                   "selfassess_CON_minus_DIS_sign_ok": diff > 0, "checking_DIS_minus_CON": S(b["q"] / b["w"] - a["q"] / a["w"]),
                   "checking_sign_ok": (b["q"] / b["w"] - a["q"] / a["w"]) > 0, "donor_L1": S(sum(abs(va[k] - vb[k]) for k in va)), "donor_vectors_identical": va == vb}
        print(name, "contrast", sp, con[sp]["float"], con[sp]["checking_DIS_minus_CON"])
    W["contrast"] = con
    # ---- CF1a decomposition on R (stages 1-3)
    dO_c = {}; ss_c = {}
    def dO(N, s):
        if (N, s) not in dO_c:
            p1 = 1; p0 = 1
            for y in s: p1 *= enum(y, 1, N); p0 *= enum(y, 0, N)
            dO_c[(N, s)] = 1 if p1 > p0 else 0
        return dO_c[(N, s)]
    def SS(N, s, Y):
        if (N, s, Y) not in ss_c: ss_c[(N, s, Y)] = sum(enum(y2, Y, N) for y2 in range(6) if dO(N, s + (y2,)) == Y)
        return ss_c[(N, s, Y)]
    rows = []
    kev = 2 if SMOKE else 3
    for r in received_histories(6, kev - 1):
        N, reads = r; k = len(reads); types = [t for t, _ in reads]; recs = [x for _, x in reads]
        idx = []; c = -1
        for t in types:
            if t in ("F", "S"): c += 1
            idx.append(c)
        ns = c + 1; Wt = WP = WS = 0
        for s in itertools.product(range(6), repeat=ns):
            for Y in (0, 1):
                pe = 1
                for y in s: pe *= enum(y, Y, N)
                if not pe: continue
                for F in (0, 1):
                    ql = 1
                    for i in range(k): ql *= qnum(recs[i], s[idx[i]], F)
                    if not ql: continue
                    w = pe * (3 if F == 0 else 1) * ql; Wt += w
                    if dO(N, s) == Y: WP += w
                    WS += w * SS(N, s, Y)
        o = [Fr(WP, Wt), Fr(WP, Wt), Fr(WS, 24 * Wt)]
        orr = oR(r); m = mass_R(R, r)
        rows.append({"k": k, "split": "E" if split_E_R(r) else "I", "w": m * Fr(1, 2 ** (k - 1)), "dF": [orr[a] - o[a] for a in range(3)]})
    cf = {}
    for sp in ("E", "I"):
        num = den = div = Fr(0); signed = [Fr(0)] * 3
        for x in rows:
            if x["split"] != sp: continue
            num += x["w"] * sum(d * d for d in x["dF"]) / 3; den += x["w"]
            if max(abs(d) for d in x["dF"]) >= Fr(1, 20): div += x["w"]
            for a in range(3): signed[a] += x["w"] * x["dF"][a]
        D2 = num / den; Mf = div / den
        cf[sp] = {"D_F": math.sqrt(fl(D2)), "D_F^2": S(D2), "M_F": S(Mf), "M_F_float": fl(Mf),
                  "mean_signed_DeltaF_P_R_S": [fl(v / den) for v in signed], "lambda_RHIST": "0 identically (m = o^R for R-HIST)",
                  "CF1a_holds_at_1/20": D2 >= Fr(1, 400) and Mf >= Fr(1, 20)}
        print(name, "CF1a", sp, cf[sp]["D_F"], cf[sp]["M_F_float"])
    W["CF1a_decomposition_on_R"] = cf
    return W

out["worlds"]["v2_PROPOSED_kappa0_1/16"] = run_world("v2", Fr(1, 16))
out["worlds"]["DIAG_kappa0_0_target_on_R"] = run_world("diag0", Fr(0))
try:
    v1 = json.load(open("../N2_output.json"))["CF1a_reference_attainability"]
    out["v1_reference_on_H_for_comparison"] = {k: v["D_div"] for k, v in v1.items()}
except Exception as e:
    out["v1_reference_on_H_for_comparison"] = str(e)
out["elapsed_s"] = round(time.time() - t0, 3)
json.dump(out, open("N2_v2_output_smoke.json" if SMOKE else "N2_v2_output.json", "w"), indent=1, default=str)
print("N2 v2 DONE elapsed", out["elapsed_s"])
