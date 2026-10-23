# Recovery manifest d0ee2bb v1

Additive record only. No frozen file, protocol, result, errata, ledger, kanban, or README was edited. `.gitignore` was not changed.

On 2026-10-20 the repository owner approved restoring the 78 frozen result files deleted by commit `d0ee2bb46e3a6ec3d80be2b9ec6f53d9a1e7a89e` (2026-10-02, "Remove large result files and snapshots from multiple versions").

## Source

- Restored from commit `3397308bdb0e386a79c768b224c7ad7639bf896f` (`d0ee2bb^`). Each path below is that commit's git blob, with the same blob SHA. Those blobs are also the objects present at A6 inventory head `370685b4ea44c26b16f3bbb49e3e8011c9cc269e`.
- Git stores every one of these blobs with LF line endings, the same way it stores the rest of the repository. The committed bytes are those LF blobs.
- Protected hashes live in `a6_decision_v1/baseline_hashes.json`, object `protected` (7,326 entries, schema 1). They were taken from a CRLF working-tree checkout. The checker is `a6_decision_v1/preservation.py` (`python -B -m a6_decision_v1.preservation a6_decision_v1/baseline_hashes.json --check`). It hashes working-tree bytes with SHA-256 and does not normalize line endings.
- The preservation check therefore depends on checkout line endings. On a CRLF checkout, replacing each LF in the blob with CRLF reproduces the protected hash, the same way it does for every other inventoried file. On an LF checkout the checker reports a line-ending mismatch for these 78 files, just as it does for the other files whose inventory entries were recorded from CRLF bytes. That mismatch is the checkout convention, not a different blob.

## Approval

- Owner approval date: 2026-10-20

## Restored files

The git blob SHA is the object id at `d0ee2bb^` and in this restore. The LF SHA-256 is the digest of that blob. The CRLF-normalized SHA-256 is the digest after replacing each LF with CRLF, and it equals the `protected` entry in `a6_decision_v1/baseline_hashes.json`.

| Path | Git blob SHA | LF SHA-256 | CRLF-normalized SHA-256 |
| --- | --- | --- | --- |
| `ac17_results_single_v1/pre_run_snapshot.json` | `ef86d4274176360cc0282382a041452f72ba17c2` | `afa7deeaa7df4919df34cd59650b4c1413f35e548d6a39dd9560fefc5143bd64` | `b6f87da47cb7f6b005e06d8df4c372ebea243171f4c082dc188b9dabfa9094dd` |
| `ac17_results_single_v1/results.json` | `49bc8276df9fa0e13a074b3672370739b8756f37` | `0ee4b09fdab2d5e01a7896a97153f5e6ff698a5c9ee60f75c74739c2c9fb48af` | `e68030862fdff6280f39e2ca7185378be4d55bac38e05e8d2ea8a53c2001e168` |
| `ac17_results_single_v1/rows.jsonl` | `c67d0d2d2173ba832e239b92a20b6ff8b1c0ef52` | `cb4fa3fd2f050d8fbad0581c3ee43201405a5b5b7178d9df1121a1ce845d5118` | `88f1feceb0ec4296c5db720dd6867ed6b8effbdce0bddbfb3c479e0c9d5ebeb0` |
| `ac18_results_v1/pre_run_snapshot.json` | `0a633a7545c6c2ea06ffbd91454aeed0f251dea0` | `2e1d3857e56870384b469d614c11b66a75ddbcc901d3c953eecd8fc43bee1052` | `7a506426ea0cbea3cecbb298c50bc12920eeffb8bf67c7c1996fb0bd652e4618` |
| `ac18_results_v1/results.json` | `51d944703d3ec0a4a6b888f764b16eedf958f46d` | `f5532dbdf63c05237706479b399af1e8716dd0947dfa15d23ae94602ea61b2d0` | `14d009a6e54b670f20bbe7437a6aa63f06c1f303f149882d0fa847408f6b5ff6` |
| `ac18_results_v1/rows.jsonl` | `b00d77d730c6f2efa2d9316ab7db94ba62244680` | `339e522442a9dc5a0a8ab44333a0dbf09e3912dadc17b2642e2734a384ed338d` | `56f940c603c606ca9c8c483f03ef32d32b1f41c1e216c6ce8b66ff940815daa5` |
| `ac32_results_v1/pre_run_snapshot.json` | `727957382c990ead6acf270a9b002644b2d48ae1` | `78ff0754204d57fef35d1ba5f89f113cc562d9b7a288947c4b92c0ef83bcad72` | `ca1d76845d9ac922b991dcbeb3502ec89c994fe01794bbe0933ff297ba1fd3c6` |
| `ac32_results_v1/results.json` | `e062433471d8dd1e5b33ea417b330a1407ecbcdf` | `d72a85899d13e5bb6b76689e854e1a1813881eeca20d19fa72d46b070201d8f6` | `25e30c091b0a116c656e95125ba72aa32df17ba6cc55f99a215e6ca9b4f79590` |
| `ac32_results_v1/rows.jsonl` | `d99415e60334c200187f2f1ae307e95ca0d87a2a` | `4a41c9b4ff1414eab10fe6ea2f01c2eaa9cc5159d87b6e102a40b4a358eadbd2` | `7eb748030552991d73e54056702c5163614bfb01d351395a2a5a883cff142d23` |
| `ac33_results_v1/pre_run_snapshot.json` | `3656daa2dc306cef85806f303eef20dddb4af354` | `81fd54471f5f89d8a8db25e73a60c3e170f0bf3d2504a6af617284b6408fc587` | `cc7c15007565e12ac309e6034da6729f2a3de969a6f6cee0ccbf1d909df2d3f4` |
| `ac33_results_v1/results.json` | `737fe979a68b32c51e9a5ddafba5471cb1c54961` | `e5e698406c1ae59633f8d14e32e2325206633a1439f968002e7d8c8d2f83fcd1` | `65235869ab9ecbb8ced4647ec5c3cd01fe2efd3d5f032c37cefcc62db62676df` |
| `ac33_results_v1/rows.jsonl` | `cf05a8d61e1c3050f00d41d6159c51f93e04700e` | `cef4effe7cac18d51d4ae7412abfaf07c6ecbf661554fb2c2fcfe80ad50211b5` | `1a5833e3b189b93773a57b8c4c33b1229de375fec18d66d0bf933f4bebf2933a` |
| `ac36_results_v1/pre_run_snapshot.json` | `e72ef529907b036567712269905ae290cd8dec20` | `6928c8758c87e63afe2f81c2df118c41070bfd5e9bb1f8ef015016ce45ad18b3` | `65a5d75853412871a3b65f32944ebdb8fbc8858dbf0d9225c94fcd1244ea61f6` |
| `ac36_results_v1/results.json` | `75b62d476e535d181c2149b8943af6cbd5c8f9d6` | `5d4df172bb90cd8b67378314317a24fc69e973160fd17c16b6334073bab09108` | `0b7cf522a083a82fdbc435065bd7556092641eba425630c9ce34b91fbfed86f3` |
| `ac36_results_v1/rows.jsonl` | `c01cb1566878534bfba2b68050b54424fac8ba05` | `9c33f4206249066e182b78c4c3b0ccb5dda4c804291a33019cfcd2994ba5f4db` | `0184e5c2dc2fd96ef5ee04f3bf355a7350361e7870998be5608187ad5ab7935d` |
| `ac43_results_v1/pre_run_snapshot.json` | `f17f2cb96e95628b04581ec34971b1efca3283f3` | `34e578a8d50b97bef05792ab56a5f29849d971f320852d3cdec9f45ffc9661f4` | `985fada6b8ba15311467d273a68b3d856ccdbdb1763b04e2fd3fd7af68dcb8a3` |
| `ac43_results_v1/results.json` | `37543b21536136d2b779e0a668319dfd4222c383` | `12c14e06c765b8a4623ab695a0e46d377c3859cbeab70b5a02f4422ba41487a5` | `e02d478dafbfb13db0152265758baf56e622db0d7169c666b78190fa5566cc09` |
| `ac43_results_v1/rows.jsonl` | `ba6995ffcea18f7fa21c7b6e7557df73329eb246` | `bec095aa599469485ae54c3593d37db6c8c42aa9d241b078388bb0e000080056` | `b7e487294a5a954101b54c6e3e3da204052dda444e1fdbe8d3a68a6e9226b496` |
| `ac45_results_v1/pre_run_snapshot.json` | `f695c9a13d450e7d6a926685735ea79041e7c14f` | `0259fa3e2f70c3eb13a8d081d41b9784a189d1f858626c80ec5290fdb00518af` | `4be20ca33a774123bdcf21ce74b7932c392712ca2231cf4eb00aa425b1ef9158` |
| `ac45_results_v1/results.json` | `3c0dcb196f9fc2768e667468dd6dc29c232bc5e9` | `4d1e4a0fc2233f368bafd12893e705fce77dd7da4ee91a1c09b2670245d5b768` | `6a080e4acd96b40f4c83a096d088cdada2fcb7b751f34eee48c2a056960a361e` |
| `ac45_results_v1/rows.jsonl` | `360c8d47d5ae08e2cddf4abc13695c966ca82e7e` | `8c3933b787ece7a2cecd56edfd0a48e017e601c8516ab8ba85daa7f8b2e515e7` | `b181ebdf0689b1f30a5b69d4c01e51461dcead1d7235c3327a022ad3b522ef4b` |
| `ac46_results_v1/pre_run_snapshot.json` | `9e743df71af9040e722d8e62f04da3c62c7b96d8` | `b1b3a840b50633d25d1e1e53d13b51d466d0f1dcb7a112b8edbb1752be724e8e` | `a1cfc2a86fbca4c07640f8915ef90449241eada67bafe3a37745568c4d19e4e4` |
| `ac46_results_v1/results.json` | `7fd603955de0a279a277e269e18477115db2e176` | `daf7f43264c5f7218b27cd6851c5c9a24bf67474b82c819a38c9ac1cb810ede7` | `c718d763e6192a0c58f2a0ff51d85f466c49e703680c4344199038cac8e96c4c` |
| `ac46_results_v1/rows.jsonl` | `3a700bd6964c789b0266b75b913214381c2d322b` | `f7d7ebd9085bfe94ccf6d1496d231b8f6ca40cfde3bb6ca3ddfb8b2bd7183b63` | `306fea945f5c652bc18525bd9ec68826a620f201790ca16508349e05809eef82` |
| `ac50_results_v1/pre_run_snapshot.json` | `a260b0960834cb47209b290552c884b8c7206890` | `d07fd53f72dadb251f2f2c3f0be76eeb255cac9457cd23e4161e663b1c500722` | `8837378bb4c7e9a28286b80e5fac717d7d5ec80f1031629bb7d22c929b9a5427` |
| `ac50_results_v1/results.json` | `9ece745e7c52296942e26d49bc4d6fa47589f900` | `2fa8c67f988972730c938296b381e3e10e465a82078aa1188ffc9d06587ba40d` | `ec25074a208b79db347526ddf8e3e4c4737677e58e3c53a263ea8d5f0eeba861` |
| `ac50_results_v1/rows.jsonl` | `0ac4bc8237e6e0500ff7aa35471dc0303216a16a` | `e754e5022cc44d92611a415433b914bd9389bae29ba52f469558e57a12b71fec` | `d501ce5f447b6f43162018f635d1fb740ad3a2729701bf3dd4fc6f31bf9a2ec8` |
| `ac54_results_v1/pre_run_snapshot.json` | `12a7d384cee85a4fc130806f1e38af9b556dbedb` | `36f1c53ed15c52b78a1ae261927dfff5337896de955f01f6d5bd3205af44b622` | `b68383c19bc51b54a068bac29d467894497f0a0dea5d1247bc73b0bb9aa8ee29` |
| `ac54_results_v1/results.json` | `269a56929b9946c95fb09ca61131a6b2824139d4` | `281549ba64da242bcceae48c3239a7084a00964fd4f484d0630b649ef277d25c` | `ca1442ebe66e37d88a286d8793056c9f193d8ead7d11f96923bb45158ef8aded` |
| `ac54_results_v1/rows.jsonl` | `01a9b6ae277c80bf24779e0f0b5a946fb54b3910` | `8cdede5eadc0cebe953c5d1605376d462f8c125c841ead8eea8cd4dfe4a2c600` | `e9e32d3558d666ab4215dea251c4fc4b9b5080d2a8f5f11ee08a1ad15e9fdcdc` |
| `ac55_results_v1/pre_run_snapshot.json` | `dd08c0eb453f889192225eff0e057b6bd356ce17` | `e0b270e25392a1a0d489c93a751bb25f1a54409346d3c1365bb7ec6c5b06382b` | `8f86dc848ebd6bc2839c0b713f59af01adfba1851d930b6870d278f5fce42ff1` |
| `ac55_results_v1/results.json` | `191f9cd764c7fa8e535047790cbdc086c3429df3` | `2b744d7fa66cf64dbcbf829d7c43a0f32e3cc63a7e20fa79f350dbf0d72ce5f8` | `c026b28b9ab12eec64feff9d104d6f69a2a5a2e877e6ac62886c12c669dc06e4` |
| `ac55_results_v1/rows.jsonl` | `9bb5e065a9bf74a9e022daf85ef34a97ff423330` | `2ca4731cb311930cd49a557253dead734a7569c19c474c6d6c3b522149f71038` | `74bb9badd75b098a219109bc0ba76b6e4e4549f342c9fa6af7bca49768fc5b74` |
| `ac57_results_v1/pre_run_snapshot.json` | `df4844660a5bdd66f04bab8d1d34add847a271e3` | `3a2a7e88a2f6f68d17988b543edcc434f6c28d3f06e15e0ac090b48bea5710ce` | `c74c4b433c69b56280d5cab606838f90b381bebf15ad6356f5dec76a6397bbd0` |
| `ac57_results_v1/results.json` | `513c5b73fa6a77bd6e5fe146820d2f6ee0b22873` | `c2b181d95a9ebfad061d707ad079d6beb63c6e72af73cb1997d22a3bdf30251f` | `cd722b59b7ce8b8f6b6c1bf1c369f6c128935787d06db52ce07b871b84c0f826` |
| `ac57_results_v1/rows.jsonl` | `25006130ed08b342cd806d00d8c3743196f238e8` | `52702659ab2d54bd35a62e6d820c4203d9d4119d5094e500ca0ea596a3d6b0de` | `7690f32f0fbf56da7b1bbe711977ceb59f7bd11c4f288042823efc2db256ead7` |
| `ac58_results_v1/pre_run_snapshot.json` | `5dbb7dcec13fa59a5c40a62e87c02162c0bbe1d4` | `903cc7c5e109feb415ac11c7d96f440ca9ce3940cefba03139580295725869f9` | `8cc83efaba989cdd0351ec2ea62381e86266477d5a64d02b838de3142219a37e` |
| `ac58_results_v1/results.json` | `e8d07a4d54bbf892b492284acc07cc0e10c60b8f` | `e8074d87730c92991888417393a7e338aca7bb6282ce21c4a8e23c900a6bbe32` | `2c18de844bdacc8c6ff24758c4e32d43506eb34303553f72c46098d10310dbc9` |
| `ac58_results_v1/rows.jsonl` | `c5ea8ff221b27895520449cb8cecf9353ce0fe66` | `c97a69b7235ef49f626df5810f62abb9468daabd880c33b61c8212ca79c36f54` | `245b8b99c1a3899bf889353944aaa21ab3dde470ffdb8e45d8a8ed3d17cef23f` |
| `ac60_results_v1/pre_run_snapshot.json` | `d7bc24c8fe88d8129af018f805ce8a4494f6015b` | `83353d7939cfc080543f4b41f71abce4b822f56c04d26637e80ccdac1746054f` | `12d59526ead35d4e5d1ecf79ff22be9ea6547426492620996747c592d07f048c` |
| `ac60_results_v1/results.json` | `bec942542097242ba213da67b1586cc4819f4039` | `f54a2515ac219a1336d12d658fc5febb3bd812f97b5ce6d0d5728596f0526f6e` | `bf80d44fba6edb88dc0c7bcf79bae4e3d22ceeee9b6c8b355eb9226aee5240b7` |
| `ac60_results_v1/rows.jsonl` | `43360204dd80739f1fefb3f9908dea0ada01d40d` | `4126fa58ecebd9a11580aca1c664db3ae47667500663a315fd80a076787a3a5a` | `f77be29d23e638c2aea7736d0946dece3fa6da6067802467d19668ac627be584` |
| `ac67_engineering_v1/pre_run_snapshot.json` | `2ac8dea047e3a45c07f4cbf0cb025b5fd73bd66d` | `859b904886f308cf14bafd51349f19e4482501f06193e67013859df205093c24` | `b7c2b81b6b861edadfb9e131c9fff66ed86d6fc2eedfccc1578c273b5ee0f1c3` |
| `ac67_engineering_v1/results.json` | `e3896292c284735b6be8373ff0928cbefd058e24` | `d9ec2bb81c1cff36e8554810db56a91e2928cebdbe8f7813bc6c937c5879b45f` | `b1afed2cd485c48fd3320a4c20b3636f122fe8a5b92d3040bd63527961d27df1` |
| `ac67_engineering_v1/rows.jsonl` | `0ea485c2abbdd1637467635aad94feae319ef23e` | `bca1e33cc2287a21a900cf7ef0a732a1f19225387595090726458db013cd05d7` | `935a06a6f626c60b6d137e1e4539569aebea353c44372d023640fa83bb9af298` |
| `ac67_results_v1/pre_run_snapshot.json` | `99f7b33b88b9ce27ba0a1c251ab02d255877f1e8` | `8110bd1fdcff241bb96bf275cedac80200a57d1a208f2e813f4e08fbe2839b9b` | `e38876cf7d19b3e6d3b4c4c26846064242dc3405a782167c7d60301aeb05847b` |
| `ac67_results_v1/results.json` | `91046b6387cb50c426da5555bf2975965e866793` | `76815080fca2ce149218ae3cf9adae81c3ff614f965fb522d8031360b6e7c7a1` | `2561bdba6a30e4174ea9229f38f2a5cd65b411fdcd3267fe1798ed0b25d09558` |
| `ac67_results_v1/rows.jsonl` | `ddb4bf7a6d006f9e7060a0c8aea93e5f6e44f2ee` | `27b9cc0c29b65af328afb01156f8df5e0fb81d063a834564462b54e507676ac1` | `94634f65f82704d8c5c6ee04f3cfd4b588209abd70fa32f7487d92e718005b19` |
| `ac68_engineering_v1/pre_run_snapshot.json` | `aa5df487f4c0690850cc40423920aef35d119883` | `4f6a278a10d0c8b7d34ae7a72433ffcad79b19a2fd0e7e612a43160022ad1ba0` | `c1f8d40d89dba6adb23bf98e2252b1c168ee09b620920dce950a209d29badaaa` |
| `ac68_engineering_v1/results.json` | `ba913081c11585952bf5f7256e5aee2aef2c632a` | `0b1bfdb6a1d8957febb4069988c82b0fe1e5c74066d1f3ae43f9bbcd0a083c25` | `0704a2e73101e842e8b306faf8e1c3b4a9f0a3e2d1c86c81bfe2c9a1346f8db6` |
| `ac68_engineering_v1/rows.jsonl` | `5d550445f17cce102c8c0d6893be9eccc6047689` | `fb2c6024352a45e0fe7da0d4d478bfe24d020f5e6fcb27e69b6312e4a96a645a` | `c0e297d77a1776b51173037b2894b87e5d24fc33a252340f1914d764645afe27` |
| `ac68_results_v1/pre_run_snapshot.json` | `8b5da5fdcc8927797628313cb61b5f3b4a7df67f` | `686339ca3072384550ef253466c0b76e75ab63a80f9bf772b2e8565e5c740490` | `01d97b55c4fabf3dcbc681c67d543a65279eb95e650634d855fba14a1e11f180` |
| `ac68_results_v1/results.json` | `b9d3da27fa6f853d981a0a4b8d8d6244dfe386ab` | `0e8fe8bbe67e62d422db263369313451672713437962c805b100f6b5a1929fe0` | `4fb808afb1e8dd144b255daeae1bea9bc9dcd9a7655dcdc9ec5e7a8b7695ae22` |
| `ac68_results_v1/rows.jsonl` | `17bda2b36da0c5e359ccdd338e9bc1fa7b5fedd6` | `eae103410374c1664ffa5298ccc5cc6573d7b83ea7bf55d03e8aaffb15b7c8ed` | `832b137001c3a78911fdc3a3112e07e01bb548a134eaf5cb23b189431ebc74f4` |
| `ac71_results_v1/pre_run_snapshot.json` | `54ef361e4040732f3aa08d270dbfdaf59fbebad3` | `dd1d93d48a68e179fdc23d1a97d5bf05f2e36e6281929c7c507f0e8f98335caa` | `bd4d896a9856eb8a081f0c2047005c3d170e804fcf45b6c0071eb556700f8183` |
| `ac71_results_v1/results.json` | `29623d077a08f1b226fadee79f8533fc983edbf0` | `0ef9091c9f21bf0347aee03cc07926456a55f9134c9eeec148379cb76783c447` | `1b6a3e350157bd9b031d564e223fa8cc1b11d40c444e4d91b86e8bf71cfcc793` |
| `ac71_results_v1/rows.jsonl` | `5b1fbb12a552480104e29b4ccb235e7f15c5cd5d` | `7a5cba288f92bfeb459e74650b8b9feedce589355f14d05979e14ae7935e16d4` | `9afb34c9ffdd893bdcb014058b6030104e97b16360b92d149e83161facf86ca1` |
| `ac75_results_v1/pre_run_snapshot.json` | `f54aa1a919775fca6b3d24a58bdc15b1e60c09b9` | `d5224fa44b4f2179af7472cf22bc841ff80efd474c07da32b8520c3280f5639b` | `8439a990afe94b9b9c45e2beaae19c5621a3b00e5bab067b2e99848ed494b29e` |
| `ac75_results_v1/results.json` | `dc8af89f843b3bd426027d427dbe9f70596da35c` | `1d2780ca84230cf3e9ab828767b07ba86458e05540fd2891e86067897c0c85d0` | `cbbd26ed00642d3870dedf0b52ba706fbf20b71798afd44819701a65899ee89e` |
| `ac75_results_v1/rows.jsonl` | `c2221619132fc00fad4055f293b2b9eae27d3706` | `37b30b2010724a7b8f4b73b1de29c76f0e2e350fc740b1d44d81ca437053318c` | `0ebbbef600724d6a01bb94040019864ee639564933fbed0c0b374e565c43dab1` |
| `ac76_engineering_v1/pre_run_snapshot.json` | `1ae034be3860c98739167fc40ba7a837656a31fb` | `6acfad47df32cb93f988749faa25cfaedc670bf0a31441c2454ccadb1b73694d` | `4907978df443b8654a3140f9f925a43d0dd1f3f9ac53e5ec63b2c7157bc43d63` |
| `ac76_engineering_v1/results.json` | `45c09a2c4523a3fbb203f9ab018e7a7b83e49aab` | `623d3a6733e92dd359fd1126fb4a9d4815f2c7aa9ed5796acca94e636fb14f98` | `9f254ed7ad2ac4f3129d960ac5751de7e744aa5840d0c1cd8fa7179862ead016` |
| `ac76_engineering_v1/rows.jsonl` | `d441912b920abf4b7536e5d701f79706e1e8d468` | `f98344f6f489c4790c64d8d094b8d1002d6f6d2acc30fca43073dc3c942796f8` | `73c2fe09d952bf9e5cdc255fe60828634ffc35639abaf5fbc458882cf00e9931` |
| `ac76_results_v1/pre_run_snapshot.json` | `018deecf7172ab6ac553ab8fd1e8df28cfb20e4f` | `c1059e0fcf428da8811aa2e0e35a91040622bb0144a4d59e20ed743bcd25e506` | `157b075a0ca557939913d35be76ff41b8184531ca0bbac66944b8ef1730b78c8` |
| `ac76_results_v1/results.json` | `2f1f9e0239f511de1ceaf062c4b9a0d5b148e3a0` | `f66ac26a474961b092cd794d82909b6d2ea46027e0ffda1a17e3c525632ba44d` | `76a38109962264163679fb65caa96c66b8d99ddd7e7d1155a15f52ecf7017d80` |
| `ac76_results_v1/rows.jsonl` | `06d7b0841997d6d82515b87e861534524a6f813d` | `01b435362e6a36b0906e30eaacec056190cfb9522627dd92fe9b64d0688c3962` | `aebc7da73b9114f1bc57e99a6e054a31a6f45f61f55ab5dbb43b14cf40c6d291` |
| `ac79_deviation_seeds4000_v1/pre_run_snapshot.json` | `ee56853d61fa32bcdbd7d8c1d3b530bcef836131` | `c5d2c8a7cca0303c7df188898551b1a3476f1e871257582de0a33710f8efc8da` | `6a02086e910bef544efcbb07a34b88823cecfb0d165896218d909dfaff9c163c` |
| `ac79_deviation_seeds4000_v1/results.json` | `6584492a73669b410b6ad03fc37148f561ba6699` | `cee055e9773aae793730e59735bfc795b438e2ab9aca9d3e3e492475a39e3b85` | `9347297fa92117df6b41094c5660e78f6b03d4d2267f4432e6ab5f6db8ac66cc` |
| `ac79_deviation_seeds4000_v1/rows.jsonl` | `144fa54fe248bad2a77b5616f3b6f54f10d7139f` | `8e757d072e5b306a062775afc4d11d9d9e0c168b6f28ef36b66f49962590baae` | `f6431dc2ac75c4e8cc8ce9514f613331ffa62a70596bb4e3202f6985c4c3ede6` |
| `ac79_engineering_v1/pre_run_snapshot.json` | `82e1abd7cac5b54257cb22babab8f47f12bce06b` | `95ac41ceb0116192dadad97614d6c4a63b3dc873813d7be67586dcf5dc0267f6` | `b79f962b1f5f3298de2c30cf828478d26891f7903fd795f1dce90d7011cab4da` |
| `ac79_engineering_v1/results.json` | `620c28c05f85ec9aa6d989acc154815c5c485566` | `7220f98e9e478c5d9e1defb07015a523357b05ac9d762e43f5579b0673ee3bca` | `b2d8dcd24abb05395d0084236b0aaffa78f852d0f818b1db46d33edf5d39e0e3` |
| `ac79_engineering_v1/rows.jsonl` | `e9f762ef82f9c84302c05d6886214029047eb286` | `8913b20c007a340326b3717ae5327d7be873751c8798a3a42bb8b32d5c38a6b8` | `f031e054837d8cd4f8fc737ef4b9ee9b5ad3ba2b12e75e2ebd56dc500eaa567d` |
| `ac79_results_v1/pre_run_snapshot.json` | `82e1abd7cac5b54257cb22babab8f47f12bce06b` | `95ac41ceb0116192dadad97614d6c4a63b3dc873813d7be67586dcf5dc0267f6` | `b79f962b1f5f3298de2c30cf828478d26891f7903fd795f1dce90d7011cab4da` |
| `ac79_results_v1/results.json` | `8fddf6939c9b9b4d9cccc1027e6f18b16ddfecc5` | `1f6e20eedd283e45c13363b9318316c37f2ab1507ad77edef900a050dad920e8` | `160cb188e93b9790fabf7449ce14af7957961e984451ff069cd7ab2102de7615` |
| `ac79_results_v1/rows.jsonl` | `f0784fc1704ebb1b0111bbdde261a15f1de921b4` | `11ca88a17aaab3cb3ee97484b895b988f610ecfe34a8f8c2044c87056c9aba2a` | `622a92ebce8850f9c268a7fd07703c443dc25a1d71dc9a418f3c945d4f4621e4` |
| `ac80_results_v1/pre_run_snapshot.json` | `d89e4d0244cc92cda8f5ca995750b55957ec5edb` | `7d754fde55dba5e9557c4049a83f789c6b5714d87b7216de6f6a4432ed93e825` | `ee6670f583672593a443b0d114d33c3749642417894a97db0c9b9b05fa2f1264` |
| `ac80_results_v1/results.json` | `bd343eb661add5c3b617f77dc5b30e9e01fd5e5a` | `2fcb11c8c6d558969d0b9bffef1c246306eb369e6db82f0898b2ae6610ab9690` | `b4a2cad7f1cef193a1aa54efbd4247a174a8074c775fbb8cfacf0da5db7c2f70` |
| `ac80_results_v1/rows.jsonl` | `331644d3541a509ff52084965b9af42082ea031e` | `58f7be836effd7a4b8cf744e1866f98fc2e84a970c158041762d10b697cacc8e` | `33e0ca85a8699e9b7f555e23569083a259f796062fed416b00cf41da29346bda` |

Restored file count: 78. LF blob bytes: 2085169. CRLF-normalized comparison: 78/78 match `a6_decision_v1/baseline_hashes.json`.
