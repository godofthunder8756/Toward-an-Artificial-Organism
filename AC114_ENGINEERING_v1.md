# AC114 — SR-2 boundary-exchange successor: engineering v1

2026-09-24. Engineering deliverable for the A2 card (t_e7781faf): *build the
minimal versioned successor that realizes the A1 exchange model (SR-2) with
interventions that identify local mediation vs a global B-count gate.* No
frozen study, no final seeds, no protocol freeze — that is A3's card. This
document records the build, the two evidential levels, the engineering cohort
results, and the failures/caveats A3 must carry into its protocol.

Every code fact is read from the frozen sources at HEAD `57ca900` (`ac4.py`,
`ac4_transport.py`, `ac9.py`, `ac10.py`); the successor is `ac114.py` and its
tests `test_ac114.py`. Vocabulary: charter v2 (§5 substrate, §7a components),
`A1_EXCHANGE_SPEC_v1.md` (SR-2), `A2_BOUNDARY_VERDICT_v1.md`.

---

## 0. The answer, stated first

The successor is a single, local change to a supplied reaction: **`ac4.react`
actions 0/1 now credit intake only while the channel's declared gate link(s)
are live**, instead of unconditionally. The aggregate B-count gate survives as
a comparison arm (`rival`). The engineering cohort (seeds 0-7 × 2 histories =
16 individuals per arm) shows every discriminating prediction holds **uniformly
across all 16 individuals**, with no tuning:

- **T5 (inertness):** `keep`, `reference`, and `rival` are byte-identical
  (`state_hash`, `ledger`, `final_inventory` all equal) in ordinary operation —
  the site gate is the only change, and it is never exercised while the
  boundary is intact.
- **D1 (decisive, location-matched):** on the identical punctured state (gate
  link 0 dead, 19 links live), the site gate gives post-onset channel-0
  admission **0 in 16/16** (≈190 contact attempts, 0 productive), while the
  count gate gives **full yield in 16/16**. Only the gate differs.
- **D2 (local):** puncturing a *non-gate* link leaves both channels' admission
  unchanged and the organism survives 16/16.
- **T2 (exchange mediation):** retention rescued with the gate links dead
  (`no_B_retention`) dies 16/16 by fuel/energy starvation with intake at most
  one contact per channel; the gate-disabled twin (`no_B_retention_ref`)
  reproduces the frozen AC10 arm and survives 16/16.
- **T1 (retention continuity) + T6 (external rescue):** hold.

The two evidential levels are separated throughout: level 1 is the imposed
transport law verified deterministically (`test_ac114.py`, 22 tests); level 2
is the organism-level consequence that endogenous boundary production sustains
exchange and retention. Verifying the imposed gate does **not** discover its
causal law — that is stated explicitly.

---

## 1. The change (what SR-2 adds, and only that)

| Site | Frozen | SR-2 |
| --- | --- | --- |
| `ac4.react` action 0 | `e['in_f']=32` always | `if ADMIT(b,0): e['in_f']=32` |
| `ac4.react` action 1 | `e['in_m']=64` always | `if ADMIT(b,1): e['in_m']=64` |

`ADMIT` is one of three functions injected into the compiled react's namespace:

- `_admit_site(b,c)`: `(b.boundary[GATE_LINKS[c]] > 0).any()` — **SR-2**.
- `_admit_count(b,c)`: `(b.boundary > 0).sum() >= B_MIN` — **the rival**.
- `_admit_none(b,c)`: `True` — **continuity / exchange bypass**.

World constants (supplied, charter §5, fixed at protocol time): `GATE_LINKS =
{0:(0,), 1:(1,)}` (singleton gates), `B_MIN = 10` (inert in ordinary operation,
cuts at count 0, admits at the punctured count 19), `YIELD = {0:32, 1:64}`
(frozen). The contact cost (1 energy) is paid whether or not admission
succeeds, so a dead interface is strictly costly — the frozen failure branch.

**No law patching.** `ac4.balance` carries `in_m`/`in_f` as variables, so
gating them to 0 satisfies every conservation identity by construction (the
AC15 lesson). The `ledger` integrity test confirms this for every arm.

---

## 2. The arm set (smallest set covering the seven required comparisons)

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

The puncture is a restriction of the action-8 candidate set (exclude the
punctured index) plus a one-time zeroing booked as `B_discard` — the same shape
as AC10's `no_B` (which excludes all), so the boundary-count identity holds.
`reference` and `no_B_retention_ref` reproduce the frozen `ac9.step` and the
frozen AC10 `no_B_retention` arm field-for-field (`state_hash` included).

---

## 3. Level 1 — the imposed transport law (deterministic)

`test_ac114.py`, 22 tests, all passing. The transport-law tests call the
compiled react on a controlled boundary state:

- site gate admits action 0 iff gate link 0 live; blocks (still pays 1 energy)
  iff dead; **ignores a non-gate hole**; blocks action 1 iff link 1 dead.
- count gate blocks below `B_MIN=10`, admits at 10, and is **site-indifferent**
  (19 links live with the gate link dead → still admits).
- disabled gate reproduces the frozen yield.
- puncture zeroes exactly its target, books a discard, and is **normal before
  onset** (the pre-onset step keeps link 0 alive).

This is the "verifying the implemented gate" level. It is not claimed to
independently discover the law — the law is imposed; the tests pin its shape.

---

## 4. Level 2 — organism-level results (engineering cohort)

16 individuals per arm (seeds 0-7 × 2 histories), 2048 ticks, 176 runs, 40.5 s.

| Arm | Survive | in_f (total) | in_m (total) | post-onset in_f | export | B_birth | external_B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `keep` | 16/16 | 608 | 3136 | 448-480 | 0 | 200-207 | 0 |
| `reference` | 16/16 | 608 | 3136 | 448-480 | 0 | 200-207 | 0 |
| `rival` | 16/16 | 608 | 3136 | 448-480 | 0 | 200-207 | 0 |
| `no_B` | 0/16 | 32 | 64 | 0 | 4-10 | 0 | 0 |
| `no_B_retention` | 0/16 | 32 | 64 | 0 | 0 | 0 | 0 |
| `no_B_retention_ref` | 16/16 | 544 | 2688-2752 | 416 | 0 | 0 | 0 |
| `permeant` | 0/16 | 0-96 | 0-512 | 0 | 7-90 | 0-24 | 0 |
| `B_rescue` | 16/16 | 544 | 2688-2752 | 416 | 0 | 0 | 160 |
| `puncture` | 0/16 | 128-160 | 704-896 | **0** | 1-5 | 49-60 | 0 |
| `rival_puncture` | 16/16 | 480-608 | 2176-3328 | **352-480** | 29-61 | 191-198 | 0 |
| `puncture_non_gate` | 16/16 | 544-608 | 2752-3264 | 384-480 | 27-48 | 194-200 | 0 |

The three "intact" arms (`keep`/`reference`/`rival`) are **byte-identical**
(equal `state_hash`, `ledger`, `final_inventory`): in ordinary operation the
gate links never reach 0 (action 8 preferentially heals the most-depleted
link), so the site gate is never exercised — the strongest possible inertness
evidence.

**T2, the exchange-mediation claim.** `no_B_retention` (site) and
`no_B_retention_ref` (no gate) are identical in every respect except the gate.
Both have zero B production and zero export (retention rescued); both see their
gate links die at t=133 (endowment decay). The site gate then cuts intake: total
intake is exactly **one contact per channel** (32 fuel + 64 material, all before
t=133), and the organism dies at t≈380 with fuel 0, energy 0, material ~60. The
reference twin keeps admitting (544 fuel + 2752 material) and survives 16/16.
The admission ledger, not a death scalar, is the mechanism.

**D1, the decisive location-matched test.** On the identical puncture (link 0
dead, 19 links live, applied at t=512 on a mature organism), the site gate and
the count gate disagree exactly as SR-2 predicts:

- `puncture` (site): post-onset channel-0 admission **0 in 16/16** — ≈190
  contact attempts, **0 productive** — then death by fuel/energy starvation
  (fuel 0, energy 0, material ≈100 not depleted).
- `rival_puncture` (count): post-onset channel-0 admission **352-480 in 16/16**
  (≈11-15 productive fuel contacts), surviving 16/16.

The two arms share the same seed, the same exogenous stream, and the same
puncture; only the gate differs. The `puncture` death signature (fuel 0, energy
0, material intact, ~190 denied fuel contacts) is the AC13 attention-hijack: the
fuel cut holds obs bit 0 set, the program loops on action 0, and material is
never spent. That is a *consequence* of the fuel cut, not a confound of the
admission measurement.

**D2, local admission.** `puncture_non_gate` (non-gate link 5 punctured) leaves
both channels' admission at full yield (in_f 544-608, in_m 2752-3264) and
survives 16/16. A single gate-link hole cuts a whole channel; a single non-gate
hole does not. This is what "local" means and what the count gate cannot
express.

**Semipermeability mirror.** `permeant` (B intact → gate links live early →
exchange present; particles permeant → retention broken) dies 16/16 by export
(7-90 particles leaked), the mirror image of `no_B_retention`. Retention and
exchange are separately load-bearing and both ride the produced B.

**Interruption and external rescue.** `no_B` dies 16/16 with zero B production,
zero post-onset intake, and export (both functions lost). `B_rescue` restores
retention (export 0) and exchange (full intake) with zero internal births and
`external_B=160` — labelled EXTERNAL, never counted as autonomous.

---

## 5. Failures, caveats, and resource constraints (recorded, not hidden)

1. **The `puncture` death is attention-hijack-shaped.** It does not falsify
   D1 (the admission signal is clean), but A3 must read the *admission ledger*
   (`assay['in_f']` / `assay['productive']`), not a death scalar, when gating
   D1. Death is a consequence, not the mechanism.
2. **`permeant` dies fast (t≈210-505)** with minimal intake (0-96 fuel), so the
   "exchange present" side of the mirror is present-but-brief. The mirror is
   established by the *export* endpoint (7-90 leaked), not by sustained intake.
3. **Two `rival_puncture` individuals (seed 4 h1, seed 7 h1) lose their acquired
   routes** (`[null,null]`) while surviving — the link-0 hole leaks enough W/C
   to starve renewal. Route holding is not gated here; survival and admission
   are. A3 should report route holding as a lower bound, not a gate.
4. **The puncture leaks** (export 1-5 in `puncture`, 29-61 in
   `rival_puncture`/`puncture_non_gate`). "Retention changes only trivially"
   (A1 D1's wording) is **not** byte-exact — one hole leaks substantially, as
   AC4 transport already showed (one-hole 35.4%). The D1/D2 claims concern
   *admission*, and the leak is a disclosed side effect, not a hidden rescue.
5. **B_MIN=10 is a supplied choice**, documented at §1, not tuned against
   results. It is inert in ordinary operation (count is always 20) and admits
   at the punctured count (19) — the two properties the rival needs to be a
   non-strawman. Any B_MIN in [2,19] has both; 10 is "half the perimeter".

No repeated tuning was used to make seeds survive: the surviving arms
(`keep`/`reference`/`rival`/`no_B_retention_ref`/`B_rescue`/`rival_puncture`/
`puncture_non_gate`) are the ones the design predicted to survive, and the
dying arms (`no_B`/`no_B_retention`/`permeant`/`puncture`) the ones it predicted
to die, in 16/16 uniform agreement.

---

## 6. What A3 freezes (handoff)

- **Runner:** `ac114.py` (the SR-2 site gate), `test_ac114.py` (level 1). The
  frozen source of truth for A3's snapshot is `ac114.py` + the frozen
  dependencies (`ac9.py`, `ac9_priority_v2.py`, `ac9_memory.py`, `ac5.py`,
  `ac5_program.py`, `ac4.py`, `ac4_transport.py`, `ac1.py`). Verification tools
  (`test_ac114.py`) are recorded but, per the AC16/AC17 lesson, their later
  edits must not drift the study's hash set.
- **Constants to fix:** `GATE_LINKS={0:(0,),1:(1,)}`, `B_MIN=10`,
  `YIELD={0:32,1:64}`, `PUNCTURE_LINKS=(0,)`, `NONGATE_PUNCTURE_LINKS=(5,)`,
  `ONSET=512`, horizon 2048.
- **Gates to prespecify (engineering-informed, frozen before finals):**
  - T5: `keep == reference` and `rival == reference` (`state_hash` equality).
  - T1: `no_B_retention_ref` reproduces the frozen AC10 `no_B_retention` rows.
  - T2: `no_B_retention` post-gate-death intake is 0 and it dies; the twin
    survives — gate the *admission ledger*, not death.
  - D1: `puncture` post-onset `in_f == 0` per individual; `rival_puncture`
    post-onset `in_f > 0` per individual (paired, per seed).
  - D2: `puncture_non_gate` post-onset `in_f > 0` and `in_m > 0`.
  - T6: `B_rescue` `external_B > 0`, `B_birth == 0`, `export == 0`.
  - Survival is a SEPARATE outcome (bimodality-aware lower bound, AC68), never
    folded into the admission gates.
- **Seeds:** engineering here used 0-7; A3 must use **untouched** final seeds
  (disjoint from 0-7) and an analysis on the actual independent units (seeds ×
  histories is 2 independent units per seed, per the AC88 lesson).

---

## Sources

`ac114.py`, `test_ac114.py`, `ac4.py` (`react` actions 0/1, `balance`),
`ac4_transport.py` (`crossing_link`, 20 links), `ac9.py` (`step` contact path),
`ac10.py` (surgery pattern, `no_B_retention`/`B_rescue`/`permeant`),
`A1_EXCHANGE_SPEC_v1.md` (SR-2, D1-D5, T1-T6), `A2_BOUNDARY_VERDICT_v1.md`.
Frozen results reproduced: `ac10_results_v1/rows.jsonl` (`keep`,
`no_B_retention`). Runtime verification: `_a1_verify_links.py` (link indexing),
`test_ac114.py` (22 tests).
