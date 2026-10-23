# Experiment results and adjustment record

Exploratory research, 28 September 2026. No preregistration or public submission has occurred.

## Decision

Adjust the task before confirmation. The original one-step setup had a survival floor; it could not support a meaningful comparison of survival robustness. Preserve that result and keep subsequent development runs separate.

## What ran

| Stage | Design | Episodes reaching 40 steps |
|---|---|---:|
| Original pilot | Five methods, three signals, four seeds, two layouts; one-step planning and initially unknown resource map | 0/120 |
| Calibration | Known-map check, one-step planning | 0/10 |
| Calibration | Known-map check, two-step planning | 2/4 |
| Adjusted pilot | Same five-method, three-signal, four-seed, two-layout grid; known resource map and two-step planning | 66/120 |

The calibration checks used seed 0. The two-step check tested uniform and coupled agents only. The adjusted pilot changed both prior map knowledge and planning horizon relative to the original. It is not a controlled single-factor attribution of the original failure.

## Adjusted pilot outcomes

Survival counts below are out of eight episodes per cell (four seeds × two layouts). This is a small descriptive pilot, not a ranking established by statistical evidence.

| Method | Clean | Biased thirst signal | Random thirst perturbation |
|---|---:|---:|---:|
| uniform | 4/8 | 4/8 | 4/8 |
| coupled | 4/8 | 4/8 | 4/8 |
| sensing | 4/8 | 3/8 | 4/8 |
| confidence | 4/8 | 4/8 | 4/8 |
| preference | 6/8 | 7/8 | 6/8 |

### Layout dependence

- km_easy_00: 59/60 episodes reached 40 steps.
- km_easy_01: 7/60 episodes reached 40 steps.

The mean seed-paired bias-induced regulation-loss difference (coupled minus preference) was 0.02052, with seed-level values from -0.07708 to 0.15375. Negative values favor coupled on this particular contrast; positive values favor preference. Four seed clusters do not establish general superiority.

## Identical-input diagnostic

On six uniform-agent reference trajectories, 165 snapshots were evaluated counterfactually. Holding observations and priors fixed changed body posteriors when assumed precision changed. Holding beliefs fixed changed the top policy in 58 snapshots for planning precision and 84 for preference reweighting.

Counterfactual evaluations did not drive the trajectories. Each reference episode was rerun without them and checked for exact equality. Snapshots within a trajectory are dependent; these counts are manipulation checks, not independent effect-size estimates or evidence of consciousness.

## Limits and next design decisions

- Preserve all pilot results, including the failed runner attempt, before changing settings again.
- Resolve task difficulty across multiple layouts and seeds before using survival as a primary comparison.
- Test parameter sensitivity with equal validation budgets; the preference weight of two was a pilot choice, not an optimized match to sensor precision.
- Separate the effects of horizon and map knowledge if attributing why competence improved; reconcile the source paper's longer horizon and repeated learning exposure before claiming replication.
- Use an intervention control that accounts for categorical boundary clipping. The random perturbation was zero-mean before clipping only.
- Freeze metrics, bias settings, analysis, exclusions, and a new confirmatory seed set after development. Register the plan before collecting confirmatory data.
- Interpret these as tests of computational regulation. No outcome validates or invalidates subjective feeling.

## Available records

Each pilot directory contains trajectories, episode summaries, configuration, dependency versions, checksums, validation, post-run data checks, and descriptive results. `pilot-methods.md` and `REPRODUCTION.md` explain the design and rerun procedure. All computing here was local CPU work; no paid model API or cloud compute service was invoked.
