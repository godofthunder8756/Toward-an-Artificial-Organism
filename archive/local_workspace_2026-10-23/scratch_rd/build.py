import re
s=open('v11.md').read()
def rep(old,new):
    global s
    n=s.count(old); assert n==1,(old[:70],n); s=s.replace(old,new)
def between(a,b,new):
    global s
    i=s.index(a); j=s.index(b,i); s=s[:i]+new+s[j:]

# ---------- header ----------
between("# C-κ class-fit validation package","## 0. Sources, hashes and precedence",
r'''# C-κ class-fit validation package: synthetic-only scope record v1.1

**Status: DRAFT. NOT FROZEN. NOTHING RUNS.** Research Delegate (Track A), 2026-10-22 (ET). This is a new file, and no existing file was edited.

I executed nothing: no training, no solver runs, no simulation, no checkpoint, no oracle code. "RD arithmetic" means my own arithmetic on committed numbers: the exact rationals in `stage_O1.json`, the stored B matrices in `fit_freeze_O6.json`, the Q array in `drawn_arrays.npz`, and the `g_coefficients` in `stage_O7.json`, all in the PR #13 outputs at `14376f38`. Every derived expectation is **UNVERIFIED** until an approved, frozen run. Nothing in this file authorizes execution (E37-9).

**System names (v1.1).** Systems are renamed so that no name collides with E37-4's "prospective S6 design" (the earlier neural design S6 in the oracle records):

| v1 name | v1.1 name | Role |
|---|---|---|
| S1 | **SYS-O6** | Existing affine exact-filter control |
| S2 | **SYS-PC** | Sign-dependent positive control (PC±) |
| S3 | **SYS-FK** | Genuinely fixed-κ control |
| S4 | **SYS-NC1** | O7 smooth symmetric lookup (confound) |
| S5 | **SYS-NC2** | Affine symmetry-breaking lookup (confound) |
| S6 | **SYS-NC3** | Cubic lookup outside the basis (confound) |
| (new) | **SYS-LIM** | Orbit-indexed limit control, REPORTED ONLY |

The bare token "S6" appears in this file only inside the E37-4 quote and in this note. "S12" and "S15" appear only inside quotes.

## Change log relative to v1 (`ckappa_classfit_scope_record_v1_RD.md`, sha256 `11a0a5ee354425423d9f1197dc10119f61e27a8400762a39ad1e3dde827c25ed`; unchanged)

This file is a complete replacement text. It **supersedes** the unposted intermediate `ckappa_classfit_scope_record_v1_1_RD.md` (sha256 `f4814f86262e1bdaf1ad7240e5f906682501712d82a7d5146206699d60e71bce`). That intermediate covered only CNA's second message; it is left unchanged and is non-governing. Both CNA messages were accepted by the Specialist, as relayed by the parent at 2026-10-22 ~11:33 and ~11:37 PM ET.

**From CNA's second message (as in the intermediate):**
1. **SYS-FK scope (C4.3).** κ ≡ 0 is kept, and the record states plainly what it checks. Its responses lie in the μ span, so it passes almost trivially, and its product-chart designs differ from the true-chart designs of SYS-O6, SYS-PC and SYS-LIM. Its design ranks are reported. The κ_a lookup alternative is rejected, because the state carries no prefix identity (E37-6).
2. **Option B as specified in v1 is NOT INFORMATIVE (§6 B-i, B-ii).** Both claims were verified by my own derivation:
   - under SYS-NC1 the floor is ≤ 0 by construction, to first order;
   - minimum-norm spreading over the 2-prefix null space breaks D2 for SYS-PC.
3. **B-repaired (shared e within a fold) is a CANDIDATE.** D2′ is derived (UNVERIFIED), with the identifiability condition dx ≠ 0, dy ≠ 0 and the table of fold values. It departs from E37-5's "separately fitted", which is disclosed.
4. **D2 rank condition.** D2 requires the class design to be resolved at rank 3 (CNA confirms; C4.2(e)).
5. **SYS-NC3 law changed (my finding).** v1's g₃ = c₃μ_x² lay inside the free-row effective basis, so it is replaced by g₃ = c₃μ_x³ (C4.4).

**From CNA's first message (new in this file):**
6. **SYS-LIM added (C4.5).** It is the orbit-indexed limit control, REPORTED ONLY, using the declared midpoint rule for t.
   - All numbers were re-verified from `stage_O1.json` and `fit_freeze_O6.json` (RD arithmetic).
   - Expectations D6 and D7 are derived (UNVERIFIED), and the #37 L112/L114 limit is stated.
   - Behaviour under B-repaired is TO BE FIXED BEFORE FREEZE.
7. **c₂/c₃ rule (C4.4).**
   - The P-weighted RMS ‖Dg‖ over the 16 baseline prefixes is matched to SYS-NC1's (O7's), using the committed `g_coefficients`.
   - If the matched value invalidates a baseline, the system reads NOT ADMISSIBLE, with no rescaling.
   - I checked that the rule is well-defined for g₂ = c₂μ_x and g₃ = c₃μ_x³ and computed the expected values (RD arithmetic).
   - CNA confirmed this rule for the quadratic, which I replaced with the cubic; that is flagged.
8. **P0 step-0 fixture (C4.0).**
   - It runs before any fit.
   - A P0 failure is PIPELINE INVALID on a *derivation premise*.
   - Once P0 has passed, a D1, D2 or D4 failure is an *implementation* failure.
9. **B1 extension kept (C3.9).** CNA withdrew void-and-pool.
10. **Summary split (§7).** The VALIDATION label covers the identities. A separate SYS-PC HEADROOM label covers the class gain. HEADROOM is no longer folded into VALIDATION.
11. **Option C (§6).** Added the falsify-only sentence.
12. **Systems renamed** throughout, as tabled above.
13. **Open questions updated (§11).** Q3, Q5 and Q7 are resolved as CNA proposed, pending Astra. SYS-LIM questions are added.
14. **Smaller changes.**
    - The workload estimate now covers 7 systems.
    - The tighter edit bound uses the stored SDs: sd_x = 0.36806, sd_y = 0.61364, sd_κ = 0.11497, read as B·Q from `fit_freeze_O6.json`.
    - Crossing bounds for SYS-PC and the SYS-FK validity bound were recomputed with these SDs.

''')

# ---------- B1 ----------
rep("CNA's alternative, voiding the class cell and pooling the rest, is OPEN QUESTION Q3.",
"CNA has withdrawn the void-and-pool alternative, so the B1 extension is the only proposal. It is resolved as CNA proposed, pending Astra (Q3).")

# ---------- P0 fixture ----------
rep("and hence **G_{g·a} = R_g G_a R_g**. P0 is UNVERIFIED numerically and is checked by C3.6(e).",
"""and hence **G_{g·a} = R_g G_a R_g**. P0 is UNVERIFIED numerically and is checked as a step-0 fixture (C4.0) before any fit. It is also reported in C3.6(e).

**C4.0 P0 step-0 fixture (v1.1).**
- **When.** After O1 and O2 (E36-13 order) and **before any fit** of any system.
- **What it checks.** On the true-chart closed-form L_a(u) (the designs shared by SYS-O6, SYS-PC and SYS-LIM), for every prefix a, every flip g ∈ {X, Y, XY} and every continuation u:
  - (i) max|L_{g·a}(g·u) − P_g L_a(u) R_g| ≤ tol_P0;
  - (ii) w(g·a, g·u) = w(a,u) (exact rational, as in O1);
  - (iii) max|G_{g·a} − R_g G_a R_g| ≤ tol_P0.
- g·u is the continuation flipped by the same reading mask (`stages.py:221`, masks 85 and 170 on full histories). P_X = diag(−1,1,−1) and P_Y = diag(1,−1,−1) (`world.py:146–150`).
- The same check runs on the SYS-FK product chart and the SYS-NC1 chart, both of which are flip-symmetric, and is reported. SYS-NC2 and SYS-NC3 break the symmetry by design, so P0 is not expected there and is not checked.
- tol_P0 is TO BE FIXED BEFORE FREEZE.
- **Failure semantics.** A P0 failure on the true-chart designs is **PIPELINE INVALID (DERIVATION PREMISE)**: D1, D6 and the orbit-sum statements lose their premise. The package stops before any fit, with no rerun.
  - Once P0 has passed, a later failure of D1, D2 or D4 on a resolved design is **PIPELINE INVALID (IMPLEMENTATION)**. The package also stops, but the diagnosis names implementation, not derivation.
  - This resolves Q5 as CNA proposed, pending Astra.""")

# ---------- c2/c3 rule ----------
rep("""  - c₂: TO BE FIXED BEFORE FREEZE by a rule declared in the frozen file, not by search. The rule must give a valid baseline at all 16 prefixes and must not be chosen on the basis of any gain value.""",
"""  - c₂ is set by the **RMS-matching rule** (C4.4.R). Expected c₂ ≈ +0.100448 (RD arithmetic; UNVERIFIED).""")
rep("""  - c₃: TO BE FIXED BEFORE FREEZE by the same kind of declared rule. Whether this form is acceptable is Q7.
  - No gain expectation. It is reported.""",
"""  - c₃ is set by the **RMS-matching rule** (C4.4.R). Expected c₃ ≈ +0.199056 (RD arithmetic; UNVERIFIED).
  - **Flag.** CNA confirmed the RMS rule for the quadratic μ_x², which I have replaced. Its application to the cubic still needs CNA's and Astra's confirmation (Q7).
  - No gain expectation. It is reported.

**C4.4.R RMS-matching rule for c₂ and c₃ (v1.1; frozen as a rule, not a search).**
- **Rule.** Let ρ(g) = sqrt(Σ_{a=0}^{15} P_a·‖Dg(μ_a)‖²), with P_a the prefix law weights (`stages.py:149–154, 317`) and μ_a the true stage-4 marginals.
  - ρ_NC1 is computed from the **committed** O7 `g_coefficients` (`stage_O7.json`, sha 994dda0a…). SYS-NC1's in-package refit must equal them to the identity tolerance; otherwise INTEGRITY DIAGNOSIS.
  - c₂ and c₃ are the **positive** solutions of ρ(g₂) = ρ_NC1 and ρ(g₃) = ρ_NC1.
  - The values are computed in-package at step 0, before any fit, and recorded. They are never changed afterward.
- **Validity.** If the matched g₂ or g₃ gives any invalid baseline (p < 10⁻⁶ at (μ_a, g(μ_a)) for any of the 16 prefixes), that system reads **RESTRICTED COMPARATOR NOT ADMISSIBLE**. There is no rescaling and no replacement (E36-6, E37-9).
- **Well-definedness (RD arithmetic).**
  - g₂ = c₂μ_x gives ‖Dg₂‖ = |c₂| at every prefix, so ρ(g₂) = |c₂| and c₂ = ρ_NC1. It is unique and positive.
  - g₃ = c₃μ_x³ gives ‖Dg₃‖ = 3|c₃|μ_x², so ρ(g₃) = 3|c₃|·sqrt(E_P[μ_x⁴]). Since E_P[μ_x⁴] > 0 (every |μ_x| ≥ 0.2501), c₃ = ρ_NC1 / (3·sqrt(E_P[μ_x⁴])). It is unique and positive.
- **Expected values (RD arithmetic; UNVERIFIED).**
  - P_a is not stored in the committed outputs, so I inferred it. By flip symmetry the P-weighted means of μ_x, μ_y and κ are 0, so the stored SDs equal the P-weighted RMS values. Solving Σ_o P_o = 1 and Σ_o P_o·(μ_x², μ_y², κ²)_o = (sd_x², sd_y², sd_κ²) gives orbit masses P_A..P_D ≈ (0.31880, 0.23968, 0.24092, 0.20060), with P_a = P_o/4 and condition number ≈ 91.
  - ρ_NC1 ≈ 0.100448. Cross-check: β·sqrt(sd_x² + sd_y²) with β = 0.140378 gives the same value to 10 digits, as expected for g ≈ βμ_xμ_y.
  - c₂ ≈ 0.100448; E_P[μ_x⁴] ≈ 0.028294; c₃ ≈ 0.199056.
  - Baseline validity, min p over the 16 prefixes:
    - SYS-NC1: 0.04527 (prefix 5);
    - SYS-NC2: 0.01837 (prefix 15);
    - SYS-NC3: 0.02427 (prefix 15).

    All exceed 10⁻⁶, so the expected result is ADMISSIBLE for both. The package recomputes this; my inferred P_a does not govern.""")

# ---------- SYS-LIM block ----------
rep("""## 5. Units, edits, masks, weights, groups and tolerances""",
r'''**C4.5 SYS-LIM: orbit-indexed limit control (v1.1; REPORTED ONLY).**
- **Purpose.** It exhibits a κ code that is orbit-coherent (it does not flip with the world's flips) but whose sign is **indexed by the orbit**. No fit type in this package can carry such a code to a held-out orbit whose sign is absent from the fitting set. It never enters VALIDATION or HEADROOM (§7).
- **Orbit statistic and the declared midpoint rule (RD arithmetic from `stage_O1.json` exact rationals).**
  - |μ_x| is flip-invariant, so it is constant within an orbit: A 0.530132, B 0.250064, C 0.253712, D 0.276837.
  - Ordering: **B < C < D < A** (strict).
  - **Midpoint rule (declared):** t = (|μ_x|_D + |μ_x|_A)/2, the midpoint of the largest gap, between the top orbit A and the next one, D. That gives **t ≈ 0.403485**.
  - **Signs:** s_o = +1 if |μ_x| > t, −1 if |μ_x| < t. So **s_A = +1 and s_B = s_C = s_D = −1**.
  - Margins: |μ_x|_A − t = t − |μ_x|_D ≈ 0.126647 (equal, by the midpoint rule). B and C are farther from t.
- **State and readout (autonomous, E37-6).**
  - ψ = (μ_x, μ_y, s(|μ_x|)·κ), with z = Q·D_ψ⁻¹(ψ − ψ̄) and Q from seed 35006 (reused; Q10).
  - ψ₃ is odd under single flips, so its P-weighted mean is 0 and its SD equals sd_κ. Hence **D_ψ = D**, the O6 SDs (0.36806, 0.61364, 0.11497).
  - Readout: recover ψ, then θ = (ψ₁, ψ₂, s(|ψ₁|)·ψ₃). The threshold is read from the state's own |ψ₁|, not from any analyst label.
  - The baseline chart equals the true θ_a, so the global and class designs are **identical to SYS-O6's and SYS-PC's**.
- **Crossing rule and bound.**
  - An edit crosses if |ψ'₁| − t has a different sign from the baseline's, or |ψ'₁| = t. A crossing edit is not scoreable, enters the common mask and is counted, never replaced.
  - Bound: |Δψ₁| ≤ ε·sd_x. With sd_x = 0.36806 (read as B·Q from `fit_freeze_O6.json`; equal in all 6 folds to ≤ 7×10⁻¹⁶):

    | ε_syn | ε·sd_x | margin | crossing possible? |
    |---|---|---|---|
    | 0.02 | 0.00736 | 0.126647 | no |
    | 0.05 | 0.01840 | 0.126647 | no |
    | 0.10 | 0.03681 | 0.126647 | no |
    | 0.25 | 0.09201 | 0.126647 | no |

  - Any observed crossing is an integrity diagnosis (C8.2).
- **Local map.** J_a(u) = L_a(u)·S′_a·C with S′_a = diag(1, 1, s_{o(a)}) and C = D·Qᵀ. It is exact for finite non-crossing edits, because the readout is linear in z off the boundary.
- **Derivation D6, global fit (UNVERIFIED; uses P0).**
  - By P0, Σ_{a∈o} G_a = 4·diag(G_r[xx], G_r[yy], G_r[κκ]) and Σ_{a∈o} G_a S′_a = 4·diag(G_r[xx], G_r[yy], s_o·G_r[κκ]).
  - Let K_o = Σ_{a∈o} G_a[κκ]. For fitting orbits o₁ and o₂: **B = [c_x; c_y; λ·c_τ]** with λ = (s₁K₁ + s₂K₂)/(K₁ + K₂), and **B_μ = [c_x; c_y]**.
  - **Folds fitting on CD, BD or BC (CD→AB, BD→AC, BC→AD):**
    - λ = −1, so B is exact for the s = −1 orbits.
    - On the held-out orbit A (s = +1) the predicted κ response has the **wrong sign**. To first order, L_full,A = 4·E_A against L_μ,A = E_A, where E_o is orbit o's held-out κ-part response energy (‖L[:,κ]c_τδ‖², weighted).
    - On the other held-out orbit Y, L_full,Y = 0 and L_μ,Y = E_Y. Fold gain ≈ E_Y − 3E_A, of undetermined sign.
  - **Folds fitting on AB, AC or AD (AB→CD, AC→BD, AD→BC):**
    - λ = (K_A − K_X)/(K_A + K_X) ∈ (−1, 1). Both held-out orbits have s = −1.
    - To first order, L_full/L_μ = (1 + λ)², so the fold gain is positive iff K_A < K_X, which is not derived.
  - The global gain is **reported, with no expectation of sign**.
- **Derivation D7, class fit (UNVERIFIED).**
  - **In the CD, BD and BC folds,** S′ is constant (−1) over the fitting set, so each class B_{f,g} = diag(1,1,−1)·C exactly **if the class design is resolved at rank 3**. Held-out A prefixes then get the wrong κ sign, as in D6.
  - **In folds containing A,** B_{f,g} = (Σ_r G_{g·r})⁻¹(G_{g·A}S′_A + G_{g·X}S′_X)·C. The within-class G_μκ does not cancel, so the μ rows bend as well. No closed form beyond this is claimed.
  - The class gain is **reported, with no expectation of sign**.
- **Limit exposed (#37 L112, L114, L120).**
  - In the three folds where orbit A is held out, the sign of A's code appears in no fitting prefix. No global or flip-class map can then predict it.
  - "**Per-orbit maps** cannot simply be applied to a wholly unseen orbit without an additional transport rule" [L112]. "**Sign alignment** requires a specified transformation. The world's flip action does not establish a corresponding action on GRU hidden coordinates" [L114].
  - SYS-LIM's sign is flip-invariant, so no flip-based alignment recovers it. Four class maps "address a specific, prospectively declared form of variation" [L120 paraphrase: "They address a specific, prospectively declared form of variation."], and SYS-LIM is outside that form.
  - **Reading.** A class-conditioned negative or mixed result on a network could come from an orbit-indexed code of this kind. That is one more reason for E37-4's negative wording (C10.1).
- **Under B-repaired: TO BE FIXED BEFORE FREEZE.**
  - s_o depends on |μ_x| through a step, while the B-repaired κ row b_g + μ_y·e₁ + μ_x·e₂ is affine in μ within each class, with e shared across classes. Whether, and how far, the shared basis absorbs s_o is not derived.
  - If B-repaired is chosen, SYS-LIM is fitted and reported under it, descriptively only, and the expectation is stated in the frozen file or explicitly marked "none".

## 5. Units, edits, masks, weights, groups and tolerances''')

# ---------- tighten PC bound ----------
rep("""    - Result. At the largest declared ε_syn = 0.25, |Δμ_x| ≤ 0.1325 < 0.2501 and |Δμ_y| ≤ 0.1826 < 0.4276. So no crossing is possible at any declared size.""",
"""    - Result. At the largest declared ε_syn = 0.25, |Δμ_x| ≤ 0.1325 < 0.2501 and |Δμ_y| ≤ 0.1826 < 0.4276. So no crossing is possible at any declared size.
    - Tighter bound (v1.1). With the stored SDs (sd_x = 0.36806, sd_y = 0.61364, read as B·Q from `fit_freeze_O6.json`), the bounds at 0.25 are 0.0920 and 0.1534 against the same margins.""")

# ---------- mask ----------
rep("  - for S2, the edit is non-crossing (C4.2(f)).","  - for S2, the edit is non-crossing (C4.2(f)); for SYS-LIM, the edit is non-crossing at t (C4.5).")
rep("    - The tolerance for the C3.6(e) normal-equation identity checks.","    - The tolerance for the C3.6(e) normal-equation identity checks.\n    - tol_P0 for the step-0 P0 fixture (C4.0).")

# ---------- Option C falsify ----------
rep("- Whether that leak transfers to a trained GRU's μ-only nonlinearity is still unknown. Two laws do not establish transfer.",
"- Whether that leak transfers to a trained GRU's μ-only nonlinearity is still unknown. Two laws do not establish transfer.\n- **Falsify-only (v1.1).** A law outside the basis can only *falsify* floor transfer, never *establish* it. If SYS-NC2's or SYS-NC3's leak exceeds the floor, the floor does not transfer to that law. If it does not, that shows nothing about transfer to any other law, including a trained GRU's.")

# ---------- §7 rewrite ----------
between("## 7. Outcome labels and order","## 8. Resources, integrity stops and timing",
r'''## 7. Outcome labels and order (N1 extended consistently; v1.1 split)

**7.1 Per-statistic labels.** Labels are evaluated per system, per fit type and per group (ALL, MARG) at ε_syn = 0.1. Other sizes are reported and never replace the reference (v1.3 §2 last row). **First match wins:**
1. **PIPELINE INVALID.** Any of the following stops the package, with no rerun under this record:
   - **(DERIVATION PREMISE)**: a P0 fixture failure (C4.0);
   - **(IMPLEMENTATION)**: an O1 or O2 fixture failure; a SYS-O6 identity failure; after P0 has passed, a SYS-PC D1/D2 or SYS-FK D4 identity failure on a resolved design; a failed scoreable edit;
   - **(INTEGRITY)**: an extended-B3 resolved third direction (C8.2).
2. **REFERENCE COVERAGE NOT MET.** In some fold (and, for class statistics, some fold×class), count coverage < 75% (the integer test 4·n_s < 3·n_t) or law-mass coverage < 0.75·(1 − 10⁻⁶) (v1_4_N L13).
3. **REFERENCE RANK UNRESOLVED.** Any required design for that statistic is rank-UNRESOLVED (closure note B1 L15, extended per C3.9). No pooled statistic is formed.
4. **RESTRICTED COMPARATOR NOT ADMISSIBLE.** SYS-NC1, SYS-NC2 and SYS-NC3 only: 5 or more of 16 prefixes voided (v1_4_N L41), or a matched c₂ or c₃ baseline invalid (C4.4.R).
5. **ZERO RESPONSE.** Pooled S = 0 exactly (v1.3 §3 L109).
6. **Identity statistics (SYS-O6; SYS-PC global and class Pred_full; SYS-FK):** IDENTITY AS DERIVED, or EXPECTATION NOT APPLICABLE (RANK) where B2 resolved lower rank voids a derivation premise (for example D2 without rank 3).
7. **Reported statistics (SYS-NC1, SYS-NC2, SYS-NC3, SYS-LIM, and every global-comparator gain other than the SYS-PC and SYS-FK identities):** REPORTED. Gain, losses, matrices and κ-row norms are descriptive. There is no pass or fail (E37-7; SYS-LIM by declaration).

**7.2 VALIDATION label (identities only).**
- **CLASS-FIT VALIDATION MET** iff all of the following hold:
  - P0 passed;
  - SYS-O6 is IDENTITY AS DERIVED, for global and class fits;
  - SYS-PC global is IDENTITY AS DERIVED (the cancellation is demonstrated);
  - SYS-PC class is IDENTITY AS DERIVED (recovery on every resolved-rank-3 class cell);
  - SYS-FK is IDENTITY AS DERIVED, for both fit types.
- Otherwise it reads **CLASS-FIT VALIDATION NOT MET (<first failing reason>)**.
- **Proposed rule (Q15).** EXPECTATION NOT APPLICABLE (RANK) on any SYS-PC class cell gives **NOT MET (RANK)**, because recovery is then not demonstrated.
- VALIDATION does not depend on any gain magnitude.

**7.3 SYS-PC HEADROOM label (separate).**
- **Statistic.** The class-conditioned SYS-PC √H and R = L_μ,class/S, for ALL and MARG at ε_syn = 0.1. The wording follows E37-3: comparator squared prediction error divided by actual response energy.
- **Thresholds.** TO BE FIXED BEFORE FREEZE. The proposal is to reuse the v1.1 §5 declared conventions: ALL √H ≥ 10⁻³ and R ≥ 0.05; MARG √H ≥ 10⁻⁴ and R ≥ 0.02 (v1.1 L115–121; `pinned.py:24–27`). See Q4.
- **Order.** Labels 2–5 of 7.1 first, then HEADROOM NOT MET / BOUNDARY / MET under the band rule of v1_4_N L15–16.
- **Formation.** The label is formed only if VALIDATION is MET. Otherwise it reads **NOT FORMED (VALIDATION NOT MET)**.
- **Meaning.** HEADROOM states only that the class-conditioned comparator leaves enough synthetic κ response on this one declared code. It is not a neural floor (#37 L164: "The later neural absolute-response floor remains unresolved; O6 does not supply it").

**7.4 What the two labels license.** VALIDATION MET with SYS-PC HEADROOM MET licenses only a *decision* on whether a neural specification is warranted (#37 L164). It is not a neural spec, a neural floor or a neural result. The SYS-LIM and NC results go with any such decision as stated limits.

''')

# ---------- C8 ----------
rep("  - Any S2 sign crossing, since C4.2(f) derives that none is possible.",
"  - Any S2 sign crossing, since C4.2(f) derives that none is possible. Likewise any SYS-LIM threshold crossing (C4.5).\n  - A mismatch between SYS-NC1's in-package g refit and the committed `g_coefficients` (C4.4.R).")
rep("  - Totals: 6 systems (S1–S6) ≈ 2.95×10⁶. Under B-repaired or C, add 2 augmented predictions per edit: 7 per edit, ≈ 4.13×10⁶.",
"  - Totals: 7 systems (SYS-O6, SYS-PC, SYS-FK, SYS-NC1–3, SYS-LIM): 7 × 491,776 ≈ 3.44×10⁶. Under B-repaired or C, add 2 augmented predictions per edit (7 per edit): 7 × (98,304 × 7 + 256) ≈ 4.82×10⁶.\n  - Step-0 additions: the P0 fixture (16 × 3 × 16 L evaluations per checked chart) and the c₂/c₃ computation. Both are negligible on paper.")
rep("Linear scaling suggests roughly 80–115 s plus fits.","Linear scaling suggests roughly 95–135 s plus fits.")

# ---------- §11 rewrite ----------
between("## 11. Open questions for Astra","## 12. Verification notes",
r'''## 11. Open questions for Astra (v1.1)

**Resolved as CNA proposed, pending Astra:**
- **Q3 (unresolved class cells).** Use the B1 extension (C3.9): one rank-UNRESOLVED (fold, class) design suppresses that system's pooled class statistic. CNA withdrew void-and-pool.
- **Q5 (control-expectation failure).** Every case stops the package, with diagnoses separated (C4.0, §7.1):
  - a P0 failure is PIPELINE INVALID (DERIVATION PREMISE), before any fit;
  - after P0 has passed, a D1, D2 or D4 failure on a resolved design is PIPELINE INVALID (IMPLEMENTATION).
- **Q7 (NC laws and coefficients).** g₂ = c₂μ_x, g₃ = c₃μ_x³, with c₂ and c₃ set by the RMS-matching rule C4.4.R and NOT ADMISSIBLE if a baseline is invalid (no rescaling). **Remaining point:** CNA confirmed the rule for the quadratic μ_x², which v1.1 replaced with the cubic. Its confirmation for the cubic is still needed.

**Open:**
1. **Q1 (Option).** A, B-repaired, C (restated, falsify-only), or descriptive-only (§6)?
2. **Q2 (Option B).**
   - **Q2a.** Withdraw v1 Option B as NOT INFORMATIVE?
   - **Q2b.** Accept B-repaired, with e shared across classes within a fold? That departs from E37-5's "separately fitted within each class". Accept D2′, including its condition (dx ≠ 0, dy ≠ 0, joint design resolved at full column rank) and the small-dx folds (BC dx = −0.0036)?
   - **Q2c.** Or the tied bilinear form, which needs a new solver?
   - **Q2d.** Must the effective basis be declared?
3. **Q4 (SYS-PC HEADROOM thresholds).** Reuse the v1.1 §5 conventions? CNA's "R near the O6 value" is not derivable (C4.2 D3).
4. **Q6 (SYS-FK scope).** Is κ ≡ 0 on the product-chart designs sufficient, with SYS-O6's class-B identity covering the true-chart designs? Any further fixed-κ control must be autonomous (E37-6).
5. **Q8 (SYS-PC adequacy).** Does τ = sign(μ_xμ_y)·κ, with the sign taken from the state's μ, satisfy E37-6's "explicitly encodes the sign/class information"?
6. **Q9 (tolerances).** tol_gain, tol_P0 and the C3.6(e) identity tolerance, each in absolute and relative form.
7. **Q10 (draw reuse).** May Q (35006), Q₂ (35007) and the O6 directions (35016) be reused, or are fresh declared seeds required?
8. **Q11 (P0 sufficiency).** Is the C4.0 fixture, checking L, w and G, sufficient support for D1 and D6?
9. **Q12 (sizes).** Keep all four ε_syn with 0.1 as reference?
10. **Q13 (SYS-O6 inclusion).** Confirm that recomputing the O6 system here is not a "rerun of the completed package" (#37 L29).
11. **Q14 (SYS-LIM threshold rule).** Is the midpoint rule acceptable as declared: t ≈ 0.403485, midway between orbit D (0.276837) and orbit A (0.530132), with s_A = +1 and s_B = s_C = s_D = −1? Should another orbit split also be declared, for example one isolating B, whose margin to C is only ≈ 0.0018?
12. **Q15 (SYS-LIM role, and rank in VALIDATION).**
    - Is REPORTED ONLY right, or should D7's exact class recovery in the CD, BD and BC folds be a further identity?
    - Should EXPECTATION NOT APPLICABLE (RANK) on a SYS-PC class cell make VALIDATION NOT MET (proposal, §7.2)?
13. **Q16 (SYS-LIM under B-repaired).** Derive an expectation before freeze, or declare "none, descriptive only"?
14. **Q17 (SYS-LIM autonomy).** Does a threshold readout on the state's own |ψ₁| meet E37-6?

''')

# ---------- §12 ----------
rep("  - v1.1: CNA's two Option B claims, checked by my own derivation (§6), and the dx/dy values from `stage_O1.json`.",
"""  - CNA's two Option B claims, checked by my own derivation (§6), and the dx/dy values from `stage_O1.json`.
  - SYS-LIM numbers (|μ_x| per orbit, ordering, t, s_o, margins, ε·sd_x) from `stage_O1.json` exact rationals and `fit_freeze_O6.json` B with `drawn_arrays.npz` Q (B·Q = diag(sd), off-diagonal ≤ 6×10⁻¹⁷, folds equal to ≤ 7×10⁻¹⁶).
  - The c₂/c₃ well-definedness, plus expected values from an inferred P_a (a 4×4 solve; P_a is not stored in committed outputs).
  - E37 substring check re-run on this file.""")
rep("- **UNVERIFIED:** derivations D1–D5, D2′, the B-i and B-ii arguments, P0,",
"- **UNVERIFIED:** derivations D1–D7, D2′, the B-i and B-ii arguments, P0, the inferred P_a and the c₂/c₃ values derived from it,")

# ---------- rename ----------
lines=s.split('\n')
out=[]
for ln in lines:
    if ln.startswith('> ') or ln.startswith('| S') and 'SYS-' in ln:
        out.append(ln); continue
    if 'The bare token "S6" appears' in ln:
        out.append(ln); continue
    if ln.startswith('| S1 |') or ln.startswith('| S2 |') or ln.startswith('| S3 |') or ln.startswith('| S4 |') or ln.startswith('| S5 |') or ln.startswith('| S6 |'):
        out.append(ln); continue
    if "v1's g₃ = c₃μ_x² lay inside" in ln:
        out.append(ln); continue
    r=ln
    r=r.replace('S1/S2','SYS-O6/SYS-PC').replace('S1–S3','SYS-O6, SYS-PC and SYS-FK').replace('S1–S6','all systems')
    r=r.replace('S4–S6','SYS-NC1–NC3').replace('S3–S6','SYS-FK and SYS-NC1–NC3').replace('S5 and S6','SYS-NC2 and SYS-NC3')
    r=r.replace('S2-global','SYS-PC-global').replace('S2-class','SYS-PC-class').replace('S4-global','SYS-NC1-global')
    r=r.replace('S4 (O7)','SYS-NC1 (O7)').replace('S4 = O7 (NC-1, symmetric)','SYS-NC1 = O7 (symmetric)')
    r=r.replace('S5 = NC-2,','SYS-NC2,').replace('S6 = NC-3,','SYS-NC3,')
    for a,b in [('S1','SYS-O6'),('S2','SYS-PC'),('S3','SYS-FK'),('S4','SYS-NC1'),('S5','SYS-NC2'),('S6','SYS-NC3')]:
        r=re.sub(r'(?<![\w-])'+a+r'(?![\w])',b,r)
    out.append(r)
s='\n'.join(out)
open('final.md','w').write(s)
