# Artificial organism research — v0.3

Current ACI research starts with the [constitution v3](ACI_RESEARCH_CONSTITUTION_v3.md),
[research tree v5](ACI_MASTER_RESEARCH_TREE_v5.md), and
[evidence index v5](EVIDENCE_INDEX_v5.md). The historical
[agent guide](NEW_AGENT_GUIDE.md) preserves earlier assignments; its reproduction
commands are not current experiment authorization.

Prospective ACI work is governed by the
[research constitution v3](ACI_RESEARCH_CONSTITUTION_v3.md), which separates
causal organizational role, functional necessity, and engineering advantage.
The [bounded A6 effort closed UNRESOLVED](A6_GATE_DECISION_v1.md).
The shared R9 existence question remains open; no neural training is authorized.
[Exact gate reduction](A6_GATE_REDUCTION_v1.md) certifies that eight-symbol
unrestricted capacity suffices, without certifying the coupled deployed family.
The [synthesis](ACI_RESEARCH_SYNTHESIS_v1.md) and
[next human decision package](ACI_NEXT_EXPERIMENT_DECISION_v1.md) move the program
to an identifiable first-order question. No organism restart, new architecture
construction or consciousness claim is authorized.

## Grounding analysis G1 (2026-11-10, analytic)

[GROUNDING_ANALYSIS_v1.md](GROUNDING_ANALYSIS_v1.md) asks what makes a body
variable matter to a system and not only to its evaluator, in an exact finite
model whose [protocol](GROUNDING_PROTOCOL_v1.md) was frozen before the run.
Dependence of the system's own memory on the variable does; a homeostatic
reward and a terminal state do not. It carries design consequences for Track C
H3/H4. [RWM_DESIGN_v1_REVIEW_1.md](RWM_DESIGN_v1_REVIEW_1.md) retracts one
finding of the RWM card and narrows its verdict.

Track C follow-up (design only):
[objective-swap amendment A1](docs/trackC/trackC_amendment_A1_objective_swap_v1.md)
adds the degradation-only cell with task rewards as the test of derived
regulation. [G1 erratum 1](GROUNDING_ANALYSIS_v1_ERRATUM_1.md) corrects a
mislabelled arm.

First Track C training run (2026-11-10):
[objective-swap results](TRACKC_SWAP_RESULTS_v1.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v1.md). Derived regulation did not
emerge in this learner at any noise dose.

Second run, a 2×2 of scaffolded start × graded gain:
[results v2](TRACKC_SWAP_RESULTS_v2.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v2.md). Regulation emerged in no cell.
Scaffolded agents learned to absorb the noise ("ARMOURED") instead of
regulating, which points to the additive noise form as the obstacle.

Third run, erasure-type fate with a scaffolded start:
[results v3](TRACKC_SWAP_RESULTS_v3.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v3.md). Regulation again did not emerge.
The skill stayed intact, but no agent found the multi-meal schedule that
erasure makes valuable, so discovery is now the leading obstacle.

Fourth run, the same with a gentler maintenance duty (wear 0.005 → 0.001):
[results v4](TRACKC_SWAP_RESULTS_v4.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v4.md). Regulation did not emerge
(one cell PARTIAL, three NO_EMERGENCE). For the first time, agents ate more
and stayed in band longer than their yoked partners, in all four cells and
not under the null objective. The difference was about a third to two-thirds of the margin
and still growing when the budget ended.

Fifth run, the same with three times the phase-2 budget:
[results v5](TRACKC_SWAP_RESULTS_v5.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v5.md). The frozen emergence rule was
met in no cell (one PARTIAL, one NO_EMERGENCE, two ARMOURED). In the SAT,
rate 0.3 cell, six of nine agents learned to keep their energy in band, timed
to need, without being paid for it. They were in band up to 0.94 of the time,
against at most 0.51 for their yoked partners. Elsewhere agents made their
memory robust to erasure instead. This per-agent finding was made after the
run and needs confirmation on fresh seeds.

Sixth run, a confirmation of that cell on 18 fresh seeds, under a per-agent
regulator criterion frozen in advance:
[results v6](TRACKC_SWAP_RESULTS_v6.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v6.md). **CONFIRMED.** Seven of 18
fate agents regulated their energy, in band 0.66–0.90 of the time and eating
3–17 times more often when low than when high, against 0 of 18 yoked partners
and 0 of 18 agents under the control objective. This is the program's first
pre-registered positive result on derived regulation, limited to this cell.
All 11 other agents made their memory robust to erasure instead (Spearman
−0.95 between the two), so the dependence must not be bypassable. Final
weights are saved for identifying the bypass (option K).

Option K, step 1: locating the bypass in v6's saved agents, with no training:
[results](TRACKC_BYPASS_DIAG_RESULTS.md), with its
[frozen protocol](TRACKC_BYPASS_DIAG_PROTOCOL.md). The frozen verdict is
NOT_IDENTIFIED, because the test of external storage was too strict. The data
are clear, though. Every bypass agent walks to a place that encodes the cue
and reads it back from the walls it sees: shuffling the wall inputs removes
most of its erasure robustness, while food and interoception carry nothing.
Step 2 (erasure also relocates the agent) was then run on the PI's decision.

Seventh run, option K step 2, the same four cells as v5 on fresh seeds, with
every erasure now also moving the agent to a random cell:
[results v7](TRACKC_SWAP_RESULTS_v7.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v7.md).
- **The primary test passed: 8 of 9 fate agents regulate** in the cell where
  v6 found 7 of 18, with the bypass closed. A second cell (GRADED, `r` = 0.3)
  went from 0 of 9 in v5 to 6 of 9. Across all four cells, 21 of 36 agents
  regulate, against 6 of 36 in v5, while 0 of 54 yoked or control agents do.
- With the position bypass closed, regulation became the rule. The competing
  route is what held v6's rate down.
- **The `r` = 0.1 cells were labelled "bypass open"** by a threshold that was
  set for `r` = 0.3. Every agent there scores exactly what internal memory
  alone predicts. SAT `r` = 0.1 has 7 of 9 regulators, which is descriptive
  only. Correcting that label is post hoc.

Eighth run, option M, a confirmation of v7's open cells on fresh seeds. Each
cell had a non-memory control at the same gain and rate, and a bypass check
matched to the erasure rate:
[results v8](TRACKC_SWAP_RESULTS_v8.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v8.md).
- **Both claims were CONFIRMED, each with 9 of 9 regulators:** SAT `r` = 0.1
  and GRADED `r` = 0.3. Both cells had 0 of 9 in v5, while the bypass was
  open.
- GRADED `r` = 0.1, where erasure is weak and continues in band, has 3 of 9.
- Pooled over v7 and v8, the confirmed cells stand at 16 of 18 and 15 of 18.
  No yoked partner or control agent has regulated (0 of 108).
- For this learner and world, derived regulation is the rule wherever the
  dependence cannot be routed around and leaving the band costs enough.

## RWM design card (2026-11-01, design only)

[RWM_DESIGN_v1.md](RWM_DESIGN_v1.md) specifies a recurrent workspace /
higher-order monitor / metabolic perception-action architecture as discrete
logic-gate primitives, with exact integration (Phi_s) and causal-density
instruments and a pre-scale gate. Its result is NO_GO: the RWM-8 skeleton
has Phi_s = 0 on all closed-loop stationary mass. No training is authorized.
Reproduce with `python -m unittest test_rwm` and `python verify_rwm.py --out <new dir>`.

## Status at 2026-10-23 hand-off

Open pull requests #3 through #14 are brought onto this branch with merge
commits. The next team should start at
[docs/handoff_2026-10-23/](docs/handoff_2026-10-23/). The lead machine's
working tree and the literature search are in
[archive/local_workspace_2026-10-23/](archive/local_workspace_2026-10-23/).

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


## Repository layout

The repository is a research log with frozen, hash-checked artifacts, so files
are intentionally **not** relocated: scripts import each other as flat modules
and many results/protocols reference paths and hashes verbatim.
See [docs/REPOSITORY_MAP.md](docs/REPOSITORY_MAP.md) for a navigation guide by
filename prefix.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` lists the third-party libraries imported by the code
(NumPy core; Matplotlib for figures; PyTorch only for the `phase3*`/bridge work).
Run scripts and tests from the repository root, e.g. `python -m unittest -v test_e1`.

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing anything.
