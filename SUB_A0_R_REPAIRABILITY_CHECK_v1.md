# SUB-A0 analytic check: can the repair circuit's own weights (R) be repaired in the calibrated regime?

2026-10-05. **Analytic card**, solver-free. It was required by option A before any
re-test freeze ([results v1](SUB_A0_CAL_RESULTS_v1.md)). No simulation, and no
candidate evaluated.

## Setting

- The stage-1 regime is the A0 law with λ = (2, 1, 1) and H = 2048.
- Every learned scalar is stored as three replicas in randomly placed physical
  regions.
- Each tick, replica i is multiplied by `1 − k·μ_i(t)`, where k = 0.0004 and
  μ_i(t) ∈ {1, 4, 16} is a **hidden** regional mode. Independent drift is then added.
- Writes are bounded by |Δ| ≤ 0.05 and at most 256 per tick, across 894
  destinations.

## A. Lost magnitude cannot be recovered from live state (exact, drift-free case)

Take a coefficient with original value r and no drift. Its live replicas are
`(r·s_1, r·s_2, r·s_3)`, where `s_i = Π_t (1 − k μ_i(t)) ∈ (0, 1]` depend on
hidden modes. Compare with a second individual whose original value was r' = c·r,
for any c > 0, seen at a time where its shrink products are `s_i' = s_i / c` (an
admissible history whenever s_i/c ≤ 1). Both individuals present the same live
triplet.

Any repair map that is a deterministic function of live state, including a learned
updater reading its own damaged traces, therefore produces the same output for
both. It cannot restore both r and c·r. **The magnitude of a real-valued
coefficient is not identifiable from live state.**

Its **sign** is identifiable whenever a majority of replicas keeps it. Drift only
adds noise, so it does not change this conclusion.

This is the SUB_A analytic-check (E) argument applied to scale rather than to
erased content.

It explains the stage-1 result. EXT_BISTABLE recovered 100% of the gap only
because T is a bit table with **one shared magnitude m** (a content-blind prior).
EXT_MEDIAN, which has no magnitude prior, recovered 33%.

## B. Which R magnitude can be maintained: one set by physics, not by content

- Suppose a sign-preserving push outward writes a destination with average
  frequency f ≤ 1 per tick, each write moving it by 0.05.
- Mean-field balance gives the fixed point `|v*| = 0.05 f / (k μ)`.
- If the budget is spread evenly (f = 256/894 ≈ 0.286), this gives
  |v*| ≈ 35.8, 8.9 and 2.2 for μ = 1, 4 and 16.

So an R coefficient can be held at a nonzero magnitude **set by its region's
hidden mode**, which varies up to **16×** between regions and switches over time.
It cannot be held at its developed value.

## C. Consequence for the A0 candidate

The candidate's 42 performing coefficients are real-valued weights of a 4-unit
tanh recurrent updater:

- **Score head:** the ranking used for top-B selection is invariant to a common
  positive scale on its weight and bias, so it tolerates uniform shrinkage.
- **Delta head and hidden layer:** neither is scale-invariant. `0.05·tanh(c·x)`
  shrinks with c, so repair slows as R decays. The input and recurrent weights set
  tanh operating points.
- **Independent per-replica, per-region scale factors** distort the
  mean-of-3 effective coefficients nonuniformly.

**Therefore:** in this regime the repair circuit can persist only if development
finds an R code whose function depends on signs, or is tolerant of about 16×
per-coefficient scale heterogeneity. The 16-step A0 development objective neither
requires nor encourages such a code. A candidate that has not found one will lose
repair capacity at a rate set by shrinkage, **whatever its allocation**. That
would show up as a row-1 or row-2 NEGATIVE
([re-test table](SUB_A0_RETEST_PROPOSAL_v1.md)), caused by the substrate rather
than by the dependence hypothesis.

## Scope and what would change it

- **Coverage.** A is exact for the drift-free common-mode case. B is a mean-field
  estimate. C is a structural argument about the A0 graph, not a proof that no
  development process could find a scale-tolerant code. Whether one does is Q-LEARN
  and can only be settled empirically.
- **Not covered:** drift-only regimes. Those make magnitude a random walk rather
  than a decay, but A's non-identifiability still applies.
- **Result: a QUALIFIED PASS for running a re-test, not a block.** The re-test is
  admissible only if it states in advance that a competence or maintenance-use
  NEGATIVE is the predicted outcome unless R self-organizes into a sign/scale-robust
  code. It must also add one descriptive diagnostic: the fraction of R function
  retained under a pure common-mode rescale of R, measured on engineering seeds
  only. If the human wants a test of allocation priority that is not dominated by
  this substrate fact, the alternative is a **substrate revision**: a sign-coded
  or bistable R parameterization declared as physics before results. That is a new
  substrate proposal and needs approval.
