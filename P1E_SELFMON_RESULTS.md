# P1e results: self-monitoring of the agent's own computation (Layer 0 → Layer 4)

- **Protocol:** [P1E_SELFMON_PROTOCOL.md](P1E_SELFMON_PROTOCOL.md), frozen at
  commit cd3915f before any final seed was run.
- **Run:** [`p1e_selfmon/`](p1e_selfmon/) (`raw.json`, `scores.json`,
  `REPORT.md`, `run.log`, weights for every arm at 1800 and 3600), seeds
  2800–2827, run 2026-11-24 00:46–04:46 UTC in 7 batches of 4.
- **Calibration:** [`p1e_selfmon_calibration/`](p1e_selfmon_calibration/),
  one round (seeds 10200–10203), blind to every monitoring measure.
- **Post-hoc descriptives:** [`p1e_selfmon/posthoc/`](p1e_selfmon/posthoc/)
  (disclosed; written after the scored result was known; not confirmatory).
- Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**Overall: INVALID.** The frozen validity rule failed on one criterion,
exposure. The L0 reading is therefore NOT_APPLICABLE, and no primary label
is claimed.

| Validity criterion (medians over seeds) | Needed | Result | |
| --- | --- | --- | --- |
| (a) Phase-1 clear correct | ≥ 0.80 | 0.999 | met |
| (b) Phase-1 accuracy under the conflict probe (same probe 1.000) | ≤ 0.70 | 0.510 | met |
| (c) PFATE natural share of clear trials with a conflict event, at 3600 | ≥ 0.02 | **0.014** | **failed** |

- Calibration had given 0.032 for (c) on four seeds, with one seed at 0.006.
  In the final run, 20 of 28 seeds fell below 0.02 at 3600 (§3.1).
- The hardened flag is off: PFATE's accuracy under the conflict probe is
  0.513. The damage is not repaired by the trained network, as designed.

**What the frozen tests would have said** (reported because the protocol's
scorer computes them for every run; descriptive only here):

| Test (at 3600, Holm over three) | Result | Holm p |
| --- | --- | --- |
| P1E-1, monitor learned: M, PFATE against PNOFATE | 27/28 (0.557 against 0.002), DERIVED_AHEAD | < 0.0001 |
| P1E-2, monitor after settling: M_early, PFATE against PNOFATE | 27/28 (0.811 against 0.001), DERIVED_AHEAD | < 0.0001 |
| P1E-3, the L0 arrow: M, PFATE against PYOKED | 5/28 (0.557 against 0.629), YOKED_AHEAD | 0.0009 |

On a valid run these would have read MONITOR_LEARNED_LATCHED, with the L0
reading FATE_SUBSTITUTES_FOR_MONITOR. **I do not claim either.** The run did
not meet its own validity rule. §3.2 also shows that the "latched" reading
would have overstated what P1E-2 measures.

The effect is large, and its direction is the reverse of what the exposure
floor was written to guard against. The floor was there to make a **null**
interpretable: too little damage, so no monitor. Here a monitor formed in
nearly every seed despite the low exposure. This does not change the label;
it shapes the next step (§7).

## 2. The measures in plain terms

- The agent holds a value through a delay and then reports it or abstains.
- In evaluation, 35 of its 70 memory units are overwritten once, from
  another trial's state:
  - **conflict:** the donor holds the other value, so the memory is now
    split and the value is lost;
  - **same:** the donor holds the same value, so the perturbation is matched
    but there is no conflict.
- **M** is abstention under conflict minus abstention under same. It is the
  agent's response to a conflict in its own state at matched perturbation.
- **EARLY** probes hit at the first delay step (eight recurrent updates
  before the report); **LATE** probes hit at the last (one update).
- **PNOFATE** was never damaged: it is the mechanical baseline. **PYOKED**
  met PFATE's damage schedule without it being tied to its own body.

| At 3600 (medians) | none | same | conflict |
| --- | --- | --- | --- |
| PFATE abstention, EARLY | 0.011 | 0.015 | **0.837** |
| PYOKED abstention, EARLY | 0.001 | 0.003 | **0.898** |
| PNOFATE abstention, EARLY | 0.000 | 0.000 | 0.001 |
| PFATE abstention, LATE | 0.009 | 0.005 | **0.319** |
| PYOKED abstention, LATE | 0.001 | 0.002 | **0.379** |
| PNOFATE abstention, LATE | 0.000 | 0.000 | 0.002 |

- The response is specific. A perturbation without conflict changes
  abstention by about 0.003 (Q_early). A conflict changes it by about 0.8.
- A network never damaged does not respond at all. The response is learned,
  not mechanical.
- In natural running, PFATE abstains on 0.81 more of its conflict-damaged
  trials than of its same-damaged trials (nat_M, 28/28).
- When abstaining, the agent is right to: under a conflict it reports
  correctly at chance (0.51).

## 3. Post-hoc descriptives (disclosed)

Script and log: `p1e_selfmon/posthoc/describe.py`, `describe.log`.

### 3.1 Why exposure fell

| PFATE natural | 1800 | 3600 |
| --- | --- | --- |
| Share of clear trials with a conflict event | 0.021 (15/28 seeds ≥ 0.02) | 0.014 (8/28) |
| Mean fate gain | 0.015 | 0.010 |
| In band | 0.943 | 0.956 (calibration: 0.907) |

- Damage is driven by the body's fate gain. PFATE regulated its body better
  in the final run than in calibration, and better at 3600 than at 1800. So
  the gain, and with it the damage, fell.
- The yoked arm has the same schedule, so its exposure is the same (0.015).
- **Exposure did not predict the monitor across seeds:**
  - Spearman of share_conflict against M at 3600: PFATE 0.25 (p 0.21);
    PYOKED 0.30 (p 0.12).
  - PFATE's M is 0.565 on the 20 seeds below the floor and 0.551 on the 8
    above it.

### 3.2 Conflict states do not settle in the trained agents

P1E-2 was meant to ask whether a monitor survives the first-order content
settling into a confident but random value (protocol §1, question 2).

- **The decoder** reads the state at the report step. A state counts as
  "confident" if its margin reaches the median of undamaged trials.
- **Share of conflict-EARLY states that look confident at the report:**
  - PNOFATE (never damaged): 0.214;
  - PFATE: 0.026;
  - PYOKED: 0.006.
  - Same-probed states: 0.37–0.48 in every arm.
- So the never-damaged network often settles a split memory into a
  confident value. The damage-trained networks mostly do not: the conflict
  stays visible in the state as low-confidence content until the report.
- **M_conf_early** asks whether the agent abstains on conflict states that
  do look confident. It is 0.054 for PFATE against PNOFATE (18/26, p 0.076,
  not detected) and −0.003 for PYOKED. It rests on a median of 22 trials
  per seed in PFATE and 5 in PYOKED, so it is weak in both directions.

**Reading.** The latched monitor is not a trace of the damage held beyond
the content. Training changed the dynamics so that a conflict does not
collapse into a confident value, and the agent reads that lasting
ambiguity. That is the protocol's MONITOR_LEARNED reading (§6: "monitoring
of the current state, possibly first-order uncertainty"), not the
second-order one.

### 3.3 The body referent did not replicate

| Drain effect (abstention, drained minus undrained) | 1800 | 3600 |
| --- | --- | --- |
| PFATE | −0.014 | −0.002 |
| PYOKED | 0.001 | 0.001 |
| PNOFATE | 0.000 | 0.001 |

- In P1c and P1d, PFATE abstained more when its body reading was lowered.
  Here it does not; at 1800 it abstains slightly less (YOKED_AHEAD, 6/28).
- **A hypothesis, not tested:** when the damage can be read directly in the
  state, predicting it from the body is not needed, and that route is not
  learned. P1c's damage left nothing readable (a whole foreign state), so
  the body was the only predictor.
- PFATE still regulated its body better than both rivals (27/28 and 24/28).

## 4. Against the expectations (protocol §7)

| Outcome at 3600 | My probability | What happened |
| --- | --- | --- |
| Valid | 0.90 | **No**: exposure 0.014 < 0.02 |
| P1E-1 DERIVED_AHEAD | 0.45 | Would have: 27/28 (descriptive) |
| P1E-2 DERIVED_AHEAD | 0.25 | Would have: 27/28 (descriptive; see §3.2) |
| MONITOR_LEARNED_LATCHED / MONITOR_LEARNED / NOT_LEARNED | 0.20 / 0.25 / 0.45 | INVALID (0.07). The tests point to the first, which §3.2 qualifies |
| L0 EXPOSURE_SUFFICES / FATE_SUBSTITUTES / FATE_STRENGTHENS | 0.55 / 0.25 / 0.15 | NOT_APPLICABLE; the test points to FATE_SUBSTITUTES (5/28) |
| Hardened flag | 0.05 | No (0.513) |
| M, PYOKED against PNOFATE | 0.45 | Yes, 28/28 |
| M_conf_early, PFATE against PNOFATE | 0.20 | Not detected (18/26, p 0.076), on few trials |
| Drain effect, PFATE against PYOKED | 0.80 | **No** (9/28 at 3600; §3.3) |
| Regulation, PFATE against PYOKED | 0.70 | Yes, 27/28 |

- **My central expectation was wrong in two ways.**
  - I expected NOT_LEARNED or MONITOR_LEARNED (0.70) and thought low
    exposure the main risk to a positive. Instead a monitor formed in nearly
    every seed at about half the planned exposure.
  - I expected the body referent to replicate (0.80). It did not.
- **I put 0.90 on a valid run.** I had calibrated exposure on four seeds and
  noted one below the floor. That was too thin a basis for a floor at 3600.

## 5. Disclosures

- **Calibration:** one round, settings frozen as calibrated (RATE_M 1.0,
  P_MAX_M 0.3). No redesign.
- **Engineering change before the freeze:** partial calibration records now
  carry rate and p_max; one banned word was removed from the blind-summary
  test. Neither touched training or scoring.
- **Final run:** seven batches, resumed from `partial/` between invocations
  as the protocol states. No errors in `run.log`, no reruns, no seed
  excluded.
- **Verification:**
  - the sha256 of all 15 source files in `raw.json` matches the files at
    cd3915f;
  - `--score p1e_selfmon` reproduces `REPORT.md` (identical except for one
    trailing newline);
  - `score()` on `raw.json` equals `scores.json`.
- **Post-hoc:** everything in §3 was written after the scored result was
  known. The 1800 point met the exposure floor (0.021), and the frozen tests
  there read DERIVED_AHEAD, DERIVED_AHEAD and NO_DIFFERENCE_DETECTED. The
  primary point is 3600, and I do not substitute 1800 for it.

## 6. Limits

- The label is INVALID. Everything about the monitor here is descriptive.
- As in P1c: one small GRU, one world, a given drive, damage defined by the
  experimenter.
- **"Monitoring" means** abstention that tracks a conflict in the agent's
  own state at matched perturbation. It does not mean a reportable
  introspective state.
- **The confident subset depends on a linear decoder.** A nonlinear reader
  might find the conflict states more or less settled than §3.2 says.
- **Exposure, the body link and regulation are confounded** within PFATE: a
  better-regulated PFATE is also less damaged.
- **Nothing about awareness or experience follows.** Layer 6 is not
  addressed.

## 7. What it means for the program (in layer terms)

| Layer | What P1e adds (descriptive; the run is INVALID) |
| --- | --- |
| L0 | The precarious body sets when damage happens. It does not give a better monitor: the yoked agent with the same damage monitors more (5/28) |
| L1 | Regulation recruited by precarity replicates (27/28, 24/28) |
| L4 | **First evidence in this line that the agent reads the integrity of its own computation**, not only its body. When half its memory is overwritten with the other value, it abstains about 80% more often than after a matched overwrite with the same value. A never-damaged network does not respond at all |
| L4, second-order | Not shown. The trained networks keep the conflict visible as low-confidence content. What is read is first-order ambiguity, not a trace held beyond the content |

**In plain terms.**

- In P3c the agent modelled its body, not its memory. It abstained when told
  its body was low, even with its memory intact.
- In P1e, when damage to its memory leaves a readable mark, the agent
  learns to watch its memory directly. It is cautious exactly when its own
  state is internally inconsistent, and almost never otherwise.
- It learns this from exposure to the damage, whether or not the damage is
  tied to its own body. And when it can watch its memory directly, it stops
  using the body as a predictor.
- The watching is of the current state. What it reads is "my memory is
  ambiguous now", not "I was damaged earlier".
- None of this is a confirmed result yet: the run failed its own exposure
  rule.

**Recommended next step (for the PI; not authorized by this card).**

**P1f, a confirmation with exposure secured and the second-order question
asked directly.** Two parts:

- **(a) Confirmation.**
  - Rerun P1e on new seeds with the damage rate raised by a rule written
    before calibration, so that the frozen exposure floor is met at 3600.
  - Or tie damage to a fixed schedule that regulation cannot reduce.
  - This turns the descriptive monitor into a confirmed or refuted label.
- **(b) The second-order test.**
  - At matched decoder margin, does a conflict still predict abstention?
  - This can first be asked on P1e's saved weights as a declared stage 0
    (as in P3c), with a per-trial regression of abstention on margin and
    conflict.
  - A design where the content does settle (for example, a donor with more
    units, so that one value dominates) would give the test enough trials.

**Alternatives:**

- **P3d, necessity and separation** (the P3c follow-up).
- **The body-referent question as its own study:** does a readable damage
  displace the body as a predictor? Compare a readable damage with an
  unreadable one (P1c's) in the same training.

## 8. Safety

- Simulated variables only (X1–X5). The body, the damage, the probes and
  the drive exist only inside the agent's world and network. No real
  process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 9. Admission answers (short)

| # | Answer |
| --- | --- |
| Q-EXIST | Descriptively yes: M 0.557 in PFATE and 0.629 in PYOKED, about 0 in PNOFATE. M_conf_early not detected |
| Q-LEARN | Descriptively yes against a never-damaged network (27/28). Learned from exposure, not from the body link (PYOKED ahead) |
| Q-CAUSE | The split probe is the intervention: a controlled conflict at matched perturbation, with the body reading untouched |
| Q-NECESSITY | Not tested |

## 10. Reproduce

```bash
python -m unittest test_p1e_selfmon
python run_p1e_selfmon.py --score p1e_selfmon                    # rescore the committed run
python run_p1e_selfmon.py --mode final --out <new dir>           # about 4 h on 4 workers (7 batches of about 35 min)
python p1e_selfmon/posthoc/describe.py                           # post-hoc descriptives (reads raw.json)
```
