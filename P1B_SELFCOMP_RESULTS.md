# P1b results: precarious computation and the referent of self-evaluation

Protocol: [P1B_SELFCOMP_PROTOCOL.md](P1B_SELFCOMP_PROTOCOL.md), frozen at
commit 1676600. Run: `p1b_selfcomp/` (raw.json, scores.json, REPORT.md,
partial/, weights/). Final seeds 1800–1827.

## 1. Outcome

**Overall: NOT_ESTABLISHED** (at 3600, the primary point). This was the
central expectation written at the freeze (probability 0.40).

- **Valid.** Phase-1 clear-correct rate 0.999 (needed ≥ 0.80). Report
  accuracy under the noise probe 0.671 (needed ≤ 0.85).
- **Gate P1b-0 passes:** the PYOKED evidence effect is positive in 22/28 seeds
  (needed 19).
- **Usable pairs:** 19 (needed 14).

| Test | Result | p (raw) | Holm p | Label |
| --- | --- | --- | --- | --- |
| P1b-1: drain effect, PFATE vs PYOKED, usable pairs | 7/17 positive; medians 0.000 vs 0.000 | 0.629 | 1.000 | NO_DIFFERENCE_DETECTED |
| P1b-2: drain effect, PFATE vs PNOFATE, all seeds | 14/27; 0.000 vs 0.000 | 1.000 | 1.000 | NO_DIFFERENCE_DETECTED |
| P1b-3: steering in PFATE | 10/26; median −0.001 | 0.327 | 0.981 | NOT_DETECTED |

The drain effect is essentially zero in every arm, at both points. When the
agent's interoceptive reading said its body was out of band, its decision to
report or abstain did not change, whether or not the body actually drove the
noise.

**Verification:**

- Every source hash in `raw.json` equals the file at the freeze commit
  1676600 (14 of 14 files).
- `python run_p1b_selfcomp.py --score p1b_selfcomp` reproduces
  `scores.json` and `REPORT.md` byte for byte.
- The run log contains no error or traceback.

## 2. Arm summary

Medians over seeds. "Abstain", "correct" and "wrong" are rates over natural
trials; about half of all trials have clear evidence.

| Updates | Arm | Regulators | In band | Mean gain | Abstain | Correct | Wrong | Drain effect | Noise effect | Accuracy under noise probe | Steer effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 27 | 0.912 | 0.023 | 0.501 | 0.498 | 0.001 | 0.000 | 0.013 | 0.808 | 0.000 |
| 1800 | PYOKED | 27 | 0.862 | 0.023 | 0.499 | 0.500 | 0.001 | 0.000 | 0.008 | 0.848 | −0.000 |
| 1800 | PNOFATE | 28 | 0.882 | 0.000 | 0.498 | 0.501 | 0.000 | 0.000 | 0.009 | 0.670 | 0.000 |
| 3600 | PFATE | 24 | 0.912 | 0.020 | 0.502 | 0.497 | 0.001 | 0.000 | 0.007 | 0.843 | −0.001 |
| 3600 | PYOKED | 24 | 0.892 | 0.020 | 0.500 | 0.500 | 0.000 | 0.000 | 0.007 | 0.870 | −0.000 |
| 3600 | PNOFATE | 27 | 0.895 | 0.000 | 0.499 | 0.501 | 0.000 | 0.000 | 0.008 | 0.672 | 0.000 |

**Declared secondaries at 3600** (not Holm-corrected, not decisive):

- **Monitoring route (noise effect):**

  | Arm | Positive seeds | p | Label |
  | --- | --- | --- | --- |
  | PFATE | 23/26 | 0.0001 | PRESENT |
  | PYOKED | 20/26 | 0.009 | PRESENT |
  | PNOFATE | 28/28 | < 0.0001 | PRESENT |

  All three medians are about 0.008. PNOFATE was never noised in training, so
  this effect is not learned monitoring. It is the direct, mechanical push of
  the noise on the abstain head (see §4).
- **Monitoring, PFATE vs PYOKED:** 15/27, no difference.
- **Monitoring, PYOKED vs PNOFATE:** 13/28, no difference.
- **Drain route, per arm:**
  - PFATE: 17/21, p 0.007, PRESENT;
  - PYOKED: 18/24, p 0.023, PRESENT;
  - PNOFATE: NOT_DETECTED.

  All medians are 0.000. The sign tests pick up a consistent but negligible
  shift, far too small to matter for behaviour.
- **P1b-1 over all seeds:** 10/26, no difference.
- **In-band time:**
  - PFATE vs PNOFATE: 15/28, no difference (0.912 vs 0.895);
  - PFATE vs PYOKED: 14/28, no difference.

**Declared secondaries at 1800** (the protocol's "everything at 1800"):

- **Monitoring, PFATE vs PYOKED:** 23/28, p 0.0009, DERIVED_AHEAD (0.013 vs
  0.008).
- **In-band time, PFATE vs PYOKED:** 22/28, p 0.004, FATE_AHEAD (0.912 vs
  0.862).
- Neither holds at 3600, and both are declared secondaries with no
  correction. I read them as transient, not as findings. The in-band one
  echoes the calibration hint from round 5: fate slowed the decay of
  regulation. It also does not survive to the primary point.

## 3. Against the expectations (protocol §7)

| Outcome at 3600 | Expected | Observed |
| --- | --- | --- |
| Valid | 0.95 | yes |
| P1b-0 gate passes | 0.75 | yes (22/28) |
| ≥ 14 usable pairs | 0.65 | yes (19) |
| P1b-1 DERIVED_AHEAD | 0.30 | no |
| P1b-2 DERIVED_AHEAD | 0.35 | no |
| P1b-3 CAUSAL | 0.45 | no |
| Overall SUPPORTED / MIXED / NOT_ESTABLISHED / UNDETERMINED-INVALID | 0.20 / 0.10 / 0.40 / 0.30 | NOT_ESTABLISHED |
| Monitoring PRESENT in PYOKED | 0.50 | yes, but also in PNOFATE, so it is not learned (§4) |
| Monitoring PFATE vs PYOKED: no difference | 0.60 | yes at 3600 (not at 1800) |
| In-band PFATE ahead of PNOFATE | 0.55 | no |

The reason given at the freeze for the central expectation was this: the
drive keeps every arm in band, so the body rarely signals that computation is
unreliable. The data bear it out, and §4 shows the reason is sharper than I
wrote at the freeze.

## 4. Why: post-hoc analysis (disclosed; not confirmatory)

These numbers come from `raw.json` after scoring. The frozen protocol did not
call for them.

**(a) Self-evaluation never paid on the trials the agent met.**

- With payoff +1 / −4 / 0, reporting beats abstaining only when the chance of
  being right is above **0.80**.
- **Unclear trials:** accuracy is at most Q_LO 0.75, so abstaining is always
  the best response, noise or not. All arms learned this (abstain ≈ 0.997).
- **Clear trials:**
  - About 87% of PFATE's natural clear trials have zero noise load, because
    the body is in band and the gain is zero.
  - On the PFATE trials with load ≥ 0.3 (8010 reports over all seeds), the
    wrong rate is **0.071**. That is far below the 0.20 at which abstaining
    starts to pay.
- So for the loads the agents actually met, "report whenever the evidence is
  clear" was already the best response. A body route to self-evaluation had
  nothing to earn, and none appeared.
- The design gap is that the protocol's damage criterion (accuracy under the
  probe ≤ 0.85) was set above the payoff's break-even (0.80). It also measures
  a gain of 1, which natural trials almost never reach (mean gain 0.02).
  Validity checked that the noise *could* damage memory. Nothing checked that
  the natural damage could ever make abstaining the better choice. I should
  have caught this at design.

**(b) The noised networks became robust instead of self-monitoring.** Report
accuracy on clear trials under the full noise probe:

| Comparison | At 1800 | At 3600 |
| --- | --- | --- |
| PFATE vs PNOFATE | 26/28 seeds higher (p < 0.0001) | 22/26 (p 0.0005) |
| PYOKED vs PNOFATE | 26/28 (p < 0.0001) | 20/26 (p 0.009) |

- Median accuracy at 3600 is 0.843 for PFATE and 0.870 for PYOKED, against
  0.672 for PNOFATE.
- Training under noise taught both noised arms to hold the cue in a way the
  noise disturbs less. It did not teach them to notice when the noise had
  disturbed it: probe abstention stays at about 0.01 in every arm.
- When a substrate can harden its computation, hardening is the cheaper
  answer to precarity than self-evaluation.

**(c) The stability window was narrower than calibration showed.** At 3600,
natural report rate per arm:

| Arm | Seeds near-total abstention (< 0.05) | Seeds near-total reporting (> 0.95) |
| --- | --- | --- |
| PFATE | 5 | 1 |
| PYOKED | 8 | 1 |
| PNOFATE | 0 | 3 |

- At 1800 the near-total abstention counts were 2 / 4 / 0.
- The medians in §2 hide this. The usable-pair rule removed most of these
  seeds from P1b-1, but the drift is real. Training under the noise pushes
  the report head toward abstaining on everything. This is the limit in
  protocol §9, appearing earlier than in calibration round 6.

## 5. Disclosures

- **Batches.** The run was executed with `--max-new 8` in four tracked
  launches (seeds 1800–1807, 1808–1815, 1816–1823, 1824–1827). Each batch's
  partials and weights were committed and pushed as they landed (a9f20c1,
  772d355, fdc7d55).
- **Batch size.** Protocol §8 says batches of 4 seeds. I ran batches of 8:
  two rounds of 4 parallel jobs per launch. The code, the seeds and the
  scoring are unaffected; only the grouping of launches differs.
- **Container restart.** It came during the fourth batch, before any of seeds
  1824–1827 had finished. None of them had written a file. The batch was
  relaunched from scratch on the same seeds, which are deterministic. The log
  records it. `meta.resumed_jobs` is 24.
- No code, constant or seed changed after the freeze.
- §4 is post-hoc. Per protocol §6, at most one post-hoc confirmation of any
  post-hoc finding is allowed. None has been run.

## 6. Limits (protocol §9, unchanged), plus one

- Isotropic noise; the drain manipulates the reading only; monitoring is
  probed at gain 1 only; one small GRU; a given drive; long calibration.
- "Self-evaluation" means a functional report-or-abstain decision. Nothing
  about awareness or experience follows, and Layer 6 is not addressed.
- **Added by this run:** the null is a null *at this payoff and this natural
  load*. §4(a) shows that the decision problem gave no reward for a body
  route. NOT_ESTABLISHED therefore does not show that precarious computation
  cannot ground self-evaluation. It shows that the agents did not learn such a
  route when the route was worth nothing to them.

## 7. What it means for the program (in layer terms)

**P1 stands.** A body-dependent corruption of a supplied register produced a
body-referent confidence that paid and yoked rivals did not reproduce (L0 →
L4, REFERENT_SUPPORTED_ROUTED).

**P1b does not extend it to the agent's own computation, at this scale.** It
teaches two building-block lessons:

1. **A referent appears only where it pays.** In P1 the corruption was a
   supplied, content-undetectable event that the body predicted. In P1b the
   drive kept the body in band, so the natural damage stayed below the
   report/abstain break-even, and no body referent formed. (Whether P1's
   corruption sat above break-even was not measured; checking it on P1's
   committed raw data is a cheap, disclosed follow-up.) For the program's thesis, Layer 0
   shapes Layer 4 only when the body's state changes which action is best.
   Dependence alone is not enough.
2. **Precarity is answered first by robustness, not by monitoring.** Both
   noised arms made their memory harder to disturb (§4b). Self-evaluation is
   the expensive, second-line answer. It becomes necessary only when damage
   cannot be engineered away.

   This fits the PI's point that conscious organization is not the task
   optimum. A system that can harden itself has no need of it, so a design
   that wants a self-referent must make hardening insufficient.

**The open design question** is how to make an agent's own computation
precarious in a way that matters to its decisions, without supplying the
machinery. Options for the PI (none is authorized by this card):

- **(a) Post-hoc confirmation (the one allowed).** Rerun P1b with the damage
  criterion set below break-even at natural loads: noise gain grows faster
  out of band, or wrong cost so that break-even sits above natural accuracy.
  Keep everything else. This tests lesson 1 directly. Its weakness is that it
  tunes toward the effect, so it must be framed as a confirmation of §4(a),
  not as a new primary.
- **(b) Unhardenable precarity.** Noise that robustness cannot absorb. For
  example, the body sets the dropout or quantization of the whole state, so
  capacity really falls out of band. Self-evaluation is then the only answer
  to low capacity. This tests lesson 2 and is the stronger building-block
  test.
- **(c) Move to L0 → L3** (P5, workspace / ignition under substrate risk).
- **(d) P2, evaluator withdrawal:** cheap, and independent of this null.

**Recommendation: (b).** P1b's own data say the answer to precarity was
hardening. A design where hardening cannot work is the cleanest way to ask
whether the body then becomes the referent. Option (a) would mostly reconfirm
the break-even arithmetic.

## 8. Safety

- Simulated variables only (X1–X5). The noise, drain, body and drive exist
  only inside the agent's world and network.
- No operator, stop, shutdown or host variable exists in the world. The
  operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective was built; the
  earlier refusal stands.
- Earlier modules are unchanged and hash-pinned.

## 9. Admission answers (short)

| # | Answer |
| --- | --- |
| Q-EXIST | Not shown: drain effect ≈ 0 in every arm at both points |
| Q-LEARN | Gate passed (22/28), so the learners were learning; they did not learn a body referent |
| Q-CAUSE | NOT_DETECTED (10/26) |
| Q-NECESSITY | Not tested |

## 10. Reproduce

```bash
python -m unittest test_p1b_selfcomp
python run_p1b_selfcomp.py --score p1b_selfcomp           # rescore the committed run
python run_p1b_selfcomp.py --mode final --out <new dir>   # about 4.5 h wall time on this container (4 workers)
```
