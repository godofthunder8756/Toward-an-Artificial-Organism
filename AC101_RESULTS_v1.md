# AC101 results v1: composition test — the four capabilities compose in the internal-state sense, but not unconditionally: the reconstruction's material cost hijacks the adaptation economy on 1/4 unseen finals (the adversarial stratum composes 4/4)

Parent: AC100. Frozen per `AC101_PROTOCOL_v1.md` (hashed before the first final seed). Runner
`ac101.py` (a faithful copy of `ac100.py`'s `gray_ctl` arm with ONE parameter change: `corrupt=True`).
Seeds **4448-4451** (unseen) + **4466, 4481, 4504, 4510** (adversarial `[3,0,2,1]`) × 2 histories,
16 rows, 16,384 ticks, the combined challenge of a controller corruption (t=8192) AND two route
reversals (channel-1 port flips at t=8192 and flips back at t=12288). One arm per individual:
`gray_ctl` (Gray streak, no reserve). Both strata unseen: disjoint from engineering 0-7, from every
prior final family ≤ 4447, and from the 4600-4871 / 5100-5507 families.

**Headline:** the four demonstrated capabilities **do compose in one organism, but not
unconditionally**. The internal-state composition — controller reconstruction (`fw` 8→0),
description maintenance (130/130), and recipe turnover (≥1 succession) — holds on **8/8** distinct
seeds. The behavioural composition — adaptation (re-acquisition at every move) + continued
production + survival — holds on **3/4** unseen seeds (4448, 4449, 4451) and **4/4**
adversarial-priority seeds (4466, 4481, 4504, 4510), failing on the unseen seed **4450**, which
dies at **8408** via the exact interaction the engineering screen found on seed 1 (identical death
tick, identical streak stall at 4).

## Verdict

**Five of six gates pass; G2 fails, recorded not moved.** The composition answer is split cleanly
along the internal-state / behavioural boundary:

- **The internal-state composition is UNCONDITIONAL (G1, 8/8).** Every individual — including the
  dying seed 4450 — applies the corruption (`fw_at_corrupt == 8`), recovers it (`flipped_still_wrong
  == 0`), keeps the description intact (130/130 at the horizon for survivors, 130/130 at death for
  the non-survivor), and turns over the recipe (≥1 succession: 6 on every survivor, 3 on the dying
  seed). These are point endpoints, not uninterrupted functioning: reconstruction recovered and the
  description remained intact at death, but the three successions on 4450 may precede the challenge,
  and that seed has zero post-move W/C/B births.
- **The behavioural composition is NOT unconditional (G2: 3/4 unseen, 4/4 adversarial).** Seed 4450
  (priority `[0,3,2,1]`) dies at 8408 with the route never re-acquired, production stopped entirely
  in the first post-move window, and the W/C collapse (energy 0, fuel 15, material 128). This
  reproduces the engineering seed-1 outcome — same death tick (8408), same streak stall (4) — which
  strengthens reproducibility, not causal isolation.
- **The adversarial priority is NOT the breaking point (G6, 4/4).** All four `[3,0,2,1]` seeds
  fully compose (survive, relinq `[1,1]`, reacq `[1,1]`, fw=0, desc 130). The AC83 adversarial
  concern does not bite under the combined challenge; the failure is an economy interaction, not a
  renewal-contention one.
- **State sufficiency holds under the combined challenge (G3, 16/16).** The per-tick observer-discard
  on gray_ctl is byte-identical at every tick — the Gray streak is recovered from maintained state
  alone even with the controller actually corrupted.
- **The corruption is the only change (G4, 16/16).** gray_ctl at `corrupt=False` reproduces AC100's
  gray_ctl byte-for-byte, licensing attribution of every difference to the corruption alone.

## Per-seed outcome (both histories identical)

| seed | priority    | outcome | relinq_by_move | reacq_by_move | fw (at corrupt → end) | desc (end / at death) | succ | streak_final |
|------|-------------|---------|----------------|---------------|-----------------------|-----------------------|------|--------------|
| 4448 | `[2,0,3,1]` | survive | `[1,1]`        | `[1,1]`       | 8 → 0                 | 130 / —               | 6    | `{0:0,1:0}`  |
| 4449 | `[0,3,1,2]` | survive | `[1,1]`        | `[1,1]`       | 8 → 0                 | 130 / —               | 6    | `{0:0,1:0}`  |
| 4450 | `[0,3,2,1]` | **dies 8408** | `[0,0]`     | `[0,0]`       | 8 → 0                 | 71 / 130              | 3    | `{0:0,1:4}`  |
| 4451 | `[3,0,1,2]` | survive | `[1,1]`        | `[1,1]`       | 8 → 0                 | 130 / —               | 6    | `{0:0,1:0}`  |
| 4466 | `[3,0,2,1]` | survive | `[1,1]`        | `[1,1]`       | 8 → 0                 | 130 / —               | 6    | `{0:0,1:0}`  |
| 4481 | `[3,0,2,1]` | survive | `[1,1]`        | `[1,1]`       | 8 → 0                 | 130 / —               | 6    | `{0:0,1:0}`  |
| 4504 | `[3,0,2,1]` | survive | `[1,1]`        | `[1,1]`       | 8 → 0                 | 130 / —               | 6    | `{0:0,1:0}`  |
| 4510 | `[3,0,2,1]` | survive | `[1,1]`        | `[1,1]`       | 8 → 0                 | 130 / —               | 6    | `{0:0,1:0}`  |

## The proposed cascade (a hypothesis, not yet causally isolated)

**The composition introduces a material-economy interaction, not a reconstruction failure.** On
4450 (and engineering seed 1, identically) the corruption at t=8192 forces the bank-0 repair
(action 2), which spends ~32 material over t=8192-8193, dropping material below 64 and setting
observation bit 1 (material ≤ 64). The program then answers with action 1 (material contact) on the
now-stale route 1, which is unproductive. The internalized Gray streak is **paid**, so during that
transient shortage the increment stalls at **4** (< STREAK_N=6); the drop never fires and the stale
entry is never erased. The proposed cascade is repair spend → obs bit 1 → material-contact hijack →
paid-streak starvation → W/C collapse. **This cascade is a hypothesis, not an established mechanism**:
G4 (corrupt=False is byte-identical to AC100's gray_ctl) licenses attributing the difference to the
corruption, but it does NOT isolate the causal path to 4450's death, and no arm here tests it
directly.

**Distinguishing the initiating shortage from the irreversible loss.** The material-at-death value
is **128**, not ~0 — so the account must separate the *initiating* material shortage (the transient
drop below 64 over t=8192-8193 that stalled the paid streak) from the *later irreversible machinery
loss* (W and C collapse, energy 0) that actually killed the organism. Material recovers to 128 by
death; what does not recover is the W/C machinery. The failure is **not** in the internal-state
machinery content: at death the reconstruction is complete (fw=0) and the description is intact
(130/130 at death; the 71/130 end read is post-mortem degradation, AC79). What is not established is
the exact ordering by which the transient shortage became an irreversible loss.

**The interaction reproduces, which is evidence of transfer, not of causal isolation.** The
engineering seed 1 (`[0,1,3,2]`) and the final seed 4450 (`[0,3,2,1]`) die at the SAME tick (8408)
with the SAME streak stall (4) — matching death ticks and stall counts strengthen reproducibility,
not causal isolation. But the four adversarial `[3,0,2,1]` seeds all fully compose, so the AC83
renewal-contention priority is not what breaks. The proposed account is that this is the AC96
economic finding (the paid decision-state write is starved by the income collapse the decision
exists to pre-empt) re-entering through the reconstruction's material cost — AC82/AC83's material-low
hijack (obs bit 1) operating now on the internalized streak — but confirming that requires a direct
causal test (e.g. a decision write that is not material-denominated, or a reconstruction staged not
to cross the obs-bit-1 threshold), not the current attribution.

## Gates (prespecified in the protocol)

- **G1 internal-state composition — PASS 8/8.** Every distinct seed: `fw_at_corrupt == 8`,
  `flipped_still_wrong == 0`, description intact (130 at horizon, or 130 at death), `successions >= 1`.
- **G2 behavioural composition (adaptation + production + survival) — FAIL: 3/4 unseen, 4/4
  adversarial.** The unseen seed 4450 dies with no re-acquisition and no post-move production.
  Recorded, not moved (AC16/17).
- **G3 state sufficiency (per-tick observer-discard on gray_ctl) — PASS 16/16.**
- **G4 corrupt-is-the-only-change (arm identity) — PASS 16/16** (gray_ctl at corrupt=False is
  byte-identical to AC100's gray_ctl).
- **G5 completeness + determinism — PASS** (16 rows; sampled rerun byte-identical).
- **G6 adversarial-priority stratum — PASS 4/4** (all four `[3,0,2,1]` seeds satisfy G1 and G2).

**Gate difference from AC100 (stated explicitly).** AC101's behavioural gate (G2) does NOT require
active relinquishment — `relinquishments_by_move` is reported, not gated (disclosed in the protocol
before finals) — whereas AC100's per-move criterion required active drops (`relinq_by_move == [1,1]`).
On these finals every survivor actively relinquishes at both moves anyway, so the outcomes are
unchanged; the two studies' acceptance criteria are nonetheless not identical.

## Reported, not gated

- **Active vs passive relinquishment.** On the finals every survivor relinquishes actively at both
  moves (`relinq_by_move == [1,1]`). The passive-expiry degradation seen on engineering seeds 6 and
  7 did NOT recur on the finals (the finals' survivors all actively drop) — the AC39 transfer
  caveat ran in the favourable direction for that sub-finding. Reported, not gated.
- **The proposed 4450 interaction cascade** (reconstruction material cost → obs bit 1 →
  material-contact hijack → paid-streak starvation → W/C collapse) — a hypothesis, not an
  established mechanism; it needs a direct causal test.
- **The unseen stratum's priorities** — reported, not prespecified (unseen seeds).
- **Survival is a bimodality-aware lower bound** (AC68).
- **Supplied machinery remains** — `advance()` and `prog.choose` are still host-supplied
  format-level machinery; no autopoiesis claim.

## Verification

- `audit_ac101.py` passes: 16 rows, 20 source hashes no drift except the one disclosed
  protocol-hash drift below, the per-individual composition invariants, the two-run records
  (observer-discard 16/16, arm-identity 16/16), and the gates re-derived WITHOUT simulating and
  matching the recorded result (including the G2 FAIL).
- `replay_ac101.py` passes: 4/4 exact (state_hash + endpoint fields), observer-discard 1/1
  per-tick byte-identical, arm-identity 1/1.
- `test_ac101.py` green (15 tests): schedule/arm-identity, the engineering recorded outcomes (the
  seed-1 interaction, the seeds-6/7 passive first move, adversarial-engineering survival), the
  finals recorded outcomes (G2 FAIL pinned, the 4450 interaction, the adversarial-stratum full
  composition, seed-disjointness), per-tick observer-discard, and conservation (ac4.balance asserts
  hold in-step).
- Core AC1-9 suite (56 tests) green; no frozen runner modified (`ac100.py`, `ac99_d2.py`, `ac99.py`
  and every earlier freeze untouched).
- **Errata (post-freeze, narrative only):** `AC101_RESULTS_v1.md` and `AUTONOMY_RESEARCH_STATUS.md`
  were corrected after the freeze for four reviewer points: the G2 behavioural composition is
  reported per stratum (3/4 unseen, 4/4 adversarial) instead of a single "7/8"; G1 is worded as its
  listed endpoints (reconstruction recovered, description intact at death) rather than
  "uninterrupted internal-state functioning"; the gate difference from AC100 (active relinquishment
  reported, not required) is stated explicitly (in this doc); and the 4450 cascade is downgraded
  from "mechanism" to a hypothesis needing a direct causal test (with the initiating material
  shortage distinguished from the later irreversible W/C loss — material is 128 at death, not ~0).
  `AC101_PROTOCOL_v1.md` is **byte-frozen** at its recorded hash (`05a9ea3a…`) — the corrections
  live in this results doc (which is not a hashed source), and `audit_ac101.py` passes with no hash
  drift. The frozen `rows.jsonl`, `results.json` and `pre_run_snapshot.json` are unchanged.

## Boundary and next step

The composition test answers the question with a split: the internal-state half of the composition
(reconstruction, description, turnover) is unconditional, while the behavioural half (adaptation +
survival) is economy-limited. The limit is not a missing capability
and not the AC83 adversarial priority; it is the **paid decision state's affordability** — on the
proposed account the internalized streak's increments are starved by the reconstruction's material
cost on top of the move's income cut, so the relinquishment decision the adaptation depends on can
stall below threshold and the organism dies holding a stale route (a hypothesis needing a direct
causal test, not an established mechanism). The next open item is unchanged in kind from
AC96-D4 (an acquired allocation that funds the decision) but now names the composition-specific
trigger: the reconstruction spend must not be allowed to collide with the adaptation's own
decision budget (e.g. a decision write that is not material-denominated, or a reconstruction that is
staged to not drop material below the obs-bit-1 threshold). Boundary unchanged: no autopoiesis
claim; `advance()` + `prog.choose` supplied; the reserve is still not part of the architecture.
All earlier results preserved untouched.
