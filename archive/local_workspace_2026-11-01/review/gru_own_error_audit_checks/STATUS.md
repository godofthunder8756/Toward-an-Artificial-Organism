# GRU own-error audit: Part 2 check status (2026-10-21, ~6:55 PM ET)

Spec: `/workspace/review/gru_own_error_audit_spec_v1.md` (sha256 `c0fad75a18b867622b75187a75a023f8c6684a02822ee2771292b268d61452a1`). DRAFT, not frozen, not reviewed.
Approval record: `/workspace/review/PI_STANDING_APPROVAL_2026-10-21_1515.md`. The sha256 `5cc6f12a…` was verified. Its only recorded application covers N1/N2 of acquired_self_correctness_spec_v1. It has no application entry for this audit.

**Nothing was run in this directory, so there is no PRE_RUN_FREEZE.txt.**

| check | status | reason |
|---|---|---|
| Roster inventory (read-only git) | DONE | `/workspace/review/gru_own_error_audit_roster_v1.json` (sha `7ad145b4…`). 290 files: 230 TRAINED, 60 INIT. PR #5 has 120 runs with no weights (missing). |
| Support (outcome-blind W2 masses, groups, n_eff) | DONE, as spec arithmetic | `/workspace/scratch/gru_audit/check_gru_audit_spec.py` (sha `d2449113…`), output `check_output.txt` (sha `46547235…`): 0 failures. No checkpoint loaded. |
| S0 replay fidelity (checkpoint inference) | NEEDS-APPROVED-RUN | Needs a reviewed, frozen spec (Astra #31 L210, L247). |
| F0 target variation (checkpoint inference) | NEEDS-APPROVED-RUN | F0 is the audit's primary falsifier. Computing it before review would make its threshold post-observation (E31-9). |
| F1 / T (decoders) | NEEDS-APPROVED-RUN | Outside the Part 2 limits in any case. |

Support values. They are exact W2 masses, P(h)-weighted. They are not outcomes.
- Group masses A–D: 0.3188 / 0.2397 / 0.2409 / 0.2006.
- Group n_eff: 57.3 / 60.2 / 61.1 / 60.7.
- Fold fit-set n_eff: 110.7–121.2, against the declared minimum of > 10.
- Total n_eff: 230.3 of 256.
