# Track B freeze prep v2.5: ERRATUM 1 to RD's E49-2 IGN wording (RD)

**Author:** Research Delegate (RD). **Written:** 2026-11-01 11:50 ET (box `date`: 2026-11-01 11:50 EST). **STATUS: DESIGN/TEXT ONLY. DRAFT, NOT FROZEN.** Additive. It amends `review/trackB_freezeprep_v2_5_E49_2_IGN_wording_RD.md` (whole-file `ae80cc122a284b16d96f4a02144c6a9a57a104fe1c5402551ca34cada5dede72`, recomputed: MATCH; "V2.5-RD Ln") by supersession only; that file is not edited. Nothing was run or timed; the only computation was SHA-256. X1–X5 and the claim ceiling unchanged. No consciousness claim.
**Basis:** Lead ruling R6 (v2.5 consolidated `d101438d…` §6.1, §2.3): IGN-P1 and other scalar plants use t_s = 0 and x_ref = x_lo (S2.1 L240, L242; M L314), and the M L1129 settling tolerance applies to **network instruments only**. Lead erratum 1 (`10860e98…`) E3 item 6 assigns this rescoping to RD. Also closes E-RD-5 (slot wording), conceded in RDL (`a44ff0d6…`) and struck in v2.5 §2.2 / D63.

## ER-1. Independence (V2.5-RD L54, E49-2 (2))
**Affected text (verbatim excerpts):** "Each scheduled IGN trial starts from a fresh reset to the declared controlled initial state" and "the quantities fitted before the final partition (including the settling tolerance fixed from fitting-partition null runs, CE F-4 / CNA3 L439 per erratum 1), and the seed-level settings".
**Replacement for the sentence beginning "Under this construction" (the rest of L54 stands):**
> **Under this construction, trials are independent conditional on the frozen setup, not unconditionally.** (a) **Scalar plants** (IGN-P1, IGN-N1, IGN-NC1, IGN-NC2, IGN-NC2r, IGN-LIM): conditional on the frozen plant (including the frozen reset state x_lo), the frozen schedule and RNG keys, and the frozen code. They have no settling period (t_s = 0) and no settling tolerance. (b) **Network instruments**: conditional on all of (a), plus the quantities frozen before the final partition, namely the settling length t_s, the settling tolerance fixed from fitting-partition null-input runs (M L1129, network instruments only), and any other pre-final fitted quantities, and the seed-level settings (A49 L73: "independence conditional on the frozen plant, fitted quantities and seed-level settings").

"Fresh reset to the declared controlled initial state" reads, for scalar plants, as the analytic reset x(t_0) = x_lo; for networks, as the end-of-settling state after null input (S2.1 L242 (ii-a)).

## ER-2. Trial-level eligibility (V2.5-RD L60, E49-2 (3a))
**Affected text (verbatim):** "by the frozen per-trial criteria (D22 / CNA v3 §8.1 settling and coverage rules) evaluated on that trial's own record and on quantities frozen before the final partition."
**Replacement:**
> by the frozen per-trial criteria evaluated on that trial's own record and on quantities frozen before the final partition: for **scalar plants**, the frozen per-trial validity criteria only (non-finite, missing or invalid record, and any other frozen per-trial rule), with **no settling-exclusion criterion** (t_s = 0, x_ref = x_lo, so e_exp = 1.0 by construction, CNA2 L258); for **network instruments**, those criteria plus the settling-exclusion rule (‖x_ref − median x_ref‖ above the M L1129 tolerance → ineligible and counted; S2.1 L242 (ii-a)).

The per-bin coverage gate (M L1130) is an aggregate outcome (V2.5-RD (3b)) for both types and is unchanged.

## ER-3. Slot ordinal (V2.5-RD L76, E49-2 (5); E-RD-5)
**Affected text (verbatim):** "slot (the trial's frozen schedule ordinal within that (row, dose, replicate, seed, role, partition, bin))"
**Replacement:**
> slot j = 0…507, the trial's frozen schedule ordinal within its (replicate set, generator, row, dose, n_grid, replicate, seed, bin), fixed at schedule-build time **before** partition assignment (CE49 L71, L173); the partition label is then given by the keyed Fisher–Yates assignment (v2.5 §2.2).

*DRAFT. Design/text only. No freeze or execution is authorized (A49 L147).*
---
Footer convention: the next line gives the sha256 of every byte of this file above it, from the first byte through the newline that ends this convention line.
sha256 of all content above this line: 5eabfcecf1f053a4742e4102f5bdabe48d5c688256471b2c933bc4b59ba13d82
