# AC102 results v1: the timing hypothesis is falsified — the composition failure is caused by the reconstruction's PRICE on a marginal economy, not its timing; and the reconstruction must be immediate (staging breaks it)

Parent: AC101. Frozen per `AC102_PROTOCOL_v1.md` (hashed before the first final seed). Runner
`ac102.py` (a parametrized copy of `ac101.py`'s gray_ctl arm: corrupt × schedule × a per-tick
reconstruction write budget). Seeds **4880, 4934, 4950, 5002** (unseen, stratified) + **4883, 4901,
4928, 5038** (adversarial `[3,0,2,1]`) × 2 histories, 6 arms each, 96 rows, 16,384 ticks.

**Headline:** the timing hypothesis is **falsified**, and the deeper finding is that the
reconstruction's immediate schedule is **load-bearing**. Staging the reconstruction (bounding its
per-tick material spend, the candidate fix AC101 named) does NOT rescue the composition failure —
the death seeds die at the SAME tick (8408) under immediate and staged — and it actively breaks
recovery on 2 of 8 finals by letting the program's own majority repair cement the corruption. The
failure is the reconstruction's **price** (~24 material) on a **marginal economy** (material ≤ 72
at the corruption tick), not the **timing** of that spend.

## Verdict

**Seven of eight gates pass; G4 fails, recorded not moved.** The answer to the question — "does
the TIMING of necessary maintenance cause the composition failure?" — is **NO**, with an important
qualifier:

- **The interaction is clean (G1, 8/8).** Every final individual survives `neither`, `move_only`,
  and `corrupt_only`; the composition death (4934, 5002) is confined to `both`. The death requires
  BOTH the corruption AND the move — neither alone kills.
- **Reconstruction recovers under `both` (G2, 8/8).** Every individual applies the corruption
  (`fw_at_corrupt == 8`) and recovers it (`flipped_still_wrong == 0`), including the dying seeds.
  The internal-state composition is unconditional, exactly as AC101 recorded.
- **The timing hypothesis is FALSIFIED (G3, PASS-in-the-falsifying-direction).** The two
  death-prone seeds die at **8408 under BOTH `both` and `staged`** — identical death tick, identical
  streak stall (5). Staging the reconstruction's material spend does NOT rescue them. The lump-spend
  timing is NOT the cause of the failure.
- **The reconstruction must be immediate (G4, FAIL 2/8).** The `staged` schedule leaves the
  controller unrecovered (`flipped_still_wrong == 2`) on 4883 and 4928, which die at 8248/8263. The
  slow reconstruction is caught by the program's own majority repair (action 2), which CEMENTS the
  4/7 majority flip and suppresses the reconstruction's trigger. The immediate schedule outruns
  this; the staged schedule does not. This gate FAILS by design (prespecified), recording that
  "stage the reconstruction" is NOT a viable fix.
- **Never-repair must fail (G5, 8/8).** The `never` arm (budget 0) dies with `fw == 8` on every
  individual — no reconstruction, no recovery. The fix is not "never repair".
- **State sufficiency holds (G6, 16/16)** — the per-tick observer-discard on `both` is byte-identical.
- **The adversarial priority is not the breaking point (G7, 4/4).** All four `[3,0,2,1]` seeds
  survive the single challenges and recover under `both` (AC101's G6, restated).
- **Completeness + determinism + arm identity (G8).** 96 rows; sampled rerun byte-identical;
  `move_only == AC100 gray_ctl`, `both == AC101 gray_ctl`, and the budgeted maintain at budget=None
  == the frozen maintain (the regen_budget is the only change in `staged`/`never`).

## Per-seed outcome (both histories identical)

| seed | priority    | neither | move_only | corrupt_only | both (immediate)     | staged (budget 8)     | never (budget 0)  | mat@8192 |
|------|-------------|---------|-----------|--------------|----------------------|-----------------------|-------------------|----------|
| 4880 | `[1,0,2,3]` | survive | survive   | survive      | survive (rec 8241)   | survive (rec 8239)    | dies 8266, fw=8   | 127      |
| 4934 | `[1,3,0,2]` | survive | survive   | survive      | **dies 8408**, streak 5 | **dies 8408**, streak 5 | dies 8298, fw=8 | 71     |
| 4950 | `[1,3,2,0]` | survive | survive   | survive      | survive (rec 8204)   | survive (rec 8224)    | dies 8282, fw=8   | 99       |
| 5002 | `[2,3,1,0]` | survive | survive   | survive      | **dies 8408**, streak 5 | **dies 8408**, streak 5 | dies 8297, fw=8 | 72     |
| 4883 | `[3,0,2,1]` | survive | survive   | survive      | survive (rec 8222)   | **dies 8248**, fw=2   | dies 8253, fw=8   | 109      |
| 4901 | `[3,0,2,1]` | survive | survive   | survive      | survive (rec 8193)   | survive (rec 8195)    | dies 8296, fw=8   | 72       |
| 4928 | `[3,0,2,1]` | survive | survive   | survive      | survive (rec 8193)   | **dies 8263**, fw=2   | dies 8282, fw=8   | 85       |
| 5038 | `[3,0,2,1]` | survive | survive   | survive      | survive (rec 8193)   | survive (rec 8262)    | dies 8299, fw=8   | 112      |

"mat@8192" is the material level at the corruption tick — the economic covariate that sorts the
death-prone seeds (71, 72) from the survivors (≥ 72; note 4901 at 72 survives, so the boundary is
tight around ~72, seed-dependent, not a clean threshold).

## The budget trace (step 2) — what actually spends the material

Recorded per row (`budget_trace`, t = 8188..8223) and re-derived by the audit without simulating:

- **The reconstruction (`reg_from_active`) is the spender, not the program's repair.** At t=8192
  the reconstruction writes ~24 replicas in ONE tick (material ~71 → ~41 on 4934), dropping material
  below 64 and setting observation bit 1 (material ≤ 64). The program then answers with action 1
  (material contact) on the now-stale route 1 (unproductive), and the paid Gray streak increment
  (7 material/tick) starves — on 4934 the streak stalls at 5 and the drop never fires.
- **The program's majority repair (action 2) is cementing, not curative.** For the corruption
  (4 of 7 replicas flipped), majority restore writes the 3 correct replicas to the wrong value —
  cementing the flip. It does NOT fire in the immediate arm on the death-prone seeds (obs bit 1
  outranks obs bit 2), but DOES fire on the high-material seeds (where material stays above 64),
  and on every seed under `staged`. This is the AC61 distinction, now measured as the cause of the
  staged arm's G4 failure.
- **The W/C collapse, not material exhaustion, is the proximate death.** The death seeds' material
  recovers to 128 by death (the AC101 errata point); what does not recover is the W/C machinery
  (energy 0). The initiating shortage (below 64 at t=8192) must be distinguished from the
  irreversible machinery loss that actually kills.

## The two failure modes of staging, both falsifying the timing hypothesis

1. **On the death-prone (marginal) seeds, staging does not even avoid the hypothesized mechanism.**
   4934/5002 have material 71/72 at the corruption tick, so ANY reconstruction spend of ≥ 8 drops
   material below 64 and fires obs bit 1 — the hijack happens regardless of the budget. Death is at
   8408 under both immediate and staged.
2. **On the high-material seeds, staging trades the hijack for a worse failure.** With material
   above 64 after a small (≤ 8) spend, obs bit 1 does NOT fire; the program instead answers obs bit 2
   (corruption) with action 2 (majority restore), which cements the corruption. The reconstruction's
   trigger is obs bit 2, whose minority count drops to zero once the flip is cemented — so the
   reconstruction stalls until the description's own damage re-triggers it. On 4883/4928 that
   re-trigger comes too late (they die at 8248/8263 with `fw == 2`); on 4880/4950/5038 it arrives in
   time (recovery 8239/8224/8262, survival). The immediate reconstruction outruns the cementing in a
   single tick; the staged one cannot.

The two constraints on the reconstruction are therefore in **tension**: it must be FAST enough to
complete before the program's cementing majority repair (G4's lesson), but at that speed its
material cost drops a marginal economy below the obs-bit-1 threshold (G3's lesson). On a marginal
economy (material ≤ 72) neither can be satisfied, and the composition fails.

## Gates (prespecified in the protocol)

- **G1 interaction (death requires both) — PASS 8/8.**
- **G2 reconstruction recovers under `both` — PASS 8/8.**
- **G3 timing hypothesis — staged rescues the composition failure — PASS-in-the-falsifying-
  direction** (staging does NOT rescue; the 2 death seeds die under both arms at 8408).
- **G4 staged schedule preserves recovery — FAIL 2/8** (4883, 4928 stall at fw=2 and die). Recorded,
  not moved (AC16/17).
- **G5 never-repair must fail — PASS 8/8.**
- **G6 state sufficiency (per-tick observer-discard on `both`) — PASS 16/16.**
- **G7 adversarial-priority stratum — PASS 4/4.**
- **G8 completeness + determinism + arm identity — PASS** (96 rows; sampled rerun byte-identical;
  `move_only == AC100`, `both == AC101`, budgeted maintain at budget=None == frozen maintain).

## Reported, not gated

- **The second-move death mode.** The disclosed scan (4872-5099) found a second distinct failure:
  deaths at ~12,500 with the streak stuck at 5 after the SECOND move (e.g. 4875, 4905) — distinct
  from the first-move 8408 death, not a gate.
- **The material level at the corruption tick** — the economic covariate that sorts death-prone
  (≤ 72) from survival (≥ 72) seeds. Reported, not gated (the boundary is seed-dependent, not a
  clean threshold).
- **The recovery-tick spread.** On the high-material seeds the immediate reconstruction recovers at
  ~8222-8241 (later than the death-prone seeds' ~8193), because the program's action-2 cementing
  delays the reconstruction's completion — the reconstruction recovers, but later. Reported.
- **Active vs passive relinquishment** per seed per move (the death seeds never relinquish; every
  survivor relinquishes at both moves).
- **The unseen stratum's priorities** — reported, not prespecified (the stratum is stratified by
  material level, disclosed pre-freeze, not by priority).
- **Survival is a bimodality-aware lower bound** (AC68).
- **Supplied machinery remains** — `advance()` and `prog.choose` are still host-supplied
  format-level machinery; no autopoiesis claim. The reconstruction budget is a property of the
  reconstruction primitive, not new content.

## Verification

- `audit_ac102.py` passes: 96 rows, all source hashes valid (no drift), the eight gates re-derived
  WITHOUT simulating and matching the recorded result (including the G4 FAIL), the interaction
  invariant, the budget-trace claim, and seed-disjointness.
- `replay_ac102.py` passes: 6/6 arms byte-identical on the first row, the death seed 4934's `both`
  and `staged` rerun byte-identical (both die 8408), observer-discard 1/1 per-tick byte-identical,
  arm-identity 1/1.
- `test_ac102.py` green (19 tests): the budgeted-maintain source surgery (budget=None reproduces
  the frozen maintain byte-for-byte; budget bounds the per-tick writes), the arm identities, the
  engineering seed-1 interaction (death requires both; staged does not rescue), and the recorded
  final outcomes (G4 FAIL pinned, the death seeds, the interaction, seed-disjointness).
- Core AC1-9 suite (56 tests) green. No frozen runner modified (`ac101.py`, `ac100.py`, `ac99_d2.py`
  and every earlier freeze untouched).

## Boundary and next step

The composition failure is an **economic** limit, not a **timing** one: the reconstruction's price
(~24 material in one tick) is what a marginal economy (material ≤ 72 at the corruption tick) cannot
absorb, and the reconstruction must remain immediate because its speed is load-bearing against the
program's cementing majority repair. The candidate fixes AC101 named — "a reconstruction staged not
to drop material below the obs-bit-1 threshold" — is now measured and REJECTED: staging does not
rescue the marginal seeds and breaks recovery on the rest. What remains open is unchanged in kind
from AC96-D4 and AC101: the reconstruction and the adaptation's decision write share ONE
material-denominated budget, and on a marginal economy they cannot both be funded. A fix that does
not change the resource model must change WHICH spend is prioritized, not WHEN the reconstruction
spends (a decision write that is not material-denominated, or an explicit budget priority between
the reconstruction and the relinquishment decision) — left to a later study. Boundary unchanged: no
autopoiesis claim; `advance()` + `prog.choose` supplied; the reserve is still not part of the
architecture. All earlier results preserved untouched.
