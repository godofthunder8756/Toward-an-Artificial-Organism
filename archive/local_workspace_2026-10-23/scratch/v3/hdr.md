# Track B instrument-validation scope v3 — RD half (built on merged v2.1 `8ea6abc5…`)

**STATUS: DRAFT, NOT FROZEN, DESIGN ONLY.** Nothing runs. Astra #42, verbatim: "No Stage-0 execution, training, simulation or checkpoint inspection is authorized by this review." (#42 L249) **P3: CLOSED by Astra #42** ("P3: CLOSED for the declared bounded scholarly-index search" (#42 L251)).

- **What this file is.** The RD half of scope v3. It is a new, additive file and edits nothing. v2.1 (`8ea6abc5…`) and every other input stay on disk unchanged. RD holds the merge; CNA's v3 half (`5dec96f5…`) is filed and enters at the merge (§PC1–§PC4).
- **Authority.** Astra #42 raw text first; Astra #41 raw text where #42 is silent; then the Lead's room rulings (2026-10-23, about 2:30 PM and 2:39 PM ET). Astra is quoted verbatim, cited "#42 Lnn" / "#41 Lnn". E42-1..9 are numbered exactly as #42 L231–247.
- **Split (Lead).** CNA drafts the mixed-code plant, the dissociation contrast, observer pathway matching and its budgets, and the donor laws. RD takes every other E42 item and every ruling. Items the raw reply assigns ambiguously are in this half, marked **CNA-overlap, light-pass**.
- **How it is built.** RD-owned sections of v2.1 (§2, §3, §4, §5, §5b, §5c, §6, §7) are carried in full with edits tagged **[v3 Cn]** (listed in §9); struck text is kept visible as ~~strikethrough~~. New sections: §2.6–§2.7, §5.9, §5d–§5f, §14 (pending-choice specification), §15 (CNA dependency settlement), §PC1–§PC4 (CNA placeholders), §8 (response table), §9–§11. v2.1's CNA-owned sections (§P1, §P3, §PA, §PS) are carried **by reference** (§16).
- **Written:** 2026-10-23, about 2:35–2:50 PM ET, by RD. Read-only on the repo and GitHub.
- **Correction for the record [v3 C2] (Lead ruling, 2:39 PM ET; CNA v3 D9).** v2.1's header (v2.1 L3) said "P3 stays OPEN and freeze-blocking pending Astra #42". #42 L251 closed it; this header records P3 CLOSED. v2.1 is not edited.

**Number provenance.** Every number here is (a) an Astra candidate, cited by line; (b) a v1 value carried; (c) a **PROPOSED DEFAULT** with a one-line rationale (§14; CNA v3 for CNA rows); or (d) marked **OPEN FOR #43** where no defensible default exists. None is measured. **Every default is chosen without reference to any instrument outcome** (#41 L186, verbatim: "Do not tune doses on final instrument outcomes."), and **calibration and sample-size choices are fixed in a separate calibration stage before confirmation** (§5.9). Arithmetic in §14 was computed on the box (scipy 1.x in a scratch venv) on proposed values, not data.

**Labels.** Confound rows: PASS / FAIL / CONFOUND NOT REALIZED only; CONFOUND NOT REALIZED → UNRESOLVED, which blocks Stage 0. AVAILABLE and UNAVAILABLE are never confound-row labels; UNAVAILABLE is only an instrument-on-system label for eligibility gates and limitation tests designated before results (#42 L216).

## 1. Inputs (all hashed on the box, 2026-10-23 about 2:45 PM ET; none edited)

| Role | Path | sha256 | Footer check |
|---|---|---|---|
| Astra #42 raw reply (GOVERNING) | `/workspace/astra_consult42_response.txt` | `e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847` | — |
| Consult summary incl. #42 entry L157–164 (non-governing; appended over time; hash as read) | `/workspace/astra_consult_1.md` | `6ad5afa02a487fa4beb26b09df74a1a2b8ac7121a292de082828d515912ace25` | — |
| #42 packet body as sent | `/workspace/astra_serve42/c42_body.md` | `7968c1913402551c1e6ee5e697ca67897fa7c172a3d3ad1a3713104f5502ccc0` | — |
| #42 cover note v1 | `/workspace/review/trackB_astra42_cover_note_v1_RD.md` | `16581a04a0cc98f208bdfd20dda45f5f446d915e98ad429b8cdb0928f29c3c43` | — |
| Merged scope v2.1 (base; frozen, not edited) | `/workspace/review/trackB_instrument_validation_scope_v2_1_merged_RD.md` | `8ea6abc50b3929a39688aa54b1a1d66fe34c8ef17b3c5dfae98cc8efa79862de` | `15a0b715ed7567084488e99045c141692513dd7ca89885e83a4ce769304f3e1f` reproduced |
| CNA v3 half (plants, confounds, observer) | `/workspace/review/trackB_scope_v3_CNA_plants_confounds_observer_v1.md` | `5dec96f59255cb2e9da29447cd102637c91a1736899f28653a606e2de8193321` | `7d93990c5bca535a1988aef3977bd23e5725827ba9c129ad446c9c6f5412fa83` reproduced |
| Astra #41 raw reply (governs where #42 is silent) | `/workspace/astra_consult41_response.txt` | `3f3b1b87faf39ac213eca6c239279a24edde0383ca789c5f2a3fce4391074f43` | — |
| Merged scope v2 (superseded by v2.1) | `/workspace/review/trackB_instrument_validation_scope_v2_merged_RD.md` | `5824d5e5651aa5ba08bf91e1a2df614be8a85122c49de2fbeafcf070fea0dcf3` | `bb06b43e23e72231cfc4d02998394421b0d7cb551e93f06c182e6eddbedab7ae` reproduced |
| CNA v2 half | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1.md` | `17832b01de2b8a029630b461111f71bafcf8b2261a4f1821a4817e9ed4399e0e` | `b666b1d76abe8e526cdc20a404c7cf047ac46823e121a2104636c9d165c68dd1` reproduced |
| CNA erratum 1 to v2 half | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum1.md` | `c2cd0732c4bd319497306b1dc47d440b50011843a9078ad5a59f46c720003543` | `9b3417d21ded80189125b2227dbe8817b02f4016074e717bd1c7fe047b2d5cd9` reproduced |
| CNA erratum 2 to v2 half | `/workspace/review/trackB_scope_v2_CNA_items1_3_A1A4_SELF1_v1_erratum2.md` | `5ddde854099020adf113d9c1fd81a1f511d272e5d294abcd3493a1283a1878bc` | `725411374e8fc7355a4f4dc897b4be4e5ed0ca508c6a4202f184dd8a697bf866` reproduced |
| CNA light pass on merged v2 | `/workspace/review/trackB_scope_v2_merged_lightpass_CNA_v1.md` | `2d52f7d372f02896e895f8350ed5b66867cb925fe4c572ae338998593424f868` | `34331e6940736e24858be38406fe0180eaaf8216f085a97c65b50af3f8a167d7` reproduced |
| CNA prior art v1.3 (full reads; Asan) | `/workspace/review/trackB_prior_art_verification_v1_3_fullreads_CNA.md` | `badf7258278fcecc11bea190f5397724ca0fdaf21348f915b1e2c34afe4cec8a` | — |
| CNA prior art v1.4 (P3) | `/workspace/review/trackB_prior_art_verification_v1_4_P3_scholarly_CNA.md` | `d7f1a43b5c83b2310bac970526f625188ac18cca31f5a59cef6423cbd4c8128d` | — |
| CNA prior art v1.5 (P3 alt routes) | `/workspace/review/trackB_prior_art_verification_v1_5_P3_altroutes_CNA.md` | `3fde80d859a640d9f55c21edc05439743ae5fb49714fb89e5e5d16d338eced75` | — |
| CNA prior art v1.6 (Palika route) | `/workspace/review/trackB_prior_art_verification_v1_6_palika_route_CNA.md` | `9704f21d2988026ce5644ec28a18b3f55620ac10edd094be7b086df9e729b851` | — |
| FoodRL commit list as fetched by CNA (v1.6 raw) | `/workspace/tmp_p6/raw/foodrl_commits.json` | `b02b91b0064081ef03d50669cf6b1bec03d2e98bc60130ba7382b9f14a06b0d3` | — |
| Merged scope v1 | `/workspace/review/trackB_instrument_validation_scope_v1_RD.md` | `7b9bf34d7b4c10c8c2a7063aa6177d94e888fbbe76f78d0cd33afbe0c905c56a` | — |
| Measurement plan v1 | `/workspace/review/trackB_measurement_plan_v1_RD.md` | `1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef` | — |
| CNA planning note v1 | `/workspace/review/trackB_workspace_allostasis_scope_note_v1.md` | `87a31cc88dc2fd0252d4cf932fabbfd8a1ce65bd3f77dce9eda5c6cfdafe2800` | — |

Full hash of the governing raw #42: `e438e329cff272bfd174a88dd917da6d7eb5560436fee06c39d0d46fd719c847` (starts `e438e329`, as briefed). All other v2.1 inputs (A1–A7, addendum, earlier CNA files) are listed with full hashes in v2.1 §1 / M1 and are unchanged.

---

## 0. Governing text: Astra #42

- **Verdict, verbatim:** "VERDICT: REVISE." (#42 L227) "SP1 addresses all five objections, and SP3 closes the original all-UNAVAILABLE loophole, but several remaining choices determine what a successful result would mean." (#42 L1)
- **Scientific choices, verbatim:** "Some PENDING items are scientific decisions, not implementation details: observer resources, the A-EXT interface, conditional donor construction, prediction horizons, baseline information sets, corruption processes, and the calibration/confirmation split. They must be specified in the revised design. Hashes, paths and counts derived from a complete design can be finalized during implementation and checked before sealing." (#42 L13)
- **Scope, verbatim:** "This review concerns the supplied condensed record. It does not independently certify the full file, hashes or implementation." (#42 L15)
- **Required revision items, verbatim (#42 L231–247):**
  - "E42-1. Freeze a claim-to-decision table separating decoding advantage, generic intervention dependence, variable-attributed use, observer-relative prediction advantage and named-signal attribution. Require a labelled dissociation criterion for variable-attributed causal wording." (#42 L231)
  - "E42-2. Add the joint history-plus-proxy comparator and specify the representational capacity needed for relay and memory ground-truth claims. Include the mixed-code, reward-used/E-decodable challenge." (#42 L233)
  - "E42-3. Replace the SELF plateau exemption with a fixed required observer comparison. Account for the representation-producing pathway and training expenditure; keep smaller observers and plateau analyses diagnostic." (#42 L235)
  - "E42-4. Specify the SELF conjunction and multiplicity rules, and correct the Ashuach description. Freeze disagreement selection using out-of-sample selection predictions, with subset eligibility and a clearly defined descriptive or inferential status." (#42 L237)
  - "E42-5. Prohibit outcome-dependent conversion of failed positives into limitation tests and outcome-dependent removal of required comparators. Define CONTENT matching against the actual degradation mediator and require conditional support." (#42 L239)
  - "E42-6. Define the S-INT decoding label, prediction origin and at-risk sampling scheme. Retain learner-only bootstrap bookkeeping and separate operational interruptibility from training-schedule equivalence." (#42 L241)
  - "E42-7. Retain uninterrupted scheduled viability evaluation and adopt a conservative confirmatory rule for incomplete paired episodes." (#42 L243)
  - "E42-8. Separate calibration, design selection and confirmation. Freeze the relevant grids, sample-size selection rule, independent confirmation allocation, error-budget interpretation and bounded meaning of each operating-characteristic claim." (#42 L245)
  - "E42-9. Complete the scientific specifications and resource plan before the next freeze review: interfaces, horizons, donor laws, corruption, noise, floors, observer budgets, comparator family, required counts and stage caps. Administrative hashes and paths may follow during implementation; scientific choices may not be delegated to implementation discretion." (#42 L247)
- "The following are the required revision items. They are not authorization to execute." (#42 L229)

---
