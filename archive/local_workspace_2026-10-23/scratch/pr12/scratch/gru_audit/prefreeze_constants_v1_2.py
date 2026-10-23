"""Outcome-blind constants for spec v1.2: W2 certificate q/P only, input bits only. Loads no checkpoint. Run with python3 -B."""
import hashlib, itertools, json, subprocess
from fractions import Fraction as F
import numpy as np
raw = subprocess.run(["git", "-C", "/workspace/repo", "show", "origin/pr/10:twostream_results_v1/results.json"], capture_output=True, check=True).stdout
assert hashlib.sha256(raw).hexdigest().startswith("bf2de92c")
cert = json.loads(raw)
P = np.zeros(256); Q = np.zeros((256, 3))
for row in cert["per_history"]:
    h = int(row["history"]); mx = F(row["marginal_x"]["exact"]); my = F(row["marginal_y"]["exact"]); c = F(row["covariance"]["exact"])
    P[h] = float(F(row["probability"]["exact"])); Q[h] = [float(mx), float(my), float(mx + my - 2 * (mx * my + c))]
R_or = float(np.sum(P[:, None] * Q * (1 - Q)))
mu = P @ Q; Vq = float(np.sum(P[:, None] * (Q - mu) ** 2))
out = {"R_oracle": R_or, "floor": 0.01 * R_or, "Var_w_q": Vq, "dR2_floor": 0.01 * R_or / Vq}
# B_in+ rank per fold fit set (inputs only).
bits = np.array([[(h >> t) & 1 for t in range(8)] for h in range(256)], float); r = 2 * bits - 1
Bin = np.column_stack([r] + [r[:, i] * r[:, j] for i, j in itertools.combinations(range(8), 2)])
FX, FY = 0x55, 0xAA
orb4 = sorted({frozenset((p ^ g) & 15 for g in (0, FX, FY, FX ^ FY)) for p in range(16)}, key=min)
grp = np.array([next(i for i, o in enumerate(orb4) if (h & 15) in o) for h in range(256)])
folds = [((0, 1), (2, 3)), ((2, 3), (0, 1)), ((0, 2), (1, 3)), ((1, 3), (0, 2)), ((0, 3), (1, 2)), ((1, 2), (0, 3))]
names = ["AB", "CD", "AC", "BD", "AD", "BC"]
rk = {}
for nm, (fit, _) in zip(names, folds):
    m = np.isin(grp, fit); w = P[m] / P[m].sum(); X = Bin[m]
    mu_x = w @ X; sd = np.sqrt(w @ (X - mu_x) ** 2); keep = sd > 1e-12
    Z = (X[:, keep] - mu_x[keep]) / sd[keep]; A = np.sqrt(w)[:, None] * Z
    s = np.linalg.svd(A, compute_uv=False); tol = s[0] * max(A.shape) * np.finfo(float).eps
    rk[nm] = {"zero_var": int((~keep).sum()), "kept": int(keep.sum()), "rank": int((s > tol).sum()), "cond_kept": float(s[0] / s[-1])}
out["Bin_plus_fit_rank"] = rk
print(json.dumps(out, indent=1))
