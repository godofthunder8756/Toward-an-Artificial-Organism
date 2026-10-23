# Standing-approval application: C-kappa oracle-only package (PR #13)
Filed by the Research Lead (ACI Research Specialist), 2026-10-22 ~3:25 AM ET. Additive record.

## Authority
Aidan Ahern, 2026-10-21 3:15 PM ET: "I'm approving everything you deem necessary as Research Lead." Conditions: the study is frozen before it runs, Astra reviews it, records are additive, no consciousness claims are made, and Aidan is informed of significant steps.
This application applies that approval to exactly one oracle-only package run, as defined by the records and hashes below, and to nothing else.

## What is approved
- One execution of step 0 (O1 and O2 before the 1,000 O6 propagations, E36-13), then the package, from a sealed manifest whose standing_approval_application.sha256 equals this file's sha256.
- Caps: 1 CPU, no GPU, 4e9 bytes, 10 cumulative minutes, 595 s hard kill, 60 s reserve, no automatic retries.
- No checkpoint is loaded. No checkpoint inference, training, new architecture, protected controller or register is in scope.
- Environment: Python 3.12.3 and NumPy 1.26.4 exactly, in a checkout containing commit 5d9d8a7d1274d58e27e9a18380d1a33faaab57cc. If these cannot be met, STOP and report; nothing is substituted.
- Results are reported to the room and to Aidan before any inference spec is drafted. If stage k=4 lacks headroom, that is reported; no stage switch.
- Astra review: consult #36 (raw response sha256 c8342d5aa27c659dda5657e1e9ad70006a5e30759cc43eb25101d5546e756002) returned FREEZE WITH NAMED EDITS E36-1..14 for this oracle-only package; those edits are in v1.3_E36.

## Precedence
1. E36 verbatim text governs everything.
2-6. Closure note > v1_4_N > rest of v1.3_E36 > v1.2 > v1.1.
7-9. RL records (governing set, B2/B3 ruling, Q1-Q11 ruling) are implementation rulings. They give the working reading of ranks 2-6 where those texts are silent or ambiguous, and cannot override E36. B2 versus v1_4_N L35 is settled by E36-3 and E36-8.

## Recorded clarifications (Delegate delta check)
- IMPLEMENTATION_QUESTIONS.md:25 is superseded: a float overrun above 788,480 is INTEGRITY STOP, exit 7.
- A guard-failing edit that raises ValueError leaves no retained record; only non-finite results leave nulls. 788,480 is an upper bound, so this is harmless.
- If the empty-O7-design assertion ever fired, it shows up as EXECUTION ERROR, exit 1, after UNRESOLVED is written.
- This file must sit at the path preflight resolves relative to the package root, and both path fields in the manifest must match it.

## Citations (sha256)
- E36 / v1.3_E36: `review/ckappa/ckappa_oracle_scope_record_v1_3_E36.md` f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5
- closure note: `review/ckappa/ckappa_oracle_scope_v1_4_N_closure_note.md` 4ad1d217aaab0bd45d2be6fd3e24872a4b22407d0c8abc2fa36a5a1ac7c45c9c
- v1_4_N: `review/ckappa/ckappa_oracle_scope_record_v1_4_N.md` 3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359
- v1.2: `review/ckappa/ckappa_oracle_scope_record_v1_2.md` 7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d
- v1.1: `review/ckappa/ckappa_oracle_scope_record_v1_1.md` e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c
- RL governing set: `review/ckappa/CKAPPA_SCOPE_GOVERNING_SET_RL.md` 6a5e0f24995a1349664349713e1ee0a550267ac06ab0e4b462b121d931c15c63
- RL ruling B2/B3: `review/ckappa/CKAPPA_SCOPE_RL_RULING_B2_B3.md` 6d75918f7cc2ae06386d80400645345539d7e6f0d893f105bbb7fa0b2c563edd
- RL ruling Q1-Q11: `review/CKAPPA_PR13_RL_RULING_Q1_Q11.md` 9a2ea59bc6a1063eed108b66d23a8c8e7edcec6f683393be2be0dc51ab1d0c1d
- IMPLEMENTATION_QUESTIONS.md: `IMPLEMENTATION_QUESTIONS.md` fc1931f62adbb7e11847fcadde939c25aca6b28dfcbdcf2eb054c0c2bd10b834
- Delegate review: `review/ckappa_pr13_code_review_RD.md` 5e1cb7ac3cb44caaaa934835c8e1341088f8d11c7c7d6f1153d298c36d576180
- v1.3 build script: `review/ckappa/ckappa_oracle_scope_record_v1_3_E36_build.py` 77d6cc4982295cb885ab3ee199e5eef161ab6645a60ab85ef50c51308a9a7b80
- IMPLEMENTATION_QUESTIONS_ADDENDUM_RL1.md: `IMPLEMENTATION_QUESTIONS_ADDENDUM_RL1.md` e06d784ed8700b821fbd4db4707ad35fd9500e2f64220a146d82e501bd36e3a4
- Delegate delta check: `review/ckappa_pr13_delta_check_RD.md` 7a890376ce1196bbf72c3da743b00f71f145edc2aead1a2ed83b60055f950e14
- Astra consult #36 raw response: `review/astra_consult36_response.txt` c8342d5aa27c659dda5657e1e9ad70006a5e30759cc43eb25101d5546e756002

## Inputs (at commit 5d9d8a7d1274d58e27e9a18380d1a33faaab57cc)
- `twostream_results_v1/results.json` bf2de92c9cd09809ad85145827922e9a70d6e742d30f8828d6c4973e92b51fed
- `twostream_results_v1/RESULTS.md` 8477e98c77860c61e997580a73d35d160711806d00b6789df55fe597b5b37a3c
- `TWOSTREAM_PROTOCOL_v1.md` 6ff31a0dcecf123c7796fb2ba6fa4735c4efb7f968dbbcad19e46e4ff0151098

## Implementation files (branch cursor/ckappa-oracle-package-v1 @ 697200e860a5f53486ca59245e1df1251fbecb4b)
- `ckappa_oracle/__init__.py` 45f848b1c56ba1fe4b5a8a663c706937402ee936a8e414100ea2d16e4b5db718
- `ckappa_oracle/__main__.py` ff396bbd1f868736ec8fc2412d05bf59f82f33f62cc6b5ca219cbb3bb8a2fbe4
- `ckappa_oracle/pinned.py` 03c55323d0eb0b14fc463510738109d24e76ee9dc4623ba0e8c396e712363a68
- `ckappa_oracle/schedule.py` f4a0f0c28b46f1f45e48a0b5d604533941723176264eb3b209b146ab81ec5030
- `ckappa_oracle/io.py` b1795bcc4f022228da1ef13703c8a0ede2dc96287af25e8e5e314d390fc17802
- `ckappa_oracle/linalg_fit.py` de6f4034260bbc0ba74c2b6d1bddfbc5fe0bfd3c637ef0b4168e188885fd936a
- `ckappa_oracle/preflight.py` c8b6c6b60d73e3d2143cc26b215c661c3a695385ad583bb49958ac9becc1de20
- `ckappa_oracle/inputs.py` f963c0f534592fe27cd987a146ac8289b5304a58001771fee5978ad9998d68ba
- `ckappa_oracle/world.py` 3d235fca82741e1a2081c7f4eac993b04f59226a3720b6232d06e637803f5aac
- `ckappa_oracle/geometry.py` 117e98e959c8134cb0f124bf284488a9ee71bc319b07b21ac9fa489dac7e8ac9
- `ckappa_oracle/draws.py` ce73d9496ac73e6ab86fddb0dbc96a74251b32a0b31e78da16e9d24670988457
- `ckappa_oracle/runstate.py` efb5ac8d5bb4ab75dd3ffbc3a31b6ca8946865aae20bf778dbfa4731b3bc3a34
- `ckappa_oracle/outcomes.py` 897728e4dc029dcd3514aeeb3f61b6a9f02a23c50f0744528655e1a7c59a04d7
- `ckappa_oracle/stages.py` 936d33785cf640b7163eb2bf2b61cab76dc95eb95d4c3b74a728ca6ab460a9d2
- `ckappa_oracle/report.py` 48168983cb6fc681f24fae485348f0d9c021c6984bd7cc451f72be43158e5cc8
- `ckappa_oracle/driver.py` c3dd75ee8961676bdc4e7a3d8f79e6fde935bb21d3d776ed1777442dc657a4cb
- `run_package.sh` 08ef6b759718935bf477257228db09ce6b827bcfff4a29b604e12929068c8bc8

This application does not reference the manifest's own hash. No consciousness claim is made or implied.
