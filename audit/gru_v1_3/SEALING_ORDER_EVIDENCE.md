# Sealing-order evidence

Manifest commit `124f60cdd420bbf95a2e2a0464cd23b1ea912829` was created before the first roster checkpoint was loaded.

- Git `CommitDate` for `124f60cd` is Thu Oct 22 02:51:29 2026 +0000 (`git show -s --format=fuller 124f60cdd420bbf95a2e2a0464cd23b1ea912829`). The reflog records the same instant: `HEAD@{2026-10-22 02:51:29 +0000}: commit: Freeze the GRU oracle-accessibility audit implementation.`
- The frozen runner was started after that commit. The tmux session `gru-audit`, which executed `audit/gru_v1_3/run_frozen.sh`, was created Thu Oct 22 02:51:36 2026 UTC. That timestamp is the session listing printed when the run was started.
- The runner copies each roster checkpoint to `/tmp/gru_oracle_audit_outside_repo` and reads that copy. The earliest file there is `PR7_s100_cand_init.json`, with mtime `2026-10-22 02:51:37.187265002 +0000`. The run log `/tmp/gru_audit_run.log` begins with `S0 seeds 40 checkpoints 290` and `S0 PR7/s100/cand_init ok`. The log's mtime is `2026-10-22 02:52:04.343400671 +0000`, when the run finished.

The manifest commit is 8 seconds before the first checkpoint copy. The runner also refuses to start when `IMPLEMENTATION_MANIFEST.json` is absent, and that file was added in `124f60cd`. No roster checkpoint was loaded before that commit.
