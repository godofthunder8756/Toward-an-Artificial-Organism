## 5. Frozen item order, compute estimate and HARD CAP (consult #22, Q6; consult #23, named edit 8)

### 5.1 Item names and execution order (frozen at approval)

| Order | Item | Content | Depends on |
| --- | --- | --- | --- |
| 1 | ITEM-1 A-SYM | §1 (a)–(d) | — |
| 2 | ITEM-2 VALUES-H0 | MB, MB-myopic, BLIND, ORACLE at T = 1..10 × 6 costs; MB-CE and switch-aware descriptive at T ∈ {4, 6} | 1 |
| 3 | ITEM-3 VALUES-H1 | the same at T = 1..5; switches at T = 4 | 1 |
| 4 | ITEM-4 CONF | R-BLIND / R-CONF-S identity, R-CONF-ENUM, R-CONF-A (H0 T ≤ 10, H1 T ≤ 5, switches) | 1 |
| 5 | ITEM-5 CG | R-CG 6 variants (H0 T ≤ 8, H1 T ≤ 5, switches at T = 4) | 1 |
| 6 | ITEM-6 MF | R-HAC-MF 2 variants (H0 and H1 T ≤ 4, switches at T = 4) | 1 |
| 7 | ITEM-7 PM | PM-ACT closure and quotient (T_SEP ∈ {3, 4}), well-definedness checks, descriptive PM_k | 2 |
| 8 | ITEM-8 A-SEP | §4, all eligible agents and settings | 2, 4, 5, 6, 7 |
| 9 | ITEM-9 REPLAY | independent second implementation; coverage in §5.4 | 1–8 |

An overall A-SEP label for a setting requires ITEM-7 and ITEM-8 to be complete for that setting, and ITEM-9 agreement on every replayed quantity.

### 5.2 Estimate (analytic only; nothing executed)

The estimates assume CPython big-integer rationals at about 1–2 µs per elementary operation. Sizes are **conservative bounds**, not proven reachable counts.

| Item | Size (conservative bound) | Ops (est.) | Time (est.) | Peak memory (est.) |
| --- | --- | --- | --- | --- |
| ITEM-1 | **3,006,865 histories including the empty history** (Σ_{t=0..3} 144^t; lengths 1–3 alone total 3,006,864) × 2 laws; 136 patterns × 2 endpoints | ~1.2×10⁸ | 2–4 min | < 100 MB (streamed) |
| ITEM-2 | Σ_{T=1..10} C(T+11, 11) = 646,645 node-evaluations × 6 costs × 2 agents; switches (1,365 + 12,376) × 30 × 2 | ~8.6×10⁸ | 14–29 min | ≤ 1 GB |
| ITEM-3 | 194,870 × 6 × 2; switches 16,105 × 30 × 2 | ~3.3×10⁸ | 6–11 min | ≤ 0.5 GB |
| ITEM-4 | Σ 2^t = 2,047 θ-paths × 2 Z × 9 × 6 | ~2×10⁷ | < 1 min | negligible |
| ITEM-5 | 125,970 × 2 Z × 6 × 6; H1 6,188; switches 1,820 × 30 | ~2.0×10⁸ | 4–7 min | ≤ 0.5 GB |
| ITEM-6 | 346,201 × 2 Z × 6 × 2 (H0 and H1); switches 345,600 × 30 × 2 × 2 | ~5.8×10⁸ | 10–19 min | ≤ 0.5 GB |
| ITEM-7 | phase-expanded closure ≤ 3 × 2,730 = 8,190 states (T_SEP = 4) × 1,344 phase-1 symbols (6 costs × 8 y × 4 forced × 7 intervention inputs) × log₂ refinement; plus PM_k | ~1.6×10⁸ | 3–6 min | ≤ 0.3 GB |
| ITEM-8 | §4.2 bounds with clamp status × configurations (R-CG 12 per T_SEP, R-CONF-A 18, R-HAC-MF 4, others small) × 11 runs (intact; SWAP, CORRUPT and SUSPEND in 2 directions; A and B branches) | ~8.6×10⁸ | 15–29 min | ≤ 1 GB (configurations sequential) |
| ITEM-9 | §5.4 coverage, including an independent ITEM-7 refinement | ~4.6×10⁸ | 8–15 min | ≤ 0.5 GB |
| **Total** | | **~3.6×10⁹** | **≈ 60–120 min** | **≤ 1.5 GB** |

**Change from spec v2:**
- The total is essentially unchanged (≈ 3.6×10⁹).
- ITEM-7 falls from about 4.6×10⁸ to 1.6×10⁸: the time-to-go input is dropped because layer is part of the state, and the per-trial input is split into phases. Clamp closure partly offsets this.
- ITEM-8 rises from about 7×10⁸ to 8.6×10⁸: SUSPEND controls, A/B branches and clamp status.
- ITEM-9 rises from about 3×10⁸ to 4.6×10⁸: an independent PM refinement is added.
- The largest single item (ITEM-2 or ITEM-8) is ≤ 29 min.

### 5.3 HARD CAP (binding)

- One CPU process on the box. No GPU and no neural network.
- **≤ 4 hours total wall-clock**, **≤ 1 cumulative hour per named item, including retries**, **≤ 8 GB resident memory**.
- Verification and replay count toward these limits. "Include replay and restarts after engineering failures in the accounting."

**When a cap is reached:**
- "Preserve completed exact results when a cap is reached, but do not issue an overall label whose required comparisons remain incomplete."
- The item that hit the cap is marked UNRESOLVED-COMPUTE.
- "Mark dependent unexecuted work as NOT-RUN, rather than pretending it failed scientifically."
- "No in-place reduction of horizons or variants." Any change is a new spec version.
- Engineering failures are diagnosed.

### 5.4 Independent-replay coverage (exact; named edit 8)

Consult #23: "subset agreement is not verification of every unreplayed quantity."

**Replayed by a second implementation** (path enumeration versus merged or backward computation):

| Item | Coverage |
| --- | --- |
| ITEM-1 | (a), (c) and (d) in full; (b) for history lengths 0–2 (Σ_{t=0..2} 144^t = 20,881 histories per law) |
| ITEM-2 | V\*, V_myopic, V_blind and V_oracle for H0 fixed costs, T ≤ 4, all 6 costs |
| ITEM-3 | the same for H1, T ≤ 4 |
| ITEM-4 | R-CONF-A, H0, T ≤ 4, all 9 × 6 |
| ITEM-5 | R-CG, all 6 variants, H0 fixed costs, T ≤ 4 |
| ITEM-7 | an independent Moore-style refinement must yield the identical partition and quotient transitions |
| ITEM-8 | every statistic for MB and all R-CG variants at T_SEP = 3, both cost pairs |

**Not replayed:**
- all switch values;
- ITEM-2 and ITEM-3 beyond T = 4;
- ITEM-5 beyond T = 4;
- ITEM-6 in full;
- ITEM-8 at T_SEP = 4;
- ITEM-8 for R-HAC-MF, R-CONF-A, R-BLIND / R-CONF-S, MB-myopic and PM-ACT.

Every unreplayed quantity is tagged **NOT INDEPENDENTLY REPLAYED** in the outputs.

## 6. Outputs, sealing and replay

1. Before execution, freeze in an implementation manifest:
   - the cleared spec (final file name plus full sha256);
   - the code tree;
   - the §4.6 table, already frozen here.
2. Results are written as exact rationals (strings) in JSON, tagged with the spec and manifest hashes.
3. A disagreement between ITEM-9 and the primary results on any replayed quantity is an integrity failure. It is diagnosed, and no label is issued until it is resolved.
4. No result is used to retune rates, costs, horizons, margins, donors or variants. Any later change is a new version, marked as informed by results.

## 7. What this check can and cannot establish

**Can establish:**
- an implementation audit of L1;
- exact planning-advantage, adaptive-information-advantage and oracle-gap values;
- named-baseline performance;
- which prespecified response patterns distinguish the named analytic implementations, with per-control reproduction and criterion columns.

**Cannot establish:**
- acquisition;
- any learned-system property;
- absence of an assessment role in any control;
- whether assessment tracks predictor-specific departures from oracle correctness (§4.7);
- longer horizons or the full cost grid for A-SEP;
- reduction against unnamed controllers;
- C4 status.

**Ledger line (consult #23, Q10, verbatim):** "W-REL: admitted as a theory-stage C4 candidate. Exact-check specification under revision; execution pending Aidan's approval. No change to the C4 evidence or status row, and no system-level C4 conclusion."

## 8. Approval (PENDING) and approval record

| item | value |
| --- | --- |
| What needs approval | Execution of ITEM-1 … ITEM-9 under §5.3, after this spec is cleared and frozen with its implementation manifest. |
| Status | **PENDING. Not run. No item, partial item or test run of any item has been executed.** Consult #23: "Aidan has not answered, so execution remains pending." |
| Question | Unchanged. Consult #23: "The existing question still matches this bounded theory-only scope. No replacement question is needed." |
| Identifier | Spec v2's hash 04992f86… is not the final executable identifier. Consult #23: "The currently submitted spec hash 04992f86 is not the final executable identifier after these edits." This v3 file is also not final until cleared and frozen. |

**Approval question (consult #21, verbatim):**

> "Approve a theory-only C4 admission and identifiability study of W-REL, including bounded exact finite-horizon calculations of source identifiability, costly exploration and the named conventional control rivals? The analysis specification and compute limit will be fixed before execution. This approval excludes neural training, an exhaustive all-controller certificate, new architecture families, protected controllers or registers, and any claim that C4 or consciousness has been demonstrated. A later empirical C4 study would require separate approval."

**Scope attachment (consult #23, part D, verbatim; identifiers to be completed only after clearance and freeze):**

> "Scope attachment to the pending W-REL approval question: the executable specification will be [FINAL filename], SHA256 [full hash], with implementation manifest [identifier and hash], incorporating consult #23's required edits. Execution covers ITEM-1 through ITEM-9 only: bounded exact analysis of the world and named analytic controllers. Limits are one CPU process, no GPU, at most four hours total wall-clock, at most one cumulative hour per named item including retries, and at most 8 GB resident memory. Verification and replay count toward these limits. The exclusions in the original approval question remain unchanged. This attachment records scope; it is not an approval."

**Approval record (to be completed; consult #23: "Record Aidan's actual answer verbatim, with date, time in ET and source"):**

| field | value |
| --- | --- |
| Aidan's verbatim answer | [AIDAN'S VERBATIM ANSWER — not yet given] |
| Date | [YYYY-MM-DD] |
| Time (ET) | [HH:MM ET] |
| Source | [e.g. widget id / message id] |
| Final frozen spec | [FINAL filename] |
| Final frozen spec SHA256 | [full hash] |
| Implementation manifest | [identifier and hash] |
| Limits | one CPU process, no GPU, ≤ 4 h total wall-clock, ≤ 1 cumulative hour per named item including retries, ≤ 8 GB resident memory; verification and replay count |

Per consult #22: "Do not ask Aidan to approve the same scope again if he approves that question with this specification attached."

## 9. Remaining questions

All ten consult #23 questions are answered and applied (§10). No open scientific question is carried by this spec. Remaining items before freeze are clerical (§10, final note).

## 10. Application log: consult #23

| Item | Applied in |
| --- | --- |
| Q1: shared-core label; separate per-control columns; strict DISTINGUISHES | §4.5 |
| Q2: binary K primary; limitation verbatim; Brier descriptive; no scoring-rule variant | §4.4, §4.7 |
| Q3: prospective margins with rationale; exact equality for invariants; all thresholds frozen | §4.4, §4.6 |
| Q4: R-HAC-MB-CE; switch-aware values descriptive, additional information identified | §0.3, §3.1 |
| Q5: R-HAC-MF kept as a myopic contextual action-value learner; no γ = 1 | §3.5 |
| Q6: CORRUPT is a compound intervention; SWAP primary; SUSPEND control; suspension end in every branch; PM clamp transitions | §4.2, §3.7 |
| Q7: per-setting labels and eligible lists; MF at T = 3 only; bounded scope | §4.1, §4.5 |
| Q8: R-BLIND / R-CONF-S one control; NOT APPLICABLE rule | §3.3, §4.2, §4.5 |
| Q9: PM-ACT preserves (action, decision) only; F0 substitution attribution | §3.7 |
| Q10: ledger line verbatim | §7; admission v3.1 |
| Edit 1: label rule completed; automatic revision trigger removed | §4.5; admission v3.1 §7 |
| Edit 2: m_a(H, I); Z-selection in the procedure; frozen readouts; absolute error and change from intact | §4.3 |
| Edit 3: C-T2 zero-baseline wording; λ_a threshold symbol and population; over/underestimation terminology | §4.4 |
| Edit 4: rescue with a shared A/B trajectory, matched-history shadow, credit relative to A, intact C separate | §4.4 |
| Edit 5: PM-ACT intervention closure, event-order phases, frozen donor/restore maps, well-definedness | §3.7 |
| Edit 6: Brier only; log scores removed | §4.4 |
| Edit 7: full threshold table and applicability rules; donor ties; absent contrast; admission tie-rule sync | §4.6; admission v3.1 §3 |
| Edit 8: bounds versus proven counts; ITEM-1 count corrected; replay coverage exact | §4.2, §5.2, §5.4 |
| Part D: scope attachment and approval record template | §8 |

**Final note: clerical items before freeze.**
- Fill the approval-record placeholders.
- Produce the implementation manifest.
- Hash the cleared final file.
