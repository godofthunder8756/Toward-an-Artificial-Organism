# AC91 results v1: production-dependencies test — W production is load-bearing for reconstruction and coordination

2026-09-18. Final seeds `4200, 4201, 4202, 4203` (4 seeds × 2 histories = 8 individuals per
condition, 224 rows), hashed protocol `AC91_PROTOCOL_v1.md`, 16,384 ticks, `transition='none'`
(no route move), corruption at t=8192. **All seven prespecified gates pass.** Audit passed (224
rows, 14 source hashes no drift, W-birth-gate no-op + content-vs-machinery contrast, generic-decode
link, gates recomputed without simulating); replay 6/6 exact; 158 tests green (56 core AC1-9 + 87
AC79-89 line + 15 AC91).

## The question

The internal-state milestone (AC86-89) is accepted: internally stored controller information is
maintained, reconstructed, and transferred to successor storage through the tested challenge. Full
autopoiesis is not established by declaring the succession mechanism "substrate" (a modeling choice
the review left unresolved). The decisive next question is the production of the machinery: can the
organization replace the finite-lived components enabling reconstruction and coordination, while
their loss actually removes those functions and their endogenous replacement restores them?

The produced, finite-lived component that enacts BOTH functions is the **W repair catalyst** (4
slots, lifetime 64, born by action 6, autocatalytic — a birth needs a live W parent). Its specified
capability, the per-action write cap `min(32, 8·available_W, energy, material)`, gates every paid
write on the reconstruction and coordination paths: `reg_from_active` (reconstruction),
`reg_description_active`, `reg_pointer`, `reg_ctrl`, the succession slot copy/remove
(`write_toward_slot`) and the pointer switch (`write_pointer`). The succession state machine's
transition *logic* (`advance()`) is the supplied format-level machinery of the accepted boundary;
what is produced and replaced is the W catalyst that executes its writes.

## The measured arms (damage on, corruption on, no route move)

| arm | survive | first death | W end | W_min | W_births (bank 0) | reg_writes | fw | desc at end | desc at death | successions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `succession` | **8/8** | — | 3 | 2 | 766 | 2276–2387 | 0 | 130 | — | 6–7 |
| `repair` | **8/8** | — | 3 | 2 | 766 | 2372–2474 | 0 | 130 | — | 0 |
| `no_W` | **0/8** | 248–254 | 0 | 0 | **0** | **7–10** | 8 | 50–78 | **130** | 0 |
| `W_restore` | **8/8** | — | 3 | 1 | 766 | 2280–2389 | 0 | 130 | — | 6–7 |
| `W_restore_late` | **0/8** | 248–254 | 0 | 0 | **0** | 7–10 | 8 | 50–78 | **130** | 0 |
| `unmaintained` | **0/8** | 1123–2420 | 0–4 | 0–2 | 37–116 | 70–188 | 8 | 50–78 | 125–129 | 0 |
| `no_repair` | **0/8** | 430–915 | 0 | 0 | 18–66 | **0** | 8 | 50–78 | 130 | 0 |

`desc at end` in the dying arms is post-mortem degradation (the damage stream keeps writing after
death while paid repair has stopped — AC79); the live measure is `desc at death`.

## The three causal links (the gates, all categorical per individual)

**G1 — blocking production reduces the machinery, then reconstruction capacity.** `no_W` blocks the
W-birth reaction (bank 0 only; memory-region catalysts are untouched). W depletes to 0 at
`first_W_empty == 63` (the initial endowment `[32,48,64,0]` fully expires), and from then on the
write cap is `8·0 = 0`, so the W-catalyzed maintenance — reconstruction included — ceases:
`reg_writes` totals 7–10 (all pre-depletion) against 2276–2474 in every surviving arm. All 8 die at
248–254. Crucially, **the content is intact at death** (`desc at death == 130/130`): the loss removes
the *machinery* and therefore the *functions*, not the controller information.

**G2 — restoring production rescues reconstruction without supplying content.** `W_restore` blocks
W-birth for `[0, RESTORE_TICK=50]`, then un-blocks it. W drops to 1 (the life-64 catalyst survives)
and recovers endogenously to 3; all 8 survive, reconstruct (`fw == 0`), keep the description at
130/130, and resume production (`W_births_bank0 == 766`). The restoration is the organism's own
W-birth reaction turned back on — the gate writes no content (`traces[0]`/`traces[1]` are never
touched by it), so no controller content is supplied or altered by construction (unit-tested).

**G3 — the restoration is bounded by autocatalytic death.** `W_restore_late` un-blocks at t=100,
after W has died out at t=63. Because W-birth needs a live W parent, the late restore cannot restart
W: all 8 die at 248–254 with `W == 0` and `W_births_bank0 == 0`, byte-identical to `no_W`
(same `state_hash`). The produced machinery must be replaced before the last W dies — a genuine
property of the autocatalytic production loop, not an experimental artifact.

**G4 — ordinary operation replaces the machinery while content persists.** Every `succession` and
`repair` individual has `W_births_bank0 == 766` (uniform — the W population is at a deterministic
steady state, ~192× the 4-slot complement, i.e. each W catalyst replaced ~255 times over 16,384
ticks = its 64-tick lifetime) while `description_correct == 130` and `fw == 0` hold.

**G5 — repair-only is retained.** `repair` (succession off) survives 8/8 with the description at
130/130 and reconstruction working (`fw == 0`), zero successions. Replacement is a demonstrated
capability, not a necessary maintenance process — the two senses are kept distinct, as the card
requires.

**G6 — controls.** `unmaintained` dies 8/8 (1123–2420) via description degradation (no repair →
the description drifts to a still-valid-but-wrong permutation, and reconstruction rebuilds a wrong
program), and `no_repair` dies 8/8 (430–915) with `reg_writes == 0` (the repair loop cut entirely,
the description stays 130/130 at death). Reconstruction and repair are load-bearing.

## The death mechanism in `no_W` (reported, not gated)

The block does not starve the organism of fuel: at death `fuel` is still 63–64 (full) and `material`
116–121, while `C == 0` and `energy == 0`. The cascade is the AC13 attention-hijack operating on the
blocked W-birth rule: with W=0 the observation bit 6 ("low W") is permanently set, so the program's
W-birth rule (mask 64) fires every tick ahead of the C-birth rule (mask 128); the blocked W-birth
wastes the action, C is never born, the converters expire, conversion stops, and energy drains. This
is the same mechanism AC10's `no_W` ablation measured in the 2048-tick world; here it is re-located
as the causal path by which W loss removes reconstruction and coordination (the organism dies with
its controller information intact but its machinery gone).

## Equivalence of the runner

`ac91.run(..., move_tick=8192)` reproduces AC89's frozen `state_hash` for the four shared arms
(`succession`, `repair`, `unmaintained`, `no_repair`) on AC89's final seed family `4052, 4054,
4096, 4110` at both `transition='perm'` (simultaneous corrupt+move) and `'none'` — **256/256 rows
byte-identical**. The W-birth gate is a no-op for the shared arms by construction (injected only
when `cfg['block_W']` is set), so the runner is a correct extension of ac89 and the only differences
are the three new arms and their additive observation fields.

## What this establishes, and its limits

Supported, model-relative: in this integrated body the W catalyst is a produced, finite-lived,
autocatalytically self-replacing component, and its production is causally required for both
reconstruction and coordination — blocking it removes the functions (while leaving the controller
information intact) and restoring its production rescues them, with no controller content supplied
by the restoration. This closes the "production of the machinery" link that the closure boundary
left open, for the reconstruction/coordination functions specifically.

Not established, and not claimed:

- **Full autopoiesis is still not claimed.** The succession state machine's transition logic
  (`advance()`) and the interpreter (`prog.choose`) remain supplied format-level machinery. What is
  now shown produced-and-replaced is the W catalyst that executes the supplied machine's writes.
  Whether the fixed `advance()` code is legitimate "reactions enacted by produced components" or an
  "always-available coordinator needing only payable resources" is a modeling judgment, not a
  measurement this study settles.
- **C and B production are not the tested target.** They remain produced (established in AC2/AC3/AC4
  and AC10), and this study records their turnover as context, but the causal links are about W
  (the machinery enabling reconstruction and coordination). A W loss also kills C via the
  attention-hijack, so the W→death path is not a clean single-variable cut — the honest claim is
  "blocking W production removes the W-catalyzed functions," with the hijack cascade reported as the
  death mechanism.
- **No content self-production** (AC78 still blocked): the description is inherited at development,
  not produced by the organism's own lifetime. The "endogenous replacement" shown here is turnover
  of the W machinery, not discovery or production of better controller content.
- **Survival is a bimodality-aware lower bound** (AC68 W/C collapse is seed-family dependent). 8/8
  finals and 16/16 engineering survive on the succession/repair/W_restore arms; this is the observed
  count, not a per-seed-family guarantee.
- **The final priorities** `[1,3,2,0]`, `[2,3,0,1]`, `[1,2,3,0]`, `[2,3,1,0]` do not include AC83's
  adversarial `[3,0,2,1]`; the production question is priority-independent (W-birth is a fixed word,
  not a bank rule), so this is recorded as a scope note, not a gap.

## Verification

- `audit_ac91.py` re-derives coverage (224 rows), arm invariants (`no_W`/`W_restore_late` have
  `W_births_bank0 == 0` and die; the shared arms turn W over), the W-birth-gate no-op + the
  content-vs-machinery contrast (`no_W` has `description_correct_at_death == 130`), the
  generic-decode link, source hashes (14 files, no drift) and all seven gates — without simulating.
- `replay_ac91.py`: 6/6 sampled conditions reproduce exactly, `state_hash` and endpoint fields.
- `test_ac91.py` (15 tests): the gate is absent for the shared arms and present for the new arms;
  it blocks exactly bank-0 births and writes no content; restore-tick semantics; W-birth is
  autocatalytic (no parent → no birth; depleted W → zero write capacity); final-seed disjointness;
  the gate shapes are categorical per individual; and the recorded freeze + the
  content-intact-at-death mechanism are pinned on the finals.
- Full suite: 158 tests green (56 core AC1-9 + 87 AC79-89 line + 15 AC91).
- Runtime: each 16,384-tick condition is ~3 s on this host; the full 224-row final grid ~11 min.

## Files

`ac91.py` (runner, sha256 `fcd8fa15d130682b75d17bdc93c610d802a741c9d0be0c4c4b5a82c8113550ff`),
`AC91_PROTOCOL_v1.md` (hashed protocol), `test_ac91.py`, `audit_ac91.py` (split audit),
`replay_ac91.py` (sampled exact reruns), `ac91_results_v1/` (frozen rows, pre-run snapshot,
results), `ac91_engineering_v1/` (engineering, seeds 0-7).
