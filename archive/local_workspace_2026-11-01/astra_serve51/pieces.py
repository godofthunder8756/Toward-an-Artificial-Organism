# Text pieces for consult #51 (exec'd by build.py). {X} placeholders are filled by build.py from verified hashes.
CEILING = ("Stage-0 success establishes only the measured operating characteristics of the declared instruments on the declared plants "
           "and confounds. It does not establish their validity on trained agents, identify a self-model from decodability alone, or "
           "establish endogenous necessity from selective intervention impairment.")
Q50 = [(41, '(d) Yes: the conservative denominator is n4+n4b+n5.'),
       (58, 'A branch can be designated analytically inapplicable before execution only with an applicable construction-level proof.'),
       (56, 'Their causes and realization treatment remain different; their absence cannot demonstrate an unmeasured operating characteristic.'),
       (125, 'Use the 990th ordered distance as the threshold, with a fixed tie rule.'),
       (248, 'E50-5. Complete the workload ledger, including omitted calibration and inference work.'),
       (250, 'no freeze, execution or timing run is authorized.')]
QM = [(3422, 'it stays in every denominator as a non-success'), (2009, 'bin shortfall'), (2784, 'do not stop at the first passing n.')]
QMP = [(69, 'from 5-fold cross-validation over trials within a seed')]
BODY = '''Consult #51 - TRACK B FREEZE PREPARATION v2.6 (design only): are E50-1..E50-5 closed, and accept/reject the named pre-data amendments. NOT a freeze, execution, timing or approval request. Challenge, don't endorse. High effort. Please wait for all parts (see END marker), then answer in plain ASCII.

== N. COVER ==

N1. Status. DRAFT, NOT FROZEN, DESIGN ONLY, NOTHING RUNS. No plant, instrument, harness, benchmark or timing run exists or was run, and none is requested: no freeze, execution or timing run is requested in this consult (your A50 L250: "no freeze, execution or timing run is authorized."). Computation this round: SHA-256, exact integer/rational arithmetic, closed forms and deterministic float64 evaluation of closed forms and of the noise-free recursion (no RNG, no simulation). Every CPU-hour figure is arithmetic on stated per-unit costs and is UNVERIFIED. ASCII: tau, sigma, theta, lambda spelled out; "A50 Ln" = your raw #50 line; "M Lnnnn" = merged scope v3.6; "MP Ln" = measurement plan v1; "CNA2 Ln" = CNA v2 half.

N2. Bounded. No instrument, arm, plant or question family is added. All changes are prospective, pre-data rulings by the Lead under Amendment A-2026-10-24 (GA-1 and A-2026-10-24 approved by Aidan, 2026-11-01 10:58 AM ET), adopted before any calibration, pilot, feasibility or diagnostic output exists. Any benchmark or timing run (incl. an S0 preflight) would need its own protocol, your review AND Aidan's explicit yes; none is planned.

N3. Sources (sha256 prefixes re-verified by the build script): v2.6 consolidated {V26}; Lead E50-5 workload ledger {WL}; CNA E50-1/E50-3 {CE50} with addendum 1 {CE50A1} and erratum 1 {CE50E1}; CNA pending parameters {PP}; RD E50-2/E50-4 {RD26} with corr1 {RD26C1} and corr2 {RD26C2}; RD light pass of CNA E50-1/E50-3 {RDLP}; RD light pass of the parameters {RDPP}; your raw #50 {A50}; v2.5 {V25}; merged v3.6 {M}; MP {MP}; CNA2 {CNA2}; amendment record {AMD} (unchanged).

N4. Claim ceiling (#41 L304, verbatim, unchanged): "{CEILING}" Safety: X1-X5 unchanged; no host coupling; "no additional stop-associated reward, penalty or terminal return" (#42 L223); no consciousness claim is made or implied.

== R. HOW E50-1..E50-5 WERE ADDRESSED (v2.6 S1-S6) ==

R1. E50-1 (GA-1). Truth table v3, one row per replicate in precedence order: 0 construction failure / INCOMPLETE; 1 all-D; 2 N (pr_i = 0); 3 Q-insufficient; 4 NOT MET; 4B BOUNDARY (computed non-licence); 4U UNRESOLVED (unavailable assessment); 5 MET. Plant realization pr_i (E5 checks 1-2, not row 0) replaces real_i*elig_i; PR >= 188/200. Availability: n_cons = n4 + n4B + n4U + n5 >= 36. Literal rate FL_lit = n5/(n4 + n4B + n5) and decisive-only n5/(n4 + n5) are REPORTED. Binding screen S_cons = (n5 + n4B + n4U)/(n4 + n4B + n4U + n5) (your literal A50 L41: "(d) Yes: the conservative denominator is n4+n4b+n5."), described as a combined specificity/informativeness screen; 4b-share cap withdrawn. ROW0-FL: a per-(seed, bin) quota shortfall makes the replicate INCOMPLETE (M L2009, "bin shortfall"), placed in row 0 under reason QUOTA-SHORTFALL: pr_i = 0 and kept in the 200; OUTSIDE S_cons; ADVERSE in both numerator and denominator of a second binding screen S_wc = (n5 + n4B + n4U + n0Q)/(n4 + n4B + n4U + n5 + n0Q); any licence in it -> row FAIL. This is a named override of M L3422 ("it stays in every denominator as a non-success"), because counting a shortfall as a non-event would lower the screens. Example (exact): 20 adverse of 200 FAIL (CP upper 0.142); recasting 12 as shortfalls gives S_cons 8/188 (CP upper 0.0755, PASS) but S_wc 20/200 -> FAIL; largest passing count at 200 is 9. Row outcome, first match: (1) licence in row 0 -> FAIL; (2) available and S_cons or S_wc violated -> FAIL; (3) PR CP lower < 0.90 -> UNRESOLVED (confound not realized); (4) n_cons < 36 -> UNRESOLVED (insufficient support), whatever row removed the support; (5) else PASS. NOT ASSESSED is never PASS. Narrowing of rows 1/2/3/4b stays closed unless a construction-level proof made before execution is filed.

R2. E50-2. s-hat* = -theta0/theta1 from the frozen H1 logistic on selection data (per replicate and c-level, pooled across seeds); fixed bound [s_1, s_9]; outside or non-locatable -> UNAVAILABLE. Gates G-i/G-ii/G-iii with precedence; G-ii is the quota (shortfall -> INCOMPLETE, R1). IGN-LIM is IN calibration: deterministic gate fixture on the analytic s*_LIM (OUTSIDE-HIGH for LIM/0, OUTSIDE-LOW for LIM/1) plus full calibration and confirmation of the estimated path. Cells: C_cal (15) = IGN-P1/0, IGN-N1/0, IGN-NC1/0, IGN-NC1/1, IGN-NC2/0, IGN-NC2/1, IGN-LIM/0, IGN-LIM/1 (scalar); BOTT/0, BOTT/1, RINIT/0, RINIT/1, RINIT/2, ARCH/0, ARCH/1 (network). C_conf (20) = those 15 + IGN-NC2r/0, IGN-NC1/D0, IGN-NC2/D0, BOTT/D0, ARCH/D0. RAND-INIT dose 0 dropped (named); NC2r demoted to descriptive (validation role withdrawn). Hysteresis scheduled as REPORTED only (<= 27,828,000 trial-equivalents).

R3. E50-3 (scalar plants). One sigma_ref = 0.05*Delta_ref per tau for every scalar row, Delta_ref = 2x* from the bistable IGN-P1 reference at s = 0 (g = 2.0: x* = 0.9575040240772688, sigma_ref = 0.09575040240772688; float64 hex frozen at freeze; never recomputed from a row's own attractors). Domains: tau = 1; graded g in [0, 0.8]; bistable g in [1.25, 4]; g = 1 excluded. Gains g_P1 = g_LIM = 2.0, graded g = 0.5. Root rule: float64 bisection, exactly 100 iterations, no early exit (graded bracket [-1, 1]; bistable [1e-3, 1] at s = 0), replacing the earlier fixed-point iteration; assertions -> construction failure: effective input u = s - theta non-finite or |u| > S_max = 8 (swept over the whole frozen input table); no sign change; |F| > 1e-12; stability margin lambda <= 0; bistable x* < 0.6; any non-finite; x0 := 0 iff u = 0 exactly; integer n_EM = t_r*100*G as literal integers plus a readout-counter check; 0 < h*lambda < 2. Validated object: the discrete Euler-Maruyama recursion; the SDE is interpretation only. Scalar plants t_s = 0 (analytic reset to x_lo); M L1127's 5 tau settling applies to networks only. Grids: s = fl(s_c*m)/4, integer m, s_c(2) = 0.532839975353552, frozen hex; LIM grids shifted -/+7 steps (transition 3 steps outside). Scalar Var(w) floor (0.01*Delta_ref)^2 = 3.6673e-4 (linearised pure noise 5.28-9.05x above it over t_r in {2,3,5}). NC2 ceiling = type-1 quantile of the 9 noise-free grid readouts, per t_r, frozen hex; clip post-readout only; bitwise pre-nonlinearity fixture.

R4. E50-4 (networks). Centre = coordinatewise median of n_c = 101 null-centre runs; threshold from n_q = 1,000 separate null-quantile runs (distinct RNG roles, never reused); T = X_(r_q), no interpolation; eligible iff d <= T. Rank r_q = ceil(0.99*(n_q + 1)) = 991 at n_q = 1,000, one rank above your 990th (A50 L125: "Use the 990th ordered distance as the threshold, with a fixed tie rule."). Event wording: "coverage < 0.97" = P[Bin(n_q, 0.97) >= r_q] = 5.6601e-06 at 991 (1.8130e-05 at 990, your A50 L130), per threshold, not simultaneous. n_q >= 199 is a construction requirement (for 99 <= n_q <= 198, r_q = n_q). Symbols renamed k_FY (Fisher-Yates index), n_EM (EM steps), r_q (rank).

R5. Fitter and Delta-LL. Delta-LL is held-out on the final partition (H0/H1 fitted per seed on that seed's 2,286 fitting trials, scored on its 1,143 final trials); cross-validation is NOT run (MP L69 said "from 5-fold cross-validation over trials within a seed", which would fit on final trials). Anti-leak pins: per-seed fits; starts and scales only from the partition being fitted; Ashman D from the fitting-partition fit. Fitter: L-BFGS-B, analytic gradients, objective = mean per-trial NLL, ftol 1e-10, absolute gtol 1e-8, maxiter 1,000, three deterministic restarts, integer status check, single-threaded BLAS. Library pin PROVISIONAL (scipy 1.18.1 / numpy 2.5.4, UNVERIFIED for the run environment, confirmed at freeze). Dose calibration: n_dc = 9 seeds per replicate, R_cal,dose = 50; under the NC2 rule only network cells can need it: max 72,009,000 trials (K_dc = 5 placeholder, PENDING).

R6. E50-5 (workload; v2.6 S6). Scheduled trials 4,005,072,000 + 45,720,000*n_seed* = {T67} at 67, {T9} at 9 (15/20 cells; supersedes v2.5's 13-cell figures). Newly ledgered at 67: null-centre {NC} and null-quantile {NQ} runs (20 steps each); dose calibration 0-72,009,000; hysteresis {HY}; fits {FL}-{FH}; dips {DP} (frozen-table p-values); bootstrap B = 10,000 on seed statistics, no refit; KATs negligible. CPU-h (UNVERIFIED, op counts only): about {CL}-{CH} at 67 ({CV} at the illustrative d_h = 256), {CL9}-{CH9} at 9; maximum-cost envelope about {CM} (adds per-test simulated dip p-values). Network terms dominate and scale with d_h^2 times an overhead factor (d_h PENDING, P4). Budgets and caps are set at the scheduled maximum (n_seed* = 67, full GRID, 15 calibration cells); cap-limited work is INCOMPLETE, never passed. Early stopping is NOT adopted: the full grid governs (M L2784, "do not stop at the first passing n."), so the full-grid cost is the expenditure. A later amendment could adopt it only by explicitly superseding the full-grid rule, keeping maximum-cost accounting and reporting later points NOT RUN BY DESIGN, with your A50 L74-L82 requirements.

== A. NAMED PRE-DATA AMENDMENTS UNDER A-2026-10-24 (for Q2) ==

AM-1 ROW0-FL: overrides M L3422 for the GA-1 false-licence screens (R1).
AM-2 Delta-LL-HO: replaces MP L69's 5-fold cross-validation with held-out final-partition Delta-LL (R5).
AM-3 NC2 ceiling: redefines CNA2 L297 ("quantile of the unclipped output distribution") as the type-1 quantile of the noise-free grid readouts, per t_r (R3).
AM-4 Scalar-plant t_s = 0: replaces M L1127's "t_s = 5 tau in plants"; settling and its tolerance apply to networks only (R3).
AM-5 RAND-INIT dose-0 drop: departs from CNA2 L242's dose-0 level for each specificity row (R2).
AM-6 NC2r demoted to descriptive: validation role withdrawn (R2).
AM-7 LIM in calibration: C_cal 13 -> 15 (R2).
AM-8 S_cons and S_wc thresholds: new pre-data binding thresholds, point <= 0.05 AND one-sided 95% CP upper <= 0.08 for both screens (R1).
AM-9 100-iteration float64 bisection replacing the earlier fixed-point iteration for x_lo (R3).
AM-10 n_q >= 199 construction requirement (R4).
AM-11 r_q = 991 (ceil(0.99*(n_q + 1))) replacing your 990th ordered distance (R4).

== Q. QUESTIONS ==

Q0. Verdict: are E50-1, E50-2, E50-3, E50-4 and E50-5 each CLOSED / CLOSED WITH NUMBERED EDITS / NOT CLOSED (which)?

Q1. GA-1 (R1; AM-1, AM-8). (a) Are the S_cons and S_wc thresholds (point <= 0.05 AND one-sided 95% CP upper <= 0.08 for each; both binding; availability n_cons >= 36 on S_cons's denominator) acceptable? (b) Is ROW0-FL acceptable: quota-shortfall INCOMPLETE in row 0 with pr_i = 0 and kept in the 200, outside S_cons (your literal L41 denominator), adverse in numerator and denominator of S_wc, any licence -> FAIL? Is overriding M L3422 this way the right direction? (c) Is the five-step row outcome correct?

Q2. Named amendments AM-1 to AM-11 (section A): for each, ACCEPT or REJECT (with the reason or required edit).

Q3. Network quantile (R4; AM-10, AM-11). We depart from your 990th: r_q = ceil(0.99*(n_q + 1)) = 991 at n_q = 1,000. Accept or reject? Is the event wording "coverage < 0.97" = P[Bin(n_q, 0.97) >= r_q] = 5.6601e-06, per threshold, correct? Is n_q >= 199 as a construction requirement correct?

Q4. Parameters, root rule, fitter (R3, R5; AM-9). Are the gains (2.0 / 0.5), sigma_ref, domains, grids, LIM offsets, scalar floor, NC2 ceiling, n_c = 101, n_q = 1,000 and n_dc = 9 sound? Is the 100-iteration float64 bisection with its assertions (S_max = 8, x0 key, integer n_EM, readout counter) a complete root rule and failure rule? Is the fitter pin (L-BFGS-B, mean-NLL objective, absolute gtol 1e-8, deterministic restarts; library PROVISIONAL) acceptable?

Q5. Workload (R6). Is the ledger complete now? Is maximum-cost accounting (caps at the scheduled maximum) correct, and is "early stopping NOT adopted; the full grid governs" a consistent reading of your Q2 ruling?

Q6. One line: we read A50 L56-L58 as "no narrowing of rows 1/2/3/4b from the insufficient-support rule unless an applicable construction-level proof, made before execution, is filed" ("A branch can be designated analytically inapplicable before execution only with an applicable construction-level proof."). Correct?

Still PENDING (not separate questions): network Var(w) floor; K_dc; network width d_h (P4); fitter library versions; pinned libm and hex KATs (P6); per-ledger caps (P5).

Answer format: Q0 first, then Q1-Q6, then numbered required items E51-n (if any) and a one-line VERDICT. Plain ASCII please.
'''
