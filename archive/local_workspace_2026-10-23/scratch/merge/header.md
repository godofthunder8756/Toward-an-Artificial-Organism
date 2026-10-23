# Track B instrument-validation scope v2 — MERGED (RD v2 + CNA items 1, 3, AQ-A1..A4, AQ-SELF1)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. No Stage-0 run, training, simulation, solver or checkpoint inspection is authorized. Astra #41, verbatim: "No Stage-0 run, training, simulation or checkpoint inspection is authorized by this review." **P3 stays OPEN and freeze-blocking pending Astra #42.**

- **What this file is.** A new, additive merge record. It edits no existing file. RD's v2 (`166370c1…`, treated as frozen) and CNA's half (`17832b01…`) both stay on disk unchanged. v1 and A1–A7 stay on disk unchanged.
- **How it is built.**
  - RD's v2 content appears in full below (from its §0 to its §10), with the merge edits listed in §13: (i) the four placeholder sections §P1, §P3, §PA, §PS are replaced by CNA's content, quoted verbatim, with only heading levels changed and "CNA §" prefixed to CNA's own section numbers, and with CNA erratum 1 (E1–E6) applied in place (each erratum insertion is tagged "[erratum 1 En]"); (ii) the inputs table gains rows; (iii) Palika material from CNA v1.6 and the Lead's rulings is added to §2.2; (iv) the §8 response table is replaced by a merged one; (v) the §10 CNA-file bullet is updated; (vi) light-pass items I1, M3, M4, M5, M6, M7, M11, M12 and erratum E3/E4 are applied in RD text, each tagged "[merge Rn]".
  - Inside quoted CNA blocks, "§n" means CNA's own section n (CNA §1 → merged §P1; CNA §2 → §P3; CNA §3 → §PA; CNA §4 → §PS; CNA §0, §0.1, §5, §6 → Appendix A), and "Ln" means line n of the raw #41 file.
  - Conflicts between the halves are in §12 (Merge reconciliations). Order of authority: Astra #41 raw text first, then the Lead's room rulings. Anything not decidable from those is marked **OPEN FOR CNA/LEAD**.
- **Written:** 2026-10-23, about 12:55 PM ET, by RD. Read-only on the repo and GitHub.
- **Lead rulings applied in this merge (room, 2026-10-23 ~12:36–12:43 PM ET):** use the raw L304 ceiling sentence verbatim; orthogonality counts as the **fifth** legitimately-satisfying control (CNA D-g); CNA's §20-1 and §20-2 are cited, not redrafted (they are CNA item 1 and item 3); Palika per §2.2; #42 packet note per §11; CNA's light pass on RD's half is a separate file, not awaited.

## M1. Inputs added for the merge (verified on the box, 2026-10-23 ~12:45–12:50 PM ET)

| Role | Path | sha256 | Footer check |
|---|---|---|---|
| RD scope v2 (frozen as of the Lead's line-276 fix) | `/workspace/review/trackB_instrument_validation_scope_v2_RD.md` | `166370c1435bdab6734aec869c94770fb8a88214066082b3a4e3996dbce13b40` | `111f163b0b1c743574c30ec6193c457fa64cb149aabec46ae659038271c7cf4b` reproduced |
| CNA v2 half (items 1, 3, AQ-A1..A4, AQ-SELF1) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` | `b666b1d76abe8e526cdc20a404c7cf047ac46823e121a2104636c9d165c68dd1` reproduced |
| CNA prior art v1.6 (Palika route check) | `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md` | `9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851` | `be61452b4d0cacd208dfae964e74b02ada69d63d1736f30661ab7f9147a0097b` reproduced (v1.6's last line is the bare hash) |

| CNA light pass on RD v2 | `/workspace/review/trackB_scope_v2_RD_lightpass_CNA_v1.md` | `9f7a6ebcfbdc4618217649bb84a5ab5728dc3389341f88e2c32e6a2c4e7b60c4` | `e7ac3a93a974a473ec0813c2392dfa2eda38a9bd14c4271353e9f82fce5d03a2` reproduced |
| CNA erratum 1 to its v2 half (E1–E6) | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md` | `c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543` | `9b3417d21ded80189125b2227dbe8817b02f4016074e717bd1c7fe047b2d5cd9` reproduced |

All other inputs are in §1 below with full hashes; each was re-verified for this merge and is unchanged.

**Number provenance (merged; corrects RD v2's header claim per light-pass M11).** Every numeric value in this file is one of: (a) quoted from Astra #41 (marked "Astra #41 candidate"); (b) a v1 PROPOSED value carried as PENDING (bootstrap B = 10,000 and the 95% CI level, both from v1, not #41); (c) a CNA **PROPOSED DEFAULT** with its stated rationale (CNA sections, erratum 1); or (d) PENDING. Nothing is from data.

**Labels.** Confound rows: PASS / FAIL / CONFOUND NOT REALIZED only; CONFOUND NOT REALIZED → specificity UNRESOLVED, which blocks Stage 0. AVAILABLE and UNAVAILABLE are never confound-row labels; UNAVAILABLE appears only as an instrument-on-system label (eligibility gates, designated limitation tests; §12 R4).

---

