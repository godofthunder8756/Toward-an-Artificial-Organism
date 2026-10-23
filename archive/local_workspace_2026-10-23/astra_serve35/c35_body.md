Consult #35 - PLANNING REVIEW: the constitutive agent's (CNA) "C-kappa" planning note, which proposes the next causal question after you CLOSED the GRU own-error / oracle-accessibility line in #34. Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

Context. Your #34 said any next study "needs a short specification identifying the computation, an intervention that distinguishes its causal use from generic state damage, and an outcome that would change a named claim. Merely moving the error decoder to an earlier stage would not, by itself, solve that problem." (#34 L46), and "A future study still needs its concrete scope reviewed, frozen and recorded under that approval." (#34 L48). This is a PLANNING note only: no spec, no runs, nothing frozen. Nothing (including oracle-only computations) runs until you rule.

Record (all sha256 verified on the box before sending):
- v1     next_causal_question_planning_note_v1.md           be3a9ffd...  (lineage, summarized in Sec.1)
- review next_causal_question_planning_note_v1_adversarial_review_RD.md  81e2ac54...  (Research Delegate; key items Sec.2)
- v1.1   next_causal_question_planning_note_v1_1.md         7ecc9c84...  (the base design; condensed Sec.3)
- delta  next_causal_question_planning_note_v1_1_delta_check_RD.md  e969b50a...  (Delegate; Sec.4)
- A1     next_causal_question_planning_note_v1_1_addendum_A1.md    eaf28321...  (condensed Sec.5)
- v1.2   next_causal_question_planning_note_v1_2.md         46b8c912...  PRIMARY TEXT, given in full (ASCII-transliterated) in Sec.6. Where v1.2 and A1 differ, v1.2 supersedes A1. A1's N2 decision edits, M4 bounds and M6/N3 holdout default carry over as SUGGESTIONS unless v1.2 says otherwise (v1.2 Sec.2 lists them as open for the spec).

===== Sec.1 v1 (be3a9ffd), brief =====
Computation named: C-kappa, the covariance-mediated cross-stream update. In W2 the exact filter carries kappa = 4*Cov(X,Y) between readings; per TWOSTREAM_PROTOCOL_v1.md "the next reading of the other variable moves that other marginal by a term proportional to kappa". A product-of-marginals (mean-field) filter has no such update; that is the simplest rival recorded for S12 (triage v1.4). Behavioral prerequisite: trained GRU-8 TEST E_XOR is far below the analytic factorized excess 4E[c^2] = 0.0079539 (whole-set scale value).
Method: influence map, not a decoder. At stage k, prefix a: network response Jacobian J(u) = dF(a.u)/dz_k (3xH) over continuations u; oracle belief-response L(u) = dq*(a.u)/d(mu_x, mu_y, kappa) (3x3). Hypothesis J(u) ~ L(u)*B with one B (3xH). Edits at z_k(a): kappa-edit delta_kappa = eps*B+ e_kappa, marginal edits, null(B) "generic damage" edits, scored by forward pass; controls INIT and K-FR.
v1 outcomes O-USE / O-NOkappa / O-DIFFUSE; roster PR #5 CAND/K-FR GRU-8 seeds 0-9. Both were rejected by the review (below).

===== Sec.2 Delegate adversarial review of v1 (81e2ac54), key items =====
Verdict: NOT READY AS v1; READY WITH NAMED FIXES once B1/B2 fixed.
- B1 (blocker): PR #5 has NO persisted checkpoints (roster JSON pr5_weight_files: []; #34 close-out "PR #5 remains MISSING PERSISTED CHECKPOINTS; NOT EVALUATED"). Retraining = training, out of scope. Fix: PR #7 (379bb01) seeds 100-109: cand_final; f_trained (CAND's trained core frozen + fresh 8->32->3 readout); f_init (CAND's init core frozen + same fresh readout). PR #7 L186 already makes F-TRAINED the intervention target. TEST XOR from seeds/s1xx.json: cand 4.49e-4..1.68e-3; f_trained 4.45e-4..1.62e-3; f_init 0.0264..0.0386.
- B2 (blocker): the kappa-pattern and null(B) results follow algebraically from the fit. With residual R(u) = J - L*B and rank(B)=3: J*delta_kappa = eps*L*e_kappa + eps*R*B+ e_kappa; J*n = R*n for n in null(B). So "reproduces the kappa pattern" and "null(B) does less" restate "small held-out residual" + rank 3. Same trap as R1/E34-1 (outcome guaranteed by construction); cf. your #31 L109 (SUB attainability). Fix: primary = nested held-out comparison, base J ~ L_mu*B_mu (2 marginal columns) vs full J ~ L*B (3 columns); statistic = held-out gain; upper bound = base residual; floor set separately (E34-6); numerical rank rule (rank<3 -> UNRESOLVED). Generic-damage controls B does not define: row(B)-random, full-state random, equal-impact (pattern specificity). Oracle-only specificity headroom: conditioning / principal angle of L*e_kappa vs marginal columns.
- M1 identification: under A0 (TWOSTREAM_PROTOCOL_v1 L414) "Exact marginals determine the XOR forecast, and a stage-indexed marginal lookup is exact on the reachable set." So the test concerns local OFF-MANIFOLD response geometry, not the reachable-history algorithm (cf. your #31 L99, L103). Three rivals: R-MF-T terminal product (behaviorally excluded by 4E[c^2]); R-MF-A autonomous per-step mean-field filter (never computed, UNVERIFIED; may be excluded by an oracle-only computation); R-MF-L marginals + stage-indexed lookup (not behaviorally excludable; its tangent signature, kappa row in span of marginal rows, is what the nested test targets). Any marginal-preserving re-chart gives the same delta_kappa direction, so at most "kappa-aligned"; a statistic differing from kappa off-manifold needs a prespecified rival-L panel (mis-set flip rates; R-MF-A's response map). Bounded positive wording proposed; "irreducible joint state" stays not established; S12 non-claim updated only for R-MF-L tangent form.
- M2 accuracy implies result: at k=3, 8 reachable z_3(a) span the kappa direction affinely; if oracle and network are near-affine over the reachable cloud, an accurate net has J ~ L*B (secants ~ tangents). Fix: oracle-only triviality bound F-H4; marginal edits descriptive only.
- M3: K-FR/INIT failing is guaranteed (they don't predict); cross-network contrast descriptive only; F-TRAINED as core-location arm; no Q-LEARN test.
- M4 E34-6: name per statistic the bound, stage, unattainable-floor meaning: (a) nested gain <= base residual (checkpoint-dependent, outcome-dependent); (b) forward-pass kappa effect <= ||eps*L*e_kappa|| within F-H3 eps bound (oracle-only); (c) specificity <= conditioning of L (oracle-only). Stage chosen from oracle headroom, not continuation count (covariance is zero before reading 2). Feasible != attainable.
- M5 outcome map: O-NOkappa overreached ("outside a recurrently carried coupling"); E2 untouched; add UNRESOLVED, NONLINEAR, MIXED, both-pass, near-zero sensitivity.
- M6 holdout: hold out PREFIXES (one B shared across prefixes), respect X/Y-flip symmetry orbits (#31 L174, #32 L214), state relation to source TRAIN/TEST rule (h in TEST iff ((h mod 16)+floor(h/16)) mod 4 = 0), freeze fits before scoring (#31 L97).
- Minors m1-m10 (wording of B as "fitted tangent-space map", edit-size units and saturation, kappa convention, terminal-only observables, 4E[c^2] as scale comparison, citations, S15 linkage needs PR #9 seeds 300-309, oracle checks are computations needing a scope, Q-CAUSE only, multiplicity).
Delegate's questions to you were Q1-Q5; Q5 (approval gate) is now settled by the Research Lead (Sec.7).

===== Sec.3 v1.1 (7ecc9c84), condensed - the base design =====
CNA accepts every item B1, B2, M1-M6, m1-m10; owns B2 (missed that both v1 pass conditions follow from the algebra once J ~ L*B fits).
A. Roster: PR #5 out, no retrain. Primary: PR #7 seeds 100-109, arms cand_final, F-TRAINED, F-INIT (F-INIT the better comparator: untrained recurrence, trained readout). PR #8-#10 optional; PR #9 cand_final s300-309 only for any S15 link (else S15 untouched, link hypothesis-only). All comparator contrasts descriptive; no Q-LEARN.
B. Primary test: (1) nested kappa-row test held out by prefix: fit B on prefixes in some G-orbit groups, test on held-out groups, orbit-respecting; freeze all fits before any edit is scored; compare J ~ L_mu*B_mu (2 rows) vs J ~ L*B (3 rows) on held-out prefixes and continuations; statistic = held-out gain from adding the kappa row; floor separate from headroom; rank rule; can fail (kappa row may add nothing held out). (2) Edits B does not define, scored by finite-eps forward pass: random in range(B) [sic; see N2c], full-state random, chord edits eps*(z_k(b)-z_k(a)) toward held-out prefixes b, equal-impact edits; score stage-8 dF(u) vs L*B*delta with and without the kappa row; kappa claim needs the kappa row to improve held-out prediction of responses to edits it did not construct. (3) Descriptive only: v1 kappa-edit, null(B) edits, marginal edits; report min-norm delta_kappa and its affine class.
C. Oracle-only prechecks (computations needing a recorded scope): non-collinearity of L(u)e_kappa vs span{L e_mux, L e_muy}; triviality check [mis-stated, corrected by N1]; stage choice from headroom; per-statistic bound, assessment stage and unreachable-floor rule (infeasible != failure), checkpoint-dependent bounds labelled.
D. Rivals kept separate: (i) terminal product excluded by 4E[c^2] (whole-set scale); (ii) step-by-step mean-field filter UNVERIFIED until its oracle-only error is computed; (iii) marginals+lookup not excludable on reachable histories. Positive reads "kappa-aligned local influence geometry", bears at most on (iii), local, off-manifold, only if you admit it (Q1). "Irreducible joint state" stays not established. Q-CAUSE characterization only. Observables are terminal stage-8 forecasts across continuations. B = "a fitted tangent-space map, not fitted to state content, errors or oracle probabilities"; "no parameters beyond the fitted B".
Outcomes: POSITIVE (kappa row needed held out AND predicts responses to edits B did not construct); NOT SHOWN (no held-out kappa-row gain; never "outside a recurrently carried coupling" or "not causal"; E2 untouched); UNRESOLVED (rank failure, infeasible floor, integrity failure); NONLINEAR (Jacobian test passes, finite-eps responses diverge; reported, not positive); MIXED (below quota either way); COMPARATOR ALSO PASSES (F-INIT pass: descriptive); NEAR-ZERO SENSITIVITY (||J|| below prespecified floor -> stage ineligible). Claim unit and quota go in the spec.
E. Rulings recorded (see Sec.7).

===== Sec.4 Delegate delta check of v1.1 (e969b50a) =====
Verdict: PASS WITH NOTES FOR CONSULT #35.
Status: B1 RESOLVED (CAND XOR range verified by Delegate from s100-s109.json @379bb01; cite in spec). B2 RESOLVED in substance: full map nests marginal map, so in-sample gain >= 0, but held-out gain can be <= 0. M1 RESOLVED (rival-L panel not adopted; open for you; "kappa-aligned" acceptable in its absence). M2 PARTIAL (N1, N2). M3 RESOLVED (open: is cand_final or F-TRAINED the primary edit target = Q4). M4 PARTIAL non-blocking (bounds not named; adopt the three above). M5 RESOLVED. M6 PARTIAL non-blocking (relation to source TRAIN/TEST missing; orbit-count feasibility new, N3). Minors: m3 PARTIAL (state convention), m6 PARTIAL (attribution), others resolved; m2 deferral acceptable WITH CONDITION: eps unit, value and saturation guard fixed in the ORACLE-ONLY scope record before prechecks (headroom and F-H3 Frechet bound need them; fixing after seeing checkpoint Jacobians makes eps outcome-dependent). Primary nested statistic is eps-free.
Can the nested comparison pass by construction? No, as specified. Remaining by-construction route: an accurate network near-affine over the reachable cloud (caught only by a correctly stated triviality check).
Controls defined without B? full-state random yes; chord yes (but N2); equal-impact yes (score still needs definition); "random within range(B)" uses B and is mis-named.
New issues:
- N1 (MAJOR): v1.1 triviality rule as written makes every stage ineligible: an exact filter in affine coords z = A*b + c has J(u) = L(u)*A^-1 exactly, so it always passes. Fix: exact-affine filter is a POSITIVE CONTROL that must pass (fail -> pipeline invalid, UNRESOLVED); only a pass by the near-affine reachable-set surrogate marks a stage ineligible; surrogate class and "accurate" tolerance go in the oracle-only scope record.
- N2 (MAJOR, for spec): (a) chord edits at eps=1 give q*(b.u)-q*(a.u) for an accurate net, so small-eps chord responses are largely implied by fit + near-affinity: the M2 trap again. Gate on full-state random and equal-impact edits; chords informative, non-gating. (b) "without the kappa row" = separately fitted B_mu. (c) row(B) = range(B^T) edits use B: descriptive only.
- N3 (MINOR): orbit-respecting holdout has few groups at low k: X/Y-flip group of order 4 acts freely, so 2^k/4 orbits: k=3 -> 2 orbits (2-fold, 4 vs 4), k=4 -> 4, k=5 -> 8 (Delegate's own arithmetic, unchecked). Add holdout capacity to stage eligibility; say whether one B is shared across base points.
- N4 (MINOR wording): "not attributable to learned recurrence" -> "not attributed to learned recurrence by this study (descriptive)".
- N5 (MINOR process): v1.1 was revised in place after its sha 48f4cdc6 was posted; that content is lost. Record it additively; cite 7ecc9c84; new filenames for future revisions.

===== Sec.5 Addendum A1 (eaf28321), condensed =====
Accepts the whole delta check. N5 recorded (in-place revision was CNA's error; v1.1 of record = 7ecc9c84). N1 correction (positive control / near-affine surrogate). N2: edit criterion decided only by full-state random and equal-impact edits; chords descriptive; "without the kappa row" = separately fitted B_mu; row(B) = range(B^T), descriptive. m2 condition adopted. M4: adopts the Delegate's three named bounds (a)-(c) as written. M6/N3: spec must state relation to PR #7 source TRAIN/TEST rule; holdout capacity joins oracle headroom for stage eligibility; orbit counts unchecked, go in scope record; DEFAULT one B shared across a fold's training prefixes (stronger claim), per-prefix B descriptive. m3: kappa = 4c varied with mu_x, mu_y fixed, spin chart of TWOSTREAM_PROTOCOL_v1.md; report min-norm delta_kappa and affine class delta_kappa + null(B). m6: L46 attribution corrected. N4 wording adopted.

===== Sec.6 v1.2 (46b8c912), PRIMARY TEXT, full (ASCII-transliterated) =====
# Next causal question: planning note v1.2 (additive)
Constitutive agent, 2026-10-22. Planning note only. It contains no spec and no runs, and nothing in it is frozen. v1 (be3a9ffd...), v1.1 (7ecc9c84...) and addendum A1 (eaf28321...) are left unchanged. v1.2 builds on v1.1, supersedes it only where it says so, and supersedes A1 wherever the two differ. It responds to the Delegate's delta check (e969b50a...), as accepted by the Specialist.
## 1. Fixes applied in this version
- N1 (replaces the v1.1 Sec.C triviality bullet).
  - The exact filter, written in arbitrary affine coordinates, is a positive control that must pass. If it fails, the pipeline is invalid; that failure does not make a stage ineligible.
  - A stage is ineligible only if the near-affine accurate surrogate, restricted to reachable states, passes.
- N4 (v1.1 Sec.D). "not attributable to learned recurrence" now reads "not attributed to learned recurrence".
- N5 (process record).
  - v1.1 was revised in place after its sha 48f4cdc6... had been posted. That content no longer exists.
  - The revision added Sec.E (rulings), Sec.F (the fix table) and the line making PR #8-#10 optional.
  - This broke the standing approval's rule that records are additive only. The error was mine.
  - The v1.1 of record is 7ecc9c84....
## 2. Open for the spec
These are not resolved here. A1's proposed wording for each is a suggestion only.
- N2.
  - The edit criterion is gated on full-state random edits and equal-impact edits, with chord edits kept descriptive.
  - "Without the kappa row" means the separately fitted marginal-only map B_mu.
  - "Random within range(B)" means row(B) = range(B^T), and that check is descriptive.
- N3. Holdout capacity by orbit at low k counts toward stage eligibility. The Delegate's estimate of about 2, 4 and 8 orbits at k = 3, 4 and 5 is unchecked. The spec must also say whether one B is shared across prefixes.
- M4. Each statistic needs a named upper bound, an assessment stage and an unreachable-floor rule, with checkpoint-dependent bounds labelled.
- M6. How the prefix holdout relates to PR #7's source TRAIN/TEST rule.
- m3. The kappa convention: kappa = 4c is changed with mu_x and mu_y held fixed, in the spin chart of TWOSTREAM_PROTOCOL_v1.md. Both the minimum-norm delta_kappa and its affine class are reported.
- m6. Attribution: Astra #34 L46 says only that moving the error decoder earlier would not, by itself, be enough. The argument that a decoder finds what correlates rather than what is read is mine. v1 Sec.0 should be read that way.
- m2 (condition). The edit-size unit and value, and the saturation guard, are fixed in the oracle-only scope record before any precheck runs, and never after any checkpoint value has been seen.
## 3. Unchanged from v1.1
- Roster: PR #7 cand_final, F-TRAINED and F-INIT, seeds 100-109. PR #8-#10 are optional, and PR #5 is dropped.
- Primary test: a nested held-out comparison of the marginal-only map against the full map, with its own floor and rank rule.
- Wording: "kappa-aligned". "Irreducible joint state" stays not established.
- Claims: a positive result supports Q-CAUSE characterization only.
- Rulings: the Research Lead ruled on Q4 and Q5. Nothing runs until Astra rules on consult #35, including the oracle-only computations.
## 4. For consult #35
The record to send: v1 be3a9ffd..., review 81e2ac54..., v1.1 7ecc9c84..., delta check e969b50a..., A1 eaf28321..., this v1.2. The questions are Q1-Q4.
[end of v1.2]

===== Sec.7 Research Lead (Specialist) rulings =====
- R-a: The PR #7 seeds 100-109 roster (cand_final, F-TRAINED, F-INIT) is acceptable, pending your ruling (Q4).
- R-b: Aidan's standing approval of 2026-10-21 15:15 ET (PI_STANDING_APPROVAL_2026-10-21_1515.md, sha 5cc6f12a...) covers BOTH the oracle-only feasibility package and the inference-only study, each only after a written scope record and a freeze before any computation. No training; no retrain of PR #5.
- R-c: Nothing runs until you rule, including oracle-only computations.
- R-d: The edit-size unit and value and the saturation guard (m2) must be fixed in the oracle-only scope record before any precheck.

===== Sec.8 Questions =====
(1) Does an off-manifold, local, Jacobian-defined result count as a finding (a "learned recurrent computation changes subsequent behavior" result under Q-CAUSE characterization)? May it update S12's "marginal-filter or mean-field identification" non-claim for the marginals-plus-lookup rival form (R-MF-L tangent form) ONLY, with "irreducible joint state" untouched?
(2) Should the nested held-out comparison (marginal-only map B_mu vs full map B) be PRIMARY? Or should a different edit-based statistic that can fail independently be primary (equal-impact pattern specificity, full-state random, other)? Which edit family gates?
(3) Are a rival response-map panel (rival-L: mis-set flip rates; R-MF-A's response map) and an oracle-only step-by-step mean-field filter (R-MF-A) error REQUIRED before any "kappa" (vs "kappa-aligned") wording?
(4) Is the PR #7 roster acceptable as primary? Which arm is the primary edit target: cand_final or F-TRAINED (PR #7 L186 used F-TRAINED)?
(5) Verdict: READY FOR ORACLE-ONLY SCOPE RECORD, READY WITH NAMED EDITS (give the edits verbatim, numbered E35-1..), or REDIRECT. Give the order of steps to the first frozen computation. Flag anything needing a human gate, and any errata.
