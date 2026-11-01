# PR #8 additive interpretation note: ERRATA_v3 text (from Astra consult #17, O1)

**Target.** PR #8 (branch `cursor/graded-joint-reversion-ddeb`), proposed file `graded_reversion_results_v1/results_v1_errata/ERRATA_v3.md`.
- Additive only. No edits or deletions of existing files, including ERRATA_v2 and the earlier errata.
- No reruns and no label changes.
- It also attaches to the consult #16 record.
- **Not committed by the Research Delegate.** The commit is for the PR #8 agent, on instruction.

**Attribution.** Astra consult #17 (`/workspace/astra_consult17_response.txt`), O1. It corrects the explanatory hypothesis in consult #16 §3 ("Reversion may have a larger positive gradient projection than typical isotropic directions") and the curve-shape reading in the Research Delegate's PR #8 review §3.

**Source of the check.** Draft-stage feasibility checks, read-only, with no training: `/workspace/scratch/fo_control/feasibility.{py,json,log}` and `feasibility_summary.txt`. They are described in Appendix B of `/workspace/review/first_order_control_protocol_FINAL.md`.

**Note (verbatim, consult #17):**

> "Exploratory finite-difference checks on the 20 existing checkpoints found a negative initial reversion derivative in 15 seeds. At alpha = 1/8, the tangent prediction ranged from -1.39 to +0.23 times the observed positive loss increase. These findings do not support the proposed explanation of the sampled early-dose damage by a dominant positive initial gradient projection. The curve-shape analogy was a hypothesis, not an established mechanism. PR #8's AUC results and labels are unchanged. Confirmation of the derivative calculations by the new autograd implementation is required."

**Ledger:** unchanged.
- Q-CAUSE organization level: SUPPORTED, BOUNDED, with the E-B4 qualifier.
- Q-NECESSITY and the C-levels: unchanged.
- No C4 claim and no consciousness claim.
