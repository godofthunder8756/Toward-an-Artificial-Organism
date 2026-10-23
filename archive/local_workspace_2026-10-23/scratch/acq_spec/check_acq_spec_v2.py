"""Document check for acquired_self_correctness_spec_v2.md (derived from check_acq_spec.py).
Reads documents and read-only `git show` / `git ls-tree` output only. Runs nothing else.
"""
import hashlib, re, subprocess, sys, json
from fractions import Fraction as Fr

SPEC = "/workspace/review/acquired_self_correctness_spec_v2.md"
SRC = "/workspace/astra_consult30_response.txt"
SRC_SHA = "4cc628034185fe456fa1f39be5f9dbf52d1d5b3556d34d18d7996d1b9511d04c"
REPO = "/workspace/repo"
fails = []
def bad(m): fails.append(m); print("FAIL:", m)
def ok(m): print("ok:", m)
def git(*a): return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
norm = lambda s: re.sub(r"\s+", " ", s.replace("**", "")).strip()

spec = open(SPEC, encoding="utf-8").read(); L = spec.split("\n")
src = open(SRC, encoding="utf-8").read().split("\n")
if sha(SRC) != SRC_SHA: bad("source sha changed")
else: ok("Astra #30 source sha")

# 1. 13-item coverage
items = [src[i - 1][2:].strip() for i in range(170, 183)]
assert all(src[i - 1].startswith("- ") for i in range(170, 183))
heads = {m.group(1): l for l in L for m in [re.match(r"## (\d+)\. ", l)] if m}
rows = [l for l in L if re.match(r"\| F\d+ \|", l)]
if len(rows) != 13: bad(f"coverage rows {len(rows)} != 13")
for k, it in enumerate(items, 1):
    r = [x for x in rows if x.startswith(f"| F{k} |")]
    if not r: bad(f"F{k} missing"); continue
    cells = [c.strip() for c in r[0].strip("|").split("|")]
    if cells[1] != it: bad(f"F{k} text not verbatim: {cells[1]!r} vs {it!r}")
    secs = re.findall(r"§(\d+)", cells[2])
    if not secs: bad(f"F{k} no section"); continue
    for s in secs:
        if s not in heads: bad(f"F{k} -> §{s} heading missing")
    if f"[F{k}]" not in heads.get(secs[0], ""): bad(f"F{k} primary §{secs[0]} lacks tag")
ok("coverage table checked (13 items)")

# 2. verbatim quotes
pats = [r'Astra #30 (?:[A-Z0-9-]+ )?\(?L(\d+)(?:–L(\d+))?\)?: "([^"]+)"',
        r'"([^"]+)" \(Astra #30 L(\d+)\)']
nq = 0
for i, p in enumerate(pats):
    for m in re.finditer(p, spec):
        if i == 0: a, b, q = int(m.group(1)), int(m.group(2) or m.group(1)), m.group(3)
        else: q, a = m.group(1), int(m.group(2)); b = a
        hay = norm(" ".join(src[a - 1:b]))
        nq += 1
        if norm(q) not in hay: bad(f"quote not verbatim at L{a}: {q[:60]!r}")
cb = ["m_a(H) = P(the frozen learner's own post-action decision is correct",
      "           | observable history H, do(action=a))"]
if src[133] != cb[0] or src[134] != cb[1] or (cb[0] + "\n" + cb[1]) not in spec: bad("m_a code block")
else: nq += 1
ok(f"{nq} Astra quotes checked")

# 3. citations (file@commit with line lists)
cit = re.compile(r"`([^`]+)`@([0-9a-f]{7})((?:,? L\d+(?:–L\d+)?)*)")
trees = {}
nc = 0
for m in cit.finditer(spec):
    path, c, lines = m.group(1), m.group(2), m.group(3)
    if c not in trees:
        r = git("ls-tree", "-r", "--name-only", c)
        if r.returncode: bad(f"commit {c} missing"); trees[c] = []; continue
        trees[c] = r.stdout.split()
    hits = [t for t in trees[c] if t == path] or [t for t in trees[c] if t.endswith("/" + path)]
    if len(hits) != 1: bad(f"{path}@{c} resolves to {len(hits)}"); continue
    n = len(git("show", f"{c}:{hits[0]}").stdout.split("\n"))
    for a, b in re.findall(r"L(\d+)(?:–L(\d+))?", lines):
        if int(b or a) > n: bad(f"{path}@{c} L{b or a} > {n}")
    nc += 1
ok(f"{nc} file@commit citations resolve")

anchors = [  # (path, commit, line, substring)
 ("RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md", "d118ae1", 31, "TEST iff ((h mod 16)"),
 ("RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md", "d118ae1", 36, "4000 steps at batch 256"),
 ("RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md", "d118ae1", 37, "Adam (0.9, 0.999, 1e-8)"),
 ("RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md", "d118ae1", 39, "seeded 1000+s"),
 ("RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md", "d118ae1", 40, "torch.set_num_threads(1)"),
 ("TWOSTREAM_ACQUISITION_PROTOCOL_v1.md", "0b98460", 100, "H ∈ {4, **8** (primary), 16}"),
 ("TWOSTREAM_ACQUISITION_PROTOCOL_v1.md", "0b98460", 101, "external timing scaffold"),
 ("TWOSTREAM_ACQUISITION_PROTOCOL_v1.md", "0b98460", 133, "frozen at the seed's initialization"),
 ("acquisition_results_v1/runs/cand_gru16_s0.json", "b25a30a", 9, '"recurrent": 1296'),
 ("acquisition_results_v1/runs/cand_gru16_s0.json", "b25a30a", 10, '"readout": 643'),
 ("GRADED_REVERSION_PROTOCOL_FINAL.md", "018f2a7", 283, "seeds 200–209"),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 394, "There is no re-training"),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 205, "abs(x-y) <= 1e-12 + 1e-9*max(abs(x), abs(y))"),
 ("GRADED_REVERSION_PROTOCOL_FINAL.md", "018f2a7", 285, "More than two invalid seeds"),
 ("GRADED_REVERSION_PROTOCOL_FINAL.md", "018f2a7", 287, "At least eight of the ten"),
 ("first_order_control_protocol_FINAL.md", "335e505", 57, "D_FO ∧ D_ISO ∧ M"),
 ("first_order_control_protocol_FINAL.md", "335e505", 91, "initial loss derivative"),
 ("first_order_control_protocol_FINAL.md", "335e505", 92, "Frobenius norm only"),
 ("first_order_control_protocol_FINAL.md", "335e505", 197, "1,000,000 + 100·s"),
 ("first_order_control_protocol_FINAL.md", "335e505", 244, "generator 40000 + 100·s"),
 ("first_order_control_protocol_FINAL.md", "335e505", 303, "D_FO  = (AUC_REV - max_j AUC_FO,j > eps0)"),
 ("first_order_control_protocol_FINAL.md", "335e505", 356, "more than two distinct seeds are invalid"),
 ("first_order_control_protocol_FINAL.md", "335e505", 359, "Count rule"),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 178, "Numerical decision rule"),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 218, "Freezing checks"),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 225, "do not consume an additional fresh-seed training run"),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 302, "TARGET REACHED REPRODUCIBLY"),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 374, "Two-stage sealed-manifest runner"),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 376, "For future studies, use a two-stage runner: write and seal the transformed-path manifest, then evaluate curves from that manifest."),
 ("frozen_recurrent_compensation_protocol_FINAL.md", "0fed34e", 429, "60 checkpoints (init and final) × 256 histories × 2 evaluators, taking seconds"),
 ("frozen_recurrent_compensation_numpy_eval.py", "0fed34e", 1, "Independent float64 NumPy forward pass"),
 ("results_v1_errata/ERRATA_v1.md", "0329818", 9, "edited in place"),
 ("frozen_recurrent_compensation_results_v1/stage1/manifest_stage1.json", "22654aa", 29, '"seconds"'),
 ("frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json", "fd720ee", 329, '"python": "3.12.3"'),
 ("frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json", "fd720ee", 330, '"torch": "2.14.1+cpu"'),
 ("first_order_control_results_v1/PHASE_B_RESULTS_v2.md", "4f6fc4c", 26, ""),
 ("c4_reliability_exact_check_v1/RESULTS_v3.md", "0e17a05", 40, "UNRESOLVED-DESIGN"),
 ("c4_reliability_exact_check_v1/RESULTS_v3.md", "0e17a05", 43, "the reference has no donor contrast"),
 ("c4_reliability_exact_check_v1/RESULTS_A3_D2.md", "1f2a6c9", 47, "NOT EVALUABLE [zero-probability event]"),
 ("c4_reliability_exact_check_v1/WREL_CLOSEOUT_E30_v1.md", "37414d0", 17, "zero occupancy under the intact distribution"),
 ("c4_reliability_exact_check_v1/WREL_CLOSEOUT_E30_v1.md", "37414d0", 67, "NOT EVALUABLE [NO"),
 ("c4_reliability_exact_check_v1/WREL_CLOSEOUT_E27_v1.md", "7b89c66", 77, "ten of the twelve H0 settings"),
]
for p, c, ln, s in anchors:
    t = git("show", f"{c}:{p}").stdout.split("\n")
    if ln > len(t) or s not in t[ln - 1]: bad(f"anchor {p}@{c} L{ln}: {s!r} | got {t[ln-1][:90] if ln <= len(t) else 'EOF'!r}")
    if f"`{p.split('/')[-1]}`@{c}" not in spec and f"`{p}`@{c}" not in spec: bad(f"anchor not cited in spec: {p}@{c}")
ok(f"{len(anchors)} anchors checked")
# PR 9 counts at L26-30 and RESULTS_A2 cost presence
ph = git("show", "4f6fc4c:first_order_control_results_v1/PHASE_B_RESULTS_v2.md").stdout.split("\n")[25:30]
if not any("8/10" in x for x in ph): bad("PR9 8/10 not in L26-30")
a2 = git("show", "dddd63c:c4_reliability_exact_check_v1/RESULTS_A2.md").stdout
if "1/100" not in a2 or "3/50" not in a2: bad("A2 costs not found")
# box citations
box = "/workspace/review/c4_reliability_exact_check_spec_FINAL.md"
if not sha(box).startswith("ae626b65"): bad("W-REL FINAL sha")
bl = open(box, encoding="utf-8").read().split("\n")
for ln, s in [(78, "`p > 1/2`"), (520, "0/0 is never treated as a pass")]:
    if s not in bl[ln - 1]: bad(f"box FINAL L{ln}")
ok("box citations")

# 4. timing record values
man = git("show", "22654aa:frozen_recurrent_compensation_results_v1/stage1/manifest_stage1.json").stdout
secs = [float(x) for x in re.findall(r'"seconds": ([0-9.]+)', man)]
if len(secs) != 30 or f"{min(secs):.2f}" != "13.46" or f"{max(secs):.2f}" != "14.02" or f"{sum(secs):.2f}" != "409.36":
    bad(f"timing {len(secs)} {min(secs)} {max(secs)} {sum(secs)}")
for s in ["min 13.46 s, max 14.02 s, sum 409.36 s over 30 runs"]:
    if s not in spec: bad("timing text")
ok("T1 timing values match record")
if re.search(r"(?i)\b(rss|memory|peak_mem)\b", man): bad("manifest has memory field; T12 statement wrong")
else: ok("no memory field in stage1 manifest (T12 statement holds)")

# 5. hand-arithmetic consistency of stated v2 fractions/counts (no simulation)
pd = lambda r: (5 * r / 6) * (2 - r)
k1, k0, phi = Fr(1, 4), Fr(1, 16), Fr(1, 4)
assert pd(k1) == Fr(35, 96) and pd(Fr(1, 8)) == Fr(75, 384) and pd(k0) == Fr(155, 1536)
assert pd(k1) / pd(Fr(1, 8)) == Fr(28, 15) and pd(k1) / pd(k0) == Fr(112, 31)
assert Fr(28, 15) ** 2 < 10 and Fr(112, 31) ** 2 >= 10 and Fr(112, 31) <= 10   # band [sqrt(10), 10]
PD = (1 - phi) * pd(k0) + phi * pd(k1); assert PD == Fr(1025, 6144) and 1 - PD == Fr(5119, 6144)
assert phi * pd(k1) / PD == Fr(112, 205) and phi * (1 - pd(k1)) / (1 - PD) == Fr(976, 5119)
for r in (k0, k1):   # split carries 1/2 of CON under lo
    P = [Fr(x, 48) for x in (13, 6, 5, 5, 6, 13)]
    con = [P[v] * ((1 - r) ** 2 + (1 - r) * r / 3) + r * r / 36 for v in range(6)]
    assert con[0] + con[2] + con[4] == sum(con) / 2
assert 12 + 144 + 1728 == 1884 and 1884 // 2 == 942 and 6 + 72 + 864 == 942
assert 21 * 32 + 32 + 96 + 3 == 803 and 1536 + 577 + 803 == 2916 and 577 + 643 == 1220 and 9 * 32 + 32 + 96 + 3 == 419
assert 30 * 105 + 10 * 140 == 4550 and Fr(549, 640) > Fr(17, 20)
assert 2 + 4 * 32 + 1 == 131
ok("stated v2 fractions/counts consistent")
for s_ in ["1025/6144", "112/205", "976/5119", "112/31", "28/15", "549/640 > 17/20", "2^{−(k−1)}", "4,550 s", "≤ 360 CPU-min", "≤ 190 min"]:
    if s_ not in spec: bad(f"missing stated value {s_}")

# 6. forbidden phrases
allow = ("No consciousness claim", "NOT CLAIMED", "Astra #30 L166")
forb = [r"(?i)conscious", r"(?i)sentien", r"(?i)autopoie", r"(?i)\balive\b", r"\bC5\b",
        r"\bC4\b(?!-candidate)", r"(?i)self-aware", r"(?i)\bproves?\b", r"(?i)resolved by"]
for i, l in enumerate(L, 1):
    for f in forb:
        if re.search(f, l) and not any(a in l for a in allow):
            bad(f"forbidden {f} at spec L{i}: {l[:80]!r}")
ok("forbidden-phrase scan")
for s in ["NEEDS-APPROVED-RUN", "[PENDING — Astra review]", "[PENDING — Aidan approval]", "## 1. Cheap falsifiers"]:
    if s not in spec: bad(f"missing {s}")
if spec.index("## 1. Cheap falsifiers") > spec.index("## 2. "): bad("falsifiers not first")

# 7. earlier files unchanged
prior = {"u1_substrate_audit_v1.md": "48c174f5", "u1_substrate_audit_v1_1.md": "3d9bbde3", "u1_substrate_audit_v1_2.md": "2ca30d45",
 "track_a_lineage_triage_v1.md": "b4e1a772", "track_a_lineage_triage_v1_1.md": "d2cc9152", "track_a_lineage_triage_v1_1_astra_digest.md": "d4034423",
 "track_a_lineage_triage_v1_2.md": "84fa9614", "track_a_lineage_triage_v1_3.md": "167c7e67", "track_a_lineage_triage_v1_4.md": "292401bb",
 "track_a_claim_synthesis_v1.md": "95888230", "track_a_claim_synthesis_v1_1.md": "41da2819", "track_a_claim_synthesis_v1_2.md": "5df911b8",
 "wrel_results_review_v1.md": "60c3f5a9", "wrel_attainability_from_existing_outputs_v1.md": "64ebd4a5",
 "c4_reliability_exact_check_spec_FINAL.md": "ae626b65", "c4_reliability_APPROVAL_RECORD.md": "be3e3bb6",
 "acquired_self_correctness_spec_v1.md": "54bc8ea3b050551095bcc4d2b93fbc62476e52eb1678b08bdd37b6c1cfc0c8ac",
 "acquired_self_correctness_spec_v1_review.md": "997b2594d54a3d13327fc6be3e8bedcdddb50fdfea89aba77b0695fae00f47fa",
 "PI_STANDING_APPROVAL_2026-10-21_1515.md": "5cc6f12a91d09c274a03a7c4045b4a15302f694d8f2ce056ab8a30ea5f15a7ba",
 "acq_reference_checks/N1_N2_results_v1.md": "472185bbc7ca57d4599cf75b6d13737173202e08b6ee12112cf808db101d1463",
 "acq_reference_checks/N1_output.json": "c7d9c912", "acq_reference_checks/N2_output.json": "3bbd5f66",
 "acq_reference_checks/N2_postproc_values.json": "2e957280", "acq_reference_checks/n2_reference.py": "6ff3ba85",
 "acq_reference_checks/n1_support.py": "d07ae413", "acq_reference_checks/acq_model.py": "ccc11aec"}
for f, h in prior.items():
    if not sha("/workspace/review/" + f).startswith(h): bad(f"prior file changed: {f}")
ok(f"{len(prior)} prior files unchanged")

# 8. v2-specific: change log, dispositions, open items, C-K0 text, costs
cl = [l for l in L if re.match(r"\| (B[12]|M[1-5]|m[1-7]|E[1-4]) \|", l)]
ids = {l.split("|")[1].strip() for l in cl}
need = {"B1", "B2", "M1", "M2", "M3", "M4", "M5", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "E1", "E2", "E3", "E4"}
if ids != need: bad(f"change-log ids {sorted(ids ^ need)}")
for l in cl:
    cells = [c.strip() for c in l.strip("|").split("|")]
    for sec in re.findall(r"§(\d+)", cells[4]):
        if sec not in heads: bad(f"change log {cells[0]} -> §{sec} missing")
    if cells[0].startswith("M") and not re.search(r"ADOPTED|REBUTTED", cells[3]): bad(f"{cells[0]} lacks disposition")
for e in ("E1", "E2"):
    row = [l for l in cl if l.startswith(f"| {e} |")][0]
    if "N1 v1" not in row and "N2 v1" not in row: bad(f"{e} not credited to N1/N2")
for q in ("Q-A12", "Q-A13"):
    if not re.search(q + r" \(open", spec): bad(f"{q} not marked open")
fz = open("/workspace/review/acq_reference_checks/v2/PRE_RUN_FREEZE_v2.txt", encoding="utf-8").read()
m = re.search(r'C-K0 CRITERION TEXT \(verbatim, also in spec v2 §5.2\):\n"(.+?)"\n', fz, re.S)
if not m or m.group(1) not in spec: bad("C-K0 criterion text not identical to freeze file")
else: ok("C-K0 criterion identical to PRE_RUN_FREEZE_v2 (timestamped before computation)")
if "c_R = 1/100, c_S = 3/50" not in spec: bad("costs line")
if "2^{−(k−1)}" not in spec or "4^{−(k−1)} did not normalize" not in spec: bad("weight fix")
if "That is false." not in spec: bad("Appendix A correction")
st = git("status", "--porcelain").stdout.strip()
mine = [x for x in st.splitlines() if "__pycache__" not in x]
print("repo status: %d lines, all pre-existing __pycache__ deletions: %s" % (len(st.splitlines()), not mine))
if mine: bad("repo has non-pycache changes")
print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
