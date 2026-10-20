# Contributing

Placeholder guidance; this is a research log, so integrity of records matters most.

- Frozen artifacts (`*_results_v*/`, `*_v1.md` protocols, `frozen_config.json`, checkpoints)
  are hash-referenced. Do not edit or move them; add a new versioned file instead.
- Run code from the repository root; modules are imported flat (e.g. `import ac4`).
- Run the relevant `test_*.py` with `python -m unittest -v <module>` before submitting.
- Do not start experiments the current constitution does not authorize (see README).
- Keep cleanup changes separate from research changes.
