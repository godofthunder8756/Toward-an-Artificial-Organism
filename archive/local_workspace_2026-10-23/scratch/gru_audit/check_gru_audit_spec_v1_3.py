"""Checks for gru_own_error_audit_spec_v1_3.md (FINAL). Outcome-blind: loads no checkpoint, runs no
inference, computes no q-decoding loss. Reads the W2 certificate and source via read-only `git show`
and uses the 8 input bits only. Run with python3 -B."""
import hashlib, itertools, json, math, re, subprocess, sys
from fractions import Fraction as F
import numpy as np
REV = "/workspace/review/"; SCR = "/workspace/scratch/gru_audit/"
SPEC = REV + "gru_own_error_audit_spec_v1_3.md"
A33 = "/workspace/astra_consult33_response.txt"; A32 = "/workspace/astra_consult32_response.txt"
REPO = "/workspace/repo"
fails = []
def ok(c, m):
    print(("PASS " if c else "FAIL ") + m)
    if not c: fails.append(m)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
git = lambda ref: subprocess.run(["git", "-C", REPO, "show", ref], capture_output=True, check=True).stdout
spec = open(SPEC, encoding="utf-8").read()
# 1. Inputs and untouched earlier files.
H = {A33: "d98549a85bb2562a31a0e6f15dca072412beba09a47d255c2746f3f0d837981f",
     A32: "99378f762fe2a21ae519b1a8368ab52b48339cba9e2477c94884cf49f9f7df7b",
     REV + "gru_own_error_audit_spec_v1.md": "c0fad75a18b867622b75187a75a023f8c6684a02822ee2771292b268d61452a1",
     REV + "gru_own_error_audit_spec_v1_1.md": "4661a8895ef495c28a1a41ff7405f029ff3c9f4451a12b1a1af9ccc701641ccf",
     REV + "gru_own_error_audit_spec_v1_2.md": "8c81d32070ba12ef94af7adbc3d224661ae4c76ddacb7239d170564e2eb4fdcd",
     REV + "gru_own_error_audit_spec_v1_2_delta_review.md": "e8f28370eaf508909029c696d2428ed9419781eaa3157880e7604ce331276502",
     REV + "gru_own_error_audit_spec_v1_review.md": "f6b2db6f210c5b77006bed5fdbb1c4b7c973a8a3b26408c700af819511363127",
     REV + "gru_own_error_audit_spec_v1_1_review_addendum.md": "721100d105daad4547fecc2a7e32172139744c5c0708a3b534832910d4c7d023",
     REV + "gru_own_error_audit_review_erratum_c32.md": "4a5ad4f360e36750cea46fb8e6782f8e4cdf94b98bcd2d339d98d1e7323e2c78",
     REV + "PI_STANDING_APPROVAL_2026-10-21_1515.md": "5cc6f12a91d09c274a03a7c4045b4a15302f694d8f2ce056ab8a30ea5f15a7ba",
     REV + "gru_own_error_audit_roster_v1.json": "7ad145b4384d3ba615c35187358236dc633918efc530b681c567e4c306c4cab3",
     SCR + "check_gru_audit_spec.py": "d244911344d1c523773ea493de5f807dc72d500058a3c4e6acf398afaf80e660",
     SCR + "check_gru_audit_spec_v1_1.py": "e25a403a7c922831139bd19f9fcefcfd96d1eefe9c6162d7e271505744a36ec8",
     SCR + "check_gru_audit_spec_v1_2.py": "ac7b752a15f2e0e5bbc06a6cec6c23738b6d32953b707b1b5b9b2494780e18f3",
     SCR + "inventory.py": "bbdbcf1a39a5287f06fa27cfc55043e00993b3fd6d3277be01f6ff037c57cad4",
     SCR + "prefreeze_constants_v1_2.py": "d2a1735e8cad8ed8bff5002670bf9d28dcc971af6eae1cefa9bc9ae327dc6cef",
     SCR + "prefreeze_constants_v1_2.json": "430d56c90937a336e865719c36b9dffe5e68e7949a4de3894c39a46067a2bb37",
     "/workspace/scratch/gru_v12_delta/rank_check.py": "61a3e4243c45a897253022a3351c19c0f8aac6248faff6a775d5a11f9a64811d"}
for p, h in H.items(): ok(sha(p) == h, "sha unchanged: %s" % p.split("/")[-1])
for p in (A33, A32, REV + "gru_own_error_audit_spec_v1_2.md", REV + "gru_own_error_audit_spec_v1_2_delta_review.md", "/workspace/scratch/gru_v12_delta/rank_check.py"):
    ok(H[p][:8] in spec, "spec cites %s… (%s)" % (H[p][:8], p.split("/")[-1]))
ok(spec.startswith("# GRU hidden-state oracle-accessibility audit: specification v1.3 (FINAL)"), "title marked FINAL")
# 2. Verbatim Astra #33.
L = [x.rstrip("\r") for x in open(A33, encoding="utf-8", newline="").read().splitlines()]
ok(len(L) == 123, "Astra #33 has 123 lines")
ok(L[0] == "Verdict: FREEZE WITH NAMED EDITS." and '"Verdict: FREEZE WITH NAMED EDITS."' in spec, "verdict quoted verbatim (L1)")
for k in range(1, 11):
    ln = 86 + 3 * (k - 1)
    ok(L[ln - 2].strip() == "E33-%d:" % k, "E33-%d header at L%d" % (k, ln - 1))
    m = re.search(r"\*\*E33-%d\*\* \(L%d\): (\".*\")\n\*Met by\*" % (k, ln), spec)
    ok(m is not None and m.group(1) == L[ln - 1].strip(), "E33-%d verbatim from L%d, followed by 'Met by'" % (k, ln))
for nm, ln in (("Claim ceiling", 117), ("Qualification", 121)):
    ok(L[ln - 2].strip() == "" and L[ln - 3].strip().endswith(":"), "%s quote line L%d preceded by header" % (nm, ln))
    m = re.search(r"\*\*%s\*\* \(L%d\): (\".*\")\n\*Met by\*" % (nm, ln), spec)
    ok(m is not None and m.group(1) == L[ln - 1].strip(), "%s verbatim from L%d, followed by 'Met by'" % (nm, ln))
    ok(("> " + L[ln - 1].strip()) in spec, "%s block-quoted in §0" % nm)
L32 = [x.rstrip("\r") for x in open(A32, encoding="utf-8", newline="").read().splitlines()]
ok(L[116] == L32[222], "#33 ceiling identical to #32 L223")
for k in range(1, 11):
    ln = 190 + 3 * (k - 1)
    m = re.search(r"\*\*E32-%d\*\* \(#32 L%d\): (\".*\")\n\*Met by\*" % (k, ln), spec)
    ok(m is not None and m.group(1) == L32[ln - 1].strip(), "E32-%d verbatim from #32 L%d" % (k, ln))
for frag, ln in [("A gain over the fitted baseline does not necessarily improve on the original predictor's output.", 79),
                 ("describe feature-space geometry. They are not estimates of the fraction of C2 gain, prediction error or oracle information attributable to that geometry.", 17),
                 ("is not established without results", 33), ("not independently verified the artifacts or hashes", 5),
                 ("This clears the bounded oracle-accessibility audit, not the earlier own-error interpretation.", 5),
                 ("No duplicate approval question or further scientific review cycle is needed unless implementation introduces a substantive departure.", 123),
                 ("is not independent verification of the certificate", 81)]:
    ok(frag in L[ln - 1] and frag in spec, "fragment verbatim from #33 L%d" % ln)
for ln in (96, 106): ok(L32[ln - 1].strip() in spec, "#32 L%d full-line quote retained" % ln)
# 3. Items 2–10 present.
items = {
 "2 fixed λ primary": ["**λ = 1e-3 is fixed**", "normalized objective in Sec.5", "**230 TRAINED checkpoints only**", "**mismatched validation geometry**",
                        "**No direction of bias in the selected λ is asserted before the results are seen**", "all uniform-weight analyses and descriptive T", "**no meets-floor, below-floor or BOUNDARY label**"],
 "3 B_in+ kept; input-only losses declared": ["**All declared B_in+ features are retained**", "declared here, computed only after the freeze", "the pooled loss under the E32-7 denominator",
                        "**input-only B_in+ → q losses have not been computed**", "It is **not** described as outcome-blind merely because it needs no checkpoint"],
 "4 wording and diagnostics": ["**beyond the declared input baselines under this split**", "geometric diagnostics", "credited to the CNA delta review M1",
                        "**Centering:**", "**Scaling:**", "**Weighting:**", "**flag F1**"],
 "5 units and counts": ["**Claim-reporting unit: (PR, arm)", "**Integrity-failure unit: (PR, seed)**", "m = verified meets-floor", "b = verified below-floor",
                        "x = BOUNDARY", "u = UNRESOLVED", "i = INCOMPLETE/unfinished", "**Unresolved cases are never counted as below-floor**", "**All 23 are reported**"],
 "6 full precision + band": ["R_oracle = 0.5823877685694766", "Var_w(q) = 0.16761223143052342", "floor = 0.01·R_oracle = 0.005823877685694766",
                        "R²-gain floor = 0.034746137772820054", "**flag F6**", "Δ_c > floor + 1e-10 gives **meets-floor**", "Δ_c < floor − 1e-10 gives **below-floor**", "**BOUNDARY**", "display summaries only"],
 "7 replay label": ["**SOURCE-REPLAY UNAVAILABLE; INDEPENDENTLY VERIFIED (E33-6, L55).**", "**numerical forward agreement only**", "does **not** certify agreement with an unavailable historical metric"],
 "8 tolerances": ["**States and outputs must agree to max-abs ≤ 1e-10**", "**abs(a-b) <= 1e-12 + 1e-12*max(abs(a), abs(b))**", "All values must be finite"],
 "9 undefined / no clip / FQ": ["**UNDEFINED**", "are **not clipped**", "The **exact FQ reconstruction**", "The **fitted FQ regressions**", "never called exact reconstructions"],
 "10 INCOMPLETE, R_exc, caps": ["marked **INCOMPLETE**", "**the audit as a whole is not described as complete**", "R_exc(P) = Σ_h w(h)·e_P(h)",
                        "**50-minute cumulative wall-clock cap that includes setup and verification**", "One pinned CPU", "**4 GB address-space limit**", "Aggregate CPU time is reported"],
 "11 delta-review minors": ["**m1**", "**m2**", "**m3**", "**Astra is followed**", "is **not** adopted"],
 "12 open Qs, runtime, change log": ["**v1.2 open questions, all resolved by Astra #33.**", "**Carried forward", "## Change log from v1.2", "about 0.6 min optimistic and about 4.9 min conservative"],
}
for it, frags in items.items():
    miss = [f for f in frags if f not in spec]
    ok(not miss, "item %s present%s" % (it, "" if not miss else " — missing: %s" % miss))
ok(sum(1 for q in range(1, 8) if re.search(r"^%d\. .*\*\*resolved\*\*" % q, spec, re.M)) == 7, "v1.2 Q1–Q7 each marked resolved")
# 4. Constants at full precision from exact rationals.
raw = git("origin/pr/10:twostream_results_v1/results.json"); ok(hashlib.sha256(raw).hexdigest().startswith("bf2de92c"), "certificate sha")
PF, QF = [], []
for row in json.loads(raw)["per_history"]:
    mx = F(row["marginal_x"]["exact"]); my = F(row["marginal_y"]["exact"]); c = F(row["covariance"]["exact"])
    PF.append(F(row["probability"]["exact"])); QF.append((mx, my, mx + my - 2 * (mx * my + c)))
ok(sum(PF) == 1, "Σw = 1 (exact)")
RoF = sum(p * sum(q * (1 - q) for q in qs) for p, qs in zip(PF, QF))
mu = [sum(p * qs[j] for p, qs in zip(PF, QF)) for j in range(3)]
VqF = sum(p * sum((qs[j] - mu[j]) ** 2 for j in range(3)) for p, qs in zip(PF, QF))
J = json.load(open(SCR + "prefreeze_constants_v1_2.json"))
ok("R_oracle = " + repr(float(RoF)) in spec, "R_oracle full precision (exact rational) %r" % float(RoF))
ok(abs(float(RoF) - J["R_oracle"]) <= 2 * np.spacing(J["R_oracle"]) and abs(float(RoF / 100) - J["floor"]) <= 2 * np.spacing(J["floor"]), "v1.2 float-summed constants within ≤2 ulp of exact (flag F6)")
ok(float(VqF) == J["Var_w_q"] and "Var_w(q) = " + repr(float(VqF)) in spec, "Var_w(q) full precision %r" % float(VqF))
ok("floor = 0.01·R_oracle = " + repr(float(RoF / 100)) in spec, "floor full precision %r" % float(RoF / 100))
ok("R²-gain floor = " + repr(float(RoF / 100 / VqF)) in spec, "ΔR² floor full precision %r" % float(RoF / 100 / VqF))
ok(RoF + VqF == F(3, 4), "R_oracle + Var_w(q) = 3/4 exactly (consistency only)")
# 5. BOUNDARY band and quota logic on synthetic values.
fl = float(RoF / 100); g = 1e-10
lab = lambda d: "meets" if d > fl + g else ("below" if d < fl - g else "BOUNDARY")
ok([lab(fl + 2e-10), lab(fl - 2e-10), lab(fl), lab(fl + 5e-11)] == ["meets", "below", "BOUNDARY", "BOUNDARY"], "BOUNDARY band ±1e-10")
def quota(m, b, x, u, i):
    if m + b + x < 8: return "UNRESOLVED-insufficient"
    if m >= 8: return "attained"
    if m + u + i < 8: return "not-attained"
    return "UNRESOLVED-attainment"
ok(quota(7, 1, 0, 2, 0) == "UNRESOLVED-attainment" and quota(8, 0, 0, 2, 0) == "attained" and quota(5, 4, 1, 0, 0) == "not-attained" and quota(3, 3, 0, 4, 0) == "UNRESOLVED-insufficient", "quota rule incl. Astra L51 example")
# 6. CNA geometry diagnostics from bits only (no q, no checkpoint).
Hb = np.array([[(h >> k) & 1 for k in range(8)] for h in range(256)]); R = 2 * Hb - 1
X = np.hstack([R, np.stack([R[:, i] * R[:, j] for i, j in itertools.combinations(range(8), 2)], 1)]).astype(float)
p4 = Hb[:, :4] @ np.array([1, 2, 4, 8]); G = {'A': {0, 5, 10, 15}, 'B': {1, 4, 11, 14}, 'C': {2, 7, 8, 13}, 'D': {3, 6, 9, 12}}
grp = np.array([[k for k, v in G.items() if p in v][0] for p in p4]); geo = {}
for a, b in [('A', 'B'), ('C', 'D'), ('A', 'C'), ('B', 'D'), ('A', 'D'), ('B', 'C')]:
    m = np.isin(grp, [a, b]); Z = X[m]; keep = Z.std(0) > 1e-12; mu0 = Z[:, keep].mean(0)
    Zc = Z[:, keep] - mu0; Zh = X[~m][:, keep] - mu0; Pi = np.linalg.pinv(Zc) @ Zc
    geo[a + b] = round(float(np.linalg.norm(Zh - Zh @ Pi) / np.linalg.norm(Zh)), 3)
ok(all(geo[k] == 0.632 for k in ("AB", "CD", "AC", "BD")) and geo["AD"] == geo["BC"] == 0.408, "geometry diagnostics reproduced (unweighted, unscaled, fit-mean centered): %s" % geo)
ok("0.632" in spec and "0.408" in spec and "Frobenius norms" in spec, "diagnostics stated with statistic")
# 7. Runtime arithmetic, caps, features.
flp = lambda n, ps: sum(4 * n * p * p for p in ps); P4 = [6, 14, 42, 50]
inf = 593920 * 816 + 74240 * 1540; prim = 290 * 6 * flp(128, P4); inp = 6 * flp(128, [36])
sens = 230 * 6 * (4 * flp(96, P4) + flp(128, P4)); uni = 230 * 6 * flp(128, P4); T = 4300 * 6 * flp(128, [6, 8, 15])
nsvd = 290 * 6 * 4 + 6 + 230 * 6 * 4 * 5 + 230 * 6 * 4 + 4300 * 3 * 6
ok((290 * 6 * 4, 230 * 6 * 4 * 5, 230 * 6 * 4, 4300 * 3 * 6) == (6960, 27600, 5520, 77400) and all(s in spec for s in ("6,960 SVDs", "27,600 SVDs", "5,520 SVDs", "77,400 SVDs")), "SVD counts")
ok(abs(prim - 4.0e9) / 4e9 < 0.01 and abs(sens - 1.27e10) / 1.27e10 < 0.01 and abs(uni - 3.2e9) / 3.2e9 < 0.01 and abs(T - 4.3e9) / 4.3e9 < 0.01, "flop counts 4.0e9 / 1.27e10 / 3.2e9 / 4.3e9")
tot = lambda r, o: (2 * inf / r + 6 + (prim + inp + sens + uni + T) / r + nsvd * o) / 60
ok(abs(tot(1e9, 30e-6) - 0.6) < 0.05 and abs(tot(1e8, 300e-6) - 4.9) < 0.05 and tot(1e8, 300e-6) < 50, "total %.2f–%.2f min < 50" % (tot(1e9, 30e-6), tot(1e8, 300e-6)))
stP = (2 * inf / 1e8 + 6 + (prim + inp) / 1e8 + (6960 + 6) * 300e-6) / 60; stD = ((sens + uni + T) / 1e8 + (27600 + 5520 + 77400) * 300e-6) / 60
ok(stP < 15 and stD < 20, "stage P %.1f < 15, stage D %.1f < 20 min" % (stP, stD))
caps = {"S0": 10, "P (primary C1/C2, TRAINED + INIT, input-only B_in+ → q, R_exc)": 15, "D (descriptive: inner-λ sensitivity, uniform weights, T, summaries)": 20, "report": 5}
ok(sum(caps.values()) == 50 and all("| %s | %d min |" % (k, v) in spec for k, v in caps.items()), "caps sum to 50")
ok(X.shape[1] == 36 and "6 → 14" in spec and "42 → **50**" in spec, "features 6/14/42/50")
Rj = json.load(open(REV + "gru_own_error_audit_roster_v1.json"))
ok(Rj["counts"] == {"total": 290, "TRAINED": 230, "INIT": 60}, "roster 290/230/60")
# 8. Forbidden wording.
NEG = re.compile(r"\bnot\b|\bNever\b|\bnever\b|\bDo not\b", re.I)
def neg_only(phrase):
    lines = [ln for ln in spec.splitlines() if phrase.lower() in ln.lower()]
    return all(NEG.search(ln) for ln in lines), len(lines)
for ph in ("beyond the information in the inputs", "double dissociation", "rewards less regularization", "input-feature signal"):
    good, n = neg_only(ph); ok(good, "'%s' only in negated/prohibition lines (%d lines)" % (ph, n))
ok(all("not beyond the information in the inputs" in ln for ln in spec.splitlines() if "beyond the information in the inputs" in ln), "'beyond the information in the inputs' only as 'not beyond …' (E33-1 verbatim)")
ok(not re.search(r"autopoie", spec, re.I), "no autopoietic terms")
ok(len(list(re.finditer(r"conscious", spec, re.I))) == 1 and all("anything about consciousness" in m.group(0) for m in re.finditer(r".{0,40}conscious.{0,5}", spec, re.I)), "consciousness only in the disclaimer")
c4 = [ln for ln in spec.splitlines() if re.search(r"\bC4\b", ln)]
ok(all(NEG.search(ln) for ln in c4), "C4 only in negated lines (%d)" % len(c4))
ok("historically outcome-blind" in spec and all(NEG.search(ln) for ln in spec.splitlines() if "historically outcome-blind" in ln), "never called historically outcome-blind")
print("\n%d failure(s)" % len(fails)); sys.exit(1 if fails else 0)
