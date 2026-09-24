# R1 — AC113 F1 reanalysis: seed-level paired structure (correcting the statistical interpretation)

2026-09-24. Reanalysis of the SAVED AC113 frozen rows (`ac113_results_v1/`,
`ac113_results_v1_eps002/`). No rerun; no frozen artifact edited or re-hashed.
This note supersedes the statistical interpretation in `AC113_RESULTS_v1.md`
§"Verdict" and §"What this establishes (and does not)", and in the P6 handoff,
while preserving every measured number as the historical record.

Supporting (non-frozen, exploratory) scripts: `_r1_reanalysis.py` (seed-level
paired recomputation), `_r1_deaths.py` (per-seed outcome table).

---

## Headline (adopted)

The tested weighted two-counter did not demonstrate an income advantage over the
single-counter rival; the frozen comparison also exposed seed-dependent candidate
failures.

---

## 1. The historical F1 gate result is preserved; its decision rule does not establish equivalence

The frozen G-COMPARE verdict stands as recorded, at the fixed engineering-selected
parameters θ\* = 0.5 vs (w,N)\* = (−6,4) [ε=0.08] and (−6,1) [ε=0.02]:

- ε=0.08: mean individual difference **−2336**, observed sum −37376, sign-flip **p = 0.375**.
- ε=0.02: mean individual difference **−2344**, observed sum −37504, sign-flip **p = 0.305**.

The prespecified rule maps this to F1 ("equivalence") as: mean < 0 but p > 0.05.

That rule commits the **nonsignificance ⇒ equivalence fallacy**. "We failed to
detect a difference at n = 16" is not "the arms are interchangeable." A
nonsignificant result is compatible with (a) a true zero difference, (b) a true
nonzero difference the study is underpowered to detect, and (c) a true difference
masked by the wrong unit structure. The frozen data are consistent with all three;
the F1 label asserts only the first. The correct reading is **"no demonstrated
advantage,"** not "equivalence."

---

## 2. Seeds are the units, not histories — and the two histories are byte-identical

`AC113_PROTOCOL_v1.md` §9 already declares the intended structure: "Every endpoint
is reported per independent seed, and the two histories (correlated matched
arm-runs, same seed) are reported separately from the across-seed sample." The
frozen verdict then violated its own protocol by pooling 8 seeds × 2 histories =
16 individuals as n = 16 independent paired units and running the sign-flip test
over 2^16 assignments.

The empirical situation is stronger than "correlated": **the two histories within
a seed are byte-identical.** For every (seed, arm, condition), history 0 and
history 1 agree on `state_hash`, `income_post`, `first_dead`, `relinquishments`,
`counter_writes`, `reg_writes`, `n_u`, `n_p`, and `holding` — 0 mismatches across
the whole cohort. Cause: `ac113._run_core` passes `activation = [True, True]` and
`grow = True` unconditionally, and the candidate arms (`two_counter`,
`single_counter`, `scramble`, `immediate`) never draw the history-seeded stream
(`ac12.Alloc.rng = default_rng([seed, history, 12012])` is consumed only by the
`random`/`fixed_schedule` arms). The damage, gate, residual-yield, coin, and
description-damage streams are all seeded on `[seed, …]` alone.

So the "16 individuals" are 8 distinct seeds, each run twice identically. The
frozen p-values are computed on a doubled sample. The corrected paired comparison
aggregates the two histories **within** each seed first (seed-level combined
income = Σ_histories [income_post(move) + income_post(cut)]), giving n = 8 paired
seed-level differences and an exact sign-flip test over 2^8 assignments.

| regime | n | mean d | median d | SD d | observed Σ | sign-flip p |
|---|---|---|---|---|---|---|
| ε=0.08 (individual, frozen) | 16 | −2336 | 0 | — | −37376 | 0.375 |
| ε=0.08 (**seed**, corrected) | **8** | **−4672** | **0** | 13320 | −37376 | **0.7109** |
| ε=0.02 (individual, frozen) | 16 | −2344 | 0 | — | −37504 | 0.305 |
| ε=0.02 (**seed**, corrected) | **8** | **−4688** | **0** | 13260 | −37504 | **0.6250** |

The seed-level mean is exactly double the individual-level mean (each seed's
income is the sum of two identical history-runs); the sign-flip p is roughly
doubled (0.71 vs 0.375; 0.63 vs 0.305) once the duplicated histories are no
longer counted as independent evidence.

---

## 3. Effect sizes, seed-level outcomes, uncertainty, survival failures

Per-seed paired differences d = two_counter − single_counter (combined move+cut
income), ε=0.08: **+128, −384, +128, +256, −128, −128, −37632, +384**; ε=0.02:
**+128, 0, +128, −256, 0, −37504, 0, 0**.

- **The mean is negative but entirely a single-seed collapse tail.** The mean
  difference is −4672 (ε=0.08) / −4688 (ε=0.02), ≈ −6.1% of the rival's mean
  combined income (~38232 / ~35864). The median is **0** in both regimes. Excluding
  the one collapse seed, the remaining 7 seeds are within ±384 (ε=0.08) / ±256
  (ε=0.02) — under ±0.5% — with a near-zero mean (+36.6 / 0). The endpoint is
  **bimodal**: a near-perfect tie on 7/8 seeds plus one catastrophic failure, not a
  graded spread.

- **The collapse is seed-dependent and lands on the finals, not engineering.** The
  two large negative differences are deaths at first_dead ≈ 8443 (ε=0.08, seed
  6406 under `cut`; ε=0.02, seed 6405 under `move`), with `relinquishments = 1`,
  `routes = [None, None]`, and income_post ≈ 256 (a ~49% loss of that seed's
  post-cause income). The recorded mechanism (results doc §"collapse tail") is a
  false relinquishment from accumulated weak-M evidence at the aggressive θ\*=0.5;
  the organism then starves and dies.

- **Survival (seed-level, 8 seeds per arm-condition):**

| arm | ε=0.08 move / cut | ε=0.02 move / cut |
|---|---|---|
| two_counter (θ\*) | 8/8 / **7/8** | **7/8** / **7/8** |
| single_counter ((w,N)\*) | 8/8 / 8/8 | 8/8 / **7/8** |
| scramble (θ\*=0.5) | 8/8 / **7/8** | 8/8 / **7/8** |
| immediate | **4/8** / 8/8 | **5/8** / 8/8 |

Candidate survival failures: ε=0.08 → 1/8 seeds (6406, `cut`), rival 0/8 — a
**candidate-only** failure. ε=0.02 → 2/8 seeds (6405 `move` candidate-only; 6406
`cut` **shared** — the single-counter rival and the scramble also die identically
at 8443 on 6406 cut). The rival therefore does NOT cleanly dominate at ε=0.02: on
one seed both arms fail identically.

- **Uncertainty.** With n = 8 the exact sign-flip test has a minimum attainable
  p of 2/2^8 = 0.0078, and the endpoint is bimodal (near-tie vs rare collapse), so
  the study resolves essentially nothing below a whole-seed collapse. The honest
  uncertainty statement is: any two-counter income advantage is either absent or
  smaller than the across-seed spread this sample can resolve, and the only
  signal that rises above noise is a seed-dependent candidate failure.

---

## 4. Frozen engineering-selected comparison vs exploratory finals-selected optima

Two distinct comparisons must not be conflated:

- **Frozen (confirmatory).** θ\*=0.5 vs (w,N)\*=(−6,4) [ε=0.08] / (−6,1) [ε=0.02],
  selected on engineering seeds 0–3 and disclosed pre-run (`AC113_PROTOCOL_v1.md`
  §7). The verdict (F1) rests on these alone. Result: no demonstrated advantage,
  one candidate-only collapse seed (ε=0.08), one candidate-only + one shared
  collapse seed (ε=0.02).

- **Exploratory (in-sample, chosen ON the finals — NOT the frozen verdict).** The
  finals' own income-maximising grid points, recomputed from the saved sweep rows:
  two-counter **θ = 0.60**, single-counter **(w,N) = (−2, 4)**, in both regimes.

  - ε=0.08: two_counter 611,840 combined; single_counter 611,840 — a **tie** (as the
    results doc reported).
  - ε=0.02: single_counter **611,584** vs two_counter **573,696** — the single
    counter **beats** the two-counter by ~6.6% at the finals-selected optima.

  The results doc's claim that "the equivalence is robust to where the optima are
  selected" holds at ε=0.08 **only**; at ε=0.02 the exploratory in-sample optimum
  is decided in favour of the single counter. This is a further recorded
  contradiction of "matches every decision-relevant endpoint" (see §5), and it is
  exploratory — it was selected on the same finals it is scored on, so it carries
  no confirmatory weight.

---

## 5. "Matches every decision-relevant endpoint" is contradicted by recorded outcomes

`AC113_RESULTS_v1.md` §"What this establishes" states the single counter "matches
a maintained two-counter weighted estimate on every decision-relevant endpoint at
the organism scale." Four recorded outcomes contradict "matches every endpoint":

1. **Survival.** ε=0.08: the candidate dies on seed 6406 (`cut`) where the rival
   survives 8/8. A seed-dependent survival failure is not "matching."
2. **Expenditure.** `counter_writes` 77.4 (two-counter) vs 40.2 (single-counter),
   ε=0.08 cut (59.5 at ε=0.02): the candidate pays ~2× the decision-state write
   cost for no graded gain. "Pays twice as much" is not "matches."
3. **Cut false-relinquish (V2).** At θ = 0.6 the candidate false-relinquishes in
   4/16 while the scramble holds in 0/16 — the accumulated content causally drives
   a **harmful** decision. "Causally effective but not useful" is not "matches."
4. **Exploratory finals optima.** At ε=0.02 the finals-selected single counter
   beats the finals-selected two-counter (§4).

The defensible formulation is: **at the fixed engineering-selected parameters the
two arms are statistically indistinguishable on the graded income endpoint
(seed-level p ≈ 0.71 / 0.63)** — i.e. no demonstrated advantage — and the
candidate is worse on survival, expenditure, and cut false-relinquish. "Matches
every decision-relevant endpoint" must be withdrawn.

---

## 6. No retrofitted equivalence margin

The frozen F1 rule already asserted equivalence from nonsignificance. I do not now
repair that by introducing a post-hoc Δ-equivalence margin and presenting it as
confirmatory. Any equivalence statement here would be **exploratory only**, and
would require a prespecified margin plus a power analysis that neither the
protocol nor the frozen sample supports (n = 8, minimum attainable p = 0.0078,
bimodal endpoint). This note therefore reports only **no demonstrated advantage**
with the seed-level structure and the candidate's observed failures — it does not
claim the arms are equivalent.

---

## 7. "No demonstrated advantage" ≠ "capability falsified" ≠ "first-order uncertainty is a wall"

- **No demonstrated advantage** — **true at the fixed parameters.** Seed-level
  sign-flip p = 0.71 (ε=0.08) / 0.63 (ε=0.02); the mean is negative but is driven
  by one collapse seed and is consistent with zero.
- **"The capability is falsified" (heterogeneous weighting is provably not
  load-bearing)** — **not established by this sample.** That conclusion requires a
  test that can distinguish "no effect" from "effect smaller than the study's
  resolution." Here n = 8 and the endpoint is bimodal; the P4 harness prediction
  (+0.03…+0.32 min-mean regret) is far below what this organism-scale sample can
  resolve. The frozen sample shows the two-counter is **not demonstrably**
  load-bearing — "not demonstrated," not "proven absent."
- **First-order uncertainty is a wall** — **this is the accurate reading.** The
  graded difference the P4 harness predicted is smaller than the across-seed
  uncertainty this design can resolve, and the only above-noise signal is a rare
  binary collapse, not a graded effect. The headline (no demonstrated advantage,
  plus seed-dependent candidate failures) is the correct summary; "equivalence"
  overstates the evidence.

---

## Audit scope: what `audit_ac113.py` actually verifies

`audit_ac113.py` reproduces the frozen decision rule faithfully — it re-derives
the **individual-level** paired differences from `rows.jsonl` and applies the same
`mean < 0 AND p > 0.05 ⇒ F1` mapping. Its PASS means the following are verified
against the saved table, without simulation:

- source hashes match the pre-run snapshot (declaration + simulation code; the
  verification tools are correctly excluded from the hash set);
- row coverage is complete (cohort + sweep + causal rows);
- arm/condition invariants hold (no_cause ⇒ 0 relinquishments; move ⇒ ≥1);
- V2 (causal role) contrast is present;
- the F1 verdict is recomputed from `rows.jsonl` rather than trusted from
  `results.json`.

The audit does **not** verify — and cannot validate — the scientific
interpretation of its own decision rule. Specifically it does not check (a) the
unit/dependence structure (it pools 16 individuals of which 8 are byte-identical
duplicates), (b) whether nonsignificance justifies an equivalence claim, or (c)
any equivalence margin or power. **Reproducing a flawed decision rule does not
validate its interpretation.** The audit is correct as an integrity check of the
frozen artifacts; the F1 label it re-derives is the claim this note corrects.
