# Erratum 2 to the CNA scope v2 contribution, and to the CNA light pass on the merged v2

CNA, 2026-10-23, about 1:02–1:06 PM ET. **Additive. Design-only. Nothing runs.** This file is filed per the Lead's ruling on light-pass item m6 and the §1a miscounts. It edits no file. The text marked "new" below replaces the text marked "old" when the files are read or next merged. It authorizes no Stage-0 run, training, simulation or checkpoint inspection (#41 L300).

**Line references used below.**
- **"CNA Lnn"**: a line in `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` (`17832b01…`), as amended by erratum 1 (`c2cd0732…`). Erratum 1 does not touch CNA L265, L287 or L288.
- **"Mg Lnn"**: a line in the merged v2, `/workspace/review/trackB_instrument_validation_scope_v2_merged_RD.md` (`5824d5e5…`).
  - Mg L382 is byte-identical to CNA L287, and Mg L383 to CNA L288 (checked with `cmp`).
  - Mg L360 carries CNA L265.
- **"Lp Lnn"**: a line in `/workspace/review/trackB_scope_v2_merged_lightpass_CNA_v1.md` (`2d52f7d3…`).

All numeric values remain **PROPOSED DEFAULTS**, as in the original. **No label, verdict or prior-art status changes.**

---

## Part A (m6). REW-CORR and PROXY realization criterion: one-sided, consistent with §2.2

**Basis.** CNA §2.2 (CNA L249; Mg L344) defines the tolerance as one-sided: "real_i = 1 if raw_i ≥ threshold_r,d × (1 − tol) … Tolerance is one-sided because a stronger imitation is still a valid challenge." The REW-CORR row's "corr within tol of ρ" was two-sided, which is inconsistent with that definition. RD's Appendix B10 (Mg L974) and CNA light pass m6 both flagged it.

### A1. REW-CORR row: "Realization threshold" cell, CNA L287 = Mg L382

- **Old:** `corr within tol of ρ, **and** raw R²(state → E) ≥ ρ²·(1 − tol)`
- **New:** `corr(E, r̄) ≥ ρ·(1 − tol), **and** raw R²(state → E) ≥ ρ²·(1 − tol) (both one-sided, per §2.2). **Dose-fidelity check (REPORTED only, not a realization criterion):** |corr(E, r̄) − ρ| ≤ tol·ρ, two-sided, reported per replicate and per dose so dose levels stay distinguishable; failing it never changes real_i and never makes a row PASS`

All other cells of the row are unchanged.

### A2. PROXY row: "Realization threshold" cell, CNA L288 = Mg L383

- **Old:** `As REW-CORR`
- **New:** `corr(E, p) ≥ ρ_p·(1 − tol), **and** raw R²(state → E) ≥ ρ_p²·(1 − tol) (both one-sided, per §2.2). **Dose-fidelity check (REPORTED only):** |corr(E, p) − ρ_p| ≤ tol·ρ_p, two-sided, as for REW-CORR`

The "Eligibility gate at risk" cell stays `As REW-CORR`.

**Effect of A1 and A2.**
- A replicate whose correlation overshoots ρ, i.e. a stronger imitation, now counts as realized. This matches §2.2's rationale.
- An overshoot that lands near the next dose level shows up in the reported dose-fidelity check and is never silently re-binned.
- The §2.4 minimum-realized-fraction rule and the §2.5 row labels are unchanged.
- With tol = 0.10 (PROPOSED DEFAULT), the thresholds are:

  | ρ | corr threshold | R² threshold |
  |---|---|---|
  | 0.5 | 0.45 | 0.225 |
  | 0.7 | 0.63 | 0.441 |
  | 0.9 | 0.81 | 0.729 |

  This is arithmetic on the proposed values, not data.

### A3. Clopper–Pearson sidedness tied to §5.4: CNA L265 = Mg L360 (parenthetical only)

- **Old:** `(With R = 200 the bound requires roughly ≥ 189/200 observed. That is arithmetic on the proposed values, not data.)`
- **New:** `(The sidedness and level of this bound, and of the e_min floor in §2.3, follow the α and sidedness frozen under merged §5.4 (cross-reference; RD-owned). As written here, the rule is one-sided 95%: with R = 200, the smallest count meeting it is 188/200, which gives a lower bound of 0.9046 (187/200 gives 0.8986). If §5.4 freezes a two-sided 95% interval instead, the smallest count is 189/200, which gives 0.9037 (188/200 gives 0.8975). These are exact binomial computations on the proposed values, not data.)`

**Effect of A3.**
- No threshold changes. f_min = e_min = 0.90 stays a PROPOSED DEFAULT.
- This is consistent with merged R12 (Mg L823) and RD Appendix B9 (Mg L973), which state the one-sided 188/200 correctly.
- The CNA §2.3 sentence (CNA L256 = Mg L351), "one-sided 95% Clopper–Pearson lower bound", now also reads as subject to the §5.4 cross-reference. Its text is unchanged.

---

## Part B. Miscounts in the CNA light pass on the merged v2, §1a

### B1. Lp L41

- **Old:** `**431 of 476 lines match byte for byte.** The 45 that don't fall into four groups:`
- **New:** `**323 of 368 non-blank lines match byte for byte (45 not exact).** The 45 that don't fall into four groups:`

The count excludes blank lines and bare `---` rules. 368 = 323 + 45.

### B2. Lp L43

- **Old:** `- **Expected, re-levelled headings (29 lines).**`
- **New:** `- **Expected, re-levelled headings (31 lines).**`

The 31 line numbers listed after it are unchanged and correct.

**The 45 lines that are not exact matches, by group:**

| Group | Lines | CNA lines |
|---|---|---|
| Re-levelled headings | 31 | as listed at Lp L43 |
| Erratum-1 replacements | 9 | CNA L63, L125, L129, L153, L170, L174, L292, L294, L328 |
| Footer | 1 | CNA L476 |
| Preamble | 4 | CNA L1, L3, L5, L7 |
| **Total** | **45** | |

**No verdict changes.** The light pass's check 1a stays CONFORMS (with m1). The overall verdict stays CONFORMS WITH MINOR EDITS: 1 ISSUE and 8 MINOR. The error was in the reported counts only, and every line accounted for is unchanged. With this erratum, m6 is filed and m7 is cross-referenced (A3).

---
Footer: input hashes (sha256; re-hashed on the box 2026-10-23, about 1:02 PM ET; none edited)
- `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md`: 17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e
- `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md`: c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543
- `/workspace/review/trackB_instrument_validation_scope_v2_merged_RD.md`: 5824d5e5651aa5ba08bf91e1a2df614be8a85122c49de2fbeafcf070fea0dcf3
- `/workspace/review/trackB_scope_v2_merged_lightpass_CNA_v1.md`: 2d52f7d372f02896e895f8350ed5b66867cb925fe4c572ae338998593424f868
- `/workspace/astra_consult41_response.txt`: 3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43
sha256 of all content above this line: 725411374e8fc7355a4f4dc897b4be4e5ed0ca508c6a4202f184dd8a697bf866
