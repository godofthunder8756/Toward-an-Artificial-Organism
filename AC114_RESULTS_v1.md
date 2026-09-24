# AC114 (A3) — SR-2 boundary-exchange successor: frozen confirmation results

2026-09-24. Confirmatory deliverable for the A3 card (t_d753dfba). The protocol
(`AC114_PROTOCOL_v1.md`) was hashed into the study snapshot BEFORE the final seeds
ran; no gate was moved after inspecting outcomes. Final seeds 6500–6507 (16
individuals, 2 histories each), untouched and disjoint from the engineering cohort
(0–7) and from every prior final family. Engineering (`AC114_ENGINEERING_v1.md`)
informed the gate shapes only.

---

## 0. Verdict, stated first

**SUPPORT at the frozen claim ceiling.** On untouched seeds the SR-2 successor
realizes every prespecified prediction uniformly across all 16 final individuals:
the site gate (D1) and the aggregate rival disagree exactly as SR-2 predicts on the
identical puncture; admission is local (D2); retention and exchange are separately
load-bearing and both ride the produced B (T2, the mirror, T6); the successor is
byte-inert in ordinary operation (T5); retention continuity is intact (T1). Survival
is a clean separate outcome (7 arms 16/16, 4 arms 0/16).

Licensed wording (A1 §5, one step above retention, one below clause (ii)): *the
organism produces and renews a finite-lived perimeter whose live links are the
sites at which the environmental resources that fund production are admitted into
the interior — the same links that retain the constituents admit the intake that
funds all production.* Not autopoiesis, not clause (ii), not "alive", not the only
successor.

---

## 1. What was frozen

- **Runner:** `ac114.py` (SR-2 site gate; finals mode added, `run`/`collect`
  unchanged from engineering). Frozen dependencies: `ac9.py`,
  `ac9_priority_v2.py`, `ac9_memory.py`, `ac5.py`, `ac5_program.py`, `ac4.py`,
  `ac4_transport.py`, `ac1.py`.
- **Protocol:** `AC114_PROTOCOL_v1.md` (gates G1–G6, cohort, controls, stopping
  rule).
- **Hash set** (pre_run_snapshot.json, 10 files): the above plus the protocol.
  Verification tools (`test_ac114.py`, `audit_ac114.py`, `replay_ac114.py`) are
  NOT in the set (AC16/AC17 lesson).
- **Constants:** `GATE_LINKS={0:(0,),1:(1,)}`, `B_MIN=10`, `YIELD={0:32,1:64}`,
  `PUNCTURE_LINKS=(0,)`, `NONGATE_PUNCTURE_LINKS=(5,)`, `ONSET=512`, horizon 2048.

---

## 2. Final cohort (seeds 6500–6507, 16 individuals per arm)

| Arm | Survive | in_f (total) | in_m (total) | post-onset in_f | export | B_birth | external_B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `keep` | 16/16 | 608 | 3136–3200 | 448–480 | 0 | 204–207 | 0 |
| `reference` | 16/16 | 608 | 3136–3200 | 448–480 | 0 | 204–207 | 0 |
| `rival` | 16/16 | 608 | 3136–3200 | 448–480 | 0 | 204–207 | 0 |
| `no_B` | 0/16 | 32 | 0–64 | 0 | 3–11 | 0 | 0 |
| `no_B_retention` | 0/16 | 32 | 0–64 | **0** | 0 | 0 | 0 |
| `no_B_retention_ref` | 16/16 | 544–576 | 2688–2752 | 416–448 | 0 | 0 | 0 |
| `permeant` | 0/16 | 0–96 | 0–512 | 0 | 11–93 | 0–22 | 0 |
| `B_rescue` | 16/16 | 544–576 | 2688–2752 | 416–448 | 0 | 0 | 160 |
| `puncture` | 0/16 | 128–160 | 704–896 | **0** | 0–5 | 48–60 | 0 |
| `rival_puncture` | 16/16 | 448–608 | 1792–3264 | **320–480** | 19–46 | 193–199 | 0 |
| `puncture_non_gate` | 16/16 | 448–608 | 1664–3328 | **320–480** | 21–45 | 190–199 | 0 |

The three "intact" arms are byte-identical (equal `state_hash`, `ledger`,
`final_inventory`), reproducing the engineering T5 result on fresh seeds.

---

## 3. Gate results (all prespecified, all pass)

| Gate | Claim | Result |
| --- | --- | --- |
| G1 (T5) | `keep == reference == rival` byte-identical | 16/16 PASS |
| G2 (T1) | `no_B_retention_ref` reproduces frozen AC10 `no_B_retention` | runner-level, 8/8 on the AC10 seeds (test_ac114.py) |
| G3 (T2) | `no_B_retention` post-onset admission 0, dies; twin survives | 16/16 PASS |
| G4 (D1) | `puncture` in_f=0 AND `rival_puncture` in_f>0, paired | 16/16 PASS (decisive) |
| G5 (D2) | `puncture_non_gate` both channels admit | 16/16 PASS |
| G6 (T6) | `B_rescue` external_B>0, B_birth=0, export=0, survives | 16/16 PASS |

**G4 is the decisive gate.** On the identical puncture (gate link 0 dead, 19 links
live, applied at t=512 on a mature organism), the site gate zeroes post-onset
channel-0 admission in 16/16 (`puncture` `assay['in_f']==0`), while the count gate
leaves it at full yield in 16/16 (`rival_puncture` `assay['in_f']` 320–480). Only
the gate differs; seed, stream, and puncture are shared. SR-2 has NOT collapsed into
SR-1.

**G3 (T2), the admission ledger not a death scalar.** `no_B_retention` (site) and
`no_B_retention_ref` (no gate) are identical except the gate: both have zero B
production, zero export, and gate links dead at t=133. The site gate then cuts
intake — post-onset admission is exactly 0 in 16/16 — and the organism dies at
t≈379–383 with fuel 0, energy 0; the twin keeps admitting (416–448 post-onset fuel)
and survives 16/16. Total intake before the gate links die is at most one contact
per channel (32 fuel, 0–64 material, the split depending on which action the
program chose first).

---

## 4. Primary measurements (per A1), each addressed

1. **Exchange at the declared interface.** G4/G5/D3: channel-c intake is a function
   of the local live-state of `GATE_LINKS[c]` alone — one gate-link hole zeroes the
   channel, one non-gate hole leaves it unchanged.
2. **Retention and export separately from intake.** G3 + the mirror: retention
   rescued with the gate links dead cuts intake to 0 (retention does not restore
   exchange); `permeant` (exchange present, retention broken) dies by export 11–93
   in 16/16; `no_B` loses both (export 3–11, intake 0). The two roles ride one paid
   structure (D3: `keep` export 0 with intake full).
3. **Endogenous boundary production/turnover.** `keep` B_birth 204–207 over 2048
   ticks = ≥10.2× the 20-link complement (D5); the gate links turn over like every
   other link and are continuously re-established by action 8 (W-anchored).
4. **Resource-supported continuation of the production network.** `keep` maintains
   W_birth 188, C_birth 31, B_birth ≥204, converted ≥613 while surviving 16/16 with
   zero export and full intake.
5. **Selective rescues.** G6: `B_rescue` (external B matter, zero internal births)
   restores both retention (export 0) and exchange (full intake), `external_B=160`,
   labelled EXTERNAL — confirms the boundary *state* carries the interface role,
   never counted as autonomous production.
6. **Survival as a SEPARATE outcome.** keep/reference/rival/no_B_retention_ref/
   B_rescue/rival_puncture/puncture_non_gate all 16/16; no_B/no_B_retention/
   permeant/puncture all 0/16. Reported as a bimodality-aware lower bound, never
   folded into the admission gates.

---

## 5. Caveats (recorded, not hidden)

1. **Route holding is a lower bound, not a gate.** 3/16 `rival_puncture` (seeds
   6500 h1, 6501 h0, 6504 h1) and 3/16 `puncture_non_gate` (6502 h1, 6503 h1,
   6507 h0) survive but lose one or both routes — the link hole leaks enough W/C to
   starve renewal (the engineering caveat, reproduced on finals and slightly more
   frequent: 3 vs 2 individuals per arm). Admission and survival are gated; route
   holding is reported.
2. **The puncture leaks.** Export is 0–5 in `puncture`, 19–46 in `rival_puncture`,
   21–45 in `puncture_non_gate`. "Retention changes only trivially" (A1 D2's
   wording) is NOT byte-exact — one hole leaks, as AC4 transport already showed.
   D1/D2 concern admission; the leak is a disclosed side effect.
3. **`permeant` dies fast** (export 11–93, brief exchange-present window); the
   mirror is established by the export endpoint, not sustained intake.
4. **`no_B`/`puncture` deaths are attention-hijack-shaped** (fuel 0, energy 0,
   material not depleted) — read the admission ledger, not death, for the mechanism.

---

## 6. Verification (split, all green)

- **Audit** `audit_ac114.py`: PASS — 176 rows, 10 source hashes valid, ledger
  identities and arm invariants hold in every row, G1/G3/G4/G5/G6 all pass.
- **Replay** `replay_ac114.py`: PASS — 21/21 sampled conditions reproduce
  field-for-field including `state_hash`.
- **Tests** `test_ac114.py`: 29 pass (22 level-1/level-2 + 7 final-gate recorded
  regressions). Full AC suite: 56 pass.

G2 (T1 retention continuity) is a runner-level check on the AC10 seed family
(1300–1303, the only seeds in `ac10_results_v1/rows.jsonl`), pinned by
`test_ac114.py::test_no_B_retention_ref_reproduces_frozen_no_B_retention`; the
final-seed `no_B_retention_ref` arm invariants (B_birth=0, external_B=0, export=0,
survives) hold 16/16 and are asserted in the audit.

---

## Sources

`ac114.py`, `AC114_PROTOCOL_v1.md`, `AC114_ENGINEERING_v1.md`,
`A1_EXCHANGE_SPEC_v1.md`, `A2_BOUNDARY_VERDICT_v1.md`, frozen deps (`ac9.py`,
`ac9_priority_v2.py`, `ac9_memory.py`, `ac5.py`, `ac5_program.py`, `ac4.py`,
`ac4_transport.py`, `ac1.py`). Frozen rows reproduced: `ac10_results_v1/rows.jsonl`.
Verification: `audit_ac114.py`, `replay_ac114.py`, `test_ac114.py`.
