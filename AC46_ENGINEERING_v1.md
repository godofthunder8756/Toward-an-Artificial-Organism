# AC46 engineering: the AC37 world re-examined with the correct paired test — and it resolves

2026-09-15. Engineering only. **No protocol was written and no final seed was run before this
measurement.** It re-opens AC37, which had stopped on a criterion AC38 later showed measured the wrong
quantity.

## What AC37 stopped on, and why that stop is now re-examined

AC37 (self-funded world: production period 4, drain 3) stopped because its endpoint gave "margin 5.92
against noise sd 0.83, ratio 7.16", below the inherited "margin/noise ≥ 10" criterion. But that
criterion measures the **marginal** noise — the sd of *one order's* rating across disjoint seed sets.
AC38 then showed that a **paired** arm comparison does not face that variance: every arm is rated on the
same scoring seeds, so the seed-set identity variance cancels in the arm difference, and the honest test
is the exact sign-flip test on the paired per-individual differences. AC37's own document required
exactly this: "a successor must justify its own threshold from the variance that actually limits a
paired comparison (the interaction, not the between-seed-set variance), before its seeds."

AC38 is that justification. This measurement applies it back to the unchanged AC37 world.

## The re-examination

12 individuals (seeds 4600–4611), the AC33/AC36 arm family, the AC37 world at 600 ticks, corruption
irrelevant (this line has no register damage; the endpoint is population retained). The paired
difference is `learner_both − no_release`.

| seed | learner | no_release | difference |
| ---: | ---: | ---: | ---: |
| 4600 | 6.17 | 1.75 | 4.42 |
| 4601 | 6.33 | 1.75 | 4.58 |
| 4602 | 6.33 | 1.75 | 4.58 |
| 4603 | 5.75 | 1.75 | 4.00 |
| 4604 | 6.33 | 2.50 | 3.83 |
| 4605 | 6.33 | 1.75 | 4.58 |
| 4606 | 5.92 | 1.75 | 4.17 |
| 4607 | 7.67 | 1.75 | 5.92 |
| 4608 | 6.33 | 2.50 | 3.83 |
| 4609 | 5.00 | 1.75 | 3.25 |
| 4610 | 7.67 | 1.75 | 5.92 |
| 4611 | 7.67 | 1.75 | 5.92 |

**Sign-flip test: p = 0.00049 — the power floor 2/2¹².** All 12 individuals impaired
(learner > no_release in every one). Mean difference +4.58 sites, median +4.50, minimum +3.25.

| arm | min | mean | max |
| --- | ---: | ---: | ---: |
| learner_both | 5.00 | 6.46 | 7.67 |
| no_release | 1.75 | 1.88 | 2.50 |
| no_search | 1.42 | 2.60 | 5.83 |
| preserve | 1.42 | 2.60 | 5.83 |
| oracle_a | 1.75 | 1.75 | 1.75 |
| oracle_b | 7.67 | 7.67 | 7.67 |

The separation of minima is clean: **learner worst 5.00 > no_release best 2.50**, a 2.5-site gap. The
oracle arms bracket the claim (oracle_b ceiling 7.67 ≥ 4.0, oracle_a floor 1.75 < 4.0). The state-blind
arms (`no_search`/`preserve`, both the random initial order) have means 2.60 < 4.0, though one individual
(4604) drew a random order that scores 5.83 — the reason the state-blind gate uses the *mean*, not the
max (the AC36 precedent).

## The AC40 four-check

| check | result |
| --- | --- |
| resolvability | p = 0.00049, n = 12, resolved at the floor |
| effect size | median +4.50 sites, in the endpoint's own units |
| stability (ratio) | unstable, as expected — AC40 finding #2: the mean/sd ratio does not discriminate; impaired fraction (1.0) and per-individual differences are reported directly |
| headroom | learner at 5.0–7.67 of 24 sites, nowhere near saturation |

## The verdict, and what it does not claim

The AC37 stop was a **criterion artifact**: the world resolves the arm contrast under the correct paired
test. The self-sufficiency line is re-opened. A protocol may follow on fresh seeds (4700–4711).

This establishes nothing about an organism yet — no protocol, no final seeds, no frozen directory, no
claim. It is a measurement that a previously-stopped world passes the statistical test its own stop
document named. Nothing here speaks to autopoiesis, experience or life; the endpoint is sites retained
by an organism that pays a constant cost to stay alive and produces energy from its own sites.

## Artifacts

`/tmp/ac46_engineering.json` (the 12 paired rows). Related: `AC37_ENGINEERING_v1.md` (the stop this
re-opens), `AC38_CRITERION_v1.md` (the paired test this applies), `AC36_RESULTS_v1.md` (the passing
insufficient-income study this complements).
