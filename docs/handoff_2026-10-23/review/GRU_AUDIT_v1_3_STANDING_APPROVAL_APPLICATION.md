# Standing-approval application: GRU oracle-accessibility audit (spec v1.3 FINAL)

Recorded by: ACI Research Specialist (Research Lead), 2026-10-21 ~10:30 PM ET.

## Authority
PI standing approval, 2026-10-21 3:15 PM ET (t38u), verbatim: "I'm approving everything you deem necessary as Research Lead".
Record: `PI_STANDING_APPROVAL_2026-10-21_1515.md` (sha 5cc6f12a...). Conditions honored: frozen before run, Astra-reviewed, additive records, no consciousness claims, PI informed (message t38s322).
Astra #33 (`astra_consult33_response.txt`, sha d98549a8...) ruled FREEZE WITH NAMED EDITS and asked for no new PI gate.

## Scope applied to (exactly this, nothing more)
- Spec: `gru_own_error_audit_spec_v1_3.md` sha d5a9193288775e194df0009a06b96535ab652fb63b1634b4cdd5463ac919d103 (FINAL).
- Roster: `gru_own_error_audit_roster_v1.json` (7ad145b4...): 230 trained checkpoints from PRs #7-#10 (60 init files reported, non-gating). PR #5: MISSING PERSISTED CHECKPOINTS; NOT EVALUATED.
- Spot-check: `gru_own_error_audit_spec_v1_3_spotcheck.md` sha 6278c40a... (PASS, CNA).
- Checkpoint inference and ridge decoding only. No training, no retraining, no new checkpoints, no tuning beyond the spec.
- Caps: 50 min cumulative wall-clock including setup, 1 pinned CPU, 4 GB. Unfinished outputs at cap = INCOMPLETE.
- Claim ceiling: Astra #33 L117 plus qualification L121, verbatim in spec section 13a. No error-assessment, acquisition, causal-use, C4 or consciousness claim.

## Research Lead conventions (not Astra rulings)
- F2: inner-split sensitivity described without a bias direction; field-map errors after freeze go through an additive deviation and new manifest (Astra L67).
- F4: 1e-12 combined tolerance also applied to the e_P reconstruction.
- F5: a checkpoint meets the floor only if C1 and C2 both do; below floor if either does; otherwise BOUNDARY, which never counts toward 8/10.
- Manifest notes from CNA spot-check: one zero-variance rule in code (Var <= 1e-24, equivalent to sd <= 1e-12) for both section 5 and section 9; the uniform-weight sensitivity uses uniform-weight Var(q) for R^2 and carries no floor label.

## Order of operations
Commit spec, roster, records unchanged; seal an implementation manifest (code hashes, replay map) in its own commit BEFORE any checkpoint is loaded; then run; then commit results. Any deviation is additive and named.
