"""N2: exact reference checks for spec v1 §12.4 at the PROPOSED v1 values (costs 1/100, 3/50).
Reference = R-HIST (exact Bayes over received history, world + fault law). Oracle = world-model
Bayes on clean world samples. Exact rationals. No learner, no network, no training."""
import json, sys, time, math
from fractions import Fraction as Fr
from acq_model import *

SMOKE = "--smoke" in sys.argv; t0 = time.time()
out = {"mode": "SMOKE" if SMOKE else "PRIMARY", "costs": {"R": "1/100", "S": "3/50"}, "phi": "1/4", "kappa": "1/4"}
S = lambda x: str(x)
fl = lambda x: float(x)

# ---------- Part A: Appendix A binary world, exact
B = binary_model(); RB = Ref(B)
appA = {}
for N in CUES:
    r1s = [(N, (("F", x),)) for x in (0, 1)]
    pred = sum(RB.joint(r)[0] + RB.joint(r)[1] for r in r1s)  # =1
    acc_now = sum(max(RB.joint(r).values()) for r in r1s)
    def acc_after(types):
        tot = Fr(0)
        for recs in itertools.product((0, 1), repeat=len(types) + 1):
            r = (N, tuple(zip(("F",) + types, recs))); tot += max(RB.joint(r).values())
        return tot
    appA[N] = {"received_accuracy_p_N": S(acc_now), "after_1_RECHECK": S(acc_after(("R",))),
               "after_1_RESAMPLE": S(acc_after(("S",))), "after_2_RECHECK": S(acc_after(("R", "R"))),
               "gain_2_RECHECK": S(acc_after(("R", "R")) - acc_now),
               "stage1_Q": {str(x): {a: S(v) for a, v in RB.Q((N, (("F", x),))).items()} for x in (0, 1)},
               "stage1_optimal_action": {str(x): RB.act((N, (("F", x),))) for x in (0, 1)}}
# does the binary reference ever check anywhere on its optimal path / any history?
any_check = [r for r in received_histories(2, KMAX - 1 if not SMOKE else 0) if len(r[1]) <= KMAX and RB.act(r) != "P"]
appA["n_histories_where_optimal_action_is_check"] = len(any_check)
appA["hand_values"] = {"p_lo": "0.85", "p_hi": "0.675", "2RECHECK_lo": "0.86875", "2RECHECK_hi": "0.684375", "2c_R": "0.02"}
out["appendixA_binary"] = appA
print("AppA:", json.dumps({N: {k: appA[N][k] for k in ("received_accuracy_p_N", "after_1_RECHECK", "after_1_RESAMPLE", "after_2_RECHECK", "stage1_optimal_action")} for N in CUES}))
print("AppA histories where checking optimal:", len(any_check))

# ---------- Part B: graded world, R-HIST profitability (§12.4 a)
M = graded_model(); R = Ref(M, kmax=1 if SMOKE else KMAX)
st1 = {}
for N in CUES:
    for y in range(6):
        r = (N, (("F", y),)); qs = R.Q(r)
        st1[f"{N},y~={y+1}"] = {"Q": {a: S(v) for a, v in qs.items()}, "gain_R": S(qs["R"] - qs["P"]), "gain_S": S(qs["S"] - qs["P"]),
                                 "gain_R_float": fl(qs["R"] - qs["P"]), "gain_S_float": fl(qs["S"] - qs["P"]), "act": R.act(r)}
out["graded_stage1_received"] = st1
for k, v in st1.items(): print("stage1", k, v["act"], "gainR=%.6f gainS=%.6f" % (v["gain_R_float"], v["gain_S_float"]))
# per world history (N,y1): probability the first optimal action is R / S
pw = {}
for N in CUES:
    for y in range(6):
        pR = sum(M["q"](rec, y, F) * (PHI if F else 1 - PHI) for F in (0, 1) for rec in range(6) if R.act((N, (("F", rec),))) == "R")
        pS = sum(M["q"](rec, y, F) * (PHI if F else 1 - PHI) for F in (0, 1) for rec in range(6) if R.act((N, (("F", rec),))) == "S")
        pw[f"{N},y1={y+1}"] = {"P(first=RECHECK)": S(pR), "P(first=RESAMPLE)": S(pS)}
out["graded_stage1_world_first_action"] = pw
# optimal-policy rollout: probabilities of actions, expected payoff vs always-predict
def rollout():
    rate = {"R": Fr(0), "S": Fr(0)}; ev = Fr(0); never = Fr(0)
    for N in CUES:
        for y1 in range(6):
            r = (N, (("F", y1),)); j = R.joint(r); p0 = Fr(1, 2) * (j[0] + j[1])
            stack = [(r, p0)]
            while stack:
                r, p = stack.pop(); a = R.act(r)
                if a == "P": continue
                rate[a] += p
                for _, r2, pn in R.next_probs(r, a):
                    if pn: stack.append((r2, p * pn))
            never += p0 * R.assess(r)
            ev += p0 * R.V(r)
    return rate, ev, never
rate, ev, never = rollout()
out["graded_optimal_policy"] = {"expected_number_RECHECK": S(rate["R"]), "expected_number_RESAMPLE": S(rate["S"]),
                                "value_optimal": S(ev), "value_always_predict": S(never), "value_gain": S(ev - never),
                                "floats": [fl(rate["R"]), fl(rate["S"]), fl(ev), fl(never)]}
print("policy:", out["graded_optimal_policy"]["floats"])
cnt = {"P": 0, "R": 0, "S": 0}
for r in received_histories(6, (1 if SMOKE else KMAX) - 1):
    cnt[R.act(r)] += 1
out["graded_optimal_action_counts_stages_1_to_%d" % (1 if SMOKE else KMAX)] = cnt
print("action counts over received histories at decision stages:", cnt)
# oracle (clean evidence) stage-1 Q: RECHECK = PREDICT - c_R exactly; RESAMPLE via clean DP
def oracle_V(N, samples, k, kmax):
    pY = {Y: Fr(1, 2) * prod(M["e"](y, Y, N) for y in samples) for Y in (0, 1)}; z = pY[0] + pY[1]
    qP = max(pY.values()) / z
    if k > kmax: return qP, {"P": qP}
    qR = qP - C["R"]
    qS = -C["S"] + sum((Fr(1, 2) * sum(pY[Y] / Fr(1, 2) * M["e"](y2, Y, N) for Y in (0, 1)) / z) * oracle_V(N, samples + (y2,), k + 1, kmax)[0] for y2 in range(6))
    qs = {"P": qP, "R": qR, "S": qS}; return max(qs.values()), qs
orc = {}
for N in CUES:
    for y in range(6):
        v, qs = oracle_V(N, (y,), 1, 1 if SMOKE else KMAX)
        orc[f"{N},y1={y+1}"] = {a: S(x) for a, x in qs.items()} | {"act": next(a for a in PREF if qs[a] == v)}
out["oracle_stage1"] = orc

# ---------- Part C: m^ref_a(H), o_a(H) on world histories (§6.1/6.2 with R-HIST as the learner)
cache = {}
def mterms(rec_r, F, ycur, N):
    """For received history rec_r: per Y, P(post-action decision correct) for a in P,R,S, given F and current world sample."""
    key = (rec_r, F, ycur)
    if key in cache: return cache[key]
    d = R.decision(rec_r); res = {}
    for Y in (0, 1):
        mP = Fr(1 if d == Y else 0)
        mR = sum(M["q"](x, ycur, F) for x in range(6) if R.decision((rec_r[0], rec_r[1] + (("R", x),))) == Y)
        mS = sum(M["e"](y2, Y, N) * M["q"](x, y2, F) for y2 in range(6) for x in range(6) if R.decision((rec_r[0], rec_r[1] + (("S", x),))) == Y)
        res[Y] = (mP, mR, mS)
    cache[key] = res; return res
def odec(N, samples):
    pY = {Y: prod(M["e"](y, Y, N) for y in samples) for Y in (0, 1)}
    return 1 if pY[1] > pY[0] else 0
stats = {}
b1 = {}
kmax_eval = 2 if SMOKE else 3
for k in range(1, kmax_eval + 1):
    for H in world_histories(M, k):
        N = H["N"]; z = H["pY"][0] + H["pY"][1]; post = {Y: H["pY"][Y] / z for Y in (0, 1)}
        types = ("F",) + H["types"]; ycur = H["samples"][-1]
        m = [Fr(0)] * 3; cls_m = {"CON": [Fr(0), Fr(0)], "DIS": [Fr(0), Fr(0)]}
        for F, rec, w in latent_patterns(M, H):
            rr = (N, tuple(zip(types, rec))); t = mterms(rr, F, ycur, N)
            for a in range(3):
                m[a] += w * sum(post[Y] * t[Y][a] for Y in (0, 1))
        # oracle
        dO = odec(N, H["samples"]); oP = post[dO]
        oR = oP
        oS = sum(post[Y] * sum(M["e"](y2, Y, N) for y2 in range(6) if odec(N, H["samples"] + (y2,)) == Y) for Y in (0, 1))
        o = [oP, oR, oS]
        sp = "E" if split_E(H) else "I"; massH = Fr(1, 2) * z
        stats.setdefault(k, []).append({"N": N, "types": H["types"], "samples": H["samples"], "split": sp, "mass": massH, "m": m, "o": o})
        if k == 2 and H["types"] == ("R",):
            for F, rec, w in latent_patterns(M, H):
                c = "CON" if rec[0] == rec[1] else "DIS"
                for key in (sp, "ALL"):
                    d = b1.setdefault((key, c), {"w": Fr(0), "m": [Fr(0)] * 3, "A": Fr(0), "q": Fr(0), "pF": Fr(0), "vec": {}})
                    ww = massH * w; d["w"] += ww
                    for a in range(3): d["m"][a] += ww * m[a]
                    rr = (N, (("F", rec[0]), ("R", rec[1])))
                    d["A"] += ww * R.assess(rr); d["q"] += ww * (0 if R.act(rr) == "P" else 1) if not SMOKE else 0
                    d["pF"] += ww * R.pF1(rr)
                    for kk, x in R.posterior_vec(rr).items(): d["vec"][kk] = d["vec"].get(kk, 0) + ww * x
# B1 class means
b1out = {}
for (sp, c), d in sorted(b1.items()):
    b1out[f"{sp}/{c}"] = {"mass": S(d["w"]), "mean_m_P": S(d["m"][0] / d["w"]), "mean_m_R": S(d["m"][1] / d["w"]), "mean_m_S": S(d["m"][2] / d["w"]),
                         "mean_RHIST_self_assessment": S(d["A"] / d["w"]), "RHIST_checking_rate": S(d["q"] / d["w"]), "mean_P(F=1|recv)": S(d["pF"] / d["w"])}
out["B1_stage2_after_RECHECK_class_means"] = b1out
for sp in ("E", "I", "ALL"):
    con, dis = b1[(sp, "CON")], b1[(sp, "DIS")]
    diff = con["m"][0] / con["w"] - dis["m"][0] / dis["w"]
    vcon = {k: x / con["w"] for k, x in con["vec"].items()}; vdis = {k: x / dis["w"] for k, x in dis["vec"].items()}
    l1 = sum(abs(vcon[k] - vdis[k]) for k in vcon)
    out.setdefault("B1_contrast", {})[sp] = {"mbar_P_CON_minus_DIS": S(diff), "abs_ge_mu_contrast_1/100": abs(diff) >= Fr(1, 100),
        "donor_vector_L1(CON,DIS)_RHIST_posterior": S(l1), "donor_vectors_identical": l1 == 0,
        "selfassess_CON_minus_DIS": S(con["A"] / con["w"] - dis["A"] / dis["w"]),
        "checking_DIS_minus_CON": S(dis["q"] / dis["w"] - con["q"] / con["w"])}
    print("B1", sp, out["B1_contrast"][sp])
# CF1a attainability with R-HIST as the learner (S_E), weights as written (4^-(k-1)) and normalized (2^-(k-1))
for wname, wf in (("spec_v1_4^-(k-1)", lambda k: Fr(1, 4 ** (k - 1))), ("normalized_2^-(k-1)", lambda k: Fr(1, 2 ** (k - 1)))):
    for sp in ("E", "I"):
        num = Fr(0); den = Fr(0); div = Fr(0)
        for k, rows in stats.items():
            for r in rows:
                if r["split"] != sp: continue
                w = r["mass"] * wf(k); d = [r["m"][a] - r["o"][a] for a in range(3)]
                num += w * sum(x * x for x in d) / 3; den += w
                if max(abs(x) for x in d) >= Fr(1, 20): div += w
        Ddiv2 = num / den; Mdiv = div / den
        out.setdefault("CF1a_reference_attainability", {})[f"{wname}/{sp}"] = {"D_div^2": S(Ddiv2), "D_div": math.sqrt(fl(Ddiv2)), "M_div": S(Mdiv), "M_div_float": fl(Mdiv),
            "CF1a_holds(D_div>=1/20 and M_div>=1/20)": Ddiv2 >= Fr(1, 400) and Mdiv >= Fr(1, 20)}
        print("CF1a", wname, sp, math.sqrt(fl(Ddiv2)), fl(Mdiv))
out["elapsed_s"] = round(time.time() - t0, 3)
json.dump(out, open("N2_output_smoke.json" if SMOKE else "N2_output.json", "w"), indent=1, default=str)
print("N2 DONE elapsed", out["elapsed_s"])
