# AC115 (I4) — integrated successor: frozen confirmation protocol

2026-09-24. Freeze-and-confirm deliverable for the I4 card (t_8a1a34aa): *run the
integrated successor on untouched final seeds and record whether the six
integrated functions — exchange, retention, renewal, reconstruction, succession,
paid updates — compose in one organism, and which are actually exercised.* This
protocol is hashed into the study snapshot BEFORE the final seeds are run; no
gate below is moved after inspecting confirmation outcomes. Predecessors: I2
(t_6db797ac, `I2_INTEGRATED_EXCHANGE_DESIGN_v1.md`) froze the design; I3
(t_9bc216f5, `AC115_ENGINEERING_v1.md`) built `ac115.py` and issued the
feasibility decision (FEASIBLE). Nothing in this document is a result.

Vocabulary: charter v2 (§5 substrate, §7a components), the closure criterion
(`references/closure-criterion.md`, K2/K3), `A1_EXCHANGE_SPEC_v1.md` (SR-2,
D1–D5, T1–T6), `AC114_PROTOCOL_v1.md`/`AC114_RESULTS_v1.md` (the SR-2 successor),
`AC105_PROTOCOL_v1.md`/`AC105_RESULTS_v1.md` (the integrated baseline).

---

## 0. The question, stated first

> Can one organization renew its produced exchange boundary while sustaining the
> internal machinery and state that support reconstruction and continued
> production?

As a testable single-architecture claim: **does AC114's SR-2 link-specific
admission gate compose with the AC105 five-mechanism closure architecture?** On
untouched final seeds, measured in the SAME organisms, does the integrated
successor realize:

1. **link-specific admission** — channel-c intake is a function of the local
   live-state of `GATE_LINKS[c]` alone, not of the aggregate boundary count;
2. **entry + retention through the produced boundary** — the same produced,
   finite-lived links admit the intake that funds production and retain the
   constituents;
3. **composition** — the boundary-exchange role coexists with, and is sustained
   by, the five internalization mechanisms AC105 already composes (description
   turnover, succession coordination, reconstruction, internalized operational
   memory, decision allowance), which are preserved byte-for-byte at the intact
   boundary.

The frozen claim ceiling (I2 §1) is **one step above AC114's ceiling and one step
below clause (ii)**: it extends the material-layer closure ({W, C, B} retention +
exchange, AC114's licensed ceiling) by showing the exchange role composes with the
informational layer. It is NOT a new closure claim — the five-component K3 verdict
already belongs to AC105. Non-claims (unchanged): not autopoiesis, not clause
(ii), not "alive", not a better boundary, no content self-production claim (AC78
blocked), no optimal-allocation or universal-survival claim.

---

## 1. The single change, and the license that pins it

The ONLY addition to AC105 `persistent_budget` at `simult` is the SR-2 admission
gate on `ac4.react` actions 0/1: `if ADMIT(b, c):` credit intake, where
`ADMIT ∈ {site, count, none}`. `site` admits iff the channel's declared gate link
is live (`b.boundary[GATE_LINKS[c]] > 0`); `count` is the demoted aggregate rival
(`(b.boundary > 0).sum() >= B_MIN`); `none` is the frozen always-admit bypass. The
gate reads organism state only — no host state, no challenge-time knowledge.

**The single-change license (G1):** with the boundary intact the gate is never
exercised (action 8 preferentially heals the most-depleted link, AC114 rule 1), so
the integrated `keep`/`rival`/`reference` arms must be byte-identical
(`state_hash`) to each other AND to AC105 `persistent_budget` at `simult`. That
byte-identity is composition direction 1: it proves the gate adds no resource
competition and disturbs none of the five mechanisms. It is exact byte equality,
**not** a "nonsignificant difference" and not inferred from endpoint agreement.

**Base architecture (fixed):** AC105 `persistent_budget` — the full five-mechanism
candidate with the decision allowance (`DECISION_ALLOWANCE = 42`), which is itself
one of the five mechanisms (I1 §4). AC105's own `persistent` control (allowance
absent) is out of scope.

---

## 2. World constants (supplied, fixed at protocol time)

- `GATE_LINKS = {0: (0,), 1: (1,)}` — singleton gates (sharpest discrimination).
- `B_MIN = 10` — rival threshold (inert at count 20, cuts at 0, admits at 19).
- `PUNCTURE_LINKS = (0,)`, `NONGATE_PUNCTURE_LINKS = (5,)` — AC114's values.
- `TICKS = 16384` — AC105 horizon (AC114 used 2048; DISCLOSED change).
- `CORRUPT_TICK = 8192`, `CORRUPT_BITS = 8` — AC105 baseline.
- Move schedule `[(8192, 'flip'), (12288, 'flip')]` — AC105 `simult`.
- **Yields `YIELD_F = 64`, `YIELD_M = 64`** — AC105's reaction yields. DISCLOSED
  difference from AC114's frozen `in_f = 32`: the gate is yield-agnostic, so the
  discriminations transfer, but the intake SCALARS differ and are never compared
  numerically against AC114's frozen numbers.
- `PUNCTURE_TICK = 512` (discrimination arms; mature organism, AC114 rule 2),
  `PUNCTURE_TICK_SIMULT = 8192` (composition-stress arms; coincident with
  corruption + move).

---

## 3. Arms (13; the smallest set covering the four controls)

Every arm holds the AC105 `persistent_budget` mechanism fixed and varies only the
admission gate and the boundary intervention. `challenge` is `none` (no
corruption, no move — the boundary is the sole event) or `simult` (corruption@8192
+ move@8192,12288).

| arm | gate | boundary | challenge | identifies |
| --- | --- | --- | --- | --- |
| `keep` | site | intact | simult | composition baseline + endogenous renewal (G1, G6) |
| `reference` | none | intact | simult | exchange bypass anchor (G1) |
| `rival` | count | intact | simult | aggregate-gate rival (G1) |
| `puncture` | site | gate link 0 dead @512 | none | D1 site side (G2) |
| `rival_puncture` | count | gate link 0 dead @512 | none | D1 count side (G2) |
| `puncture_non_gate` | site | non-gate link 5 dead @512 | none | D2 local admission (G3) |
| `no_B` | site | B production suppressed | none | production interruption: entry + retention (G4) |
| `no_B_retention` | site | B suppressed, retention rescued | none | retention-only rescue: admission NOT restored (G5) |
| `no_B_retention_ref` | none | B suppressed, retention rescued | none | retention continuity (G4, G5) |
| `B_rescue` | site | external B supply | none | external restoration, labelled EXTERNAL (G6) |
| `puncture_simult` | site | gate link 0 dead @8192 | simult | composition stress, site side (G7) |
| `rival_puncture_simult` | count | gate link 0 dead @8192 | simult | composition stress, count side (G7) |
| `permeant` | site | retention broken | none | exchange-only mirror (reported, not gated) |

`permeant` is the mirror of `no_B_retention` (retention broken, admission intact →
export → death); it is a reported-not-gated arm (I2 §4). No conservation identity
is patched: `ac4.balance` carries `in_m`/`in_f` as variables (the AC15 lesson).

---

## 4. Criterion typing (prespecified: which evidence each claim is)

Every claim below is classified by its evidence type, so that "present" is never
read as "exercised", "exercised" never inferred from endpoint agreement alone, and
no nonsignificant difference is read as equivalence.

| type | meaning | how it is evidenced here |
| --- | --- | --- |
| (a) presence | the capability is implemented and reachable | byte-identity license, admission ledger structure |
| (b) actual exercise | the mechanism fires and is recorded firing | `fw_at_corrupt==8 → flipped_still_wrong==0`, `successions>=1`, `reg_writes>0`, `relinquishments>0`, `B_births>0` |
| (c) causal dependence | the function depends on the named cause | puncture/no_B ablations changing admission/entry |
| (d) recovery after interruption | the function returns after an interruption | `recovery_tick` after the corruption |
| (e) comparative utility | better than a rival/control | `site` vs `count` gate under an identical puncture |
| (f) survival | the organism completes the horizon | `completed` / `first_dead`, separate outcome |

Gate → type map (prespecified):

- **G1** — (a) presence: the admission law is correctly implemented and inert at
  the intact boundary (byte-identity, not a margin).
- **G2 (D1)** — (c) causal dependence + (e) comparative: admission depends on the
  LOCAL gate link, and the two gates disagree under an identical puncture.
- **G3 (D2)** — (c) causal dependence: a non-gate puncture (a different link)
  leaves admission intact, so the dependence is local, not global.
- **G4 (T2)** — (c) causal dependence: boundary production causally supports
  entry (killing B production kills entry).
- **G5** — (c) causal dependence: retention-only rescue does NOT restore
  admission (the two roles are separable).
- **G6** — (a) presence of endogenous renewal; `B_rescue` is a labelled EXTERNAL
  control, not comparative utility of a policy.
- **G7** — (b) actual exercise + (c) causal dependence: reconstruction and
  succession are recorded ACTUALLY exercised while the admission discrimination
  holds through them.
- **G8** — verification (completeness + determinism), not a scientific claim.

Mechanism exercise, measured in the SAME organisms (the `keep` arm; reported, not
each one a separate gate):

| mechanism | endpoint | type |
| --- | --- | --- |
| controller reconstruction | `fw_at_corrupt==8` → `flipped_still_wrong==0`, `recovery_tick` | (b) + (d) |
| description/recipe succession | `successions>=1`, `description_correct==130` | (b) |
| operational memory + decision allowance | `relinquishments`, `register`, `allowance_breached` | (b) |
| paid operational-state updates | `reg_writes`, `succ_writes`, `ctrl_writes` > 0 | (b) |
| boundary + production | `B_births>0`, `particle_export==0` | (b) + (c, via G4) |

"Do NOT infer an exercised process from endpoint agreement alone": each (b) claim
is backed by the mechanism record named above, not by the survival/state endpoint.

---

## 5. Endpoints (measured per individual, reported separately)

- **Admission (the I1-corrected discriminator).** Per channel, per contact, in
  the alive window `[gate_c_dead_tick, first_dead]`: `attempted` (channel-c
  contacts with port match), `admitted`. Never aggregate post-onset intake,
  never post-mortem (AC114 rule 12). Under simultaneous corruption + puncture
  (C3), the comparison is per contact-attempt with the action forced (AC15
  lesson 6).
- **Retention/export.** `particle_export`, `B_birth`, `external_B`, `B_discard`.
- **Production.** `W_birth`, `C_birth`, `B_birth`, `converted` (`births_by_window`).
- **The five mechanisms (composition endpoints, never folded).** reconstruction
  (`fw_at_corrupt`, `recovery_tick`, `flipped_still_wrong`), description turnover
  + coordination (`successions`, `description_correct`, `ctrl_idle_end`),
  operational memory (`register`, `relinquishments`, `streak_final`), decision
  allowance (`allowance_breached`, `mat_min_post_corrupt`), production
  (`births_by_window`).
- **Survival/activity.** `completed`, `first_dead`, `first_gate_dead` (chrono),
  reported as a bimodality-aware lower bound (AC68), never folded into an
  admission gate. Route holding reported as a lower bound (AC114 rule 9).
- `state_hash` for every byte-identity comparison.

---

## 6. Gates (prespecified before confirmation; engineering informed shapes only)

Categorical and per-individual (AC114 rule 8). Seeds are the replication unit;
two histories are repeated measures (AC88). Every gate is stated per individual
(all 16 = 8 seeds × 2 histories must hold); paired gates are stated per matched
cell (16 cells = 8 seeds × 2 histories).

- **G1 (single-change license / composition direction 1).** Every final
  individual, at `simult`, intact boundary: `keep`, `rival`, `reference` are
  byte-identical (`state_hash`) to each other AND to AC105 `persistent_budget` at
  `simult`. Non-vacuous: `fw_at_corrupt == 8`, `successions >= 1`,
  `flipped_still_wrong == 0`.
- **G2 (D1 — link-specific admission).** Every matched cell, paired per seed:
  `puncture` (site) has alive-window channel-0 admission == 0 (every attempted
  channel-0 contact refused, and attempted > 0) AND `rival_puncture` (count) has
  alive-window channel-0 admission > 0. Only the gate differs.
- **G3 (D2 — local admission).** Every final individual: `puncture_non_gate` has
  alive-window admission > 0 on BOTH channels.
- **G4 (T2 — boundary production supports entry).** Every final individual:
  `no_B` (site) has both gate links dead and alive-window admission == 0 on both
  channels (non-vacuous on the material channel) and does NOT complete;
  `no_B_retention_ref` (none) admits every contact on both channels and
  completes.
- **G5 (retention vs admission separated).** Every final individual:
  `no_B_retention` (site) has both gate links dead and alive-window admission ==
  0 on both channels and does NOT complete; `no_B_retention_ref` (none) admits
  and completes. The retention rescue restores retention but NOT admission.
- **G6 (endogenous renewal vs external).** Every final individual: `keep` has
  `B_births > 0`, `external_B == 0`, `particle_export == 0`; `B_rescue` has
  `external_B > 0`, `B_births == 0`, and completes (labelled EXTERNAL).
- **G7 (composition under stress — the novel gate).** Every final individual:
  `rival_puncture_simult` (count) reconstructs (`fw_at_corrupt == 8` and
  `flipped_still_wrong == 0`), holds the description (`description_correct == 130`
  and `successions >= 1`), and completes; AND, paired per seed, `puncture_simult`
  (site) has alive-window channel-0 admission == 0 after the puncture under the
  same corruption+move challenge.
- **G8 (completeness + determinism).** Row count == 8 seeds × 2 histories × 13
  arms; a sampled exact rerun is byte-identical (`state_hash`).

**Reported, not gated:** survival (bimodality-aware lower bound), route holding
(lower bound), the puncture leak (export), `permeant`, the per-mechanism endpoint
tables, `mat_at_corrupt`, and each seed's priority (measured covariate).

---

## 7. Cohort, analysis units, and stopping rule

- **Engineering:** seeds 0–7 (16 individuals, both histories). Informed the gate
  shapes only; DISCLOSED here and excluded from the final sample.
- **Finals:** seeds **6600–6607** (16 individuals, both histories) — untouched,
  disjoint from the engineering cohort and from every prior final family
  (0–7, 8–15, 16–23, 1300–1303, 1800–1803, 1900–1903, 2800–2803, 2900–2903,
  3300–3311, 3400–3411, 3500–3511, 4004–4031, 4052/4054/4096/4110, 4300–4303,
  4408–4451, 4466/4481/4504/4510, 4600–4871, 4872–5099, 5100–5507, 5600–5607,
  5700–5707, 5800–5807, 5900–5907, 6000–6007, 6100–6107, 6200–6207, 6300–6307,
  6400–6407, 6500–6507). Run ONCE after this protocol is hashed. NOT screened
  (no outcome observed before the freeze).
- **Analysis units (reported separately).** (i) Independent seeds: 8. (ii)
  Arm-runs (rows): 208 = 8 × 2 × 13. (iii) Matched comparisons: paired per
  (seed, history) cell — 16 cells per paired gate. Histories are repeated
  measures, not independent units; the two move schedules share the
  corruption+first-move tick, so a finding on both schedules is one seed's
  mechanism firing, not two instances (AC105 errata). Gate denominators are
  stated per gate (per-individual 16, or matched cell 16).
- **Stopping rule.** G1 and G2 are decisive. If G1 fails, the build is defective
  (the gate changed the frozen economy with the boundary intact). If G2 fails,
  SR-2 has collapsed into SR-1 and the produced-interface ceiling is not earned:
  record the negative and stop, without weakening the criterion. G3–G7 failures
  are recorded with their measured values and NOT moved (AC16/AC17 discipline).
  A failed gate is never reclassified; the record keeps the measured value.

---

## 8. Unavoidable changes from the two precedents (documented, not hidden)

1. **Yields** `in_f = in_m = 64` (AC105) vs AC114's `in_f = 32` — discriminations
   transfer, intake scalars do not, and no AC114 frozen number is compared
   numerically.
2. **Horizon** 16,384 (AC105) vs 2,048 (AC114) — the alive-window discriminator
   is horizon-independent, but the puncture leak (AC114 rule 7) is lethal at this
   horizon.
3. **Organism** carries the bank-1 130-bit description, succession controller,
   reconstruction, operational memory, and allowance (AC105's organism) — this is
   the integration itself, not a concession.

No change is made to any frozen runner, protocol, result, or hash.

---

## 9. Disclosed caveats, carried as lower bounds (NOT gate requirements)

1. **The puncture leaks, and the long horizon makes it lethal** (I3 caveat 1):
   puncturing any link opens a hole (`puncture_non_gate` dies 12/16,
   `rival_puncture` 2/16 on engineering) via W/C leak. Admission and route
   holding are reported as lower bounds; survival and route holding are never
   folded into an admission gate.
2. **Description reads at the horizon are post-mortem for dying arms** (I3
   caveat 2): gate description integrity on survivors or
   `description_correct_at_death` (AC79), never on a dying arm's horizon read.
3. **Survival is bimodality-aware** (I3 caveat 3): the design's gates are
   categorical per-individual; no unconditional-survival claim is gated on one
   seed family (AC39).

---

## 10. Verification plan (split, per the AC9 pattern)

- **Audit** (`audit_ac115.py`): re-derives source hashes, row coverage, the
  G1–G8 gate verdicts, survival, and the keep-arm mechanism-exercise endpoints
  from the saved table WITHOUT simulating (stdlib only).
- **Replay** (`replay_ac115.py`): sampled exact reruns of frozen rows, compared
  field-by-field including `state_hash` (determinism/integrity check only).
- **Implementation tests** (`test_ac115.py`): level-1 gate/puncture law on the
  compiled react (yield 64/64, gate on actions 0/1, puncture candidate mask),
  level-2 organism-level consequences (G1 ac105 byte-identity on a sampled final
  seed, the four discriminations on engineering seeds, observer-discard
  byte-identity), plus the final-gate verdicts pinned as recorded-outcome
  regressions.

---

## 11. Frozen source of truth (hash set)

The frozen source set is the declaration plus the simulation code:

`AC115_PROTOCOL_v1.md`, `ac115.py`, and the frozen dependencies (`ac105.py`,
`ac104.py`, `ac103.py`, `ac102.py`, `ac101.py`, `ac100.py`, `ac99_d2.py`,
`ac99.py`, `ac97.py`, `ac96.py`, `ac95.py`, `ac76.py`, `ac71.py`, `ac12.py`,
`ac12_memory.py`, `ac9.py`, `ac9_priority_v2.py`, `ac9_memory.py`, `ac5.py`,
`ac5_program.py`, `ac4.py`, `ac4_transport.py`, `ac1.py`, `ac114.py`).

Verification tools (`test_ac115.py`, `audit_ac115.py`, `replay_ac115.py`) are
recorded separately and are NOT in the hash set, so a later improvement to a tool
does not drift the study (AC16/AC17 lesson). The design doc
`I2_INTEGRATED_EXCHANGE_DESIGN_v1.md` is a design artifact, not a frozen
dependency, and is likewise not in the finals hash set.

---

## Sources

`I2_INTEGRATED_EXCHANGE_DESIGN_v1.md`, `AC115_ENGINEERING_v1.md`,
`AC114_PROTOCOL_v1.md`, `AC114_RESULTS_v1.md`, `A1_EXCHANGE_SPEC_v1.md`,
`AC105_PROTOCOL_v1.md`, `AC105_RESULTS_v1.md`, `I1_BOUNDARY_CORRECTION_v1.md`,
`ac115.py`, `ac105.py`, `ac104.py`, `ac95.py`, `ac12.py`, `ac114.py`, `ac9.py`,
`ac4.py`. All code facts verified against the runner sources at the commit in
scope; no simulation run for this protocol.
