## 0. Sources, hashes and precedence

| Source | sha256 | Role |
|---|---|---|
| `/workspace/astra_consult38_response.txt` (Astra #38 raw, 385 lines, E38-1..16) | `87fd77e05cd4121959ee59b09bbf5b7ba268fa6d86b7426058c65877817ca2a5` | **Governs over everything**, including this file and any summary of #38 |
| `/workspace/astra_consult37_response.txt` (Astra #37 raw) | `ce010fdb0a4af2304cd43c06ad476c2a51e2b117ce6c24ee7744b0a1c08063e2` | Governs below #38 |
| `/workspace/astra_consult36_response.txt` (Astra #36 raw, E36-1..14) | `c8342d5aa27c659dda5657e1e9ad70006a5e30759cc43eb25101d5546e756002` | Governs the inherited oracle definitions, below #37 |
| `review/ckappa_classfit_synthetic_scope_record_v1_1.md` | `97165ac6cb90fbd9433fa3a8777c017319b7cefc88b6ed45d9f902f3aaca23aa` | Superseded base text (unchanged) |
| `review/ckappa_classfit_synthetic_scope_record_v1_1_NOTE_1.md` | `00ec1902fcd16f2d722447c8f52d67123a5eb305bbe0c73c3657afb73b531aea` | Superseded additive note (unchanged); §3 withdrawn |
| `review/CKAPPA_SCOPE_GOVERNING_SET_RL.md` | `6a5e0f24995a1349664349713e1ee0a550267ac06ab0e4b462b121d931c15c63` | Oracle governing set |
| `review/CKAPPA_SCOPE_RL_RULING_B2_B3.md` | `6d75918f7cc2ae06386d80400645345539d7e6f0d893f105bbb7fa0b2c563edd` | B2/B3 |
| `review/ckappa_oracle_scope_v1_4_N_closure_note.md` | `4ad1d217aaab0bd45d2be6fd3e24872a4b22407d0c8abc2fa36a5a1ac7c45c9c` | B1, 595 s, N-b |
| `review/ckappa_oracle_scope_record_v1_4_N.md` | `3f0c5c129fbf290ab2ebf2661749ce64f2d0305670d385392aa3a3a6336ff359` | N1–N4, n1–n5 |
| `review/ckappa_oracle_scope_record_v1_3_E36.md` | `f6263fb80517a582123a23d8f8b9a1426a4157b82a2d3de8f548dc8b61da04e5` | E36 verbatim, §3 values |
| `review/ckappa_oracle_scope_record_v1_1.md` | `e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c` | World, folds, O6/O7 definitions |
| `review/ckappa_oracle_results_review_RD.md` | `617e983d96c0487f7345fdaae83fe972cf9d5ffe5102f84a4b37e94ad73f64ba` | M-1 |
| PR #13 scratch clone `/workspace/scratch/pr13` @ `14376f38fe09157eef85bfac1cc4a4433d49bebc` | code: `stages.py` 936d3378, `linalg_fit.py` de6f4034, `geometry.py` 117e98e9, `world.py` 3d235fca, `pinned.py` 03c55323. Outputs: `stage_O1.json` 794746a7, `stage_O7.json` 994dda0a, `results.json` 6adb5de2, `fit_freeze_O6.json` b6f817c8, `fit_freeze_O7.json` 347bcd51 | Read only |

**Precedence (proposed for freeze).**
1. Astra #38 raw text.
2. Astra #37 raw text, where #38 does not revise it.
3. E36 raw text.
4. This record.
5. The oracle governing set. It supplies every inherited definition that this record does not replace.

A summary of #38 that departs from the raw text, including the Specialist's, has no standing; see §12.3.

**Development-informed disclosure.**
- #37 L162: "This is development-informed work: O7 and its cancellation are already known. New freezing does not make them unseen."
- Q, Q₂ and the directions are reused per #38 Q10, and that reuse is likewise development-informed.

## 1. Claim ceiling (C1)

E38-15, verbatim (also quoted in §2b):

> "This package tests implementation identities, synthetic response headroom and limitations of declared intervention-prediction models on specified synthetic systems. It establishes no result about trained GRUs and answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY. Confound gains do not identify an independent covariance register or exclude two-coordinate mediation or reachable-set lookup implementations. Failure of a class-conditioned criterion does not exclude nonlinear, prefix-dependent or orbit-dependent covariance codes. No result establishes acquisition, recurrent-transition-specific use, necessity, irreducible joint state, C4, C5, consciousness, autopoiesis or life."

- **C1.1 Synthetic-only.** The package concerns declared synthetic systems only.
- **C1.2 No checkpoint.** No checkpoint or weight file is opened (E37-9, E38-16).
- **C1.3 Q-tags.** None of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY is answered, and the four stay separate. The package's only forward role is to inform whether a later, separately frozen **Q-CAUSE** measurement specification is warranted (#37 L164). That is a decision input, not a Q-CAUSE result.
- **C1.4 Neural ceiling.** E37-10 (§2) plus the #38 L202 sentence, which must be retained explicitly:

  > "Failure of the declared class-conditioned criterion does not exclude orbit-dependent covariance codes, including codes whose local coordinate relation differs on held-out orbits."

- **C1.5 No consciousness, C4, C5, autopoiesis/"autopoietic", life/"alive"** claim is made or implied.

## 2. Astra #37 items: verbatim text and compliance map (kept from v1.1)

The E37 quotes are carried over unchanged. Where #38 revises the mapped clause, the #38 rule governs, as shown in §2b.

