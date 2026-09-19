# AC95 results v1: state sufficiency — the trajectory is carried by maintained state alone

2026-09-18. Final seeds `4408, 4409, 4410, 4411` (4 seeds × 2 histories = 8 individuals per condition,
136 rows, 17 conditions/individual, 8 arms), hashed protocol `AC95_PROTOCOL_v1.md` (sha256
`2e6dbc6d85e71b58160b7e10ee2e7917087cc265c69935052cef545ada0fd1ed`), runner `ac95.py` (sha256
`feef9022a67c6c0c54c0e4707e15bd3fd623d324cf4cb6114220a95b0fa95f80`), 16,384 ticks,
`transition='none'`, no forced succession. **All four prespecified gates pass.** Audit passed (136 rows,
14 source hashes no drift, arm invariants, generic-decode link, observer-discard record, gates
recomputed without simulating); replay 8/8 exact + 2/2 observer-discard byte-identical; 17 AC95 tests;
56-test core AC1-9 suite green.

## The question

AC95 asks whether the machinery that enacts the AC94 coherent resumable succession depends on
host-side operational memory. AC95-D1 found two class-C leaks; D2 closed the timer's
`timer_reset_done` host flag by moving it into maintained state as a reset-in-progress (RIP) bit
(CTRL bit 17), and D3 built the mid-reset interruption (a direct W cut, the mirror of AC92's direct W
restoration) plus a machinery-only rescue. The decisive test is **observer-discard equivalence**:
preserve the organism's maintained state, discard the host's observational history, resume, and the
organism continues correctly — observer-discard **endpoint** equivalence (identical final
`state_hash`; per-tick trajectory not compared). This run freezes that claim.

## The four gates (all pass, categorical per individual)

**G1 — state sufficiency (observer-discard equivalence).** For every individual, the `gated`
run with the observer discarded during an active succession (`swap_succ_at='mid_succession'`, mid-COPY)
ends at an identical final `state_hash` to the undisturbed run, and the `reset_rescue` run with the
observer discarded at the rescue tick (mid-reset, mid-succession) does likewise — endpoint equivalence,
per-tick trajectory not compared. **16/16 byte-identical** (8 individuals × 2 discard points). The swap demonstrably
fired (the fresh observer re-stamps the in-flight succession's start at `succ_start + 10`, a later
tick than the true start) — it is not a silent no-op.

**G2 — reset interruption + resume.** Every `reset_block` individual froze the reset part-way
(`reset_progress_at_cut` = 10–11 of 13), never completed it without W (`reset_completed_tick is None`
— no host memory completes it), completed no succession, and died at 2803–2815 with the description
intact (130/130 at death): the machinery is cut, not the content. Every `reset_rescue` individual
froze, then completed the reset after the machinery-only rescue (`reset_completed_tick` ≈
`reset_start` + 43, i.e. ~3 ticks after the restore at +40), survived, and completed **6 successions**
— the healthy rate-limited count, identical to the uninterrupted `gated` run.

**G3 — coherence carry-forward.** Every `gated` (damage=T, corrupt=T) individual: 6 successions,
`source_intact_at_switch_all`, `verified_all`, `split_events == 0`, `removal_all`,
`occupied_slots_end == 2`, `description_correct == 130`, `flipped_still_wrong == 0`. Every
`timer_block` individual froze the counter at W=0 (`timer_at_W_empty < 13`, zero increments after
W=0, `successions == 0`, died 1243–1278) — no runaway. Every `timer_rescue` individual resumed to a
healthy count (6 successions, survived, W=3, C=2). The RIP-bit fix is behaviour-preserving.

**G4 — completeness + determinism.** 136 rows == seeds × 2 × 17; the first row's exact rerun is
byte-identical (`state_hash`).

## The rival controls (what each removes, and the honest contrast)

- **`split`** (the AC93 gated rival: two-step switch + host reset flag). Direct rival for the
  atomicity fix (G3). **Unlike AC94, the defect fired on these finals:** `split_events` totals 6
  across the 8 damage-on individuals — seeds 4408/4409/4411 fire once (seed 4411 twice on c=T) and
  seed 4411 ends both histories with `occupied_slots_end == 3`, the stale-duplicate signature of the
  skipped removal; seed 4410 does not fire (W never dips to 2 during a SWITCH). The atomicity fix's
  necessity is therefore demonstrated at the organism level on this family, not only at the
  single-step level — the opposite of AC94's outcome (AC39's seed-dependence, in the favourable
  direction this time). The single-step form remains pinned by `test_ac95.py`.
- **`ungated`** (the frozen comparator: write_ctrl NOT W-gated, timestamp rate limiter). Runner
  correctness: byte-identical to frozen AC92 `intact` — **32/32 state_hash** (pre-final equivalence
  check); 6–7 successions on the finals.
- **`ungated_block`** (the AC93 ungated-under-cut rival). Its rate limiter is the W-independent
  timestamp (NOT frozen by W=0), but the succession still stalls at the W-gated copy: `successions
  == 0`, dies 1240–1276, W=0, C=0 — the same organism-level outcome as `timer_block`, for a
  different reason (a single-step property, reported not gated).

## The measured rows (damage on)

| arm | succ | split_events | source intact | verified | removal | occ | completed | W / C |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `gated` | 6 (8/8) | **0** | **8/8** | **8/8** | **8/8** | 2 | 8/8 | 3 / 2 |
| `split` | 6 (8/8) | 0–2 (6 total) | 8/8 | 8/8 | 7/8 (4411 stale) | 2–3 | 8/8 | 3 / 2 |
| `ungated` | 6–7 (8/8) | — | — | — | 8/8 | 2 | 8/8 | 3 / 2 |
| `timer_block` | 0 | 0 | — | — | — | 3–4 | 0/8 | 0 / 0 |
| `timer_rescue` | 6 (8/8) | 0 | 8/8 | 8/8 | 8/8 | 2 | 8/8 | 3 / 2 |
| `ungated_block` | 0 | 0 | — | — | — | 3–4 | 0/8 | 0 / 0 |
| `reset_block` | 0 | 0 | — | — | — | 4 | 0/8 | 0 / 0 |
| `reset_rescue` | 6 (8/8) | 0 | 8/8 | 8/8 | 8/8 | 2 | 8/8 | 3 / 2 |

`description_correct == 130` and `flipped_still_wrong == 0` in every surviving arm; the description
is intact at death in every blocked/stalled arm (130/130) — the cut removes the machinery, not the
content (AC91's distinction). The coherence fields (`source_intact_at_switch_all`, `verified_all`)
are recorded only on the `gated`/`split` arms (the instrumented switch branch); the frozen `ungated`
comparator's two-step switch does not record them, so its rows read `—` by construction.

## What this establishes, and its limits

Supported:

- **The trajectory is carried by maintained state alone.** Preserving the organism's vulnerable,
  maintained state while discarding the host's observational history (a fresh observer) leaves the
  trajectory byte-identical at the two hardest points — during an active succession and mid-reset —
  for every individual. The class-C timer leak (D1) is closed: the reset-progress flag is a
  maintained, damaged, paid-repaired bit, and no branch reads a log field back.
- **A mid-reset machinery cut freezes the reset with no host-assisted completion, and a
  machinery-only rescue resumes it from maintained state alone.** The reset is W-gated and resumable;
  a frozen reset stays frozen (the sticky damage stream can re-set the cleared counter bits, which is
  damage, not progress), and the rescue — labeled EXTERNAL — restores only the W population
  (`life[:4]`), never content.

Not established, and not claimed:

- **`alloc.streak` (the second D1 class-C leak) remains open.** It is inert in these finals
  (`transition='none'` leaves no stale route; measured `relinquishments == 0`), and its fix would
  change the byte-identity comparator digests. The state-sufficiency claim does not cover it until
  it is closed — flagged, not silent (a follow-up, not part of AC95-D4).
- **Full autopoiesis is still not claimed.** `advance()` and `prog.choose` remain supplied
  format-level machinery; what is shown is that the *operational memory* of the succession (its
  reset-progress flag, its rate-limit counter, its coordinator MODE) is carried in the organism's own
  vulnerable, paid-maintained state. The `restore_W` re-seed in the reset/timer rescue arms is
  EXTERNAL (AC91 established endogenous W production separately).
- **Survival is a bimodality-aware lower bound** (AC68 W/C collapse is seed-family dependent): the
  8/8 `gated`/`split`/`ungated`/`timer_rescue`/`reset_rescue` survival is the observed count on this
  family, not a per-seed-family guarantee. `reset_block`/`timer_block`/`ungated_block` are expected
  to die (a frozen reset/timer cannot complete without W).
- **The final priorities** `[0,3,2,1]`, `[1,2,3,0]`, `[1,2,0,3]`, `[2,0,1,3]`: seed 4408's
  `[0,3,2,1]` ranks bank-1 renewal last (the AC83 adversarial pattern in spirit), but the succession
  copies rule words verbatim and the corruption challenges rule 0 (a fixed word), so the mechanism is
  priority-independent — recorded as a scope note, not a gate.

## Verification

- `audit_ac95.py` re-derives coverage (136 rows), arm invariants (the reset-interruption endpoints,
  the coherence carry-forward endpoints, the timer machinery-dependence, the ungated_block
  copy-stall), the generic-decode link (order-preserving, generic over syntax), source hashes (14
  files, no drift), the observer-discard record (16/16) and all four gates — without simulating.
- `replay_ac95.py`: 8/8 sampled conditions reproduce exactly (`state_hash` + endpoint fields),
  and 2/2 observer-discard reruns are byte-identical.
- `test_ac95.py` (17 tests): the reviewer's single-step harness (observer cleared vs kept vs stale
  flag → identical writes), the RIP bit (maintained, damaged+repaired, W-gated paid write), the
  observer-discard equivalence (idle ticks and mid-succession, with the swap-fires check), the reset
  interruption (cut_W machinery-only, reset frozen at W=0, block freezes / rescue resumes, rescue-tick
  discard identical), the comparator byte-identity (`ungated` ≡ frozen AC92 32/32, `split` ≡ frozen
  AC94 32/32), and final-seed disjointness. The change touches only new files (`ac95.py`,
  `test_ac95.py`, `audit_ac95.py`, `replay_ac95.py`); no frozen runner or test was edited.
- 56-test core AC1-9 suite green (the AC95 change does not touch any frozen AC1-9 file).
- Equivalence (pre-final): `ac95.ungated` reproduces frozen AC92 `intact` byte-for-byte, 32/32;
  `ac95.split` reproduces frozen AC94-D4 `split` byte-for-byte, 32/32 — proving the runner is a
  correct extension and the RIP-bit fix is applied only to the fixed architecture.

## Files

`ac95.py` (runner, sha256 `feef9022a67c6c0c54c0e4707e15bd3fd623d324cf4cb6114220a95b0fa95f80`),
`AC95_PROTOCOL_v1.md` (hashed protocol), `test_ac95.py` (17 tests), `audit_ac95.py` (split audit),
`replay_ac95.py` (sampled exact reruns), `ac95_results_v1/` (frozen rows, pre-run snapshot, results),
`AC95_D1_AUDIT.md`, `AC95_D2_RESULTS.md`, `AC95_D3_RESULTS.md` (the D1-D3 engineering record),
`ac95_d4_smoke_v1/` (smoke, seeds 0-1).
