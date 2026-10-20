# Recovery manifest d0ee2bb v1

Additive record only. No frozen file, protocol, result, errata, ledger, kanban, or README was edited.

On 2026-10-20 the repository owner approved restoring the 78 frozen result files deleted by commit `d0ee2bb46e3a6ec3d80be2b9ec6f53d9a1e7a89e` (2026-10-02, "Remove large result files and snapshots from multiple versions").

## Source

- Restored from commit `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`). The git blobs at that commit are the same objects recorded at A6 inventory head `370685b4ea44c26b16f3bbb49e3e8011c9cc269e`.
- Protected hashes live in `a6_decision_v1/baseline_hashes.json`, object `protected` (7,326 entries, schema 1). The preservation checker is `a6_decision_v1/preservation.py` (`python -B -m a6_decision_v1.preservation a6_decision_v1/baseline_hashes.json --check`), which hashes working-tree bytes with SHA-256 and does not normalize line endings.
- Each git blob is LF-only (no CR). Its SHA-256 does not equal the protected hash. Replacing each LF with CRLF, and changing nothing else, produces bytes whose SHA-256 equals the protected hash. That CRLF sequence is what was written. Converting the restored file back from CRLF to LF reproduces the `d0ee2bb^` blob exactly.
- There is no `.gitattributes` in this repository, and this restore did not enable `core.autocrlf`. Files were written as raw bytes so checkout normalization could not alter them.

## Approval

- Owner approval date: 2026-10-20

## Restored files

| Path | Restored SHA-256 | Protected SHA-256 | Protected-list source | Restored from |
| --- | --- | --- | --- | --- |
| `ac17_results_single_v1/pre_run_snapshot.json` | `b6f87da47cb7f6b005e06d8df4c372ebea243171f4c082dc188b9dabfa9094dd` | `b6f87da47cb7f6b005e06d8df4c372ebea243171f4c082dc188b9dabfa9094dd` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac17_results_single_v1/results.json` | `e68030862fdff6280f39e2ca7185378be4d55bac38e05e8d2ea8a53c2001e168` | `e68030862fdff6280f39e2ca7185378be4d55bac38e05e8d2ea8a53c2001e168` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac17_results_single_v1/rows.jsonl` | `88f1feceb0ec4296c5db720dd6867ed6b8effbdce0bddbfb3c479e0c9d5ebeb0` | `88f1feceb0ec4296c5db720dd6867ed6b8effbdce0bddbfb3c479e0c9d5ebeb0` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac18_results_v1/pre_run_snapshot.json` | `7a506426ea0cbea3cecbb298c50bc12920eeffb8bf67c7c1996fb0bd652e4618` | `7a506426ea0cbea3cecbb298c50bc12920eeffb8bf67c7c1996fb0bd652e4618` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac18_results_v1/results.json` | `14d009a6e54b670f20bbe7437a6aa63f06c1f303f149882d0fa847408f6b5ff6` | `14d009a6e54b670f20bbe7437a6aa63f06c1f303f149882d0fa847408f6b5ff6` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac18_results_v1/rows.jsonl` | `56f940c603c606ca9c8c483f03ef32d32b1f41c1e216c6ce8b66ff940815daa5` | `56f940c603c606ca9c8c483f03ef32d32b1f41c1e216c6ce8b66ff940815daa5` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac32_results_v1/pre_run_snapshot.json` | `ca1d76845d9ac922b991dcbeb3502ec89c994fe01794bbe0933ff297ba1fd3c6` | `ca1d76845d9ac922b991dcbeb3502ec89c994fe01794bbe0933ff297ba1fd3c6` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac32_results_v1/results.json` | `25e30c091b0a116c656e95125ba72aa32df17ba6cc55f99a215e6ca9b4f79590` | `25e30c091b0a116c656e95125ba72aa32df17ba6cc55f99a215e6ca9b4f79590` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac32_results_v1/rows.jsonl` | `7eb748030552991d73e54056702c5163614bfb01d351395a2a5a883cff142d23` | `7eb748030552991d73e54056702c5163614bfb01d351395a2a5a883cff142d23` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac33_results_v1/pre_run_snapshot.json` | `cc7c15007565e12ac309e6034da6729f2a3de969a6f6cee0ccbf1d909df2d3f4` | `cc7c15007565e12ac309e6034da6729f2a3de969a6f6cee0ccbf1d909df2d3f4` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac33_results_v1/results.json` | `65235869ab9ecbb8ced4647ec5c3cd01fe2efd3d5f032c37cefcc62db62676df` | `65235869ab9ecbb8ced4647ec5c3cd01fe2efd3d5f032c37cefcc62db62676df` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac33_results_v1/rows.jsonl` | `1a5833e3b189b93773a57b8c4c33b1229de375fec18d66d0bf933f4bebf2933a` | `1a5833e3b189b93773a57b8c4c33b1229de375fec18d66d0bf933f4bebf2933a` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac36_results_v1/pre_run_snapshot.json` | `65a5d75853412871a3b65f32944ebdb8fbc8858dbf0d9225c94fcd1244ea61f6` | `65a5d75853412871a3b65f32944ebdb8fbc8858dbf0d9225c94fcd1244ea61f6` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac36_results_v1/results.json` | `0b7cf522a083a82fdbc435065bd7556092641eba425630c9ce34b91fbfed86f3` | `0b7cf522a083a82fdbc435065bd7556092641eba425630c9ce34b91fbfed86f3` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac36_results_v1/rows.jsonl` | `0184e5c2dc2fd96ef5ee04f3bf355a7350361e7870998be5608187ad5ab7935d` | `0184e5c2dc2fd96ef5ee04f3bf355a7350361e7870998be5608187ad5ab7935d` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac43_results_v1/pre_run_snapshot.json` | `985fada6b8ba15311467d273a68b3d856ccdbdb1763b04e2fd3fd7af68dcb8a3` | `985fada6b8ba15311467d273a68b3d856ccdbdb1763b04e2fd3fd7af68dcb8a3` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac43_results_v1/results.json` | `e02d478dafbfb13db0152265758baf56e622db0d7169c666b78190fa5566cc09` | `e02d478dafbfb13db0152265758baf56e622db0d7169c666b78190fa5566cc09` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac43_results_v1/rows.jsonl` | `b7e487294a5a954101b54c6e3e3da204052dda444e1fdbe8d3a68a6e9226b496` | `b7e487294a5a954101b54c6e3e3da204052dda444e1fdbe8d3a68a6e9226b496` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac45_results_v1/pre_run_snapshot.json` | `4be20ca33a774123bdcf21ce74b7932c392712ca2231cf4eb00aa425b1ef9158` | `4be20ca33a774123bdcf21ce74b7932c392712ca2231cf4eb00aa425b1ef9158` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac45_results_v1/results.json` | `6a080e4acd96b40f4c83a096d088cdada2fcb7b751f34eee48c2a056960a361e` | `6a080e4acd96b40f4c83a096d088cdada2fcb7b751f34eee48c2a056960a361e` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac45_results_v1/rows.jsonl` | `b181ebdf0689b1f30a5b69d4c01e51461dcead1d7235c3327a022ad3b522ef4b` | `b181ebdf0689b1f30a5b69d4c01e51461dcead1d7235c3327a022ad3b522ef4b` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac46_results_v1/pre_run_snapshot.json` | `a1cfc2a86fbca4c07640f8915ef90449241eada67bafe3a37745568c4d19e4e4` | `a1cfc2a86fbca4c07640f8915ef90449241eada67bafe3a37745568c4d19e4e4` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac46_results_v1/results.json` | `c718d763e6192a0c58f2a0ff51d85f466c49e703680c4344199038cac8e96c4c` | `c718d763e6192a0c58f2a0ff51d85f466c49e703680c4344199038cac8e96c4c` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac46_results_v1/rows.jsonl` | `306fea945f5c652bc18525bd9ec68826a620f201790ca16508349e05809eef82` | `306fea945f5c652bc18525bd9ec68826a620f201790ca16508349e05809eef82` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac50_results_v1/pre_run_snapshot.json` | `8837378bb4c7e9a28286b80e5fac717d7d5ec80f1031629bb7d22c929b9a5427` | `8837378bb4c7e9a28286b80e5fac717d7d5ec80f1031629bb7d22c929b9a5427` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac50_results_v1/results.json` | `ec25074a208b79db347526ddf8e3e4c4737677e58e3c53a263ea8d5f0eeba861` | `ec25074a208b79db347526ddf8e3e4c4737677e58e3c53a263ea8d5f0eeba861` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac50_results_v1/rows.jsonl` | `d501ce5f447b6f43162018f635d1fb740ad3a2729701bf3dd4fc6f31bf9a2ec8` | `d501ce5f447b6f43162018f635d1fb740ad3a2729701bf3dd4fc6f31bf9a2ec8` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac54_results_v1/pre_run_snapshot.json` | `b68383c19bc51b54a068bac29d467894497f0a0dea5d1247bc73b0bb9aa8ee29` | `b68383c19bc51b54a068bac29d467894497f0a0dea5d1247bc73b0bb9aa8ee29` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac54_results_v1/results.json` | `ca1442ebe66e37d88a286d8793056c9f193d8ead7d11f96923bb45158ef8aded` | `ca1442ebe66e37d88a286d8793056c9f193d8ead7d11f96923bb45158ef8aded` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac54_results_v1/rows.jsonl` | `e9e32d3558d666ab4215dea251c4fc4b9b5080d2a8f5f11ee08a1ad15e9fdcdc` | `e9e32d3558d666ab4215dea251c4fc4b9b5080d2a8f5f11ee08a1ad15e9fdcdc` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac55_results_v1/pre_run_snapshot.json` | `8f86dc848ebd6bc2839c0b713f59af01adfba1851d930b6870d278f5fce42ff1` | `8f86dc848ebd6bc2839c0b713f59af01adfba1851d930b6870d278f5fce42ff1` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac55_results_v1/results.json` | `c026b28b9ab12eec64feff9d104d6f69a2a5a2e877e6ac62886c12c669dc06e4` | `c026b28b9ab12eec64feff9d104d6f69a2a5a2e877e6ac62886c12c669dc06e4` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac55_results_v1/rows.jsonl` | `74bb9badd75b098a219109bc0ba76b6e4e4549f342c9fa6af7bca49768fc5b74` | `74bb9badd75b098a219109bc0ba76b6e4e4549f342c9fa6af7bca49768fc5b74` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac57_results_v1/pre_run_snapshot.json` | `c74c4b433c69b56280d5cab606838f90b381bebf15ad6356f5dec76a6397bbd0` | `c74c4b433c69b56280d5cab606838f90b381bebf15ad6356f5dec76a6397bbd0` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac57_results_v1/results.json` | `cd722b59b7ce8b8f6b6c1bf1c369f6c128935787d06db52ce07b871b84c0f826` | `cd722b59b7ce8b8f6b6c1bf1c369f6c128935787d06db52ce07b871b84c0f826` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac57_results_v1/rows.jsonl` | `7690f32f0fbf56da7b1bbe711977ceb59f7bd11c4f288042823efc2db256ead7` | `7690f32f0fbf56da7b1bbe711977ceb59f7bd11c4f288042823efc2db256ead7` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac58_results_v1/pre_run_snapshot.json` | `8cc83efaba989cdd0351ec2ea62381e86266477d5a64d02b838de3142219a37e` | `8cc83efaba989cdd0351ec2ea62381e86266477d5a64d02b838de3142219a37e` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac58_results_v1/results.json` | `2c18de844bdacc8c6ff24758c4e32d43506eb34303553f72c46098d10310dbc9` | `2c18de844bdacc8c6ff24758c4e32d43506eb34303553f72c46098d10310dbc9` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac58_results_v1/rows.jsonl` | `245b8b99c1a3899bf889353944aaa21ab3dde470ffdb8e45d8a8ed3d17cef23f` | `245b8b99c1a3899bf889353944aaa21ab3dde470ffdb8e45d8a8ed3d17cef23f` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac60_results_v1/pre_run_snapshot.json` | `12d59526ead35d4e5d1ecf79ff22be9ea6547426492620996747c592d07f048c` | `12d59526ead35d4e5d1ecf79ff22be9ea6547426492620996747c592d07f048c` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac60_results_v1/results.json` | `bf80d44fba6edb88dc0c7bcf79bae4e3d22ceeee9b6c8b355eb9226aee5240b7` | `bf80d44fba6edb88dc0c7bcf79bae4e3d22ceeee9b6c8b355eb9226aee5240b7` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac60_results_v1/rows.jsonl` | `f77be29d23e638c2aea7736d0946dece3fa6da6067802467d19668ac627be584` | `f77be29d23e638c2aea7736d0946dece3fa6da6067802467d19668ac627be584` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac67_engineering_v1/pre_run_snapshot.json` | `b7c2b81b6b861edadfb9e131c9fff66ed86d6fc2eedfccc1578c273b5ee0f1c3` | `b7c2b81b6b861edadfb9e131c9fff66ed86d6fc2eedfccc1578c273b5ee0f1c3` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac67_engineering_v1/results.json` | `b1afed2cd485c48fd3320a4c20b3636f122fe8a5b92d3040bd63527961d27df1` | `b1afed2cd485c48fd3320a4c20b3636f122fe8a5b92d3040bd63527961d27df1` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac67_engineering_v1/rows.jsonl` | `935a06a6f626c60b6d137e1e4539569aebea353c44372d023640fa83bb9af298` | `935a06a6f626c60b6d137e1e4539569aebea353c44372d023640fa83bb9af298` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac67_results_v1/pre_run_snapshot.json` | `e38876cf7d19b3e6d3b4c4c26846064242dc3405a782167c7d60301aeb05847b` | `e38876cf7d19b3e6d3b4c4c26846064242dc3405a782167c7d60301aeb05847b` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac67_results_v1/results.json` | `2561bdba6a30e4174ea9229f38f2a5cd65b411fdcd3267fe1798ed0b25d09558` | `2561bdba6a30e4174ea9229f38f2a5cd65b411fdcd3267fe1798ed0b25d09558` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac67_results_v1/rows.jsonl` | `94634f65f82704d8c5c6ee04f3cfd4b588209abd70fa32f7487d92e718005b19` | `94634f65f82704d8c5c6ee04f3cfd4b588209abd70fa32f7487d92e718005b19` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac68_engineering_v1/pre_run_snapshot.json` | `c1f8d40d89dba6adb23bf98e2252b1c168ee09b620920dce950a209d29badaaa` | `c1f8d40d89dba6adb23bf98e2252b1c168ee09b620920dce950a209d29badaaa` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac68_engineering_v1/results.json` | `0704a2e73101e842e8b306faf8e1c3b4a9f0a3e2d1c86c81bfe2c9a1346f8db6` | `0704a2e73101e842e8b306faf8e1c3b4a9f0a3e2d1c86c81bfe2c9a1346f8db6` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac68_engineering_v1/rows.jsonl` | `c0e297d77a1776b51173037b2894b87e5d24fc33a252340f1914d764645afe27` | `c0e297d77a1776b51173037b2894b87e5d24fc33a252340f1914d764645afe27` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac68_results_v1/pre_run_snapshot.json` | `01d97b55c4fabf3dcbc681c67d543a65279eb95e650634d855fba14a1e11f180` | `01d97b55c4fabf3dcbc681c67d543a65279eb95e650634d855fba14a1e11f180` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac68_results_v1/results.json` | `4fb808afb1e8dd144b255daeae1bea9bc9dcd9a7655dcdc9ec5e7a8b7695ae22` | `4fb808afb1e8dd144b255daeae1bea9bc9dcd9a7655dcdc9ec5e7a8b7695ae22` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac68_results_v1/rows.jsonl` | `832b137001c3a78911fdc3a3112e07e01bb548a134eaf5cb23b189431ebc74f4` | `832b137001c3a78911fdc3a3112e07e01bb548a134eaf5cb23b189431ebc74f4` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac71_results_v1/pre_run_snapshot.json` | `bd4d896a9856eb8a081f0c2047005c3d170e804fcf45b6c0071eb556700f8183` | `bd4d896a9856eb8a081f0c2047005c3d170e804fcf45b6c0071eb556700f8183` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac71_results_v1/results.json` | `1b6a3e350157bd9b031d564e223fa8cc1b11d40c444e4d91b86e8bf71cfcc793` | `1b6a3e350157bd9b031d564e223fa8cc1b11d40c444e4d91b86e8bf71cfcc793` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac71_results_v1/rows.jsonl` | `9afb34c9ffdd893bdcb014058b6030104e97b16360b92d149e83161facf86ca1` | `9afb34c9ffdd893bdcb014058b6030104e97b16360b92d149e83161facf86ca1` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac75_results_v1/pre_run_snapshot.json` | `8439a990afe94b9b9c45e2beaae19c5621a3b00e5bab067b2e99848ed494b29e` | `8439a990afe94b9b9c45e2beaae19c5621a3b00e5bab067b2e99848ed494b29e` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac75_results_v1/results.json` | `cbbd26ed00642d3870dedf0b52ba706fbf20b71798afd44819701a65899ee89e` | `cbbd26ed00642d3870dedf0b52ba706fbf20b71798afd44819701a65899ee89e` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac75_results_v1/rows.jsonl` | `0ebbbef600724d6a01bb94040019864ee639564933fbed0c0b374e565c43dab1` | `0ebbbef600724d6a01bb94040019864ee639564933fbed0c0b374e565c43dab1` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac76_engineering_v1/pre_run_snapshot.json` | `4907978df443b8654a3140f9f925a43d0dd1f3f9ac53e5ec63b2c7157bc43d63` | `4907978df443b8654a3140f9f925a43d0dd1f3f9ac53e5ec63b2c7157bc43d63` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac76_engineering_v1/results.json` | `9f254ed7ad2ac4f3129d960ac5751de7e744aa5840d0c1cd8fa7179862ead016` | `9f254ed7ad2ac4f3129d960ac5751de7e744aa5840d0c1cd8fa7179862ead016` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac76_engineering_v1/rows.jsonl` | `73c2fe09d952bf9e5cdc255fe60828634ffc35639abaf5fbc458882cf00e9931` | `73c2fe09d952bf9e5cdc255fe60828634ffc35639abaf5fbc458882cf00e9931` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac76_results_v1/pre_run_snapshot.json` | `157b075a0ca557939913d35be76ff41b8184531ca0bbac66944b8ef1730b78c8` | `157b075a0ca557939913d35be76ff41b8184531ca0bbac66944b8ef1730b78c8` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac76_results_v1/results.json` | `76a38109962264163679fb65caa96c66b8d99ddd7e7d1155a15f52ecf7017d80` | `76a38109962264163679fb65caa96c66b8d99ddd7e7d1155a15f52ecf7017d80` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac76_results_v1/rows.jsonl` | `aebc7da73b9114f1bc57e99a6e054a31a6f45f61f55ab5dbb43b14cf40c6d291` | `aebc7da73b9114f1bc57e99a6e054a31a6f45f61f55ab5dbb43b14cf40c6d291` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_deviation_seeds4000_v1/pre_run_snapshot.json` | `6a02086e910bef544efcbb07a34b88823cecfb0d165896218d909dfaff9c163c` | `6a02086e910bef544efcbb07a34b88823cecfb0d165896218d909dfaff9c163c` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_deviation_seeds4000_v1/results.json` | `9347297fa92117df6b41094c5660e78f6b03d4d2267f4432e6ab5f6db8ac66cc` | `9347297fa92117df6b41094c5660e78f6b03d4d2267f4432e6ab5f6db8ac66cc` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_deviation_seeds4000_v1/rows.jsonl` | `f6431dc2ac75c4e8cc8ce9514f613331ffa62a70596bb4e3202f6985c4c3ede6` | `f6431dc2ac75c4e8cc8ce9514f613331ffa62a70596bb4e3202f6985c4c3ede6` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_engineering_v1/pre_run_snapshot.json` | `b79f962b1f5f3298de2c30cf828478d26891f7903fd795f1dce90d7011cab4da` | `b79f962b1f5f3298de2c30cf828478d26891f7903fd795f1dce90d7011cab4da` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_engineering_v1/results.json` | `b2d8dcd24abb05395d0084236b0aaffa78f852d0f818b1db46d33edf5d39e0e3` | `b2d8dcd24abb05395d0084236b0aaffa78f852d0f818b1db46d33edf5d39e0e3` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_engineering_v1/rows.jsonl` | `f031e054837d8cd4f8fc737ef4b9ee9b5ad3ba2b12e75e2ebd56dc500eaa567d` | `f031e054837d8cd4f8fc737ef4b9ee9b5ad3ba2b12e75e2ebd56dc500eaa567d` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_results_v1/pre_run_snapshot.json` | `b79f962b1f5f3298de2c30cf828478d26891f7903fd795f1dce90d7011cab4da` | `b79f962b1f5f3298de2c30cf828478d26891f7903fd795f1dce90d7011cab4da` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_results_v1/results.json` | `160cb188e93b9790fabf7449ce14af7957961e984451ff069cd7ab2102de7615` | `160cb188e93b9790fabf7449ce14af7957961e984451ff069cd7ab2102de7615` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac79_results_v1/rows.jsonl` | `622a92ebce8850f9c268a7fd07703c443dc25a1d71dc9a418f3c945d4f4621e4` | `622a92ebce8850f9c268a7fd07703c443dc25a1d71dc9a418f3c945d4f4621e4` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac80_results_v1/pre_run_snapshot.json` | `ee6670f583672593a443b0d114d33c3749642417894a97db0c9b9b05fa2f1264` | `ee6670f583672593a443b0d114d33c3749642417894a97db0c9b9b05fa2f1264` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac80_results_v1/results.json` | `b4a2cad7f1cef193a1aa54efbd4247a174a8074c775fbb8cfacf0da5db7c2f70` | `b4a2cad7f1cef193a1aa54efbd4247a174a8074c775fbb8cfacf0da5db7c2f70` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |
| `ac80_results_v1/rows.jsonl` | `33e0ca85a8699e9b7f555e23569083a259f796062fed416b00cf41da29346bda` | `33e0ca85a8699e9b7f555e23569083a259f796062fed416b00cf41da29346bda` | `a6_decision_v1/baseline_hashes.json` `protected` | `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`) |

## Git-blob SHA-256 (LF), for the line-ending check

These are the SHA-256 digests of the `d0ee2bb^` git blobs before the LF-to-CRLF conversion. They are not the protected hashes. Each restored file's CRLF-to-LF conversion equals that blob.

| Path | `d0ee2bb^` blob SHA-256 (LF) | Bytes after CRLF restore |
| --- | --- | --- |
| `ac17_results_single_v1/pre_run_snapshot.json` | `afa7deeaa7df4919df34cd59650b4c1413f35e548d6a39dd9560fefc5143bd64` | 1463 |
| `ac17_results_single_v1/results.json` | `0ee4b09fdab2d5e01a7896a97153f5e6ff698a5c9ee60f75c74739c2c9fb48af` | 333247 |
| `ac17_results_single_v1/rows.jsonl` | `cb4fa3fd2f050d8fbad0581c3ee43201405a5b5b7178d9df1121a1ce845d5118` | 179736 |
| `ac18_results_v1/pre_run_snapshot.json` | `2e1d3857e56870384b469d614c11b66a75ddbcc901d3c953eecd8fc43bee1052` | 1545 |
| `ac18_results_v1/results.json` | `f5532dbdf63c05237706479b399af1e8716dd0947dfa15d23ae94602ea61b2d0` | 334035 |
| `ac18_results_v1/rows.jsonl` | `339e522442a9dc5a0a8ab44333a0dbf09e3912dadc17b2642e2734a384ed338d` | 180440 |
| `ac32_results_v1/pre_run_snapshot.json` | `78ff0754204d57fef35d1ba5f89f113cc562d9b7a288947c4b92c0ef83bcad72` | 370 |
| `ac32_results_v1/results.json` | `d72a85899d13e5bb6b76689e854e1a1813881eeca20d19fa72d46b070201d8f6` | 15070 |
| `ac32_results_v1/rows.jsonl` | `4a41c9b4ff1414eab10fe6ea2f01c2eaa9cc5159d87b6e102a40b4a358eadbd2` | 5144 |
| `ac33_results_v1/pre_run_snapshot.json` | `81fd54471f5f89d8a8db25e73a60c3e170f0bf3d2504a6af617284b6408fc587` | 551 |
| `ac33_results_v1/results.json` | `e5e698406c1ae59633f8d14e32e2325206633a1439f968002e7d8c8d2f83fcd1` | 15187 |
| `ac33_results_v1/rows.jsonl` | `cef4effe7cac18d51d4ae7412abfaf07c6ecbf661554fb2c2fcfe80ad50211b5` | 5065 |
| `ac36_results_v1/pre_run_snapshot.json` | `6928c8758c87e63afe2f81c2df118c41070bfd5e9bb1f8ef015016ce45ad18b3` | 550 |
| `ac36_results_v1/results.json` | `5d4df172bb90cd8b67378314317a24fc69e973160fd17c16b6334073bab09108` | 14925 |
| `ac36_results_v1/rows.jsonl` | `9c33f4206249066e182b78c4c3b0ccb5dda4c804291a33019cfcd2994ba5f4db` | 4914 |
| `ac43_results_v1/pre_run_snapshot.json` | `34e578a8d50b97bef05792ab56a5f29849d971f320852d3cdec9f45ffc9661f4` | 363 |
| `ac43_results_v1/results.json` | `12c14e06c765b8a4623ab695a0e46d377c3859cbeab70b5a02f4422ba41487a5` | 3171 |
| `ac43_results_v1/rows.jsonl` | `bec095aa599469485ae54c3593d37db6c8c42aa9d241b078388bb0e000080056` | 1610 |
| `ac45_results_v1/pre_run_snapshot.json` | `0259fa3e2f70c3eb13a8d081d41b9784a189d1f858626c80ec5290fdb00518af` | 359 |
| `ac45_results_v1/results.json` | `4d1e4a0fc2233f368bafd12893e705fce77dd7da4ee91a1c09b2670245d5b768` | 9285 |
| `ac45_results_v1/rows.jsonl` | `8c3933b787ece7a2cecd56edfd0a48e017e601c8516ab8ba85daa7f8b2e515e7` | 6090 |
| `ac46_results_v1/pre_run_snapshot.json` | `b1b3a840b50633d25d1e1e53d13b51d466d0f1dcb7a112b8edbb1752be724e8e` | 556 |
| `ac46_results_v1/results.json` | `daf7f43264c5f7218b27cd6851c5c9a24bf67474b82c819a38c9ac1cb810ede7` | 15150 |
| `ac46_results_v1/rows.jsonl` | `f7d7ebd9085bfe94ccf6d1496d231b8f6ca40cfde3bb6ca3ddfb8b2bd7183b63` | 4858 |
| `ac50_results_v1/pre_run_snapshot.json` | `d07fd53f72dadb251f2f2c3f0be76eeb255cac9457cd23e4161e663b1c500722` | 554 |
| `ac50_results_v1/results.json` | `2fa8c67f988972730c938296b381e3e10e465a82078aa1188ffc9d06587ba40d` | 16887 |
| `ac50_results_v1/rows.jsonl` | `e754e5022cc44d92611a415433b914bd9389bae29ba52f469558e57a12b71fec` | 5689 |
| `ac54_results_v1/pre_run_snapshot.json` | `36f1c53ed15c52b78a1ae261927dfff5337896de955f01f6d5bd3205af44b622` | 645 |
| `ac54_results_v1/results.json` | `281549ba64da242bcceae48c3239a7084a00964fd4f484d0630b649ef277d25c` | 6543 |
| `ac54_results_v1/rows.jsonl` | `8cdede5eadc0cebe953c5d1605376d462f8c125c841ead8eea8cd4dfe4a2c600` | 2316 |
| `ac55_results_v1/pre_run_snapshot.json` | `e0b270e25392a1a0d489c93a751bb25f1a54409346d3c1365bb7ec6c5b06382b` | 645 |
| `ac55_results_v1/results.json` | `2b744d7fa66cf64dbcbf829d7c43a0f32e3cc63a7e20fa79f350dbf0d72ce5f8` | 6724 |
| `ac55_results_v1/rows.jsonl` | `2ca4731cb311930cd49a557253dead734a7569c19c474c6d6c3b522149f71038` | 2352 |
| `ac57_results_v1/pre_run_snapshot.json` | `3a2a7e88a2f6f68d17988b543edcc434f6c28d3f06e15e0ac090b48bea5710ce` | 736 |
| `ac57_results_v1/results.json` | `c2b181d95a9ebfad061d707ad079d6beb63c6e72af73cb1997d22a3bdf30251f` | 9413 |
| `ac57_results_v1/rows.jsonl` | `52702659ab2d54bd35a62e6d820c4203d9d4119d5094e500ca0ea596a3d6b0de` | 3576 |
| `ac58_results_v1/pre_run_snapshot.json` | `903cc7c5e109feb415ac11c7d96f440ca9ce3940cefba03139580295725869f9` | 647 |
| `ac58_results_v1/results.json` | `e8074d87730c92991888417393a7e338aca7bb6282ce21c4a8e23c900a6bbe32` | 5403 |
| `ac58_results_v1/rows.jsonl` | `c97a69b7235ef49f626df5810f62abb9468daabd880c33b61c8212ca79c36f54` | 2025 |
| `ac60_results_v1/pre_run_snapshot.json` | `83353d7939cfc080543f4b41f71abce4b822f56c04d26637e80ccdac1746054f` | 370 |
| `ac60_results_v1/results.json` | `f54a2515ac219a1336d12d658fc5febb3bd812f97b5ce6d0d5728596f0526f6e` | 9191 |
| `ac60_results_v1/rows.jsonl` | `4126fa58ecebd9a11580aca1c664db3ae47667500663a315fd80a076787a3a5a` | 3612 |
| `ac67_engineering_v1/pre_run_snapshot.json` | `859b904886f308cf14bafd51349f19e4482501f06193e67013859df205093c24` | 941 |
| `ac67_engineering_v1/results.json` | `d9ec2bb81c1cff36e8554810db56a91e2928cebdbe8f7813bc6c937c5879b45f` | 41137 |
| `ac67_engineering_v1/rows.jsonl` | `bca1e33cc2287a21a900cf7ef0a732a1f19225387595090726458db013cd05d7` | 25034 |
| `ac67_results_v1/pre_run_snapshot.json` | `8110bd1fdcff241bb96bf275cedac80200a57d1a208f2e813f4e08fbe2839b9b` | 1035 |
| `ac67_results_v1/results.json` | `76815080fca2ce149218ae3cf9adae81c3ff614f965fb522d8031360b6e7c7a1` | 54741 |
| `ac67_results_v1/rows.jsonl` | `27b9cc0c29b65af328afb01156f8df5e0fb81d063a834564462b54e507676ac1` | 33490 |
| `ac68_engineering_v1/pre_run_snapshot.json` | `4f6a278a10d0c8b7d34ae7a72433ffcad79b19a2fd0e7e612a43160022ad1ba0` | 941 |
| `ac68_engineering_v1/results.json` | `0b1bfdb6a1d8957febb4069988c82b0fe1e5c74066d1f3ae43f9bbcd0a083c25` | 5963 |
| `ac68_engineering_v1/rows.jsonl` | `fb2c6024352a45e0fe7da0d4d478bfe24d020f5e6fcb27e69b6312e4a96a645a` | 2970 |
| `ac68_results_v1/pre_run_snapshot.json` | `686339ca3072384550ef253466c0b76e75ab63a80f9bf772b2e8565e5c740490` | 1035 |
| `ac68_results_v1/results.json` | `0e8fe8bbe67e62d422db263369313451672713437962c805b100f6b5a1929fe0` | 7793 |
| `ac68_results_v1/rows.jsonl` | `eae103410374c1664ffa5298ccc5cc6573d7b83ea7bf55d03e8aaffb15b7c8ed` | 4040 |
| `ac71_results_v1/pre_run_snapshot.json` | `dd1d93d48a68e179fdc23d1a97d5bf05f2e36e6281929c7c507f0e8f98335caa` | 1035 |
| `ac71_results_v1/results.json` | `0ef9091c9f21bf0347aee03cc07926456a55f9134c9eeec148379cb76783c447` | 13629 |
| `ac71_results_v1/rows.jsonl` | `7a5cba288f92bfeb459e74650b8b9feedce589355f14d05979e14ae7935e16d4` | 7476 |
| `ac75_results_v1/pre_run_snapshot.json` | `d5224fa44b4f2179af7472cf22bc841ff80efd474c07da32b8520c3280f5639b` | 1035 |
| `ac75_results_v1/results.json` | `1d2780ca84230cf3e9ab828767b07ba86458e05540fd2891e86067897c0c85d0` | 108171 |
| `ac75_results_v1/rows.jsonl` | `37b30b2010724a7b8f4b73b1de29c76f0e2e350fc740b1d44d81ca437053318c` | 66786 |
| `ac76_engineering_v1/pre_run_snapshot.json` | `6acfad47df32cb93f988749faa25cfaedc670bf0a31441c2454ccadb1b73694d` | 1035 |
| `ac76_engineering_v1/results.json` | `623d3a6733e92dd359fd1126fb4a9d4815f2c7aa9ed5796acca94e636fb14f98` | 24873 |
| `ac76_engineering_v1/rows.jsonl` | `f98344f6f489c4790c64d8d094b8d1002d6f6d2acc30fca43073dc3c942796f8` | 14748 |
| `ac76_results_v1/pre_run_snapshot.json` | `c1059e0fcf428da8811aa2e0e35a91040622bb0144a4d59e20ed743bcd25e506` | 1035 |
| `ac76_results_v1/results.json` | `f66ac26a474961b092cd794d82909b6d2ea46027e0ffda1a17e3c525632ba44d` | 32881 |
| `ac76_results_v1/rows.jsonl` | `01b435362e6a36b0906e30eaacec056190cfb9522627dd92fe9b64d0688c3962` | 19808 |
| `ac79_deviation_seeds4000_v1/pre_run_snapshot.json` | `c5d2c8a7cca0303c7df188898551b1a3476f1e871257582de0a33710f8efc8da` | 1199 |
| `ac79_deviation_seeds4000_v1/results.json` | `cee055e9773aae793730e59735bfc795b438e2ab9aca9d3e3e492475a39e3b85` | 55822 |
| `ac79_deviation_seeds4000_v1/rows.jsonl` | `8e757d072e5b306a062775afc4d11d9d9e0c168b6f28ef36b66f49962590baae` | 35950 |
| `ac79_engineering_v1/pre_run_snapshot.json` | `95ac41ceb0116192dadad97614d6c4a63b3dc873813d7be67586dcf5dc0267f6` | 1199 |
| `ac79_engineering_v1/results.json` | `7220f98e9e478c5d9e1defb07015a523357b05ac9d762e43f5579b0673ee3bca` | 109557 |
| `ac79_engineering_v1/rows.jsonl` | `8913b20c007a340326b3717ae5327d7be873751c8798a3a42bb8b32d5c38a6b8` | 71362 |
| `ac79_results_v1/pre_run_snapshot.json` | `95ac41ceb0116192dadad97614d6c4a63b3dc873813d7be67586dcf5dc0267f6` | 1199 |
| `ac79_results_v1/results.json` | `1f6e20eedd283e45c13363b9318316c37f2ab1507ad77edef900a050dad920e8` | 55805 |
| `ac79_results_v1/rows.jsonl` | `11ca88a17aaab3cb3ee97484b895b988f610ecfe34a8f8c2044c87056c9aba2a` | 35934 |
| `ac80_results_v1/pre_run_snapshot.json` | `7d754fde55dba5e9557c4049a83f789c6b5714d87b7216de6f6a4432ed93e825` | 1199 |
| `ac80_results_v1/results.json` | `2fcb11c8c6d558969d0b9bffef1c246306eb369e6db82f0898b2ae6610ab9690` | 58391 |
| `ac80_results_v1/rows.jsonl` | `58f7be836effd7a4b8cf744e1866f98fc2e84a970c158041762d10b697cacc8e` | 38070 |

Restored file count: 78. Total restored bytes: 2148331.
