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

## Follow-up recommendation
A physical move into `src/`, `experiments/`, `tests/`, `docs/` would require
rewriting hundreds of flat imports and hash-pinned path references. Do it
incrementally per sub-program with tests, not in a single pass.
