# AC103 protocol v1: distinguish resource shortage from premature termination of repair (persistent triggering × immediate/staged reconstruction)

STATUS: **frozen before the first final seed.** Written 2026-09-20. Parent: AC102 (frozen).

AC102 established the corruption-move interaction and rejected the eight-write staging policy
(`REPAIR_BUDGET = 8`), but left the CAUSE of the staging failure open. The staged budget still
crossed the material threshold on the marginal seeds (material ≤ 72 at the corruption tick, so
any spend ≥ 8 drops material below 64 and fires obs bit 1), and staging introduced a SECOND
failure on the high-material seeds: the program's own majority repair (action 2) cements the 4/7
corruption flip and removes the reconstruction's trigger (obs bit 2's minority count drops to
zero once the flip is cemented), so the staged reconstruction stalls (fw stays nonzero) and the
organism dies. AC102's inference was bounded to that policy and did NOT establish whether the
failure is a **resource shortage** (the material spend crosses the threshold) or **premature
termination of repair** (the trigger disappears mid-reconstruction).

This protocol freezes the direct test. Prices and W requirements are UNCHANGED; no decision write
is made material-independent; no reserve is added; no accepted internal-memory milestone is
reopened. The ONLY new degree of freedom is the reconstruction's TRIGGER condition and its
per-tick SPEND, both properties of the reconstruction primitive.

SOURCES (declared): ac103.py ac102.py ac101.py ac100.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC103_PROTOCOL_v1.md

## What is NOT changed (the resource model is untouched)

The reconstruction (`reg_from_active`) keeps its total prices (1 energy + 1 material per replica),
its machinery requirement (the W-catalyzed `_cap = min(32, 8·available_W, energy, material)`), and
its world (corruption at t=8192, two route reversals at t=8192 and t=12288, the Gray streak, the
erase-on-relinquishment, the observer-discard, every world constant). The `current` arms are
byte-for-byte the AC102 arms. The ONLY changes are (a) the trigger condition and (b) the per-tick
spend.

## The two axes

### Axis 1 — CURRENT vs PERSISTENT repair triggering

- **Current** (frozen AC102): `reg_from_active` fires when `reg_trigger = obs2 or (repair and
  (desc_minority ≥ DESC_TRIGGER or pointer_minority ≥ POINTER_TRIGGER))`.
- **Persistent**: `reg_from_active` fires when `reg_trigger OR program_incomplete`, where
  `program_incomplete` is the **internally determined completion condition**: the DECODED program
  (majority read) still differs from the description-derived target (`build_program(read_slot(...))`),
  excluding the decision-state offsets (register + streak). The completion condition is read from
  the organism's own maintained program + description; it is NOT driven by the experiment's
  corruption flag (`corrupt`) and NOT by an observer's pristine template (the acquired bits).

  Because the completion condition is DERIVED from maintained state, there is **no added
  pending-repair state**: persistence is a pure function of the program + description, so the
  "added pending-repair state must be vulnerable, maintained, and paid" constraint is satisfied
  vacuously — the trigger and completion condition already live entirely in the maintained,
  paid-repaired substrate (the program bank and the description), and no host-side flag steers
  the persistence. The persistent trigger is INERT whenever the program already matches the
  target, so the persistent immediate arm is byte-identical to the current arm wherever the
  immediate reconstruction outruns the cementing.

### Axis 2 — IMMEDIATE vs STAGED reconstruction

Per-tick write budget on `reg_from_active`, exactly AC102's `regen_budget`: `None` (immediate,
up to `_cap` ≈ 24 at W=3) vs `REPAIR_BUDGET = 8` (staged, ≥ 4 ticks for the 32-site corruption).

### The state-dependent spending policy (decisive sequence step 2)

`persistent_defer` = persistent trigger + a material-aware budget: for `t ≥ CORRUPT_TICK`, the
reconstruction DEFERS (budget 0) while `material ≤ DEFER_THRESHOLD` (64, the obs-bit-1 boundary)
and reconstructs (budget None) otherwise; for `t < CORRUPT_TICK` it is byte-identical to the
immediate arm. The policy is "do not spend on the reconstruction while material is at/below the
obs-bit-1 threshold", so the reconstruction does not compete with the material contact and the
paid decision write (the Gray streak increment) during the scarcity window. Gated to the challenge
tick so the pre-challenge trajectory is a clean control (AC89's single-change rule).

## The cementing measurement (quantifying reversal)

`reg_from_active` (curative — rebuilds the program from the description) and action 2 (the
program's own majority restore — cementing for a 4/7 flip) are recorded separately per tick:
`action2_writes` (bank-0 majority-restore replica writes) and `action2_cementing` (those writes
that move a replica toward a WRONG majority, i.e. a program bit whose current majority differs
from the acquired value). This quantifies whether ordinary majority repair REVERSES reconstruction
progress.

## Arms (all on `corrupt=True` + the two-move SCHEDULE)

| arm                | trigger   | regen_budget | equals                 |
|--------------------|-----------|--------------|------------------------|
| `current`          | current   | None         | AC102 `both`           |
| `current_staged`   | current   | 8            | AC102 `staged`         |
| `persistent`       | persistent| None         | trigger-only change    |
| `persistent_staged`| persistent| 8            | trigger-only change    |
| `persistent_defer` | persistent| 'defer'      | trigger + defer spend  |

`REPAIR_BUDGET = 8`, `DEFER_THRESHOLD = 64`.

## Screening disclosed (engineering, before this protocol was frozen)

Engineering ran on seeds 0-7 (disjoint from the final sample), 16,384 ticks, both histories
identical on every seed:

- **The interaction is clean** (AC102): `current` (immediate) recovers fw→0 on every seed; the
  marginal seed 1 (material 65 at the corruption tick) dies at 8408 with fw=0 (reconstruction
  complete, streak stalls at 4).
- **Premature termination (cementing) is a RECOVERY failure.** `current_staged` fails to recover
  (fw>0) and dies on 5/8 seeds (2,3,4,5,7; fw 1-5); `persistent_staged` recovers fw→0 on 8/8 —
  persistence closes the recovery failure completely. The cementing write is quantified:
  `current_staged` writes 15-20 cementing replicas on those seeds vs 0-6 under `current`.
- **Resource shortage is a SURVIVAL failure, distinct from the recovery failure.** `persistent_staged`
  recovers fw→0 on 8/8 but survives only 4/8 (dies on 0,1,3,4 with fw=0 — the persistent
  reconstruction's spend still crosses the material threshold and stalls the streak). Persistence
  alone therefore does NOT achieve "recovery AND survival".
- **The state-dependent defer closes the survival failure.** `persistent_defer` recovers fw→0 AND
  survives 8/8 — by deferring the reconstruction while material ≤ 64 it frees material for the paid
  decision write, the streak reaches the drop threshold, the stale route is erased, and the
  organism re-acquires.

The gates below are shaped by this engineering screen on the disjoint seeds 0-7; the final seeds
are NOT screened (see Anti-drift).

## Gates (prespecified, categorical per distinct seed; both histories must satisfy each)

- **G1 (arm identity — the single-change licensing).** Every final individual: `current` is
  byte-identical (`state_hash`) to AC102 `both`, and `current_staged` is byte-identical to AC102
  `staged`. The persistent arms differ ONLY by the trigger (and, for `persistent_defer`, the
  challenge-gated defer spend) — established by construction (the maintain function is the only
  change) plus this byte-identity for the current arms.
- **G2 (persistent staging completes reconstruction — premature termination is a recovery failure,
  closed by persistence).** Every final individual: `persistent_staged` recovers
  (`flipped_still_wrong == 0`). Non-vacuous: at least one final individual's `current_staged` does
  NOT recover (`flipped_still_wrong > 0`).
- **G3 (the state-dependent defer preserves adaptation resources — resource shortage is a survival
  failure, closed by the defer).** Every final individual: `persistent_defer` recovers
  (`flipped_still_wrong == 0`) AND survives (`completed`).
- **G4 (the two failure modes are distinct).** Every final individual where `persistent_staged`
  dies with `flipped_still_wrong == 0` (recovery complete, survival failed): `persistent_defer`
  survives. Non-vacuous: at least one such individual (a seed where persistence closes recovery but
  not survival).
- **G5 (state sufficiency — observer-discard).** Per-tick observer-discard on `current` is
  byte-identical at every tick (non-vacuous: `swap_applied`, `streak_at_swap == 2`). Carried from
  AC102's G6; the persistent arms add no host-side state.
- **G6 (completeness + determinism).** Row count == 8 seeds × 2 histories × 5 arms (80); a sampled
  exact rerun of the first row is byte-identical (`state_hash`).

## Reported, not gated

- The budget trace (which writes consume material, when the streak stalls, when W/C fails), with
  `action2_writes` / `action2_cementing` per tick — the quantitative reversal measurement.
- `persistent` (immediate) recovers FAST (t≈8193) where `current` is cementing-delayed (t≈8235),
  but the OUTCOME (survival) is unchanged — persistence is inert on the immediate schedule's
  survival, and `persistent` is byte-identical to `current` on the marginal seed. Reported, not
  gated (the recovery tick is seed-dependent).
- The material level at the corruption tick and each seed's priority — covariates, reported not
  prespecified (untouched seeds).
- Survival is a bimodality-aware lower bound (AC68). No autopoiesis claim; `advance()` and
  `prog.choose` remain supplied format-level machinery.

## Anti-drift rules

- The runner creates `ac103_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed
  set (which includes this protocol file).
- `test_ac103.py`, `audit_ac103.py`, `replay_ac103.py` are NOT hashed into the frozen snapshot
  (AC17's rule).
- Engineering seeds (0-7) are excluded from the final sample. The final seeds 5600-5607 are a fresh
  range, disjoint from every prior family (0-7, 4412-4439, 4440-4443, 4444-4447, 4448-4451,
  4466/4481/4504/4510, 4600-4871, 4872-5099, 5100-5507) and are NOT screened — no final outcome is
  observed before the freeze; `mat_at_corrupt` and priority are measured, not selected on.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.
- The frozen AC102 results and every earlier freeze are untouched.

## Source hashes (computed before the first final seed)

    (recorded in ac103_results_v1/pre_run_snapshot.json at freeze time)
