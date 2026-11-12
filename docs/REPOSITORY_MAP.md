# Repository map (by filename prefix)

| Pattern | Meaning |
|---|---|
| `README.md`, `ACI_*.md`, `EVIDENCE_INDEX_v*.md`, `NEW_AGENT_GUIDE.md` | Entry points: constitution, research tree, evidence index |
| `E1_*`, `e1/`, `e1_results/`, `test_e1*` | E1a benchmark package, protocol, results |
| `AC<n>_*.md` | Protocols, results, findings for numbered experiments (AC = assignment/check) |
| `ac<n>_*.py` | Experiment/library modules for experiment `<n>` (imported flat by other scripts) |
| `audit_*.py`, `replay_*.py`, `diagnose_*.py`, `verify_*.py`, `explore_*.py` | Audit, replay and diagnostic scripts |
| `test_*.py` | `unittest` suites; run from repo root |
| `*_results_v*/`, `*_engineering_v*/`, `*_calibration_v*/` | Frozen run outputs (`results.json`, `rows.jsonl`, snapshots) |
| `phase3*`, `PHASE*.md` | Phase 3 neural experiments (needs PyTorch); checkpoints are `.pt` files |
| `bridge/` | Bridge package; see `bridge/README.md` |
| `SUB_A_*`, `A6_*`, `M5_*`, `R*` | Sub-programs, gate decisions and monitor design docs |
| `_*.py` | Private helper/analysis scripts |
| `GROUNDING_*.md`, `grounding/`, `grounding_v1/`, `verify_grounding.py`, `test_grounding.py` | Grounding analysis G1: frozen protocol, exact model, grid results |
| `TRACKC_SWAP_*.md`, `trackc_swap/`, `trackc_swap_v1/`, `run_trackc_swap.py`, `test_trackc_swap.py` | Track C objective-swap experiment (needs PyTorch CPU) |
| `TRACKC_SWAP_*_v2.md`, `trackc_swap/factorial.py`, `trackc_swap_v2/` (incl. `phase1_weights/`), `run_trackc_swap2.py` | Track C swap v2: 2×2 of scaffolded start × graded gain |
| `TRACKC_SWAP_*_v3.md`, `trackc_swap/erasure.py`, `trackc_swap_v3/` (incl. `phase1_weights/`), `run_trackc_swap3.py` | Track C swap v3: erasure-type fate, scaffolded start |
| `TRACKC_SWAP_*_v4.md`, `trackc_swap_v4/` (incl. `phase1_weights/`), `run_trackc_swap4.py` | Track C swap v4: erasure fate, scaffolded start, wear 0.001 (option E) |
| `TRACKC_SWAP_*_v5.md`, `trackc_swap/longrun.py`, `trackc_swap_v5/` (incl. `phase1_weights/`), `run_trackc_swap5.py` | Track C swap v5: v4 with 3600 phase-2 updates (option G) |
| `TRACKC_SWAP_*_v6.md`, `trackc_swap/confirm.py`, `trackc_swap_v6/` (incl. `phase1_weights/`, `pair_weights/`), `run_trackc_swap6.py` | Track C swap v6: confirmation of v5's SAT `r` = 0.3 regulators on fresh seeds (option J); CONFIRMED |
| `TRACKC_BYPASS_DIAG_*.md`, `trackc_swap/bypass.py`, `trackc_bypass_diag/` (incl. post-hoc `posthoc_position.py`), `run_trackc_bypass_diag.py` | Track C swap option K step 1: where v6's bypass agents hold the cue bit (position, read through walls) |
| `TRACKC_SWAP_*_v7.md`, `trackc_swap/relocate.py`, `trackc_swap_v7/` (incl. `phase1_weights/`, `pair_weights/`), `run_trackc_swap7.py` | Track C swap option K step 2: erasure also relocates the agent; K1 SUPPORTED (8/9 regulators in SAT `r` = 0.3), GRADED 0.3 EMERGES |
| `TRACKC_SWAP_*_v8.md`, `trackc_swap_v8/` (incl. `phase1_weights/`, `pair_weights/`), `run_trackc_swap8.py` | Track C swap option M: confirmation in the relocation world; SAT `r` = 0.1 and GRADED `r` = 0.3 CONFIRMED (9/9 each) |
| `TRACKC_PROBE_*.md`, `trackc_swap/probe.py`, `trackc_probe/`, `run_trackc_probe.py` | Track C swap option P: probe of v7/v8 weights; regulators' states anticipate E (P1, P2 hold), regulation runs through interoception (P3 undetermined, 29/29) |
| `TRACKC_SWAP_ERRATUM_1.md` | Swap-line erratum: fate and yoked agents shared Adam optimizer state in every scaffolded pair, v2–v8; what it puts in doubt |
| `TRACKC_PROBE_ERRATUM_1.md` | Option P erratum: agents do not receive previous action or reward; no number changes |
| `TRACKC_ROUTE_ASSESSMENT_v1.md` | Route check after v8 and P: what the swap line has established, what it has not, and the deciding experiments |
| `TRACKC_CAUSAL_*.md`, `trackc_swap/causal.py`, `trackc_causal/`, `run_trackc_causal.py` | Track C swap option Q: causal probes; closed loop through interoception holds (42/42); post-meal suppression and contingent-erasure claims fail their bars (small effects) |
| `TRACKC_PAID_*.md`, `trackc_swap/paid.py`, `trackc_paid/`, `run_trackc_paid.py` | Track C swap option R: derived against paid regulators with independent optimizers; derived regulation holds (18/18, 0 yoked); derived ahead on anticipation (13/16, weak), no difference on suppression or robustness; both lose regulation when their ground is removed |
| `docs/trackC/` | Track C design amendments written after the 2026-11-01 archive |
| `RWM_*.md`, `rwm/`, `rwm_gate_v1/`, `verify_rwm.py`, `test_rwm.py` | RWM design card: discrete topology, Phi_s/causal-density gate, untrained reference model |

## Follow-up recommendation
A physical move into `src/`, `experiments/`, `tests/`, `docs/` would require
rewriting hundreds of flat imports and hash-pinned path references. Do it
incrementally per sub-program with tests, not in a single pass.
