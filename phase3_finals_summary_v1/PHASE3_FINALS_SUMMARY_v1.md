# Phase-III finals summary v1 — G13

The frozen final runs on seeds 100–111 (N = 12 model seeds), all six arms, plus the five interventions (I1–I5), the π-cut, F1, the coordination and novel-consumer endpoints. Frozen statistical plan (§10): exact sign-flip on paired per-seed differences, α = 0.01, floor 2/2^12 = 0.00049. Equivalence and byte-identity gates are reported per-seed, never inferred from nonsignificance.

- Frozen artifact: `phase3_results_finals_v1/` (72 rows, state_hash from results.json)
- Cross-check (analysis re-train vs frozen rows): 0 mismatches — byte-reproducible
- Seeds: [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]

## 1. The six arms at a glance (per-arm mean over 12 final seeds)

| arm | probe_acc | clean_acc | incoherence | π-cut probe | S_conf ll | S_bias acc | S_conf ceiling |
| --- | --- | --- | --- | --- | --- | --- | --- |
| candidate | 0.9632 | 0.9639 | 0.000000 | 0.5000 | 0.0960 | 0.9555 | 0.0904 |
| r1 | 0.9634 | 0.9631 | 0.014038 | 0.5000 | 0.0985 | 0.9526 | 0.0904 |
| r4 | 0.9645 | 0.9645 | 0.000000 | 0.9645 | 0.0917 | 0.9552 | 0.0904 |
| r5 | 0.9645 | 0.9645 | 0.000000 | 0.9645 | 0.0917 | 0.9552 | 0.0904 |
| r2 | 0.9643 | 0.9645 | 0.003817 |  |  |  |  |
| r3 | 0.9648 | 0.9652 | 0.012856 |  |  |  |  |

Rivals: R1 private-state, R4 sufficient-statistic broadcast (ceiling), R5 independent-copy, R2 monolithic RNN, R3 raw-history.

## 2. Gates (frozen statistical plan)

### H1 — maintained hidden-state content (latent-state inference + W information)
- H1.1 probe above memoryless bound 0.500: candidate mean 0.9632, min 0.9570 (every seed above chance+ε: True).
- H1.2 ceiling equivalence with R4 (empirical ceiling 0.9645): candidate−R4 per seed [-0.0029, 0.0000, -0.0039, 0.0000, -0.0029, -0.0020, 0.0039, 0.0029, -0.0029, -0.0020, -0.0049, -0.0010], max |diff| 0.0049. Equivalence, reported not tested.
- H1.3 paid persistence (π-cut): probe 0.9632 → π-cut 0.5000; sign-flip p = 0.00049 (N_eff 12, floor 0.00048828125).
- H1.4 free recurrence (F1): h_t decode of z under π-cut+zero-W mean 0.4884, max 0.4980 (chance 0.500; all ≤ chance+ε: True).

### H4 — coordination (the load-bearing candidate-vs-R1 contrast)
- H4.1 incoherence: candidate all-zero True; R1 mean 0.014038 (any>0: True); sign-flip p = 0.00049 (N_eff 12).

### H5 — novel-consumer reuse (treated separately)
- H5.1 S_conf log loss 0.0960 vs posterior-entropy ceiling 0.0904 (max gap 0.0125). Equivalence, reported not tested.
- H5.2 candidate−R4 S_conf ll per seed [0.0013, -0.0003, 0.0041, 0.0019, 0.0062, 0.0020, 0.0067, 0.0014, 0.0109, 0.0075, 0.0061, 0.0039]; S_bias acc [0.0020, -0.0020, -0.0010, 0.0020, -0.0010, 0.0020, 0.0068, 0.0020, -0.0020, 0.0010, -0.0078, 0.0020]. Equivalence, reported not tested.

## 3. Interventions (each specialist's response to a W intervention)
- I1 differential-scramble (w★ ↦ triple traces the sign/two-sided/even functions): matches on all seeds — True.
- I2 per-consumer W-cut (cut consumer → exact no-W baseline, survivors byte-identical): all seeds — True.
- I5 coherent error (wrong-sign and stale → mutually consistent triple): all seeds — True.
- I4 private-copy divergence (identity vs value): mean divergence spol 1.0923, splan 1.0923, sreg 1.0923.
- Single-write reach (SHARED): candidate [True, True, True] (one write → 3 consumers); R1 [True, False, False]; R5 [True, False, False] (one write → 1 consumer).

## 4. Per-specialist task performance + resource cost

| arm | S_pol probe | S_plan commit rate | S_plan commit acc | S_reg preserve | refresh targets | total refresh | mean refresh/ep | final E |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| candidate | 0.9632 | 0.9632 | 0.9775 | 0.9812 | 1.0 | 32768.0 | 32.0 | 30.4000 |
| r1 | 0.9634 | 0.9604 | 0.9763 | 0.9829 | 3.0 | 98304.0 | 96.0 | 30.4000 |
| r4 | 0.9645 | 0.9632 | 0.9789 | 0.9785 | 0.0 | 0.0 | 0.0 | 0.0000 |
| r5 | 0.9645 | 0.9632 | 0.9789 | 0.9785 | 0.0 | 0.0 | 0.0 | 0.0000 |
| r2 |  |  |  |  | 0.0 | 0.0 | 0.0 |  |
| r3 |  |  |  |  | 0.0 | 0.0 | 0.0 |  |

- Trainable parameters: candidate encoder 393, R1 three× 103 (total 309), R2 1257, R3 3465, R4/R5 0.

## 5. Not claimed
No equivalence is inferred from nonsignificance; ceiling/byte-identity gates are per-seed facts. This is a level-(b)/(c) representational result — no autopoiesis, workspace-seat, metacognition, or consciousness claim.
