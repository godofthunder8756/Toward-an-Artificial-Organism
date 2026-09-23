# AC106 errata v1 — K1: the engineering negative was real, but nine downstream claims overreach the saved artifacts

2026-09-22. Non-frozen correction note (K1, task t_a26a6854), in the AC100/102/103/104/105
convention. No frozen artifact is touched: `ac106.py` is an engineering runner (never frozen),
`ac106_engineering_v1/{rows.jsonl, results.json}` are engineering output (no protocol, no
`pre_run_snapshot.json`, no final seeds), and none of `C3_DISPOSITION_v1.md`,
`X1_COUPLING_ASSESSMENT_v1.md`, or `S1_SYNTHESIS_v1.md` is hashed into any study snapshot. This
note records the corrections and supersedes the overgeneralized dispositions in those three
documents; it invents no positive finding.

Every number below was re-derived from `ac106_engineering_v1/rows.jsonl` (288 rows) and
`ac106_engineering_v1/results.json` directly, and every implementation claim was checked against
`ac106.py` source.

The valid negative is preserved unchanged (§3). The corrections are to **scope and wording**, not
to the measured result.

---

## 1. The nine overreach points, each verified against code and artifacts

### P1 — `HOLD_N == STREAK_N`; r4 did not implement the advertised longer-threshold comparison

`ac106.py` line 77 declares `HOLD_N = STREAK_N`, with the comment "the candidate's E_world
threshold IS the frozen streak threshold (the 3-bit Gray streak saturates at 7, so any larger
threshold is unreachable)". r4 is built as `BeliefAlloc(estimate=False, threshold=HOLD_N,
proactive=False)` (line 320), i.e. the **same** threshold as r2's streak, minus the estimate and
minus proactive renewal.

The docstring (lines 36-37) and `AC106_ENGINEERING_v1.md` §1 nonetheless advertise r4 as "a
longer-threshold counter … the sharpest falsification, a raw counter with a **bigger** threshold".
That arm was never implemented. r4 is behaviourally identical to r2 in every condition
(`rows.jsonl`: r4's relinquishment count equals r2's on all 16 cut individuals — 0 on seeds
0/1/2/6, 1 on 3/5/7, 2 on 4). The "sharpest falsification" comparison (an estimate's hold vs a raw
counter with a genuinely longer threshold) does not exist in the data.

**Correction:** r4 is a *no-estimate duplicate of r2 at the same streak threshold*, not a
longer-threshold counter. The C1 §7 sharpest-falsification was not run; the G6 gate as named
("proactive renewal beats the longer counter") was testing the wrong thing, and its failure is a
consequence of r4 == r2, not of any measured comparison.

### P2 — the estimator did not distinguish re-acquisition from resumed access; that is a defect, not a proof of no representation

The update rule (`BeliefAlloc.outcome`, lines 203-216) fires `_bel_write(0)` (→ E_machinery) on
**any** productive contact-1 that follows a failure (`if cur > 0 and self.now >= DEV`), with no
check of whether the entry was still bound. A dropped-and-blind-rebound stale route (the frozen
`grow=True` + erase-on-relinquishment path) emits exactly that productive-after-failure signature,
so the re-bind is mislabelled as "productivity resumed without re-binding".

This is an **implementation defect in the update rule** (the C1 §4 re-bind-and-compare probe — gate
the E_machinery conclusion on `selected is None` vs `selected is not None` — was not implemented).
It is **not** evidence that the organism cannot represent the E_world/E_machinery distinction, nor
that the distinction is unrepresentable in this architecture. `AC106_ENGINEERING_v1.md` §5 already
names this as "R1 fix (information)" and says "it was not implemented and its absence is what R1
measures"; the downstream documents then dropped that scoping and wrote "the estimate carries no
cause information" as if it were a property of the organism.

**Correction:** state it as "the estimate *as implemented* carries no discriminating cause
information, because its update rule is confounded by the re-acquisition path"; never as "the
organism cannot represent the cause." The representation question is untested.

### P3 — identical terminal labels do not establish zero cause information throughout the trajectory

The "carries no cause information" claim rests on `bel_at_horizon` alone (gate G1 reads only the
horizon). That is the wrong read of the trajectory, in two ways:

1. **It is numerically wrong as stated.** In `move`, the estimate does **not** read E_machinery in
   all 16 individuals: it reads E_world (correct) in 6/16 (seeds 4, 5, 6) and E_machinery (wrong)
   in 10/16 (seeds 0, 1, 2, 3, 7). In `cut` it reads E_machinery (correct) in 16/16. The report's
   §2 table and §3 R1 ("reads E_machinery at the horizon in **both** causes") and `test_ac106.py`'s
   docstring overstate this to 16/16.
2. **The horizon is the wrong time to read it.** At the relinquishment *decision* (the `_drop`,
   which writes `reset_world` → e=E_world), the estimate is E_world in **all 16** move individuals
   (`bel_events`); the E_machinery mislabel on seeds 0/1/2/3/7 is a *post-decision* drift caused by
   the re-bind confound (P2), applied after the drop has already happened. The estimate reads the
   cause correctly when the decision is made and only later drifts.

**Correction:** report discrimination at decision times (`drop_ticks`, `restore_ticks`,
`bel_events`), not only `bel_at_horizon`. The accurate statement is "the estimate reads the cause
correctly at decision time in 16/16 move and 16/16 cut individuals, and is confounded only at the
horizon in 10/16 move individuals by the re-acquisition path."

### P4 — changes in route holding and relinquishment ARE behavioural effects

In `cut`, the candidate holds route-1 without relinquishing in 14/16 individuals (0
relinquishments on seeds 0/1/2/3/5/6/7), while r2 relinquishes and re-acquires in 8/16 (1-2
relinquishments on seeds 3/5/7, plus the seed-4 death). The terminal `route1_bound_at_horizon`
label is *identical* for both (True on 14/16, the same 14), so the difference lives entirely in the
mid-trajectory relinquishment count — the candidate holds through the cut, r2 drops and re-binds.

`X1_COUPLING_ASSESSMENT_v1.md` §6 dismisses this as "not even a clean advantage … a confounded,
non-load-bearing artefact." That dismissal is itself an overreach: a 14/16 vs 8/16 difference in
whether the organism relinquishes a valid entry mid-outage **is** a behavioural effect, regardless
of whether it changes survival. The honest sentence is "a real, seed-dependent behavioural
difference in holding/relinquishment with no demonstrated survival consequence", not "nothing".

### P5 — the scramble arm overrides reads AND suppresses writes; it is not a selective, expenditure-matched ablation

`BeliefAlloc` with `scramble=True` differs from the candidate in **three** ways, not one:
`_bel` returns 1 unconditionally (the read is forced to E_world, lines 172-174); `_bel_write`
returns 0 unconditionally (the estimate's paid writes are suppressed, lines 176-179); and
proactive renewal is gated on `self._bel(o) == 0` (lines 213, 226), so with the read forced to
E_world it **never fires** — the scramble arm also suppresses the proactive-renewal spend.

The docstring (line 38) and `X1_COUPLING_ASSESSMENT_v1.md` §3 describe scramble as "the candidate
with the estimate forced to E_world (the causal-role control, P4)". That is not what the arm does:
it forces the read, removes the estimate's maintenance spend, and removes the proactive spend.
It is **not** a selective causal-role control, and it is **not** expenditure-matched (it spends
less, so any behavioural identity is partly a spend confound, not a read-only demonstration).

**Correction:** state the confound explicitly. A read-only scramble (read forced E_world, writes
and proactive renewal left intact) was not run; the G5 gate as written cannot separate "the read is
causally irrelevant" from "the read is irrelevant because its two consumptions were also removed."

### P6 — AC106 is an engineering negative, not a confirmatory rejection

`AC106_ENGINEERING_v1.md` §0 already says "Engineering report, not a study. No protocol, no final
seeds, no freeze." There is no `AC106_PROTOCOL_v1.md`, no `pre_run_snapshot.json`, no disjoint
final seed family, no audit/replay split. The downstream documents nonetheless use rejective
language: `S1_SYNTHESIS_v1.md`'s verdict ("level-(d) … is **FALSIFIED** on measured, structural
grounds"), `X1_COUPLING_ASSESSMENT_v1.md` ("**NEGATIVE (the card's falsification)**"),
`C3_DISPOSITION_v1.md` ("CLOSED").

**Correction:** report it as "**falsified in engineering** — a strong candidate-negative on 16
individuals with no frozen confirmatory protocol and no untouched final cohort." That is exactly
one step weaker than "confirmatorily rejected", and the difference is what the level-(d) disposition
must carry. A confirmatory rejection requires a hashed protocol run on disjoint finals; that was
never done.

### P7 — unchanged survival does not establish absent maintenance dependence

`X1_COUPLING_ASSESSMENT_v1.md` §3-§4 concludes "maintenance dependence — none" and "cutting or
scrambling the estimate does not degrade the organism at all." What the data show is narrower:
survival is **arm-independent** (candidate, r2, r4, r1, scramble all die only on seed 4 `cut`; only
the crude duty rival r3 dies elsewhere — 30/288 rows die). That establishes the estimate is
**survival-irrelevant**. It does **not** establish that the estimate's function is not *maintained*
— the paid bank-0 repair and the estimate's own writes are still running; they simply do not move
survival. "No survival dependence" ≠ "no maintenance dependence."

**Correction:** replace "maintenance dependence — none" with "no survival dependence was observed;
maintenance of the estimate's *function* (as opposed to survival) was not separately isolated by
any arm, because the scramble arm also removed the maintenance spend it was meant to match (P5)."

### P8 — similar behaviour to an externally supported controller does not falsify internal integration

`X1_COUPLING_ASSESSMENT_v1.md` frames the card's falsification as "no difference from an externally
supported controller — the mechanism is not genuinely integrated" and treats it as met. But
behavioural similarity to an externally supported controller is **not** falsification of internal
integration: an internally integrated mechanism can produce the same observable behaviour as an
external one (that is the point of the C1/C2 byte-identity discipline — the acquired organism is
*meant* to be byte-identical to the frozen one where no cause is present). What the data actually
establish is that the estimate is **redundant** — it adds no causal role over the frozen first-order
machinery — which is a claim about the mechanism's *utility*, not about whether the organism
genuinely integrates its state (the observer-discard test, `observer_discard_equivalence`, passes:
the estimate lives in maintained state and survives host-state discard).

**Correction:** the falsification is "the estimate is redundant with the frozen first-order
machinery", not "the mechanism is not genuinely integrated." Integration and redundancy are
different questions; AC106 measured the second, not the first.

### P9 — a failed cause estimator does not falsify metacognition, consciousness-related mechanisms generally, or all cognition-maintenance coupling

The failure is of **one candidate mechanism** (the maintained one-bit cause estimate) under **one
operational definition** (the C1 two-cause task) in **one architecture configuration** (AC100-derived,
`corrupt=False` — no corruption challenge, no persistent-trigger reconstruction, no allowance-42;
see `BASELINE_v2.md` §3). `S1_SYNTHESIS_v1.md`'s one-line verdicts ("level-(d) … FALSIFIED",
"Maintained belief, metacognitive monitoring, reliability estimation — falsified") and `C3`'s
"does not distinguish the two causes at all" read as verdicts on the whole level. They are not: the
level-(b)/(c) representational machinery's maintenance *is* load-bearing (AC75/AC67/AC71/AC91/AC92),
and the C-track's own §2 scope split in `X1_COUPLING_ASSESSMENT_v1.md` already says exactly this.

**Correction:** scope every level-(d) sentence to "the maintained-belief cause-estimate candidate, as
implemented, in the AC100-derived configuration." A failed cause estimator does not falsify
metacognition, consciousness-related mechanisms generally, or all cognition-maintenance coupling.

---

## 2. Numerical and survival-reporting corrections

- **"e reads E_machinery in both causes" is wrong as stated.** In `move` the horizon estimate is
  E_machinery in 10/16 and E_world in 6/16 (seeds 4/5/6). Correct wherever it appears
  (`AC106_ENGINEERING_v1.md` §2 table + §3 R1, `test_ac106.py` docstring, `X1` §3/§5, `C3` §1,
  `S1` §2 C2 bullet).
- **The §2 "entry survives cut" column is mislabelled.** The candidate and r2 have the *same*
  terminal `route1_bound_at_horizon` (True on 14/16, both), so "r2 yes (8/16)" is not "entry
  survives" — it is "holds without relinquishing" (0 relinquishments). The two endpoints must not be
  conflated: the trajectory-level holding/relinquishment difference (P4) is real, and the
  terminal-route endpoint does not distinguish the arms at all.
- **Survival reporting is verified correct** (no correction needed, but recorded so the correction
  does not invent an error): 30/288 rows die; candidate/r2/r4/r1/scramble die only on seed 4 `cut`
  (2 rows each, tick 8443/8447); r3 dies 20 (6 cut on seeds 2/4/5, 8 move on 0/2/4/5, 6 no_cause on
  2/4/5). `X1` §4's re-derived arm-independent survival is accurate.
- **Gate state (verified from `results.json`):** G1 false, G2 false, G3 true, G4 true, G5 false, G6
  false, G7 null (engineering run). The candidate passed only the no-cause identity (G4) and the
  relinquish-in-E_world (G3, which is the frozen streak's own behaviour, not the estimate's).

---

## 3. What the data establish (the valid negative, preserved unchanged)

The candidate failed its intended discrimination role: it did not demonstrate that a maintained
cause-estimate adds a causal role over its matched rivals, and no arm showed a survival advantage
(survival is arm-independent). This is the card's falsification and it stands.

Strongest wording the engineering data earn: "**the maintained cause-estimate, as implemented, is
not causally load-bearing in the AC100-derived two-cause task — its update rule is confounded by
the re-acquisition path (so its horizon label carries no discriminating information in 10/16 move
individuals), its hold adds no survival consequence, and its proactive renewal spend is redundant
with the frozen reactive renewal.**" No stronger negative is earned (specifically: nothing here
falsifies representation of the cause, metacognition generally, or all cognition-maintenance
coupling).

## 4. What the implementation explains vs what remains untested

Explained by the implementation (not by the organism's capacity):

- R1/P2: the update rule confounds re-acquisition with resumed access (defect, not capacity).
- P1: r4 never implemented the longer threshold, so the sharpest falsification was not run.
- P5: the scramble arm is a three-way confound, so the causal-role control was not clean.

Remains untested:

- A maintained estimate with the C1 §4 update rule (gate E_machinery on `selected is None`), i.e.
  whether the organism *can* represent the distinction once the confound is removed.
- A first-order controller that errs uniformly, so the estimate has something real to fix (the
  frozen streak + reactive renewal already handle half the individuals).
- Cognitive integration in AC105's combined-challenge architecture (`corrupt=True`, persistent
  trigger, allowance-42) — AC106 ran `corrupt=False` and did not touch it.

---

## 5. Reopened / superseded dispositions

- **C3_DISPOSITION_v1.md** — superseded in part: the "carries NO cause information" / "does not
  distinguish the two causes at all" wording is scoped to the implemented, confounded update rule
  (P2/P3), and "CLOSED, not blocked" is re-read as "closed for the implemented mechanism, whose
  activation-condition failure is an implementation defect, not a measured absence of representable
  accuracy." C3's own re-open clause (fix C2's R1) is unchanged.
- **X1_COUPLING_ASSESSMENT_v1.md** — superseded in part: "maintenance dependence — none" → "no
  survival dependence observed" (P7); "no difference from an externally supported controller — not
  genuinely integrated" → "redundant with the frozen first-order machinery" (P8); the
  holding/relinquishment difference is a behavioural effect, not dismissed (P4); the scramble arm is
  a confound, not a clean causal-role control (P5).
- **S1_SYNTHESIS_v1.md** — superseded in part: "level-(d) FALSIFIED" → "the maintained-belief
  cause-estimate candidate falsified in engineering" (P6/P9); the "reads E_machinery in both causes"
  number is corrected to 10/16-in-move (P3); the level-(d)/metacognition/coupling negatives are
  scoped to the single candidate mechanism in the AC100-derived configuration (P9).

The valid negative (§3) is retained in all three documents; only the overgeneralized scope and the
mis-stated numbers are corrected. No positive finding is invented: nothing here claims the estimate
worked, carried information, or was load-bearing.

## 6. Verification

All counts re-derived from `ac106_engineering_v1/rows.jsonl` (288 rows) and `results.json`; all
implementation claims checked against `ac106.py` source lines cited above. `test_ac106.py` still
passes 12/12 (it pins the mechanism and the recorded negative; its docstring's "E_machinery in both
causes" is the one overstatement this note corrects, and the test itself — which only asserts
seed 0's horizon value — remains a valid recorded-outcome regression). No frozen artifact was
re-run, re-hashed, or edited; this note is not hashed into any snapshot.
