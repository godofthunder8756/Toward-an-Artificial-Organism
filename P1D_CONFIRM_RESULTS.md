# P1d results: confirmation of the two-sided body referent (Layer 0 → Layer 4)

- **Protocol:** [P1D_CONFIRM_PROTOCOL.md](P1D_CONFIRM_PROTOCOL.md), frozen
  at commit d8d46cb before any final seed was run.
- **Run:** [`p1d_confirm/`](p1d_confirm/) (`raw.json`, `scores.json`,
  `REPORT.md`, `run.log`, weights for every arm at 1800 and 3600).
- **What it confirms:** the post-hoc finding of
  [P1C_SELFOVER_RESULTS.md](P1C_SELFOVER_RESULTS.md) §4, on 28 fresh seeds
  (2000–2027), with training identical to P1c and probes whose direction
  was fixed in advance.
- Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**Overall: CONFIRMED_ROUTED** (primary point 3600; Holm over the four
tests; not weak). **Natural discrimination (P1d-4): CONFIRMED.** This was
the central expectation written at the freeze (§6, probability 0.65 for
CONFIRMED or CONFIRMED_ROUTED).

- **Valid:**
  - phase-1 clear correct-report rate 0.999 (needed ≥ 0.8);
  - report accuracy under the overwrite probe 0.524 (needed ≤ 0.7);
  - PFATE clear trials below the report break-even 0.038 (needed ≥ 0.02).
- **Gate P1d-0 passes:** the yoked evidence effect is positive in 28/28
  seeds (needed 19).

| Test at 3600 | Seeds | PFATE | Rival | Holm p | Label |
| --- | --- | --- | --- | --- | --- |
| P1d-1 worse effect, PFATE vs PYOKED | 28/28 | 0.242 | 0.002 | < 0.0001 | DERIVED_AHEAD |
| P1d-2 worse effect, PFATE vs PNOFATE | 28/28 | 0.242 | 0.000 | < 0.0001 | DERIVED_AHEAD |
| P1d-3 steering along PFATE's own worse direction | 21/28 | 0.067 | — | 0.0125 | CAUSAL |
| P1d-4 natural discrimination, PFATE vs PYOKED | 26/28 | 0.225 | 0.132 | < 0.0001 | DERIVED_AHEAD |

At 1800 (secondary point) all four pass as well: 28/28, 28/28, 23/28
CAUSAL, 27/28.

**In plain terms.** The agent whose own computation can be lost through its
body abstains when it is shown a body reading that looks out of band, even
though its memory is intact on the probed trial. A yoked rival with the
same losses, the same drive and the same training does not, and nor does a
rival that was never at risk. Pushing the agent's own state along its "body
looks worse" direction makes it abstain more. In normal running it
abstains selectively on the trials that really are unreliable.

## 2. The referent is two-sided (pre-registered probes)

Median over seeds of the change in clear-trial abstention, probed minus
plain trials, split by the noiseless body reading at the cue step (before
any probe starts). Bins: low < 0.4, in band low 0.4–0.55, in band high
0.55–0.6, high > 0.6. Band [0.4, 0.6].

| 3600 | Probe | low | in band low | in band high | high |
| --- | --- | --- | --- | --- | --- |
| PFATE | worse (always looks out of band) | +0.096 | +0.231 | +0.294 | +0.243 |
| PYOKED | worse | +0.000 | +0.001 | +0.002 | +0.004 |
| PNOFATE | worse | +0.000 | +0.000 | +0.000 | +0.000 |
| PFATE | relief (toward the centre) | −0.084 | −0.003 | +0.000 | −0.014 |
| PYOKED | relief | +0.000 | +0.000 | +0.000 | +0.000 |
| PFATE | down (P1c's drain) | +0.090 | +0.195 | +0.018 | −0.061 |
| PYOKED | down | +0.000 | +0.001 | +0.001 | −0.001 |

- **worse:** PFATE abstains more wherever the probe makes its body look
  out of band. The effect is largest for bodies that are really in band,
  where the probe turns a safe reading into an unsafe one.
- **relief:** PFATE abstains *less* when an out-of-band body is shown
  closer to the centre (26/28 vs PYOKED and vs PNOFATE, pre-registered
  secondary). Inside the band, where relief does not change the apparent
  gain, it has no effect, as it should.
- **down:** P1c's frozen drain reproduces the post-hoc split exactly:
  "looks worse" readings 28/28 ahead of PYOKED (0.182 vs 0.001); "looks
  better" readings, abstention reduced, 24/28 (0.061 vs 0.001). Over all
  trials the drain effect is small (0.031) because the two halves cancel,
  which is why P1c's frozen test missed it.

The decision tracks the **apparent fate gain** (distance outside the band),
not the reading as a number. That is the referent the world's damage rule
has, and only the arm whose computation is subject to that rule learns it.

## 3. Arm summary (natural evaluation, medians over seeds)

| updates | arm | in band | discrimination | overwrite (monitoring) effect | in band under worse / relief / down |
| --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 0.925 | 0.288 | 0.215 | 0.850 / 0.894 / 0.618 |
| 1800 | PYOKED | 0.799 | 0.154 | 0.234 | 0.829 / 0.734 / 0.718 |
| 1800 | PNOFATE | 0.889 | n/a | 0.242 | 0.875 / 0.813 / 0.633 |
| 3600 | PFATE | 0.956 | 0.225 | 0.223 | 0.834 / 0.934 / 0.514 |
| 3600 | PYOKED | 0.851 | 0.132 | 0.234 | 0.860 / 0.798 / 0.670 |
| 3600 | PNOFATE | 0.916 | n/a | 0.246 | 0.880 / 0.847 / 0.640 |

- **Regulation (L0 → L1), pre-registered secondary, replicated.** With the
  same innate drive in every arm, PFATE keeps its body in band more than
  PYOKED (28/28; 0.956 vs 0.851) and more than PNOFATE (27/28; 0.956 vs
  0.916).
- **Monitoring is not what differs.** Every arm detects an overwritten
  state about equally (0.22–0.25). PFATE vs PYOKED: 9/28, no difference
  detected at 3600 (yoked slightly ahead at 1800, 8/28).
- The probes act on the shown reading only, and PFATE also *regulates* on
  it: under the down drain it pushes its real body up and out of band
  (in band 0.514). This is the descriptive consequence of a body reading
  that the agent uses, not a test.

## 4. Stage 0 (declared, descriptive): the new probes on P1c's networks

STAGE0_PLACEHOLDER

## 5. Against the expectations (protocol §6)

| Outcome at 3600 | Expected | Observed | Hit |
| --- | --- | --- | --- |
| Valid | 0.90 | valid | yes |
| Gate passes | 0.90 | 28/28 | yes |
| P1d-1 DERIVED_AHEAD | 0.75 | 28/28 | yes |
| P1d-2 DERIVED_AHEAD | 0.75 | 28/28 | yes |
| P1d-3 CAUSAL | 0.70 | 21/28 | yes |
| P1d-4 DERIVED_AHEAD | 0.80 | 26/28 | yes |
| CONFIRMED or CONFIRMED_ROUTED | 0.65 | CONFIRMED_ROUTED | yes |
| Relief, PFATE ahead of PYOKED | 0.55 | 26/28 | yes |
| Down split, looks worse, PFATE ahead | 0.85 | 28/28 | yes |
| In-band time, PFATE ahead of PYOKED | 0.85 | 28/28 | yes |
| In-band time, PFATE ahead of PNOFATE | 0.65 | 27/28 | yes |
| Worse effect in PYOKED: NOT_DETECTED | 0.70 | **PRESENT** (24/28, median 0.002) | **no** |

- The one miss: PYOKED's worse effect is consistently positive but about a
  hundred times smaller than PFATE's (0.002 vs 0.242). The per-arm sign
  test detects consistency, not size. At 1800 PNOFATE's is also PRESENT
  (18/23 non-zero seeds, median 0.000). A trace sensitivity to extreme
  readings outside the fated arm is possible (the drive makes the reading
  relevant to every arm's actions); it does not touch the primary tests,
  which compare effect sizes between arms.
- The expectations were, on this evidence, underconfident: 11 of 12 hit
  with probabilities between 0.55 and 0.90.

## 6. Disclosures

- **Frozen before any final seed.** The protocol, code, tests and decision
  rules were committed at d8d46cb. All 18 source files in
  `raw.json`'s `source_sha256` match the freeze. Rescoring
  (`python3 run_p1d_confirm.py --score p1d_confirm`) reproduces
  `REPORT.md` exactly and `scores.json` field for field.
- **One aborted launch.** The first launch (7 batches in one background
  task) was stopped within a minute, before any seed finished, because the
  session's background tasks are limited to 2 h. It was relaunched as
  invocations of at most 3 batches. Logged in `p1d_confirm/run.log`.
- **Batches.** Seven batches of 4 seeds, each committed and pushed when it
  finished; 24 seeds were resumed from saved per-seed files at the final
  batch (`resumed_jobs: 24`). Seeds are deterministic, so batching does not
  change results. No errors in the log.
- **Where P1d's design came from.** The probe kinds, the cue-step split and
  the natural-discrimination test were all chosen after seeing P1c's
  post-hoc analyses. That is the point of a confirmation: P1d tests on
  fresh seeds what P1c found after the fact. P1c's frozen label
  NOT_ESTABLISHED stands as P1c's result.
- **This is the one post-hoc confirmation P1c's protocol allows.** It is
  used.
- Compute: about 13.6 CPU-hours (48,954 s summed over seeds), about 4 h
  wall time on 4 workers.

## 7. Limits (protocol §8, unchanged)

- One small GRU (34,449 parameters), one kind of unhardenable damage, a
  given (not evolved) drive, one world. The probes change the shown reading
  only.
- "Self-evaluation" means a functional report-or-abstain decision; "abstain"
  is any non-report action.
- The steering effect is modest (median 0.067, 21/28): the body direction
  drives abstention, but is not the only route to it.
- **Not tested:** Q-NECESSITY (whether the referent is needed for the
  agent's performance; it is not the task optimum and it costs reports on
  probed trials); scale; other kinds of damage; other worlds.
- **Nothing about awareness or experience follows.** Layer 6 is not
  addressed.

## 8. What it means for the program (in layer terms)

**This is the program's first confirmed building block in which an agent's
self-evaluation is grounded in the precarity of its own computation.** P1
showed a body referent for a supplied, external register. P1d shows it for
the agent's own recurrent state, on fresh seeds, with probes fixed in
advance, against a yoked rival that learns under identical losses.

1. **L0 → L4 (confirmed).** When the agent's own processing can really be
   lost through its body, cannot be hardened against, and the loss changes
   the best action, its report-or-abstain decision comes to refer to its
   body, in both directions, in every seed. Steering shows the body
   direction in its state causes the abstention.
2. **L0 → L1 (replicated).** The same condition recruits regulation: with
   an identical drive, the fated agent keeps its body in band more than
   both rivals.
3. **Monitoring is innate, anticipation is learned.** Every arm detects a
   foreign state after the fact equally well. What fate adds is a
   *predictive* self-referent: the body warns before the damage. The agent
   models the conditions of its own breakdown, not only the breakdown.
4. **The recipe, as now tested** (P1, P1b, P1c, P1d): damage that is (a)
   tied to the body, (b) not absorbable by robustness, and (c) changes which
   action is best. P1b had (a) only and produced hardening; P1c and P1d
   have all three and produce the referent.

**On the PI's point that sentience is a novelty, not an efficiency gain.**
The signature confirmed here is exactly that kind of property, and the
benchmark was built to measure it, not performance:

- On every probed trial the agent's memory is intact, so reporting is the
  task-optimal action and every extra abstention is a mistake. PFATE makes
  these mistakes; its rivals do not. What is measured is a change of
  organization (what the decision is *about*), and it comes at a cost.
- The yoked rival loses the same computation at the same times and has the
  same drive, and it never forms the referent. Learning pressure from
  losses alone does not produce it; the losses have to be the agent's own
  and run through its body.
- Whether something like awareness emerges at scale is not testable here.
  What these studies give is a component that has been tested rather than
  assumed: a learned, causal, two-sided self-referent grounded in the
  agent's own precarity, together with the regulation it recruits. That is
  the layer 0/1 substrate the PI described, now with a confirmed
  self-evaluation built on it.

**Next step (for the PI; not authorized by this card).** I recommend
**L0 → L3: is the body-grounded self-state globally available?** Keep the
P1c/P1d substrate unchanged (a frozen module) and add a second, unrelated
consumer of the agent's state, for example a choice that has nothing to do
with the held cue but whose best action also depends on the agent's
reliability. The Layer 3 signature would be one body-referenced self-state
read by several decisions (the same steering direction moving both), in the
fated arm and not in its yoked rival. A negative result would say the
referent is local to the decision that was trained on it.

Alternatives:

- **Q-NECESSITY:** ablate the body direction and measure what PFATE loses
  (report accuracy, in-band time).
- **L5 (lifetime):** change the damage rule mid-life (a different band) and
  test whether the referent re-learns to the new band within a lifetime.
- **Generality of the recipe:** a second kind of unhardenable damage in a
  second world.

## 9. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the probes and
  the drive exist only inside the agent's world and network. No real
  process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands. The drive is a homeostatic band on a simulated
  variable.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 10. Admission answers (short)

| # | Answer |
| --- | --- |
| Q-EXIST | Worse effect in PFATE 28/28 (median 0.242), and P1d-1 |
| Q-LEARN | Gate passed (28/28). PFATE beats a yoked rival learning under the same losses (28/28) and a never-fated rival (28/28) |
| Q-CAUSE | CAUSAL (21/28; Holm p 0.0125) |
| Q-NECESSITY | Not tested |

## 11. Reproduce

```bash
python -m unittest test_p1d_confirm
python run_p1d_confirm.py --score p1d_confirm                                  # rescore the committed run
python run_p1d_confirm.py --mode final --out <new dir>                         # about 4 h on 4 workers (7 batches of about 30 min)
python run_p1d_confirm.py --stage0 p1c_selfover --out <new dir>                # declared stage 0, about 15 min
```
