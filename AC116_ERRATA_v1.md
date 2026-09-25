# AC116 — errata v1 (corrected inference + control-implementation audit)

2026-09-25. Reanalysis deliverable for the M2 card (t_0d15a26e). Reuses the frozen
evidence (`ac116_results_v1/`, 240 rows) — no simulation re-run, no frozen artifact
re-hashed, no gate moved, no new cohort launched. Every number below is read from
`rows.jsonl`. Seeds are the replication unit (8 independent units × 2 histories = 16
individuals); the paired comparisons aggregate the two histories within each seed (n=8).

Three things this errata does:
1. Correct the inference drawn from the G4 sign-flip result (the frozen outcome and the
   p=0.0625 threshold are preserved; only the gloss on top of them is withdrawn).
2. Audit the `scramble` read-control implementation and specify a clean readout-only
   intervention for future work.
3. Audit the counter candidate's handling of productive occluded observations.

---

## 1. Corrected inference: p = 0.0625 is the resolution floor, not evidence of absence

**The frozen primary outcome, unchanged:** per-seed combined post-cause income difference
d = income_post(counter) − income_post(tuned), n = 8:

| seed | d (counter − tuned) |
|---|---|
| 6600 | +128 |
| 6601 | +192 |
| 6602 | 0 |
| 6603 | 0 |
| 6604 | +576 |
| 6605 | 0 |
| 6606 | +192 |
| 6607 | +512 |

- five positive nonzero differences, three ties, **zero negative**;
- observed sum **+1600**, mean **+200**;
- exact two-sided sign-flip **p = 16/256 = 0.0625** (one-sided p = 8/256 = 0.03125).

**Why 0.0625 is the *smallest attainable* two-sided p at n=8 for this result.** The
sign-flip test re-signs the five nonzero differences and leaves the three zeros fixed; the
2^3 zero assignments only reproduce the same sum. The observed sum +1600 is the maximum
over all 2^5 signings (all five positive), so exactly one signing of the nonzero values
attains it — and its negation (all five negative) would also attain |−1600|, but that
direction does not occur in the data. Two-sided, the count is 2 · 2^3 = 16 of 256. No
sample with five nonzero and three tied differences could produce a two-sided p below
16/256; p = 0.0625 **is** the floor. The observed result is therefore the most positive
the test can express — the counter is *weakly dominant* (never worse, 5 better, 3 tied),
not merely "nonsignificant by a little".

**What this does and does not establish.**

- **Established (measured):** in the pure occluded-`used_held` world (ε=0, q=0.9), the
  maintained counter is *weakly dominant* on income over the tuned memoryless rival and
  the margin is at the sign-flip test's resolution floor, just above the prespecified 0.05
  threshold. Its accumulation is causally effective (G3: threshold-drop precedes the open
  held-fail path under move; 4/16 vs 16/16 false relinquishments under cut), and its
  open-blind latch buys a cut-safety edge this world's economics do not price.
- **NOT established:** that retained state is *useless*. A result that attains the most
  positive configuration the test can express cannot license a statement of absence. The
  honest claim is **"no demonstrated significant income advantage in this one task at
  this resolution"** — an F1, not an F2, and not an equivalence.
- **Withdrawn:** "the storage line is closed at this scale" and "retained history beats
  tuned memoryless on no graded income endpoint" over-reach the measured F1. A decision to
  stop allocating effort to the storage line is a *resource decision*, not a scientific
  demonstration of absence. The correct terminal statement is: the storage question is
  **suspended at the resolution floor of the tested world**, not closed.
- **Withdrawn, a fortiori:** "maintenance not graded-useful" (the phrase used in the
  M0/S0 handoff line and in downstream synthesis docs). Ongoing-repair dependence was
  **deliberately not tested** here (C2 §5; AC110's question). A study that does not run a
  repair contrast cannot grade maintenance's usefulness — absence of a test is not a null
  result. Say "ongoing repair: NOT tested", not "maintenance not useful".

---

## 2. Endpoints reported separately (from the frozen rows, n=16 individuals per arm×cause)

| endpoint | counter | tuned | estimate | no_write | scramble |
|---|---|---|---|---|---|
| income_post (move), mean / sum | 18,620 / 297,920 | 18,568 / 297,088 | 18,756 / 300,096 | 13,908 / 222,528 | 16,232 / 259,712 |
| income_post (cut), mean / sum | 18,628 / 298,048 | 18,580 / 297,280 | 18,724 / 299,584 | 18,552 / 296,832 | 18,568 / 297,088 |
| move latency (ticks past 8192), mean | 21.75 (16/16) | 19.00 (16/16) | 30.375 (16/16) | 23.71 (14/16) | 23.71 (14/16) |
| cut false-relinquish (≥1 drop) | 4/16 | 16/16 | 0/16 | 0/16 | 0/16 |
| survival (move / cut) | 16/16 · 16/16 | 16/16 · 16/16 | 16/16 · 16/16 | **12/16** · 16/16 | **14/16** · 16/16 |
| counter (acquisition/write) writes, mean | 36.9 (move) / 63.2 (cut) | 0 | 0 | 0 | 14.1 (move) / 21.2 (cut) |
| ongoing repair dependence | NOT tested | NOT tested | AC110's question | NOT tested | NOT tested |

- **Directional income differences** are the G4 table above: 5 positive, 3 zero, 0
  negative; the direction is uniform. Do not fold the separate endpoints into one
  composite sentence.
- **Response latency**: the counter is *slower* to drop than the tuned rival under move
  (21.75 vs 19.00 ticks) — the latch's cost. The counter's edge is not speed.
- **False relinquishment** (cut): counter 4/16 vs tuned 16/16 — the real decision-quality
  edge, income-invisible (AC113 rule 1: a false drop re-binds the entry, `life=64`
  refreshes).
- **Survival**: counter and tuned both survive 16/16; `no_write` and `scramble` both lose
  individuals under move (deaths below) — a write-machinery schedule effect, reported as a
  lower bound, not gated.
- **Acquisition/write expenditure**: the counter pays ~37/63 writes vs 0 for the tuned
  rival; see §3 for why the `scramble` write count is lower than the honest counter's.
- **Ongoing repair: NOT tested** — stated, not graded.

Move-condition deaths (reported, not gated; the AC109 "write shifts the contact schedule"
effect acting on survival):

| arm | dying seed | death ticks (h0/h1) |
|---|---|---|
| no_write | 6603 | 8442 / 8442 |
| no_write | 6604 | 8540 / 8540 |
| scramble | 6603 | 8444 / 8444 |

---

## 3. Control-implementation audit: `scramble` is not a clean readout-only intervention

The `scramble` arm sets `CounterAlloc.scramble=True`, which forces the counter **read** to
0 in `_n(o)` (ac116.py:143-146):

```python
def _n(self, o):
    if self.scramble:
        return 0
    return counter_read(o, self.n_offs)
```

**(1) Every use of the scrambled read.** `_n(o)` is the only read path, and it is consumed
in two places in `CounterAlloc.outcome`:
- the productive-occluded branch: `self._write(o, e, max(self._n(o) + self.w, 0))` — with
  `_n=0` and `w=-6` this always writes `0`;
- the occluded-unproductive branch: `self._write(o, e, min(self._n(o) + 1, 7))` — with
  `_n=0` this always writes `1`, and the threshold test `if self._n(o) >= self.n_thr` is
  always `0 >= 4` = False, so the threshold-drop **can never fire**.

**(2) Forcing the read to 0 changes the writes, not only the decision.** The write target
is computed *from the read*: `min(_n+1, 7)` and `max(_n+w, 0)`. With the read pinned to 0
the counter bits can only ever be written to 1 (unproductive) or 0 (productive), so the
counter **never accumulates beyond 1** — the honest arm writes the full ramp
1→2→3→4→(drop). Two direct consequences, both visible in the frozen rows:
- **Expenditure changes**: the honest counter's counter_writes are ~36.9 (move) / ~63.2
  (cut); the scramble arm's are ~14.1 (move) / ~21.2 (cut) — the scramble arm does *less*
  counter writing because it repeatedly writes 1 to bits already 1. So the intervention
  reduces the write cost it was meant to hold constant.
- **The drop mode changes**: the honest counter drops via `drop_threshold` in 12/16 (move)
  and 12/16 (cut, the false-relinquishments) and via the decisive open path in 4/16; the
  scramble arm drops **only** via `drop_decisive` (14/16 move, 0 under cut). G3's contrast
  (counter vs scramble) is still a *valid* demonstration that the accumulated content
  drives the decision — but it is not a pure read-content contrast, because the scramble
  arm also loses the internal accumulation ramp and its write cost.

**(3) Whole-mechanism vs readout-only.** `scramble` is therefore a selective intervention
on the *read*, but because the read feeds the write target, it contaminates the internal
update as well. It sits between the two clean cuts: `no_write` (write disabled, read
honest — the acquisition cut) and a true readout-only control (below). It is correctly
labelled a *causal-role* control, not a *readout-only* control.

**(4) The clean readout-only intervention (for future work).** Force the *decision* to
see zero while the *update* uses the true accumulated value — split the single read into
two: an internal value `v = counter_read(o, n_offs)` used for the write target
(`min(v+1,7)` / `max(v+w,0)`), and a decision value `d = 0 if scramble else v` used only in
the threshold test and the drop. Then the internal counter follows the identical
accumulation trajectory as the honest arm and spends the same write budget **up to the
first decision point**; after that the honest arm drops and the scrambled arm continues
accumulating, and their expenditures legitimately diverge. Do **not** demand identical
long-term expenditure across the two arms — divergence *after* the decision is the
mechanism working, not a control failure. The matched-state requirement applies only up to
the first behavioural divergence.

(For the record, the frozen `scramble` rows cannot be reinterpreted as this clean control;
they stand as the causal-role control they are. The clean readout-only control is a new
diagnostic implementation to build if a future study needs it — it is not a replacement
for the frozen AC116 arm, and no confirmatory storage cohort is being launched.)

---

## 4. Productive-occlusion audit (the ε=0 task)

**When is a productive occluded observation decisive?** In the pure ε=0 world a contact is
`productive` iff the bound entry's stored port matched the current mapping (`e['in_m'] +
e['in_f'] > 0`). Under `move` the route-1 entry is stale, so a held contact **never**
matches and never yields: a productive *occluded* (bound, used=2) contact is **impossible
under move** in ε=0. Under `cut` (and `no_cause`) the entry is valid, so a productive
occluded contact *can* occur — and it is decisive evidence that the entry is valid (C).
Consequence: the counter's productive-occluded branch is **only ever exercised in the
cut/no_cause world, never under move**, so it can never dilute the move decision.

**Do the episode assumptions remain valid after the action / re-acquisition?** Yes. A
productive contact calls `_restore` (which re-binds/keeps the entry and refreshes its
`life`), and the episode continues with the entry intact. The reset-to-0 write is the
"re-bound: episode over" bookkeeping the design names, and it is consistent: a productive
contact confirms the entry is valid, so accumulated weak-M evidence is stale.

**Does the candidate discard usable information?** Two findings.
- *In ε=0, no — the reset is correct.* `w = -6` saturates the 3-bit counter (`max(n+w, 0)`
  maps n≤6→0 and n=7→1), so one productive occluded contact erases the whole weak-M count.
  This is lossless only because productive is decisive C here: under ε=0 there is no
  residual yield, so a productive contact cannot occur on a stale entry, and discarding the
  M count on a confirmed-valid entry is the sufficient-statistic behaviour, not an
  information loss.
- *The w=-6 saturation is a hard reset, not a graded weight, and would discard usable
  information under residual yield (ε>0).* If a stale entry could yield with probability
  ε (the AC112/AC113 world), a productive occluded contact would be weak evidence for C,
  not decisive, and clamping to 0 would throw away accumulated M evidence the counter
  should keep. The pure ε=0 world is the one place the hard reset is provably safe. If a
  future study moves to ε>0, the productive weight must become a graded decrement, not a
  clamp-to-zero.

---

## 5. Downstream documents carrying the withdrawn wording

The following files repeat "storage line closes/closed at the organism scale" and/or
"maintenance not graded-useful", which this errata withdraws. They are reporting/synthesis
docs, none in AC116's hash set (only `AC116_PROTOCOL_v1.md` + the runner + frozen deps
are), so correcting them is a reporting errata, not a frozen-source edit. Reconciling them
is W0's downstream work (this card unblocks M4 and W0); listed here so the correction
propagates:

- `AC116_RESULTS_v1.md` (frozen and NOT edited in place — this errata is the sole
  correction; its §Verdict/§What-this-establishes/§Scope wording is superseded by §1
  above);
- `EVIDENCE_INDEX_v3.md` (lines 43, 66, 134, 321, 351, 390, 431);
- `AUTONOMY_RESEARCH_STATUS.md` (lines 72, 228);
- `S0_SYNTHESIS_v3.md` (lines 36, 42, 183);
- `P1_MANUSCRIPT_DRAFT_v1.md` (line 571);
- `CONSCIOUSNESS_ROADMAP_v1.md` (lines 315, 345);
- `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md` (line 18);
- `M0_BASELINE_EVIDENCE_INDEX_v1.md` (line 114 already flags the over-reach; line 25's
  "maintenance not graded-useful" should read "ongoing repair not tested").

---

## Sources

`ac116_results_v1/rows.jsonl` (240 rows), `ac116_results_v1/results.json`,
`audit_ac116.py` (G4 recomputation reproduced: p = 0.0625), `ac116.py` (§3 code
trace), `ac112.py` (`counter_read`/`counter_write`), `ac99.py`/`ac99_d2.py` (`_restore`,
`_drop_no_streak`). No frozen artifact touched; no study re-run; no new cohort.
