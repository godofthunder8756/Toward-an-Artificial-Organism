# P3 results: global availability of the body-grounded self-state (Layer 0 → Layer 3)

- **Protocol:** [P3_GLOBAL_PROTOCOL.md](P3_GLOBAL_PROTOCOL.md), frozen at
  commit 17ef9ca before any final seed was run.
- **Run:** [`p3_global/`](p3_global/) (`raw.json`, `scores.json`,
  `REPORT.md`, `run.log`, weights for every arm at 1800 and 3600).
- **Post-hoc descriptives:** `p3_global/posthoc/` (disclosed; not
  confirmatory).
- Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**Overall: GLOBAL_ROUTED** (primary point 3600; Holm over the three
tests; not weak). **Gating: UNGATED.** My central expectation at the freeze
was LOCAL (0.45). I gave GLOBAL_ROUTED 0.12 and UNGATED 0.60 conditional on
a global outcome.

- **Valid:**
  - phase-1 clear correct-report rate 0.987 / 0.987 / 0.999 for A / B / C
    (needed ≥ 0.8 each);
  - report accuracy under the overwrite probe 0.531 (A) and 0.537 (B)
    (needed ≤ 0.7);
  - PFATE clear A trials below break-even 0.046 (needed ≥ 0.02).
- **Usable seeds:** 19 of 28. The 9 excluded seeds are listed in the
  report; §5 says why.
- **Gate passes:** the yoked B evidence effect is positive in 19/19 seeds,
  and B retention is 0.98–1.00 in every arm.
- **The A referent formed:** 18/19 seeds (PFATE 0.088 vs PYOKED 0.001).

| Test at 3600 (19 usable seeds) | Seeds | PFATE | Rival | Holm p | Label |
| --- | --- | --- | --- | --- | --- |
| P3-1 B worse effect, PFATE vs PYOKED | 19/19 | 0.041 | 0.006 | < 0.0001 | DERIVED_AHEAD |
| P3-2 B worse effect, PFATE vs PNOFATE | 19/19 | 0.041 | 0.002 | < 0.0001 | DERIVED_AHEAD |
| P3-3 steering along A's worse direction, B trials, PFATE | 15/19 | 0.025 | — | 0.019 | CAUSAL |
| Transfer ratio (B effect / A effect in PFATE), median | — | 0.53 | needed ≥ 0.2 | — | — |
| *Secondary:* C worse effect, PFATE vs PYOKED | 18/19 | 0.043 | 0.005 | (0.0001, uncorrected) | DERIVED_AHEAD → UNGATED |

At 1800, P3-1 (16/19) and P3-2 (19/19) also pass, with a transfer ratio of
0.35. P3-3 is not detected there (11/19).

**In plain terms.** The at-risk agent learned, through its first decision
only, to abstain when its body looks out of band. That learning also
reached two decisions that were never trained while the body-linked damage
was on:

- B, a second memory decision for which the body warning is relevant;
- C, a decision the body cannot affect.

On both, the at-risk agent abstains more when its body looks bad, at about
half the strength of its first decision. The yoked rival with identical
losses, drive and rehearsal does not, and nor does the never-damaged rival.

## 2. The three consumers

Medians over the 19 usable seeds, 3600. Effects are abstention on
worse-probed minus unprobed clear trials.

| Arm | worse A (trained) | worse B (relevant, untrained) | worse C (irrelevant, untrained) | baseline clear abstention A / B / C |
| --- | --- | --- | --- | --- |
| PFATE | 0.088 | 0.041 | 0.043 | 0.008 / 0.013 / 0.014 |
| PYOKED | 0.001 | 0.006 | 0.005 | 0.001 / 0.009 / 0.011 |
| PNOFATE | 0.000 | 0.002 | 0.001 | 0.000 / 0.001 / 0.001 |

- **B and C receive the same amount.** B minus C in PFATE is 11/19, median
  0.006, not detected. The spread does not distinguish the decision the
  body warning could help (B) from the one it cannot (C).
- **Where in the trial** (post-hoc, by the noiseless cue-step reading):
  - In A, the effect is largest for bodies that were really low (0.283
    below the band, 0.131 in its lower half) and about zero in the upper
    half of the band.
  - B and C follow the same profile at about half the size (0.14 and 0.12
    below the band).
- **Consistency across seeds is weak** (post-hoc, Spearman over 19 seeds):
  A–B 0.34, A–C 0.19, B–C 0.24. Every seed shows some transfer, but how
  much does not track closely how strong a seed's A referent is.

## 3. Natural running, regulation and monitoring

- **Regulation (L0 → L1), replicated a third time.** With the same drive,
  PFATE keeps its body in band more than PYOKED (19/19; 0.945 vs 0.882) and
  than PNOFATE (19/19; vs 0.906).
- **B natural discrimination** (secondary): PFATE abstains on its
  low-reliability B trials more than PYOKED does (15/19; 0.166 vs 0.139). B
  was never trained under the damage, yet in natural running it uses the
  spread state where it is useful.
- **A natural discrimination:** 14/19 (0.211 vs 0.144), not detected
  (p 0.064). Lower than P1d's 26/28.
- **The cost of the ungated spread is small** (post-hoc). In natural
  running PFATE abstains on clear C trials 0.027 of the time, against 0.023
  (PYOKED) and 0.002 (PNOFATE).
- **Monitoring** (the overwrite probe) is equal across arms for A and B
  (about 0.25), as in P1c and P1d.

## 4. Steering: the routing label is fragile (post-hoc)

The pre-registered rule labels the outcome ROUTED because steering along
A's worse direction raises B abstention more than a random direction does
(15/19, Holm p 0.019). The post-hoc descriptive split weakens that reading.

| 3600, medians | A-direction effect | random-direction effect | net |
| --- | --- | --- | --- |
| PFATE, A trials | 0.060 | 0.052 | 0.000 (10/19) |
| PFATE, B trials | 0.066 | 0.041 | 0.025 (15/19) |
| PFATE, C trials | 0.052 | 0.056 | −0.002 (9/19) |
| PYOKED, A / B / C | 0.015 / 0.025 / 0.003 | 0.001 / 0.008 / 0.004 | — |
| PNOFATE, A / B / C | about 0 | about 0 | — |

- **PFATE abstains when its state is pushed in *any* direction** of that
  size (about 0.05 on every type). Its rivals barely respond.
- **A's own worse direction is no more effective than a random one on A
  trials,** nor on C trials. Only on B does it beat random. P1d's A steering
  was CAUSAL (21/28), so in P3 the direction-specific route did not
  replicate, even for the trained decision.
- So the robust finding is the **behavioural** availability (§1–2). The
  "routed" part rests on one test that its own decision (A) and its sibling
  (C) do not support. I read it as unestablished and do not build on it.
- The non-specific perturbation sensitivity is itself new and is PFATE's
  alone. Its report decision is fragile to any small displacement of its
  own state, while its rivals' decisions are not. It was not
  pre-registered.

## 5. Against the expectations (protocol §7)

| Outcome at 3600 | Expected | Observed | Hit |
| --- | --- | --- | --- |
| Valid | 0.90 | valid | yes |
| At least 14 usable seeds | 0.90 | 19 | yes |
| Gate passes | 0.85 | PASS | yes |
| P3-0 referent DERIVED_AHEAD | 0.85 | 18/19 | yes |
| P3-1 DERIVED_AHEAD | 0.40 | 19/19 | yes (against my lean) |
| P3-2 DERIVED_AHEAD | 0.40 | 19/19 | yes (against my lean) |
| P3-3 CAUSAL | 0.30 | 15/19 | yes (fragile, §4) |
| Overall LOCAL (central) | 0.45 | GLOBAL_ROUTED (0.12) | **no** |
| If global: GATED | 0.40 | UNGATED | no (as favoured) |
| C worse effect, PFATE ahead of PYOKED | 0.30 | 18/19 | **no** |
| In-band time, PFATE ahead of PYOKED | 0.85 | 19/19 | yes |
| In-band time, PFATE ahead of PNOFATE | 0.70 | 19/19 | yes |
| A natural discrimination, PFATE ahead | 0.70 | 14/19, not detected | **no** |

My central argument at the freeze was that a body-driven abstention would
be learned as a conjunction ("A probe and body bad") that leaves other
decisions alone. That argument was wrong. What small recurrent networks
found is a general state ("body looks bad, so report less") that reaches
every decision, including those it cannot help.

## 6. Disclosures

- **Frozen before any final seed.** All 20 source files in `raw.json`
  match the freeze. Rescoring (`python3 run_p3_global.py --score
  p3_global`) reproduces `REPORT.md` exactly and `scores.json` field for
  field.
- **Calibration** (protocol §3): three rounds on seeds 9980–9991. The
  calibration summaries never computed or printed a B or C probe or
  steering effect. Changes were: safe rehearsal; a longer phase 1; a
  phase-1 cost peak of 8; the usability rule; and the TRACE magnitude
  rule. All were made before any final seed.
- **Exclusions.** 9 of 28 seeds (32%) failed the pre-treatment usability
  rule, more than the 25% seen in round 3.
  - All nine collapsed during phase 1, before the arms split, into
    abstaining on every A trial, every B trial or both: 2223 on A only,
    2205 on B only, the other seven on both. C was learned in every seed.
  - The cost peak that made unclear abstention learnable also makes this
    collapse more likely. It is a known cost of the training choice.
  - **Sensitivity (post-hoc):** on all 28 seeds without the rule,
    P3-1 26/28, P3-2 25/28 and P3-3 22/28 all pass, with a transfer ratio
    of 0.43; C is 21/28. The conclusion does not depend on the exclusions.
- **One container restart** during batch 4. No finished seed was lost; the
  batch was rerun from its start (seeds are deterministic). Logged in
  `p3_global/run.log`. Seven batches of 4 seeds, each committed and pushed
  when it finished.
- **Post-hoc analyses** (§2 trial profile and correlations, §3 natural
  cost, §4 steering split, §6 sensitivity) are in
  `p3_global/posthoc/describe.py` and its log. They read `raw.json` only.
- Compute: about 17.9 CPU-hours (64,267 s summed over seeds), about 5 h
  wall time on 4 workers.

## 7. Limits

- As P1c and P1d: one small GRU (35,293 parameters), one kind of
  unhardenable damage, a given drive, one world, and probes that change the
  shown reading only.
- **The A referent is smaller than in P1d** (0.088 vs 0.242), probably
  because the safe rehearsal punishes body-driven abstention on A as well.
  The transfer ratio is relative to this smaller referent.
- **The absolute B and C effects are small** (about 0.04: four extra
  abstentions per hundred probed clear trials). They are very consistent
  (19/19), and 7–20 times the rivals' effects.
- **All three decisions read one 70-unit recurrent state.** Availability
  through a shared state is the architectural default, which is why the
  comparison is against rivals with the same architecture, losses and
  rehearsal. What differs is that only the fated agent's shared state
  carries the body warning.
- **The routing part of the label is fragile (§4).** The behavioural
  availability is not.
- **Not tested:** Q-NECESSITY, scale, other kinds of damage, other worlds,
  and workspace dynamics (ignition, capacity limits).
- **Nothing about awareness or experience follows.** Layer 6 is not
  addressed.

## 8. What it means for the program (in layer terms)

**The body-grounded self-state is globally available, and ungated.** This
is the first Layer 3 result of the program.

1. **L0 → L3 (pre-registered, established at the behavioural level).**
   - A self-state learned through one decision's precarity is used by
     decisions that never learned with it. It reaches them at about half
     its strength, in every usable seed.
   - Two rivals share the architecture, rehearsal and losses (one of them
     every loss), and neither shows it.
   - What carries the body warning is not a decision-specific rule but a
     state of the whole agent.
2. **It is undifferentiated.** The warning reaches the decision it could
   help (B) and the one it cannot (C) equally. Functionally it behaves
   less like a self-model of "my memory may fail" and more like a
   **global affective tone**: when the body looks bad, the agent becomes
   cautious everywhere. Two families of theory predict a distinction here:
   - global-workspace views: content is broadcast to every consumer;
   - homeostatic-affect views (feeling as a whole-organism state set by
     the body's condition).

   In this small system the body warning behaves like the second: a
   pervasive, valenced state rather than a piece of content routed where
   it is relevant.
3. **It is useful where it is relevant.** In natural running, B uses the
   spread state on its own low-reliability trials (15/19 ahead of the
   yoked rival). The cost on C is small (0.027 vs 0.023 abstention).
4. **L0 → L1 replicates** (19/19 against both rivals).
5. **A new, unplanned property.** The fated agent's decisions abstain when
   its own state is displaced in any direction. A self-monitoring
   sensitivity to perturbation of its own state, not only to its body, is
   unique to the arm whose computation is precarious. Post-hoc; it needs
   its own test.

**The program now has, in one small agent and its rivals:**

- **L0:** a precarious substrate (P1c);
- **L1:** regulation recruited by that precarity (P1c, P1d, P3);
- **L4:** a learned, two-sided, causal self-referent to the body (P1d);
- **L3:** that self-referent becoming a global state of the agent (P3).

The open question for consciousness-relevant organization is no longer
whether a body-grounded self-state can become global. It is whether it can
become *differentiated*: a global state that also carries content about
which processing is at risk.

**Next step (for the PI; not authorized by this card).** I recommend
**P3b: differentiation.**

- Keep everything in P3, but give B its own precarity: B's held value is
  overwritten with a probability set by a *second* body variable (or by a
  separate band of the same variable). C stays immune.
- Then ask whether the agent forms one undifferentiated state or two
  content-specific ones:
  - A abstains on body 1;
  - B on body 2;
  - C on neither.
- Rivals: yoked on each body.
- **The Layer 3/4 signature** would be selective broadcast, the step from a
  global mood to a self-model.

Alternatives:

- **Q-NECESSITY:** remove the spread (for example by training C to ignore
  the body) and measure what PFATE loses.
- **The perturbation-sensitivity finding** (§4) as its own pre-registered
  test.
- **L5:** a lifetime change of band.

## 9. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the probes,
  the rehearsal world and the drive exist only inside the agent's world and
  network. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 10. Admission answers (short)

| # | Answer |
| --- | --- |
| Q-EXIST | B worse effect present in PFATE 19/19 (median 0.041); C 19/19 (0.043) |
| Q-LEARN | B and C never learned under the fate. PFATE beats a yoked rival learning under the same losses and rehearsal (19/19) |
| Q-CAUSE | Pre-registered: CAUSAL (15/19; Holm p 0.019). Post-hoc: fragile, since A's own direction is no better than random on A (§4) |
| Q-NECESSITY | Not tested |

## 11. Reproduce

```bash
python -m unittest test_p3_global
python run_p3_global.py --score p3_global                       # rescore the committed run
python run_p3_global.py --calib-summary p3_global_calibration/round3
python run_p3_global.py --mode final --out <new dir>            # about 5 h on 4 workers (7 batches of about 40 min)
python p3_global/posthoc/describe.py                            # post-hoc descriptives (reads raw.json)
```
