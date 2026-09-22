# Evidence index v1 — accepted capabilities mapped to their frozen studies

2026-09-22. Companion to `BASELINE_v1.md`. Maps each *accepted* capability to the frozen
study that establishes it, and separately lists the frozen studies that are **negative or
falsified** so they are never re-inherited as capabilities. A "frozen" entry means the study
has a hashed protocol, a results dir written under `mkdir(exist_ok=False)`, an audit script
that re-derives gates without simulating, and a replay script for sampled exact reruns.

Conventions: "results" = the `AC*_RESULTS_v1.md` narrative; "dir" = the frozen
`ac*_results_v1/` tree; "gates" = prespecified-gate outcome as recorded. Seeds are the
replication unit (N seeds × 2 histories = N independent units). Survival is a
bimodality-aware lower bound, never a per-seed-family guarantee.

## 1. Reference architecture components (the AC105 body)

| Component | Established by | Status |
| --- | --- | --- |
| `gray_ctl` — Gray-coded relinquishment streak, no reserve | AC99 (Gray encoding passes 5/5), AC100 (2×2 factorial isolates Gray, not reserve, as the carrier — 6/6) | ACCEPTED; reserve dropped as unnecessary for Gray |
| Persistent reconstruction trigger (fire while decoded program ≠ description-derived target) | AC103 (persistent vs current triggering — 3/6 gates, G1/G5/G6 pass) | ACCEPTED as the recovery mechanism |
| Allowance-42 material budget (`max(0, spendable − 42)`, `DECISION_ALLOWANCE = STREAK_N × 7`) | AC104 (6/6 gates, 5700-5707), AC105 (6/6 gates, 5800-5807, operating range) | ACCEPTED; generalization = one fresh instance + no-harm, not universal |

## 2. Accepted milestones

| Milestone | Frozen studies | Status |
| --- | --- | --- |
| Internal-state milestone (controller info maintained, reconstructed, transferred to successor storage) | AC85 (6/6), AC86 (7/7), AC87 (9/9), AC88 (9/9, byte-identical re-verification), AC89 (9/9, simultaneous + adversarial) | ACCEPTED; boundary in `CLOSURE_BOUNDARY_v2.md` |
| Gray encoding carries adaptation | AC99 (5/5), AC100 (6/6) | ACCEPTED |
| Composition (internal-state) | AC101 — G1/G3/G5/G6 pass 8/8; G2 behavioural composition FAIL 3/4 unseen | PARTIAL: internal-state composition accepted, behavioural (survival) composition not |
| Premature-termination vs resource-shortage separation | AC102 (6/8 gates), AC103 (3/6 gates; the *separation* finding stands) | ACCEPTED (the distinction); no spending policy resolves all combined failures |
| Internal spending rule | AC104 (6/6), AC105 (6/6) | ACCEPTED |

## 3. Accepted foundational capabilities

| Capability | Frozen study | Status |
| --- | --- | --- |
| Controller pays for its own repair | AC1 (+ follow-up + AC1–AC4 confirmatory, fresh seeds 5100–5507) | ACCEPTED |
| Produced W repair catalysts | AC2 | ACCEPTED (positive at two rates) |
| Produced C energy converters | AC3 | ACCEPTED (2/3 rates in confirmatory; one top-rate death recorded) |
| Produced B boundary + measured transport | AC4 / AC4_TRANSPORT | ACCEPTED |
| Integrated architecture sustains activity via repair | AC4_FOLLOWUP | ACCEPTED |
| Developmental allocation + broad controls (relocation, inert burden, protected copy, oracle) | AC9 controls v3 | ACCEPTED (frozen baseline, 64 rows) |
| Every constituent dependency isolated in the integrated body | AC10 (seeds 1300–1303, 72 rows, 9/9 gates) | ACCEPTED |
| Graded access law — being wrong costs a fraction, decision is real | AC15 (1900–1903, 5/5 gates) | ACCEPTED |
| Two-way relinquish/restore holds a route; separation of minima | AC18 (2500–2503, 8/8 gates) | ACCEPTED |
| Repair is load-bearing under sticky (non-self-reversing) damage | AC67 | ACCEPTED |
| Majority-read register closes the closure triplet at 16,384 ticks | AC71 | ACCEPTED |
| Erase-on-relinquishment makes the closure world-accommodating | AC75 (2900–2903, 8/8 gates) | ACCEPTED |
| Controller turnover / regeneration from a corruption-immune description | AC76 (3000–3003) | ACCEPTED (economically bounded) |
| Description maintenance (paid majority-restore of the stored description) | AC79 (4004–4007, 6/6 gates) | ACCEPTED |
| Reconstruction recipe internalized (full 78-bit description + own trigger) | AC80 (4008–4011, 6/6 gates) | ACCEPTED |
| Component replacement across generations (turnover accounting) | AC81 (4012–4015, 8/8 gates) | ACCEPTED |
| Unconditional turnover floor (births ≥ complement, every individual) | AC84 (6/6 gates) | ACCEPTED |
| Bank-rule convention stored, not derived | AC85 (4024–4027, 6/6 gates) | ACCEPTED |
| Recipe-bearing storage replaceable (slot succession + pointer) | AC86 (4016–4019, 7/7 gates) | ACCEPTED |
| W production is load-bearing for viability + maintenance capacity | AC91 (4200–4203, 7/7 gates) | ACCEPTED |
| Functional interruption-and-rescue (W cut mid-reconstruction) | AC92 (4300–4303, 6/6 gates) | ACCEPTED |
| Coordinator transition write W-gated | AC93 (4400–4403, 8/8 gates) | ACCEPTED |
| Coherent resumable succession | AC94 (4404–4407, 4 requirement-gates) | ACCEPTED |
| State sufficiency (observer-discard endpoint equivalence) | AC95 (4408–4411, 4/4 gates) | ACCEPTED |
| Internalized relinquishment streak (state sufficiency complete) | AC96 (4412–4415, 5/5 gates) | ACCEPTED (economic viability flagged, not gated) |

## 4. Negative / falsified frozen records (NOT capabilities — do not inherit)

| Study | Outcome | Why it is listed |
| --- | --- | --- |
| AC11 | Falsified by pre-run controls | state-blind fixed duty cycle beats the adaptive arm; do not run as written |
| AC13 | Falsified | calibration's saving did not replicate |
| AC14 | Negative | decision-state integrity not maintained by the loop (XOR self-reversing damage) |
| AC16 | Falsified (mean-margin gate, +0.2437 vs +0.25) | gate-shape lesson; mechanism intact |
| AC17 | Falsified (unsatisfiable dominance gate) | gate-shape lesson; separation of minima is the right test |
| AC97 | Falsified G1 | reserve withholds the decision it funds |
| AC98 | Falsified G1, passed no-harm | revised reserve insufficient (W-denominated shortfall) |
| AC102 | 6/8 gates (staging fails two ways) | recorded, not moved; the tested staging policy failed |
| AC103 | 3/6 gates | recorded; the *distinction* stands, no spending policy is universal |

## 5. Limits carried into every downstream card

- The controller's *interpreter* (`prog.choose`) and the succession *transition logic*
  (`advance()`) are supplied substrate — internalization covers information + working state,
  not the mechanism (AC90 review: boundary unresolved).
- Content self-production blocked (AC78); consciousness gate archived
  (`CONSCIOUSNESS_BLOCKS_DISPOSITION_v1.md`).
- The reserve is not in the reference architecture (AC100).
- External scaffolds (protected copy, fixed-correct oracle, machinery-only rescue re-seeds)
  are labeled EXTERNAL and never counted as autonomous results.

This index is a derived document and is not hashed into any study snapshot.
