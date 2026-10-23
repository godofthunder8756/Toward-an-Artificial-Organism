# PR #5 results erratum A: claim wording (DRAFT v1)

**Status:** DRAFT for the ACI Research Specialist. Not committed, not frozen. This is an **additive, versioned** erratum. It does not edit any frozen artifact.
**Proposed repo path when adopted:** `acquisition_results_v1_errata/ERRATUM_A_CLAIM_WORDING_v1.md`. This is a new file in a new directory; nothing under `acquisition_results_v1/` changes.
**Applies to:** PR #5, head `b25a30ab014355aaec123258031b597c5a78ba55`, results commit `b25a30a`, freeze commit `0b98460`.
**Frozen files referenced (sha256, read-only):**
- `acquisition_results_v1/RESULTS.md`: `7e4a1e1b27f80d44b283df83c92e43fe4c3594dfc0549f9d9da7ff55cf6de56a`
- `TWOSTREAM_ACQUISITION_PROTOCOL_v1.md`: `5fa5a795859d5ea7ee74f90fb043e143b484e32445741e9e4141a27d7dbf5d7c`

**Source of the correction:** Astra consult #11, §1 ("Allowed claim") and §3 ("What E3 actually says").

---

## 1. What this erratum does and does not change

- **Unchanged.** The study verdict ADMIT stays. So do:
  - E1 SHOWN.
  - E2 RECURRENT ADAPTATION SUPPORTED.
  - E3 NOT LOCALIZED BY THIS INTERVENTION.
  - K-FR E3 UNRESOLVED.
  - Every number, threshold, seed, split, budget, arm and file in `acquisition_results_v1/`.

  These are protocol verdict words and are kept as recorded (Constitution v3: "Preserve original study verdict words separately").
- **Changed.** Only the **prose headline / claim ceiling** used when the result is summarized. That covers the PR description, ledgers, synthesis cards and agent reports. The scoped wording in §3 below supersedes it.
- **Not a retroactive strengthening or weakening of any test.** No re-analysis is done. No E3 reinterpretation is made.

## 2. Exact current lines being superseded

From `acquisition_results_v1/RESULTS.md` (frozen; quoted verbatim, line numbers at `b25a30a`):

> L14: `## Claim ceiling`
>
> L16: `Within a supplied generic recurrent architecture with an external timing scaffold, gradient training on environment-supplied terminal outcomes acquired a history-dependent prediction function for X, Y and XOR in the frozen W2 world. …with a reliable contribution from recurrent adaptation relative to a frozen-recurrence readout.`

The same paragraph appears verbatim under "## Claim ceiling" in the PR #5 description.

L16 has three problems:
1. **"a supplied generic recurrent architecture"** names no specific network. The admitted result is for **GRU-8**: E1, E2 and E3 are GRU-8 tests.
2. **"…with a reliable contribution from recurrent adaptation relative to a frozen-recurrence readout"** is the protocol §9 append fragment (`E2_SUPPORTED_APPEND` in `twostream_acquisition_spec.py`), concatenated with its leading ellipsis. The result is an ungrammatical sentence. "Reliable contribution from recurrent adaptation" can also be read as a mechanism claim. E2 only shows that **allowing recurrent parameters to train improved held-out prediction relative to readout-only training on the matched frozen initialization**.
3. It does not say that causal localization was **tested and not demonstrated** (E3 NOT LOCALIZED BY THIS INTERVENTION). That fact appears only in the label list at L8.

Kept as-is and not superseded: L5–L12 (the verdict labels) and L20 (the "Not established" list). §3 extends L20.

**Withdrawn as an unqualified headline anywhere it is used:**

> "acquired [history-dependent] state that causally supports joint prediction"

This phrase does **not** appear in the PR #5 branch. It was checked by `rg` over the whole branch, including `RESULTS.md`, the protocol and the PR description. It comes from the pre-study ceiling proposal:
- Astra consult #1, part B: "Ceiling: acquired history-dependent state causally supporting joint prediction".
- `/workspace/review/twostream_acquisition_protocol_draft_v1.md` L402.
- The paraphrase in `/workspace/astra_consult_5_raw.md` L91.

It must not be used to summarize PR #5. E2 shows a benefit from allowing recurrent adaptation. E3 did **not** identify the proposed content-carrying subspace. Whole-state transplant equivalence (identity checks) gives no independent evidence of localization (consult #11 §1).

## 3. Superseding claim ceiling (ERRATUM-A v1)

> **Claim ceiling (supersedes RESULTS.md L16 for all summaries).** In the frozen W2 task, supervised training of a supplied GRU-8 with an external timing scaffold acquired history-dependent X, Y and XOR predictions. Training the recurrent parameters improved held-out prediction relative to readout-only training on the matched frozen initialization, under the declared budget. The tested causal localization was not demonstrated.

This is Astra's wording from consult #11 §1, verbatim except for the split into three sentences.

**Scope qualifiers (to be printed with the ceiling):**
- "Supervised" means gradient training on environment-supplied terminal outcome labels (protocol §9 base claim). No oracle forecast was used as a target.
- "Held-out" means the 64 TEST histories of the frozen split. Supporting numbers:
  - GRU-8 CAND median TEST E_total is 0.0021216866; K-FR GRU-8 is 0.05009871.
  - ratio_total ≤ 0.0677 in 10/10 seeds.
  - K-FR GRU-8 meets A-FIT in 0/10 seeds.
- "Matched frozen initialization" means K-FR: the same initialized GRU-8 with only the readout trained, on the same episode stream and with the same budget.
- Frozen GRU-16 and RNN-8 readouts also fail. Their median TEST E_total is 0.045078988 and 0.046842186. So the readout-only failure is not specific to GRU-8 (consult #11 §2). This **does not** show that recurrent training is necessary (Q-NECESSITY untested). No tuned or larger frozen reservoir was tested.
- "Tested causal localization": the cross-fitted 3-d chart-decoder partial transplant at stage 4 (protocol §6). All 10 GRU-8 seeds passed coverage and rank-3 requirements.
  - Partial-transplant vector ratios were 1.649–14.21, against a threshold of ≤ ½.
  - Complement-transplant vector ratios were 0.127–0.641, against a threshold of ≥ ¾. The complement tracked donors better than the chart subspace in every seed.
  - K-FR's E3 label is UNRESOLVED (coverage fails in 9/10 seeds), so it is not a clean negative control.

**Not established (extends RESULTS.md L20):**
- That the acquired recurrent parameters carry a localized, content-specific or independently manipulable state component.
- That the chart-decoder subspace is or is not the mechanism. A null under this intervention establishes neither a distributed code nor the absence of a low-dimensional mechanism. Nonlinear encoding, poor cross-fitted decoding (8 fit points in 8-d per fold), redundancy and hybrid-state artifacts all remain possible.
- That recurrent training is necessary.
- Irreducible joint state.
- Marginal-filter or mean-field identification.
- C4.
- Consciousness.
- Organism claims.
- The K-EXACT precision line (RESULTS.md L2339) is subject to the separate erratum B (`pr5_quantization_erratum_v1.md`). It does not enter this ceiling.

## 4. Ledger and question mapping (Constitution v3)

| Question | Status after PR #5 + erratum A |
| --- | --- |
| Q-EXIST | Not addressed by PR #5. W2 existence and the oracle come from PR #4. |
| Q-LEARN | **SUPPORTED_BOUNDED:** GRU-8 acquired the history-dependent X/Y/XOR prediction function (E1). Training the recurrent parameters improved held-out prediction over readout-only on the matched frozen init (E2). |
| Q-CAUSE | **NOT_ESTABLISHED:** causal localization was tested by the chart-decoder intervention and not demonstrated (E3). Identity and restoration checks are integrity checks, not causal evidence. |
| Q-NECESSITY | **NOT_ESTABLISHED / untested:** no tuned or alternative frozen reservoir was tried. The draft study `recurrent_core_transfer_protocol_draft_v1.md` addresses robustness only, not necessity. |

ORIGIN/ROLE/REDUCTION for the row "Recurrent dynamics organization" (protocol §10), recorded as:
- ORIGIN: **ACQUIRED (in part) at the level of "recurrent parameters that improve prediction"**.
- ROLE: "carries history" is **not** separately verified, beyond the fact that training it helps.
- The "Causal localization of forecast content" row stays **UNRESOLVED**.

## 5. Proposed adoption mechanics

1. Add `acquisition_results_v1_errata/ERRATUM_A_CLAIM_WORDING_v1.md` with §§1–4 above, as a new commit on the PR #5 branch or a follow-up PR. It quotes the frozen sha256 values above.
2. Do not modify `acquisition_results_v1/RESULTS.md`, `summary.json` (`claim` key), the protocol, or `twostream_acquisition_spec.py` constants.
3. Add one sentence pointing to the erratum file in the PR #5 description. This is a GitHub edit and is externally visible, so it needs Aidan's or the Specialist's go-ahead.
4. Any future card that cites PR #5 cites the §3 ceiling, not RESULTS.md L16.
