# Stage 0 manifest addendum

The working-tree file `frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json` was edited in place at fd720ee. These copies are separate immutable provenance artifacts. This addendum does not rewrite that file or any checkpoint.

> "Stage 0 was originally sealed at 0fed34e with code tree 1349a678.... Before Stage 1 optimization, fd720ee added the missing load_snapshot import and recorded corrected code tree d00ff89b.... The sealed manifest was edited in place to update code hashes, contrary to the intended immutable-manifest practice. Initial checkpoints, W0 hashes, episode digests and pairing records were unchanged. Stage 1 and Stage 2 used the corrected implementation. The original and corrected manifests are preserved as separate immutable provenance artifacts."

| copy | git source | code tree | sha256 of the copy |
| --- | --- | --- | --- |
| `STAGE0_MANIFEST_original_0fed34e` | `0fed34ebad4bee2b794ce1324ec286ae0a2c68ab` | `1349a6786e92d81ba194d866d48dd88304961b5acda900fc5cadc3c52998f7f9` | `17a6ff525261e43d951ae07546717c496bca20cc06e43478cb72e3a70aca2e4d` |
| `STAGE0_MANIFEST_corrected_fd720ee` | `fd720ee78ae7d60b7db425baca55bc1fca7af6b9` | `d00ff89b5c4be698a690c0c472a6bbdf00c1a0279af5d82a4a8c907d22696ee4` | `5b533f6ed372bbef18508aeff809a2dafe93fd9ee9b791e573058a0dd1dffb2a` |

Each copy is the manifest blob at that commit. The corrected copy matches the manifest still stored at `frozen_recurrent_compensation_results_v1/stage0/manifest_stage0.json`.
