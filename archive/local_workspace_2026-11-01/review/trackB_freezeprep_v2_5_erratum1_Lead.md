# Track B freeze preparation v2.5: ERRATUM 1 (Lead) — hedging safeguards for row 4b; IGN-N1 x_lo; DOSE0 address; Hoeffding citation; independence scoping

**STATUS: DESIGN ONLY. DRAFT, NOT FROZEN. NOTHING RUNS.** Additive. It amends `review/trackB_freezeprep_v2_5_consolidated_Lead.md` (whole-file sha256 `d101438d75ae60afe31a8ef420c7e4bbec9aea6d72354478943a7e9162a784a5`, footer `36dbcb5f48c7e21ab572af6da5cce63548f54f4b30403955f6d5fb9d8631e0c0`, both recomputed: MATCH; "V25 Ln") by supersession only. V25 is not edited. Sources for E3: CNA room statement 11:47 AM ET (no file), accepted by the Lead. Nothing was run or timed; the only computation was SHA-256.
- **Written:** 2026-11-01, about 11:50–11:58 AM ET, by the Lead's executor. (An 11:50 draft of this erratum, sha256 7cc789a8…, carried only E1–E3; it was replaced before any send and is superseded by this file; copy at scratch/lead_v25/erratum1_draft_7cc789a8_superseded.md.)

## E1. Correction: the two hedging safeguards (supersedes V25 L67–L68 in part, and the "§1.3" pointer at V25 L31)
V25 L67 misidentified "the two hedging safeguards" and V25 L68 said a further guard was only "asked in #50 Q1; **no position is taken** and nothing is added here". **That is superseded.** The Lead **ADOPTED both safeguards provisionally at about 11:39 AM ET** (Lead message to the executor, item 3b, and the room post), and **CNA endorsed exactly these two** (room, 11:39 AM ET):

1. **(i) Worst-case false-licence rate.** A **pre-registered worst-case FL rate** that counts **every row-4b replicate (E-ATTR BOUNDARY or UNRESOLVED, incl. E2-floor UNRESOLVED) as a false licence**: FL_wc = (n_5 + n_4b) / (n_4 + n_4b + n_5), over all 200 prespecified replicates per row and dose. **How it enters the gate (provisional):** it is **reported alongside the primary FL rate** (n_5 / (n_4 + n_5)) in every assessed row and dose. It does **not** at present gate on its own. **Whether FL_wc must also meet the 0.08 one-sided 95% CP upper-bound criterion (M L1965) is asked in #50 Q1(c).**
2. **(ii) Maximum row-4b share.** A **pre-registered maximum share** of row-4b replicates among Q-labelled replicates (rows 4 + 4b + 5). **Value: PENDING** (to be fixed before any calibration output, A49 L47; the basis for setting it is asked in #50 Q1(c)). Exceeding it is a separate aggregate outcome with its own reason code; its consequence is fixed with the value.

**Existing rules, kept as such (not "the two safeguards"):** (a) no replicate earns realization credit as a withhold (rows 1, 3, 4b earn real_i only from the label-independent E5 plant checks, M L1630); (b) row 4b is outside the primary FL denominator, does not count toward the ≥ 36 assessability condition, and is reported by label and dose. RD's observation that hedging at nulls also costs power at positive rows (LP2 AD-1) stands as context.

The rest of V25 L68 stands: CNA's "cannot lower the false-licence rate" is withdrawn; hedging a would-be MET to BOUNDARY can lower the primary FL rate (e.g. 5/100 → 0/95), which is why (i) is reported.

**Consequential updates:** V25 §10 O2 now reads "Row 4b treatment; whether FL_wc must meet the 0.08 CP criterion; the row-4b cap value and basis (#50 Q1)". V25 D61 is unchanged. Status of both safeguards: **PROVISIONAL, pending #50.**

## E2. Confirmation: plant cost fraction
The "2/8 to 5/8" steering relayed to the consolidation was **retracted** (RD withdrew it in LP2 (g), `6c02198c…`). **3/8 to 5/8 of the 8τ basis stands**, as already stated in V25 §6.4 and §12 item 3; at the provisional t_r grid a plant trial is 5/8 (500 steps for g ≤ 2). No number in V25 §8 changes.

## E3. CNA room statement, 2026-11-01 11:47 AM ET (no file), ACCEPTED by the Lead — updates V25 §12 items 1, 2, 6, 7
| V25 §12 item | Ruling | Status |
|---|---|---|
| 7 (IGN-N1 x_lo; also V25 §6.1 PENDING and O6 in part) | For **g < 1** (IGN-N1), x_lo := the **unique stable fixed point x\* = tanh(g·x\* + b) of the noise-free plant**, computed by fixed-point iteration from x = 0 until |Δx| < 1e-12 in float64 under the pinned libm, and **frozen as a constant per dose**. Rows with g ≥ 1 keep the existing lower-branch definition. The reset is analytic and t_s = 0 (as V25 §6.1). | **RESOLVED** (the frozen constants themselves are computed at freeze; the pinned libm stays P6) |
| 2 (dose index vs dose 0; V25 §3.2 rule, O11) | Dose-0 arms use the **reserved dose value 2^64 − 1 = 18446744073709551615 ("DOSE0")** in the u64 dose-index field of the RNG address. Dose index 0 stays the **first required dose**. No KAT is recomputed (no existing vector uses DOSE0). **Four DOSE0 cells:** IGN-NC1, IGN-NC2, BOTTLENECK-ONLY, Architecture-imposed. | **RESOLVED** (supersedes V25 §3.2's "own index in the frozen dose list" wording) |
| 1 (Hoeffding issue number; V25 §2.5, O13 in part) | Citation: **Hoeffding, W. (1956), Ann. Math. Statist. 27(3):713–721, September 1956, DOI 10.1214/aoms/1177728178.** "27(4)" (V2.5-RD L68) is the error. | **RESOLVED** for the citation; **p. 718 regime still UNVERIFIED** (O13 stays open for p. 718) |
| 6 (V2.5-RD (2) settling-tolerance clause applies to all IGN trials) | Rescoping the E49-2 independence text so the fitted settling tolerance is named for **network instruments only** is **assigned to the Delegate**. V25 §2.3's reading governs meanwhile. | **PENDING (RD)** |

V25 §12 items 3, 3a, 3b, 4, 5, 8 and 9 are unchanged.

## E4. #50 packet
The #50 packet is rebuilt with Q1(c) restated as the adopted-provisional safeguards (i) and (ii), the E3 items reflected where they appear (IGN-N1 x_lo, DOSE0 address, Hoeffding citation, independence scoping PENDING), and this erratum cited by hash in the governing list and cover.

*DESIGN ONLY. Draft, not frozen. No freeze or execution is authorized (A49 L147). X1–X5 and the claim ceiling unchanged. No host coupling. No consciousness claim is made or implied.*

---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 4d51b00cdb17a4bc86b2dc0863a8264113c7e38d9cdf1ae706382f8294249511
