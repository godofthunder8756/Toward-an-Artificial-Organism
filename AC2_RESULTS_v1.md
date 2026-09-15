# AC2: mutual maintenance of an acquired controller and its repair catalysts

2026-09-14. Engineering results, with all configurations and failures retained.
**The long-term autonomy goal remains active and incomplete.**

## New result

AC2 implements the first production stage proposed after AC1. Each memory bank
has short-lived local catalysts. Effective trace writes require those catalysts.
The acquired, vulnerable controller must choose and pay for their production;
the resulting catalysts enable repairs to the same controller's information.

At the two lower corruption rates, all 16 individuals sustained this loop for
4,096 ticks, equivalent to 64 maximum catalyst lifetimes. Every one produced
508 replacement catalysts from precursor, starting from an endowment of 12.
They finished with 100% controller and arbitrary-payload accuracy.

Blocking synthesis caused catalyst depletion and reduced functioning. Supplying
catalysts externally restored functioning in those same two environments. The
effect on controller information persists when energy and material are held
abundant. Together with targeted mechanism tests, this supplies model-relative
evidence for both P→W production and W→P repair dependencies.

It is not full autopoiesis. Catalyst laws, sensing, generic execution, demonstrated
priorities and external supplies remain specified by us. There is no produced
energy converter or spatial boundary yet. The chemistry is an abstract finite
reaction model, not a biological validation.

## Design and evidence provenance

[Protocol](AC2_PROTOCOL_v1.md) was written before the run. The
[pre-run snapshot](ac2_results_v1/pre_run_snapshot.json) records source, tests,
protocol and inherited generic-helper hashes. The full grid contains three
corruption rates, 16 seeds and seven arms: 336 rows. Seed is the replication
unit; arms and rates are repeated conditions. All comparisons are engineering
descriptives, not external preregistration or independent confirmation.

Each catalyst binds four material units, requires two energy units to assemble,
and expires after at most 64 ticks. Synthesis needs a surviving local catalyst;
it cannot restart an empty bank. Each catalyst enables at most eight trace
writes per action. The acquired controller's information occupies two of four
damageable banks. Its table is memorized from demonstrations and belongs to the
same 24-priority-permutation family as AC1, not an independently learned set of
new needs. Additional table rows and larger banks are required by the W sensor.

There is no death rule based on catalyst count. Without catalysts, writes cease
because their reaction cannot occur. Depleted energy terminates activity. As in
AC1, final raw information in terminated individuals is their stopped state;
separate functional endpoints assign zero after termination.

## Full results

Mean fraction of 4,096 planned ticks active:

| Per-copy flip rate | Self | No synthesis | No policy writes | Protected policy | Catalyst rescue | Self, resources clamped | No synthesis, resources clamped |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0.00025 | 1.000 | 0.640 | 0.469 | 1.000 | 1.000 | 1.000 | 1.000 |
| 0.0005 | 1.000 | 0.283 | 0.283 | 1.000 | 1.000 | 1.000 | 1.000 |
| 0.001 | 0.581 | 0.177 | 0.186 | 1.000 | 0.825 | 1.000 | 1.000 |

Self completion was 16/16, 16/16 and 7/16 respectively. No-synthesis completion
was 2/16, 0/16 and 0/16. Catalyst-rescue completion was 16/16, 16/16 and 11/16.
The protected-policy control completed every run, but that does not mean its
damaged body retained its policy: at the highest rate, body policy accuracy was
88.4% while the protected external policy sustained behavior.

The first two environments passed every prespecified engineering criterion.
The highest rate failed self viability, catalyst-rescue viability and the
all-individual turnover criterion. Its narrower causal contrasts remained
positive; that does not turn it into a successful robust construction.

## Removing the common-starvation explanation

External reservoir clamps keep both arms active; they do not restore trace bits.

| Rate | Self with clamp: final policy accuracy | No synthesis with clamp | Paired difference, percentage points [descriptive 95% interval] |
| --- | ---: | ---: | --- |
| 0.00025 | 100.0% | 25.9% | +74.1 [72.3, 76.1] |
| 0.0005 | 100.0% | 13.8% | +86.2 [85.0, 87.3] |
| 0.001 | 99.95% | 11.9% | +88.0 [86.4, 89.7] |

Every initial catalyst in the blocked-synthesis clamp arm expires by tick 64.
Resource abundance preserves execution but not the acquired decision information
without the produced writing machinery. This avoids interpreting survival alone
as successful maintenance.

Self minus no-synthesis activity differences were +36.0, +71.7 and +40.4
percentage points, with descriptive 95% intervals [25.2,46.9], [69.0,74.4] and
[20.4,61.0]. All intervals bootstrap paired seeds (10,000 resamples) and are
uncorrected across the exploratory grid.

## Production, turnover and conservation

At either lower rate, every self individual starts with 12 catalysts, produces
508, experiences 512 expiries, and ends with eight. Thus 12+508−512=8. The
initial endowment is completely gone long before the endpoint. All four banks,
including both controller banks, receive paid trace writes.

The audit checks for every row:

**initial free material + initial catalyst-bound material + imports + clamp
inputs + external catalyst-bound additions = final free material + final
catalyst-bound material + trace replacement waste + expired catalyst waste +
overflow.**

Energy is separately balanced against collection, clamps, living, synthesis,
writes and overflow. No catalyst is created by a zero-substrate or parent-free
synthesis reaction. External catalyst rescue is explicitly counted and is not
mistaken for internal production.

## Highest-rate failures: exploratory chronology

[The observer-only replay diagnostic](AC2_FAILURE_CHRONOLOGY_v1.json) reproduces
all 16 final states exactly and records the first policy error, wrong action,
empty catalyst bank and termination.

- All nine terminated self individuals had policy corruption followed by a
  wrong action before termination.
- Eight of those nine terminated without any catalyst bank ever becoming empty.
- The remaining individual first lost a policy row at tick185, made a wrong
  action at386, lost catalysts at432 and terminated at849.
- The seven completing individuals had no observed post-step policy error or
  wrong action in this replay.

Thus a blanket explanation that catalyst extinction caused the highest-rate
failures is contradicted by eight cases. Limited repair capacity, allocation,
resource constraints and irreversible controller-bit errors remain candidate
causes. Chronology alone is not causal mediation. The near-perfect policy
accuracy with resource clamps points to a resource/maintenance interaction,
but does not identify its detailed mechanism. No tuning followed these results.

## Verification and limits

[Audit](AC2_AUDIT_v1.json): source hashes match; all 336 rows have expected unique
coverage and recorded environment pairing; energy, material, birth/expiry and
write ledgers balance; arm means and bootstrap contrasts reproduce; 21 sampled
reruns (seed0, all arms and rates) match exactly. Seven mechanism tests pass.

Tests directly show that:

- removing W blocks actual writes while resources remain;
- W births require parent W and paid substrate;
- changing an acquired SYNTH decision to REST prevents production;
- all original W expires without replacement even under resource clamps;
- full-state erasure removes history dependence under identical future inputs;
- a protected policy argument is rejected by the self arm.

This is a same-author audit of a trusted in-process simulator. It does not provide
independent scientific review, adversarial process isolation, biological rates,
autonomous dependency discovery or a self-produced boundary.

## Next research decision

The P↔W mechanism is feasible at two declared rates. That warrants the next
planned constituent: **C, a produced energy-conversion mechanism**, replacing
the current direct food-to-energy action with catalyst-dependent conversion.
The corresponding tests must block C production, clamp energy, and distinguish
production of a converter from merely controlling an externally working charger.

A spatially produced boundary remains a subsequent mandatory target for the
broader autopoietic claim. Autonomous acquisition of new needs and viable
relinquishment must later be demonstrated in that coupled architecture. The
successful P↔W stage does not replace those requirements or complete the goal.

## Reproduction

```powershell
py -3.12-arm64 -B -m unittest -v test_ac2
py -3.12-arm64 -B ac2.py --out new_ac2_engineering
```

The runner refuses an existing directory. The recorded run took about57 seconds
on Python3.12.10 ARM64/NumPy2.3.5; this is not a hardware-independent estimate.
[Model](ac2.py), [tests](test_ac2.py), [full data](ac2_results_v1/results.json),
[audit source](audit_ac2.py), [chronology source](diagnose_ac2.py).

All earlier experiment sources, freezes and results remain unchanged.
