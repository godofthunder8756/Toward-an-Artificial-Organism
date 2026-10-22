"""Arithmetic/anchor checks for gru_own_error_audit_spec_v1.md. Outcome-blind: loads no checkpoint.
Reads the W2 certificate via `git show` (read-only). Run with python3 -B."""
import hashlib, itertools, json, math, re, subprocess, sys
from fractions import Fraction as F
import numpy as np
SPEC = "/workspace/review/gru_own_error_audit_spec_v1.md"
ASTRA = "/workspace/astra_consult31_response.txt"
ROSTER = "/workspace/review/gru_own_error_audit_roster_v1.json"
REPO = "/workspace/repo"
fails = []
def ok(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: fails.append(msg)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
spec = open(SPEC, encoding="utf-8").read()
# 1. Verbatim Astra quotes.
ok(sha(ASTRA).startswith("b67ff37b55c5e21f"), "Astra #31 file sha")
lines = open(ASTRA, encoding="utf-8", newline="").read().splitlines()
for lab, ln in [("E31-2", 218), ("E31-3", 221), ("E31-4", 224), ("E31-5", 227), ("E31-6", 230), ("E31-7", 233), ("E31-8", 236), ("E31-9", 239)]:
    src = lines[ln - 1].strip()
    ok(lines[ln - 2].strip() == lab + ":", "%s header at L%d" % (lab, ln - 1))
    m = re.search(r"\*\*%s\*\* \(L%d\): (\".*\")" % (lab, ln), spec)
    ok(m is not None and m.group(1) == src, "%s quoted verbatim from L%d" % (lab, ln))
q204 = lines[203].strip()
ok(("> " + q204) in spec, "question quoted verbatim from L204")
for ln in (210, 247):
    frag = re.search(r'L%d says: (".*?")' % ln, spec)
    ok(frag is not None and frag.group(1).strip('"') in lines[ln - 1], "quote from L%d verbatim" % ln)
ok("sqrt(mu1_abs)" not in spec.replace(lines[217], "") and "√μ1_abs argument (erratum `967e99b4" in spec, "√μ1_abs not used except E31-2 quote / withdrawal note")
ok(sha("/workspace/review/acquired_self_correctness_spec_v2_delta_review_erratum_c31.md").startswith("967e99b4"), "erratum sha 967e99b4")
ok(sha("/workspace/review/PI_STANDING_APPROVAL_2026-10-21_1515.md") == "5cc6f12a91d09c274a03a7c4045b4a15302f694d8f2ce056ab8a30ea5f15a7ba", "approval record sha")
# 2. Roster arithmetic.
R = json.load(open(ROSTER))
ok(sha(ROSTER) == "7ad145b4384d3ba615c35187358236dc633918efc530b681c567e4c306c4cab3" and sha(ROSTER) in spec, "roster file sha in spec")
ok(R["counts"] == {"total": 290, "TRAINED": 230, "INIT": 60}, "roster counts 290/230/60")
ok(all(r["identical_at_later_heads"] for r in R["roster"]), "all files identical at later heads")
ok(len(R["missing"]) == 120 and all(m["pr"] == 5 for m in R["missing"]) and R["pr5_weight_files"] == [], "missing = 120 PR#5 runs, no PR#5 weight files")
from collections import Counter
tr = Counter((r["pr"], r["seed"]) for r in R["roster"] if r["role"] == "TRAINED")
pairs = sum(math.comb(n, 2) for n in tr.values())
ok(pairs == 1000 and math.comb(14, 2) == 91 and all(tr[(7, s)] == 14 for s in range(100, 110)), "pair family 910+30+30+30 = 1000")
ok(Counter(r["pr"] for r in R["roster"] if r["role"] == "TRAINED") == {7: 140, 8: 30, 9: 30, 10: 30}, "TRAINED per PR 140/30/30/30")
ok(sha("/workspace/scratch/gru_audit/inventory.py").startswith("bbdbcf1a"), "inventory script sha")
# 3. Groups / prefix consistency.
FX, FY = 0x55, 0xAA
Gp = [0, FX, FY, FX ^ FY]
def orbit(h, mask=0xFF): return frozenset((h ^ g) & mask for g in Gp)
orbits = {orbit(h) for h in range(256)}
ok(len(orbits) == 64 and all(len(o) == 4 for o in orbits), "64 terminal orbits of size 4")
for k in range(2, 9):
    ok(len({orbit(p, (1 << k) - 1) for p in range(1 << k)}) == 2 ** (k - 2), "prefix orbits at depth %d = 2^(k-2)" % k) if k in (3, 4) else None
k0 = 4
gorb = sorted({orbit(p, 15) for p in range(16)}, key=min)
ok([sorted(o) for o in gorb] == [[0, 5, 10, 15], [1, 4, 11, 14], [2, 7, 8, 13], [3, 6, 9, 12]], "groups A-D as listed")
group = {h: next(i for i, o in enumerate(gorb) if (h & 15) in o) for h in range(256)}
ok(all(len({group[x] for x in o}) == 1 for o in orbits), "groups are unions of whole terminal orbits")
ok(all(sum(group[h] == i for h in range(256)) == 64 for i in range(4)), "64 histories per group")
is_test = lambda h: ((h % 16) + (h // 16)) % 4 == 0
ok(all(sum(is_test(h) for h in range(256) if group[h] == i) == 16 for i in range(4)), "16 source-TEST histories per group")
bip = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
folds = [(a, b) for x, y in bip for a, b in ((x, y), (y, x))]
ok(len(folds) == 6 and all(sum(group[h] in e for _, e in folds) == 3 for h in range(256)), "6 folds; each history evaluated 3 times")
nb = sum(1 for c in itertools.combinations(range(4), 2) if 0 in c)
ok(nb == 3, "3 balanced bipartitions at k0=4 (k0=3 gives 1)")
def shared(L, fit, ev):
    pf = {h & ((1 << L) - 1) for h in range(256) if group[h] in fit}
    pe = {h & ((1 << L) - 1) for h in range(256) if group[h] in ev}
    return pf & pe
ok(all(not shared(L, f, e) for f, e in folds for L in range(4, 9)), "no prefix of length >=4 shared across fit/eval in any fold")
ok(all(shared(1, f, e) == {0, 1} for f, e in folds), "both length-1 prefixes shared in every fold (impossibility)")
ok(all(len({h & 1 for h in range(256) if group[h] == i}) == 2 for i in range(4)), "every group contains both length-1 prefixes")
# 4. W2 symmetry + support (exact, from certificate).
raw = subprocess.run(["git", "-C", REPO, "show", "origin/pr/10:twostream_results_v1/results.json"], capture_output=True, check=True).stdout
ok(hashlib.sha256(raw).hexdigest().startswith("bf2de92c"), "certificate file sha bf2de92c")
cert = json.loads(raw)
P = {}; Q = {}
for row in cert["per_history"]:
    h = int(row["history"]); mx = F(row["marginal_x"]["exact"]); my = F(row["marginal_y"]["exact"]); c = F(row["covariance"]["exact"])
    P[h] = F(row["probability"]["exact"]); Q[h] = (mx, my, mx + my - 2 * (mx * my + c))
ok(sum(P.values()) == 1, "sum P(h) = 1")
ok(all(P[h ^ FX] == P[h] and P[h ^ FY] == P[h] for h in range(256)), "P invariant under F_X, F_Y")
ok(all(Q[h ^ FX] == (1 - Q[h][0], Q[h][1], 1 - Q[h][2]) for h in range(256)), "F_X: q_X->1-q_X, q_Y fixed, q_XOR->1-q_XOR")
ok(all(Q[h ^ FY] == (Q[h][0], 1 - Q[h][1], 1 - Q[h][2]) for h in range(256)), "F_Y: q_Y->1-q_Y, q_XOR->1-q_XOR")
r = {h: sum(x * (1 - x) for x in Q[h]) for h in range(256)}
ok(all(r[h ^ g] == r[h] for h in range(256) for g in Gp), "oracle risk r is G-invariant")
def neff(S):
    w = [P[h] for h in S]; return float(sum(w) ** 2 / sum(x * x for x in w))
print("support: group mass", [round(float(sum(P[h] for h in range(256) if group[h] == i)), 6) for i in range(4)])
print("support: group n_eff", [round(neff([h for h in range(256) if group[h] == i]), 2) for i in range(4)])
fitn = [neff([h for h in range(256) if group[h] in f]) for f, _ in folds]
print("support: fold fit n_eff", [round(x, 2) for x in fitn], " total n_eff", round(neff(range(256)), 2))
ok(all(x > 10 for x in fitn), "F1 support condition: every fold fit n_eff > 10")
tl = cert["per_history"][0]
# 5. Sign test and threshold identities.
ok(F(sum(math.comb(10, k) for k in (8, 9, 10)), 1024) == F(56, 1024), "P(>=8/10 | 1/2) = 56/1024")
ok(abs(1 - (1 / math.sqrt(2)) ** 2 - 0.5) < 1e-15, "s=1/2 <=> |c|=1/sqrt2")
# 6. Ceiling |tau| <= 2 sqrt(1-c^2) for in-sample weighted LS with intercept (synthetic data only).
rng = np.random.default_rng(0); worst = -1.0
for _ in range(3000):
    n = 64; w = rng.dirichlet(np.ones(n)); W = np.sqrt(w)[:, None]
    def proj(X):
        X = np.column_stack([np.ones(n), X]); A = W * X; Qm, _ = np.linalg.qr(A); return Qm @ Qm.T
    def R2(Pm, y):
        yc = np.sqrt(w) * (y - np.sum(w * y)); one = np.sqrt(w)
        Py = Pm @ (np.sqrt(w) * y); res = np.sqrt(w) * y - Py
        return 1 - res @ res / (yc @ yc)
    SP, SQ = rng.normal(size=(n, 8)), rng.normal(size=(n, 8))
    base = rng.normal(size=n); eP = base + rng.normal(size=n) * rng.uniform(0, 2); eQ = base + rng.normal(size=n) * rng.uniform(0, 2)
    eP += SP[:, 0] * rng.uniform(0, 3); eQ += SQ[:, 0] * rng.uniform(0, 3)
    PP, PQ = proj(SP), proj(SQ)
    tau = (R2(PP, eP) - R2(PQ, eP)) + (R2(PQ, eQ) - R2(PP, eQ))
    mP, mQ = np.sum(w * eP), np.sum(w * eQ)
    c = np.sum(w * (eP - mP) * (eQ - mQ)) / math.sqrt(np.sum(w * (eP - mP) ** 2) * np.sum(w * (eQ - mQ) ** 2))
    worst = max(worst, abs(tau) - 2 * math.sqrt(max(0.0, 1 - c * c)))
    # input-only identity: same features for both brackets -> tau = 0
    PI = proj(rng.normal(size=(n, 8)))
    ti = (R2(PI, eP) - R2(PI, eP)) + (R2(PI, eQ) - R2(PI, eQ))
    assert ti == 0.0
ok(worst <= 1e-12, "ceiling |tau| <= 2 sqrt(1-c^2) holds on 3000 synthetic cases (max excess %.2e)" % worst)
ok(True, "input-only features give tau_in == 0 exactly (3000 cases)")
# 7. Budget.
caps = {"S0": 10, "F0": 10, "F1+T": 25, "report": 5}; cum = 50
ok(sum(caps.values()) == cum and "**50 min**" in spec and all("| %s | %d min |" % (k, v) in spec for k, v in caps.items()), "stage caps sum to binding cumulative cap 50")
ok(290 * 256 * 8 == 593920, "0.6 M GRU steps")
fits = 1000 * 6 * 10 + 230 * 6 * 7
ok(6e4 < fits < 8e4, "~7e4 ridge solves (%d)" % fits)
# 9. Inherited constants exist in PR #7 spec module.
src = subprocess.run(["git", "-C", REPO, "show", "origin/pr/7:recurrent_core_transfer_spec.py"], capture_output=True, check=True).stdout.decode()
for pat in ["EPS0 = 1e-12", "RIDGE_LAMBDA = 1e-3", "SHOWN_MIN = 8", "CONTINUATION_STAGES = (4, 5, 6, 7)", "EARLY_STAGES = (0, 1, 2, 3)", "INPUT_SIZE = 9", "HIDDEN = 8"]:
    ok(pat in src, "inherited constant: " + pat)
proto = subprocess.run(["git", "-C", REPO, "show", "origin/pr/10:TWOSTREAM_PROTOCOL_v1.md"], capture_output=True, check=True).stdout.decode().splitlines()
ok("flipping every X reading sends" in proto[400] and "(μ_x, -μ_y, -κ)" in proto[402], "TWOSTREAM_PROTOCOL L401-403 flip identities")
ok(subprocess.run(["git", "-C", REPO, "diff", "--quiet", "origin/pr/7", "origin/pr/10", "--", "recurrent_core_transfer_models.py"]).returncode == 0, "models.py identical PR7..PR10")
# 8. Repo cleanliness: no new __pycache__ created by this script (it imports nothing from repo).
print("\n%d failure(s)" % len(fails)); sys.exit(1 if fails else 0)
