# AC94 results v1: coherent, resumable succession under produced-machinery limits

2026-09-18. Final seeds `4404, 4405, 4406, 4407` (4 seeds × 2 histories = 8 individuals per condition,
120 rows, 15 conditions/individual), hashed protocol `AC94_PROTOCOL_v1.md` (sha256
`2d0c42db85fef3e9daf4b0ccfac4f2a51d2af50948b679f65ebb6ef0ab4f970a`), 16,384 ticks, `transition='none'`,
no forced succession (the rate limiter is the sole event in the interruption arms). **All four
prespecified requirement-gates pass, plus the completeness/determinism gate.** Audit passed (120 rows,
14 source hashes no drift, arm invariants, generic-decode link, gates recomputed without simulating);
replay 6/6 exact; 18 AC94 tests; 241-test AC-line suite green (56 core AC1-9 + the AC67-94 line).

## The question

AC93 revoked the coordinator transition write's W-independence (`write_ctrl` MODE becomes W-gated) but
left two residuals its near-equivalence framing masked. (D1/D2) At W=2 the SWITCH branch wrote the
pointer and the SWITCH→REMOVE MODE transition as two separately-gated writes, so the pointer advanced
while the 21-replica MODE transition was refused, the next tick re-derived source/target from the
advanced pointer and reverted to COPY, and the old source's REMOVE was permanently skipped — a
pointer/phase/remove inconsistency, not "a 1-2 tick delay only". (D3) The rate limiter's start
timestamp was funded by energy + material alone, whose 35-69-replica value delta is structurally
unbounded by the W cap, so a W-gated timestamp would be permanently truncated and the rate limiter would
run away (E1). AC94 asks whether a succession can be **coherent** (source preserved, verified activation,
correct removal) and **resumable** (the rate limit survives interruption-and-rescue) when every paid
coordinator write is enacted by the produced finite-lived machinery. The frozen AC88/AC92/AC93 rows are
never edited; they are the comparators.

## The four requirement-gates (all pass, categorical per individual)

**G1 — correct source preservation.** Every `gated` (damage=T, corrupt=T) individual runs 6 successions
and leaves the source slot intact at every switch (`source_intact_at_switch_all` = True in 8/8, 16/16
including engineering): the copy builds the successor from the untouched source. Pinned at the
single-step level (`write_toward_slot` targets `target`/`old_source`, never the source).

**G2 — verified successor activation.** Every `gated` individual: every completed succession was verified
(`verified_all` = True — the successor decodes valid AND matches the source) and the switch was atomic
(`split_events == 0` in 8/8 — no tick where the pointer advanced while the MODE transition was refused).
The D2 `commit_switch` refuses both writes together, so a refused transition retries the same pair next
tick instead of splitting.

**G3 — correct old-source removal.** Every `gated` individual: every completed succession cleared its old
source (`removal_all` = True) and no stale slot remains (`occupied_slots_end == 2` in 8/8 — the active
slot plus one successor, never the 3-slot stale duplicate the split produces).

**G4 — rate limiting across interruptions.** `timer_block` (damage=T, corrupt=F): the W-funded counter
freezes at W=0 (`timer_at_W_empty == 5 < 13`, `timer_increments_after_W_empty == 0` in 8/8), the
succession never arms (`successions == 0`), and the organism dies (1242-1277, W=0, C=0) — no runaway.
`timer_rescue` (damage=T, corrupt=F): the counter froze before the rescue (W=0 at 1008-1063, timer 5)
then resumed after the machinery-only re-seed, completing 6 successions (a healthy rate-limited count,
not the E1 86-137 runaway) and surviving (W=3, C=2) in 8/8.

**G5 — completeness + determinism.** 120 rows == seeds × 2 × 15; the first row's exact rerun is
byte-identical (`state_hash`).

## The rival controls (what each removes, and the honest contrast)

- **`split`** (the AC93 gated rival: W-gated MODE + W-funded timer, but the two-step switch). It is the
  direct rival for the atomicity fix (G2/G3). **On the finals 4404-4407 the defect was not exercised:**
  `split_events == 0` in all 16 damage-on individuals and `occupied_slots_end == 2` everywhere — W never
  dipped to 2 during a SWITCH on this family, so the two-step switch completed cleanly at W=3 and the
  rival is behaviorally indistinguishable from `gated`. The defect itself is real and pinned elsewhere:
  engineering seeds 0/1/7 (and seed 7 with corrupt=F) exhibit `split_events == 1`, and seed 7 ends with
  `occupied_slots_end == 3` — the stale duplicate the skipped removal leaves — and `test_ac94.TestSplitRival`
  pins the W=2 pointer-advances-alone event at the single-step level. This is AC39's lesson in the
  unfavourable direction: a seed-dependent defect (W=2-during-SWITCH) is not guaranteed to fire on any
  given final family, so the rival's *organism-level* divergence is reported, not gated, and the contrast
  is carried by the unit test + engineering.
- **`ungated`** (the frozen comparator: write_ctrl NOT W-gated, timestamp rate limiter). Runner
  correctness: byte-identical to frozen AC92 `intact` — **32/32 state_hash** (pre-final equivalence
  check). Its succession count is 6 on the finals (6-7 on engineering — the frozen 6-7 range).
- **`ungated_block`** (the AC93 ungated-under-cut rival: `ungated` + the same W cut). Its rate limiter is
  the W-independent timestamp (NOT frozen by W=0), but the succession still stalls at the W-gated copy:
  `successions == 0`, dies 1240-1276, W=0, C=0 — the same organism-level outcome as `timer_block`, for a
  different reason. This pins that the fixed architecture's rate limiter is the machinery-dependent
  counter, while the rival's is a host-clock service; the contrast is a single-step property, reported
  not gated.

## The gated architecture (the measured rows, damage on)

| arm | succ | split_events | source intact | verified | removal | occ | completed | W / C |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `gated` | 6 (8/8) | **0** | **8/8** | **8/8** | **8/8** | 2 | 8/8 | 3 / 2 |
| `split` | 6 (8/8) | 0 | 8/8 | 8/8 | 8/8 | 2 | 8/8 | 3 / 2 |
| `ungated` | 6 (8/8) | — | — | — | 8/8 | 2 | 8/8 | 3 / 2 |
| `timer_block` | 0 | 0 | — | — | — | 3-4 | 0/8 | 0 / 0 |
| `timer_rescue` | 6 (8/8) | 0 | 8/8 | 8/8 | 8/8 | 2 | 8/8 | 3 / 2 |
| `ungated_block` | 0 | 0 | — | — | — | 3-4 | 0/8 | 0 / 0 |

`description_correct == 130` and `flipped_still_wrong == 0` in every surviving `gated` individual (the
reconstruction and description maintenance are unchanged from AC92/AC93). The coherence fields
(`source_intact_at_switch_all`, `verified_all`) are recorded only on the `gated`/`split` arms (which pass
through the instrumented switch branch); the frozen `ungated` comparator's two-step switch does not
record them, so its rows read `—` there by construction.

## What this establishes, and its limits

Supported:

- **The succession is coherent.** The source is preserved through the copy (G1), the pointer switches
  only after a verified successor is built and does so atomically with the MODE commit (G2), and the old
  source is actually cleared (G3) — the three coherence properties D1 showed the AC93 architecture could
  violate, now pinned per individual on the fixed architecture.
- **The rate limiter is a resumable, machinery-dependent service.** Cutting W freezes the counter and
  stops the succession (no runaway); restoring W resumes it at the healthy rate (G4). There is no
  W-independent write service left on the coordinator path — the E1 "permanently truncated timestamp"
  mode is structurally gone.
- **The fixes are the only changes.** The `ungated` comparator reproduces frozen AC92 byte-for-byte
  (32/32), and the `split` rival differs from `gated` only in the switch mechanism (pinned by
  `test_ac94`), so any gated/split divergence is attributable to the atomicity fix alone.

Not established, and not claimed:

- **The split defect was not exercised on the finals.** The rival's organism-level divergence (a stale
  slot, `split_events > 0`) fired on engineering seeds 0/1/7 but not on 4404-4407, because W=2-during-
  SWITCH is seed-dependent. The atomicity fix's necessity is carried by the single-step unit test and the
  engineering run, not re-demonstrated at the organism level on the finals. Reported plainly, not gated.
- **Full autopoiesis is still not claimed.** `advance()` and `prog.choose` remain supplied format-level
  machinery — what is shown W-gated and coherent is the write that enacts the supplied machine's
  transitions and its rate limiter. The `timer_rescue` re-seed is EXTERNAL (AC91 established endogenous
  W production separately).
- **Survival is a bimodality-aware lower bound** (AC68 W/C collapse is seed-family dependent): the 8/8
  `gated`/`split`/`ungated`/`timer_rescue` survival is the observed count on this family, not a
  per-seed-family guarantee.
- **The final priorities** `[0,2,3,1]`, `[2,1,0,3]`, `[1,0,2,3]`, `[0,2,3,1]` do not include AC83's
  adversarial `[3,0,2,1]` (bank-1 renewal last); the mechanism is priority-independent (the succession
  copies rule words verbatim and the corruption challenges rule 0, a fixed word), recorded as a scope
  note.

## Verification

- `audit_ac94.py` re-derives coverage (120 rows), arm invariants (`split_events == 0` in every gated
  individual, the timer machinery-dependence, the ungated_block copy-stall), the generic-decode link,
  source hashes (14 files, no drift) and all four gates — without simulating. The split rival's
  `split_events` is reported (0 on finals), not failed on.
- `replay_ac94.py`: 6/6 sampled conditions reproduce exactly (`state_hash` and endpoint fields).
- `test_ac94.py` (18 tests): the D2 atomic-switch primitives, the split rival's single-step
  pointer-advances-alone event, switch_tick-on-commit, the timer primitives (atomic increment, resumable
  W-gated reset), the arm config (6 arms, the split/ungated/ungated_block rival configs), final-seed
  disjointness, and the ungated ≡ frozen AC92 equivalence (32/32).
- 241-test AC-line suite green (56 core AC1-9 + the AC67-94 line). The AC94 change touches only new
  files (`ac94.py`, `test_ac94.py`, `audit_ac94.py`, `replay_ac94.py`); no frozen runner or test was
  edited, so the order-line (AC15-60) tests are unaffected by construction.
- Equivalence (pre-final): `ac94.ungated` reproduces frozen AC92 `intact` byte-for-byte, 32/32 state_hash.

## Files

`ac94.py` (runner, sha256 `1909c1794f2dc90bff7bc2e9eee060d67f2bfee2edc275f90dde3dc85525608d`),
`AC94_PROTOCOL_v1.md` (hashed protocol), `test_ac94.py`, `audit_ac94.py` (split audit), `replay_ac94.py`
(sampled exact reruns), `ac94_results_v1/` (frozen rows, pre-run snapshot, results), `ac94_d4_engineering_v1/`
(D4 engineering, seeds 0-7), `AC94_D1_DIAGNOSTIC.md` (D1 diagnosis), `AC94_D2_RESULTS.md` (D2 fix),
`AC94_D3_RESULTS.md` (D3 timer), `ac94_d3_engineering_v1/` (D3 engineering), `ac94_engineering_v1/` (D2
engineering).
