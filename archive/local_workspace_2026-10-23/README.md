# Local workspace archive, 2026-10-23

This directory is the hand-off location for material that lived only on the
lead machine. The next team should start at
[docs/handoff_2026-10-23/](../../docs/handoff_2026-10-23/).

The consolidation agent did not receive the uploaded archives, so this
directory does not yet contain the extracted trees. The expected inputs were:

- `uploads/aci_ws_A_papers_2026-10-23.tar.gz`
  (sha256 `f8f18a7d568354f9bc323f31351f85845c89e4b8d427005d3c587e859ea6e87d`):
  downloaded literature and prior-art search material.
- `uploads/aci_ws_B_work_2026-10-23.tar.gz`
  (sha256 `2c278927552eb5d29f76d58aed4f6f8bbeeb592ce832d67cea7c61bf8b73defb`):
  the lead agent's local working directory, including Astra consult replies
  #5–#42, review drafts, hand-offs, pending briefs, scratch work, and
  cloud-agent transcripts.
- `uploads/all.txt`, missed from archive B, to be placed at `all.txt` here.

Two files in the git hand-off still need archive B:

- `docs/handoff_2026-10-23/handoff/RD_addendum_trackC.md` is the stale copy
  (sha256 `11bf1aa6141285333391bb7f3e8bc601b2b9a6523db6e9cae00c478cb641b7a2`).
  It should be renamed to `RD_addendum_trackC.prior-11bf1aa6.md`, and the
  final version from archive B `handoff/RD_addendum_trackC.md`
  (sha256 `d6fe1233c6e8789d0b16b68fb39d722688850a5d1954c590180bafbc4e35b896`)
  should take the original path.
- Archive B `handoff/RD_repo_gap_list.md` (sha256 prefix `167cccff`) should be
  copied to `docs/handoff_2026-10-23/handoff/RD_repo_gap_list.md`.

No secret scan was run, because the archives were not on disk.
