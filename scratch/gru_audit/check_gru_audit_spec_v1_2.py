"""Checks for gru_own_error_audit_spec_v1_2.md. Outcome-blind: loads no checkpoint; reads the W2
certificate and source files via read-only `git show`. Run with python3 -B."""
import hashlib, itertools, json, math, re, subprocess, sys
from fractions import Fraction as F
import numpy as np
REV = "/workspace/review/"
SPEC = REV + "gru_own_error_audit_spec_v1_2.md"
ASTRA = "/workspace/astra_consult32_response.txt"
REPO = "/workspace/repo"
fails = []
def ok(c, m):
    print(("PASS " if c else "FAIL ") + m)
    if not c: fails.append(m)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
git = lambda ref: subprocess.run(["git", "-C", REPO, "show", ref], capture_output=True, check=True).stdout
spec = open(SPEC, encoding="utf-8").read()
# 1. Input hashes and untouched earlier files.
H = {ASTRA: "99378f762fe2a21ae519b1a8368ab52b48339cba9e2477c94884cf49f9f7df7b",
     REV + "gru_own_error_audit_spec_v1_1.md": "4661a8895ef495c28a1a41ff7405f029ff3c9f4451a12b1a1af9ccc701641ccf",
     REV + "gru_own_error_audit_spec_v1.md": "c0fad75a18b867622b75187a75a023f8c6684a02822ee2771292b268d61452a1",
     REV + "gru_own_error_audit_spec_v1_review.md": "f6b2db6f210c5b77006bed5fdbb1c4b7c973a8a3b26408c700af819511363127",
     REV + "gru_own_error_audit_spec_v1_1_review_addendum.md": "721100d105daad4547fecc2a7e32172139744c5c0708a3b534832910d4c7d023",
     REV + "gru_own_error_audit_review_erratum_c32.md": "4a5ad4f360e36750cea46fb8e6782f8e4cdf94b98bcd2d339d98d1e7323e2c78",
     REV + "PI_STANDING_APPROVAL_2026-10-21_1515.md": "5cc6f12a91d09c274a03a7c4045b4a15302f694d8f2ce056ab8a30ea5f15a7ba",
     REV + "gru_own_error_audit_roster_v1.json": "7ad145b4384d3ba615c35187358236dc633918efc530b681c567e4c306c4cab3",
     "/workspace/scratch/gru_audit/check_gru_audit_spec.py": "d244911344d1c523773ea493de5f807dc72d500058a3c4e6acf398afaf80e660",
     "/workspace/scratch/gru_audit/check_gru_audit_spec_v1_1.py": "e25a403a7c922831139bd19f9fcefcfd96d1eefe9c6162d7e271505744a36ec8",
     "/workspace/scratch/gru_audit/prefreeze_constants_v1_2.py": "d2a1735e8cad8ed8bff5002670bf9d28dcc971af6eae1cefa9bc9ae327dc6cef",
     "/workspace/scratch/gru_audit/prefreeze_constants_v1_2.json": "430d56c90937a336e865719c36b9dffe5e68e7949a4de3894c39a46067a2bb37"}
for p, h in H.items(): ok(sha(p) == h, "sha %s" % p.split("/")[-1])
for p, h in list(H.items())[:8]:
    ok(h[:8] in spec, "spec cites %s… for %s" % (h[:8], p.split("/")[-1]))
# 2. Verbatim Astra quotes.
L = open(ASTRA, encoding="utf-8", newline="").read().splitlines(); L = [x.rstrip("\r") for x in L]
ok(len(L) == 227, "Astra #32 has 227 lines")
E = {1: 190, 2: 193, 3: 196, 4: 199, 5: 202, 6: 205, 7: 208, 8: 211, 9: 214, 10: 217}
for k, ln in E.items():
    ok(L[ln - 2].strip() == "E32-%d:" % k, "E32-%d header at L%d" % (k, ln - 1))
    m = re.search(r"\*\*E32-%d\*\* \(L%d\): (\".*\")\n\*Met by\*" % (k, ln), spec)
    ok(m is not None and m.group(1) == L[ln - 1].strip(), "E32-%d verbatim from L%d, followed by 'Met by'" % (k, ln))
ok(("> " + L[222].strip()) in spec, "§9 claim ceiling verbatim (L223)")
ok(("> " + L[30].strip()) in spec, "primary question verbatim (L31)")
for ln in (1, 96, 106):
    ok(L[ln - 1].strip() in spec, "full-line quote L%d" % ln)
for ln, frag in [(225, "The Research Lead should attach the existing standing approval to the revised, reviewed and frozen specification, roster and implementation manifest."), (227, "v1.1 remains unapproved for execution.")]:
    ok(frag in L[ln - 1] and ('"' + frag + '"') in spec, "sentence quote L%d" % ln)
for ln, frag in [(133, '"PR #5: MISSING PERSISTED CHECKPOINTS; NOT EVALUATED."'), (137, "available persisted checkpoints from PRs #7-#10"),
                 (141, "f_init can be described as a frozen random recurrent core with a trained readout."),
                 (142, "R-FIX has frozen W_hh with other core parameters and the readout trained. Its entire recurrent core is not frozen."),
                 (110, "can remain a descriptive replication requirement on top of the effect floor"),
                 (53, "a stronger named input benchmark, not a complete representation of all functions of history"),
                 (86, 'does not divide variance into "shared task content" and "predictor-specific content."'),
                 (185, "not permission to reduce the analysis in place")]:
    ok(frag in L[ln - 1] and frag in spec, "fragment verbatim from L%d" % ln)
# 3. Withdrawn claims not relied on; erratum cited with A2.
ok("A2" in spec and all("4a5ad4f3" in spec[max(0, m.start() - 400): m.start() + 400] for m in re.finditer(r"\bA2\b", spec)), "every A2 mention cites erratum 4a5ad4f3 nearby")
ok("It is a double dissociation" not in spec and "**not called a double dissociation**" in spec, "no double-dissociation claim")
ok("does not make τ_fq a universal ceiling" in spec and "not used" in spec, "τ_fq not a ceiling; 2√s not used")
ok("s_PQ ≥ ½" in spec and "**removed as an admission gate**" in spec, "correlation F0 removed")
ok("sqrt(mu1_abs)" not in spec and "√μ1_abs" not in spec, "no √μ1_abs")
ok([m.group(0) for m in re.finditer(r".{0,40}conscious.{0,5}", spec, re.I)] == ["or anything about consciousness."] or all("anything about consciousness" in m.group(0) for m in re.finditer(r".{0,40}conscious.{0,5}", spec, re.I)), "consciousness appears only in the disclaimer")
# 4. Roster and pairs.
R = json.load(open(REV + "gru_own_error_audit_roster_v1.json"))
ok(R["counts"] == {"total": 290, "TRAINED": 230, "INIT": 60}, "roster 290/230/60")
from collections import Counter
tr = [r for r in R["roster"] if r["role"] == "TRAINED"]
blk = Counter((r["pr"], r["seed"]) for r in tr); arms = Counter((r["pr"], r["arm"]) for r in tr)
ok(sum(math.comb(n, 2) for n in blk.values()) == 1000, "within-seed pairs 1000")
ok(len(arms) == 23 and all(v == 10 for v in arms.values()) and sum(math.comb(v, 2) for v in arms.values()) == 1035, "23 (PR,arm) units × 10 seeds; cross-seed pairs 1035")
ok(sum(1 for r in tr if r["pr"] in (8, 9) and r["arm"] == "cand_final") == 20 and sum(1 for r in R["roster"] if r["pr"] in (8, 9) and r["arm"] == "cand_init") == 20, "20 + 20 PR#8/#9 cand checkpoints without source metric")
# 5. Groups, folds, prefix statement, inner orbits.
FX, FY = 0x55, 0xAA; G = [0, FX, FY, FX ^ FY]
orb = lambda p, k: frozenset((p ^ g) & ((1 << k) - 1) for g in G)
g4 = sorted({orb(p, 4) for p in range(16)}, key=min)
ok([sorted(o) for o in g4] == [[0, 5, 10, 15], [1, 4, 11, 14], [2, 7, 8, 13], [3, 6, 9, 12]], "groups A–D")
grp = np.array([next(i for i, o in enumerate(g4) if (h & 15) in o) for h in range(256)])
names = {"AB": (0, 1), "CD": (2, 3), "AC": (0, 2), "BD": (1, 3), "AD": (0, 3), "BC": (1, 2)}
folds = [("AB", "CD"), ("CD", "AB"), ("AC", "BD"), ("BD", "AC"), ("AD", "BC"), ("BC", "AD")]
def shared(k, fit, ev):
    m = (1 << k) - 1
    return {h & m for h in range(256) if grp[h] in names[fit]} & {h & m for h in range(256) if grp[h] in names[ev]}
ok(all(len(shared(k, f, e)) > 0 for f, e in folds for k in (1, 2)), "lengths 1–2 shared in every fold")
ok(all(len({orb(p, k) for p in range(1 << k)}) == 1 for k in (1, 2)), "lengths 1–2: single orbit ⇒ unavoidable under any whole-orbit holdout")
s3 = [len(shared(3, f, e)) > 0 for f, e in folds]
ok(sum(s3) == 4 and [f for (f, e), s in zip(folds, s3) if not s] == ["AC", "BD"], "length 3 shared in 4 folds; AC|BD folds share none")
o3 = sorted({orb(p, 3) for p in range(8)}, key=min)
ok(sorted(o3[0]) == [0, 2, 5, 7] and {h & 7 for h in range(256) if grp[h] in (0, 2)} == set(o3[0]), "A∪C = depth-3 orbit {0,2,5,7}")
ok(all(not shared(k, f, e) for f, e in folds for k in range(4, 9)), "lengths ≥4 never shared")
ok(all(sum(grp[h] in names[e] for _, e in folds) == 3 for h in range(256)), "each history evaluated 3 times ⇒ denominator 3·Σw")
g5 = {orb(p, 5) for p in range(32)}
ok(len(g5) == 8 and all(len({grp[p] for p in o}) == 1 for o in g5) and all(sum(1 for o in g5 if grp[min(o)] == i) == 2 for i in range(4)), "8 depth-5 orbits, 2 per group ⇒ 4 inner folds per fit set")
ok(all(sum(1 for h in range(256) if (h & 31) in o) == 32 for o in g5), "depth-5 orbit = 32 histories ⇒ inner fit 96, outer fit 128")
# 6. Constants from certificate.
raw = git("origin/pr/10:twostream_results_v1/results.json"); ok(hashlib.sha256(raw).hexdigest().startswith("bf2de92c"), "certificate sha")
P = np.zeros(256); Q = np.zeros((256, 3)); PF = []
for row in json.loads(raw)["per_history"]:
    h = int(row["history"]); mx = F(row["marginal_x"]["exact"]); my = F(row["marginal_y"]["exact"]); c = F(row["covariance"]["exact"])
    PF.append(F(row["probability"]["exact"])); P[h] = float(PF[-1]); Q[h] = [float(mx), float(my), float(mx + my - 2 * (mx * my + c))]
ok(sum(PF) == 1, "Σw = 1")
Ro = float(np.sum(P[:, None] * Q * (1 - Q))); Vq = float(np.sum(P[:, None] * (Q - P @ Q) ** 2))
ok("R_oracle = 0.582388" in spec and abs(Ro - 0.582388) < 5e-7, "R_oracle = %.6f" % Ro)
ok("Var_w(q) = 0.167612" in spec and abs(Vq - 0.167612) < 5e-7, "Var_w(q) = %.6f" % Vq)
ok("floor = 0.00582388" in spec and abs(0.01 * Ro - 0.00582388) < 5e-9, "floor 0.01·R_oracle")
ok("R²-gain floor = 0.034746" in spec and abs(0.01 * Ro / Vq - 0.034746) < 5e-7, "ΔR² floor = %.6f" % (0.01 * Ro / Vq))
mass = [round(float(P[grp == i].sum()), 3) for i in range(4)]
ok(mass == [0.319, 0.240, 0.241, 0.201] and "0.319 / 0.240 / 0.241 / 0.201" in spec, "carried support masses")
ok("7·10⁻⁴" in spec and "111–121" in spec, "carried CAND s100 and n_eff disclosures")
# 7. Feature counts and B_in+ rank (inputs only).
r = 2 * np.array([[(h >> t) & 1 for t in range(8)] for h in range(256)], float) - 1
Bin = np.column_stack([r] + [r[:, i] * r[:, j] for i, j in itertools.combinations(range(8), 2)])
ok(Bin.shape[1] == 36 and 6 + 36 + 8 == 50 and 6 + 8 == 14 and 6 + 36 == 42 and "**50**" in spec, "features 6/14/42/50")
ok(all(len({(r[h, 0] * r[h, 2], r[h, 1] * r[h, 3]) for h in range(256) if grp[h] == i}) == 1 for i in range(4)), "r0r2 and r1r3 constant within each group")
exp = {"AB": (1, 28), "CD": (1, 28), "AC": (1, 28), "BD": (1, 28), "AD": (0, 33), "BC": (0, 33)}
for nm, (z, rk) in exp.items():
    m = np.isin(grp, names[nm]); w = P[m] / P[m].sum(); X = Bin[m]; mu = w @ X; sd = np.sqrt(w @ (X - mu) ** 2); keep = sd > 1e-12
    A = np.sqrt(w)[:, None] * ((X[:, keep] - mu[keep]) / sd[keep]); s = np.linalg.svd(A, compute_uv=False)
    ok(int((~keep).sum()) == z and int((s > s[0] * max(A.shape) * np.finfo(float).eps).sum()) == rk, "B_in+ fit %s: zero-var %d, rank %d" % (nm, z, rk))
# 8. d-hat identity and reconstruction identity (synthetic numbers only).
rng = np.random.default_rng(1); f = rng.uniform(0.01, 0.99, (256, 3)); qh = rng.uniform(0, 1, (256, 3))
dh, d = f - qh, f - Q
ok(np.max(np.abs(((dh - d) ** 2).sum(1) - ((qh - Q) ** 2).sum(1))) < 1e-14, "Σ(d̂−d)² = Σ(q̂−q)² identity")
ok(np.max(np.abs(((f - Q) ** 2).sum(1) - (f * f - 2 * f * Q + Q * Q).sum(1))) < 1e-14, "known-coefficient reconstruction of e_P")
ok(F(56, 1024) == F(sum(math.comb(10, k) for k in (8, 9, 10)), 1024), "56/1024 arithmetic")
# 9. Source float64 path and field names (code/keys only).
m7 = git("origin/pr/7:recurrent_core_transfer_metrics.py").decode(); st7 = git("origin/pr/7:recurrent_core_transfer_study.py").decode()
ok("copied = eval_copy(model)" in m7 and ".double()" in git("origin/pr/7:recurrent_core_transfer_models.py").decode(), "PR#7 evaluate_arm/predict_histories use float64 eval_copy")
ok("criterion = probability_excess(preds, histories, world)[\"total\"]" in st7, "PR#7 sel criterion via predict_histories+probability_excess")
ok("eval_copy" in git("origin/pr/8:graded_reversion_eval.py").decode() and "from recurrent_core_transfer_metrics import evaluate_arm" in git("origin/pr/10:frozen_recurrent_compensation_eval.py").decode(), "PR#8 eval_copy; PR#10 evaluate_arm")
k7 = json.loads(git("origin/pr/7:recurrent_core_results_v1/seeds/s100.json"))
ok(all("errors" in k7[a] for a in ("cand", "f_init", "f_trained", "f_tuned32", "r_tuned843")) and "init_errors" in k7["cand"] and len(k7["selection"]["grid"]) == 9 and all("criterion" in g for g in k7["selection"]["grid"]), "PR#7 recorded field names present")
e8 = json.loads(git("origin/pr/8:graded_reversion_results_v1/seeds/s200.json"))["evaluation"]
ok("intact_outcomes" in e8 and "f_init_outcomes" in e8 and not any(k.startswith("cand") and "sha" not in k for k in e8) , "PR#8 fields: intact/f_init outcomes; no cand metric")
e9 = json.loads(git("origin/pr/9:first_order_control_results_v1/seeds/s300.json"))["evaluation"]
ok("intact_outcomes" in e9 and "f_init_outcomes" in e9, "PR#9 fields: intact/f_init outcomes")
r10 = json.loads(git("origin/pr/10:frozen_recurrent_compensation_results_v1/stage2/results.json"))["runs"]
ok(len(r10) == 30 and all("E1" in x[s] and "E2" in x[s] for x in r10 for s in ("init", "final")), "PR#10 E1+E2 for 30 init + 30 final")
# 10. Caps and runtime arithmetic.
caps = {"S0": 10, "P (primary C1/C2, TRAINED + INIT)": 15, "D (descriptive: uniform weights, T, summaries)": 20, "report": 5}
ok(sum(caps.values()) == 50 and all("| %s | %d min |" % (k, v) in spec for k, v in caps.items()) and "wall-clock" in spec, "caps sum to 50 wall-clock min")
fl = lambda n, ps: sum(4 * n * p * p for p in ps)
pf = fl(128, [6, 14, 42, 50]) + 4 * fl(96, [6, 14, 42, 50]); prim = 290 * 6 * pf; uni = 230 * 6 * pf
tt = 4300 * 6 * (fl(128, [6, 8, 15]) + 4 * fl(96, [6, 8, 15])); inf = 593920 * 816 + 74240 * 1540
ok(abs(pf - 9.2e6) / 9.2e6 < 0.01 and abs(prim - 1.6e10) / 1.6e10 < 0.01 and abs(uni - 1.27e10) / 1.27e10 < 0.01 and abs(tt - 1.7e10) / 1.7e10 < 0.02, "flop counts 9.2e6 / 1.6e10 / 1.27e10 / 1.7e10")
ok(290 * 4 * 6 * 5 == 34800 and 4300 * 3 * 6 * 5 == 387000 and abs(inf - 6e8) / 6e8 < 0.01, "SVD counts and inference flops")
opt = 2 * inf / 1e9 + 6 + prim / 1e9 + 1 + uni / 1e9 + tt / 1e9 + 12; con = 2 * inf / 1e8 + 6 + prim / 1e8 + 1 + uni / 1e8 + tt / 1e8 + 12
ok(abs(opt / 60 - 1.1) < 0.1 and abs(con / 60 - 8.2) < 0.15 and con / 60 < 50, "total %.1f–%.1f min < 50" % (opt / 60, con / 60))
ok((prim + 290 * 4 * 30 * 30e-6 * 1e8) / 1e8 / 60 < 15 and (uni + tt) / 1e8 / 60 + 12 / 60 < 20, "stage estimates under stage caps")
print("\n%d failure(s)" % len(fails)); sys.exit(1 if fails else 0)
