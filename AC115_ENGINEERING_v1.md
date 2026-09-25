# AC115 (I3, engineering): the integrated successor — feasibility decision

2026-09-24. Engineering deliverable for the I3 card (t_9bc216f5). Predecessor:
I2 (t_6db797ac, `I2_INTEGRATED_EXCHANGE_DESIGN_v1.md`). This document reports the
engineering build, its verification, and the feasibility decision for I4
(confirmation + `AC115_PROTOCOL_v1.md`). Nothing here is a freeze: no protocol, no
final seeds, no confirmatory claim.

Runner: `ac115.py`. Results: `ac115_engineering_v1/` (208 rows = 8 seeds × 2 histories
× 13 arms, 16,384 ticks). Engineering seeds 0-7, disjoint from every prior family.

---

## 1. What was built

`ac115.py` places AC114's SR-2 link-specific admission gate into the AC105
five-mechanism closure architecture, in ONE organism and ONE run. The base is AC105
`persistent_budget` at `simult` (corruption@8192 + move@8192,12288, TICKS=16384,
`DECISION_ALLOWANCE=42`). The only addition is the gate on `ac4.react` actions 0/1:

    ADMIT(b, c) ∈ {site, count, none}

- `site`: admit iff channel c's declared gate link is live (`b.boundary[GATE_LINKS[c]] > 0`).
- `count`: the aggregate rival (live links ≥ `B_MIN=10`).
- `none`: the frozen always-admit bypass.

The gate reads organism state only (`b.boundary`). Yields are AC105's (`in_f=64`,
`in_m=64`), a disclosed difference from AC114's frozen `in_f=32` (I2 §8.1): the gate is
yield-agnostic, so the discriminations transfer and the intake scalars do not.

Composition method (I2 §2): `build_integrated` reproduces `ac95.build`'s surgery
verbatim and then applies AC114's boundary primitives at the SAME markers (`B_EXPIRY_LINE`
for the puncture zeroing + external-B; the transport call for retention-rescue/permeant),
with `ac12.react_world()` replaced by a gated react carrying the admission gate and the
action-8 puncture candidate mask. No conservation identity is patched (`ac4.balance`
carries `in_m`/`in_f` as variables — the AC15 lesson).

## 2. The single-change license (G1) — gate inert at intact boundary

`keep`/`rival`/`reference` are byte-identical (`state_hash`) to each other AND to AC105
`persistent_budget` at `simult` on all 16 individuals (8 seeds × 2 histories). The gate
never fires with the boundary intact (action 8 preferentially heals the most-depleted
link, AC114 rule 1), so the gated react produces the identical event ledger and state
digest. Non-vacuous: the corruption is applied (`fw_at_corrupt == 8`) and reconstruction +
succession are recorded active on every individual (recovery tick 8193-8201, `successions`
= 6, `flipped_still_wrong == 0`).

This is composition direction 1 — the gate adds no resource competition and disturbs none
of the five mechanisms when inert — and it is the same discipline AC105 uses to inherit
AC104.

## 3. The five mechanisms are exercised in one organism (the `keep` arm)

| mechanism | endpoint | measured (16 individuals) |
| --- | --- | --- |
| controller reconstruction | `fw_at_corrupt` / `flipped_still_wrong` | 8 → 0 on all 16 |
| description/recipe succession | `successions`, `description_correct` | 6 cycles, 130/130 on all 16 |
| operational memory + decision allowance | `relinquishments`, `register` | 2 relinquishments / individual; register majority-clean |
| paid operational-state updates | `reg_writes` / `succ_writes` / `ctrl_writes` | 2300-2419 / 2677-2689 / 1675-1689 |
| boundary + production | `B_births`, `particle_export` | 1674-1679 B births, 0 export |

Reconstruction recovers 8193-8201 ticks after the corruption; the description holds at
130/130 through 6 successor copies; the boundary turns over ~1670 births (vs a 20-link
complement) with zero export. All five mechanisms run in the same body that is also
contacting the environment and renewing its boundary.

## 4. Boundary exchange: the four discriminations hold

Alive-window admission is the I1-corrected discriminator (per channel, per contact,
measured from the gate link's death/puncture to first death; never aggregate post-onset
intake, never post-mortem — AC114 rule 12).

- **D1 link-specific (G2)**: `puncture` (site, link 0 dead @512) admits 0 of its 65-68
  channel-0 attempts; `rival_puncture` (count, same puncture) admits 98/98. Paired per
  seed, 16/16.
- **D2 local (G3)**: `puncture_non_gate` (link 5 dead) admits > 0 on BOTH channels, 16/16
  (the non-gate puncture blocks neither channel).
- **T2 boundary-supports-entry (G4)**: `no_B` (site, B suppressed) gate links dead
  (t≈127-133), 0 admitted on both channels, dies 255-360; `no_B_retention_ref` (none) admits
  every contact (ch0 186/186, ch1 ≈880/882) and completes. The same produced links admit
  intake; killing B production kills entry.
- **Retention vs admission separated (G5)**: `no_B_retention` (site, retention rescued by
  the kernel flag) still admits 0 (gate links dead) and dies 377-383 with zero export; the
  `no_B_retention` vs `no_B_retention_ref` pair is the cleanest exchange-mediation control
  (AC114 rule 6) — identical except the gate.
- **Endogenous vs external (G6)**: `keep` `B_births > 0`, `external_B == 0`, `export == 0`;
  `B_rescue` `external_B > 0`, `B_births == 0`, completes (labelled EXTERNAL).

## 5. Composition under stress (G7) — the novel gate

`rival_puncture_simult` (count, link 0 dead @8192 under corruption + move) reconstructs
(`fw 8 → 0`), holds the description (130/130, 6 successions), and completes, 16/16;
`puncture_simult` (site, same challenge) admits 0 channel-0 contacts after the puncture
(50-106 attempts, all refused) while its reconstruction still completes (recovery 8193-8201)
and its description is intact at death (130). The admission discrimination holds THROUGH
active reconstruction and succession, and the site arm's death (8274-8332) is the boundary
block (fuel starvation), not a reconstruction failure.

## 6. State sufficiency and host-side audit

- **Observer-discard** on the integrated candidate (`keep`): 16/16 per-tick AND terminal
  byte-identical (all 16,384 ticks). The gate adds no host state — `ADMIT` reads
  `b.boundary` only — so state sufficiency is a property of the maintained substrate.
- **Audit** (`_ac115_audit.py`): the injected react/step fragments (gated intake,
  puncture candidate mask, transport call, `puncture_gate`, `external_B_restore`) contain no
  challenge-time or challenge-location token; the budget rule is a pure function of
  (material, allowance); the gate reads organism state only. The corruption tick, move
  schedule, and puncture tick are module constants applied by the run loop, exactly as in
  AC114/AC105.

## 7. Gates (engineering cohort, prespecified shapes from I2 §9)

All eight pass on all 16 individuals (a gate is per-individual; 8 seeds × 2 histories).

| gate | result |
| --- | --- |
| G1 single-change license (byte-identity to AC105 `persistent_budget`) | PASS 16/16 |
| G2 D1 link-specific admission | PASS 16/16 |
| G3 D2 local admission | PASS 16/16 |
| G4 T2 boundary-supports-entry | PASS 16/16 |
| G5 retention-vs-admission separated | PASS 16/16 |
| G6 endogenous-vs-external | PASS 16/16 |
| G7 composition-under-stress | PASS 16/16 |
| G8 completeness + determinism (sampled exact rerun) | PASS |

## 8. Disclosed caveats (carried to I4; not gate failures)

1. **The puncture leaks, and the long horizon makes it lethal.** Puncturing any link (gate
   or non-gate) opens a hole: `puncture_non_gate` dies 12/16 (1686-14410) and
   `rival_puncture` 2/16 (seed 5, both histories, t=2215) via W/C leak, while their
   admission discriminations still hold. AC114 ran TICKS=2048; this study runs 16,384
   (I2 §8.2), so the leak (AC114 rule 7) has time to kill. Admission and route-holding are
   reported as lower bounds, never folded into an admission gate.
2. **Description reads at the horizon are post-mortem for the dying arms** (`description_correct`
   41-98/130); `description_correct_at_death == 130` on all 16 dying individuals confirms
   the description is intact at death and degrades only after the paid repair stops (AC79).
   The gates read the correct endpoint (surviving arms) or `description_correct_at_death`.
3. **Survival is bimodality-aware.** `keep`/`reference`/`rival`/`rival_puncture_simult`/
   `no_B_retention_ref`/`B_rescue` complete 16/16 on this engineering family; the design's
   gates are categorical per-individual (AC114 rule 8), and I4 must not gate an unconditional
   survival claim on one seed family (AC39).

## 9. Feasibility decision

**FEASIBLE for confirmation.** The integrated successor exists (`ac115.py`), and every
claimed mechanism is reachable AND exercised in one organism: boundary renewal (B birth
turnover with zero export), resource admission + constituent retention (the site gate's
alive-window discriminations), controller reconstruction (fw 8 → 0), description/recipe
succession (6 cycles, 130/130), and paid operational-state updates (register, relinquishment,
succession controller writes) — all while the SR-2 gate's four discriminations hold, the
single-change license (G1 byte-identity to AC105) is verified, the observer-discard is
per-tick byte-identical (no host state, no challenge-time/location knowledge in the
operational code), and all eight prespecified gates pass uniformly on 16 individuals.

The next step is I4: write `AC115_PROTOCOL_v1.md` (hashing the declaration + runner + frozen
dependencies, excluding verification tools — AC16/AC17), select a disjoint untouched final
seed family, and freeze the confirmation. The design's disclosed leak (caveat 1) and the
horizon transfer (caveat 3) are the two things the protocol must carry as lower-bound
caveats rather than gate requirements.

## Sources

`I2_INTEGRATED_EXCHANGE_DESIGN_v1.md`, `AC114_PROTOCOL_v1.md`, `AC114_RESULTS_v1.md`,
`AC105_PROTOCOL_v1.md`, `AC105_RESULTS_v1.md`, `A1_EXCHANGE_SPEC_v1.md`,
`ac115.py`, `ac105.py`, `ac104.py`, `ac95.py`, `ac12.py`, `ac114.py`, `ac9.py`, `ac4.py`.
All code facts verified against the runner sources at the commit in scope; engineering run
recorded in `ac115_engineering_v1/` with `pre_run_snapshot.json`.
