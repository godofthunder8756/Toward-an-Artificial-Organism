# AC115 (I4) — integrated successor: frozen confirmation results

2026-09-24. Confirmatory deliverable for the I4 card (t_8a1a34aa). The protocol
(`AC115_PROTOCOL_v1.md`) was hashed into the study snapshot BEFORE the final seeds
ran; no gate was moved after inspecting outcomes. Final seeds **6600–6607** (16
individuals, 2 histories each), untouched and disjoint from the engineering cohort
(0–7) and from every prior final family. Engineering (`AC115_ENGINEERING_v1.md`)
informed the gate shapes only.

---

## 0. Verdict, stated first

**MIXED — mechanism-level composition SUPPORTED; survival-level composition NOT
confirmed.** On untouched seeds the integrated successor realizes the admission
law and its discriminations uniformly (G1–G3, 16/16), and all six functions —
exchange admission, retention, renewal, reconstruction, succession, paid updates
— are present AND actually exercised in the SAME organisms (the `keep` arm,
16/16). But the four gates that prespecified a SURVIVAL or completion requirement
(G4–G7) FAIL on a minority of finals, and the failures are recorded, not moved.

The failures are a transfer failure, not a mechanism failure: the admission,
retention, and reconstruction discriminations hold in every failing individual;
what does not transfer is the survival of the intake-bearing control arms
(`no_B_retention_ref`, `B_rescue`) and of the count arm under simultaneous
corruption+move+puncture (`rival_puncture_simult`) at the 16,384-tick horizon.
This is the AC68 W/C bimodality re-entering through the long horizon (the exact
risk the protocol's caveats §9 carried as lower bounds), and it is seed-dependent
(AC39). The prespecified gates that bundled survival into a mechanism gate are
recorded as FAILED; the mechanism they were meant to guard is intact.

Licensed wording at the mechanism level (I2 §1): *one organism renews its
produced exchange boundary while the admission gate is byte-inert at the intact
boundary (G1), admission is link-specific (G2) and local (G3), and the five
internalization mechanisms are preserved byte-for-byte (G1) and recorded
exercised (keep arm).* NOT supported at the survival level: the composition
under simultaneous stress is NOT uniformly survivable on one final family. Not
autopoiesis, not clause (ii), not "alive".

---

## 1. What was frozen

- **Runner:** `ac115.py` (SR-2 site gate on the AC105 five-mechanism closure;
  finals mode added; `run`/`_run_core`/`gates_ac115` unchanged from engineering).
- **Protocol:** `AC115_PROTOCOL_v1.md` (gates G1–G8, cohorts, criterion typing,
  stopping rule, caveats).
- **Hash set** (`pre_run_snapshot.json`, 26 files): the declaration
  (`AC115_PROTOCOL_v1.md`) + `ac115.py` + the frozen dependencies (the AC105
  SOURCES list plus `ac114.py`). Verification tools (`test_ac115.py`,
  `audit_ac115.py`, `replay_ac115.py`) are NOT in the set (AC16/AC17 lesson).
- **Constants:** `GATE_LINKS={0:(0,),1:(1,)}`, `B_MIN=10`,
  `PUNCTURE_LINKS=(0,)`, `NONGATE_PUNCTURE_LINKS=(5,)`, `YIELD_F=YIELD_M=64`,
  `TICKS=16384`, `CORRUPT_TICK=8192`, `CORRUPT_BITS=8`, move
  `[(8192,'flip'),(12288,'flip')]`, `PUNCTURE_TICK=512`,
  `PUNCTURE_TICK_SIMULT=8192`.

---

## 2. Final cohort (seeds 6600–6607) — priority covariate

Seed → priority (measured covariate, `ac4.acquire`, deterministic):

| seed | priority |
| --- | --- |
| 6600 | (0,2,3,1) |
| 6601 | (0,3,1,2) |
| 6602 | (2,0,1,3) |
| 6603 | (2,0,1,3) |
| 6604 | (1,2,3,0) |
| 6605 | (3,0,2,1) |
| 6606 | (0,1,2,3) |
| 6607 | (2,0,3,1) |

Note 6605 realizes the AC83 adversarial priority `(3,0,2,1)` (bank-1 renewal
last). Note 6602 and 6603 share priority `(2,0,1,3)` yet differ in outcome (6603
survives where 6602 dies), so the failures are seed-specific trajectories, not
priority-determined.

---

## 3. Gate results (prespecified; failures retained)

| Gate | Type (protocol §4) | Result |
| --- | --- | --- |
| G1 single-change license | (a) presence | **16/16 PASS** |
| G2 D1 link-specific admission | (c)+(e) | **16/16 PASS** |
| G3 D2 local admission | (c) | **16/16 PASS** |
| G4 T2 boundary-supports-entry | (c) | **FAIL 2/16** (seed 6602) |
| G5 retention-vs-admission | (c) | **FAIL 2/16** (seed 6602) |
| G6 endogenous-vs-external | (a) | **FAIL 4/16** (6602, 6606) |
| G7 composition-under-stress | (b)+(c) | **FAIL 6/16** (6601, 6602, 6605) |
| G8 completeness+determinism | verification | **PASS** |

**G1 (the decisive license) — PASS.** `keep`/`rival`/`reference` are
byte-identical (`state_hash`) to each other and to AC105 `persistent_budget` at
`simult` on all 16 individuals, non-vacuously (corruption applied, `fw_at_corrupt
== 8`, `successions == 6`, `flipped_still_wrong == 0`). The gate is correctly
implemented and adds no resource competition when inert. This is exact byte
equality, not a "nonsignificant difference".

**G2 (D1) — PASS.** Paired per seed: `puncture` (site) has zero alive-window
channel-0 admission (attempted > 0) while `rival_puncture` (count) admits, 16/16.
The SR-2 site gate has not collapsed into SR-1.

**G3 (D2) — PASS.** `puncture_non_gate` (non-gate link 5 dead) admits on both
channels, 16/16 — admission is local, not global.

**G4 (T2) — FAIL 2/16, mechanism intact.** The admission discrimination holds
16/16: `no_B` (site) has gate links dead and zero alive-window admission on both
channels (non-vacuous on channel 1) and dies; `no_B_retention_ref` (none) admits
every contact. But the prespecified gate also required `no_B_retention_ref` to
**complete**, and on seed 6602 (both histories) it dies at t=347 with W=0, C=0 —
the W/C collapse under B suppression, not an admission failure. The gate is
recorded FAILED (2/16); the discrimination it guards is intact.

**G5 (retention-vs-admission) — FAIL 2/16, same cause.** `no_B_retention` (site)
has zero alive-window admission on both channels and dies (16/16); the retention
rescue restores retention but not admission. The `no_B_retention_ref` completion
clause fails on 6602 (t=347), identical to G4. Recorded FAILED (2/16).

**G6 (endogenous-vs-external) — FAIL 4/16.** The endogenous half holds: `keep`
has `B_births` 1674–1679, `external_B == 0` on all 16, and `particle_export == 0`
on 15/16 — **6606 (both histories) leaks a single particle** (`particle_export ==
1` over 16,384 ticks), so the `export == 0` clause fails there. The external half
holds on 14/16: `B_rescue` has `external_B > 0`, `B_births == 0`, and completes,
except on **6602 (both histories) where `B_rescue` dies at t=347** (the same W/C
collapse; the external B supply cannot rescue the collapsed converter). Recorded
FAILED (4/16).

**G7 (composition-under-stress) — FAIL 6/16, mechanism intact.** In every
failing individual the composition MECHANISM holds: `fw_at_corrupt == 8` →
`flipped_still_wrong == 0` (reconstruction completes before death),
`successions >= 1`, and the paired `puncture_simult` (site) arm has zero
alive-window channel-0 admission under the same challenge. What fails is the
prespecified completion/description-integrity clause: `rival_puncture_simult`
(count) dies on 6601 (t=15276, desc 129), 6602 (t=9589, desc 80), and 6605
(t=16336, desc 130 — 48 ticks short of the horizon), all via the puncture W/C
leak. Recorded FAILED (6/16).

**G8 — PASS.** 208 rows = 8 × 2 × 13, no duplicates, no gaps; sampled exact
reruns byte-identical (see §6).

---

## 4. The six functions: present and actually exercised, in the SAME organisms

Measured in the `keep` arm (the integrated candidate), 16/16 unless noted. These
are the mechanism records, not endpoint agreement — each (b) claim is backed by
the named firing record (protocol §4).

| function | endpoint | measured (min–max over 16) |
| --- | --- | --- |
| reconstruction (d recovery) | `fw_at_corrupt` → `flipped_still_wrong`, `recovery_tick` | 8 → 0; 8193–8202 |
| succession | `successions`, `description_correct` | 6, 130 |
| operational memory + allowance | `relinquishments`, `register` | 2, majority-clean |
| paid updates | `reg_writes` / `succ_writes` / `ctrl_writes` | 2327–2460 / 2671–2699 / 1672–1689 |
| boundary production | `B_births`, `particle_export` | 1674–1679; 0 (15/16, one leak on 6606) |
| exchange admission | `admission` (ch0 202/202, ch1 ~992/992) | full |

The five internalization mechanisms (reconstruction, succession, operational
memory, decision allowance, paid updates) run in the same body that contacts the
environment and renews its boundary. `observer_discard_keep` is per-tick AND
terminal byte-identical on all 16 — the gate adds no host state.

---

## 5. Survival as a SEPARATE outcome (lower bound)

| arm | survive (of 16) |
| --- | --- |
| `keep` / `reference` / `rival` | 16 |
| `no_B_retention_ref` / `B_rescue` | 14 |
| `rival_puncture_simult` | 10 |
| `rival_puncture` / `puncture_non_gate` | 4 |
| `puncture` / `no_B` / `no_B_retention` / `puncture_simult` / `permeant` | 0 |

Reported as a bimodality-aware lower bound (AC68), never folded into an admission
gate. The control arms that complete 16/16 on the engineering family (0–7)
complete 14/16 (`no_B_retention_ref`, `B_rescue`) on finals — AC39 in the
unfavourable direction.

---

## 6. Verification (split, all green)

- **Audit** `audit_ac115.py`: PASS on integrity — 208 rows, 26 source hashes
  valid, coverage complete, observer-discard identical 16/16. Gate verdicts
  recomputed from the saved table WITHOUT simulating and agree with the runner
  (G1/G2/G3/G8 pass; G4/G5/G6/G7 fail as above).
- **Replay** `replay_ac115.py`: PASS — 26/26 sampled conditions reproduce
  field-for-field including `state_hash`, covering the failing individuals (6602
  `no_B_retention_ref`/`B_rescue`, 6606 `keep`, 6601/6605 `rival_puncture_simult`)
  so the recorded failures are confirmed deterministic.
- **Tests** `test_ac115.py`: 14 pass (8 level-1 gate/puncture law; 5 level-2
  organism-level including the G1 ac105 byte-identity on final seed 6600 and
  observer-discard; 1 final-gate recorded-outcome regression pinning G4/G5/G6/G7
  = FAIL). Full AC suite: 56 pass.

---

## 7. The specific feasibility limit (carried to the assessment)

The design question — *does the SR-2 gate compose with the AC105 five-mechanism
closure?* — is answered **YES at the mechanism level** and **NOT at the survival
level**. The limit is precisely located: at `TICKS = 16384` (AC105's horizon),
the W/C bimodality (AC68) and the puncture leak (AC114 rule 7) make the
SURVIVAL of (a) the B-suppressed control arms and (b) the count arm under
simultaneous corruption+move+puncture seed-dependent, so any gate that prescribes
completion or description-integrity on those arms fails on a minority of fresh
seeds. The gates that did NOT bundle survival — G1 (byte-identity), G2 (link
specific), G3 (local) — pass 16/16, and the survival-bundled gates' mechanism
portions hold in every failing individual.

The honest reading: the exchange role DOES ride the produced boundary that the
five-mechanism organism already maintains (G1–G3, keep-arm exercise), and the
composition is real — but "composes AND survives the simultaneous stress" is a
survival claim that the single-final-family confirmation cannot license (AC39).
A successor study that wants a pure-mechanism gate (admission discrimination
without the completion clause) must write a new protocol on fresh seeds; this
protocol's G4–G7 are retained as failed, not re-shaped.

---

## 8. Reported, not gated

- **The puncture leak** (export): `rival_puncture` 133–406, `puncture_non_gate`
  158–399, `rival_puncture_simult` 27–209 — one hole leaks at the long horizon
  (AC114 rule 7).
- **Route holding** (lower bound): degrades on finals; `rival_puncture` 4/16 and
  `puncture_non_gate` 4/16 survive, and several lose routes to the W/C leak.
- **`permeant`** (reported mirror): dies 0/16 by export, exchange present,
  retention broken.
- **`mat_at_corrupt`, `mat_min_post_corrupt`, `allowance_breached`** per seed.

---

## Sources

`ac115.py`, `AC115_PROTOCOL_v1.md`, `AC115_ENGINEERING_v1.md`,
`I2_INTEGRATED_EXCHANGE_DESIGN_v1.md`, `AC114_PROTOCOL_v1.md`,
`AC114_RESULTS_v1.md`, `AC105_PROTOCOL_v1.md`, `AC105_RESULTS_v1.md`,
`I1_BOUNDARY_CORRECTION_v1.md`. Frozen deps: the AC105 SOURCES list plus
`ac114.py`. Verification: `audit_ac115.py`, `replay_ac115.py`, `test_ac115.py`.
Frozen results: `ac115_results_v1/` (208 rows, `pre_run_snapshot.json` of 26
sources, `results.json`, `rows.jsonl`).
