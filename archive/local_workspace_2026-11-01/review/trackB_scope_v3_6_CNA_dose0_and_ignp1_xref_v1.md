# Track B v3.6 freeze prep: CNA on dose 0 for the IGN rows, NC2r/LIM calibration membership, and the IGN-P1 x_ref conflict (CNA v1)

**Author:** CNA. **Written:** 2026-11-01, about 11:35 AM ET. **STATUS: PLANNING/AUDIT RECORD. DRAFT, NOT FROZEN.** Additive; no existing file is modified. Nothing here authorizes execution: no training, simulation, Monte Carlo, Stage 0, calibration, pilot, timing or checkpoint inspection, and nothing was run or timed. The only computation was closed-form arithmetic on standard distributions (half-normal and chi quantiles and tails; /tmp/sv/bin/python, scipy 1.18.1). X1–X5 and the claim ceiling are unchanged. No consciousness claim.
**Convention:** "RD Ln" = review/trackB_ign_cost_v1_lightpass_items2to4_RD.md (sha256 d5ee9a1b3790aa71a6585ee77ef46bccff552e938e79d849d7cb9a78e430bdc1, recomputed: MATCH). "CNA2 Ln" = review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md (17832b01…). "S2.1 Ln" = merged scope v2.1. "M Lnnnn" = merged v3.6 (ab80afa5…). "MP Ln" = measurement plan v1 (1d5458e3…). "CNA3 Ln" = review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md (5dec96f5…), the source of M L1126–L1130.

## A. Dose 0
**Governing text.** CNA2 L242: "Each specificity row has at least two **required doses** … plus a dose-0 sanity level that is REPORTED only. All required doses are listed in §2.6. Only required doses enter the label." CNA2 L328: "about 2–3 required doses each plus dose 0, each at R prespecified replicates". M L1951 runs the calibration loop over "each … generator g and required dose k".

**A1. Which IGN rows have a dose-0 arm (text-determined).** Dose 0 attaches to *specificity* rows only (CNA2 L242). In the IGN table (CNA2 §1.5) the specificity roles are:
| Row | Role text | Dose-0 arm |
|---|---|---|
| IGN-NC1 (CNA2 L185, L296) | "Confound, specificity" | yes |
| IGN-NC2 (CNA2 L186, L297) | "Confound, specificity" | yes |
| BOTTLENECK-ONLY (CNA2 L188, L298) | "specificity for joint IGN∧BCAST" | yes |
| RAND-INIT (CNA2 L189, L289) | "specificity for C-LEARN-on-IGN" | yes |
| Architecture-imposed (CNA2 L134, L290) | C-LEARN specificity (imposed bimodality) | yes |
| IGN-P1, IGN-N1 (L183–L184) | P, N | no (not specificity) |
| IGN-NC2r (L187) | "**Mechanism-present**" | no |
| IGN-LIM (L190, L308) | "Designated limitation test", "2 levels each", construction check | no |
**Count: d0 = 5** (the upper end of RD L100's {0…5}). Three of the five (BOTTLENECK, RAND-INIT, Architecture-imposed) are network-type cells.

**A2. Run policy (text-determined).**
- **Not calibration.** Dose 0 is not a required dose (CNA2 L242), and the loop runs over required doses only (M L1951). It adds no calibration or 3a cell and no term to n_seed selection (M L2785, L3175). RD L100 agrees.
- **Confirmation-run, not derived from existing arms.** CNA2 L328 says dose 0 runs "at R prespecified replicates", and M L375 says R_rep = 200 fresh replicates "per generator and dose". No text says that a dose-0 level may be read off another row's arms. So each dose-0 cell is a fresh confirmation arm at R_rep = 200 and the frozen n_seed. It is REPORTED only and enters no label (CNA2 L242). It never changes n_seed, and a dose-0 result can never block or pass a row. Cost: 914,400·n_seed* trials per cell (RD L100).
- No arm may be reused for it: for example, IGN-NC1 at Δs = 0 is not the IGN-N1 arm unless the plants are identical, and the text does not say they are.

**A3. Dose-0 parameter values (genuinely unspecified; PROPOSED for a Lead ruling).** Rule: dose 0 = the row's construction with the confound mechanism switched off and everything else unchanged.
- NC1: Δs = 0, giving two identical graded subpopulations.
- NC2: no clip (ceiling = the 1.0 quantile).
- BOTTLENECK-ONLY and Architecture-imposed: the gate replaced by a linear (non-thresholding) gate over the probed range, at the same read-out width.
- RAND-INIT: its dose is a ratio to the declared init gain (CNA2 L289), so it has no natural "off" value. **Lead choice:** either define dose 0 as g_0 → 0 (no recurrence at init) or drop it. Dropping it gives d0 = 4.

**A4. NC2r and LIM calibration membership.**
- **Is it mine?** The row roles are my scope text (CNA2 L187, L190, L257, L308), so CNA can state the scope reading. Membership itself is a Lead ruling under M L2785. Neither row appears in M: grep finds no "NC2r" and no "IGN-LIM" in v3.6, and the M L2785 required-row list ("positives, negatives, specificity and confound rows, including RCAL-ADV, NLN and ATTR-P1") names neither.
- **NC2r: its gate depends on a calibrated n_seed, but as written the row is out.**
  - Its expected outcome is "C-IGN MET" (CNA2 L187), scored in layer (i) with e_exp = 1.0 (CNA2 L259). A MET rate on the seed-pooled dip/D statistic rises with n_seed. The only frozen precedent for a mechanism-present gate is MIXED-CODE: "one-sided 95% Clopper–Pearson lower bound of the MET rate ≥ 0.90" (M L1536). That is n_seed-dependent.
  - As written, NC2r has no required dose (it is absent from CNA2 §2.6 L284–L310, and its dose parameter is PENDING per RD L110), and it "Challenges only the 'not imposed by architecture' (C-LEARN) reading" (L187). That reading is already tested by Architecture-imposed (L290).
  - **Scope answer:** OUT (REPORTED, confirmation-only at the inherited n_seed). If the Lead makes it a required check, it must go IN. A required n_seed-dependent gate at an inherited n_seed could fail in confirmation without being in the selection set.
- **LIM: the gate is required. Whether it is out depends on a rule that is still absent.**
  - Its gate is "Correct UNAVAILABLE on LIM ≥ 0.90" (MP L199), with a Clopper–Pearson one-sided 95% rule (M L345). It is required at Stage 0.
  - The scope text makes it a "Construction check only (out of range by design)" (CNA2 L308). It is not listed at M L2785. Its trigger is MP L79, "s* lies outside the probed grid".
  - **Scope answer:** OUT, at the inherited n_seed, **provided** the frozen MP L79 decision is n_seed-independent (for example, no near-transition bin is selectable inside the grid). The s* fit procedure is still ABSENT (E49 file §2(c)). If the frozen rule estimates s* from pooled data, its error rate depends on n_seed, and LIM must go IN.
  - **Flag for the Lead:** fix that rule before ruling.

## B. IGN-P1 x_ref: CNA REJECTS RD's proposal (and the Lead's provisional adoption) for scalar plants
**The two texts.**
- **Text A** (S2.1 L240, L242; M L314). Each trial starts from "a **reset to the low attractor x_lo**". "In IGN-P1, x_ref = x_lo, so plant and instrument share one definition."
- **Text B** (M L1127–L1129 = CNA3 L437–L439, my own text). "t_s = 5τ in plants … t_r = 3τ in plants". Tolerance = "2 × the median absolute deviation of ‖x_ref − median x_ref‖ in null-input runs".

**Reason 1 (decisive): Text B makes IGN-P1 fail coverage by construction.**
- With process noise ξ (M L1126), the end-of-settling state near the stable point x_lo is, to first order, a stationary Ornstein–Uhlenbeck (OU) state. Linear drift is −(1 − g·sech²(g·x_lo + s))/τ. So x_ref − median x_ref is Gaussian with some σ, and d = ‖x_ref − median‖ is half-normal in 1-D.
- The excluded fraction is therefore **scale-free**: it does not depend on σ, g or τ. These are closed-form values, not simulated:
  - **Reading I** (tolerance = 2·median d): tolerance = 1.3490σ, and P(exclude) = **0.1773**.
  - **Reading II** (tolerance = 2·MAD of d): tolerance = 0.7982σ, and P(exclude) = **0.4248**.
- Per-trial eligibility is then 0.823 or 0.575. The coverage gate (M L1130: CP lower bound of the eligible fraction ≥ 0.90 at every required and near-transition bin) cannot pass, so IGN would be UNRESOLVED and the known answer MET would be lost.
- This also contradicts CNA2 L259: "P rows and mechanism-present (reclassified) rows: e_exp = 1.0 by construction". The same applies to every scalar IGN plant: N1, NC1, NC2, NC2r and LIM.

**Reason 2.** Text A is the explicit, line-specific definition. It appears twice (S2.1 L240/L242 and M L314), and it is the reason the plant and instrument share one definition. Text B's plant clause is my CNA3 L437 error: the "residual e^−5 < 1%" rationale presumes an off-attractor start, but the reset is to the attractor. I withdraw the plant half of CNA3 L437.

**Reason 3.** #42 L221's purpose (an exercised settling-exclusion path with coverage checks) is still met. The network-type IGN rows settle under S2.1 L242 (ii-a), namely RAND-INIT, Architecture-imposed and BOTTLENECK-ONLY (7 of the 16 RD cells, RD cell table), so the path is exercised in Stage 0 where it applies.

**Replacement wording (for the Lead's merge; M L314 unchanged).**
- **M L1127 (settling length).** "t_s = 0 in scalar plants: each trial starts from the analytic reset x(t_0) = x_lo and x_ref = x_lo (S2.1 L240, L242; M L314); no settling, so no trial is excluded on this gate and e_exp = 1.0 by construction (CNA2 L259). Networks: 20 steps (rationale unchanged)."
- **M L1129 (tolerance).** Prefix "Network instruments only."

**Effect on the known answer and cost.**
- **Known answer:** unchanged (IGN-P1 MET, bimodal near s*). Under Text B it would become UNRESOLVED by construction.
- **Cost:** each plant trial is t_r,max long, not 5τ + t_r,max. Against LC's 8τ basis (RD L128), that is 3/8 at t_r,max = 3τ, or 5/8 at the proposed grid maximum of 5τ.
**Second defect, network side (CNA's own CNA3 L439 text; flagged for the Lead and possibly #50).**
- The 2×MAD tolerance's exclusion rate depends on dimension. For an isotropic Gaussian settled state in d dimensions under Reading I, P(exclude) is:
  - d = 1: 0.1773
  - d = 2: 0.0625
  - d = 3: 0.0237
  - d = 4: 0.0094
  - d = 8: 0.0003
- Anisotropy behaves like a lower d. A low-dimensional workspace could fail coverage purely through this rule.
- **PROPOSED replacement:** tolerance = the 0.99 quantile of ‖x_ref − median x_ref‖ over null-input runs on the fitting partition. That gives about 1% expected exclusion in any dimension and is still chosen without w.
- Separately, Reading I vs Reading II must be pinned whichever rule is kept.

## C. Δt and the t_r grid: missing inputs for the Lead
- **Δt: ABSENT** in S2.1, M, MP and CNA3. LC L86 (via RD L56) costs both τ/20 and τ/100.
  - Constraint: the linearized drift rate is at most 1/τ, so explicit Euler–Maruyama needs Δt ≤ τ/20 (≤ 5% decay per step) for accuracy. Every t_r must be an integer multiple of Δt.
  - **PROPOSED Δt = τ/100**, with τ/20 as the floor. Any discretization-sensitivity check is a pre-freeze item and is not run here.
- **Noise discretization: PENDING.**
  - Placement conflict: MP L84 puts ξ inside tanh, but M L1126 states it as process noise scaled by ‖x_hi − x_lo‖.
  - PROPOSED: additive Wiener increment, variance (0.05·‖x_hi − x_lo‖)²·Δt per step ("per unit time", M L1126).
- **t_r grid: ABSENT.** M L377 freezes "the IGN t_r grid" but gives no values; M L1128 gives only t_r = 3τ (plants) and 5 steps (networks).
  - Constraints: the grid must contain 3τ and 5 steps. Its lower end must exceed the rise time of a suprathreshold trial, and its span must cover the slower near-s* ignitions (critical slowing).
  - **PROPOSED:** plants {2τ, 3τ, 5τ}; networks {3, 5, 8} steps.
  - All candidates are read from one trajectory per trial on the selection partition (M L376), so only t_r,max costs.
- **Steps per trial.**
  - Scalar plants (Text A): N_steps = t_r,max/Δt. At the proposed values (5τ, τ/100) that is **500**. At τ/20 it is 100. If the grid is {3τ}, it is 300 or 60.
  - Text B, for reference only: (5τ + t_r,max)/Δt = 1000 or 200, and 800 or 160 at 3τ (= LC's 8τ basis).
  - Networks: N_steps = t_s + t_r,max = 20 + 8 = **28** agent steps at the proposed grid, or 25 at t_r = 5.
  - All numbers are PROPOSED; the Lead recosts.

## D. Open items
| # | Item | Owner |
|---|---|---|
| D1 | RAND-INIT dose 0: define as g_0 → 0, or drop (d0 = 5 or 4) | Lead |
| D2 | NC2r required or REPORTED (sets IN or OUT) | Lead |
| D3 | MP L79 rule: n_seed-independent or not (sets LIM OUT or IN) | Lead / RD |
| D4 | Confirm REJECT of Text B for scalar plants; merge the M L1127/L1129 wording | Lead |
| D5 | Network tolerance rule (quantile proposal) and Reading I vs II | Lead; possibly #50 |
| D6 | Δt, noise discretization and t_r grid values | Lead |

*DRAFT. Planning only. Nothing was run or timed. X1–X5 and the claim ceiling unchanged. No consciousness claim.*
---
sha256 of all content above this line: 550617f12839a198cb6ad09728aff92f9cb93aa6f9fe06f9ae6be8f65ce4f627
