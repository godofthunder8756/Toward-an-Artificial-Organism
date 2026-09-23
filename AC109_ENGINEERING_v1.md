# AC109 (C1, engineering): the stored cause-estimate adds nothing over a direct diagnostic controller

2026-09-23. Engineering only — no protocol, no freeze, no finals. This answers the C1
card's question: does the AC107 stored one-bit cause-estimate add information, decisions, or
benefit BEYOND a rival that reads the diagnostic interface (bound, used_held, productive)
directly at decision time, with no stored estimate?

**Verdict: EQUIVALENCE (falsification of "storage adds benefit").** The direct diagnostic
matches the stored-estimate candidate on every behavioural endpoint, and the stored estimate
is pure cost — it buys no information, no decision, and no benefit. Reported honestly, rival
not weakened.

---

## 1. The direct-diagnostic rival (`direct`)

`ac109.py` adds one arm to the frozen AC107 world by patching `ac107._make_alloc` (the AC108
extension rule); the frozen arms delegate to the original factory and are proven inert by a
`state_hash` reproduction gate (16/16). The rival keeps everything the candidate has except
the storage:

- Same information access: `bound = o.memory.read(1) is not None` (unshimmed introspection),
  `used_held` (the shimmed retrieval result, forwarded by the injected outcome line),
  `productive = e['productive'] > 0`.
- Same discriminator rules, evaluated on the CURRENT triple:
  - `bound & not used`        -> E_machinery (cut signature)
  - `used & not productive`   -> E_world   (held entry failed -> stale)
  - `not bound & productive`  -> E_world   (blind re-bind -> re-acquisition)
  - no rule fires             -> E_world   (the acquired reactive default, which the acquired
                                            bit already holds)
- Same decision timing (per contact-1), same permitted actions (`_drop`/`_restore`,
  `gray_streak_write`, proactive renewal), same maintained per-key Gray streak.
- The only difference: the cause label is a transient local. It is never written to vulnerable
  state and never read back, so the rival has no estimate-bit write (`bel_writes == 0`) and no
  persistence of the last conclusion into contacts where the diagnostic is silent.

Rules 2 and 3 and the silent default all conclude E_world — the value the acquired bit already
holds — so the transient cause collapses to "machinery iff the read is suppressed while the
entry is still bound". This is the candidate's own rule set with the two E_world branches and
the fallback collapsed to their common value, not a weakened rival.

## 2. Results (engineering seeds 0-7, 16 individuals, 48 seed/history/condition cells)

- **Inertness**: the patched factory reproduces the frozen candidate byte-for-byte in 16/16
  (`state_hash` equality). The extension does not disturb the frozen arms.
- **Behavioural equivalence**: 48/48 cells identical on every decision endpoint —
  `completed`, `first_dead`, `relinquishments`, `routes`, `drop_ticks`, `reacquire_ticks`,
  `streak_final`. The direct diagnostic makes the SAME hold/drop decisions at the SAME times,
  retains the SAME routes, and survives identically (16/16 in every condition).
- **Conclusions**: in `no_cause` and `move` the two arms' conclusion-event sequences are
  event-for-event identical (16/16); in `cut` the sequence differs (0/16) only because the
  candidate's 7-replica estimate write shifts its contact schedule, while the conclusion KINDS
  remain identical (16/16) — both arms only ever conclude `machinery_cut` in-window.
- **Cost** (the only divergence, in the candidate's disfavour):
  - `bel_writes`: candidate 7 in `cut` (the single atomic 1->0 storage flip), 0 in `no_cause`
    and `move`; direct 0 everywhere.
  - `proactive_writes` in `cut`: candidate 72-141 vs direct 0-13. The candidate's stored
    e=0 never resets after the window, so it keeps paying redundant proactive renewal for the
    rest of the run; the direct arm stops when the diagnostic goes silent. Both are redundant
    anyway (AC107 M6: the frozen reactive renewal holds the entry).

## 3. The three hypothesis conditions, answered

- (a) *adds information unavailable in the current observation* — **NO.** The discriminator is
  a pure function of the current (bound, used_held, productive) triple; K4's perfect
  identifiability (disjoint action-observation histories) means the current observation already
  fully determines the cause. There is nothing for a stored bit to remember.
- (b) *supports decisions between diagnostic observations* — **NO.** The decision is made
  per-contact, the same granularity as the diagnostic. This world has no between-observation
  decision the bit could serve.
- (c) *alters behaviour/cost beyond direct use* — **NO benefit; only cost.** Behaviour is
  identical (48/48); the estimate adds a 7-write storage cost and a persistence-driven stream
  of ~100 redundant proactive renewals.

## 4. Disposition

The AC107/108 positive — the estimate's CONTENT is causally load-bearing (E_machinery vs
E_world selects hold vs drop-fast) — is not contradicted. What C1 shows is the narrower fact
that the estimate's STORAGE (persistence) carries no load in this world: the content is
recomputable from the current observation alone. The estimate's causal role is as a content
SELECTOR, not as a memory. A stored estimate would only earn its keep in a world where the
diagnostic is not a pure function of the current observation (partial observation, noise, a
third cause, or a decision that must outlive the observation that supported it) — exactly the
reopening conditions already on record for K8.

**Stop condition**: C1 is answered — the rival exists, the comparison is measured, equivalence
is reported honestly. Unblocks C2 with this disposition: no persistence benefit in the
AC107/108 two-cause world.

## Verification

All numbers recomputed from `ac109_engineering_v1/rows.jsonl` (96 rows) and `results.json`.
No frozen artifact (runner, protocol, results dir, or hash) was edited. `ac107.py`,
`ac106.py`, and the AC107/108 frozen rows are untouched.
