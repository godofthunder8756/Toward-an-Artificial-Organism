"""Summarize drain_by_body.json (cue-step split): per-seed sign tests. Post-hoc, disclosed."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from natural_by_rel import sign_p

d = json.load(open(os.path.join(HERE, "drain_by_body.json")))
S = sorted(d)
out = {}


def test(name, f):
    v = [f(d[s]) for s in S]
    v = [x for x in v if x is not None]
    nz = [x for x in v if x != 0]
    k = sum(x > 0 for x in nz)
    out[name] = {"positive": k, "n": len(nz), "sign_p": sign_p(k, len(nz)), "median": float(np.median(v))}
    print(f"{name}: {k}/{len(nz)} positive, p {sign_p(k, len(nz)):.2g}, median {np.median(v):.3f}")


def eff(r, a, s):
    return r[a]["effect"][s]


for a in ("PFATE", "PYOKED"):
    for s in ("UP", "FLAT", "DOWN"):
        test(f"{a}_{s}", lambda r, a=a, s=s: eff(r, a, s))
    test(f"{a}_UP_minus_DOWN", lambda r, a=a: None if None in (eff(r, a, "UP"), eff(r, a, "DOWN"))
         else eff(r, a, "UP") - eff(r, a, "DOWN"))
    out[f"{a}_shares_median"] = {s: float(np.median([d[x][a]["share"][s] for x in S])) for s in ("UP", "FLAT", "DOWN")}
    out[f"{a}_x_cue_median"] = float(np.median([d[x][a]["x_mean_clear"] for x in S]))
    out[f"{a}_x_shift_drained_vs_plain_median"] = float(np.median(
        [d[x][a]["x_probe_minus_cue_drained"] - d[x][a]["x_probe_minus_cue_plain"] for x in S]))
    print(a, out[f"{a}_shares_median"], "x_cue", round(out[f"{a}_x_cue_median"], 3),
          "drain-induced energy rise", round(out[f"{a}_x_shift_drained_vs_plain_median"], 4))
test("UP_PFATE_minus_PYOKED", lambda r: None if None in (eff(r, "PFATE", "UP"), eff(r, "PYOKED", "UP"))
     else eff(r, "PFATE", "UP") - eff(r, "PYOKED", "UP"))
test("DOWN_PYOKED_minus_PFATE", lambda r: None if None in (eff(r, "PFATE", "DOWN"), eff(r, "PYOKED", "DOWN"))
     else eff(r, "PYOKED", "DOWN") - eff(r, "PFATE", "DOWN"))
fz = json.load(open(os.path.join(HERE, "..", "scores.json")))["scores"]["points"]["3600"]["per_seed"]
f = np.array([fz[s]["drain_effect"]["PFATE"] for s in S])
y = np.array([d[s]["PFATE"]["drain_effect_all"] for s in S])
out["corr_with_frozen_drain_effect_PFATE"] = float(np.corrcoef(f, y)[0, 1])
print("corr with frozen per-seed PFATE drain effect", round(out["corr_with_frozen_drain_effect_PFATE"], 3))
json.dump(out, open(os.path.join(HERE, "drain_by_body_summary.json"), "w"), indent=1)
