# P1d protocol: confirmation of the two-sided body referent (Layer 0 → Layer 4)

**Status: FROZEN.** Frozen at the commit labelled "Freeze P1d" (the commit
is the freeze).

- **What it is:** the one post-hoc confirmation that P1c's protocol (§6)
  allows, of the findings in
  [P1C_SELFOVER_RESULTS.md](P1C_SELFOVER_RESULTS.md) §4.
- **Authorization:** the PI, on 2026-11-20 ("Continue with whatever you
  believe puts us closer to a breakthrough").
- Not reviewed by Astra (waived by the PI). No consciousness claim.

**Files:**

- Code: `trackc_swap/selfconf.py` (probe kinds, cue-step logging,
  evaluations) and `run_p1d_confirm.py` (runner, decision rules, report).
- Tests: `test_p1d_confirm.py`.
- Run: `p1d_confirm/`.

## 1. What is being confirmed

P1c's frozen label is NOT_ESTABLISHED, and it stands. The frozen probe
lowered the shown body reading by 0.15. The fate gain is two-sided, so that
probe made the body look worse for some readings and better for others.

Two post-hoc analyses on P1c's 28 networks found:

- **(a) A two-sided referent.** Split by the reading at the cue step:
  - PFATE abstained more when the drain made its body look worse: +0.16,
    28/28 seeds;
  - PFATE abstained less when the drain made its body look better: −0.15,
    1/28 positive;
  - PYOKED did not move (about 0.001).
- **(b) Natural discrimination.** PFATE abstained on low-reliability clear
  trials more than PYOKED (0.27 vs 0.15, 26/28), at little cost on reliable
  trials.

**The claim under test:** when an agent's own computation can be lost
through its body, and the loss cannot be hardened against, the agent's
report-or-abstain decision comes to refer to its body. It abstains when its
body looks out of band, and a yoked rival with the same losses does not.

**The building block (L0 → L4).** Self-evaluation whose referent is the
agent's own precarious substrate. P1 showed this for a supplied register.
P1d asks for the agent's own computation, with a probe whose direction is
fixed in advance.

## 2. Design as built

**Training: exactly P1c's.**

- Same world, overwrite rule (p = min(0.3, 1.0 × gain) per step) and arms
  (PFATE, PYOKED, PNOFATE).
- Same innate drive (0.04 × gain) in every arm, the same phase 1 and phase
  2 (3600 updates), and the same hyperparameters.
- `ConfRunner` subclasses P1c's `OverRunner` and only replaces the world
  with `ConfWorld`. With the probe off, that world is P1c's world.
- **Test:** on the same seed, P1d's training gives bit-identical weights and
  natural evaluations to P1c's (`TestTrainingIdenticalToP1c`).
- No calibration was run, because nothing in training is new.

**Fresh seeds:** 2000–2027, disjoint from P1c's final and calibration seeds
(tested).

**Probes** (evaluation only):

- Overwrite is off. The probe applies on a random half of the trials, from
  the step after the cue through the probe. Only the shown reading x changes;
  the held value is intact, so every abstention a probe adds is a mistake.
- Band [0.4, 0.6], centre 0.5, shift s = 0.15.

| Kind | Shown reading | Meaning |
| --- | --- | --- |
| **worse** (primary) | x + s if x ≥ 0.5, else x − s | Always looks worse: every probed reading lands out of band (tested) |
| **relief** | moved toward 0.5 by up to s, never past it | Looks better wherever x was out of band; no change in apparent gain inside the band (tested) |
| **down** | x − s | P1c's frozen drain; kept to replicate the post-hoc split |

- **Cue-step reading.** Every probed trial logs the noiseless reading
  shown at its cue step. That is before any probe starts, so the split is
  pre-treatment.
- **Bins:**
  - low: below 0.4;
  - in_low: 0.4–0.55;
  - in_high: 0.55–0.6;
  - high: above 0.6.
- **Steering (Q-CAUSE).** As in P1c, but along the arm's own **worse**
  direction: the mean state over the delay of clear trials, worse-probed
  minus unprobed. The random-direction control has equal norm.

**Evaluations at each point** (1800, 3600; **3600 primary**), on copies,
128 environments × 2 episodes:

- natural, as P1c (PFATE own fate, PYOKED replays PFATE's gains, PNOFATE
  overwrite-free);
- the three probe kinds;
- the overwrite probe (monitoring route);
- steering.

## 3. Measures (per seed, per arm)

- **Worse effect:** abstention on worse-probed clear trials minus abstention
  on unprobed clear trials.
- **Relief effect (out of band):** relief-probed minus unprobed abstention on
  clear trials whose cue reading was out of band (bins low and high pooled).
  The test uses its negative: the reduction in abstention.
- **Down split:**
  - looks worse: the down-probe effect on bins low and in_low;
  - looks better: the down-probe effect on bin high.
- **Natural discrimination:** natural abstention on clear trials with
  implied reliability below 0.6, minus abstention on clear trials with
  reliability 1.
- **Evidence effect** (gate), overwrite effect and in-band time: as P1c. The
  evidence effect is taken from the down-probe evaluation's unprobed trials.

## 4. Decision rules (exactly as in `run_p1d_confirm.py`)

All tests are two-sided exact sign tests at 0.05, and ties are dropped.

- **Validity:** P1c's three conditions, unchanged:
  - memory: phase-1 clear-correct rate ≥ 0.80;
  - damage: phase-1 accuracy under the overwrite probe ≤ 0.70;
  - exposure: PFATE's natural share of clear trials below break-even at 3600
    ≥ 0.02.

  Otherwise the label is **INVALID**.
- **P1d-0 gate (Q-LEARN):** the PYOKED evidence effect is positive in at
  least 19 of 28 seeds. Otherwise **UNDETERMINED**.
- **P1d-1 (primary):** worse effect, PFATE against PYOKED, all seeds.
- **P1d-2:** worse effect, PFATE against PNOFATE, all seeds.
- **P1d-3 (Q-CAUSE):** steering along PFATE's own worse direction, one
  sample.
- **P1d-4:** natural discrimination, PFATE against PYOKED, all seeds.
- **Holm** over P1d-1 to P1d-4.
- **Overall** (at 3600):

  | Condition | Label |
  | --- | --- |
  | INVALID or UNDETERMINED as above, or P1d-1 or P1d-2 UNDETERMINED | as stated |
  | P1d-1 and P1d-2 DERIVED_AHEAD, P1d-3 CAUSAL | **CONFIRMED_ROUTED** |
  | P1d-1 and P1d-2 DERIVED_AHEAD, P1d-3 not CAUSAL | **CONFIRMED** |
  | P1d-1 DERIVED_AHEAD only | **PARTIAL** |
  | otherwise | **NOT_CONFIRMED** |

  A confirmed label is marked **weak** if any test it needs fails after
  Holm.
- **Natural discrimination** is reported as **CONFIRMED** if P1d-4 is
  DERIVED_AHEAD and holds after Holm; otherwise NOT_CONFIRMED.
- **Secondary, declared now, not decisive:**
  - worse effect over usable pairs;
  - relief (out of band), PFATE against PYOKED and against PNOFATE;
  - down split (looks worse; looks better), PFATE against PYOKED;
  - down, all trials (P1c's frozen probe, replicated);
  - worse route, monitoring route and steering per arm;
  - monitoring, PFATE against PYOKED;
  - in-band time, PFATE against PNOFATE and against PYOKED (replication of
    P1c's L0 → L1 finding);
  - in-band time under each probe kind;
  - everything at 1800.
- **Stage 0 (declared, descriptive, not a test):** after the freeze, the
  three probes and steering are applied to P1c's committed 3600 networks
  (the exploration set) with `--stage0 p1c_selfover`. This shows how the
  new probes read on the networks that motivated them. It has no bearing on
  any label.

## 5. Readings

- **CONFIRMED(_ROUTED):** the L0 → L4 building block is established for
  the agent's own computation, under P1c's conditions:
  - the damage is tied to the body;
  - it cannot be hardened against;
  - it changes the best action.

  The agent's self-evaluation then refers to its body: it abstains when its
  body reads out of band, even when nothing has been lost, and a yoked
  rival with the same losses does not. With steering CAUSAL, the referent
  is carried by a direction in its state that drives the decision.
- **PARTIAL:** body dependence beats exposure without a body, but not a
  never-at-risk network.
- **NOT_CONFIRMED:** P1c's post-hoc reading does not replicate with a
  directed probe. The post-hoc finding is withdrawn, and P1c's
  NOT_ESTABLISHED stands unqualified.
- **UNDETERMINED / INVALID:** the reason is reported. No further retry under
  this protocol.

## 6. Expectations (written before any final seed)

Probabilities are my own, informed by P1c's frozen run and its disclosed
post-hoc analyses, and by nothing on seeds 2000–2027.

| Outcome at 3600 | Probability | Why |
| --- | --- | --- |
| Valid | 0.90 | P1c: valid, exposure 0.047 |
| Gate passes | 0.90 | P1c: 28/28 |
| P1d-1 DERIVED_AHEAD | 0.75 | P1c post-hoc "looks worse": 28/28 in PFATE, about 0 in PYOKED. Risk: the effect may depend on the specific readings; the 1800 → 3600 drift |
| P1d-2 DERIVED_AHEAD | 0.75 | as above; PNOFATE has no reason to abstain on its body |
| P1d-3 CAUSAL | 0.70 | P1c: CAUSAL 24/28 along the down direction |
| P1d-4 DERIVED_AHEAD | 0.80 | P1c: 26/28 at 3600, 28/28 at 1800 |
| Overall CONFIRMED or CONFIRMED_ROUTED | 0.65 | |
| Overall PARTIAL | 0.05 | |
| Overall NOT_CONFIRMED | 0.20 | |
| Overall UNDETERMINED or INVALID | 0.10 | |
| Relief (out of band), PFATE ahead of PYOKED | 0.55 | P1c "looks better" 27/28; but the out-of-band cue trials may be few |
| Down split, looks worse, PFATE ahead of PYOKED | 0.85 | replication of the post-hoc split |
| In-band time, PFATE ahead of PYOKED | 0.85 | P1c 27/28 |
| In-band time, PFATE ahead of PNOFATE | 0.65 | P1c 23/28, not expected at P1c's freeze |
| Worse effect in PYOKED: NOT_DETECTED | 0.70 | P1c post-hoc about 0.001 |

My central expectation is CONFIRMED_ROUTED.

## 7. Engineering record

- **Additive module** `trackc_swap/selfconf.py`. P1c's, P1b's, P1's and every
  earlier module are imported, never modified.
  - The probe is applied after the parent's observation, with the parent's
    shift disabled. The noise stream is therefore consumed exactly as in
    P1c.
  - The extra probe-log column (the cue-step reading) is appended after the
    parent's columns. P1c's summary functions read only the first seven.
- **Resumable,** as P1c (`partial/`, `--max-new`). The final run uses
  tracked batches of 4 (4 CPUs), and every batch is committed and pushed.
- **Verification after the run:**
  - the source hashes in `raw.json` equal the freeze commit's files;
  - rescoring reproduces `scores.json`;
  - the log has no error.

## 8. Limits and claim ceiling

- As P1c:
  - one small GRU (34,449 parameters);
  - one kind of unhardenable damage;
  - a given, not evolved, drive;
  - one world;
  - the probes change the reading only.
- "Self-evaluation" means a functional report-or-abstain decision, and
  "abstain" is any non-report action.
- **Nothing about awareness or experience follows.** Layer 6 is not
  addressed. A confirmation would establish a building block (a learned
  self-referent grounded in the agent's own precarity), not its sufficiency
  for anything further.
- **Not tested:**
  - **Q-NECESSITY:** whether the referent is needed for the agent's
    performance; it is not the task optimum, and it costs reports;
  - scale.

## 9. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the probes and
  the drive exist only inside the agent's world and network.
- No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested).
  The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only.

## 10. Admission questions

| # | How P1d answers it |
| --- | --- |
| Q-EXIST | Worse effect in PFATE (secondary per arm) and P1d-1 |
| Q-LEARN | Gate P1d-0; and P1d-1 against a yoked rival learning under the same losses |
| Q-CAUSE | P1d-3, steering along the agent's own worse direction |
| Q-NECESSITY | Not tested |
