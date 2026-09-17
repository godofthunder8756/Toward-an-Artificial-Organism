# AC78 engineering v1: content self-production is blocked by the fixed-point signal — a structural obstacle, not a learner deficiency

2026-09-17. `ac78_engineering.py`, `ac78_engineering_addendum.py`,
`ac78_engineering_addendum2.py`, `ac78_engineering_addendum3.py`. **No protocol, no final
seeds, no claim.** This is the measurement AC72's reframe and AC77's conclusion pointed at: can
the organism produce its priority description from its **own accumulated activity signal**?

## The question, stated precisely

AC76 (frozen) established that the organism re-derives its 126-bit rules from an 8-bit priority
through its own paid, vulnerable machinery — but the priority is externally supplied. That is
turnover of an inherited description, not production of it. The one remaining structural gap for
full autopoiesis: can the organism **produce** the priority from its own activity?

The arena is the AC32/33 regime-B ranking world, where a priority (a six-position renewal order)
has a measurable production consequence (sites retained). This is the most favourable world to
ask the question in: it is the only place where the priority's value is graded (the AC76
4-bank priority is behaviourally near-inert — its 24 orders all survive the same way). If
self-production fails here, it fails everywhere the organism lives.

The prior measurements fixed the premise: AC73 (single-life noise sd 0.94 vs a ~0.25 fine gap —
a signal floor, not a search problem) and AC77 (the production signal is a **fixed point**,
N_eff ≈ 1 at every horizon; the fine plateau is below the fixed-point noise floor and largely
not a stationary fact; the ranking is real only at the **coarse** good-vs-bad scale). AC77's
reframe: gate on the coarse good-order plateau, not the fine/optimal order. This measurement
asks whether even that coarse gate is producible from the organism's **own single life**.

## Measurement 1 — the coarse ranking is real, but barely above the single-life floor

Stationary ranking of 32 orders × 30 seeds (8500–8529), and the paired single-life good-vs-bad
comparison on 100 seeds:

| quantity | value |
| --- | ---: |
| stationary good order `(0,1,2,3,4,5)` | 12.20 |
| stationary ceiling `(2,0,1,3,5,4)` | 12.17 (tied — AC77's graded plateau reproduced) |
| stationary min / median / max | 10.31 / 11.07 / 12.20 |
| coarse good-minus-bad gap (stationary) | **1.90 sites** |
| single-life noise (snapshot sd) | 0.96 (good), 1.55 (bad) |
| paired single-life good-minus-bad | +1.47, sd 1.81, se 0.33 |
| P(good beats bad on the same seed) | **0.70** |

The coarse structure is real but only ~2× the single-life noise, and a single life sorts good
from bad correctly only 70% of the time. That is already marginal — but it is not the decisive
obstacle. The decisive obstacle is that the organism cannot *use* that signal within one life.

## Measurement 2 — the within-life signal stops responding to the priority after the transient

`ac78_engineering_addendum.py`: run one order for 8000 ticks, then switch, 12 seeds. The live-site
count just before the switch, just after, and at end:

| switch | seeds where the count MOVED |
| --- | ---: |
| GOOD → BAD at t=8000 | **0 / 12** |
| GOOD → GOOD at t=8000 (control) | 0 / 12 |
| BAD → GOOD at t=8000 | **0 / 12** |
| BAD → GOOD at t=400 (early, during the transient) | 10 / 12 |

After ~8000 ticks the production signal is a **locked fixed point**: changing the priority
changes nothing observable, because the count is pinned at whatever integer survived the early
transient and renewal keeps every surviving site alive forever. The only window in which the
signal responds to the priority is the early transient — and that window is exactly where the
next measurement shows the signal is confounded.

## Measurement 3 — in the only responsive window, the signal is path-dependent at the same size as the ranking

`ac78_engineering_addendum2.py`: on the **same seed**, compare a good order run from birth vs the
same good order adopted at t=400 after a bad transient, 24 seeds:

| condition | mean final sites | sd |
| --- | ---: | ---: |
| GOOD from birth | 11.92 | 0.72 |
| GOOD adopted at t=400 after BAD | **10.08** | 0.97 |
| BAD from birth | 10.17 | 0.96 |

Paired difference (fresh GOOD minus adopted-late GOOD): **+1.83**, sd 1.05, P(fresh > late) = 0.96.
Adopting the good priority after a bad transient leaves ~1.83 sites on the table — and the
adopted-good organism ends statistically indistinguishable from a bad-from-birth organism
(P(adopted-good > bad-fresh) = 0.21). The priority's value is **confounded with the history it
inherits**, and the confound (1.83) is the **same size as the entire coarse good-vs-bad gap**
(1.90). A single organism cannot run the counterfactual ("what would this priority have produced
from birth?") that evaluation requires.

Robustness (`ac78_engineering_robustness.py`, 50 seeds, disjoint): confound +1.96 (sd 1.18,
P(fresh > late) = 0.94) against a coarse gap of +1.82 — the confound is, if anything, *larger*
than the gap. The history an organism inherits matters as much as the priority it chooses, so a
within-life comparison cannot separate the priority's value from the trajectory it lands on.

## Measurement 4 — a within-life self-directed learner does not beat random

`ac78_engineering_addendum3.py`: the AC72 mechanism made concrete — the organism lives one life,
revises its priority against its own running production signal (propose a swap, hold it one
window, keep it iff production did not worsen), no oracle, no re-runs, no correct state. Its
produced order is then rated on the stationary scale (a score the organism never sees). 16 seeds:

| produced by | stationary quality |
| --- | ---: |
| within-life learner | **11.11** ± 0.55 |
| random order | 11.09 ± 0.17 |
| good order (reference) | 11.97 |
| bad order (reference) | 10.63 |

The learner's produced order is indistinguishable from random (+0.02). The revision loop is
chasing a signal that (a) is locked after the transient and (b) is history-confounded during it.

## The answer

**No — the organism cannot produce its priority from its own accumulated activity signal, for a
measured structural reason, not a search deficiency.**

The organism's own production signal is a **seed-specific fixed point**: it is set by the early
transient, then locked — the priority becomes behaviourally inert after ~8000 ticks (0/12 seeds
respond to a change), and in the only window where it does respond, the response is
path-dependent at the same magnitude as the coarse ranking it would have to resolve (confound
1.83 vs gap 1.90). The signal that actually ranks priorities — averaging across many independent
environments, the 12-seed oracle — is exactly the external multi-environment evaluation that a
single organism's own single life cannot generate. Content self-production requires a signal the
organism's own activity does not carry.

## What this establishes, and what it does not

**Established:** the remaining gap is structural, located, and quantified. It is not that the
learner is weak (AC73: a population does not help) nor that the signal is unmeasurable (AC77: it
is a fixed point). It is that the signal is a **locked, path-dependent fixed point** — the
organism's own single life carries no ranking information that survives its own history, and the
only ranking-resolving signal is across-environment averaging, which is external by construction.
This closes the content self-production question with the honest negative the task's success
criterion anticipated ("a negative result exposing a structural obstacle is valued over a
redefined success").

**Not established, and deliberately not implied:** this is not a claim that a *population* or a
*lineage* cannot produce good rules (that is a different question — many lives, not one); not a
claim about the AC76 4-bank priority's own fitness signal (which is near-nil and never the
question); nothing about autopoiesis, consciousness or life. The measured quantity is sites
retained under the declared regime-B stress rates.

## The reframe for any successor work

The coarse ranking *is* resolvable — but only by the multi-environment averaging that a single
organism's single life cannot do. Any successor claim of content self-production must therefore
supply a within-life signal that (a) is not a fixed point and (b) is not path-dependent, or it
must stop using "the organism's own single life" as the production unit and say so explicitly.
The AC77 corollary stands, sharpened: it is not merely the fine plateau that a single life cannot
resolve — it is the coarse good-vs-bad separation too, once the organism is confined to its own
one trajectory.

## Bounds

Engineering prerequisite. No protocol, no final seeds, nothing frozen, nothing claimed about
autopoiesis/consciousness/life. Measured quantities: live-site count (snapshot, stationary mean,
and within-life series) in the declared AC32/33 regime-B ranking world, over disjoint engineering
seeds 8500–8799. Disjoint from every frozen family (1000–3400, 5100–5507) and from AC76's
3000–3003.

## Artifacts

`ac78_engineering.py` (coarse ranking + single-life noise), `ac78_engineering_addendum.py`
(fixed-point inertness), `ac78_engineering_addendum2.py` (path-dependence),
`ac78_engineering_addendum3.py` (within-life learner), `ac78_engineering_robustness.py`
(50-seed path-dependence check). Related: `AC77_ENGINEERING_v1.md` (the
fixed-point and oracle-artifact measurement this extends), `AC73_ENGINEERING_v1.md` (the signal
floor), `AC72_FINDING_v1.md` (the AC30-learner proposal this tests behaviourally),
`AC76_RESULTS_v1.md` (the turnover mechanism whose "not established" list this closes, negatively).
