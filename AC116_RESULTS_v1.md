# AC116 (C3) results v1 — no demonstrated income advantage over the tuned memoryless rival (F1)

Frozen on finals 6600–6607 (8 seeds × 2 histories = 16 individuals), q = 0.9, ε = 0 (the pure C2
gated world), `AC116_PROTOCOL_v1.md` hashed pre-run (`pre_run_snapshot.json`). Engineering seeds
0–7 selected the fixed comparison parameters (disclosed in the protocol) and are excluded from the
sample. 240 rows.

## Verdict

**F1 (no demonstrated advantage).** At the organism scale in the pure occluded-`used_held` world,
the maintained integer counter does **not** demonstrate a significant post-cause income advantage
over the strongest tuned memoryless rival. At the fixed parameters (N\* = 4, p\* = 1.00) the
counter's per-seed combined income is directionally higher in 5/8 seeds, tied in 3/8, and **never
lower** — mean difference **+200** (≈ 3 contacts), exact sign-flip **p = 0.0625**, just above the
prespecified 0.05. This is the "thin, possibly sub-resolution graded advantage" the C2 design's
honest prior predicted (§6); it materialised exactly at the resolution edge and is recorded as
**no demonstrated advantage**, not as support.

This is the completion the C2 identification was built to produce: retained history does **not**
demonstrate a decision-relevant income edge over the strongest memoryless policy at the organism
scale, and the storage line is closed at this scale. It does **not** erase any prior representational
finding (see Scope, below).

## Gates (prespecified; measured, not moved)

| gate | claim | required | measured | verdict |
|------|-------|----------|----------|---------|
| G1 | world license: estimate reproduces frozen AC110 `maintained` (q=0.5) | 48/48 | 48/48 | PASS |
| G2 | no-cause identity: counter family byte-identical, all arms 0 relinquish | — | 0 violations | PASS |
| G3 | causal role: content drives the decision | (a) or (b) | both | PASS |
| G4 | graded income comparison (fixed params, paired sign-flip) | verdict | F1 | F1 (recorded) |

## G4 — the scientific question (the fixed comparison)

Fixed parameters (engineering-selected, disclosed): **N\* = 4** (counter threshold), **p\* = 1.00**
(tuned ambiguity). Per-seed combined post-cause income difference d = income_post(counter) −
income_post(tuned), two histories aggregated within each seed (n = 8):

- mean **+200**, observed sum **+1600**, exact sign-flip **p = 0.0625**.
- differences: `[0, 0, 0, +128, +192, +192, +512, +576]` (counter − tuned).

The counter is **weakly dominant** on income (0 seeds worse, 5 better, 3 tied) but the margin is
sub-significant at the prespecified threshold. The full engineering sweep confirms the equivalence
is robust to parameter choice: at every (N, p) in the grid the comparison is F1 (p ≥ 0.125 for
p ≥ 0.25; the only p with a large margin is p = 0, which collapses under move from churn-death — a
survival artifact, not a decision-quality result, AC113 rule 3).

## The Pareto readout — the defer-vs-act tradeoff, and why the counter's edge is income-invisible

| arm | move latency (ticks) | cut false-relinquish | notes |
|---|---|---|---|
| `tuned` (p=1) | **19.0** | 16/16 | fastest drop, zero cut-safety |
| `counter` (N=4) | 21.75 | **4/16** | intermediate: latch gives cut-safety at a small speed cost |
| `scramble` (read 0) | 23.7 | 0/16 | slow, safe (never drops via accumulation) |
| `no_write` (write cut) | 23.7 | 0/16 | slow, safe — but dies 4/16 under move (below) |
| `estimate` (1-bit) | 30.4 | 0/16 | slowest, safe |

The counter sits at a **genuinely intermediate** Pareto point the single-parameter memoryless rival
cannot reach: its open-blind hold latch gives it 4× the cut-safety of the p=1 rival (4 vs 16 false
relinquishments) at only a small move-latency cost (21.75 vs 19.0). This is the mechanism the C2
design named — "relinquish faster than wait-for-open under move, net of false-drop risk under cut".
**But it is income-invisible**: under cut a false relinquishment merely re-binds the entry (the
entry `life=64` refreshes on re-acquisition), so the counter's cut-safety does not translate into
income (AC113 rule 1: "a false relinquish actually refreshes the entry"). The graded INCOME gate is
flat; the counter's real advantage lives in a decision-quality axis (cut-safety) that this world's
economics do not price.

## G3 — causal role (information carried + causally effective, but thin)

At N\* = 4: (a) under move the counter drops **earlier than** the scramble (read forced 0) in 12/16
individuals and equal in 4/16, **never later** — the accumulated count accelerates the drop ahead of
the rare 10% open held-fail path; (b) under cut the counter false-relinquishes in 4/16 where the
scramble holds in 0/16 — the accumulated content causally drives the decision. The content is
informative and causally effective; its measured *usefulness* is the F1 income result.

## Acquisition cut (no_write) — the write machinery is load-bearing for SURVIVAL, confounded by schedule

`no_write` (counter write disabled, read honest) dies **4/16** under move (seeds 6603, 6604, both
histories, t ≈ 8442–8540, routes `[None, None]`): without the accumulation the organism never drops
the stale route and starves waiting for the open held-fail. The `scramble` (write intact, read forced
0) dies only **2/16** (seed 6603) — it accumulates but reads 0, so it too never drops via the
threshold, yet its counter WRITES perturb the contact schedule enough to survive on 2 more seeds.
This is the AC109 "storage write shifts the contact schedule" effect, now shown to be partially
protective: the counter's write machinery is load-bearing for *survival* under move, but the load is
a schedule perturbation, not a clean read-content effect. The `counter` and `tuned` arms survive
16/16.

## Expenditure (resource accounting)

The counter pays for its retained history: **~37 counter replicas** under move, **~63 under cut**
(mean, per individual); the tuned rival writes **0** decision state, the estimate 0, `scramble`
~14–21 (writes accumulate, read discarded). The counter's decision-state write cost is ~1/35th of
the shared program-repair cost (`reg_writes` ~2,170), so the retained history rides the program
maintenance at negligible marginal cost — but it buys no significant income.

## Engineering-vs-finals (AC39, in the unfavourable-but-mild direction)

Engineering (0–7): counter N=4 vs tuned p=1, mean +96, p = 0.5. Finals (6600–6607): mean +200,
p = 0.0625. Both F1, but the finals are directionally stronger (the counter never loses on the
finals, vs a mixed sign on engineering). The transfer is stable in verdict, unstable in magnitude —
report the finals as the record.

## What this establishes (and does not)

- **Established.** In the pure occluded-`used_held` world (ε=0, q=0.9), a maintained integer counter
  does not demonstrate a significant income advantage over the strongest tuned memoryless policy at
  the organism scale. Its accumulation is causally effective (G3) and weakly dominant on income (never
  worse, +200/seed, p=0.0625), and its open-blind latch buys a real cut-safety edge (4/16 vs 16/16
  false relinquishments) that this world's economics do not price. The storage line closes at the
  organism scale: retained history beats tuned memoryless on no graded income endpoint.
- **Not established.** No significant income advantage; no survival advantage for the counter over
  the tuned rival (both 16/16); no maintenance-dependence claim (repair was deliberately out of
  scope — AC110's question, not this one). A negative comparative result bounds usefulness in the
  tested task; it does NOT erase AC107's positive content-role, AC108's acquisition necessity,
  AC110's repair-dependence, or AC113's single-counter sufficiency.

## Scope notes

- **q = 0.7 declared secondary, not frozen.** The protocol declares q = 0.7 as a secondary world
  constant; the frozen study covers the primary q = 0.9 (the informative end — C4 rule 3: the
  accumulator is load-bearing only at high occlusion, and at q = 0.7 the open decisive path does
  most of the work, so the comparison is even less informative). The card's "ONE bounded study" is
  the q = 0.9 confirmation; the q = 0.7 diagnostic is left unfrozen rather than run as a second
  study.

## Files

- runner: `ac116.py` (extends `ac110.py`; the counter/tuned/no_write/scramble arms are new
  allocations in the AC110 world)
- protocol: `AC116_PROTOCOL_v1.md` (hashed pre-run)
- frozen results: `ac116_results_v1/` (`pre_run_snapshot.json` + `rows.jsonl` 240 rows +
  `results.json`, clean control 48/48)
- audit: `audit_ac116.py` (re-derives coverage, G2/G3/G4 from the saved table WITHOUT simulating) —
  PASS
- replay: `replay_ac116.py` (12 sampled exact reruns, byte-identical `state_hash`) — PASS
- tests: `test_ac116.py` (11 tests: world license, no-cause identity, decision mechanics, recorded
  gates pinned as F1) — PASS
- engineering (disclosed, excluded): seeds 0–7 (`ac116_engineering_v1/`, 592 rows: cohort + N/p
  sweep)
