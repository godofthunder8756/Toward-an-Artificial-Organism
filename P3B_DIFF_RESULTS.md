# P3b results: differentiation of the body-grounded self-state (Layer 3 → Layer 4)

- **Protocol:** [P3B_DIFF_PROTOCOL.md](P3B_DIFF_PROTOCOL.md), frozen at
  commit 195bd64 before any final seed was run.
- **Run:** [`p3b_diff/`](p3b_diff/) (`raw.json`, `scores.json`,
  `REPORT.md`, `run.log`, weights for every arm at 1800 and 3600), seeds
  2400–2427, run 2026-11-22 17:54–21:55 UTC.
- **Post-hoc descriptives:** `p3b_diff/posthoc/` (disclosed; not
  confirmatory).
- Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**Overall: UNDETERMINED.** The pre-registered precondition that failed is
the perception referent (C_high, PFATE vs PYOKED: 18/27, p 0.12).

**Pre-registered partial reading: A_SIDE_SPECIFIC, NO_SPREAD.**

- **A_SIDE_SPECIFIC:** the self-state learned through memory precarity
  responds to the side of the body that threatens memory, not the other
  side.
- **NO_SPREAD:** it does not spread to the perception decision as P3's
  mood did. The cross-side cell is **reversed**: when the body looks low,
  the fated agent abstains *less* on C than the yoked rival (7/27 ahead,
  p 0.019).

Everything below is at the primary point (3600 updates), on the 27 usable
seeds (seed 2401 excluded; §6).

| Step | Test | Result | Label |
| --- | --- | --- | --- |
| Validity | phase-1 clear correct A / C; overwrite-probe accuracy A; exposure A / C | 0.988 / 0.999; 0.522; 0.029 / 0.054 | valid |
| Gate | yoked evidence effects positive; retention ≥ 0.6 | A 27/27, C 27/27; retention ≥ 0.95 everywhere | PASS |
| Referent A | A_low, PFATE vs PYOKED | 25/27, 0.102 vs 0.000, p < 0.0001 | DERIVED_AHEAD |
| **Referent C** | C_high, PFATE vs PYOKED | 18/27, 0.005 vs 0.000, p 0.12 | **NO_DIFFERENCE_DETECTED** |
| P3B-1 | D in PFATE | 26/27, median 0.326, Holm p < 0.0001 | DIFFERENTIATED |
| P3B-2 | D, PFATE vs PYOKED | 26/27, 0.326 vs 0.000, Holm p < 0.0001 | DERIVED_AHEAD |
| P3B-A | A half (A_low − A_high) in PFATE | 25/27, median 0.109, Holm p < 0.0001 | PRESENT |
| P3B-C | C half (C_high − C_low) in PFATE | 22/27, median 0.038, Holm p 0.0015 | PRESENT |
| Selectivity | median S in PFATE | 1.379 (needed ≥ 0.5) | — |

**Not the result:** the four primary tests and the selectivity all reach
their DIFFERENTIATED thresholds. Had the perception referent formed, the
label would have been DIFFERENTIATED. It did not form, so by the frozen
rules **the label is UNDETERMINED**. §2 shows what carries the C half
instead.

**At 1800** the pattern is the same but weaker. The memory referent holds
(25/27). The perception referent does not form (18/27). P3B-C is not
detected (19/27, p 0.052): the C half grows between 1800 and 3600.

**Sensitivity on all 28 seeds** (posthoc §2), without the usability rule:

- every label is unchanged (referent A ahead, referent C not detected,
  P3B-1, P3B-2, P3B-A and P3B-C passing);
- C_low is reversed against the yoked rival;
- S is 1.311.

## 2. The four cells: two decisions read one body variable with opposite signs

The four cells are each a change in abstention on clear, probed trials
against unprobed ones: the decision (A or C) under a reading that looks
low or high. PFATE medians at 3600:

| | look low | look high |
| --- | --- | --- |
| **A** (memory; at risk when the body is low) | **+0.102** (25/27 > 0) | −0.007 (22/27 < 0) |
| **C** (perception; at risk when the body is high) | **−0.031** (21/27 < 0) | +0.005 (19/27 > 0) |

The yoked and no-fate rivals are about 0.000 in every cell.

**Against the rivals** (pre-registered secondary tests, §5 of the
protocol):

- **Both cross-side cells are reversed against the yoked rival.**
  - A_high: 3/27 ahead, p < 0.0001.
  - C_low: 7/27, p 0.019.
- **The global component G is negative.** PFATE vs PYOKED is 2/27
  (−0.029 vs 0.000); vs PNOFATE it is 1/27. There is no residual global
  tone.
- **The perception cell does beat the rival that never had a fate.**
  C_high vs PNOFATE is 20/27 (p 0.019), but it does not beat the yoked
  rival.
- **D is specific to the fated arm.** It is detected in PFATE only (26/27).
  PYOKED has 14/27 and PNOFATE 15/27, both with median 0.000.

**What carries the C half** (post-hoc decomposition, posthoc §3–§4):

- **About 85% of the C half comes from −C_low,** a release of caution
  when the body looks low, not from extra caution when it looks high.
- **The fated agent abstains more on clear C trials at baseline.** Its
  median is 0.037, against 0.003 for the yoked rival. In about 10 of 27
  seeds the baseline is large, from 0.08 to 0.72.
- **Looking low removes a median 76% of that baseline.**
- **In the seeds where C is body-graded, both directions agree.** C_high
  and −C_low correlate across seeds (Spearman 0.87). Seeds 2416 and 2427
  show the full two-sided form: C_high +0.62 / +0.50 and C_low −0.71 /
  −0.63.
- **So the C decision did learn a body-graded self-state with the
  correct sign** for its own risk: caution about perception that the body
  can switch off.
- **It mostly takes the form "body low, perception safe".** It rarely
  takes the form "body high, perception unsafe", which is what the
  pre-registered referent asked for.

**A's half is the mirror image, but carried by the other cell.**
About 94% of it is A_low ("body low, memory unsafe"). A_high is a small
release (−0.007), bounded by A's low baseline abstention (0.020).

**The two readouts are independent across seeds.**

| Pair | Spearman |
| --- | --- |
| A_low vs −C_low | −0.02 |
| A_low vs C_high | 0.14 |

So the readouts do not look like two expressions of one shared factor, as
P3's would. P3's worse effects correlated across the three decisions at
0.19–0.34.

## 3. Natural running, regulation and monitoring

**Natural discrimination** (abstaining more on trials whose reliability
is actually low):

| Decision | PFATE vs PYOKED | p | Label |
| --- | --- | --- | --- |
| A | 20/27 (0.218 vs 0.185) | 0.019 | ahead |
| C | 16/27 (0.126 vs 0.100) | 0.44 | not detected |

The memory self-state is used in natural running. The perception one is
not detectably so.

**Regulation:** time in band, PFATE vs each rival.

| Rival | Score | PFATE vs rival |
| --- | --- | --- |
| PYOKED | 25/27 | 0.945 vs 0.882 |
| PNOFATE | 25/27 | 0.945 vs 0.899 |

This replicates P1c, P1d and P3.

**Monitoring:**

- The noise route on A is present in every arm (27/27 each, about 0.25),
  as in P1c.
- Retention of clear-trial accuracy under the fate is 0.95 (A) and 0.96
  (C), against 0.995 or more in the rivals.

## 4. Against the expectations (protocol §7)

| Outcome | Expected | Observed |
| --- | --- | --- |
| Valid | 0.85 | yes |
| ≥ 14 usable seeds | 0.95 | yes (27) |
| Gate passes | 0.90 | yes |
| Memory referent DERIVED_AHEAD | 0.85 | yes (25/27) |
| Perception referent DERIVED_AHEAD | 0.40 | **no** (18/27) |
| UNDETERMINED | 0.57 (central) | **yes** |
| If so, A_SIDE_SPECIFIC | 0.65 | yes |
| If so, MOOD_SPREAD | 0.50 | **no**, and the cross-side cell is reversed (not anticipated) |
| In-band PFATE > PYOKED | 0.85 | yes (25/27) |

**The central expectation held:** UNDETERMINED through the perception
referent, with A_SIDE_SPECIFIC.

**What was not anticipated:** the cross-side cells are not merely free of
spread but negative. Each decision's body readout carries the sign of its
own risk on both sides. I had put even odds on P3's mood spreading. The
protocol §7 note ("a body-driven abstention on C is a mistake whenever the
body is low") named the pressure against spread. It did not predict an
opposite-sign readout.

## 5. Readings against protocol §6

- **Formally:** UNDETERMINED. The design did not get far enough to ask
  the full question by its own rules.
- **Descriptively** (not a label; disclosed as an interpretation):
  - The pattern is closest to protocol §6's row "DIFFERENTIATED, G not
    ahead": content-specific self-states and no global tone.
  - The perception side has an unexpected form: a release on the safe side
    rather than caution on the risky side.
- **The UNDIFFERENTIATED row is not supported.** That row reads "the P3
  mood is the attractor", but G is behind both rivals and the
  cross-side cells are reversed.
- **Not established:**
  - A **confirmatory** claim of differentiation needs a new run, with the
    perception referent defined in a way that admits this form (§8).
  - A **causal** claim needs steering, which P3b did not test.

## 6. Disclosures

- **Calibration:** four rounds on seeds 10100–10115, one redesign after
  round 2, and the perception corruption rebased on the trial mean after
  round 3 (protocol §3).
  - The calibration summaries were blind to every cross-side cell, the
    index and the selectivity.
  - All 16 calibration seeds were used, and none overlaps the final seeds.
- **Exclusion:** seed 2401 collapsed on A in phase 1 (clear correct
  0.001, unclear-minus-clear abstention 0.001). C was learned (0.999).
  - The usability rule is pre-treatment and arm-blind.
  - Sensitivity on all 28 seeds agrees (§1).
- **Running:**
  - The final run was 7 invocations of 4 seeds each, because of the 2 h
    limit on background tasks. Each invocation resumed from the committed
    partial records ("resuming" lines in `run.log`).
  - No container restart, no failed batch, no error in the log.
  - Seeds are deterministic.
- **Verification:**
  - The SHA-256 of all 21 source files recorded in `scores.json` equals
    the files at the freeze commit 195bd64 and the files now.
  - `python run_p3b_diff.py --score p3b_diff` reproduces `REPORT.md`
    exactly (apart from the trailing newline `print` adds), and `score()`
    on `raw.json` equals `scores.json`.
- **Post-hoc (`p3b_diff/posthoc/describe.py`, reads `raw.json` only):**
  - the per-seed cells;
  - the baseline abstention;
  - the decomposition of both halves;
  - the cross-seed correlations;
  - the all-28-seed sensitivity.

  None of these is a pre-registered test. The C_low and A_high comparisons
  quoted in §2 are pre-registered secondary tests.

## 7. Limits

- As in the protocol §9:
  - one small GRU (35,293 parameters);
  - one world;
  - a given drive;
  - the probes change the shown reading only.
- **Each decision was trained under its own risk**, so differentiation is
  the task-optimal organization. P3b shows that the agent reaches it, or
  part of it. It does not show that differentiation arises without its own
  training signal. The contrast with P3's mood is confounded by that
  training: P3's B and C never learned under the fate.
- **The two precarities differ in kind** (own recurrent state vs evidence
  received) as well as in side.
- **The C self-state is uneven across seeds.** It is large in about 10 of
  27 and near zero in the rest. Its natural use is not detected.
- **Its dominant form** (release when the body looks low) leans on an
  elevated baseline caution, so part of the C half may reflect a general
  wariness about C that the body switches off. That is still body-graded
  and correctly signed, but it is not the "high body, unsafe perception"
  referent the protocol asked for.
- **No steering:** Q-CAUSE is untested.
- **"Self-state"** means a functional abstention pattern. Nothing about
  awareness or experience follows. Layer 6 is not addressed.

## 8. What it means for the program (in layer terms)

**L3 → L4: the global mood is not an attractor. Under different risks to
different processing, the agent reads its body differently per decision.**

1. **The memory self-referent replicates** (L0 → L4, after P1d and P3).
   - Under precarity of its own recurrent state at every step, the agent
     learns to abstain when its body looks low: 25/27, about 0 in both
     rivals.
   - It is side-specific: it does not fire when the body looks high.
   - It is used in natural running (A discrimination 20/27).
2. **No mood spread; the opposite.**
   - In P3 a state learned through one decision spread to every decision
     ("cautious everywhere when the body looks bad").
   - Here the perception decision, trained under its own risk on the other
     side, reads the low body as *safe* for it and abstains less.
   - The global component is behind both rivals.
   - The same interoceptive variable is read with opposite signs by two
     decisions, and the two readouts are independent across seeds.
   - **This is the first sign in the program of a self-state whose content
     depends on which processing is concerned,** rather than one valence
     broadcast everywhere.
3. **But it is not yet a confirmed differentiated self-model.**
   - The pre-registered perception referent ("body high, perception
     unsafe") did not form. The C side mostly takes the safe-side form.
   - Its natural use is not detected.
   - The label is UNDETERMINED.
4. **A design finding (calibration, descriptive).**
   - Precarity of the agent's own computation, acting at every step, yields
     a body referent reliably.
   - Precarity confined to task windows did not.
   - Damage to the evidence received gave a weaker, uneven one.
   - The substrate-level, everywhere-and-always character of the risk seems
     to be what the building block needs. In this sense the risk resembles
     metabolism more than a task hazard.
5. **L1 replicates** (25/27 vs both rivals).

**The program now has:**

| Layer | Building block | Where |
| --- | --- | --- |
| L0 | a precarious substrate | P1c, P3b |
| L1 | regulation recruited by that precarity | P1c, P1d, P3, P3b |
| L4 | a learned, two-sided, causal self-referent to the body | P1d; side-specific again in P3b |
| L3 | that self-referent becoming a global state | P3, when other decisions have no risk of their own |
| L3 → L4 | the global state giving way to per-decision readouts with opposite signs | P3b, descriptive; formally UNDETERMINED |

**Next step (for the PI; not authorized by this card).** I recommend
**P3c: confirm and test the cause of the differentiated readout.**

Confirmation on new seeds (2600–2627) with the frozen P3b code, unchanged.
The only change is a new, additive scorer whose pre-registered referent for
C is the C half (or C_low reversed against the yoked rival), the form the
data showed.

Add a cross-steering test, using P3's steering machinery:

- estimate a hidden-state direction for A's body readout and one for C's;
- check whether they are distinct (cosine, against random directions);
- check whether each moves only its own decision.

Distinct, decision-specific causal directions would be the Layer 4
signature: a self-model with content, not only a pattern of abstention.

About 4 h of compute; the steering adds a little.

**Alternatives:**

- **Differentiation without its own training signal:** train C with no
  risk of its own, but give A two separate body-linked risks (low and
  high) with two different consequences, and ask whether the content
  separates inside A.
- **Q-NECESSITY:** remove A's or C's readout and measure what each loses.
- **The perturbation-sensitivity finding** of P3, as its own test.
- **L5:** a lifetime change of band.

> **Forward note (2026-11-23).** The recommended study was run as P3c. See
> [P3C_STEER_RESULTS.md](P3C_STEER_RESULTS.md). Label: **CONFIRMED_CAUSAL**,
> structure **ONE_DIRECTION_TWO_READOUTS**. The opposite-sign readout
> replicates on new seeds (P3b's own rules give DIFFERENTIATED there), and
> steering along the body direction moves both decisions with their own
> signs; the C half is fragile post-hoc. The decision-specific directions
> proposed above were not found: u_A and u_C are one axis (cosine 0.99 in
> every arm), and the differentiation lies in the readouts.

## 9. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the
  perception corruption, the probes and the drive exist only inside the
  agent's world and network. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 10. Admission answers (short)

| # | Answer |
| --- | --- |
| Q-EXIST | Memory referent present in PFATE (A_low 25/27, median 0.102). Perception: the C half is present (22/27) but the pre-registered C referent is not detected (18/27) |
| Q-LEARN | Both are learned under the fate. PFATE beats a yoked rival with the same losses (A_low 25/27, D 26/27). C_high is not detected against the yoked rival |
| Q-CAUSE | Not tested (no steering) |
| Q-NECESSITY | Not tested |

## 11. Reproduce

```bash
python -m unittest test_p3b_diff
python run_p3b_diff.py --score p3b_diff                          # rescore the committed run
python run_p3b_diff.py --calib-summary p3b_diff_calibration/round4
python run_p3b_diff.py --mode final --out <new dir>              # about 4 h on 4 workers (7 batches of about 35 min)
python p3b_diff/posthoc/describe.py                              # post-hoc descriptives (reads raw.json)
```
