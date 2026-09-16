# AC50 PROTOCOL v1 — registered before the first final seed

**Endorsement.** This protocol was written and its source list hashed **before** any final seed was run.
The result directory is created with `mkdir(exist_ok=False)`, so a frozen directory can never be
overwritten. A self-declared defect elsewhere causes a hash mismatch; none is declared here.

## 1. The claim, in the form its own shape permits

*In a self-funded world with regime-dependent heterogeneous site values, after the stress regime
reverses, an organism that releases its stored order and re-acquires retains more production value over a
run than one that keeps its stale order — and it does so at a stable, steady-state equilibrium, not
during a collapse.*

The endpoint is **cumulative value-weighted production under regime B** — horizon-robust, like AC43's
ledger totals, not a terminal site count.

**Why the claim is shaped this way.** AC47/AC48 showed that under *homogeneous* sites the self-funded
world cannot be both stable and graded: the order's only lever (which site to renew) moves the outcome
only under scarcity, and scarcity in self-funding is the death regime. AC49 found the fix: make sites
heterogeneous in value, with value **regime-dependent** (region 0 most valuable under A, region 5 under B,
reversing with the stress). The order's renewal priority then decides *which* sites survive, and that
becomes a persistent production difference at a stable equilibrium. The two properties AC47/AC48 proved
impossible for homogeneous sites — stability (no death spiral) and horizon-robustness (steady state) — are
the gates that make this claim what it is.

## 2. Design

| item | declared value |
| --- | --- |
| world | self-funded, value-weighted production; `VALUES_A = (5,4,3,2,1,0.5)`, `VALUES_B = reversed` |
| stress | regime A rates ×3, regime B = reversed; burst probability 0.03 |
| economy | production period 4, drain 2.0, renewal energy 5 |
| capable arm | `learner_both` (releases the stored order, re-acquires under B) |
| cut arm | `no_release` (keeps the A-acquired order under B) |
| state-blind controls | `no_search`, `preserve` (random order) |
| oracle controls | `oracle_b` (declared B value-optimum), `oracle_a` (declared A value-optimum) |
| optima | `OPT_A = (2,0,1,3,4,5)`, `OPT_B = (3,2,4,5,1,0)` (24-start climb on the 12 scoring seeds, `ac50_heterogeneous.py`) |
| endpoint | cumulative value-weighted production at 600 ticks under B |
| individuals | **seeds 4800–4811 = 12** |
| freshness | engineering used seeds 4600–4611 and 9000–9011; these are disjoint |
| **effect-size bar** | **median paired difference ≥ 500 value-units** — engineering median 1012 |
| runner | `ac50_heterogeneous.py` (`main`), result directory `ac50_results_v1/` |

## 3. Declared gates — all nine must pass

| gate | criterion | declared from |
| --- | --- | --- |
| **G1 resolvable** | sign-flip test on the 12 paired differences, **p ≤ 0.01**, n ≥ 8 | engineering p = 0.00098 |
| **G2 effect size in value-units** | **median paired difference ≥ 500** | engineering median 1012 |
| **G3 stability, no death spiral** | **zero dead scoring runs** across all arms × individuals | AC47/AC48's delimiter; engineering 0/12 |
| **G4 horizon-robust steady state** | production@1500 / production@600 ∈ **[2.4, 2.6]** (linear = 2.50) | engineering 2.49 — a steady state, not a collapse transient |
| **G5 oracle_b ceiling** | min(`oracle_b`) ≥ min(`learner_both`) | the declared B-optimum brackets the top |
| **G6 state-blind below learner** | mean(`no_search`) < mean(`learner_both`) and mean(`preserve`) < mean(`learner_both`) | a random order must not reach the learner's value |
| **G7 completeness** | all 12 declared individuals present, no substitution | — |
| **G8 determinism** | re-running two individuals reproduces them exactly | — |
| **G9 register in the loop** | every held order a 6-tuple through the register | the re-acquisition goes through the register, not a hidden copy |

**This gate set is frozen.** No threshold may be moved after results are seen. If a gate fails, the study
is recorded as failed and a successor protocol is written; the existing result directory is never re-run.

## 4. The AC40 four-check, run before this protocol

Applied to the paired differences at engineering seeds, before this protocol was written:

| check | result |
| --- | --- |
| resolvability | p = 0.00098, n = 12 — resolved |
| effect size | median +1012 value-units, in the endpoint's own units |
| stability | 0/12 dead — no death spiral (the AC47/AC48 property) |
| horizon-robustness | production ratio 2.49 (600→1500) — steady state, not a transient |

## 5. Predictions registered in advance

1. The 12 paired differences resolve at p ≤ 0.01 (engineering 0.00098).
2. Median paired difference ≥ 500 value-units (engineering 1012).
3. **Zero** dead scoring runs — stability holds on fresh seeds, not just engineering.
4. Production is linear in time (steady-state ratio ≈ 2.50) — horizon-robust.
5. `oracle_b` ≥ learner (ceiling); state-blind means below the learner.

## 6. What is excluded from the claim, in advance

- Not an experience, an understanding, or a life; the endpoint is value-weighted production.
- Not autopoiesis or closure. "Self-funded" means the organism's own sites fund its energy; nothing is
  claimed about self-production in any stronger sense.
- Not survival: the endpoint is cumulative production, not alive/dead (AC34's rejected endpoint).
- The effect size is **modest by design** (~11%: the order can only differentiate the ~10% of sites that
  die at a stable equilibrium, and AC49 showed the value spread saturates). This is a claim about the
  *existence* of a stable graded self-funded regime, not about a large effect.
- Comparisons to anything outside this line are not offered.

## 7. Verification to be performed after the finals

- `audit_ac50.py`: recompute every gate from `rows.jsonl`, independently of the runner.
- `replay_ac50.py`: reproduce two individuals in a fresh process.
- `test_ac50.py`: assert the recorded gate values, the frozen shas, and that the protocol's declared
  source list equals the hashed set (`preflight`).

SOURCES (declared): ac50_heterogeneous.py ac33_search.py ac30_acquire.py ac29_register.py ac38_variance.py AC50_PROTOCOL_v1.md
