"""N1: exact support-mass and split-mass enumeration for spec v1 §7 and §12.2.
World + fault law only. No learner, no network."""
import json, sys, time
from fractions import Fraction as Fr
from acq_model import *

SMOKE = "--smoke" in sys.argv
M = graded_model(); t0 = time.time()
S_MIN, N_MIN, NH_MIN, DEC_MIN = Fr(1, 100), 32, 4, 72
res = {"mode": "SMOKE" if SMOKE else "PRIMARY", "checks": []}
def chk(name, value, expect=None, cond=None):
    ok = (value == expect) if expect is not None else bool(cond)
    res["checks"].append({"name": name, "value": str(value), "expect": None if expect is None else str(expect), "pass": ok})
    print(("PASS " if ok else "FAIL ") + name + ": " + str(value) + ("" if expect is None else "  (expect " + str(expect) + ")"))

kmax_stage = 2 if SMOKE else 3
# --- stage-level totals, split masses (§6.3, §7)
dec = {"I": {"samples": 0, "H": 0}, "E": {"samples": 0, "H": 0}}
for k in range(1, kmax_stage + 1):
    nH = 0; nS = 0; split = {}; cue = {}
    prefix_mass = {}
    for H in world_histories(M, k):
        nH += 1; sp = "E" if split_E(H) else "I"
        pH = H["pY"][0] + H["pY"][1]
        for F, rec, w in latent_patterns(M, H):
            nS += 1
        # P(N) * P(samples | N); pY includes P(Y)
        mass = Fr(1, 2) * pH
        split[sp] = split.get(sp, 0) + mass
        cue[(H["N"], sp)] = cue.get((H["N"], sp), 0) + mass
        prefix_mass[H["types"]] = prefix_mass.get(H["types"], 0) + mass
        dec[sp]["H"] += 1
        dec[sp]["samples"] += sum(1 for _ in latent_patterns(M, H))
    exp_H = {1: 12, 2: 84, 3: 588}[k]; exp_S = {1: 84, 2: 3108, 3: 127596}[k]
    chk(f"stage{k} world histories", nH, exp_H)
    chk(f"stage{k} positive-weight samples", nS, exp_S)
    for p, m in prefix_mass.items():
        chk(f"stage{k} prefix {''.join(p) or '-'} total law mass (do-space)", m, Fr(1))
    np = len(prefix_mass)
    chk(f"stage{k} split S_E mass per do-space", split["E"] / np, Fr(1, 2))
    chk(f"stage{k} split S_I mass per do-space", split["I"] / np, Fr(1, 2))
    for N in CUES:
        chk(f"stage{k} cue {N}: S_E mass / cue mass", cue[(N, "E")] / (cue[(N, "E")] + cue[(N, "I")]), Fr(1, 2))
    # spec §6.3 prefix weight 4^-(k-1): total pooled weight across prefixes
    tot_spec = sum(m * Fr(1, 4 ** (k - 1)) for m in prefix_mass.values())
    res.setdefault("prefix_weight_note", {})[f"stage{k}"] = {"n_prefixes": np, "sum_of_4^-(k-1)_weights": str(tot_spec)}
    chk(f"stage{k} spec §6.3 weight 4^-(k-1) normalizes to 1 over prefixes", tot_spec, Fr(1))

# --- stage-2 after RECHECK events (§10.3, §12.2) and K3 continuation events
ev = {}
for H in world_histories(M, 2):
    if H["types"] != ("R",): continue
    sp = "E" if split_E(H) else "I"; pH = Fr(1, 2) * (H["pY"][0] + H["pY"][1])
    for F, rec, w in latent_patterns(M, H):
        cls = "CON" if rec[0] == rec[1] else "DIS"
        d = ev.setdefault((sp, cls), {"mass": Fr(0), "samples": 0, "H": set(), "recv": set(), "k3_samples": 0, "k3_mass": Fr(0)})
        d["mass"] += pH * w; d["samples"] += 1; d["H"].add((H["N"], H["samples"])); d["recv"].add((H["N"], rec))
        # forced RECHECK at stage 2 -> stage-3 read of the same sample
        y = H["samples"][0]
        for r3 in range(6):
            p3 = M["q"](r3, y, F)
            if p3: d["k3_samples"] += 1; d["k3_mass"] += pH * w * p3
hand = {("E", "DIS"): (Fr(35, 768), 180, 6, 1080), ("E", "CON"): (Fr(349, 768), 42, 6, 222)}
hand[("I", "DIS")] = hand[("E", "DIS")]; hand[("I", "CON")] = hand[("E", "CON")]
res["events"] = {}
for key in sorted(ev):
    d = ev[key]; hm, hs, hh, hk = hand[key]; tag = f"{key[0]}/{key[1]}"
    chk(f"stage2|R {tag} mass vs hand", d["mass"], hm)
    chk(f"stage2|R {tag} samples vs hand", d["samples"], hs)
    chk(f"stage2|R {tag} world histories vs hand", len(d["H"]), hh)
    chk(f"K3 {tag} x forced RECHECK x y3 mass vs hand", d["k3_mass"], hm)
    chk(f"K3 {tag} x forced RECHECK x y3 samples vs hand", d["k3_samples"], hk)
    chk(f"stage2|R {tag} threshold (i) mass >= 1/100", d["mass"], cond=d["mass"] >= S_MIN)
    chk(f"stage2|R {tag} threshold (ii) samples >= 32", d["samples"], cond=d["samples"] >= N_MIN)
    chk(f"stage2|R {tag} threshold (iii) world histories >= 4", len(d["H"]), cond=len(d["H"]) >= NH_MIN)
    chk(f"K3 {tag} threshold (ii) samples >= 32", d["k3_samples"], cond=d["k3_samples"] >= N_MIN)
    res["events"][tag] = {"mass": str(d["mass"]), "samples": d["samples"], "world_H": len(d["H"]),
                          "distinct_received_states": len(d["recv"]), "k3_samples": d["k3_samples"], "k3_mass": str(d["k3_mass"])}
    print(f"INFO {tag} distinct received recipient states: {len(d['recv'])}")
# P(DIS | H) for every stage-2|R world history
pdis = set()
for H in world_histories(M, 2):
    if H["types"] != ("R",): continue
    pdis.add(sum(w for F, rec, w in latent_patterns(M, H) if rec[0] != rec[1]))
chk("P(DIS | H) identical for all 12 stage-2|R world histories", sorted(map(str, pdis)), ["35/384"])

# --- decoder pooled S_I (iv)
if not SMOKE:
    chk("decoder S_I world histories stages 1-3", dec["I"]["H"], 342)
    chk("decoder S_I positive-weight samples stages 1-3", dec["I"]["samples"], 65394)
    chk("decoder S_I threshold (iv) samples per action >= 72", dec["I"]["samples"], cond=dec["I"]["samples"] >= DEC_MIN)
    res["decoder"] = dec
# --- received histories (compiled domain)
nR = sum(1 for _ in received_histories(6, 1 if SMOKE else 3))
chk("received histories stages 1-4 (compiled domain)", nR, 156 if SMOKE else 22620)
res["elapsed_s"] = round(time.time() - t0, 3)
res["n_fail"] = sum(1 for c in res["checks"] if not c["pass"])
json.dump(res, open("N1_output_smoke.json" if SMOKE else "N1_output.json", "w"), indent=1, default=str)
print("N1 DONE fails:", res["n_fail"], "elapsed", res["elapsed_s"])
