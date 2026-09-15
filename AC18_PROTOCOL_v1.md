# AC18 protocol v1: separation of worst cases — the corrected gate, fresh seeds

Frozen before the first final seed. Final seeds **2500-2503** (disjoint from AC17's
2300-2303, AC16's 2100-2103, AC15's 1900-1903, the AC15 deviation's 1800-1803, AC13's
replication seeds 3-8, and every engineering seed 0-2). Runner: `ac18.py`, driving the frozen
`ac17.run` unchanged. Audit: `audit_ac18.py`. Replay: `replay_ac18.py`. Tests: `test_ac18.py`.

## What AC18 is, and what it is not

AC16 v1 and AC17 v1 were both falsified by gate **shape**, not by the mechanism: AC16 asked
for a mean margin over a rival that partially succeeds (+0.2437 vs +0.25 while the learner was
strictly better in 8/8 individuals); AC17 asked for strict per-individual dominance, which is
**unsatisfiable** when both arms can reach the ceiling (2 of 8 individuals tied at 1.000).
Neither failure was a fact about the organism.

AC18 is a **confirmatory replication** of the same mechanism on fresh seeds, with a gate
derived from the claim's logic rather than from convenience. The world, arms, horizon,
intervention, primitive and runner are **unchanged** from AC17 — `ac17.run` is imported, not
modified. What AC18 adds is the gate, declared here, plus a satisfiability check performed
before the run.

**This is not a third attempt at the same gate.** Both prior gates are recorded as permanent
falsifications and are not re-run with better-chosen numbers; their results documents stand.
AC18 tests a *differently stated* claim — the categorical one — on data it has never seen.

## Claim

In the graded world with the growth window open, after an unannounced post-development move of
the material channel, an organism whose per-slot maintenance decision is driven in both
directions by its own realized contact outcomes **holds a correct route for the moved channel
in the worst individual of the sample**, whereas one-way relinquishment **does not** — the
worst case, not the average, is where "a one-way rule cannot hold" lives.

Formally: the minimum over individuals of the learner's final-eighth moved-channel
productivity is >= 0.90, and the minimum over individuals for one-way `allocate` is < 0.90.

## Why a minimum, and why this is the claim's own shape

- "One-way relinquishment cannot hold a re-bound route" is a statement about the **worst
  case**: it says there exist individuals on which holding fails, and that the failure is not
  a matter of degree. Its correct test is therefore whether one-way's *minimum* clears the
  bar, not whether its mean is lower or whether it loses in every individual.
- The learner's claim is the complementary universal: it holds on **every** individual, so the
  test is the learner's minimum >= 0.90.
- A mean would let a lucky re-binding timing compensate for a failure to hold (AC16's
  misfit). Strict per-individual dominance additionally requires the rival to lose *everywhere*,
  which the mechanism does not predict and the ceiling makes impossible (AC17's misfit).

## Satisfiability check, performed before the run

The gate must be able to pass **and** able to fail.

- Can it fail? Yes: if one-way's minimum is >= 0.90, the separation does not hold and the claim
  is falsified. AC17's data show one-way reaching 1.000 on some individuals, so a sample where
  it holds everywhere is entirely possible. Nothing in the gate requires the learner to win on
  individuals where the rival also reaches the ceiling, so the gate is not unsatisfiable by
  construction.
- Can it pass with the mechanism failing? No: the learner must clear 0.90 on **every**
  individual, and the keeping arms must be exactly 0.000 (below), so a learner that merely
  dropped more often would fail G1 and G3.
- Bound: the score is a fraction in [0, 1]; the bar is 0.90, below the ceiling, so strict
  separation of minima is well posed.

## Endpoints

Primary: **the minimum over the 8 individuals of the moved-channel final-eighth productivity**,
for the learner and for one-way `allocate`, reported alongside the full per-individual lists.

Secondary: kept-channel productivity per individual; the re-binding tick; relinquishments and
restorations; final stored route versus the true mapping. Aggregate income is not an endpoint.

## Gates, prespecified

- **G1 (the claim, worst case):** min over individuals of the learner's moved-channel
  productivity >= 0.90.
- **G2 (the separation):** min over individuals for one-way `allocate` < 0.90. **G1 and G2
  together are the claim**; failing either falsifies it.
- **G3 (barred, categorical):** `preserve`, `no_learning`, `fixed_schedule` and `random` score
  exactly 0.000 on the moved channel and record no re-binding tick, in every individual.
- **G4 (no sacrifice, categorical):** the learner's kept-channel productivity >= 0.95 in every
  individual.
- **G5 (consistency, exact):** `fixed_period_1` and `streak_never` reproduce `preserve`, and
  `restore_disabled` reproduces one-way `allocate` — same `state_hash`, every individual.
- **G6 (Claim A, structural):** `restore_only` scores exactly 0.000 with no re-binding tick, in
  every individual.
- **G7 (rival competence):** no blind rival and no swept blind configuration reaches 0.90.
- **G8 (scope):** the learner, one-way, `preserve`, `no_learning`, `restore_only`, both
  consistency arms and `restore_disabled` complete the horizon in every individual. The crude
  `relinquish` extreme is excluded by declaration (it dies in 2 of 8 AC17 individuals, and it is
  not the claim's comparator); its survival is reported, not gated.

Failure of G1-G7 falsifies the claim, including failure on a single individual where the gate
is categorical. Thresholds may not be changed after the run.

## Sample and analysis

4 seeds x 2 histories = 8 individuals per arm, 11 arms, 88 rows. Seeds are the replication
unit; histories are repeated measures. Report every individual's value. The learner's
configuration stays prespecified at drop-threshold 6. The rivard sweep from AC17
(`sweep_ac17.py`) covers the rival families and is re-used for G7; it ran on engineering seeds
and its numbers are disclosed as such.

## Expectation, declared so a surprise is visible

Based on AC17's fresh sample the expectation is: learner minimum **1.000** (invariant across
individuals), one-way minimum in the **0.4-0.6** range (seed-dependent, 0.462-1.000 observed),
keeping arms exactly 0.000, no re-binding for any keeping arm or for `restore_only`. A learner
minimum below 0.90, or a one-way minimum above it, is a genuine falsification and not a
technicality.

## Known limitations, stated before running

- Same as AC17: the growth window's W-birth loop is not separated from the deposit path; the
  restore fires on a single productive contact (sound only because the frozen gate cannot be
  passed by a wrong port); Claim A's structural prediction depends on `mem.deposit` requiring
  `selected is None`.
- AC18 is a confirmation on fresh seeds of a mechanism already measured twice, not a new
  capability. The line's remaining open item (the need to allocate under a post-development
  intervention with no protected copy) is what this whole sequence addresses; AC18 closes it if
  G1 and G2 both pass.
