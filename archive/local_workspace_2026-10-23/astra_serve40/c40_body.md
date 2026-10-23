Consult #40 - C-kappa CLASS-FIT RESULTS (attempt 2, completed) + GO/NO-GO. Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

What is sent. (A) run facts; (B) the VALIDATION and HEADROOM blocks of results.json verbatim; (C) a compact pooled table and what it shows about eps; (D) four governing clauses of scope record v1.3 verbatim (C3.10, C7.3, C7.4, E38-15 only); (E) the Research Delegate's results review, summarized with key lines quoted; (F) the CNA's two points, checked against results.json; (G) the RL-14 record of attempt 1 vs attempt 2; (H) the Lead's provisional call; (I) Track B context, for Q5 only; (J) six questions. ASCII transliteration only (Greek spelled out, markdown dropped). Nothing new has run since attempt 2; nothing is being run while you answer.

Sources (sha256, all re-verified today):
- scope record ckappa_classfit_synthetic_scope_record_v1_3.md a17e133d7dd733c4... (status line: "SCOPE APPROVED FOR FREEZE PER ASTRA #39 (E39-1)"; consolidates v1.2 + NOTE_1 + E39-1..11; the package was later sealed under manifest e7a9d3a4)
- classfit_outputs/results.json (attempt 2) 05385099c4f0b4a0...
- Delegate results review ckappa_classfit_results_review_RD.md cabd7fae619b4445...
- Application v1 Addendum 1 (RL-14) 5f7e06e084e8da40...; its Note 1 c05fdb5abb658a75...; Delegate concurrence on Addendum 1 a927ac7e914416...
- PR #14 HEAD cffe125b; re-sealed manifest e7a9d3a49b0a41cf...; REPORT.md c755e5ea...

== (A) RUN FACTS (attempt 2) ==
- stop_kind = "COMPLETED", exit_code = 0, t_elapsed_s = 125.286 (cap 540 s operational stop). No projection halt (T_rem 59.97 s vs limit 539.37 s at 0.631 s).
- Propagations: 272 exact + 3443968 float = all scheduled, all attempted; SVDs 541; 336 pooled rows, all formed; 189 accounting records all closed, every skip/unknown count 0; no voids, no crossings, coverage 1.0 everywhere; d7_investigate = [] (empty).
- Final VmPeak 84,964 kB (cap RLIMIT_AS 4e9 B).
- Labels: SYS-O6, SYS-PC, SYS-FK = IDENTITY AS DERIVED (global and class, ALL and MARG); SYS-NC1..NC3 and SYS-LIM = REPORTED. No first_failing_reason anywhere.

== (B) VALIDATION and HEADROOM, verbatim from results.json ==
{
 "VALIDATION": {
  "first_failing_reason": null,
  "label": "CLASS-FIT VALIDATION MET",
  "met": true
 }
}
{
 "HEADROOM": {
  "ALL": {
   "H_definition": "L_mu of the SYS-PC class fit at eps_syn 0.1",
   "clearly_below": [
    "sqrt_H",
    "R"
   ],
   "eps_syn": "0.1",
   "group": "ALL",
   "label": "HEADROOM NOT MET",
   "met": false,
   "values": {
    "H": 4.89556152279922e-07,
    "R": 0.016487539966074785,
    "R_definition": "comparator squared prediction error divided by actual response energy",
    "R_threshold": 0.05,
    "S": 2.9692492226690342e-05,
    "sqrt_H": 0.000699682894088402,
    "sqrt_H_threshold": 0.001
   }
  },
  "MARG": {
   "H_definition": "L_mu of the SYS-PC class fit at eps_syn 0.1",
   "clearly_below": [
    "R"
   ],
   "eps_syn": "0.1",
   "group": "MARG",
   "label": "HEADROOM NOT MET",
   "met": false,
   "values": {
    "H": 1.444266445924549e-07,
    "R": 0.017685105380191104,
    "R_definition": "comparator squared prediction error divided by actual response energy",
    "R_threshold": 0.02,
    "S": 8.166569635158952e-06,
    "sqrt_H": 0.0003800350570571811,
    "sqrt_H_threshold": 0.0001
   }
  }
 }
}

== (C) POOLED ROWS (weighted mode unless marked UNWTD; eps_syn = 0.02 0.05 0.1 0.25) ==
There is no separate size dimension in the pooled rows: every row has n_scoreable 24576; the 4 rows per (system, fit, group, mode) are the 4 eps values. XOR group omitted for space. SYS-FK omitted: |R| <= 5.9e-28 at every eps (exact, as derived).
row                    | R @ 4 eps                       | sqrt_H @ 4 eps
O6 global ALL          | 0.07992 0.07991 0.07988 0.07967 | 3.08e-04 7.70e-04 1.54e-03 3.85e-03
O6 class ALL           | 0.01655 0.01657 0.01663 0.01703 | 1.40e-04 3.51e-04 7.03e-04 1.78e-03
O6 global MARG         | 0.07869 0.07868 0.07865 0.07845 | 1.60e-04 4.01e-04 8.02e-04 2.01e-03
O6 class MARG          | 0.01776 0.01778 0.01783 0.01822 | 7.62e-05 1.91e-04 3.82e-04 9.67e-04
PC global ALL          | 0.07925 0.07924 0.07922 0.07901 | 3.07e-04 7.67e-04 1.53e-03 3.84e-03
PC class ALL           | 0.01641 0.01643 0.01649 0.01689 | 1.40e-04 3.49e-04 7.00e-04 1.77e-03
PC global MARG         | 0.07803 0.07803 0.07800 0.07780 | 1.60e-04 3.99e-04 7.98e-04 2.00e-03
PC class MARG          | 0.01761 0.01763 0.01769 0.01807 | 7.58e-05 1.90e-04 3.80e-04 9.62e-04
NC1 global ALL         | 0.00438 0.00438 0.00438 0.00437 | 7.43e-05 1.86e-04 3.72e-04 9.30e-04
NC1 class ALL          | 0.00152 0.00152 0.00153 0.00159 | 4.38e-05 1.10e-04 2.20e-04 5.62e-04
NC2 global ALL         | 0.01142 0.01142 0.01142 0.01141 | 1.08e-04 2.71e-04 5.42e-04 1.36e-03
NC2 class ALL          | 0.00201 0.00201 0.00202 0.00206 | 4.55e-05 1.14e-04 2.28e-04 5.77e-04
NC3 global ALL         | 0.01182 0.01184 0.01189 0.01225 | 1.10e-04 2.76e-04 5.53e-04 1.41e-03
NC3 class ALL          | 0.00703 0.00703 0.00706 0.00726 | 8.50e-05 2.13e-04 4.26e-04 1.08e-03
LIM global ALL         | 0.07992 0.07991 0.07988 0.07967 | 3.08e-04 7.70e-04 1.54e-03 3.85e-03
LIM class ALL          | 0.21118 0.21118 0.21120 0.21131 | 5.01e-04 1.25e-03 2.51e-03 6.28e-03
PC class ALL UNWTD     | 0.01893 0.01895 0.01901 0.01946 | 1.46e-04 3.65e-04 7.32e-04 1.86e-03
PC class MARG UNWTD    | 0.02003 0.02005 0.02011 0.02053 | 7.82e-05 1.96e-04 3.92e-04 9.92e-04
What the data show (checked over all non-FK series, both modes, 3 groups):
- R is nearly eps-invariant: max relative spread across eps is 5.4% in any series; for the headroom row (PC class ALL weighted) 0.01641 -> 0.01689 (+2.9%) over a 12.5x eps range.
- sqrt_H scales ~linearly with eps: sqrt_H(0.25)/sqrt_H(0.02) is 12.51-12.86 against an eps ratio of 12.5 (class fits slightly superlinear, up to ~3% at 0.25). S scales as eps^2 (PC: 1.187e-6 -> 1.863e-4, ratio 157 vs 156.25). So H and S are both second order in eps and R = H/S is set by the system and fit, not by perturbation size.
- Consequence: at eps 0.25, PC class ALL would clear the sqrt_H threshold (1.77e-3 >= 1e-3), but R stays ~0.017 < 0.05. Changing eps cannot buy R headroom.

== (D) GOVERNING CLAUSES, verbatim from v1.3 (bold/backticks dropped, Greek spelled out) ==
C3.10 Pooling (E36-5, inherited).
- Occurrences are pooled with their original w(a,u) and equal direction and sign weights, normalized once over the pooled scoreable occurrences.
- The class statistic pools over all 6 folds x 4 classes.
- H, S and their ratio use identical masks and weights.

C7.3 SYS-PC HEADROOM (E38-12; Q4).
- Formation and eligibility (E39-5; #39 L147-156). VALIDATION MET is necessary but not sufficient. A threshold label is issued only if all of the following hold:
  1. VALIDATION MET;
  2. the required SYS-PC maps are available and no required fit is unresolved;
  3. the declared count and law-mass coverage (C7.1 item 3 rule) hold in every required fold/class at eps_syn = 0.1;
  4. the scoreable denominator is positive;
  5. S > 0.
  Missing eligibility receives its applicable status: NOT FORMED (VALIDATION NOT MET), REFERENCE RANK UNRESOLVED, UNAVAILABLE, REFERENCE COVERAGE NOT MET or ZERO RESPONSE. It cannot yield HEADROOM MET. Diagnostic values are stored where permitted.
- Statistic. H = L_mu,class for SYS-PC at eps_syn = 0.1, with sqrtH and R = H/S, for ALL and MARG.
- Thresholds (synthetic reporting conventions only). ALL sqrtH >= 10^-3 and R >= 0.05; MARG sqrtH >= 10^-4 and R >= 0.02 (pinned.py:24-27). Labels are HEADROOM NOT MET / BOUNDARY / MET under the inherited band rule (v1_4_N L15-16).
- No prediction is made that SYS-PC will meet them.
- They supply no neural response floor (#37 L164).

C7.4 What the labels license. VALIDATION MET with SYS-PC HEADROOM MET licenses only a decision on whether a neural specification is warranted. SYS-LIM and the confound results go with any such decision as stated limits. So does any D7 INVESTIGATE flag, which that decision must address (E39-8; #39 L15).

E38-15 (v1.3 S1, verbatim):
> "This package tests implementation identities, synthetic response headroom and limitations of declared intervention-prediction models on specified synthetic systems. It establishes no result about trained GRUs and answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY. Confound gains do not identify an independent covariance register or exclude two-coordinate mediation or reachable-set lookup implementations. Failure of a class-conditioned criterion does not exclude nonlinear, prefix-dependent or orbit-dependent covariance codes. No result establishes acquisition, recurrent-transition-specific use, necessity, irreducible joint state, C4, C5, consciousness, autopoiesis or life."

== (E) RESEARCH DELEGATE RESULTS REVIEW (cabd7fae), summary ==
Read-only at HEAD cffe125b; nothing rerun; arithmetic on stored JSON only. Headline: "Verdict: CONFIRMED WITH NOTES".
- Stop/exit: COMPLETED exit 0 consistent across stop_kind.json, run.log, results.json and index; S1/S2/S4 PASS; no NaN/Inf; all 189 accounting records closed; propagation (3,444,240), SVD (541), loss-record (16,128) and pooled-row (336) counts match v1.3.
- VALIDATION: "CLASS-FIT VALIDATION MET" correct under C7.2; every required identity PASS, every rank FULL/FULL; worst residual/tolerance ratio 7.8e-7.
- HEADROOM recomputed from the 48 SYS-PC loss records per group: ALL "both clearly below -> NOT MET"; MARG "R clearly below (ratio 0.884), sqrt_H passes (3.8x) -> NOT MET". "MARG NOT MET with sqrt_H passing is correct under the 'and' rule and clear-failure-first ordering." Nothing within the 1e-6 BOUNDARY band; closest is MARG R, 11.6% below.
- D6 6 rows REPORTED, D7 12 rows PASS, d7_investigate empty. SYS-LIM class R 0.211, gain -2.39e-6 kept as REPORTED; small negative REPORTED gains (NC1, NC3, FK ~-1e-33) retained.
- Weighting: "The mode is fixed. It is not open." (C3.10 adopts E36-5; oracle record and oracle label code also weighted; unweighted exists only as a C3.6(c) diagnostic.) Unweighted MARG would read R 0.02011, sqrt_H 3.92e-4, i.e. AVAILABLE; ALL fails either way. "The MARG result is sensitive to the mode, which deserves a report note, but it does not change the label."
- Oracle comparison: "PC class 0.0165 against oracle 0.080 compares across both system and fit type. It is not a like-for-like comparison." Legitimate: O6 global 0.0799 vs O6 class 0.0166; PC global 0.0792 vs PC class 0.0165.
- Ceiling: REPORT.md within ceiling. "Out: any statement that kappa is unused, absent, unnecessary or irrelevant in GRUs, or any 'negative result about kappa'." Failure wording must be the REPORT.md sentence: "The declared class-conditioned-map intervention-prediction criterion was not met."
- Section 6: "Provisional NO-GO: Supported." Notes: "(i) The MARG margin is narrow and sensitive to the mode. Report it, but don't re-label. (ii) The oracle comparison must be stated within each system (O6 global against O6 class). (iii) The NO-GO is a decision not to proceed with this neural specification unchanged. It is not a scientific negative about kappa or GRUs (E38-15)."
- Minor: S1 val_readout_rejection "UNVERIFIED" (pre-declared, non-gating); REPORT.md memory attribution cosmetic.

== (F) CNA POINTS (10:03 AM ET), checked against results.json ==
1. "SYS-O6 global R 0.0799 reproduces the oracle's 0.080, while the class R is 0.0166, so about 4/5 of the oracle headroom came from M-1 structure." Check: SYS-O6 global ALL weighted eps 0.1 R = 0.079879; SYS-O6 class = 0.016626; 1 - class/global = 0.792 (~4/5, consistent). The oracle value itself (0.0798794...) is not in classfit results.json; the Delegate checked it against the sealed oracle outputs/results.json section5 (equal to the last digits). Within PC the same pattern: global 0.0792 vs class 0.0165. Per the Delegate, state the comparison within each system, not "PC class vs oracle".
2. Weighted MARG R 0.01769 vs unweighted 0.02011 (results.json pooled, SYS-PC class MARG eps 0.1): matches. Under C3.10/E36-5 the weighted mode governs; unweighted is a sensitivity note only.
No number mismatches found between the brief, the Delegate review and results.json.

== (G) RL-14: ATTEMPT 1 vs ATTEMPT 2 ==
- Attempt 1 (PR #14 at 8ff3fb15, seal 992a30e6, manifest 364b7dad): exit 5, PREFLIGHT FAILED in 0.155 s, "standing-approval application is not filed": standing_approval_application.status stayed PENDING because the Lead's seal instruction omitted that field from the allowed list. load_manifest refused before the application-hash check, sealed-hash check, B0 and S0; no system constructed, no propagation/fit/SVD, all labels None. Nothing was computed or observable.
- Addendum 1 / RL-14 (5f7e06e0): attempt 1 is an administrative preflight refusal, not a study result; the single-run rule (against outcome-dependent repetition) is not engaged; exactly one attempt 2 under identical caps, environment, claim ceiling and no-rerun rule; "After attempt 2 there are no further attempts, whatever the outcome." Re-seal from 364b7dad changing only status, seal_timestamp, review_records and one note; attempt-1 outputs git mv'd byte-unchanged to classfit_outputs_attempt1/; no code change.
- Note 1 (c05fdb5a): status exactly "FILED" (preflight.py:219 is a deny-list); Addendum amends only application v1's "Exactly one attempt" clause and allowed-field list; adopts the Delegate's C1 (canonical output paths absent before launch), C2 (re-verify all five attempt-1 shas after the move), C4 (Aidan informed ~9:55 AM ET, before re-seal).
- Delegate concurrence (a927ac7e): "CONCUR WITH CONDITIONS". Static reading confirms nothing past load_manifest ran; attempt-1 outputs carry no study information ("one weak inference: ... pinned Python and NumPy were present. That is environmental, not an outcome"). Literal application text made attempt 1 "the one attempt", so attempt 2 needed the Lead's amendment, which RL-14 supplies under the standing approval.
- Attempt 2: COMPLETED, exit 0, 125.3 s, PR #14 HEAD cffe125b, re-sealed manifest e7a9d3a4, results.json 05385099.

== (H) LEAD'S PROVISIONAL CALL ==
NO-GO: the design does not proceed unchanged to a neural specification. Basis: VALIDATION MET but SYS-PC HEADROOM NOT MET for ALL (both statistics) and MARG (R), so the C7.4 licence condition ("VALIDATION MET with SYS-PC HEADROOM MET") fails. This is a programme decision under C7.4, not a negative result about kappa, GRUs or any Q-tag (E38-15). Carried notes: the MARG mode-sensitivity (sensitivity note only), the within-system oracle comparison, and SYS-LIM/confound results as stated limits.

== (I) CONTEXT FOR Q5 ONLY: Track B planning note v1 (CNA, ~10:15 AM ET; planning only, nothing frozen, nothing run) ==
Aidan proposed a toy-scale agent with a global-workspace bottleneck and a simulated "fate-shared" allostatic internal state (simulated energy/integrity variables whose deviation degrades the agent's own computation inside the sim), with hard exclusions: no coupling to the real host, no real-world self-continuity objective, operator interruptibility checked (S-INT), and a claim ceiling excluding awareness/sentience/experience/life. Arms (A-FULL, A-NOWS, A-NOFATE, A-REWARD, A-INIT) would be scored on pre-registered Q-EXIST/Q-LEARN/Q-CAUSE/Q-NECESSITY measures plus ignition, broadcast and self-prediction tests, CPU first under the standard scope/freeze/Astra/annex/application process. Its own open Q4 asks whether, as with C-kappa, a synthetic validation of the Q-EXIST/Q-CAUSE instruments on a planted internal-state model should come first. Prior-art citations are unverified and a novelty check is pending.

== (J) QUESTIONS - answer each with a one-line verdict first; keep the whole answer under ~2,500 words ==
(1) Labels: do you confirm CLASS-FIT VALIDATION MET, HEADROOM NOT MET for ALL and for MARG, IDENTITY AS DERIVED for O6/PC/FK, REPORTED for NC1-3/LIM, and D7 empty?
(2) Is NO-GO right? Give the exact permitted wording for the decision and the result (what may and may not be said under C7.4 and E38-15).
(3) How should the oracle comparison (O6 global 0.0799 vs O6 class 0.0166; "about 4/5 of oracle headroom came from M-1 structure") and the weighting note (MARG weighted 0.01769 vs unweighted 0.02011) be stated in the record?
(4) Is RL-14 (attempt 1 as administrative preflight refusal; one attempt 2 under Addendum 1 + Note 1) acceptable, and is any further record needed?
(5) Next step - recommend ONE, with conditions: (a) close C-kappa; (b) redesign for real headroom - and if so, what could plausibly work, given that R does not scale with eps; or (c) hand the lessons (instrument validation on synthetic plants, within-system comparisons, governed pooling) to Track B (see I).
(6) Overall verdict, and any change to the claim ceiling (restate it if it changes).
