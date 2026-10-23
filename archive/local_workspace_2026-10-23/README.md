# Local workspace archive, 2026-10-23

Start with [docs/handoff_2026-10-23/](../../docs/handoff_2026-10-23/).

This directory is the lead machine's local working tree plus the downloaded
literature search, extracted with their original paths. Nothing here was
re-run. Two hand-off files from this tree are also installed under
`docs/handoff_2026-10-23/handoff/`: the final `RD_addendum_trackC.md`
(sha256 `d6fe1233c6e8789d0b16b68fb39d722688850a5d1954c590180bafbc4e35b896`;
the stale copy is `RD_addendum_trackC.prior-11bf1aa6.md`) and
`RD_repo_gap_list.md` (sha256 `167cccff2ee629ccb88f333e002062b8c366726c6b568cdb421ed4a8271084b0`).

## Sources

- `aci_ws_A_papers_2026-10-23.tar.gz`
  (sha256 `f8f18a7d568354f9bc323f31351f85845c89e4b8d427005d3c587e859ea6e87d`),
  474 files. Prior-art and literature downloads, mostly under `tmp_pa2/`,
  `tmp_pa4/`, `tmp_pa/`, `tmp_p3/`, `tmp_p3b/`, and `tmp_p6/`.
- `aci_ws_B_work_2026-10-23.tar.gz`
  (sha256 `2c278927552eb5d29f76d58aed4f6f8bbeeb592ce832d67cea7c61bf8b73defb`),
  1211 files. Astra consult replies #5–#42 (`astra_consult*_response.txt`,
  `astra_consult_1.md`), review drafts (`review/`), hand-offs (`handoff/`),
  pending briefs (`pending/`), scratch (`scratch/`, `scratch_rd/`),
  ASCII-part serve trees (`astra_serve*/`), and cloud-agent transcripts
  (`cloud-agent-transcripts/`).
- `all.txt` (sha256 `f93fccfe1b95f16fee4c62dc3381999a534d63f8d6c6df26baf2723bf12d2d99`),
  placed at `all.txt`. It was not inside archive B.

1,686 extracted files, plus this README. No file is over 50 MB. `__pycache__/`
and `.pyc` files were not present.

## Redactions

One third-party API key in `tmp_pa2/cos_rr.html` (a BugHerd `apikey` query
parameter on a saved page) was replaced with `[REDACTED]`. OpenAlex responses
that say `api_key=YOUR_KEY` are the publisher's placeholder, and
`tmp_pa2/asp.html` only clears an empty `last_page` cookie. Those were left
as saved.
