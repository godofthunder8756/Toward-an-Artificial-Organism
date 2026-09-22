# AC106 — the causal role of a maintained belief: engineering result is NEGATIVE (no protocol frozen)

2026-09-22. **Engineering report, not a study.** No protocol, no final seeds, no freeze. This is C2's
engineering measurement of the C1 task (`MAINTAINED_BELIEF_TASK_v1.md`), run on engineering seeds
0-7 (2 histories each). It is reported as a finding, exactly as the card's falsification rule
requires: a negative result is a finding and completes the card honestly.

## 1. What was built

`ac106.py` implements the C1 task on the AC100 Gray-streak architecture (corrupt=False, 16,384
ticks, DEV=512, PORTS=4 so blind fallback is 1/4, mapping over {0,1}):

- **Two causes** (conditions), both landing at T = 8192 as an "identical immediate failure" (a
  channel-1 contact stops yielding):
  - `move` (E_world): the channel-1 mapping flips; the route-1 entry is intact but stale.
  - `cut` (E_machinery): the organism's READ of the route-1 entry is suppressed for a 96-tick
    window (`ReadCut`, the same machinery-suppression kind as `ac9.blocked` / the AC91-92 W-cut);
    the entry is intact and correct, contacts fall back to blind search.
  - `no_cause`: neither (baseline).
- **The estimate** e ∈ {E_world, E_machinery}: a one-bit second-order state in a dead-rule action
  bit (14·dead_rule_index + 10, acquired value 1 = E_world, the AC12 inverted-semantics pattern),
  damaged by the ambient sticky-SET stream, read by majority, repaired by the paid bank-0
  majority-restore (action 2), excluded from `reg_from_active`. Update rule (from the organism's
  own outcomes only): productive contact-1 after a failure → e = E_machinery; relinquishment →
  e = E_world. Two consumptions: E_world → relinquish at the streak threshold; E_machinery →
  withhold relinquishment (infinite threshold) + proactive paid renewal of the entry.
- **Five rivals + one control**: `r2` = the frozen Gray streak (STREAK_N=6, the history-based
  rival); `r4` = a longer-threshold counter (no proactive renewal — the C1 §7 sharpest
  falsification); `r1` = reactive (relinquish on first failure); `r3` = state-blind duty cycle;
  `scramble` = the candidate with the estimate forced to E_world (the causal-role control, P4).

Verified before measurement: the runner is a faithful copy of ac100 — `r2` at the AC100
single-move world (PORTS=2) reproduces ac100 `gray_ctl` **byte-for-byte** (`state_hash`), and
the no-cause arm is byte-identical (`candidate == r2`). The estimate is inert by construction
where no cause is present (G4 holds).

## 2. The measured result (engineering seeds 0-7, 16 individuals)

Endpoints, per condition (all 16,384 ticks; every arm completes):

| condition | arm      | relinquishments            | entry survives cut | bel at horizon | proactive writes |
|-----------|----------|----------------------------|--------------------|----------------|------------------|
| `cut`     | candidate| 0 (14/16), 1 (2/16)        | yes (14/16)        | E_machinery    | 97-171           |
| `cut`     | r2       | 0 (8/16), 1-2 (8/16)       | yes (8/16)         | E_world        | 0                |
| `cut`     | r4       | same as r2                 | same as r2         | E_world        | 0                |
| `cut`     | scramble | same as r2                 | same as r2         | E_world        | 0                |
| `move`    | candidate| 1 (16/16)                  | —                 | E_machinery    | 64-171           |
| `move`    | r2       | 1 (16/16)                  | —                 | E_world        | 0                |

The four seeds where r2/r4/scramble relinquish in `cut` (3, 4, 5, 7 — the priority corner, where
the acquired priority ranks the material contact ahead of the renewal, so the organism contacts
channel 1 repeatedly through the cut and the streak reaches 6) are also the four where the
candidate's hold is *not* uniform: on seeds 3, 5, 7 the estimate latches E_machinery in time and
holds (candidate 0 vs r2 1-2), but on seed 4 the streak reaches 6 *before* the first blind success
latches the estimate, and the candidate also relinquishes (1 vs 2). So the candidate holds 14/16
where r2 holds 8/16 — a real but partial, seed-dependent edge.

## 3. Three measured reasons the task is not discriminating

**R1 — the estimate's update rule cannot distinguish the causes (G1 fails).** The
"productive-after-failure → E_machinery" probe is confounded by re-acquisition. In `move`, after
the stale route is dropped (estimate reset to E_world), the post-drop blind contacts fail
(3/4) and then one succeeds (1/4); that success follows a failure, so the update rule fires and
sets e = E_machinery — misattributing the blind re-bind of a dropped stale route as "productivity
resumed without re-binding". The estimate reads E_machinery at the horizon in **both** `move` and
`cut`, so it carries no cause information. The C1 §6 "distinguishability argued before
implementation" fails: the hold-and-observe probe's "productivity resumed" signature is also
produced by the blind re-acquisition path, which the frozen world (grow=True, erase-on-
relinquishment) enables.

**R2 — the frozen streak already does the right thing in E_machinery (G2 fails).** The streak is a
3-bit Gray counter (max 7); at blind 1/4 the consecutive-failure count is reset by every blind
success, so it rarely reaches 6 — r2 *already holds* route-1 through the cut in 8/16 individuals,
without any estimate. The candidate's hold only differs from r2 on the 8/16 priority-corner
individuals (seeds 3, 4, 5, 7) where the streak does reach 6, and even there it is not uniform: on
seed 4 the streak reaches 6 before the estimate latches, and the candidate also relinquishes. The
estimate's "hold" adds nothing where the frozen counter already holds, and fails where it is
needed most (the fast-streak corner).

**R3 — the reactive renewal already maintains the entry (G6 fails).** The frozen program renews
the entry on the renewal-urgent observation bit (life ≤ 16), so r4 (no proactive renewal) keeps
the entry alive through the cut in 8/16 individuals — the candidate's proactive renewal spends
97-171 extra writes to no end. The proactive renewal only differs from the reactive renewal in the
8/16 priority-corner individuals, and even there the difference is a wasted spend, not a rescued
function.

## 4. Verdict

The maintained estimate is **not causally load-bearing** in this task. Its information is
confounded (R1: it reads E_machinery in both causes, so the "hold" is a blind
failure-then-success latch, not a cause attribution), and its causal role is partial and
seed-dependent: it holds through the cut in 14/16 individuals where r2 holds only 8/16, but (a)
it fails exactly on seed 4 where the streak reaches 6 before the estimate latches, and (b) the
"proactive renewal" it directs on top of the hold spends 97-171 replicas whose benefit the frozen
reactive renewal already provides. Scrambling the estimate leaves the behavioural outcome
unchanged in 10/16 individuals and only removes a redundant maintenance spend in the remaining
6/16.

This is the card's falsification, reached by its own pre-run controls: the organism was relying on
the first-order failure counter and the reactive renewal, not on a maintained second-order cause
estimate. The negative result is reported; no protocol is written and no confirmation data is
frozen, because the task as specified does not discriminate a maintained belief from its matched
rivals.

## 5. What would be needed to re-open (for C3/X1, not done here)

- **R1 fix (information):** the update rule must not fire on the blind re-acquisition path. The
  organism must distinguish "productivity resumed, entry still bound" from "entry dropped, blind
  re-bind" — e.g. gate the E_machinery conclusion on the entry still being *bound* at the resumption
  (a re-bind is `selected is None`, a held entry is `selected is not None`). C1 §4 named this
  re-bind-and-compare probe; it was not implemented and its absence is what R1 measures.
- **R2/R3 fix (causal role):** the estimate's hold must do something the frozen streak does not in
  a world where the frozen streak gets it wrong in *most* individuals, not a priority corner —
  e.g. an intervention that makes the streak mis-fire uniformly (a cut longer than the streak's
  reset horizon), or a maintenance target the reactive renewal cannot reach. The 3-bit streak's
  saturation also caps any longer threshold, so a "longer hold window" needs its own counter
  state, not the streak.

## 6. Discipline notes

- The runner is `ac106.py` (new file; no frozen study edited). Engineering output in
  `ac106_engineering_v1/` (rows.jsonl + results.json + gates). Verification helpers
  (`_ac106_smoke.py`, `_ac106_dbg.py`, `_ac106_dbg2.py`, `_ac106_key*.py`, `_ac106_probe_offsets.py`)
  are throwaway diagnostics, not part of any freeze.
- The ac100 byte-identity reproduction and the no-cause identity (G4) are the single-change
  license; both hold. Everything else in §2-§4 is a recorded measurement, not a gate that was
  moved.
