# AC91 protocol v1: production-dependencies test — can the organization replace the finite-lived components enabling reconstruction and coordination?

STATUS: **frozen before the first final seed.** Written 2026-09-18. This is a NEW experiment, not
a re-run: it measures whether the *produced, finite-lived machinery* that enacts reconstruction and
coordination — the W repair catalyst — is itself produced and replaceable, which is the decisive
next question after the accepted internal-state milestone (AC86-89). Full autopoiesis is not
claimed by declaring the succession mechanism "substrate" (a modeling choice the review left
unresolved); this study measures the production of the machinery instead.

SOURCES (declared): ac91.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC91_PROTOCOL_v1.md

## The finite component list (fixed before the run; the produced-vs-supplied map)

Produced, finite-lived machinery (the components whose production is the question):

- **W repair catalysts** (4 slots, `life[:4]`, lifetime 64, born by action 6 via `birth(b, 0, …)`,
  expire after 64 ticks, autocatalytic — a birth needs a live W parent). W's specified capability,
  the per-action write cap `min(32, 8·available_W, energy, material)`, gates EVERY paid write on the
  reconstruction and coordination paths: reconstruction (`reg_from_active`), description repair
  (`reg_description_active`), pointer repair (`reg_pointer`), controller-state repair (`reg_ctrl`),
  the succession slot copy/remove (`write_toward_slot`) and the pointer switch (`write_pointer`).
  W is therefore the produced machinery enabling BOTH target functions; no distinct coordinator
  component is introduced.
- **C converters** (4 slots, `life[16:20]`, lifetime 128, born by action 7): fuel→energy conversion.
- **B boundary** (20 sites, lifetime 256, born by action 8): retention.

Stored, maintained content (not machinery): the 130-bit description + 2-bit generation pointer +
18-bit controller state (bank 1), and the acquired 126-bit program (bank 0).

Supplied format-level machinery (the accepted boundary, `CLOSURE_BOUNDARY_v2.md`): the succession
state machine's transition logic `advance()` (copy → verify → switch → remove), the interpreter
`prog.choose`, the conservation laws, the observation function, the damage model, the world
constants. The controller-state transition write (`write_ctrl`) is the distinct-resource model
declared in AC88.

## The one declared change from ac89.py (everything else is byte-identical)

**The W-birth gate.** A new `make_birth(ns, cfg)` wraps `ac9.birth` and, when `cfg['block_W']` is
set, refuses bank-0 (W) births until `cfg['restore_tick']` (`None` = forever). Banks 1 and 2
(memory-region catalysts) are never touched, so the cut isolates exactly the W-birth reaction. The
gate is injected into the step namespace ONLY for the three new arms; for the four shared arms
(`succession`, `repair`, `unmaintained`, `no_repair`) it is absent, so those arms are byte-identical
to ac89's. The gate writes no content (`traces[0]`/`traces[1]` are never written by it); it only
changes the birth outcome, so a restoration supplies no controller content by construction.

The three new arms are `no_W` (block forever), `W_restore` (block `[0, RESTORE_TICK=50]`, then
un-block — W drops to 1 and recovers endogenously), and `W_restore_late` (block `[0, 100]`, i.e.
un-block AFTER W has autocatalytically died out at t=63 — irreversible). `RESTORE_TICK=50` is chosen
so the block ends before the initial W endowment `[32, 48, 64, 0]` is fully expired at t=64, leaving
one live W parent to restart production.

## Equivalence of the runner (declared, verified in engineering before finals)

`ac91.run(seed, history, arm, damage, corrupt, transition, move_tick=8192)` on AC89's final seed
family `4052, 4054, 4096, 4110` must reproduce AC89's frozen rows' `state_hash` for the four shared
arms, at both `transition='perm'` (simultaneous corrupt+move) and `'none'`, for every damage/corrupt
combination. This is the proof that the runner is a correct extension and the W-birth gate is a
no-op for the shared arms. The new fields (`first_W_empty`, `W_min_seen`, `W_at_corruption`,
`W_births_bank0`, `region0_births`, `region1_births`, `C_births`, `B_births`,
`description_correct_at_death`) are additive observations; they do not change the world state, so
`state_hash` is unchanged. Row equality is therefore asserted on `state_hash`, not on the full
row (the new fields are additions).

## Arms, world, seeds

Seven arms: `succession`, `repair`, `no_W`, `W_restore`, `W_restore_late`, `unmaintained`,
`no_repair`. The condition grid is arm × damage × corrupt = 7 × 2 × 2 = 28 conditions per
individual, at `transition='none'` (the production question is about the machinery, not the AC75
route-move adaptation, which is already tested in AC87/89). World constants unchanged from AC89:
PORTS=4, YIELD=64, TICKS=16384, CORRUPT_TICK=8192 (8 bits of rule 0 flipped), sticky 1e-4 damage on
both banks from independent streams, DESC_TRIGGER=2, POINTER_TRIGGER=2, CTRL_TRIGGER=2, SLOTS=4,
SUCC_MIN_SPACING=2400, SUCC_BUDGET=6, REGISTER_THRESHOLD=4, the corrected MODE/last atomic
controller write, the order-preserving generic-over-syntax decoder, AC75's erase-on-relinquish.
Final seeds `4200, 4201, 4202, 4203` (4 seeds × 2 histories = 8 individuals per condition, 224
rows). Engineering seeds 0-7 (disjoint from every prior final family ≤ 4110).

## Gates (prespecified; G1-G3 are the three causal links)

All gates are categorical (per individual, dead or alive unless a paid-maintenance endpoint requires
survivors — AC79's rule), no mean margins.

- **G1 (link 1 — blocking production reduces the machinery, then reconstruction capacity).** Every
  `no_W` individual: `first_W_empty ≤ 64` (W depletes within the initial endowment's lifetime),
  `W == 0` at end, `W_births_bank0 == 0` (production fully blocked), `reg_writes < 100` (the
  W-catalyzed maintenance — reconstruction included — ceases; the surviving arms' `reg_writes` is
  ~2280, so the bound is not knife-edge), and `not completed` (dies).
- **G2 (link 2 — restoring production rescues reconstruction without content).** Every `W_restore`
  individual: `completed`, `flipped_still_wrong == 0` (reconstruction works), `description_correct
  == 130` (controller content intact), `W_births_bank0 > 0` (production resumed), `W >= 2`
  (machinery recovered). The restoration supplies no content by construction (the gate only
  un-blocks the W-birth reaction); `description_correct == 130` is the observed content-intactness.
- **G3 (link 2, autocatalytic boundary — a late restore is irreversible).** Every `W_restore_late`
  individual: `not completed`, `W == 0`, `W_births_bank0 == 0` — restoring W-birth after W has
  autocatalytically died out (t=63) cannot restart W, so `W_restore_late` is identical to `no_W`.
  This pins the mechanism: replacement must occur before the last W dies.
- **G4 (link 3 — ordinary operation replaces the machinery while content persists).** Every
  `succession` and `repair` individual: `W_births_bank0 >= 4` (the 4-slot W complement replaced at
  least once — the unconditional turnover floor, AC84's lesson), `description_correct == 130` and
  `flipped_still_wrong == 0` (controller information and reconstruction hold).
- **G5 (retained repair-only arm — replacement is a capability, not a necessity).** Every `repair`
  individual: `completed`, `successions == 0`, `description_correct == 130`,
  `flipped_still_wrong == 0`.
- **G6 (controls — reconstruction and repair are load-bearing).** Every `unmaintained` and
  `no_repair` individual: `not completed`.
- **G7 (completeness + determinism).** The row count equals seeds × 2 × conditions, and a sampled
  exact rerun is byte-identical.

## Reported, not gated

- The death mechanism in `no_W`/`W_restore_late` (the AC13 attention-hijack: obs bit 6 stays set, the
  blocked W-birth rule preempts C-birth, C dies, energy drains) is reported as a named finding, not
  a gate.
- `description_correct` at end-of-run in the dying arms is post-mortem degradation (the damage
  stream keeps writing after death while paid repair has stopped — AC79); the live measure is
  `description_correct_at_death`, reported for the dying arms and expected to be 130/130.
- Survival is a bimodality-aware lower bound (AC68 W/C collapse is seed-family dependent); the G2
  arm's survival is asserted on the engineering and final families, not as a per-seed-family
  guarantee.

## Anti-drift rules

- The runner creates `ac91_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the hashed set.
- `test_ac91.py`, `audit_ac91.py`, `replay_ac91.py` are NOT hashed into the frozen snapshot (AC17's
  rule). If a gate fails, it fails. This protocol may not be edited after the first final seed.
- Engineering seeds (0-7) are excluded from the final sample and are disjoint from the final family.

## Source hashes (computed before the first final seed)

    (recorded in ac91_results_v1/pre_run_snapshot.json at freeze time)
