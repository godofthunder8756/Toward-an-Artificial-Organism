# C-kappa class-fit close-out note (Research Delegate, additive)

Written 2026-10-23 (ET) for commit to PR #14 by the Research Lead. This note is additive: it edits no existing file, changes no sealed output, and records no new computation. The only numbers below are read from the committed results.json at PR #14 HEAD, plus simple arithmetic that is shown. Astra consult #40 governs. Where this note quotes Astra, the quotation is verbatim from the raw reply.

## 0. Sources (sha256)

| Source | Path | sha256 |
|---|---|---|
| Astra #40 raw reply (governs) | /workspace/astra_consult40_response.txt | b574b57fd4ef5ca9b242eff02589a2eb5f6ed545de15e0d867adc87de47868b1 |
| Astra consult digest (summary only; #40 entry at L135) | /workspace/astra_consult_1.md | c630fa1b95617b95a7ccc6046d4e94082979c0b73544838fa11c4433c91d167c |
| #40 packet body as sent (contains Section E) | /workspace/astra_serve40/c40_body.md | 414a36f66f9117d8109f9beabefac9ae1211762fa3b634d2ca69dedf5b66747d |
| #40 brief | /workspace/pending/astra_consult40_brief.DONE.md | c82dd2f59d8cde95c8f128d46b50d030d17b5078775f38ceccc58dd3db550e1b |
| PR #14 HEAD | commit "Record class-fit attempt 2." | cffe125bf50b9e16db36e071981a0642827c041e |
| Attempt-2 results | classfit_outputs/results.json @ cffe125b | 05385099c4f0b4a0ca0c71302abe42eabb4673d83f2f6c5236f6286cb82bfdd2 |
| Attempt-2 report | classfit_outputs/REPORT.md @ cffe125b | c755e5eaceed928c626f306d7efc21146b79f805fd62250d1d27017f283ea5db |
| Attempt-2 post-run index | classfit_post_run_index.json @ cffe125b | 4552b79426f73c8a9ff4bf1373e0f715aa737df69d1d66aa53af94a88edad79d |
| Re-sealed manifest | classfit_manifest.json @ cffe125b | e7a9d3a4... (prefix checked) |
| Delegate results review | /workspace/review/ckappa_classfit_results_review_RD.md | cabd7fae619b444571678a67d8ec27ffa7bd00d8251dfe9dd5c82fd5bad00c6f |
| Addendum 1 / RL-14 | /workspace/review/ckappa_classfit_application_v1_ADDENDUM_1.md (= review/ckappa_classfit/ckappa_classfit_application_v1_ADDENDUM_1_cb1b.md @ cffe125b) | 5f7e06e084e8da400e6c98f95b9e2f093cafcc5ba1fe1cd686c263e603ff4131 |
| Addendum 1 Note 1 | /workspace/review/ckappa_classfit_application_v1_ADDENDUM_1_NOTE_1.md (= ..._NOTE_1_003f.md @ cffe125b) | c05fdb5abb658a750669d0b2fe8fa36899ff68083b293fd2707cf125f5e5f9ff |
| Re-seal diff | review/ckappa_classfit/classfit_reseal_diff.txt @ cffe125b | 3967158da91abe4b... (prefix) |

All results.json values below come from `.pooled` rows at weighted mode (C3.10), eps_syn 0.1, unless marked otherwise. Each row is keyed by (system, fit_type, group, eps_syn, mode).

## 1. Programme decision (verbatim)

Astra #40, Q2, raw L35-37. The decision wording is recorded verbatim, including its second sentence:

> "NO-GO for advancing the present C-kappa class-conditioned design unchanged to a neural inference specification. CLASS-FIT VALIDATION MET, but the frozen SYS-PC headroom requirements were not met for either ALL or MARG under the governing weighted evaluation."

Check: the first sentence matches the Lead's assignment text character for character, apart from the closing quotation mark. Astra's "C-kappa" is ASCII, so the note keeps it in ASCII.

Result wording, raw L39-41, verbatim:

> "The declared class-conditioned-map intervention-prediction criterion was not met. Specifically, the synthetic headroom requirements failed; the implementation identities, including recovery of the declared sign-dependent synthetic map, passed."

**This is a programme decision, not a negative result about kappa or GRUs.** Astra, raw L33: "That supports the programme decision; it does not establish a scientific impossibility or a negative neural result." Under raw L45-51 and E38-15, the record may not infer that a GRU does not use or represent kappa; that covariance-sensitive computation is absent, unnecessary or irrelevant; that class-conditioned recovery is impossible; that any Q-tag received a negative result; or that the synthetic thresholds define an intrinsic boundary of neural feasibility. "The thresholds are frozen conventions, not discovered natural constants." (raw L53).

Stored labels, which this note does not change: VALIDATION = "CLASS-FIT VALIDATION MET"; HEADROOM ALL = "HEADROOM NOT MET"; HEADROOM MARG = "HEADROOM NOT MET". Astra confirmed all labels (raw L5-11).

## 2. Correction (a): SYS-LIM gains on their correct rows

Astra, raw L22: "Section E incorrectly pairs SYS-LIM's class R with its global gain."

From results.json `.pooled`, SYS-LIM, weighted, group ALL, eps_syn 0.1:

| SYS-LIM fit | R (results.json) | gain (results.json) | Astra #40 (raw L26-27) |
|---|---:|---:|---|
| global | 0.07987942230238854 | -2.392265155537524e-06 | 0.0798794 / -2.392265e-6 ✓ |
| class | 0.21119917769729965 | +2.0344163449079375e-06 | 0.2111992 / +2.034416e-6 ✓ |

Both pairings match to every digit Astra printed.

**Where the misplacement was:**
- The #40 packet, Section E (`astra_serve40/c40_body.md` L125, my review as summarized by the Lead), reads: "SYS-LIM class R 0.211, gain -2.39e-6 kept as REPORTED". This pairs the class R with the global gain, and it is the text Astra corrected.
- My own results review (cabd7fae, §5 L185) reads: "Its class R is 0.211 and its global R is 0.0799, with gain −2.39e-6." Grammatically it attaches −2.39e-6 to the global R, which is correct, but the sentence is ambiguous and leaves out the class gain. That ambiguity is the most likely source of the packet's mis-pairing. I take responsibility for it, and this note supersedes that line.
- REPORT.md (c755e5ea) does not print SYS-LIM gains. It lists the four SYS-LIM rows as REPORTED (L88-91), so it needs no correction.

**Corrected statement:** "SYS-LIM (weighted ALL, eps_syn 0.1): global fit R 0.0798794 with measured gain -2.39e-6; class fit R 0.2111992 with measured gain +2.03e-6. Both rows are REPORTED only and enter neither VALIDATION nor HEADROOM."

Astra's interpretive sentence, raw L29, verbatim: "The positive pooled class gain does not contradict D7's specified failure on held-out A: an aggregate improvement can coexist with a systematic failure on particular evaluation prefixes." The stored results need no correction (raw L29).

Side observation, not a correction: the SYS-LIM global R (…238854) and the SYS-O6 global R (…238844) agree to 15 significant figures. Both round to 0.0798794. The same printed figure therefore appears in (a) and in (b) below, but the rows differ: (a) is SYS-LIM and (b) is SYS-O6.

## 3. Correction (b): replace the "about 4/5 from M-1" line with a within-system comparator ratio

**Superseded text:** this is the CNA's 10:03 AM ET point, recorded in the #40 brief (L8) and the #40 packet §F.1 (c40_body.md L133): "SYS-O6 global R 0.0799 reproduces the oracle's 0.080, while the class R is 0.0166, so about 4/5 of the oracle headroom came from M-1 structure." My results review §3 (cabd7fae, L166) has a related line: "Both show that most of the oracle-scale headroom was carried by structure a class-conditioned μ map can represent. This agrees with CNA and M-1." It is superseded on the same basis. Astra, raw L63: "'about four-fifths of oracle headroom came from M-1 structure' over-interprets it."

**Source rows** (results.json `.pooled`, system SYS-O6, group ALL, eps_syn 0.1, mode weighted):

| Row | R | L_mu | L_full | S |
|---|---:|---:|---:|---:|
| SYS-O6 global | 0.07987942230238844 | 2.373531e-06 | 1.93e-33 | 2.971392e-05 |
| SYS-O6 class | 0.016625781241345363 | 4.940172e-07 | 2.53e-33 | 2.971392e-05 |

These are 0.0798794 and 0.0166258 as Astra prints them (raw L60, L67) ✓. Both rows have the same S, so the actual response energy is unchanged, and L_full is effectively zero in both, so both full predictors are effectively exact. This agrees with raw L67.

**Arithmetic:**
- class/global = 0.016625781241345363 / 0.07987942230238844 = 0.2081360
- relative decrease = 1 − 0.2081360 = 0.7918640, about 79.2%

The 79.2% is the relative decrease in R from global to class. It is not the ratio class/global, which is about 20.8%. Astra's own expression (raw L60) is "1 - 0.0166258 / 0.0798794 = approximately 79.2%".

**Replacement wording**, Astra raw L67, verbatim:

> "Within SYS-O6, at weighted ALL and eps_syn = 0.1, class conditioning reduced the fixed-kappa comparator-loss ratio from 0.0798794 to 0.0166258, a relative decrease of approximately 79.2%. The actual response energy and evaluation coverage were unchanged. Both full predictors remained effectively exact. The difference therefore reflects the lower held-out error of the class-conditioned fixed-kappa comparator under this design."

Qualifications Astra attaches (raw L69, L78), recorded so the replacement isn't read as an attribution:
- "It is not a decomposition assigning 79.2% of some intrinsic signal to M-1."
- "R is not itself measured gain. The global PC value near 0.0792 must not be described as successfully recovered signal."

For reference, the same within-system contrast in SYS-PC (weighted ALL, eps 0.1) is global R 0.0792154 against class R 0.0164875. There, the global fit has measured gain 0 (L_mu = L_full = 2.352102e-6) and the class fit has gain 4.895562e-7, which matches Astra's table at raw L73-76 ✓.

## 4. Correction (c): eps statement limited to the four declared sizes

**Superseded text:** the #40 packet §C (c40_body.md L94) says "Changing eps cannot buy R headroom." The Lead's room carry-forward said that a bigger eps "wouldn't buy any headroom". Astra, raw L90: "'Changing eps cannot buy R headroom' is too universal. Nonlinear finite responses can change R outside the observed regime."

**Replacement wording**, Astra raw L88, verbatim:

> "Across the four declared edit sizes, increasing eps did not make the governing relative headroom requirements pass. The observed scaling is consistent with leading-order quadratic scaling of both H and S."

The supporting values below are SYS-PC class, weighted, at the four declared eps_syn values only (0.02, 0.05, 0.1, 0.25). The arithmetic is H/eps² and S/eps².

| Group | eps | H (= L_mu) | S | H/eps² | S/eps² | R |
|---|---:|---:|---:|---:|---:|---:|
| ALL | 0.02 | 1.948002e-08 | 1.186815e-06 | 4.8700e-05 | 2.96704e-03 | 0.0164137 |
| ALL | 0.05 | 1.218898e-07 | 7.418804e-06 | 4.8756e-05 | 2.96752e-03 | 0.0164298 |
| ALL | 0.1 | 4.895562e-07 | 2.969249e-05 | 4.8956e-05 | 2.96925e-03 | 0.0164875 |
| ALL | 0.25 | 3.147443e-06 | 1.863383e-04 | 5.0359e-05 | 2.98141e-03 | 0.0168910 |
| MARG | 0.02 | 5.749544e-09 | 3.264121e-07 | 1.4374e-05 | 8.16030e-04 | 0.0176144 |
| MARG | 0.05 | 3.597226e-08 | 2.040418e-06 | 1.4389e-05 | 8.16167e-04 | 0.0176298 |
| MARG | 0.1 | 1.444266e-07 | 8.166570e-06 | 1.4443e-05 | 8.16657e-04 | 0.0176851 |
| MARG | 0.25 | 9.262891e-07 | 5.125659e-05 | 1.4821e-05 | 8.20106e-04 | 0.0180716 |

Across the four sizes, S/eps² varies by at most 0.5% and H/eps² by at most 3.4%, which is consistent with leading-order quadratic scaling. R stays below its threshold at every declared size (ALL 0.05, MARG 0.02). This note makes no statement about any eps outside these four values. Astra, raw L90: "Nothing here warrants testing additional sizes or substituting a different reference size." Only eps_syn 0.1 governs the labels (C7.3).

## 5. Weighting (Astra's sentence, verbatim)

Astra, raw L82:

> "The governing law-weighted SYS-PC class MARG ratio is 0.0176851, below 0.02. The diagnostic unweighted ratio is 0.0201098 and would satisfy the numerical MARG thresholds under that different weighting. The frozen weighted result remains HEADROOM NOT MET. This sensitivity reflects a change in the evaluation measure, not statistical uncertainty or permission to select another mode."

And raw L84: "Avoid calling the counterfactual result AVAILABLE: that imports the earlier oracle terminology. Say that the unweighted diagnostic meets the numerical MARG thresholds. ALL fails under either mode."

Check against results.json (SYS-PC, class, MARG, eps 0.1):
- weighted R = 0.017685105380191104, which equals 0.0176851 ✓ and equals HEADROOM.MARG.values.R.
- unweighted R = 0.020109810490499952, which equals 0.0201098 ✓; unweighted √H = 3.9198e-4.
- unweighted ALL R = 0.0190138, below 0.05, so ALL fails under either mode ✓.

Weighted MARG 0.0176851 governs (C3.10). Unweighted 0.0201098 is a diagnostic only and is never called AVAILABLE.

**Superseded text:** my results review (cabd7fae, L146) says "Both would clear, so MARG would read AVAILABLE." The packet §E repeats it ("i.e. AVAILABLE"). Both are superseded by the wording above. "AVAILABLE" remains only as the name of a frozen label in the REPORT.md template (L25, L80; RL-7), which the stored weighted result does not carry.

## 6. RL-14 disposition (verbatim)

Astra, raw L108, verbatim:

> "Attempt 1 was an archived administrative preflight refusal. Attempt 2 was the sole completed scientific execution under the amended application. No further attempts are authorized."

Context (raw L92-110): RL-14 is "acceptable as an explicit administrative amendment, not as an automatic exception to the attempt limit." No new authorization record is needed. Addendum 1 (5f7e06e0) contains the line "the single-run rule (against outcome-dependent repetition) is not engaged". Astra would not keep that line without qualification (raw L102: "The outcome-selection concern was not implicated, but the literal application restriction still applied. NOTE_1 correctly addresses that."), so this note reads Addendum 1 together with Note 1 (c05fdb5a). Addendum 1 L12 already says "After attempt 2 there are no further attempts, whatever the outcome", which is consistent with the sentence above. Astra, raw L110: "Do not generalize this disposition to failures after arrays, fits, responses or study-dependent timing have been inspected."

Linked records, as Astra's raw L106 asks: application v1 (review/ckappa_classfit/ckappa_classfit_standing_approval_application_v1_1f6d.md); Addendum 1 (…_ADDENDUM_1_cb1b.md, 5f7e06e0); Note 1 (…_NOTE_1_003f.md, c05fdb5a); Delegate concurrence (ckappa_classfit_addendum1_review_RD_20ee.md, a927ac7e per the #40 packet §G); re-seal diff (classfit_reseal_diff.txt); attempt 1 (classfit_outputs_attempt1/, classfit_post_run_index_attempt1.json); attempt 2 (classfit_outputs/, classfit_post_run_index.json 4552b794).

## 7. Q5: package closes, lessons go to Track B, no rerun

Astra, raw L112-114: "Choose (c), transferring the lessons through one design-only Track B instrument-validation scope." and "Close this C-kappa package as completed and do not begin another headroom redesign."

Astra, raw L143: "Preserve all sealed outputs. No rerun, threshold adjustment, weighting substitution or new C-kappa fixture is warranted."

Disposition: the C-kappa class-fit package is **CLOSED** (raw L135: "CLOSE THE CLASS-FIT PACKAGE WITH ADDITIVE INTERPRETATION CORRECTIONS; retain NO-GO and the existing claim ceiling"). Its lessons move into the single Track B instrument-validation scope, which is design-only. Raw L133: "This recommendation authorizes preparation of that scope, not a Track B experiment or checkpoint inspection." That scope is tracked separately.

## 8. Claim ceiling (unchanged)

Astra, raw L145, verbatim: "The claim ceiling does not change. This package establishes bounded synthetic implementation and measurement results. It establishes no result about trained GRUs, answers none of the four Q-tags, excludes neither general two-coordinate mediation nor lookup implementations, and supports no consciousness, C4/C5, autopoiesis or life claim. The limitations concerning nonlinear, prefix-dependent and orbit-dependent codes remain explicit."

## 9. Mismatch log

- No numerical mismatch was found between the assigned figures, the Astra #40 raw text and results.json @ cffe125b. All of these agree at the printed precision: 0.0798794, -2.39e-6, 0.2111992, +2.03e-6, 0.0166258, 79.2%, 0.0176851 and 0.0201098.
- Wording point: "79.2%" is the relative decrease, 1 − class/global. The ratio class/global is 20.8%. Section 3 uses Astra's wording, which states the relative decrease.
- Wording point: the NO-GO decision wording in the raw text has a second sentence. Section 1 records both sentences.
