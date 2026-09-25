# AC116 (C3) — the counter-vs-tuned-memoryless storage comparison in the pure gated world

2026-09-24. The C3 deliverable (task `t_c8bbb211`): execute the ONE study the C2 identification
(`C2_STORAGE_COMPARISON_v1.md`, task `t_04ae4ff3`) left open — the POSITIVE direction of the C2
gate's claim. This protocol is hashed BEFORE the finals are accessed.

---

## 1. Question and the hypothesis under test

**Question.** In the occluded-`used_held` world (the C2 gate, ε=0), at high occlusion (q=0.9), does
maintained retained history — an accumulated, vulnerable, paid-maintained integer counter —
demonstrate a decision-relevant advantage over the strongest TUNED memoryless policy receiving the
same current observations, on a graded endpoint?

**Support hypothesis (the claim being tested for falsification).** Retained history contributes a
decision-relevant difference at the organism scale that a tuned memoryless policy cannot match: the
counter relinquishes a stale route under move faster than "wait for an open contact", while holding
under cut (via the open-blind hold latch), net of the false-drop risk.

**Named falsifications (all legitimate findings, none converted into a passing gate):**

- **F1 (no demonstrated advantage).** The counter offers no graded (income) advantage over the tuned
  memoryless rival within noise. This CLOSES the storage line at the organism scale (retained history
  does not demonstrate a decision-relevant edge over the strongest memoryless policy).
- **F2 (no-advantage, negative).** The counter is informative but worse than the tuned rival.
- **F3 (no-information).** The counter's read content does not causally matter even against its own
  read-forced (scramble) control.

The C2 design's honest prior (§6) is an F1 outcome: a "thin, possibly sub-resolution graded advantage"
that converts the weakly-load-bearing measurement into a definitive organism-scale statement.

## 2. Architecture (frozen: the AC110 world, extended with the counter and its rivals)

The world is the AC110/C2 gated world (imported unmodified from `ac110.py`; the counter/tuned/no_write/
scramble arms are new allocations running in that world). ε = 0 by construction: `ac110`'s contact line
has no residual-yield surgery, so a held stale entry yields exactly 0 under move — the PURE gated world
C2 §5 names as the clean comparison. Two causes land at t=8192:

- **move** — the channel-1 mapping flips; the route-1 entry is intact but STALE. Correct: relinquish.
- **cut** — the route-1 read is suppressed for [8192, 8288); the entry is intact. Correct: hold.

The C2 occlusion gate: on a Bernoulli(q) fraction of channel-1 contacts the `used_held` bit is
forwarded as `2` (occluded), so at an occluded-unproductive contact both causes read
`(bound=1, used_held=occluded, productive=0)` identically while the correct action differs.

**Arms (decision-time information prespecified).**

| arm | decision state | decision-time information |
|---|---|---|
| `counter` | 3-bit Gray integer counter (dead-rule free bits) + 1-bit hold latch | accumulated occluded-unproductive count, negative productive weight, latch on open blind; drop at counter ≥ N |
| `tuned` | NONE (memoryless) | current `(bound, used_held, productive)` triple + one coin; drop on occluded-unproductive with prob p; open contacts forced (relinquish on open held-fail, hold on open blind/productive) |
| `estimate` | 1-bit cause estimate + frozen per-key streak | the AC110 GatedEstimator (retained history WITHOUT accumulation) |
| `no_write` | counter with the counter's paid write DISABLED (read honest) | acquisition cut — separates "accumulated value" from "write machinery" |
| `scramble` | counter with the counter READ forced to 0 (writes intact) | read-only causal-role control |

Repair intervention deliberately OMITTED (C2 §5): the claim is about acquisition, not repair; AC110
already established repair is not load-bearing in-window. Retained-history dependence (counter vs
tuned) is tested SEPARATELY from ongoing-repair dependence (AC110's question, not re-tested), so no
combined pass/fail label obscures which capability succeeds. Calibration deliberately OMITTED: the
counter is a categorical latch, not a probabilistic confidence estimate — no confidence score is
invented to satisfy a gate.

## 3. Declared world constants

- q = 0.9 (primary), q = 0.7 (secondary), q = 0.5 (the clean-control anchor only), ε = 0.
- PORTS = 4, WINDOW = 96, TICKS = 16384, DEV = 512, MOVE_TICK = CUT_TICK = 8192.
- YIELD_M = 64, YIELD_F = 64 (the AC107/110 world), blind fallback uniform over 4 ports.

## 4. Conditions

- `no_cause` — no intervention (clean control).
- `move` — channel-1 mapping flips at t=8192. Correct: relinquish.
- `cut` — route-1 read suppressed for [8192, 8288). Correct: hold.

## 5. Endpoints (reported; only the graded income endpoint is gated)

1. **Post-cause income per channel** (`income_post` = Σ_{t≥8192} (in_m + in_f)) — PRIMARY graded
   decision-utility endpoint. Combined score = income_post(move) + income_post(cut).
2. **Relinquish-under-move latency** = first drop tick − 8192 (None if never dropped).
3. **Cut false-relinquish rate** = relinquishment count under cut.
4. **Mechanism readout (reported, not gated):** per-channel counter value and hold-latch state at
   horizon, counter/bel writes.
5. **Survival (reported, not gated):** bimodality-aware lower bound only (AC45/AC68); survival is
   confounded by re-acquirability and churn.

## 6. Prespecified parameter grids (both families swept — AC11's rule)

- counter threshold N ∈ {1, 2, 3, 4, 5, 6} (productive weight w = −6 fixed — reset-on-productive, the
  design's "negative productive weight").
- tuned ambiguity parameter p ∈ {0.00, 0.25, 0.50, 0.75, 1.00}.

## 7. Cohort, tuning, and stopping rule

- **Engineering** (DISCLOSED, excluded from the finals): seeds 0–7. Used ONLY to select the fixed
  comparison parameters N* (counter) and p* (tuned) by maximising combined post-cause income, and to
  confirm the arms discriminate. The measured engineering surface (q=0.9):

  - counter N: combined income **flat** across N (561,728–562,240 over 16 individuals; the strict
    argmax is N=1, which degenerates to the p=1 tuned rival — drop on the first occluded contact);
    cut false-relinquish falls monotonically 14→2 as N grows 1→6.
  - tuned p: combined income flat for p ≥ 0.25 (560,800–560,960; the strict argmax is p=1.00); p=0
    (hold-on-occluded) collapses under move (4 deaths, income 523,328) — a churn-death artifact, not
    a decision-quality result (AC113 rule 3).

  **Selected and fixed here, pre-run: N\* = 4, p\* = 1.00.** N\* = 4 is the mid-threshold where the
  counter genuinely accumulates before dropping (the design's "accumulate then drop", avoiding the
  N=1↔p=1 degeneracy); p\* = 1.00 is the income-max. The income surface is flat, and the verdict is
  F1 at EVERY (N, p) in the grid (see §8) — the equivalence is robust to where the optima are
  selected (AC113 rule 4). The full engineering sweep is a declared diagnostic, never the gate.

- **Finals** (confirmation, untouched): seeds 6600–6607 (8 seeds × 2 histories = 16 individuals),
  disjoint from 0–7, 6000–6007 (AC107), 6100–6107 (AC108), 6200–6207 (AC110), 6300–6307 (AC111),
  6400–6407 (AC113), 6500–6507 (AC114).

- **Stopping rule.** The finals are the confirmatory sample, run ONCE after this protocol is hashed.
  Gates are NOT moved after seeing the result; a failed gate is recorded with its measured value.
  No individual, seed, condition, or configuration is dropped post hoc.

## 8. Gates (prespecified; validity gates must pass, the comparison is a measured verdict)

**G1 (world license / clean control).** The `estimate` arm reproduces the frozen AC110 `maintained`
arm byte-for-byte (`state_hash`) at q=0.5 on the AC110 frozen seeds 6200–6207 (8×2×3 = 48 cells).
This licenses the world construction. (The C2 design's G1 wording "the candidate reproduces AC110"
is interpreted as the estimate arm, since the counter is a different decision object and cannot be
byte-identical to AC110's one-bit estimate; see C2 §6.)

**G2 (no-cause identity).** In `no_cause`, the four counter-family arms (`counter`, `tuned`,
`no_write`, `scramble`) are byte-identical to each other (`state_hash`), and all five arms have 0
relinquishments and complete. (The `estimate` arm is exempt from byte-identity: it maintains the
frozen per-key streak for BOTH channels, a different decision-state structure — measured distinct
from the counter family at tick ~100, the first channel-0 unproductive contact.)

**G3 (causal role / content matters).** At fixed N\*, the counter's accumulated content causally
matters: (a) under move, the counter's first-drop tick is ≤ the scramble's in every individual with
strict inequality in ≥ 1 (accumulation accelerates the drop ahead of the open held-fail path); (b)
under cut, the counter false-relinquishes in ≥ 1 individual while the scramble (read forced 0)
false-relinquishes in 0. Failure of BOTH (a) and (b) = F3 (no-information).

**G4 (the scientific question — a measured verdict, not a pass/fail gate).** At the fixed parameters
(N\*, p\*), compute the per-individual combined post-cause income difference
d_i = income_post(counter) − income_post(tuned) on the finals, aggregate the two histories WITHIN each
seed (n = 8 seeds; R1's correction), and run the exact sign-flip test over the 2^8 sign assignments
(AC38/AC46). Verdict:

- SUPPORT (bounded) if mean(d) > 0 AND p ≤ 0.05.
- F2 (no-advantage, negative) if mean(d) < 0 AND p ≤ 0.05.
- **F1 (no demonstrated advantage) otherwise** (mean small or p > 0.05) — the verdict vocabulary is
  "no demonstrated advantage", never "equivalence" from nonsignificance.

The (move-latency, cut-false-relinquish) Pareto readout is reported alongside G4 (the design's
"defer-vs-act" readout); it is descriptive, not a separate gate. No mean-margin gate (AC16), no strict
per-individual dominance that the ceiling makes unsatisfiable (AC17).

## 9. Reporting scope

Every endpoint is reported per independent seed, the two histories reported separately from the
across-seed sample. A negative comparative result bounds usefulness in the tested task; it does NOT
erase any prior representational finding (AC107's positive content-role, AC108's acquisition
necessity, AC110's repair-dependence, AC113's single-counter sufficiency all stand). Neither outcome
revives the ε-world weighting question (AC113 settled it) nor the repair question (AC110 settled it).

## 10. SOURCES (declared, hashed pre-run)

ac116.py ac110.py ac112.py ac107.py ac106.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py
ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py
ac4_transport.py ac1.py AC116_PROTOCOL_v1.md

Verification tools (audit_ac116.py, replay_ac116.py, test_ac116.py) are NOT in the frozen hash set
(AC16/AC17's rule).
