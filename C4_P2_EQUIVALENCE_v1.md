# C4 P2 — the sufficient-statistic rival is resolved: the graded posterior IS an integer counter

2026-09-24. P2's deliverable (`t_dac7256e`): resolve the stated equivalence concern, then
deliver one of (a) equivalence, (b) a named assumption that breaks it, or (c) an
implementation/reporting defect behind the prior result.

**Outcome: (a) — equivalent policies — with the specific defect (c) identified as the sole
source of the C4 dominance.** The graded posterior is computationally equivalent to an integer
ambiguous-failure counter with matched decisive-observation handling. The reported dominance of
`graded` over `binary+imm` is entirely attributable to a rival defect — `binary+imm` throws away
the occluded-productive-is-decisive-C observation — not to gradedness or likelihood-ratio
weighting. Fixing that one observation makes `binary+imm` bit-for-bit the integer counter, hence
bit-for-bit the graded policy, and the dominance vanishes.

This is a finding, not a failure. It changes the P4 question (see §6).

---

## 1. The question, stated exactly

Under C4's stationary two-cause model (`C4_REPRODUCIBILITY_v1.md` §2), every ambiguous
(occluded-unproductive) contact contributes the same log-likelihood increment `L_n = L_0 +
n·log(4/3)`, so a fixed posterior threshold `logit(θ)` is an integer ambiguous-failure threshold
`n >= ceil((logit(θ) − L_0) / log(4/3))`. Is the graded posterior therefore just an integer
counter in float clothing?

The model (unchanged from P1):

| observation | possible under | log-LR toward M | decision |
|---|---|---|---|
| open `held` | M only | +∞ (decisive M) | relinquish now |
| open `blind` | C only | −∞ (decisive C) | hold forever |
| occluded, productive | C only (M never yields) | −∞ (decisive C) | hold forever |
| occluded, unproductive | both | `log(4/3) ≈ 0.288` (weak M) | accumulate |

Graded prior `L_0 = 0`; loss: hold under M = +1/contact, relinquish under C = +R (R=4), the other
two = 0; horizon H=96; cause fixed for the episode.

## 2. The rival

`regret_int(obs, cause, N)` — the integer ambiguous-failure counter with the **same** decisive
handling, prior, action timing, and stopping rule as `regret_graded`:

- open `held` → relinquish immediately (decisive M);
- open `blind` **or** `productive` → hold forever (decisive C);
- otherwise (occluded-unproductive) → increment the counter `n`; relinquish when `n >= N`.

The alignment is `N = ceil(logit(θ) / log(4/3))`, with `logit(θ) = log(θ/(1−θ))`. The prior
`L_0 = 0` is `n = 0`; the stopping rule (act at the first crossing tick, else hold through H) is
identical.

## 3. Analytic equivalence

In the finite branch the graded accumulator takes exactly the values `0, LR, 2·LR, …, n·LR`
(after `n` occluded-unproductive contacts), and the decision is `L >= logit(θ)`. Because
`LR = log(4/3)` is irrational and every grid `θ` is rational, `logit(θ)/LR` is never an integer
(the one exception, `θ=0.5` → `logit=0`, is an exact multiple of `LR` and is aligned by the `>=`
convention — see §4), so the threshold `logit(θ)` sits strictly between `k·LR` and `(k+1)·LR` for
`k = floor(logit(θ)/LR)`. Therefore `L >= logit(θ)` ⟺ `n >= k+1 = ceil(logit(θ)/LR)`. The three
decisive branches (`+∞`, `−∞`, `−∞`) are matched term-for-term. The two policies make the same
decision on every admissible history.

The C4 design's §10 claim — "no uniform counter can express that split" — is false for this
construction: the "split" is decisive-observations-act-immediately vs
weak-observations-accumulate-slowly, and an integer counter expresses exactly that split once the
three decisive observations are handled the same way. The float log-odds carries **no information
that the integer counter lacks**: with a constant LR, the log-odds is a scaled, translated copy of
the count.

## 4. Executable verification

`_c4_p2_equivalence.py` (run, deterministic). Four checks:

1. **Threshold mapping** — `θ ∈ {0.5, 0.52, 0.55, 0.58, 0.6, 0.62, 0.66, 0.7, 0.75, 0.8, 0.85,
   0.9, 0.95}` maps to `N ∈ {0,1,1,2,2,2,3,3,4,5,7,8,11}` (nine distinct thresholds; the Pareto
   grid maps to `{0,1,2,3,4,5,7,8,11}`).
2. **Boundary check** — the nearest non-zero distance from `logit(θ)/LR` to an integer is `0.0296`
   (at `θ=0.85`), i.e. `≈ 8.5e-3` in log-odds, against a float accumulation error of `1.8e-14`
   after 96 adds: no `θ` sits within float noise of a boundary. `θ=0.5` is exactly on the
   boundary (`logit=0 == 0·LR`) and is aligned by the `>=` convention (confirmed by the exhaustive
   test, `graded(0.5) == int(0)` on every history).
3. **Exhaustive equality** — over the **full** 6-symbol observation alphabet `{held,blind,occluded}
   × {productive,unproductive}` for every horizon `H ∈ {1,…,7}` (279,936 histories at H=7) and
   over 200,000 random length-96 full-alphabet histories: `regret_graded(θ) == regret_int(N)` with
   `N = ceil(logit(θ)/LR)` returns the identical act-tick on **every** history, both causes. Exact,
   not within-MC-noise.
4. **Regret attribution** — min-mean regret (mean over M and C, each policy at its own best
   parameter), vectorized, n_ep=200,000, same episode stream per (cause, q):

   | q | binary+imm (as-is) | binary+imm (full) | int counter | graded |
   |---|---|---|---|---|
   | 0.5 | 0.487 @ N=5 | 0.477 @ N=4 | 0.477 @ N=4 | 0.477 @ θ=0.75 |
   | 0.7 | 0.994 @ N=4 | 0.881 @ N=3 | 0.881 @ N=3 | 0.881 @ θ=0.66 |
   | 0.9 | 1.743 @ N=1 | 1.351 @ N=1 | 1.351 @ N=1 | 1.351 @ θ=0.5 |

   `graded == int == binary+imm(full)` coincide **to 1e-12** at their optima (they are the same
   decision rule). The q=0.9 numbers reproduce P1's §9 re-run (`binary+imm` 1.740 → 1.743;
   `graded` 1.341 → 1.351; the small deltas are seed/grid/n_ep). The `binary+imm (as-is)` column
   is the only one that differs, and it is strictly worse at every q.

## 5. The one-observation defect behind the C4 dominance

`binary+imm` (frozen `regret_binary_immediate`) handles a productive contact with `n = 0` — a
streak **reset** — not with `e = 'C'` (decisive-C, hold forever). Under the stated model a
productive contact conclusively identifies C (M never yields), so this is an **omitted decisive
observation**: the rival throws away a conclusion the model makes available to every arm. It then
keeps counting occluded-unproductive contacts and can wrongly relinquish the valid entry.

Concrete counterexample (cause C, `obs = [occ·0, occ·1, occ·0, occ·0, occ·0, occ·0]`, i.e. one
productive contact then four unproductive):

```
graded(theta=0.75)  = 0.0   (sees the productive, holds forever — correct)
binary+imm(N=4)     = 4.0   (resets on the productive, then re-accumulates 4 and wrongly relinquishes)
```

At q=0.9 the gate is open only ~10% of the time, so this reset-defect fires often — exactly the
regime where §9 reported the largest "dominance" (1.743 vs 1.351). When `binary+imm` is upgraded
to `e = 'C'` on productive (`regret_binary_immediate_full`), it is identical to the integer
counter and to the graded policy on every admissible history (verified, §4). The dominance
vanishes **completely** — it was never about gradedness.

The tuning comparison is also fair, in the rival's favor: the graded grid maps to nine integer
thresholds `{0,1,2,3,4,5,7,8,11}`, all inside the integer counter's (and `binary+imm`'s) grid
`N ∈ {1,…,24}`. The integer counter has **more** tuning opportunities and still traces the same
frontier — the graded policy is a strict re-parameterization, not a strictly-dominant policy.

The one caveat, stated for completeness: `regret_binary_immediate_full` and `regret_int` differ
only on the **impossible** `(held, productive)` observation (the frozen binary's
`elif held: return` fires before the productive check, while graded/int treat any productive
contact as decisive C). Under the stated model `held ⇒ productive=0` always, so this corner is
unreachable and does not affect any admissible history. `regret_int` and `regret_graded` are equal
on the full alphabet including this corner.

## 6. What this changes for P4

The C4 support statement was: "a **graded** first-order posterior is calibrated and strictly
dominates ordinary uncertainty heuristics." The graded-vs-binary+imm half of that now resolves
into two cleaner facts:

1. **Calibration survives** — the graded posterior's confidence tracks error frequency (P1 §4.2,
   unchanged). That claim is not about dominance and is untouched by this finding.
2. **The "strict dominance over the strongest heuristic" was a rival defect, not a property of
   gradedness.** With matched decisive handling, the graded posterior and an integer counter are
   the **same policy**; the only thing `binary+imm` lacked was the occluded-productive
   conclusion.

The P4 question therefore shifts from "is a *graded* estimate needed?" to "does any estimate of
this kind need to be *graded*, or does a maintained **integer ambiguous-failure counter** (with the
three decisive observations) suffice?" — the first-order utility claim no longer licenses a graded
register as the load-bearing object; the load-bearing objects are (i) the decisive-observation
handling (act on held, hold forever on blind-or-productive) and (ii) a counter with threshold N.
Whether the *reliability* tier (an estimated `P_YIELD`, C4 §11) reintroduces a graded quantity is
untouched and remains deferred.

## 7. Claim discipline

This is a decision-theoretic analysis of the C4 model, not an organism result. It does not re-run
or re-hash any frozen study (AC107/108/110/111 or C4's probes are imported, not edited). The
equivalence is a **model** fact: under a stipulated correct constant likelihood `P_YIELD = 1/4`
supplying `LR = log(4/3)`, the posterior is a scaled counter. It says nothing new about organism-
level acquisition or maintenance of uncertainty; it *narrows* what the first-order claim can be
asked to buy.

## Files

- analysis + executable check: `_c4_p2_equivalence.py` (run:
  `.venv/bin/python -B _c4_p2_equivalence.py`)
- this record: `C4_P2_EQUIVALENCE_v1.md`
