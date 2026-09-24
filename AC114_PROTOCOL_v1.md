# AC114 (A3) — SR-2 boundary-exchange successor: frozen confirmation protocol

2026-09-24. Freeze-and-confirm deliverable for the A3 card (t_d753dfba): *run the
A2 successor on untouched final seeds and record whether it realizes exchange at the
declared interface, retention separately from intake, endogenous boundary turnover,
resource-supported production, and the selective-rescue effects.* This protocol is
hashed into the study snapshot BEFORE the final seeds are run; no gate below is
moved after inspecting confirmation outcomes.

Vocabulary: charter v2 (§5 substrate, §7a components), `A1_EXCHANGE_SPEC_v1.md`
(SR-2, D1–D5, T1–T6), `AC114_ENGINEERING_v1.md` (the engineering cohort this
confirms), `A2_BOUNDARY_VERDICT_v1.md` (retention, established). The successor is
`ac114.py`; its level-1 law is pinned by `test_ac114.py`.

---

## 0. The question, stated first

On untouched final seeds, does the SR-2 successor realize — measured per A1's
predictions — (a) exchange at the declared interface, (b) retention and export
separately from intake, (c) endogenous boundary production/turnover, (d)
resource-supported continuation of the production network, and (e) the
selective-rescue effects, with survival reported as a SEPARATE outcome?

The frozen claim ceiling (A1 §5), one step above retention and one step below
clause (ii): *the organism produces and renews a finite-lived perimeter whose live
links are the sites at which the environmental resources that fund production are
admitted into the interior — the same links that retain the constituents admit the
intake that funds all production.* Non-claims: not autopoiesis, not clause (ii),
not "alive", not "the only possible successor".

---

## 1. The change (SR-2, confined to the admission decision)

`ac4.react` actions 0/1 credit intake only while the channel's declared gate
link(s) are live (`if ADMIT(b,c):`), instead of unconditionally. `ADMIT` is one of
three functions: `_admit_site` (SR-2: `(b.boundary[GATE_LINKS[c]] > 0).any()`),
`_admit_count` (the demoted aggregate rival: `(b.boundary > 0).sum() >= B_MIN`),
`_admit_none` (continuity: always `True`). The aggregate B-count gate survives as a
comparison arm only. No conservation identity is patched: `ac4.balance` carries
`in_m`/`in_f` as variables, so gating them to 0 satisfies every identity by
construction (AC15 lesson). The contact cost (1 energy) is paid whether or not
admission succeeds.

---

## 2. World constants (supplied, fixed at protocol time)

- `GATE_LINKS = {0: (0,), 1: (1,)}` — singleton gates (sharpest discrimination).
- `B_MIN = 10` — rival threshold (inert at count 20, cuts at 0, admits at the
  punctured count 19).
- `YIELD = {0: 32, 1: 64}` — frozen yields, unchanged.
- `PUNCTURE_LINKS = (0,)` — channel 0's gate link (D1 decisive).
- `NONGATE_PUNCTURE_LINKS = (5,)` — a non-gate link (D2 local admission).
- `ONSET = 512`, horizon `2048` ticks.

---

## 3. Arm set (11 arms; the smallest set covering A1's seven comparisons)

| Arm | Gate | Boundary | Retention | Identifies |
| --- | --- | --- | --- | --- |
| `reference` | none (frozen `ac9.step`) | intact | intact | continuity anchor / exchange bypass |
| `keep` | site | intact | intact | intact produced boundary (successor ordinary) |
| `rival` | count | intact | intact | aggregate gate is a fair baseline (non-strawman) |
| `no_B` | site | suppressed | broken | boundary-production interruption |
| `no_B_retention` | site | suppressed | rescued (kernel) | retention-only rescue, exchange NOT restored (T2) |
| `no_B_retention_ref` | none | suppressed | rescued (kernel) | retention continuity (T1) |
| `permeant` | site | intact | broken | exchange-only, retention NOT restored (mirror) |
| `B_rescue` | site | external | intact | external restoration, labelled external (T6) |
| `puncture` | site | gate link 0 dead | ~intact (19/20) | D1 decisive (site side) |
| `rival_puncture` | count | gate link 0 dead | ~intact (19/20) | D1 decisive (count side) |
| `puncture_non_gate` | site | non-gate link 5 dead | ~intact (19/20) | D2 (admission is local) |

`reference` is the frozen `ac9.step` object itself (no surgery). The puncture is a
restriction of the action-8 candidate set plus a one-time zeroing booked as
`B_discard`; the puncture arms run the normal step before `ONSET` and switch to the
punctured step at `ONSET`.

---

## 4. Endpoints (measured per individual, reported separately)

- **Admission** (exchange): `ledger['in_f']`, `ledger['in_m']` (total) and
  `assay['in_f']`, `assay['in_m']` (post-onset, t >= 512).
- **Retention/export**: `ledger['particle_export']`, `ledger['B_birth']`,
  `ledger['external_B']`.
- **Production**: `ledger['W_birth']`, `ledger['C_birth']`, `ledger['B_birth']`,
  `ledger['converted']`.
- **Activity/survival**: `activity`, `completed` (planned-denominator), `routes`,
  `state_hash`, `chrono` (first acquire/loss/export/dead/gate-dead).

Death alone identifies no mechanism (A1 measurement discipline).

---

## 5. Gates (prespecified before confirmation; engineering informed the shapes, not the outcomes)

- **G1 (T5 inertness).** For every individual (16/16): `keep`, `rival`, and
  `reference` are byte-identical — equal `state_hash`, `ledger`, and
  `final_inventory`. The site gate is the only change and is never exercised while
  the boundary is intact.
- **G2 (T1 retention continuity).** For every individual: `no_B_retention_ref`
  reproduces the frozen AC10 `no_B_retention` arm field-for-field (`state_hash`,
  `ledger`, `final_inventory`, `activity`, `routes` equal to
  `ac10_results_v1/rows.jsonl`).
- **G3 (T2 exchange mediation).** For every individual: `no_B_retention` (site)
  has post-onset admission zero (`assay['in_f'] == 0` AND `assay['in_m'] == 0`)
  and does NOT complete; `no_B_retention_ref` (no gate) completes. The admission
  ledger, not the death scalar, is the mechanism.
- **G4 (D1 site vs count — the decisive gate).** For every individual, paired per
  seed: `puncture` has `assay['in_f'] == 0` (post-onset channel-0 admission
  zeroed) AND `rival_puncture` has `assay['in_f'] > 0` (post-onset channel-0
  admission retained). The two arms share seed, stream, and puncture; only the
  gate differs.
- **G5 (D2 local admission).** For every individual: `puncture_non_gate` has
  `assay['in_f'] > 0` AND `assay['in_m'] > 0` (both channels still admit).
- **G6 (T6 external rescue).** For every individual: `B_rescue` has
  `ledger['external_B'] > 0`, `ledger['B_birth'] == 0`,
  `ledger['particle_export'] == 0`, and completes. Labelled EXTERNAL, never
  counted as autonomous.

**Survival is a SEPARATE outcome** (reported per arm as a bimodality-aware lower
bound, AC68), never folded into the admission gates.

**Reported, not gated:** D3 semipermeability (`keep` has `particle_export == 0`
AND `in_f > 0` AND `in_m > 0` — the same links retain and admit); D5 renewal
(`keep` has `B_birth > 0`, with the turnover multiple `B_birth / 20` reported); the
permeant mirror (dies by export with `particle_export > 0`, the mirror image of
`no_B_retention`). D4 (production dependence) inherits B's already-established C3
dependence (A2 §2) and is not re-tested here; it has no dedicated arm in this set.

---

## 6. Cohort and stopping rule

- **Engineering:** seeds 0–7 (16 individuals, both histories). Informed the gate
  shapes; DISCLOSED here and excluded from the final sample.
- **Finals:** seeds 6500–6507 (16 individuals, both histories) — untouched, disjoint
  from the engineering cohort and from every prior final family. Run ONCE after
  this protocol is hashed.
- **Analysis unit:** seeds are the replication unit; the two histories per seed are
  repeated measures, not independent units (AC88). Every gate is stated per
  individual (all 16 must hold); inference is reported at the seed level (8
  independent units).
- **Stopping rule:** G4 (D1) is decisive. If it fails — puncturing the gate link
  does not zero channel-0 admission, or the rival's admission is also zeroed — SR-2
  has collapsed into SR-1 and the produced-interface ceiling is not earned: record
  the negative and stop, without weakening the criterion. If G1 fails, the build is
  defective (the gate changed the frozen economy with the boundary intact). Gates
  are NOT moved after seeing outcomes; a failed gate is recorded with its measured
  value (AC16/AC17 discipline).

---

## 7. Verification plan (split, per the AC9 pattern)

- **Audit** (`audit_ac114.py`): re-derives coverage, source hashes, ledger
  identities, arm invariants, and the G1–G6 gate verdicts from the saved table
  WITHOUT simulating.
- **Replay** (`replay_ac114.py`): sampled exact reruns of frozen rows, compared
  field-by-field including `state_hash` (determinism/integrity check only, not
  independent confirmation).
- **Implementation tests** (`test_ac114.py`): level-1 transport-law tests (22) plus
  level-2 organism-level consequences on engineering seeds, extended with the final
  gate verdicts pinned as recorded-outcome regressions.

---

## 8. Frozen source of truth (hash set)

The frozen source set is the declaration plus the simulation code:
`ac114.py`, `ac9.py`, `ac9_priority_v2.py`, `ac9_memory.py`, `ac5.py`,
`ac5_program.py`, `ac4.py`, `ac4_transport.py`, `ac1.py`, `AC114_PROTOCOL_v1.md`.
Verification tools (`test_ac114.py`, `audit_ac114.py`, `replay_ac114.py`) are
recorded separately and are NOT in the hash set, so a later improvement to a tool
does not drift the study (AC16/AC17 lesson).

SOURCES (declared): `ac114.py`, `ac9.py`, `ac9_priority_v2.py`, `ac9_memory.py`,
`ac5.py`, `ac5_program.py`, `ac4.py`, `ac4_transport.py`, `ac1.py`,
`AC114_ENGINEERING_v1.md`, `A1_EXCHANGE_SPEC_v1.md`, `A2_BOUNDARY_VERDICT_v1.md`.
Frozen results reproduced: `ac10_results_v1/rows.jsonl` (`keep`, `no_B_retention`).
