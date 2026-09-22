# AC103 errata v1: recovery count five of six (not 6/7); the defer uses advance knowledge of the challenge tick; the defer tests "stop once scarce," not budget preservation; bounded conclusion

2026-09-21. Non-frozen correction note, in the AC100/102 convention. The frozen artifacts are
preserved unchanged — `ac103.py`, `AC103_PROTOCOL_v1.md` (a hashed source), and
`ac103_results_v1/{rows.jsonl, results.json, pre_run_snapshot.json}` — no gate was re-run and no
frozen code or protocol was edited. `AC103_RESULTS_v1.md` (not a hashed source) and
`AUTONOMY_RESEARCH_STATUS.md` carry the corrected narrative; this note records the corrections.

## 1. Headline recovery count: five of six, not "6/7 cementing seeds"

`current_staged` fails recovery (`fw > 0`) on six seeds — 5601, 5602, 5604, 5605, 5606, 5607.
Persistence restores `fw == 0` on the first five (5601, 5602, 5604, 5605, 5606); 5607 stays
incomplete (`fw == 1`). `persistent_staged` recovery is 7/8 seeds (14/16), but that count includes
5600 and 5603, which already recovered under `current_staged` (`fw == 0`) without persistence —
they are not staged-recovery failures. "6/7 cementing seeds" therefore mixes denominators: 7 is the
persistent recovery count over all 8 seeds, 6 is the staged-stall population. Unless "cementing
seeds" is defined as a separate population, the correct statement is **five of six staged-recovery
failures** restored by persistence. Two of the restored seeds (5602, 5605) recover `fw == 0` but
still die — recovery and survival are separable (see §4).

## 2. The defer uses advance knowledge of the challenge time; observer-discard was run on `current`, not the persistent arms

The `persistent_defer` implementation gates deferral on `now >= CORRUPT_TICK and
o.body.material <= DEFER_THRESHOLD` (`ac103.py`, the maintain surgery). The policy therefore knows
the scheduled corruption tick — a disclosed experimental intervention, not a policy governed solely
by the organism's internal condition. Preserving the pre-challenge trajectory is useful
diagnostically (AC89's single-change rule), but using the scheduled corruption tick is unsuitable
for the eventual autonomous architecture; a fully internal defer must key off internal state alone.

Also: the observer-discard test (G5) was run on `current`, not on the new persistent arms. Source
inspection supports the claim that the persistent arms add no host-side state (the completion
condition is derived from the maintained program + description), but the direct per-tick
observer-discard test should follow the selected (persistent) architecture.

## 3. The defer tests "stop once scarce," not "limit spending to preserve a decision budget"

Deferring while `material <= 64` does not prevent the reconstruction from crossing 64: above the
threshold the policy permits the full reconstruction budget, so an organism just above 64 can spend
its way below it. The policy is "stop once scarce," not "limit spending to preserve a decision
budget." Its failure (5603 dies 8410, `fw == 2`) therefore does **NOT** reject the
budget-preservation hypothesis — an un-tested spending policy that caps total spend to preserve the
decision budget would need its own test.

## 4. Headline and conclusion replacement (exact wording)

> Persistent triggering restores reconstruction in five of six staged-recovery failures. Recovery
> and survival remain separable: some organisms reconstruct successfully and still die. Neither
> tested spending policy resolves every combined-challenge failure.

Replaces the earlier headline ("...closes the cementing recovery failure on 6/7 cementing seeds...")
and the conclusion's "shared material budget kills it regardless" framing, which was too broad. The
observed failures persist under these interventions; an **unavoidable funding limit has not been
established**.

## 5. Verification and audit state

Frozen artifacts untouched. `audit_ac103.py` checks the frozen snapshot (`ac103_results_v1/`), not
this note; `AC103_RESULTS_v1.md`'s verification section still refers to that audit. This note is
non-frozen and is not hashed into the snapshot.
