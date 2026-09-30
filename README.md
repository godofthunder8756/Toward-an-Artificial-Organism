# Artificial organism research — v0.3

New agents should begin with `NEW_AGENT_GUIDE.md`. It preserves the project's
research standards, negative results, claim boundaries, and the current E3
assignment.

Prospective ACI work is governed by the
[research constitution v2](ACI_RESEARCH_CONSTITUTION_v2.md), which separates
causal organizational role, functional necessity, and engineering advantage.
The current conditional authorization starts with the
[shared-four-context analytic gate](SHARED4_STAGE_A_GATE_v1.md); it does not
authorize an organism restart or a consciousness claim.

E1a implements the behavioral and causal gate for acquiring a new maintenance
priority. A learned recurrent memory circuit requires precursor for its actual
recurrent connections. An ordinary online controller learns resource choices.
Read RESEARCH_NOTEBOOK.md for the findings and E1_PROTOCOL.md for the exact scope.

This is a scaffolded research benchmark, not an artificial living or conscious
system. It does not yet implement locally growing neural tissue. The main
controller receives an explicit net-energy-production objective.

## Reproduce E1a

Python 3 and NumPy suffice for training/replay. Matplotlib exports figures.
Actual tested versions are recorded in e1_results/run.json and
e1_results/analysis_environment.json. Run from this directory:

```bash
python -m unittest -v test_e1
python -m e1.experiment --config e1/frozen_config.json --out reproduced_e1
python analyze_e1.py reproduced_e1
python export_e1_figure.py reproduced_e1
python verify_e1.py reproduced_e1
```

The runner refuses to overwrite an existing directory. No GPU, pretrained
models, text dataset, online service, or network access is required. Setting
OPENBLAS_NUM_THREADS=1 can avoid small-matrix thread overhead. Runtime and exact
numerical reproducibility depend on hardware and numerical-library versions.

A short engineering run uses only two seeds:

```bash
python -m e1.experiment --feasibility --out new_feasibility
python analyze_e1.py new_feasibility
```

To observe a trained agent without retraining:

```bash
python replay_e1.py --results e1_results --seed 100 --variant neural_q --stage acquired --world 0 --out replay.csv
```

Other stages: pre, acute, dependency, rescue, sham, lost_usefulness.
Other variants: tabular_q, frozen_neural_q, fixed_drive_q.
Checkpoints load without pickle. Evaluation replay is supported; exact
mid-training resumption is not currently supported.

## Implementation

| File | Purpose |
| --- | --- |
| e1/circuits.py | Sparse recurrent circuit, rewarded exploration, BPTT and Adam |
| e1/environment.py | Fixed grid paths, cues, energy and connection conductance |
| e1/control.py | Neural/tabular Q learning, frozen and assigned-drive controls |
| e1/experiment.py | Paired branches, training, evaluation and checkpoints |
| e1/config.py, e1/frozen_config.json | Default and frozen configuration |
| E1_PROTOCOL.md | Objectives, budgets, gates and departures from developmental tissue |
| E1_FREEZE.json | Hashes recorded before final data collection |
| ENGINEERING_LOG.md | Feasibility findings and baseline correction |
| test_e1.py | Ten numerical, causal, information-leak and geometry tests |
| analyze_e1.py | Seed-level inference, tables and PNG/PDF figures |
| replay_e1.py | Saved-policy evaluation without training |
| verify_e1.py | Frozen-source, coverage and exact-checkpoint-replay audit |

## Evidence

- e1_results/RESULTS.md: all controller/condition means and paired contrasts.
- e1_results/summary.json: seed means, bootstrap intervals and frozen gates.
- e1_results/E1_RESULTS.png and .pdf: exportable research figure.
- e1_results/evaluation.csv: all 4,480 final evaluation episodes.
- e1_results/assays.csv: initial, learned, degraded, lesioned and restored recall.
- e1_results/budgets.csv: planned/realized experience and parameter counts.
- e1_results/run.json: configuration, source hashes, versions and runtime.
- e1_results/VALIDATION.json: data audit and 28 exact checkpoint replays.
- e1_results/seed_100 through seed_119: per-seed adaptation logs, evaluation
  and checkpoints. Seed-100/world-0 traces were selected before evaluation.
- e1_feasibility_v1 and e1_feasibility_v2: exploratory runs, excluded from the
  final sample. V1 also preserves its differing module source.

## Earlier E0 pilot

pilot.py and results/ preserve the original experiment. Its notebook remains
in history/RESEARCH_NOTEBOOK_v0_1.md.

```bash
python pilot.py --out reproduced_e0
```

E2 now partially implements that target in `e2/`: one maintained recurrent
network jointly learns resource choices and delayed recall while local edge
biomass develops under material constraints. See `E2_PROTOCOL.md`,
`e2_results/RESULTS.md`, and `E2_DIAGNOSTIC_PROTOCOL.md`.

E2 found history-sensitive resource preferences and lesion dependencies, but
activity-guided local growth was less reliable than a fixed structural target.
The current frontier is `E3_DESIGN.md`: preserving acquired neural information
without a protected perfect copy. E1a remains the ordinary-learning baseline.
