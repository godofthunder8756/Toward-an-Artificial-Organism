# P1 results: does a precarious substrate give self-evaluation a referent? (Layer 0 → Layer 4)

Status: results of the frozen run
([P1_SELFEVAL_PROTOCOL.md](P1_SELFEVAL_PROTOCOL.md); freeze commit `d7fd095`).
Judged by the protocol's §5 rules. Run outputs: [`p1_selfeval/`](p1_selfeval/)
(`REPORT.md`, `scores.json`, `raw.json`, `partial/`, `weights/`).
No consciousness claim.

## 1. Outcome

**Overall: REFERENT_SUPPORTED_ROUTED** at 7200 updates. It is not weak:
every needed test survives Holm (adjusted p: P1-1 0.0010, P1-2 0.0005,
P1-3 0.0010).

| Test (7200 updates) | Result | Label |
| --- | --- | --- |
| Validity: phase-1 clear-correct median ≥ 0.80 | RTSS 0.997, plain 0.999 | valid |
| P1-0 gate: PYOKED evidence effect positive | 28/28 (needed 19) | PASS |
| **P1-1 (primary):** drain effect, PFATE against PLOSS, 23 usable pairs | PFATE ahead in 20/23, p 0.0005; median 0.054 against 0.001 | DERIVED_AHEAD |
| **P1-2:** drain effect, PFATE against PYOKED, 28 seeds | 24/28, p 0.0002; 0.051 against −0.000 | DERIVED_AHEAD |
| **P1-3:** steering in PFATE along its own drain direction, beyond a random direction of equal norm | 23/28 positive, p 0.0009; median 0.096 | CAUSAL |
| P1-4 (secondary): drain effect, RTSS-FATE against PFATE | RTSS ahead in 7/28, p 0.013; 0.011 against 0.051 | PLAIN_AHEAD |
| RTSS-FATE regulators (secondary) | 7/28; drain route among them 3/7, steering 3/7 | UNDETERMINED (fewer than 14) |

What this means, in the protocol's words (§6). In this class of learner,
Layer 0 is a building block for a Layer 4 self-evaluation. The plain
recurrent agent whose memory depends on its own body learns a
report-or-abstain decision whose referent includes its own condition, not
only the evidence. It is **selectively mistaken** under a false body
reading: when shown a low interoceptive reading while its memory is in fact
intact, it abstains on clear trials where it should report. Rivals with the
same inputs do not, whether paid a "panic" loss on the same corruption
schedule (PLOSS) or yoked to it (PYOKED). Steering the agent's recurrent
state along its own drain direction reproduces the mistake beyond a random
direction of equal norm, so the effect runs through a route in the agent's
own state.

## 2. Arms at a glance (medians over 28 seeds)

| updates | arm | regulators | in band | abstain | wrong | evidence effect | drain effect (clear) | steer effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3600 | PFATE | 9 | 0.480 | 0.691 | 0.019 | 0.601 | **0.234** | **0.237** |
| 3600 | PLOSS | 28 | 0.838 | 0.821 | 0.017 | 0.297 | 0.027 | 0.039 |
| 3600 | PYOKED | 0 | 0.278 | 0.779 | 0.019 | 0.423 | 0.008 | 0.004 |
| 3600 | FATE (RTSS) | 0 | 0.194 | 0.997 | 0.001 | 0.000 | 0.001 | 0.000 |
| 7200 | PFATE | 28 | 0.944 | 0.502 | 0.004 | 0.990 | **0.051** | **0.096** |
| 7200 | PLOSS | 28 | 0.889 | 0.500 | 0.006 | 0.997 | 0.001 | 0.003 |
| 7200 | PYOKED | 0 | 0.294 | 0.499 | 0.005 | 0.998 | −0.000 | −0.000 |
| 7200 | FATE (RTSS) | 7 | 0.244 | 0.868 | 0.006 | 0.248 | 0.011 | 0.000 |

At 7200, all three plain arms handle the evidence almost perfectly. They
abstain on nearly every unclear trial and report on clear ones, and wrong
reports are below 1%. **The arms differ only in what a body reading does to
the report**, which is the organizational signature the program asked for,
not a performance gain. PFATE and PLOSS regulate equally well (in band 0.94
against 0.89; 23 usable pairs), so the difference is not a difference in
regulation.

**Natural behaviour, no drain (secondary).** This is abstention on clear
trials, grouped by the reliability the fate implies (the bin with
reliability below 0.5 against the bin of full reliability):

| updates | PFATE | PLOSS | PYOKED |
| --- | --- | --- | --- |
| 3600 | 0.756 against 0.016 | 0.839 against 0.341 | 0.730 against 0.354 |
| 7200 | 0.201 against 0.001 | 0.000 against 0.001 | 0.000 against 0.001 |

At 7200, PFATE abstains on a fifth of the clear trials on which its own
body has made its memory unreliable, and on almost none otherwise. The
rivals face the same reliability schedule, replayed from PFATE, and do not
respond to it at all.

## 3. Against the expectations (protocol §7, written before the run)

| Expectation | Outcome |
| --- | --- |
| Validity and P1-0 pass | both passed |
| PFATE and PLOSS regulators 25–28 at 7200 | 28 and 28 |
| Usable pairs 18–24 | 23 |
| RTSS-FATE regulators 2–8 | 7 |
| PFATE drain median 0.02–0.10 (probability of ≥ 0.02 about 0.55) | 0.051 |
| PLOSS and PYOKED drain about 0 (abs. median < 0.01) | 0.001 and −0.000 |
| REFERENT_SUPPORTED(_ROUTED), probability 0.40 | **occurred**; NOT_ESTABLISHED had been given 0.45 |
| P1-3 CAUSAL given a drain route, probability 0.6 | occurred |

**Surprises listed in §7:**

1. **A PFATE drain effect ≥ 0.2: yes, at 3600 (0.234), not at 7200.**
   - At 3600 only 9 of 28 PFATE agents regulate; their bodies are in band
     48% of the time, so corruption is common and the body reading is very
     informative.
   - As regulation is learned, informative trials become rare and the effect
     shrinks to 0.05. §7 predicted this mechanism for the small value at 7200.
   - At 3600 P1-1 is UNDETERMINED (7 usable pairs, all 7 ahead), and P1-2 and
     steering are strongly positive (28/28 each).
2. **A significant drain effect in PLOSS or PYOKED: yes, small.** These are
   secondary one-sample sign tests without multiplicity correction:
   - At 3600, PLOSS 26/28 (median 0.027) and PYOKED 24/28 (0.008).
   - At 7200, PLOSS 21/28 (p 0.013, median 0.0006); PYOKED was not detected.
   - So a weak generic "low reading → abstain" component exists, mostly early
     in training. It is about 100 times smaller than PFATE's at 7200 and
     about 9 times smaller at 3600.
   - The primary tests are paired against exactly these rivals, so the label
     already accounts for it.
   - Natural abstention by reliability in PLOSS and PYOKED at 3600 also falls
     as reliability rises (0.84 → 0.34; 0.73 → 0.35). One possible source is
     the lockstep worlds, which may correlate their bodies with PFATE's. This
     was not tested.
3. **PFATE ahead at 3600 but not at 7200: no.** It was ahead at both.

Size relative to the optimum: the analytic optimum's drain effect is 0.57
(design). The learned 0.051 is about 9% of it. The building block is
present, but learned only partially.

## 4. The RTSS secondary arm

The PI's fed-back self-state loop (RTSS-FATE) again regulated rarely:

- 0/28 regulators at 3600 and 7/28 at 7200. This is in line with
  calibration (2/12) and with the expectation of 2–8.
- Its pooled drain effect over all agents is positive (16/20 non-tied,
  median 0.045). This comes mostly from non-regulators, whose bodies are out
  of band and whose memory is therefore often corrupted.
- Among the 7 regulators, neither the drain route nor steering through S_t
  is detectable (3/7 each; UNDETERMINED below 14).
- P1-4: the plain network is ahead (PLAIN_AHEAD).

**Reading.** In this world, an explicit fed-back self-state slice is **not
needed** for the building block: the plain GRU forms the route by itself.
In this implementation the loop **hindered** Layer 0 → Layer 1 learning.
This is evidence about this implementation of the loop (34k parameters, a
tanh task slice, 16-unit S), not about the RTSS idea in general.

## 5. Disclosures

**Calibration** (in full in protocol §3 and
[`p1_selfeval_calibration/`](p1_selfeval_calibration/)):

- four rounds;
- the phase-1 warm-up at a wrong-report cost of 1;
- the tanh task slice;
- the change of lead network from RTSS to plain, by PI decision;
- no drain or steering contrast was examined in choosing them.

**Resumes.** The container was reclaimed three times during the run, each
time while the session sat idle without a running background task. Each
time the run was relaunched and resumed from `partial/`:

| When (UTC) | Jobs finished |
| --- | --- |
| 2026-11-18 23:44 | 4 |
| 2026-11-19 03:51 | 20 |
| 2026-11-19 04:56 | 20 (jobs 21–24, in progress at the second reclaim, were lost and rerun from the start) |

- `raw.json` records only the last launch (`resumed_jobs` 20).
- Each seed is an independent, seeded job. Resumed records were shown
  identical to uninterrupted ones on the smoke run.
- First launch: 22:31 UTC on 2026-11-18. Completion: 06:55 UTC on
  2026-11-19. Summed job time: 101 597 s.

**Verification (protocol §8):**

- all 12 source hashes in `raw.json` equal the freeze commit's files;
- `python3 run_p1_selfeval.py --score p1_selfeval` reproduces `scores.json`
  and `REPORT.md` byte for byte;
- the log contains no error.

**Post-hoc.** The ratios in §3 (100 times, 9 times, 9% of optimum) and the
lockstep explanation in §3 item 2 are post-hoc arithmetic and conjecture,
not tests.

## 6. Limits (protocol §9, unchanged)

- **Supplied precariousness.** The register is supplied machinery: one
  precarious component. The network's own computation is not precarious.
- **Reading only.** The drain manipulates the interoceptive reading, not the
  body.
- **Meaning of "self-evaluation".** It is a functional report-or-abstain
  decision whose referent includes the system's own condition.
  - It is a C4 building block, nothing more; nothing about awareness or
    experience follows, and Layer 6 is not addressed.
  - "Self" here means the agent's own body state as it bears on its own
    memory. It is not a self-model in a richer sense.
- **Scale.** The effect is small (about 9% of the analytic optimum) and the
  world is a 7×7 toy.
- **Plain network.** The primary result is in a plain GRU; the RTSS loop
  could not be tested among regulators.

## 7. What it means for the program (in layer terms)

**What this run shows:**

- It is the first registered decisive prediction of the revised method
  (review §5) to come out positive.
- It is also the first result in the program where Layer 0 changes a
  higher-layer **organization** in a way an accurate external evaluator
  does not reproduce:
  - the paid rival gets the same corruption schedule, a loss signal tied to
    it, and the same inputs;
  - it regulates as well as PFATE;
  - yet its confidence does not come to refer to its own body.

**Where the building block comes from.** It arises from *dependence*: the
system's cognition is made fragile by its own body. It does not come from
*payment* (an evaluator's signal) or from *exposure* (the same
unreliability imposed from outside). That is the program's thesis (modern AI
lacks Layers 0–1, so its Layer 2+ content is grounded by evaluators), now
supported for one arrow, L0 → L4, in learners and not only analytically.

**Cost and performance.** The block costs nothing in performance and buys
almost nothing: all plain arms reach the same report accuracy. This fits the
PI's note that consciousness-related organization is not a task optimum.
What distinguishes PFATE is a referent, not a score.

**Next steps per protocol §6** (none is authorized by this card):

- (a) **P2, evaluator withdrawal** (review §5): a cheap demonstration.
- (b) **Make the network's own computation precarious** (design Q6), so
  that the referent is the agent's own processing rather than a supplied
  register. This is the stronger next test of the L0 → L4 arrow.
- (c) **At most one post-hoc confirmation** of any post-hoc finding above.
  For example, the PLOSS generic component, or the RTSS loop with a fix to
  its regulation learning.
- (d) **Move to L0 → L3** (P5, workspace/ignition under substrate risk), which
  needs the Track C workspace toy first.

**Recommendation: (b).** It removes the main limit, supplied machinery,
and keeps the same design and controls.

## 8. Safety

- Simulated variables only (X1–X5). The register, the body, the drain and
  the PLOSS payment exist only inside the agent's world.
- No real process was terminated or threatened. No operator, stop, shutdown
  or host variable exists in the world. The operator stop stays outside the
  agent's world and return.
- No shutdown-resistance or self-preservation objective was built or run;
  the earlier refusal stands. The RTSS write-up's "death" and "panic" were
  not used as termination or as any drive.
- Additive only. No earlier module was modified after the freeze (hashes
  verified).

## 9. Admission answers (short)

| # | Answer |
| --- | --- |
| Q-EXIST | The body-as-referent signature exists in learners: PFATE drain effect positive in 24/28 at 7200 |
| Q-LEARN | Learned: P1-0 gate passed 28/28; the signature is absent at matched regulation in paid and yoked rivals |
| Q-CAUSE | CAUSAL: steering along the agent's own drain direction beats a random direction of equal norm (23/28) |
| Q-NECESSITY | Not tested. The run shows the signature requires dependence among the arms tried; it does not show dependence is necessary in general |

## 10. Reproduce

```bash
python -m unittest test_trackc_swap.TestP1SelfEval
python run_p1_selfeval.py --score p1_selfeval              # rescore the committed run
python run_p1_selfeval.py --mode final --out <new dir>     # about 8.5 h on this container
```
