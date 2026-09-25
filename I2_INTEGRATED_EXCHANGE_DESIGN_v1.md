# I2 — Integrated boundary-exchange study: frozen design

2026-09-24. Design deliverable for the I2 card (t_6db797ac). Predecessors:
t_3eba13c2 (I0, `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`), t_cbdeceec (I1,
`I1_BOUNDARY_CORRECTION_v1.md`). This document freezes the design question, the
claim ceiling, the challenge set, and the controls. It runs nothing, edits no
frozen artifact, and writes no results. I3 (t_9bc216f5) implements the runner as
`ac115.py` (next available AC identifier) and issues a feasibility decision; I4
carries the scientific claims and freezes the protocol (`AC115_PROTOCOL_v1.md`).

Vocabulary: charter v2 (§5 substrate, §7a components), the closure criterion
(`references/closure-criterion.md`, K2/K3), `A1_EXCHANGE_SPEC_v1.md` (SR-2,
D1-D5, T1-T6), `AC114_PROTOCOL_v1.md`/`AC114_RESULTS_v1.md` (the SR-2 successor),
`AC105_PROTOCOL_v1.md`/`AC105_RESULTS_v1.md` (the integrated baseline).

---

## 0. The design question, stated first

> Can one organization renew its produced exchange boundary while sustaining the
> internal machinery and state that support reconstruction and continued
> production?

Reframed as a testable single-architecture claim: **does AC114's SR-2
link-specific admission gate compose with the AC105 five-mechanism closure
architecture?** Concretely, three evidence levels, in order:

1. **The admission law is implemented correctly** in the integrated organism
   (link-specific, not aggregate, and inert when the boundary is intact).
2. **Boundary production causally supports resource entry AND retention** in the
   integrated organism (the same produced links admit intake and retain
   constituents; killing B production kills both; a retention-only rescue does
   not restore admission).
3. **Those boundary functions compose with the integrated production and
   reconstruction network** (the gate does not disturb reconstruction,
   description turnover, succession coordination, operational memory, or the
   decision allowance; and the admission discriminations hold while those
   mechanisms are actively exercised).

The composition direction matters because the two precedents live on disjoint
lineages (I0 §1): AC114's gate is on the minimal AC9 body (no description store,
no succession, no reconstruction, no operational memory, no allowance), while the
five-mechanism closure is on AC105. No run today shows the exchange role riding
the produced boundary that the five-mechanism organism already maintains.

---

## 1. Claim ceiling (frozen; everything above this is a non-claim)

On untouched final seeds, the integrated successor realizes, in ONE organism and
one run:

- **link-specific admission** — channel-c intake is a function of the local
  live-state of `GATE_LINKS[c]` alone, not of the aggregate boundary count;
- **entry + retention through the produced boundary** — the same produced,
  finite-lived links admit the intake that funds production and retain the
  constituents; and
- **composition** — the boundary exchange role coexists with, and is sustained
  by, the five internalization mechanisms AC105 already composes
  (description turnover, succession coordination, reconstruction, internalized
  operational memory, decision allowance), which are preserved byte-for-byte at
  the intact boundary.

This is **one step above AC114's ceiling and one step below clause (ii)**. It
extends the material-layer closure (`{W, C, B}` retention + exchange, AC114's
licensed ceiling) by showing the exchange role composes with the informational
layer (the AC105 five-mechanism network). It is **not** a new closure claim — the
five-component K3 verdict already belongs to AC105 (I1 §1.3); this study
establishes only that the boundary-exchange extension rides that architecture.

Non-claims (unchanged from AC114 and the charter): not autopoiesis, not clause
(ii), not "alive", not a better boundary. Supplied coordinates and physical laws
are permitted substrate (I1 §3); the non-spatial informational core remains the
one genuine clause-(ii) limitation. No content self-production claim (AC78
blocked). No claim about optimal allocation or universal survival.

---

## 2. The single change, and the license that pins it

The ONLY addition is the SR-2 admission gate: `ac4.react` actions 0/1 credit
intake only while the channel's declared gate link is live (`if ADMIT(b,c):`),
where `ADMIT ∈ {site, count, none}`. `none` is the frozen always-admit behaviour
(the exchange bypass). The gate reads organism state (`b.boundary[GATE_LINKS[c]]`)
— no host state, no challenge-time knowledge. The aggregate B-count gate survives
only as the `count` comparison arm.

**The single-change license (G1):** with the boundary intact, the gate is never
exercised (gate links never reach lifetime 0 while B is produced, AC114 rule 1),
so the integrated `keep`/`rival`/`reference` arms must be byte-identical
(`state_hash`, ledger, final inventory) to each other **and to AC105's
`persistent_budget` at the `simult` condition**. That byte-identity is the
composition direction 1 — it proves the gate adds no resource competition and
disturbs none of the five mechanisms — and it is the same discipline AC105 uses
to inherit AC104 (AC105 G1).

**Base architecture (fixed):** AC105 `persistent_budget` — the full five-mechanism
candidate with the decision allowance (`DECISION_ALLOWANCE = 42`). The allowance
is one of the five mechanisms (I1 §4), so the base is the allowance-bearing arm,
not `persistent`. AC105's own `persistent` control (allowance absent) is out of
scope: the allowance's no-harm/rescue properties are AC105's frozen finding and
are re-used, not re-tested ("reuse unaffected evidence").

**Integration point (verified in code):** AC105's step is built by `ac95.build`,
which sets the step's `ac4` shim to `ac12.react_world()` and its base source to
`ac12.STEP_SRC` (= `ac9.step`). `ac95.build`'s surgery (RENEW_BLOCK, OUTCOME_LINE,
DAMAGE_LINE, ACTION_LINE, BALANCE_LINE) leaves the react's intake block and the
action-8 candidate line untouched, so AC114's react-level surgery (gate + action-8
candidate restriction) and step-level surgery (puncture zeroing, retention
rescue, external B, permeant) compose directly with the AC105 build. The runner
applies AC114's surgery primitives to `ac12.react_world()` and the AC105-built
step, not to `ac9.step` directly.

---

## 3. World constants (supplied, fixed at protocol time)

- `GATE_LINKS = {0: (0,), 1: (1,)}` — singleton gates (sharpest discrimination),
  inherited from AC114.
- `B_MIN = 10` — rival threshold (inert at count 20, cuts at 0, admits at 19).
- `PUNCTURE_LINKS = (0,)`, `NONGATE_PUNCTURE_LINKS = (5,)` — AC114's values.
- `TICKS = 16384` — AC105 horizon (AC114 used 2048; DISCLOSED change, §8).
- `CORRUPT_TICK = 8192`, `CORRUPT_BITS = 8` — AC105 baseline.
- Move schedule `[(8192, 'flip'), (12288, 'flip')]` — AC105 `simult`.
- **Yields: `YIELD_F = 64`, `YIELD_M = 64`** — AC105's reaction yields. This is
  a DISCLOSED difference from AC114's frozen `in_f = 32` (§8): the gate is
  yield-agnostic, so the discriminations transfer, but the intake SCALARS will
  differ from AC114's frozen numbers and must not be compared numerically.
- `PUNCTURE_TICK = 512` for the discrimination arms (mature organism, AC114 rule
  2), `= 8192` for the composition-stress arms (coincident with corruption + move).

---

## 4. Arms (12 required + 1 optional; the smallest set covering the four controls)

Every arm holds the AC105 `persistent_budget` mechanism fixed and varies only the
admission gate and the boundary intervention. `challenge` is either `none` (no
corruption, no move — the boundary is the sole event) or `simult` (corruption@8192
+ move@8192,12288 — the AC105 baseline).

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
| `permeant` (optional) | site | retention broken | none | exchange-only mirror (reported, not gated) |

`permeant` is the mirror of `no_B_retention` (retention broken, admission intact
→ export → death). Retention is inherited from AC10 (G2 field-for-field, AC114
rule 11) and re-shown by the `no_B`/`no_B_retention`/`no_B_retention_ref` triad
plus `keep`'s zero export, so `permeant` is a reported-not-gated mirror, not a
gated arm; I3 may include it for completeness but must not gate on it.

The surgery mapping is AC114's, unchanged in kind: the gate + action-8 candidate
restriction are react-level; the puncture zeroing (booked `B_discard`), the
retention-rescue kernel flag, `external_B_restore`, and the permeant mask are
step-level. `no_B` routes through the frozen arm guard (`action 8` suppressed).
No conservation identity is patched: `ac4.balance` carries `in_m`/`in_f` as
variables (the AC15 lesson), so gating them to 0 satisfies every identity by
construction.

---

## 5. The challenge set (bounded, exercising the integration dependencies)

Three conditions, each bounded, and each with a named causal target:

- **C1 — composition baseline (intact boundary, `simult`).** `keep`/`rival`/
  `reference`. The corruption + two moves are present, so reconstruction and
  succession are ACTUALLY exercised (not assumed): the runner must record
  `fw_at_corrupt == 8` → `flipped_still_wrong == 0` and `successions >= 1` per
  individual, alongside the byte-identity of G1. This is the "actual
  reconstruction and succession activity" requirement, not a survival check.
- **C2 — admission + boundary (no corruption, no move).** `puncture`,
  `rival_puncture`, `puncture_non_gate`, `no_B`, `no_B_retention`,
  `no_B_retention_ref`, `B_rescue`, (`permeant`). The boundary intervention is
  the sole event, so the admission and retention discriminations are isolated
  from the reconstruction/move challenge. Succession still runs (ambient
  description damage), which is the point: the five-mechanism organism is
  present, but its reconstruction path is unchallenged here.
- **C3 — composition stress (`simult` + puncture @8192).** `puncture_simult`,
  `rival_puncture_simult`. Corruption, move, and boundary puncture coincide, so
  the admission discrimination is asked to hold THROUGH active reconstruction
  and succession.

The challenge set is bounded (12-13 arms, three conditions) and deliberately does
NOT reproduce every historical study: retention continuity (AC10 G2), the
allowance's operating range (AC105), and the succession/coordination coherence
(AC87/88/95) are re-used with the rationale above, not re-run.

---

## 6. Controls (the four required distinctions, and which arms realize them)

1. **Link-specific admission vs exchange bypass vs aggregate gate.** `site`
   (`keep`, `puncture`) vs `none` (`reference`, `no_B_retention_ref`) vs `count`
   (`rival`, `rival_puncture`). The `site`/`count` pair under an identical
   puncture is the D1 discriminator; `none` is the frozen always-admit bypass.
2. **Retention loss vs admission loss.** `no_B` (both lost) vs `no_B_retention`
   (retention rescued by the kernel flag, admission still lost because the gate
   links are dead) vs `no_B_retention_ref` (no gate: retention rescued AND
   admission retained). The `no_B_retention` vs `no_B_retention_ref` pair is the
   cleanest exchange-mediation control (AC114 rule 6): identical except the gate.
3. **Endogenous renewal vs external restoration.** `keep` (endogenous B-birth
   turnover) vs `B_rescue` (external B, `B_birth == 0`). `B_rescue` is labelled
   EXTERNAL and never counted as autonomous.
4. **Baseline behaviour vs integration-induced resource competition.** The
   intact-boundary `keep` arm is byte-identical to AC105 `persistent_budget`
   (G1): the gate adds no resource competition when inert. The composition-stress
   pair (C3) then shows the gate's income effect is the gate, not an
   integration artifact.

---

## 7. Endpoints (measured per individual, reported separately)

- **Admission (the I1-corrected discriminator).** NOT aggregate post-onset
  intake (which AC114 G3 showed is post-mortem). Record, per channel, in the
  alive window `[first_gate_dead, first_dead]`: `attempted` (channel-c contacts
  with port match), `admitted`. This is the mechanism; death is a consequence.
  Where corruption coexists with the puncture (C3), the admission comparison is
  per contact-attempt with the action forced (AC15 lesson 6), never aggregate
  income, because corruption changes which actions the program chooses.
- **Retention/export.** `particle_export`, `B_birth`, `external_B`, `B_discard`.
- **Production.** `W_birth`, `C_birth`, `B_birth`, `converted`.
- **The five mechanisms (composition endpoints, never folded).** reconstruction
  (`fw_at_corrupt`, `recovery_tick`, `flipped_still_wrong`), description turnover
  + coordination (`successions`, `description_correct`, `ctrl_idle_end`),
  operational memory (`register`, `relinquishments`, `streak_final`), decision
  allowance (`allowance_breached`, `mat_min_post_corrupt`), and production
  (`births_by_window`).
- **Survival/activity.** `completed`, `first_dead`, `first_gate_dead` (chrono),
  reported as a bimodality-aware lower bound (AC68), never folded into an
  admission gate. Route holding reported as a lower bound (AC114 rule 9).
- `state_hash` for every byte-identity comparison.

---

## 8. Unavoidable changes from the two precedents (documented, not hidden)

1. **Yields.** AC105's reaction yields are `in_f = 64, in_m = 64` (via
   `ac12.react_world()` with `YIELD_F = 64`); AC114's frozen `ac4.react` uses
   `in_f = 32`. The integrated study keeps AC105's yields (the base). The gate is
   yield-agnostic; the DISCRIMINATIONS transfer, the intake scalars do not, and
   no AC114 frozen number is compared numerically.
2. **Horizon.** `TICKS = 16384` (AC105) vs AC114's 2048. The discrimination is
   measured in the alive window, which is horizon-independent.
3. **Organism.** The integrated organism carries the bank-1 130-bit description,
   succession controller, reconstruction, operational memory, and allowance
   (AC105's organism), unlike AC114's `ac9.acquire` which zeroes `traces[1:]`.
   This is the integration itself, not a concession.
4. **Base arm.** `persistent_budget` (allowance present), not `persistent`. The
   allowance is one of the five mechanisms being composed.

No change is made to any frozen runner, protocol, result, or hash. AC114 and
AC105 and every earlier freeze are untouched.

---

## 9. Gates (prespecified shapes; I4 carries the verdicts, I2 freezes the shapes)

Categorical and per-individual (AC114 rule 8: deterministic mechanism, not a
statistical margin). Seeds are the replication unit; two histories are repeated
measures (AC88). Every gate is stated per individual (all 16 must hold).

- **G1 (single-change license / composition direction 1).** Every final
  individual, at `simult`, intact boundary: `keep`, `rival`, and `reference` are
  byte-identical (`state_hash`, ledger, final inventory) to each other AND to
  AC105 `persistent_budget` at `simult`. Non-vacuous: the corruption is applied
  (`fw_at_corrupt == 8`) and reconstruction + succession are recorded active.
- **G2 (D1 — link-specific admission).** Every final individual, paired per seed:
  `puncture` (site) has alive-window channel-0 admission == 0 (every attempted
  channel-0 contact refused) AND `rival_puncture` (count) has alive-window
  channel-0 admission > 0. The two arms share seed, stream, and puncture; only
  the gate differs.
- **G3 (D2 — local admission).** Every final individual: `puncture_non_gate` has
  alive-window admission > 0 on BOTH channels (a non-gate puncture blocks neither).
- **G4 (T2 — boundary production supports entry).** Every final individual:
  `no_B` (site) has gate links dead and alive-window admission == 0 and does NOT
  complete; `no_B_retention_ref` (none) has alive-window admission == every
  contact admitted and completes. The admission ledger while alive is the
  mechanism, not the death scalar.
- **G5 (retention vs admission separated).** Every final individual:
  `no_B_retention` (site) has gate links dead and alive-window admission == 0 and
  does NOT complete; `no_B_retention_ref` (none) admits and completes. The
  retention-rescue (kernel flag) restores retention but NOT admission, because
  the gate links are still dead (no B produced) — retention loss and admission
  loss are separated.
- **G6 (endogenous renewal vs external).** Every final individual: `keep` has
  `B_birth > 0` and `external_B == 0` and `particle_export == 0` (endogenous
  turnover; the same links retain and admit — D3, reported); `B_rescue` has
  `external_B > 0` and `B_birth == 0` and completes (labelled EXTERNAL).
- **G7 (composition under stress — the novel gate).** Every final individual:
  `rival_puncture_simult` (count) reconstructs (`fw_at_corrupt == 8` and
  `flipped_still_wrong == 0`), holds the description (`description_correct == 130`
  and `successions >= 1`), and completes; AND, paired per seed, `puncture_simult`
  (site) has alive-window channel-0 admission == 0 after the puncture under the
  same corruption+move challenge. The count arm's `fw → 0` and `successions >= 1`
  are the proof reconstruction and succession are ACTUALLY exercised; the site
  arm's zero admission is the discrimination holding through that activity.
- **G8 (completeness + determinism).** Row count == 8 seeds × 2 histories ×
  N arms; a sampled exact rerun of the first row is byte-identical (`state_hash`).

**Reported, not gated:** survival (bimodality-aware lower bound), route holding
(lower bound), the puncture leak (export, AC114 rule 7), the per-mechanism
endpoint tables, `mat_at_corrupt`, and each seed's priority (measured
covariates). If G1 fails, the build is defective (the gate changed the frozen
economy with the boundary intact); if G2 fails, SR-2 collapsed into SR-1 and the
produced-interface ceiling is not earned. A failed gate is recorded with its
measured value and NOT moved (AC16/AC17 discipline).

---

## 10. Anti-drift and verification (carried forward)

- Runner creates `ac115_results_v1/` with `mkdir(exist_ok=False)`; engineering in
  its own labelled directory; finals on a fresh seed range disjoint from every
  prior family (0-7, 2800-2803, 4300-4303, 4408-4411, 4412-4439, 4440-4443,
  4444-4447, 4448-4451, 4466/4481/4504/4510, 4600-4871, 4872-5099, 5100-5507,
  5600-5607, 5700-5707, 5800-5807, 6500-6507), NOT screened.
- The frozen hash set is the declaration (`AC115_PROTOCOL_v1.md`) + the runner and
  its frozen dependencies (the AC105 SOURCES list plus `ac114.py` if its surgery
  primitives are imported). Verification tools (`test_ac115.py`,
  `audit_ac115.py`, `replay_ac115.py`) are NOT hashed (AC17 rule).
- `ac115.py` reproduces AC105 `persistent_budget` at `simult` byte-for-byte (G1)
  BEFORE any gate/puncture is applied, as the single-change license.
- Engineering first (seeds 0-7, plus the AC105 diagnostic seeds 5603/5607 for the
  marginal economy), then the frozen protocol, then disjoint finals. Engineering
  informs gate shapes only; no final outcome is observed before the freeze.
- I3 must additionally: run observer-discard on the integrated candidate (the
  `keep` arm), audit for new host-side state, and expose any challenge-time or
  challenge-location knowledge (none is permitted in the operational code). The
  gate's `ADMIT` reads organism state only; the puncture tick is a module
  constant applied by the run loop, as in AC114.

---

## Sources

`ARCHITECTURE_BY_CLAIM_MATRIX_v1.md` (I0), `I1_BOUNDARY_CORRECTION_v1.md` (I1),
`AC114_PROTOCOL_v1.md`, `AC114_RESULTS_v1.md`, `A1_EXCHANGE_SPEC_v1.md`,
`A2_BOUNDARY_VERDICT_v1.md`, `AC105_PROTOCOL_v1.md`, `AC105_RESULTS_v1.md`,
`CLOSURE_VERDICT_v1.md`, `DEFINITIONS_CHARTER_v2.md`,
`ac105.py`, `ac104.py`, `ac95.py`, `ac12.py`, `ac71.py`, `ac99_d2.py`, `ac9.py`,
`ac4.py`, `ac114.py`. All code facts verified against the runner sources at the
commit in scope; no simulation run for this design.
