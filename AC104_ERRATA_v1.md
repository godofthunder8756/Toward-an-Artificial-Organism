# AC104 errata v1: generalization untested (not "cannot"); the fresh sample had no rescue opportunity; the allowance is a spend constraint, not guaranteed decision funding; 5702 relinq [0,1] not 2/2

2026-09-22. Non-frozen correction note, in the AC100/102/103 convention. The frozen artifacts are
preserved unchanged — `ac104.py`, `AC104_PROTOCOL_v1.md` (a hashed source), and
`ac104_results_v1/{rows.jsonl, results.json, pre_run_snapshot.json}` — no gate was re-run and no
frozen code or protocol was edited. `AC104_RESULTS_v1.md` (not a hashed source) and
`AUTONOMY_RESEARCH_STATUS.md` carry the corrected narrative; this note records the corrections.

## 1. Generalization wording: untested, not "cannot"

Replace "a fixed declared allowance cannot be gated to rescue every unseen marginal economy" with
**"generalization of allowance 42 to unseen marginal economies remains untested."** The two
diagnostic thresholds — 33 on engineering seed 1, 42 on 5603 — demonstrate *different* requirements
in two diagnostic cases, and 42 covers both. That does not establish that a fixed allowance cannot
be gated to an unseen economy; it establishes only that 42 has not been tested on one.

Also: equal starting material (both 65) does **NOT** isolate priority as the cause of the threshold
difference. The two seeds differ in other respects too (different priorities `[0,1,3,2]` vs
`[1,2,3,0]`, different trajectories), so the 33-vs-42 difference is not attributed to priority
alone. Do not state it as the priority's effect.

## 2. The fresh sample had no rescue opportunities

"Rescue did not transfer" / "did not recur" reads as a failed replication. In fact **all eight
controls survived**, so the fresh cohort (5700-5707) tests tolerability and recovery, not rescue
efficacy. Report **eight distinct seeds × two histories**, not 16 rows treated as independent
opportunities.

## 3. The allowance is a reconstruction spending constraint, not guaranteed decision funding

G3 counts post-corruption ticks with material below 42; it does **NOT** guarantee that the next
decision stays affordable. In seed 5702 those ticks fall from 51 (control) to 48 (candidate) — the
allowance is *still breached* under the candidate. The mechanism is useful despite the allowance
still being breached; say this explicitly rather than implying the allowance is preserved.

## 4. Seed 5702 relinq [0,1], not 2/2

"Every final survivor relinquishes 2/2" is false: seed 5702 records `relinquishments_by_move
[0,1]` in **both arms and both histories** (`relinquishments == 1`). G4 establishes no
deterioration relative to the control; it does **NOT** establish active relinquishment after every
move.

## 5. Headline replacement (exact wording)

> An internally evaluated reconstruction budget rescues two diagnostic failures and preserves
> survival, recovery, and relinquishment counts on eight fresh seeds. Rescue generalization
> remains untested.

Replaces the earlier headline ("...its rescue of the marginal seed is conditional on a marginal
economy and did not recur on the fresh sample") and the "fixed declared allowance cannot be gated
to rescue every unseen marginal economy" framing, which over-claimed in both directions.

## 6. Verification and audit state

Frozen artifacts untouched. `audit_ac104.py` checks the frozen snapshot (`ac104_results_v1/`), not
this note; `AC104_RESULTS_v1.md`'s verification section still refers to that audit. This note is
non-frozen and is not hashed into the snapshot.
