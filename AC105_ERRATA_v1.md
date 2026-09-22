# AC105 errata v1: unit-of-analysis and "never harms" scoping (all counts verified correct; 4 rescues = 1 seed × 2 shared-challenge schedules × 2 histories; allowance 42 is a reconstruction-spending constraint)

2026-09-22. Non-frozen correction note, in the AC100/102/103/104 convention. The frozen artifacts are
preserved unchanged — `ac105.py`, `AC105_PROTOCOL_v1.md` (a hashed source), and
`ac105_results_v1/{rows.jsonl, results.json, pre_run_snapshot.json}` — no gate was re-run and no frozen
code or protocol was edited. `AC105_RESULTS_v1.md` and `AUTONOMY_RESEARCH_STATUS.md` are not hashed
sources; their corrected narrative is carried in those files, and this note records the corrections.

Every claim count was re-derived from `ac105_results_v1/rows.jsonl` (160 rows) and
`ac105_results_v1/results.json` directly. **The counts are all correct**; the corrections are to the
*units*, the *replication framing*, and the *scope* of "never harms".

## 1. The unit of analysis: 160 arm-runs, not 160 observations; 80 matched comparisons

`rows.jsonl` holds 160 rows = 8 seeds × 5 conditions × 2 histories × 2 arms (`persistent`,
`persistent_budget`). Each row is an **arm-run**. The experimental unit is the **matched comparison**:
one seed × one condition × one history, pairing the two arms. There are 8 × 5 × 2 = **80 matched
comparisons**. The results doc's "Counts" line reports rescue, both-die and relinquishment-improvement
as `N/160`; those numerators are matched-comparison counts, so the denominator should be 80, not 160.
Stated as matched comparisons: **rescue 4/80, both-die 2/80, relinquishment-completeness improvement
6/80, reconstruction-harm 0/80.** The four counts were verified correct — only the denominator (and the
word "individuals") was wrong.

## 2. The 4 rescues attribute to ONE seed × TWO schedules × TWO histories

All four rescue comparisons are **5804** (priority `(0,3,2,1)`, `mat_at_corrupt` 71 in both arms), under
**`simult` and `simult3`**, in **both histories** (h0 and h1). Control dies at 8408 with
`relinquishments_by_move [0,0]` (simult) / `[0,0,0]` (simult3); the candidate survives with `[1,1]` /
`[1,1,1]`. No other seed × condition × history cell is a rescue (verified: exactly 4 cells where the
control dies and the candidate survives). The rescue is **one fresh seed**, not four independent
instances.

## 3. `simult` and `simult3` share the initial rescue challenge — not independent replications

Both schedules corrupt at tick 8192 and place the first route move at tick 8192 (verified from each
row's `corrupt_tick` and `schedule`); `simult3` differs only by adding a **third** move at 14336. The
5804 rescue fires on the same corruption-coincides-with-first-move event in both schedules; the
`simult3` case is the same rescue plus an extra move the candidate also survives. Treating `simult` and
`simult3` as two independent replications of the rescue mechanism therefore over-counts. The rescue is
demonstrated on **one fresh seed**; the two schedules (and the two histories, which share the seed's
RNG state) are correlated realisations, not independent units.

## 4. "Never harms" is scoped to the gated directions on the tested cohorts — the 5603 reconstruction harm stands

"Never harms" is true only when read as: on the **final sample (5800-5807)**, there is **no survival
reversal** (G3: 0 cells where the control survives and the candidate dies) and **no relinquishment harm**
(G4: 0 cells where the control survives and the candidate relinquishes less). It is **not** true of
every measured endpoint: the diagnostic **5603 under `late`** (engineering, disclosed) is a real
**reconstruction-level harm** — the candidate ends `flipped_still_wrong == 2` (reconstruction never
completed, `recovery_tick is None`) where the control recovers (`fw == 0`), both arms dying. The
headline's bare "never harms" must be scoped to "no survival reversal and no relinquishment harm on the
final 80 matched comparisons"; the 5603 reconstruction harm is retained as a finding, not folded into a
no-harm claim. (Verified: `flipped_still_wrong` is 0 for all 160 final rows, so reconstruction-harm on
the finals is genuinely 0/80 — the 5603 harm lives in the engineering screen, which is not persisted in
`rows.jsonl` and is reported only in the protocol and results docs.)

## 5. 5802 `move_first` is a shared failure, not an isolated causal diagnosis

Under `move_first`, 5802 dies under **both arms** (control 12539, candidate 12540), with `fw == 0`
(reconstruction complete) and `reacquisitions_by_move [1,0]` (the second move is never re-acquired) in
both arms. The observed fact is *shared, near-identical failure*; attributing it to "the re-acquisition
path, not the budget" is an **inference from the shared failure** (the two arms diverge only in the
spending rule, yet fail identically), not a separately isolated causal experiment. State it as such —
"both arms fail identically with reconstruction complete and the second move un-re-acquired, which
localises the failure outside the spending rule" — rather than as a demonstrated mechanism boundary.

## 6. Allowance 42 is a reconstruction-spending constraint, not guaranteed decision funding

`budget = max(0, material - 42)` caps what the reconstruction may spend, reserving 42 material so the
decision transition (streak → drop write) can be funded when material is scarce. It does **not**
guarantee the decision gets funded: on 5603 under `late` the allowance starves the reconstruction
(`fw == 2`) *and* the organism dies anyway — the reserved material buys neither reconstruction nor
survival there. The correct description is a **spend constraint that reserves a decision allowance**, not
"funds the decision" or "guarantees decision funding". (This repeats and carries forward AC104 errata §3,
now with a concrete finals-adjacent demonstration that the reserve can be wasted.)

## 7. Headline replacement (exact wording)

> The frozen allowance-42 budget holds its AC104 properties across the operating range, rescuing one
> fresh marginal priority (5804) in two schedules that share the initial challenge; no survival reversal
> and no relinquishment harm on the 80 final matched comparisons; one move-first boundary (5802) kills
> both arms.

Replaces "…it rescues a new marginal priority (5804), never harms, and improves relinquishment
completeness under late corruption; one move-first boundary (5802) kills both arms", which over-claimed
the rescue's replication breadth and the reach of "never harms".

## 8. Verification and audit state

Frozen artifacts untouched: `audit_ac105.py` re-derives the six gates and the three finding counts from
the frozen snapshot and still passes (rescue 4, reconstruction-harm 0, relinquishment-improvement 6 —
matched-comparison counts, no hash drift). This note is non-frozen and is not hashed into the snapshot.
`AC105_RESULTS_v1.md` and `AUTONOMY_RESEARCH_STATUS.md` carry the corrected narrative; the numbers they
report were already correct and are unchanged.
