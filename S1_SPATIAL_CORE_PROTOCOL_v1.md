# S1 — Spatial informational-core successor: proposed protocol v1

**AWAITING SEPARATE EXECUTION AUTHORIZATION.** This document is a *proposed* frozen protocol.
It licenses no run, freezes no seeds, and hashes into no `pre_run_snapshot.json`. The build
(a new `acN.py` plus this protocol's confirmation) is a further card that S1's successor may
authorize. Design-only; see `S1_SPATIAL_SUCCESSOR_SPEC_v1.md` for the architecture and gate set
this protocol instantiates.

2026-09-25. Predecessors: S0 (`S0_CONTINUATION_DECISION_v1.md`), A0 §6 (T1–T5),
`A0_SUCCESSOR_SPEC_v1.md` (SR-1), the AC92/AC95-D3/D4/AC114 intervention patterns.

---

## 1. World constants (supplied, frozen at build time)

Carried from the frozen AC115 world where a quantity exists there; new quantities are the
permitted-substrate additions the successor introduces.

| Constant | Value | Source / note |
| --- | --- | --- |
| `TICKS` | 16,384 | AC115 horizon |
| `CORRUPT_TICK` / `CORRUPT_BITS` | 8,192 / 8 | AC115 corruption challenge (applied to the program sites) |
| `GATE_LINKS` / `B_MIN` / `YIELD` | `{0:(0,),1:(1,)}` / 10 / 64/64 | AC115 admission gate + yields |
| `DECISION_ALLOWANCE` | 42 | AC115 |
| informational site inventory | program 126, description 130, pointer 2, coordination 18, route memory 12 → **288 logical bits** | A0 §5 / I5 §5, folded per the spec §0 |
| `I_REPLICAS` | 7 | frozen majority convention (AC71 read-by-majority) |
| `I_PARTICLES` | 288 × 7 = **2,016** | the substrate size (rows in `life`/`pos`) |
| `I_BIRTH_COST` | 4 M + 2 E | frozen `birth` (`pay(b,e,4,2)`), booked `W_birth` |
| `I_WRITE_COST` | 1 E + 1 M per particle move | frozen write primitive, gated by `_cap` |
| `I_LIFETIME` | 64 | matches W (ac9.py:45 `b.life[j]=64`) |
| lattice size | enlarged to hold 288 sites × 2 cells + the W/C/B interior | geometry = permitted substrate (charter §5) |
| `PUNCTURE_LINKS` | `(0,)` | AC114 channel-0 gate link, the T2 puncture |

The informational site layout (which bit lives at which site) is a fixed, host-declared
bijection between the 288 logical bits and 288 sites, supplied at acquisition — the same
category as `GATE_LINKS`, and content-inherited (C4).

---

## 2. Arms

| Arm | Realization | Gate | Purpose |
| --- | --- | --- | --- |
| `spatial` | I-substrate, position-mediated read/write (the successor) | T1–T5 | the candidate |
| `exempt` | informational core in a fixed array, never passed to `tr.move` (the frozen declared representation) | T2 contrast | transport-exempt core; T2's "must NOT degrade" arm; also the falsification-(iii) target |
| `spatial_no_reader` | `spatial` with the reader ablated at one program site | T1 | localized-read ablation |
| `spatial_scramble` | `spatial` with the informational→production read scrambled | T4(i) | directed read cut |
| `spatial_block_I` | `spatial` with `I_birth_enabled=False` from a mid-function tick | T3, T4(ii) | directed production cut |
| `spatial_block_I_rescue` | `spatial_block_I` + machinery-only EXTERNAL I re-seed (no content) | T3 | functional rescue |
| `puncture` | `spatial` + `PUNCTURE_LINKS` zeroed (AC114 `puncture_gate`) | T2 | retention vulnerability |
| `exempt_puncture` | `exempt` + the same puncture | T2 contrast | the exempt core must NOT degrade |

`exempt` is the single-change continuity arm: at intact boundary and full reader coverage,
`spatial` must reproduce `exempt` byte-identically (the re-architecture's own inertness
license, the analogue of SR-1 T4 / AC115 G1), so any behavioural difference is attributable
to the spatial realization and nothing else.

---

## 3. Interventions (machinery-only, no content supplied)

- **Reader ablation (T1).** Remove/block the produced reader at one named program bit-site at
  a mid-function tick; no content is supplied, and the organism re-births/re-positions the
  reader endogenously (record `reader_restored_tick`). The ablation gate targets the site only;
  the W class elsewhere is untouched (a clean local cut — the AC10 `no_policy_write` lesson:
  cut exactly the link under test).
- **Puncture (T2).** Zero `PUNCTURE_LINKS` once, booking live links as `B_discard`
  (AC114 `make_puncture_gate`); the informational substrate then exports/decays alongside the
  constituents.
- **Production block (T3/T4(ii)).** `I_birth_enabled=False` at `FUNCTION_TICK − I_LIFETIME`
  (the AC92 timing: interrupt while underway, not at t=0), so the I substrate depletes
  naturally to ~0 at or just before the function tick; record `first_I_empty` per seed and
  verify it lands ≤ the function tick. The W banks keep birthing (the cut is I-only).
- **EXTERNAL rescue (T3).** Re-seed the I bank directly at `I_RESCUE_TICK`, before the step so
  `ac4.balance`'s within-step identities hold (the AC92 direct-restore shape); labelled
  EXTERNAL, machinery-only, no content.

---

## 4. Endpoints (causal, not economic — AC116)

For each individual record: `informational_correct` (bits read correctly through the reader vs
the supplied content), `read_failures` (site-reads returning unreadable), `action_divergence`
(per-tick action-selection difference from `exempt`), `production_ceases` / `state_degrades`
(the T4 directional readouts), `I_births` / `I_expiry` / `I_export` (turnover), `first_I_empty`,
`reader_restored_tick`, `description_correct_at_death`, `completed`, and `state_hash`.
Endpoints are the causal load-bearing readouts; income is reported, **never gated** (the
informational core's value is representational, not economic — AC116/M6).

---

## 5. Seed families and the engineering-vs-finals split

- **Engineering:** 8 seeds (0–7) × 2 histories — used to validate the build, the reader
  scheduling, the T1/T3 timing, and that `spatial ≡ exempt` byte-identically at intact
  boundary. Engineering output goes in its own labelled directory; **every** engineering seed
  is excluded from the final sample.
- **Finals:** 16 untouched seeds × 2 histories (32 individuals), disjoint from every prior
  family, declared at build time and hashed into `pre_run_snapshot.json` only after this
  protocol is frozen. Seeds are the replication unit; the two histories per seed are repeated
  measures, not independent units (AC88).
- Gates T1–T5 are prespecified in §2 of the spec; a predeclared gate that fails is **recorded,
  not moved** (AC16). The four prespecified falsification conditions (A0 §6) are the stopping
  rule: any one of (i) hidden host array reproduces under T5, (ii) reader removal leaves action
  selection unchanged under T1, (iii) exempt core behaves identically to spatial under T2
  → the successor is falsified and reported as such.

---

## 6. Runner and verification discipline (unchanged from the extension checklist)

New file `acN.py`, never an edit to a frozen runner. `root.mkdir(exist_ok=False)`;
`pre_run_snapshot.json` hashes the runner + frozen dependencies + **this protocol** (the
declaration and simulation code are the frozen source of truth; verification tools are recorded
separately, not hashed into the drift-prone set — AC16/17). `rows.jsonl` incremental;
`results.json` at end. Split verification: `audit_acN.py` re-derives coverage/ledgers/arm
invariants from the saved table **without** simulating; `replay_acN.py` does sampled exact
reruns. Survival is reported as a bimodality-aware lower bound (AC68/AC39), never folded into a
mechanism gate. No frozen artifact is edited; no re-run or re-hash of any prior study is used
to "refresh" anything.

---

## Sources

`S1_SPATIAL_SUCCESSOR_SPEC_v1.md` (this protocol's architecture and gates), `ac4.py`,
`ac4_transport.py`, `ac9.py`, `ac5_program.py`, `ac95.py`, `ac9_memory.py` (frozen, read only),
`ac114.py` (puncture/rescue patterns), `A0_AUTONOMY_VERDICT_v1.md` (§5–§6),
`S0_CONTINUATION_DECISION_v1.md`, `A0_SUCCESSOR_SPEC_v1.md`. Proposed only; nothing is frozen
and no run is authorized.
