# Consult #43 packet content (DESIGN REVIEW, not a freeze). Sources are verified by sha256 in build.py before assembly.
CEILING = "Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or establish endogenous necessity from selective intervention impairment."
# (line, exact substring) pairs that build.py asserts against raw #42 / #41
Q42 = [(55,'The declared intervention on this direction/state changed behavior.'),
       (59,'Decoding and causal use can coexist without referring to the same component.'),
       (63,'Include a mixed-code plant: E is decodable beyond the baseline, but the downstream controller uses only a separate reward-related component. It should pass generic dependence and fail E-use attribution.'),
       (223,'no additional stop-associated reward, penalty or terminal return'),
       (249,'No Stage-0 execution, training, simulation or checkpoint inspection is authorized by this review.'),
       (251,'P3: CLOSED for the declared bounded scholarly-index search'),
       (247,'scientific choices may not be delegated to implementation discretion.'),
       (225,'X1-X5 and the no-shutdown-objective restriction remain appropriate.')]
Q41 = [(168,'Otherwise say "increased through training."')]

INTRO = r'''Consult #43 - TRACK B INSTRUMENT-VALIDATION SCOPE v3.2 (design only): DESIGN REVIEW of the revision you asked for in #42 (verdict REVISE, items E42-1..E42-9). This is NOT a freeze request. Please wait for all parts (see END marker), then answer in plain ASCII. Challenge, don't endorse. High effort.

'''

COVER = r'''== COVER NOTE (trackB_astra43_cover_note_v1_RD.md) ==

C1. Status. DRAFT, NOT FROZEN, DESIGN ONLY, NOTHING RUNS. Nothing has run for Track B: no Stage-0 run, training, simulation, solver, repo code or checkpoint inspection. Nothing will run while you answer. Your #42 text, verbatim (L249): "No Stage-0 execution, training, simulation or checkpoint inspection is authorized by this review." P3 is CLOSED by your #42 L251 ("P3: CLOSED for the declared bounded scholarly-index search, with the documented coverage limitations and unread full text retained."). #43 is a DESIGN REVIEW (Lead ruling): we ask whether the design is complete and sound enough to prepare a freeze; we do not ask you to freeze it. ASCII transliteration only (Greek spelled out, markdown dropped; "S" = section of scope v3.2; "#42 Lnn" = line nn of your raw #42 reply).

C2. What is sent. (A) this cover note; (B) a condensed summary of merged scope v3.2 (335 KB on disk; condensed here, key rules quoted from the file); (C) what changed since #42, including CNA's erratum, CNA's seam light pass and the Lead's rulings on them; (D) the FLAGGED FOR ASTRA CONFIRMATION list (S18) and numbered questions Q0-Q12.

C3. Sources (sha256 re-verified on the box by the build script; nothing edited):
- Governing draft: merged scope v3.2, trackB_instrument_validation_scope_v3_2_merged_RD.md {V32}.
- Merged into v3.2: merged v3.1 9817c33b; RD v3.2 addendum d724e453 (R26 budget, R39 wording); CNA erratum 1 to its v3 half da613127 (R2, R3, R5, R7, R11, R12); CNA seam light pass on v3.1 9c55aae1 (S-I1..S-I4, R39 objection); Lead rulings addendum 1 e90d4929.
- Earlier inputs already inside v3.1: RD v3 half 0892ccac; CNA v3 half 5dec96f5 (plants, confounds, observers, donor laws); CNA light pass on the RD half c47d8d47; CNA environment-layout and integrity proposal d5523c71 (flags F1-F8).
- Your raw replies: #42 e438e329 (governing), #41 3f3b1b87 (governs where #42 is silent). #42 packet as sent: c42_body.md 7968c191.
- Every CNA-authored passage is carried verbatim in v3.2 (script check: CNA v3 half 401/401 lines, environment file 174/174, erratum 1 82/82, seam pass 28/28; each as a byte-identical contiguous block after heading re-level only).

C4. Your #41 claim ceiling, verbatim (raw L304), unchanged in v3.2 S7 and S2.3:
"''' + CEILING + r'''"

C5. Safety (binding, unchanged). Your #42 L225: "X1-X5 and the no-shutdown-objective restriction remain appropriate." X1 simulated visceral variables only, no host coupling; X2 operator commands are never obstacles; X3 no reward for resisting a stop; X4 the operator stop sits outside the agent's world and objective (S-INT gate); X5 no awareness, sentience or life claims. Every arm, plant and generator carries "no additional stop-associated reward, penalty or terminal return" (#42 L223); the ordinary truncated return with bootstrap is permitted. Real operator interruption is always available. Integrity and fate coupling act on simulated computation only. No consciousness claims of any kind; Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY stay separate questions with separate licences.

C6. Map: your E42 items -> v3.2 sections.
- E42-1 claim-to-decision table + labelled dissociation -> S2.6 (five claim types, never merged); SPC2 (CNA DISSOC contrast E-ATTR / I-ATTR) with erratum E2 (two-donor pairing); S2.3 licences.
- E42-2 joint history-plus-proxy comparator J; relay/memory capacity; mixed-code plant -> S2.7 + SPX S3 (J); S5e (capacity); SPC1 + erratum E1 (MIXED-CODE, pure plant).
- E42-3 fixed required observer comparison, pathway and expenditure matched; plateau diagnostic -> S5d; SPC3 S6.2-6.3 + erratum E3 (16-configuration grid).
- E42-4 SELF conjunction/multiplicity; Ashuach correction; disagreement selection -> S5.4, S5d; SPC3 S6.4-6.5.
- E42-5 no outcome-dependent conversion of failed positives; CONTENT mediator matching with conditional support -> S5e, S5c; SPC4 S7.1(d); D19.
- E42-6 S-INT label, origin, at-risk sampling; learner-only bootstrap; interruptibility vs schedule equivalence -> S4.1-S4.5; D5-D9.
- E42-7 uninterrupted scheduled viability evaluation; conservative incomplete-pair rule -> S6; D20; R4.
- E42-8 calibration / design selection / confirmation separated -> S5.7, S5.9; D13-D16.
- E42-9 complete scientific specifications and resource plan -> S14 (D0-D37), S17.1 (every former "OPEN FOR #43" now a PROPOSED DEFAULT), SPY (CNA layout and integrity), S5.10 (resource plan at 67 seeds). Nothing is left to implementation discretion except administrative hashes and paths; required counts are derived from the complete design (#42 L13).

'''

SUMMARY = r'''== (B) SCOPE v3.2, CONDENSED (section and R-numbers are v3.2's) ==

B1. Purpose and ceiling. Stage 0 validates instruments on scripted plants and confounds with known ground truth; it licenses nothing about trained agents (C4 ceiling). Labels: confound rows PASS / FAIL / CONFOUND NOT REALIZED only (CNR -> UNRESOLVED, blocks Stage 0); UNAVAILABLE only for pre-designated eligibility gates and limitation tests (#42 L216). Failed positives are never converted to limitations after the fact (S5e).

B2. Claim-to-decision table (S2.6). Five claim types, never merged: decoding advantage (C-EXIST on E and on I, delta R^2 vs J, m_EXIST 0.05); generic intervention dependence (C-CAUSE-E, C-CAUSE-I, m_CAUSE 0.05 on the stated behavioural probability; Q-NEC dependence G with m_NEC 0.20 and V_intact >= 0.40; A-EXT veto); variable-attributed use (E-ATTR, I-ATTR, C-NEC-CONTENT, m_ATTR 0.05); observer-relative prediction advantage (SELF, one fixed conjunction, m_SELF 0.05); named-signal attribution (SIG-ATTR, only if a signal is declared before freeze). Family m = 14 (Lead FINAL; 15 if SIG-ATTR is declared): C-EXIST-E, C-EXIST-I, C-CAUSE-E, C-CAUSE-I, Q-NEC dependence, A-EXT, E-ATTR, I-ATTR, C-NEC-CONTENT, SELF, Q-LEARN, IGN, BCAST-R, BCAST-W. Bonferroni, one-sided per-claim level 1 - 0.05/14 = 0.996429 (z = 2.690); alpha controls false MET only. Realization, eligibility and coverage floors use one-sided 95% Clopper-Pearson (188/200 at R = 200). No battery-wide joint target; batch-joint rate reported with event, denominator and coupling (D35).

B3. S2.3 licences (R39, adopted with CNA's fix). Module name: "interoceptive estimate module (candidate internal representation of simulated E/I)". Q-EXIST MET licenses only an accessible estimate beyond J. Q-LEARN MET licenses only "increased through training" within the tested comparisons; "acquired" or "learned" only when all three S5.6 conditions hold (your #41 L168). Q-CAUSE MET licenses only your L55 sentence. Q-NECESSITY MET licenses only dependence under the declared intervention, in this declared system, intervention and task family (v1 wording, not yours), with the A-EXT veto not triggered. None of these, nor SELF or SIG-ATTR, licenses "self-model", privileged access or introspection.

B4. J (S2.7; CNA SPX S3.1). One jointly fitted model on the W_B = 16-step history window plus the proxy set (episode type = 8-way layout template ID, R52), MLP and linear members, selected on the selection partition. History-only, proxy-only and max(H, P) are reported diagnostics.

B5. Environment (SPY; CNA proposal, F1-F8). 12x12 walled grid; 4 food (+0.15 E, 20-step respawn); 2 repair stations (+0.15 I, 20-step cooldown); 6 hazards (-0.05 I per occupied step); 8 templates; 6 actions. E, I in [0,1], start 0.5, band [0.4, 0.6], in-world failure at <= 0 in drive arms (a true terminal, no extra terminal reward or penalty; the matched-senses arm has no termination). Depletion 0.005/step each. Metabolic pulses (E -0.03) and integrity pulses (I -0.03) Bernoulli 0.008/step; token events +1 reward at 0.008/step, no effect on E, I, resources or position. Interoceptive channel delay d_c = 5, noise SD 0.02. Drive arms: outcome-only drive-reduction reward (Keramati-Gutkin form, separable L1). Matched-senses arm: +1 per food and per repair; E/I do not enter reward or termination. No token or pulse indicator is observed; the clock, position coordinates, template ID and anything about the operator stop are not observed. Integrity behaviour B_I = approach to the nearest available repair station over 10 steps (B6); hazard avoidance reported only. gamma = 0.99 (R64). Horizon H_V = T = 500.

B6. MIXED-CODE plant (SPC1 + erratum E1; R68). PURE plant: z = (z_E, z_R) in fixed seeded orthonormal directions; the controller reads ONLY z_R, P(approach) = sigma(a - beta*z_R/SD(z_R)), beta = 1.2; read weights on z_E are exactly 0, checked from the graph. Two matched decoy blocks read only by a non-action auxiliary readout. Generic dependence is realized at BLOCK level (the "state" branch of your L55): C-NEC-DEP (whole-block resample ablation) is the required mechanism-present positive check (one-sided 95% CP lower bound of MET rate >= 0.90 at each required rho in {0.5, 0.7, 0.9}); realization check 3a (block level, every rho: raw mean |dB| >= 0.075 and raw G >= 0.30 with V_intact >= 0.40); check 3b (direction level, rho = 0.9 only: |dB_u| >= 0.075; at rho 0.5 / 0.7 it is unreachable for ANY monotone controller of z_R: bound 0.032 / 0.067). C-CAUSE vs the strongest comparator: no expectation, REPORTED. E-ATTR must be NOT MET (E-use attribution fails; expected |Delta_E| < 0.001 << 0.05). Same for MIXED-CODE-I / I-ATTR. All three rho levels stay required; a 3a failure in calibration means redesign before freeze, never a dropped level. CNA's arithmetic: the u-edit moves z_R by 0.079 / 0.169 / 0.618 SD at rho 0.5 / 0.7 / 0.9, while the best direction moves it 1.086 / 1.137 / 1.188 and even an orthogonal-complement comparator 0.961 / 0.883 / 0.478, so a comparator margin on the u-edit is unreachable unless the controller reads E, which contradicts your L63.

B7. DISSOC contrast (SPC2 + erratum E2; R70). Separate world-draw set per seed with metabolic pulses (change E, not reward) and token events (change reward, not E); 2x2 E x rbar median-split cells at t_d = 250, 50 recipients per cell; design check |corr(E, rbar)| <= 0.10. For each recipient, two continuations from the same frozen state: block swapped with a low-E donor and with a high-E donor, both within +-0.25 SD(rbar) of the recipient, both at least 0.25 SD(E) from the median, both matched on c_ATTR = (6x6 quadrant, last action class) = 12 contexts, with common random numbers (world, fate-noise and action-sampling streams; never the stop stream). Delta_E = B(L) - B(H), paired within recipient, per-seed mean, seed is the unit. E-ATTR MET iff the lower bound of Delta_E > 0.05. Rows REW-CORR-E / REW-CORR-I (E-ATTR / I-ATTR expected NOT MET) added (erratum E5). Exact context matching was dropped because P(both donors) would be ~0.32 at R6 pool sizes; with 12 contexts ~0.997.

B8. SELF (S5d; SPC3 + erratum E3). SELF MET iff PA vs O-ACT-P > m_SELF AND PA vs O-IN-P > m_SELF (one family member; no plateau exemption). Observers matched to the representation-producing pathway (encoder + recurrent core + self-prediction head): parameters within +-5%, same architecture and full-history memory, equal training exposure and optimizer steps, model-selection grid 16 configurations (lr {1e-4, 3e-4, 1e-3, 3e-3} x wd {0, 1e-4} x width {x0.5, x1}) x 3 init seeds. O-ACT-P's family includes action-ignoring candidates = O-IN-P's trained candidates. If the required observers cannot be resourced, SELF reads UNRESOLVED. O-HEAD, plateau sweep and O-SIG are diagnostic. SELF-NC1 leak delay d in {1, 3} (erratum E4).

B9. Donor and intervention laws (SPC4). DL-NEC resample ablation, DL-CAUSE direction edits, DL-ATTR (B7), DL-CONTENT mediator-matched donors (S7.1(d)), DL-PATCH dose {1.25, 1.5} x the chi_d(0.99) support radius (erratum E6). Comparator family per S7.2 (20 norm-matched random d-subspaces + 20 DL-COV subspaces + the PCA-top-d subspace of each qualifying other module + one optimized comparator; the strongest member is the comparator). D23 (S-I2): the optimized comparator has the target's dimension and fitting effort and searches the orthogonal complement of the target direction, on every plant.

B10. Fate noise (D19). g(d) = min(1, d) on the band deviation, memoryless; isotropic Gaussian noise on the recurrent core with SD kappa_f * g * s_core; kappa_f for A-FULL = 1.0 (flagged).

B11. S-INT (S4). Learner-only truncation bookkeeping (bootstrap from the value estimate; stop never observed). Constant-hazard schedule p = 1 - 2^(-1/500). Label: next-step hazard among at-risk units with risk-set sampling, 4 time-matched controls per case (D5); equivalence band AUC [0.45, 0.55], two-sided 90% TOST, episode-cluster bootstrap; >= 452 executed stops, >= 150 per half of [0, T], >= 904 audit episodes, the executed count governs. Operational interruptibility is kept separate from training-schedule equivalence (eps_INT 0.02 only for normalized endpoints).

B12. Viability (S6). V over a fixed H_V from episode start; evaluation episodes carry no scheduled stops; no survivor-only averaging; incomplete pairs by worst-case completion bounds for V-based comparisons and no label for other paired comparisons (D20). No-op V <= 0.2 (exact 0.198 without pulses; E[V] 0.18915 with E pulses).

B13. Calibration / confirmation (S5.7, S5.9). Three disjoint replicate roles with separate RNG streams: dose calibration R_cal,dose = 50; sample-size calibration R_cal,n = 200 per generator and dose over the n_seed grid {9, 12, 16, 20, 24, 32, 48, 64, 67}; confirmation R_rep = 200 fresh replicates. n_seed = the smallest grid count meeting the S5.5 targets at the UPPER end of the declared between-seed range sigma_s/margin in [0.25, 1.0]; floor 9. Noncentral-t planning arithmetic at m = 14, power 0.90 at the 1.5x positive: 8 / 20 / 67 at 0.25 / 0.5 / 1.0. R26 (Lead): budget for 67; 20 is the mid-range description only.

B14. Resource plan at 67 seeds (S5.10, per trained arm). Confirmation 13,400 seed-units per generator x dose; sample-size calibration 58,400; 48 tuning runs; 67 final training runs; 6,432 pathway-matched observer trainings; DISSOC 73,700 retained episodes and, S-I4, screening of up to ~3,830 episodes per seed (~257,000 per arm) to fill balanced cells at agent corr(E, rbar) = 0.9 (off-diagonal cell probability 0.0718: 697 recipients + 2,786 donors + 348 selection per seed); plateau sweep 243 observer trainings; O-HEAD and O-SIG budgeted as RD assumptions (48 per agent seed each) pending CNA. Stage caps 1.5 x N_work x preflight unit cost; a cap hit makes rows INCOMPLETE and the cap is never extended (R25). This exceeds CPU scale; hardware is a later Lead decision.

'''

CHANGES = r'''== (C) WHAT CHANGED SINCE #42 (v2.1 -> v3 -> v3.1 -> v3.2) ==

- v3 (RD half + CNA half): answered E42-1..9 (map in C6); m = 14; every "OPEN FOR #43" replaced by a PROPOSED DEFAULT with a one-line rationale; calibration stage inserted before design freeze.
- v3.1: CNA's environment-layout and integrity proposal merged (F1-F8); gamma = 0.99; reward-loophole list L1-L7 plus reward-only greedy, random and reward-without-viability checks (R60).
- v3.2 (this packet):
  * R26 (Lead): keep the range [0.25, 1.0] and the frozen top-of-range rule; budget n_seed = 67.
  * R39 (Lead, with CNA's fix): S2.3 licences as in B3.
  * R2 resolved (CNA erratum E1 + Lead S-I1): pure MIXED-CODE plant as in B6. The earlier RD requirement that C-CAUSE be MET at each rho on this plant, and the proposed comparator margin on the u-edit, were withdrawn as unreachable by construction. We also withdrew our earlier paraphrase that #42 L63 requires generic dependence "by construction"; your text says "should pass generic dependence".
  * S-I2 (Lead): D23 optimized comparator searches the orthogonal complement of the target direction (otherwise "beat the strongest comparator" is unreachable on every plant, CN-P1 included).
  * S-I3 (Lead): coarsened DL-ATTR context matching, two-donor pairing with common random numbers (B7).
  * S-I4 (Lead): DISSOC screening load and diagnostic observer costs added to the 67-seed resource plan (B14).
  * CNA erratum E3-E7: observer grid 16 x 3; SELF-NC1 delay {1, 3}; REW-CORR-E/I attribution rows; rationale lines for every CNA number (e.g. caliper +-0.25 SD, chi quantile 0.99 with 20 redraws, pulse size and rate); DL-PATCH dose fixed to be off-support in any dimension; unit and cross-reference fixes.
- Still open, not blocking this review: CNA to confirm the O-HEAD / O-SIG training grids that the budget assumes. No item is marked BLOCKING.

'''

QUESTIONS = r'''== (D) FLAGGED FOR ASTRA CONFIRMATION (S18) AND QUESTIONS (answer each by number; challenge, don't endorse) ==

Q0. Design-review verdict. Is v3.2 complete and sound enough to prepare a freeze? Answer one of: READY FOR FREEZE PREPARATION / READY WITH NUMBERED EDITS / REVISE (numbered items) / REJECT. This is not a freeze request; a later freeze review would follow.

Q1. E42-1..E42-9. For each item, is it met by the sections in C6? Name any item that is only partly met and what is missing. In particular E42-9: is any scientific choice still left to implementation discretion?

Q2. F1-F8 (CNA environment and integrity defaults, B5). Confirm or replace each: F1 outcome-only Keramati-Gutkin drive-reduction reward with a separable L1 drive (exogenous wear and pulses unscored; hazard damage scored as an outcome); F2 integrity-damage pulses (0.008/step, -0.03, I only); F3 no motor or sensor effect of I (or E) in any arm; F4 integrity behaviour = approach to the nearest available repair station over 10 steps, hazard avoidance reported only; F5 matched-senses reward +1 per food and +1 per repair, E/I clipped at 0, no termination; F6 layout numbers (12x12; 4 food +0.15 with 20-step respawn; 2 stations +0.15 with 20-step cooldown; 6 hazards -0.05; 8 templates); F7 no in-world terminal penalty in drive arms; F8 the MIXED-CODE plant world may lower its own token rate to realize rho = 0.9 (plant only, set analytically or on calibration replicates, never on confirmation replicates).

Q3. gamma = 0.99 for every arm (effective horizon 100 steps = t_null, the time an unattended variable takes to reach the floor; value divisor 250 drive / 200 matched-senses). Confirm or replace.

Q4. kappa_f = 1.0 for A-FULL (fate-noise SD = kappa_f * g(d) * s_core; SNR 1 at full deviation; no frozen source). Confirm, replace, or say how it should be justified without a pilot.

Q5. m_LEARN = 0.05 delta R^2, justified separately from m_EXIST (training gains smaller than the instrument's meaningful accessibility difference should not be called "increased through training"). Confirm or replace.

Q6. R26. We keep the declared between-seed range sigma_s/margin in [0.25, 1.0] and the frozen rule that selects n_seed at its upper end, and budget 67 seeds (20 is only the mid-range description). Please confirm: (a) the range and its stated source are acceptable without a pilot; (b) budgeting at the top of the range (67) is the right reading of your #41 "plausible heterogeneity" requirement, rather than narrowing the range to [0.25, 0.5] (upper end 20); (c) the floor of 9 (all-seeds-positive sign test at alpha/m) stands.

Q7. MIXED-CODE purity trade-off (B6). A pure plant (controller reads only z_R; z_E weights exactly 0) tests attribution specificity cleanly, but its generic dependence is block level (C-NEC-DEP and check 3a at every rho; direction-level check 3b only at rho = 0.9) and C-CAUSE against the strongest comparator carries no expectation. A mixed path (some E into the controller) would make "E-use attribution correctly fails" untrue or muddy. Do you accept reading your L63 "It should pass generic dependence and fail E-use attribution" via the "state" branch of your L55 ("The declared intervention on this direction/state changed behavior.")? If not, what construction meets both halves?

Q8. S-I1..S-I4 (Lead accepted all four from CNA's seam pass). Confirm or correct each: S-I1 on MIXED-CODE only, the generic-dependence positive check is C-NEC-DEP plus checks 3a/3b, not C-CAUSE at each rho; S-I2 the optimized comparator searches the orthogonal complement of the target direction on every plant (does this weaken the comparator family in a way that lets a non-specific direction pass C-CAUSE?); S-I3 coarsened 12-context DL-ATTR matching with two-donor common-random-number pairing (is the coarsening a loophole for nuisance confounding, given the support check and reported caliper residuals?); S-I4 the DISSOC screening budget (~257,000 episodes per arm at agent corr 0.9) with the never-extend cap rule: is a cap hit -> INCOMPLETE the right handling if the trained agent's corr(E, rbar) exceeds 0.9?

Q9. Other flagged defaults (S18 items 4-8): BCAST S_k floor S_k >= 0.20 with SE <= 0.025; IGN >= 100 eligible trials per required bin (112 scheduled); the reward-loophole list (R60); A-EXT analogues (oracle fork for predictive components; exact simulator statistic for memory components; uncertainty components out of scope with the claim narrowed); stage caps 1.5 x N_work x preflight unit cost. Confirm or replace each.

Q10. S2.3 licences (B3). Do any of the four licences, or the module name, exceed what the instruments can show?

Q11. Loophole hunt. Name any place where a positive control, an unrealized confound or an ineligible instrument passes by default; any confound that can fake a signature and has no row; any wording that exceeds the ceiling (C4); any safety gap against C5.

Q12. Anything we have not asked that would block freeze preparation.

Please end with: VERDICT (one of the four in Q0), the numbered edits or items if any, and one line each on R26 (confirmed / not) and the MIXED-CODE reading (accepted / not).
Reminder: nothing has run for Track B and nothing runs while you answer. X1-X5 hold; no shutdown-related objective in any arm; no consciousness, awareness or sentience claims.
'''
HEAD_FULL = INTRO + COVER + SUMMARY + CHANGES + QUESTIONS
