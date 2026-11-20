"""P1c post-hoc (disclosed, exploratory): natural abstention on clear trials by implied reliability,
PFATE against PYOKED, per seed, from raw.json. PYOKED replays PFATE's evaluation gains, so the two arms
meet overwrites with the same probabilities, but only PFATE's body predicts them.
Low reliability = r < 0.6 (bins [0.3, 0.6) and [0, 0.3) pooled; reporting loses there).
Two-sided exact sign test, ties dropped."""
import json, os
from math import comb
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def sign_p(k, n):
    if n == 0:
        return 1.0
    t = min(k, n - k)
    return min(1.0, 2 * sum(comb(n, i) for i in range(t + 1)) / 2 ** n)


def pool(b, ix):
    nn = sum(b[i]["n"] for i in ix)
    return None if nn == 0 else sum(b[i]["abstain"] * b[i]["n"] for i in ix if b[i]["n"]) / nn


def main():
    r = json.load(open(os.path.join(HERE, "..", "raw.json")))
    out = {}
    for pt in r["meta"]["points"]:
        rows = []
        for sd in r["seeds"]:
            P = [p for p in sd["points"] if p["iters"] == pt][0]["natural"]
            rows.append({a: (pool(P[a]["probes"]["clear_by_rel"], [0]), pool(P[a]["probes"]["clear_by_rel"], [2, 3]))
                         for a in ("PFATE", "PYOKED")})
        res = {}
        for name, f in (("abstain_low_rel", lambda t: t[1]), ("abstain_rel_1", lambda t: t[0]),
                        ("discrimination", lambda t: t[1] - t[0])):
            d = [f(x["PFATE"]) - f(x["PYOKED"]) for x in rows
                 if None not in x["PFATE"] and None not in x["PYOKED"]]
            nz = [v for v in d if v != 0]
            k = sum(v > 0 for v in nz)
            res[name] = {"pfate_ahead": k, "n": len(nz), "sign_p": sign_p(k, len(nz)),
                         "median_difference": float(np.median(d)),
                         "median_PFATE": float(np.median([f(x["PFATE"]) for x in rows if None not in x["PFATE"]])),
                         "median_PYOKED": float(np.median([f(x["PYOKED"]) for x in rows if None not in x["PYOKED"]]))}
            print(pt, name, {k2: round(v, 4) if isinstance(v, float) else v for k2, v in res[name].items()})
        out[str(pt)] = res
    json.dump(out, open(os.path.join(HERE, "natural_by_rel.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
