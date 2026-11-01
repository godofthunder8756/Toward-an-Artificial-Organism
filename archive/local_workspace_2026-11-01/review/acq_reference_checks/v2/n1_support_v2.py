"""N1 v2: exact support and split masses on received states R (spec v2 §6.3, §7, §12.2).
World + fault law only (PROPOSED phi=1/4, kappa=1/4, kappa_0=1/16). No learner, no network."""
import json, sys, time
from fractions import Fraction as Fr
from acq_model_v2 import *

SMOKE = "--smoke" in sys.argv; t0 = time.time()
M = graded_model(Fr(1, 16)); R = Ref(M)
res = {"mode": "SMOKE" if SMOKE else "PRIMARY", "kappa0": "1/16", "checks": [], "events": {}}
def chk(name, value, expect=None, cond=None):
    ok = (value == expect) if expect is not None else bool(cond)
    res["checks"].append({"name": name, "value": str(value), "expect": None if expect is None else str(expect), "pass": ok})
    print(("PASS " if ok else "FAIL ") + name + ": " + str(value) + ("" if expect is None else "  (expect " + str(expect) + ")"))

top = 2 if SMOKE else 4
states = {}
for r in received_histories(6, top - 1):
    states[r] = mass_R(R, r)
kcount = {}
for r, m in states.items():
    k = len(r[1]); kcount[k] = kcount.get(k, 0) + 1
for k in range(1, top + 1):
    chk(f"stage{k} distinct received states", kcount[k], {1: 12, 2: 144, 3: 1728, 4: 20736}[k])
chk("all received states have positive law mass", min(states.values()) > 0, True)
# F=0-only reachability (kappa_0 > 0)
pos0 = all(sum(sum(R.alpha(r)[(Y, 0)]) for Y in (0, 1)) > 0 for r in states)
chk("all received states reachable under F=0 alone (kappa_0>0)", pos0, True)
for k in range(1, min(top, 3) + 1):
    byp = {}; split = {}; cue = {}
    for r, m in states.items():
        if len(r[1]) != k: continue
        p = tuple(t for t, _ in r[1][1:]); byp[p] = byp.get(p, 0) + m
        sp = "E" if split_E_R(r) else "I"
        split[(p, sp)] = split.get((p, sp), 0) + m
        cue[(p, r[0], sp)] = cue.get((p, r[0], sp), 0) + m
    for p, m in byp.items():
        chk(f"stage{k} prefix {''.join(p) or '-'} mass", m, Fr(1))
        chk(f"stage{k} prefix {''.join(p) or '-'} S_E mass", split[(p, "E")], Fr(1, 2))
        for N in CUES:
            chk(f"stage{k} prefix {''.join(p) or '-'} cue {N} S_E/cue", cue[(p, N, "E")] / (cue[(p, N, "E")] + cue[(p, N, "I")]), Fr(1, 2))
    chk(f"stage{k} weight 2^-(k-1) normalizes over prefixes", sum(Fr(1, 2 ** (k - 1)) for _ in byp), Fr(1))
    nE = sum(1 for r in states if len(r[1]) == k and split_E_R(r)); nI = sum(1 for r in states if len(r[1]) == k and not split_E_R(r))
    chk(f"stage{k} states per split equal", (nE, nI), ({1: 6, 2: 72, 3: 864}[k],) * 2)
# events
hand = {"DIS": (Fr(1025, 12288), 30, (15, 15), 180, (90, 90)), "CON": (Fr(5119, 12288), 6, (3, 3), 36, (18, 18))}
classF = {}
for sp in ("E", "I"):
    for cls in ("CON", "DIS"):
        rec = [r for r in states if len(r[1]) == 2 and r[1][1][0] == "R" and split_E_R(r) == (sp == "E") and ((r[1][0][1] == r[1][1][1]) == (cls == "CON"))]
        m = sum(states[r] for r in rec); percue = tuple(sum(1 for r in rec if r[0] == N) for N in CUES)
        recset = set(rec)
        k3 = [r for r in states if len(r[1]) == 3 and r[1][2][0] == "R" and (r[0], r[1][:2]) in recset] if not SMOKE else []
        k3m = sum(states[r] for r in k3); k3cue = tuple(sum(1 for r in k3 if r[0] == N) for N in CUES)
        hm, hn, hc, hk, hkc = hand[cls]; tag = f"{sp}/{cls}"
        chk(f"stage2|R {tag} mass vs hand", m, hm)
        chk(f"stage2|R {tag} distinct states vs hand", len(rec), hn)
        chk(f"stage2|R {tag} states per cue (lo,hi) vs hand", percue, hc)
        chk(f"stage2|R {tag} (i) mass >= 1/100", m, cond=m >= Fr(1, 100))
        chk(f"stage2|R {tag} (ii) >=4 states and >=1 per cue", len(rec), cond=len(rec) >= 4 and min(percue) >= 1)
        ev = {"mass": str(m), "mass_float": float(m), "distinct_states": len(rec), "states_per_cue_lo_hi": percue}
        if not SMOKE:
            chk(f"K3 {tag} stage-3 states vs hand", len(k3), hk)
            chk(f"K3 {tag} states per cue vs hand", k3cue, hkc)
            chk(f"K3 {tag} mass vs hand", k3m, hm)
            chk(f"K3 {tag} (ii) >=4 states and >=1 per cue", len(k3), cond=len(k3) >= 4 and min(k3cue) >= 1)
            ev.update({"k3_states": len(k3), "k3_states_per_cue": k3cue, "k3_mass": str(k3m)})
        res["events"][tag] = ev
        for r in rec:
            pf = R.pF1(r); classF.setdefault(cls, [Fr(0), Fr(0)]); classF[cls][0] += states[r] * pf; classF[cls][1] += states[r]
chk("P(F=1 | DIS) vs hand", classF["DIS"][0] / classF["DIS"][1], Fr(112, 205))
chk("P(F=1 | CON) vs hand", classF["CON"][0] / classF["CON"][1], Fr(976, 5119))
if not SMOKE:
    nI = sum(1 for r in states if len(r[1]) <= 3 and not split_E_R(r))
    chk("decoder S_I distinct states stages 1-3", nI, 942)
    chk("decoder (iii) S_I states >= 38", nI, cond=nI >= 38)
    chk("decoder S_I states per cue", tuple(sum(1 for r in states if len(r[1]) <= 3 and not split_E_R(r) and r[0] == N) for N in CUES), (471, 471))
    chk("compiled domain states stages 1-4", len(states), 22620)
res["elapsed_s"] = round(time.time() - t0, 3); res["n_fail"] = sum(1 for c in res["checks"] if not c["pass"])
json.dump(res, open("N1_v2_output_smoke.json" if SMOKE else "N1_v2_output.json", "w"), indent=1, default=str)
print("N1 v2 DONE fails:", res["n_fail"], "elapsed", res["elapsed_s"])
