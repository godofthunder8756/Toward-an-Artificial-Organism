# P4 — the smallest cognition continuation after the P2 equivalence: heterogeneous likelihood ratios

2026-09-24. P4's deliverable (task `t_260b4671`): select ONE discriminating cognition
question — the smallest scientifically justified continuation given P2's equivalence — and
deliver the six pre-implementation items. This is a **design document**, not a study: no
organism-scale run, no seeds, no freeze. It is accompanied by a decision-theoretic
demonstration (`_p4_heterogeneous_lr.py`, run; output reproduced in §7) in the C2/C4/P2
lineage (identifiability and the predicted benefit are demonstrated at the harness level
*before* any organism-scale question, exactly as C2 and C4 did). No frozen artifact is
edited, re-run, or re-hashed.

---

## 1. The question, and the one hypothesis selected

P2 (`C4_P2_EQUIVALENCE_v1.md`) established that under C4's **stationary** two-cause model
the graded posterior is computationally equivalent to an integer ambiguous-failure counter
with matched decisive handling (`N = ceil(logit θ / log(4/3))`). The equivalence rests on
exactly one premise: **every ambiguous (occluded-unproductive) observation carries the same
log-likelihood ratio** `LR = log(4/3)`. With a constant LR, the float log-odds is a scaled,
translated copy of the count, and the load-bearing objects are (i) decisive-observation
handling and (ii) a counter threshold — not the graded register.

The smallest continuation is therefore the one change that breaks that premise. Of the four
candidate designs the card names, exactly one does:

| design | does it break P2's premise? | verdict |
|---|---|---|
| 1. reuse one estimate for multiple decisions (different costs) | **no** — two decisions with different thresholds read the *same* counter at two thresholds; the sufficient statistic is unchanged | not the continuation |
| 2. integrate observations with genuinely different likelihood ratios | **yes** — heterogeneous LR makes the log-odds a *weighted sum of distinct counts*, which a single counter cannot express | **selected** |
| 3. retain informative history through non-informative periods | already done — that is the C2 occluded-gate world (C2 design, C3/AC110) | not new |
| 4. use uncertainty to decide whether info is worth its cost (VOI) | **no** — under i.i.d. observations + fixed cost the optimal policy is an SPRT = a threshold = a counter (Wald); VOI collapses to a counter under homogeneous LR | not minimal |

**Selected hypothesis (design 2).** In the heterogeneous-likelihood-ratio world, the
sufficient statistic for the cause is a **two-dimensional weighted count** `(n_u, n_p)` — the
counts of the two weak observation types, consumed as the weighted sum `n_u·w_u + n_p·w_p` with
`w_u ≠ −w_p`. The minimal state that realizes it is **two integer counters with the two
likelihood weights supplied**; a single integer counter cannot express the non-integer optimal
weighting ratio, and a real-valued graded register is a *lossy re-encoding* of the same integer
pair that gains nothing. So the load-bearing object is **heterogeneous weighting**, not
gradedness — this is the P2 finding extended: gradedness is still not required, but (unlike the
homogeneous case) a single counter is now insufficient.

---

## 2. The minimal change: relax "M never yields" to a residual yield ε

The frozen C4/C2 model has two causes and **one** weak observation (occluded-unproductive,
`LR = log(4/3)`) because the productive observation is *decisive* (M never yields). The one
change that makes the LR heterogeneous is to relax that sharpening:

- **M (move).** The held entry is stale and the channel-1 mapping has flipped; a contact is
  unproductive with probability `1 − ε` and **yields with residual probability ε** (the old
  port retains residual activity). `ε ∈ (0, 1/4)` is a new declared world constant, the
  direct analogue of `P_YIELD = 1/4` for the cut.
- **C (cut).** Unchanged: blind fallback yields with `P_YIELD = 1/4`.
- **Gate.** Unchanged: `used_held` occluded on an i.i.d. Bernoulli(`q`) fraction of contacts,
  not synchronized with the cause onset.

The new likelihood structure (only the two *weak* observations change; the decisive ones are
unchanged):

| observation | possible under | log-LR toward M |
|---|---|---|
| open `held` (any) | M only | `+∞` (decisive M) |
| open `blind` (any) | C only | `−∞` (decisive C) |
| occluded, productive | both | `w_p = log(4ε)` (weak C, since ε < 1/4) |
| occluded, unproductive | both | `w_u = log((4/3)(1−ε))` (weak M) |

For `ε ∈ (0, 1/4)` the two weak weights are **genuinely different magnitudes and opposite
signs**, with ratio `w_p/w_u = log(4ε)/log((4/3)(1−ε))` ranging from `−9.44` (ε=0.02) to
`−3.46` (ε=0.2) — always non-integer. This is the minimal heterogeneity: two distinct weak
LRs, one new world constant, no conservation law touched (the residual yield is a property
of the observation process, exactly as `P_YIELD` already is for the cut).

Boundary controls (recorded, not hidden): `ε → 0` recovers P2's homogeneous world exactly
(`w_p → −∞` so productive is decisive-C again, `w_u → log(4/3)`); `ε → 1/4` makes both weak
signals uninformative (`w_u, w_p → 0`), leaving only the open decisive contacts.

---

## 3. The sufficient statistic and the strongest simple implementation

In the hold-and-observe regime (withhold relinquishment, keep contacting), the observations
are i.i.d. given the cause, and the open contacts are decisive, so the sufficient statistic
for the cause is the pair of counts

    (n_u, n_p) = (# occluded-unproductive, # occluded-productive)

consumed as the weighted log-odds `L = n_u·w_u + n_p·w_p`. The optimal decision is a linear
threshold on this pair (`relinquish when L ≥ logit θ`). Because `w_u/w_p` is irrational, the
threshold never coincides with an integer-weighted boundary, so the decision function is
*fully determined* by the pair and the two supplied weights.

Three realizations, one sufficient statistic:

1. **Graded register (candidate):** a real log-odds accumulator, `L += w_u` / `L += w_p` per
   contact. This is C4's object, now in the heterogeneous world.
2. **Two-counter finite-state (strongest simple implementation):** store the two integers
   `(n_u, n_p)`, decide by `n_u·w_u + n_p·w_p ≥ logit θ` each tick, weights supplied.
3. **Single-counter (the P2 rival, generalized):** one integer `n`, `n += 1` on unproductive,
   `n += w` (integer) on productive, relinquish when `n ≥ N`.

The probe's §2 result (reproduced in §7) is that (1) and (2) are **the same decision function**
— exact equality over the full 6-symbol observation alphabet for horizons up to 6 (46,656
histories × 10 thresholds, zero mismatches). The graded register is a re-encoding of the
integer pair; gradedness carries no information the two counters lack. This is the P2 finding
carried into the heterogeneous regime: **the load-bearing object is the two-dimensional
weighting, not the float register.**

---

## 4. The six pre-implementation items (the card's required deliverable)

### (1) Identifiability from permitted observations/actions — DEMONSTRATED

The cause is identifiable from the organism's own `(used_held, productive)` history, not from
any single observation. Under M the expected log-LR drift per occluded contact is
`(1−ε)·w_u + ε·w_p > 0`; under C it is `(3/4)·w_u + (1/4)·w_p < 0` — opposite signs, so the
weighted history separates the causes (and the open `held`/`blind` contacts are decisive with
probability `1−q` each). Measured (§7, table 1): drift `+0.212 / −0.431` at ε=0.02 and
`+0.048 / −0.058` at ε=0.125. No hidden cause label, no schedule access, no privileged read —
the gate withholds one observation bit and is applied uniformly to every arm (C2's three
anti-confound properties, unchanged).

### (2) Sufficient statistic and strongest simple implementation — IDENTIFIED

The sufficient statistic is the integer pair `(n_u, n_p)`; the strongest simple implementation
is the **two-counter finite-state rival with the two likelihood weights supplied** (the graded
register is equivalent to it and is a lossy float re-encoding, §3).

### (3) What requires memory vs what is computable from the current observation

- **Requires memory (the stored, maintained state):** the running pair of counts `(n_u, n_p)`.
  It is a function of the *history*, not of any single observation — the "internally stored
  and resource-maintained estimate" the card asks about.
- **Computable from the current observation:** which weight applies (`w_u`, `w_p`, or the
  decisive `+∞/−∞` branch). The current contact tells the organism *how* to update; it does
  not tell it *where the accumulated evidence stands*.
- **Supplied, neither stored nor computed per-episode:** the weights `w_u, w_p` and the
  threshold `θ` are frozen world constants.

### (4) Supplied vs learned — DECLARED (nothing is learned)

The likelihood weights `w_u, w_p` (equivalently the model `{ε, P_YIELD}`), the prior `L_0 = 0`,
and the decision threshold `θ` are **supplied** frozen constants — exactly as `P_YIELD = 1/4`
was supplied in C4. This keeps the design at the **first-order content** tier. The
**learned** version — estimate `ε` (or `P_YIELD`) when it varies across distinguishable
conditions, i.e. a state about the evidence channel's *own diagnostic value* — is the
**reliability tier** (C4 §11), explicitly deferred and named as the next-after (§9), not
built here.

### (5) Predicted benefit and the falsification outcome — DEFINED, regime-conditional

**Predicted benefit.** In the informative-heterogeneous regime (`ε ≤ 0.125`, `q ≥ 0.7`), the
weighted accumulator (equivalently the two-counter rival) strictly beats the strongest
single-counter rival on expected regret, because the single counter's *integer* productive
weight cannot match the *non-integer* optimal weighting ratio `w_p/w_u`. Measured: min-mean
regret gap `+0.098 … +0.320` at ε=0.02 (largest at q=0.9), `+0.039 … +0.164` at ε=0.08,
monotone in both the heterogeneity (`1/ε`) and the incompleteness (`q`).

**Falsification outcomes (both meaningful, both measurable):**
- **F1** — if the single counter *matches* the weighted policy in the informative regime,
  heterogeneous weighting is **not** load-bearing and a maintained integer counter suffices
  (the P2 conclusion survives the heterogeneous LR). *Not realized:* the weighted policy wins
  by up to `+0.32`.
- **F2** — if the graded register beats the two-counter rival, real-valued gradedness **is**
  load-bearing (a positive result *against* P2's spirit). *Not realized:* exact equality (§3).

The design is discriminating: it cleanly separates "heterogeneous weighting is load-bearing"
(F1 fails) from "gradedness is load-bearing" (F2 fails), and the measured outcome is F1
fails / F2 fails — heterogeneous weighting load-bearing, gradedness not.

**Named boundary (a property of the problem, not a falsification).** As `ε → 1/4` the two
weak signals become uninformative and the advantage vanishes then *reverses* (at ε=0.2, q=0.9
the single counter wins `−0.20`): with near-zero evidence the cost asymmetry (`R = 4 ≪ H = 96`)
makes immediate action optimal, so the fast single counter is the better policy and no
uncertainty estimate is needed. This is C4's `q → 0` boundary control extended to a second
dimension (`ε`), and it is *why* the prediction must be stated as regime-conditional rather
than universal.

### (6) Named consciousness-related mechanism — HOT-2, without claiming subjective experience

The organism's route-memory entry is the first-order representation; the weighted cause
estimate is the **second-order state about why that representation is failing** — E_world
(obsolete → noise) vs E_machinery (still valid, access degraded). Distinguishing those two
from the organism's own observations, and *weighting heterogeneous evidence by its likelihood
ratio* before acting, is the function of **HOT-2 — metacognitive monitoring** (Butlin et al.
2023, Table 1: "metacognitive monitoring distinguishing reliable representations from noise"),
the roadmap's chosen mechanism (`CONSCIOUSNESS_ROADMAP_v1.md` §4–5). The strongest wording this
design's result could earn is **"meets candidate indicator HOT-2 at degree Y"** — never
"metacognitive" and never "conscious" (the level-(d)/(e) boundary is untouched). The mapping
carries the same flagged adaptation as C4 (HOT-2's canonical domain is perceptual; here the
content is interoceptive/route-level — a modeling judgment, not a settled finding). The graded
*reliability* tier (estimate the weights when they vary) is the specific HOT-2 reliability
function and remains the deferred target, not this design.

---

## 5. Rivals (same information set, never a strawman)

All three read the same `(used_held, productive)` stream and handle the two decisive
observations identically (open `held` → act now; open `blind` → hold forever). They differ
only in how they accumulate the two weak occluded observations:

1. **`graded`** — the real log-odds accumulator (`θ` grid, includes `θ = 0.5` so it can also
   act fast; matched tuning, never a weaker set).
2. **`two_counter`** — the finite-state `(n_u, n_p)` rival with the two weights supplied.
3. **`single_counter`** — one integer `n`; `n += 1` on unproductive, `n += w` (integer,
   clamped ≥ 0) on productive, relinquish at `n ≥ N`. Swept over `w ∈ {−6 … 0}` and
   `N ∈ {1 … 16}`, so it is the *strongest* single-integer rival, not a strawman.

The comparison is functional capability vs organizational cost, as the card requires: the
single counter is the cheapest (one integer + one threshold), the two-counter is two integers
+ two supplied weights, the graded register is a real register + two supplied weights. The
two-counter strictly dominates the graded register on cost with *equal* capability; both
dominate the single counter on capability in the informative regime (at higher cost).

---

## 6. Cost model (unchanged from C4/P2, faithful to the AC107 economics)

Hold under M: `+1` per contact (sustained lost income); relinquish under M: `0`; hold under C:
`0`; relinquish under C: `+R` with `R = 4` (one-time re-bind). Horizon `H = 96` (the cut
window); never acting under M costs `H`. Expected regret = mean over Monte Carlo episodes,
separately per cause; "min-mean" = `(regret_M + regret_C)/2` at each policy's own best
parameter (in-sample, a design diagnostic, not a generalization estimate — same as C4/P2).

---

## 7. The demonstration (run, reproduced from `_p4_heterogeneous_lr.py`)

Decision-theoretic only. No organism-scale run.

**Table 1 — identifiability (expected log-LR drift per occluded contact).**

| ε | w_u | w_p | ratio w_p/w_u | E[drift \| M] | E[drift \| C] |
|---|---|---|---|---|---|
| 0.02 | +0.268 | −2.526 | −9.44 | +0.212 | −0.431 |
| 0.08 | +0.204 | −1.139 | −5.58 | +0.097 | −0.132 |
| 0.125 | +0.154 | −0.693 | −4.50 | +0.048 | −0.058 |
| 0.20 | +0.064 | −0.223 | −3.46 | +0.007 | −0.007 |

**Equivalence (sufficient statistic).** Graded log-odds == two-counter finite-state, exact
over the full 6-symbol alphabet for horizons 1–6 (46,656 histories × 10 thresholds at H=6,
zero mismatches). `w_u/w_p = −0.222…` irrational ⇒ no `(n_u, n_p)` makes the weighted sum
equal `logit θ` for a rational grid θ ⇒ the decision is a pure linear threshold on the pair.

**Predicted benefit (min-mean regret, n_ep = 20,000; gap = single − weighted).**

| ε | q | single (w,N) | weighted (θ) | gap |
|---|---|---|---|---|
| 0.02 | 0.5 | 0.494 (−3,5) | 0.487 (0.7) | +0.008 |
| 0.02 | 0.7 | 1.016 (−6,4) | 0.918 (0.66) | +0.098 |
| 0.02 | 0.9 | 1.755 (−6,1) | 1.435 (0.5) | **+0.320** |
| 0.08 | 0.7 | 1.057 (−6,4) | 1.018 (0.6) | +0.039 |
| 0.08 | 0.9 | 1.781 (−6,1) | 1.617 (0.5) | +0.164 |
| 0.125 | 0.7 | 1.113 (−6,4) | 1.076 (0.6) | +0.037 |
| 0.125 | 0.9 | 1.799 (−6,1) | 1.769 (0.5) | +0.030 |
| 0.20 | 0.7 | 1.162 (−1,6) | 1.156 (0.55) | +0.006 |
| 0.20 | 0.9 | 1.848 (−6,1) | 2.047 (0.5) | **−0.199** |

The gap is positive (weighted wins) throughout the informative regime and flips only at the
uninformative boundary (ε=0.2, q=0.9).

**Boundary.** At q=0.7 the gap falls from `+0.115` (ε=0.001) through `+0.101` (ε=0.02),
`+0.037` (ε=0.125), `+0.006` (ε=0.2) to `−0.0003` (ε=0.24) — recovering P2's homogeneous
world at `ε → 0` and the no-information world at `ε → 1/4`.

**Pareto frontier (ε=0.08, q=0.7), the C4-rule-4 comparison.** The weighted frontier lies
below the single-counter frontier across the accurate region (e.g. at regret_M≈1.4 weighted
pays C≈0.6 vs the single counter's C≈0.85–1.03); the single counter reaches the *fast* end
(regret_M down to 0.06, C=2.54) that the weighted cannot (its fastest is regret_M=0.17,
C=2.12). The single counter trades accuracy for speed; the weighted accumulator dominates on
accuracy at matched speed, which is exactly the trade the two-dimensional weighting is for.

---

## 8. Claim discipline

- This is a **design + decision-theoretic demonstration**, not a study. No organism-scale run,
  seeds, freeze, or hashes. The probe's claims are about the observation process and the
  decision problem, not about any organism's behaviour.
- The headline is: **"under heterogeneous likelihood ratios, the sufficient statistic is a
  two-dimensional weighted count — realized by two integer counters with supplied weights —
  which strictly beats the strongest single-counter rival in the informative regime, while a
  graded register gains nothing over it. Heterogeneous weighting is load-bearing; gradedness
  is not."** It is *not* "the organism maintains a graded posterior", *not* "gradedness is
  load-bearing", *not* "metacognition".
- The prediction is **regime-conditional** and the two boundaries (`ε → 0` homogeneous, `ε →
  1/4` uninformative) are stated as the correct non-vacuous controls, not weaknesses — the
  mirror of C4's `q → 0` boundary.
- The weights, prior, and threshold are **supplied**, and the design says so; the learned
  (reliability) tier is deferred, not conflated in.

---

## 9. What this hands to P5 (and the named next-after)

**P5 receives one frozen design** — the heterogeneous-LR task with the six items delivered —
and an implementing-study question: at the organism scale, does a maintained **two-counter**
estimate (counts in vulnerable paid-maintained state, weights supplied, the AC12/AC96
free-bit pattern extended to two low-bit-width counters) beat a maintained single-counter
rival in the informative-heterogeneous regime (`ε ≈ 0.02–0.125`, `q = 0.7–0.9`), gated on
decision utility **and not survival**? The equivalence result (graded ≡ two-counter) means the
organism-scale question is *not* "graded vs counter" — it is "two-dimensional weighting vs a
one-dimensional counter", and the graded register is expected to be re-encoded as the integer
pair, not as floats.

**Named next-after (deferred, not built):** the **reliability tier** — make the evidence
channel's diagnostic value (`ε`, or `P_YIELD`) **vary across distinguishable conditions** and
ask whether an *estimated* weight (a genuinely graded, second-order state) restores the
discriminating weighting that a *supplied* weight gives here. That is the one remaining place
a graded magnitude could become load-bearing, and it is the roadmap's reliability target
(C4 §11, K8's narrowed reopening condition). It is gated on this design's organism-scale
result and is not this design.

---

## Files

- design: `P4_COGNITION_CONTINUATION_v1.md` (this file)
- diagnostic: `_p4_heterogeneous_lr.py` — observation process, three policies, identifiability,
  exhaustive equivalence, min-mean regret sweep, boundary, calibration, Pareto frontier.
  Run: `.venv/bin/python -B _p4_heterogeneous_lr.py`. Output: `_p4_heterogeneous_lr.out.txt`.
- No frozen artifact, runner, protocol, or hash was edited, re-run, or re-hashed.
