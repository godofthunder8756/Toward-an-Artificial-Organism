# Artificial organism research — v0.3

Current ACI research starts with the [constitution v3](ACI_RESEARCH_CONSTITUTION_v3.md),
[research tree v5](ACI_MASTER_RESEARCH_TREE_v5.md), and
[evidence index v5](EVIDENCE_INDEX_v5.md). The historical
[agent guide](NEW_AGENT_GUIDE.md) preserves earlier assignments; its reproduction
commands are not current experiment authorization.

Prospective ACI work is governed by the
[research constitution v3](ACI_RESEARCH_CONSTITUTION_v3.md), which separates
causal organizational role, functional necessity, and engineering advantage.
The [bounded A6 effort closed UNRESOLVED](A6_GATE_DECISION_v1.md).
The shared R9 existence question remains open; no neural training is authorized.
[Exact gate reduction](A6_GATE_REDUCTION_v1.md) certifies that eight-symbol
unrestricted capacity suffices, without certifying the coupled deployed family.
The [synthesis](ACI_RESEARCH_SYNTHESIS_v1.md) and
[next human decision package](ACI_NEXT_EXPERIMENT_DECISION_v1.md) move the program
to an identifiable first-order question. No organism restart, new architecture
construction or consciousness claim is authorized.

## Methodology review v1 (2026-11-18, synthesis)

[ACI_METHODOLOGY_REVIEW_v1.md](ACI_METHODOLOGY_REVIEW_v1.md) reviews the
Track C swap line against the seven layers. It finds that the line
established Layer 0 → Layer 1 sufficiency but no Layer 1 difference an
accurate evaluator cannot buy, and that it tested the arrow G1 predicted to
be weakest. It proposes a prediction-first method, a ranked register of
decisive predictions led by Layer 0 → Layer 4 self-evaluation (P1), and a
brief assessment of the PI's
[self-state / viability-boundary architecture](docs/proposals/self_state_viability_architecture_2026-11-18.jpg).
No experiment is authorized by it.

P1 (Layer 0 → Layer 4 self-evaluation) was authorized by the PI on
2026-11-18. [P1_SELFEVAL_DESIGN_v1.md](P1_SELFEVAL_DESIGN_v1.md) holds the
analytic stage ([results](p1_selfeval_analytic/REPORT.md): the body-as-referent
signature exists in the optimal fate agent at 36 of 36 grid points and is
exactly absent in host and paid rivals), a descriptive check on stored
agents, the proposed neural design with RTSS arms, and the power check.
The neural study is frozen in [P1_SELFEVAL_PROTOCOL.md](P1_SELFEVAL_PROTOCOL.md)
(`trackc_swap/selfeval.py`, `run_p1_selfeval.py`). Four calibration rounds
are disclosed in [`p1_selfeval_calibration/`](p1_selfeval_calibration/).
- Calibration found that the RTSS network under its own fate rarely learned
  to regulate: 2 of 12 seeds, against 12 of 12 for a plain GRU.
- So the plain network carries the primary test: PFATE against a paid
  "panic"-loss rival (PLOSS) and a yoked rival (PYOKED), with RTSS-FATE as a
  secondary arm.
- Final run: 28 seeds, verified against the freeze.
  [P1_SELFEVAL_RESULTS.md](P1_SELFEVAL_RESULTS.md) gives the outcome:
  **REFERENT_SUPPORTED_ROUTED**, not weak after Holm.
  - The agent whose memory depends on its own body learns to abstain when
    shown a false low body reading. Its drain effect is 0.051, against 0.001
    for the paid rival (20/23 usable pairs) and −0.000 for the yoked rival
    (24/28).
  - Neither rival does this, though both regulate and judge the evidence
    as well.
  - Steering the agent's recurrent state along its own drain direction
    reproduces the effect (23/28).
  - The effect is small, about 9% of the analytic optimum.
  - The RTSS self-state loop again regulated rarely (7/28), so it is
    untested among regulators.
  - The container was reclaimed three times during the run; each restart
    resumed and is disclosed.

**P1b (precarious computation, run 2026-11-20): NOT_ESTABLISHED.**
[P1B_SELFCOMP_PROTOCOL.md](P1B_SELFCOMP_PROTOCOL.md) moves the precarious
part inside the agent.

- There is no register: the agent holds the cue in its own recurrent state,
  and noise whose size follows its own body (the swap line's D19 rule)
  disturbs that state.
- A state-monitoring route is therefore possible alongside the body route.
- Every arm has the same innate homeostatic drive, so Layer 1 is equal
  across arms.
- Primary test: does the agent whose computation depends on its own body
  (PFATE) abstain on a false low body reading more than a rival with the
  same noise not tied to its body (PYOKED) and a never-noised rival
  (PNOFATE)? Steering is the mechanism check.
- Six calibration rounds and two engineering checks are disclosed in
  [`p1b_selfcomp_calibration/`](p1b_selfcomp_calibration/). Along the way,
  calibration found a death spiral: a fate on all computation without a
  drive.
- **Result** ([P1B_SELFCOMP_RESULTS.md](P1B_SELFCOMP_RESULTS.md)):
  **NOT_ESTABLISHED**, the central expectation written at the freeze.
  - Valid, gate passed, 19 usable pairs. The drain effect is about zero in
    every arm (PFATE vs PYOKED 7/17; vs PNOFATE 14/27; steering 10/26).
  - Post-hoc (disclosed): with the drive, natural noise left clear-trial
    errors at 7%, below the 20% at which abstaining pays (+1 / −4), so a body
    route had nothing to earn.
  - Both noised arms instead became *robust* to the noise (probe accuracy
    0.84–0.87 vs 0.67 for the never-noised arm), not self-monitoring.
  - Lesson: precarity is answered first by hardening. A body referent can
    form only where hardening is insufficient and the body changes the best
    action.
  - Recommended next step (for the PI): precarity that robustness cannot
    absorb.

**P1c (unhardenable precarious computation, frozen 2026-11-20).**
[P1C_SELFOVER_PROTOCOL.md](P1C_SELFOVER_PROTOCOL.md) follows P1b's lesson.

- With a probability set by its body, the agent's whole recurrent state is
  overwritten by another agent's state, so no hardening can keep the held
  value. This is P1's corruption rule, applied to the agent's own
  computation: p = min(0.3, 1.0 × gain) per step.
- A new validity condition requires that PFATE meets clear trials on which
  abstaining pays.
- Arms and tests as in P1b. P1c-1 (PFATE against PYOKED) runs over all
  seeds.
- Four calibration rounds are disclosed in
  [`p1c_selfover_calibration/`](p1c_selfover_calibration/).
- **Result** ([P1C_SELFOVER_RESULTS.md](P1C_SELFOVER_RESULTS.md)):
  **NOT_ESTABLISHED** at 3600, the central expectation written at the freeze.
  - Valid, gate passed 28/28. Drain effect PFATE vs PYOKED and vs PNOFATE
    18/28 each; steering CAUSAL (24/28). At 1800 all three passed (20/28,
    20/28, 23/28) and then faded.
  - Pre-registered secondary: with the same drive, PFATE keeps its body in
    band more than both rivals (0.947 vs 0.856 and 0.892; 27/28, 23/28).
    Precarious computation recruits regulation (L0 → L1).
  - Post-hoc (disclosed): the frozen drain is one-sided, but the fate is
    two-sided, and the probe pushed bodies above the band. Split by the
    pre-drain reading, PFATE abstains more when the drain makes its body
    look worse (+0.16, 28/28) and less when it looks better (−0.15, 27/28).
    PYOKED does not move (about 0.001). In natural running, PFATE abstains on
    low-reliability trials far more than PYOKED (0.27 vs 0.15, 26/28).
  - Recommended next step (for the PI): the one allowed post-hoc
    confirmation, on fresh seeds with a two-sided, pre-registered probe.

**P1d (confirmation of P1c's post-hoc finding, run 2026-11-20):
CONFIRMED_ROUTED.** [P1D_CONFIRM_PROTOCOL.md](P1D_CONFIRM_PROTOCOL.md) was
frozen before any final seed. It uses P1c's training unchanged on 28 fresh
seeds, with probes whose direction is fixed in advance: "worse" always moves
the shown body reading away from the band centre, and "relief" moves it
toward the centre.

- **Result** ([P1D_CONFIRM_RESULTS.md](P1D_CONFIRM_RESULTS.md)):
  **CONFIRMED_ROUTED**, the central expectation written at the freeze.
  Natural discrimination: CONFIRMED.
  - Worse effect, PFATE vs PYOKED and vs PNOFATE: 28/28 each (0.242 vs
    0.002 and 0.000). Steering along PFATE's own worse direction: CAUSAL
    (21/28). Natural low-reliability discrimination: 26/28 (0.225 vs 0.132).
  - Two-sided: relief lowers PFATE's abstention on out-of-band bodies
    (26/28); P1c's drain split replicates (28/28 looks worse, 24/28 looks
    better). Rivals do not move.
  - Regulation replicates: PFATE in band 0.956 vs 0.851 (PYOKED) and 0.916
    (PNOFATE). Monitoring of an overwritten state is equal across arms.
  - **The program's first confirmed building block in which self-evaluation
    is grounded in the precarity of the agent's own computation.**
  - Recommended next step (for the PI): L0 → L3, whether the body-grounded
    self-state is globally available to a second, unrelated decision.

**P3 (L0 → L3: global availability, run 2026-11-21): GLOBAL_ROUTED,
UNGATED.** [P3_GLOBAL_PROTOCOL.md](P3_GLOBAL_PROTOCOL.md) adds two decisions
to P1c's world that are never trained while the body-linked damage is on:

- B, a second held-cue decision for which a body warning is relevant;
- C, a decision the body cannot affect.

Only A runs in the fate phase; B and C are kept working by safe rehearsal
(overwrite off). Three calibration rounds were run, blind to every B and C
effect, and a pre-treatment usability rule kept 19 of 28 seeds.

- **Result** ([P3_GLOBAL_RESULTS.md](P3_GLOBAL_RESULTS.md)):
  **GLOBAL_ROUTED, UNGATED**, against the central expectation written at the
  freeze (LOCAL).
  - The fated agent abstains when its body looks bad on B (19/19 vs both
    rivals; 0.041 vs 0.006 and 0.002), at about half its strength on A
    (transfer ratio 0.53), and equally on C (18/19; 0.043).
  - The rivals, with the same architecture, losses and rehearsal, do not.
  - B uses the spread state in natural running (15/19). Regulation
    replicates (19/19 vs both).
  - Steering along A's direction moves B (15/19, CAUSAL). Post-hoc this
    routing is fragile: the same direction is no better than random on A
    itself.
  - **The program's first Layer 3 result:** the body-grounded self-state is
    a global state of the agent, but undifferentiated, more like a global
    affective tone than a content-specific self-model.
  - Recommended next step (for the PI): P3b, differentiation (a second,
    separate precarity for B).

## Grounding analysis G1 (2026-11-10, analytic)

[GROUNDING_ANALYSIS_v1.md](GROUNDING_ANALYSIS_v1.md) asks what makes a body
variable matter to a system and not only to its evaluator, in an exact finite
model whose [protocol](GROUNDING_PROTOCOL_v1.md) was frozen before the run.
Dependence of the system's own memory on the variable does; a homeostatic
reward and a terminal state do not. It carries design consequences for Track C
H3/H4. [RWM_DESIGN_v1_REVIEW_1.md](RWM_DESIGN_v1_REVIEW_1.md) retracts one
finding of the RWM card and narrows its verdict.

Track C follow-up (design only):
[objective-swap amendment A1](docs/trackC/trackC_amendment_A1_objective_swap_v1.md)
adds the degradation-only cell with task rewards as the test of derived
regulation. [G1 erratum 1](GROUNDING_ANALYSIS_v1_ERRATUM_1.md) corrects a
mislabelled arm.

**[Swap erratum 1](TRACKC_SWAP_ERRATUM_1.md) (2026-11-12) applies to every
swap run from v2 to v8 below.** In each scaffolded pair, the fate and yoked
agents shared Adam optimizer state, so their learning was coupled. The main
result (fate agents regulate, yoked partners do not) is probably
conservative, but its rates under an ordinary optimizer are not yet known.
Option R is the first run with independent optimizers; options R2, R3 and
R4 confirm it on 28 further seeds each, option G in two further cells, and
option T over three times the training, and option G2 in the
two-variable cell to 14 400 updates; option W found no difference in
what the two arms' states hold, and option B no benefit of the derived
objective when the world changes.

First Track C training run (2026-11-10):
[objective-swap results](TRACKC_SWAP_RESULTS_v1.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v1.md). Derived regulation did not
emerge in this learner at any noise dose.

Second run, a 2×2 of scaffolded start × graded gain:
[results v2](TRACKC_SWAP_RESULTS_v2.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v2.md). Regulation emerged in no cell.
Scaffolded agents learned to absorb the noise ("ARMOURED") instead of
regulating, which points to the additive noise form as the obstacle.

Third run, erasure-type fate with a scaffolded start:
[results v3](TRACKC_SWAP_RESULTS_v3.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v3.md). Regulation again did not emerge.
The skill stayed intact, but no agent found the multi-meal schedule that
erasure makes valuable, so discovery is now the leading obstacle.

Fourth run, the same with a gentler maintenance duty (wear 0.005 → 0.001):
[results v4](TRACKC_SWAP_RESULTS_v4.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v4.md). Regulation did not emerge
(one cell PARTIAL, three NO_EMERGENCE). For the first time, agents ate more
and stayed in band longer than their yoked partners, in all four cells and
not under the null objective. The difference was about a third to two-thirds of the margin
and still growing when the budget ended.

Fifth run, the same with three times the phase-2 budget:
[results v5](TRACKC_SWAP_RESULTS_v5.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v5.md). The frozen emergence rule was
met in no cell (one PARTIAL, one NO_EMERGENCE, two ARMOURED). In the SAT,
rate 0.3 cell, six of nine agents learned to keep their energy in band, timed
to need, without being paid for it. They were in band up to 0.94 of the time,
against at most 0.51 for their yoked partners. Elsewhere agents made their
memory robust to erasure instead. This per-agent finding was made after the
run and needs confirmation on fresh seeds.

Sixth run, a confirmation of that cell on 18 fresh seeds, under a per-agent
regulator criterion frozen in advance:
[results v6](TRACKC_SWAP_RESULTS_v6.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v6.md). **CONFIRMED.** Seven of 18
fate agents regulated their energy, in band 0.66–0.90 of the time and eating
3–17 times more often when low than when high, against 0 of 18 yoked partners
and 0 of 18 agents under the control objective. This is the program's first
pre-registered positive result on derived regulation, limited to this cell.
All 11 other agents made their memory robust to erasure instead (Spearman
−0.95 between the two), so the dependence must not be bypassable. Final
weights are saved for identifying the bypass (option K).

Option K, step 1: locating the bypass in v6's saved agents, with no training:
[results](TRACKC_BYPASS_DIAG_RESULTS.md), with its
[frozen protocol](TRACKC_BYPASS_DIAG_PROTOCOL.md). The frozen verdict is
NOT_IDENTIFIED, because the test of external storage was too strict. The data
are clear, though. Every bypass agent walks to a place that encodes the cue
and reads it back from the walls it sees: shuffling the wall inputs removes
most of its erasure robustness, while food and interoception carry nothing.
Step 2 (erasure also relocates the agent) was then run on the PI's decision.

Seventh run, option K step 2, the same four cells as v5 on fresh seeds, with
every erasure now also moving the agent to a random cell:
[results v7](TRACKC_SWAP_RESULTS_v7.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v7.md).
- **The primary test passed: 8 of 9 fate agents regulate** in the cell where
  v6 found 7 of 18, with the bypass closed. A second cell (GRADED, `r` = 0.3)
  went from 0 of 9 in v5 to 6 of 9. Across all four cells, 21 of 36 agents
  regulate, against 6 of 36 in v5, while 0 of 54 yoked or control agents do.
- With the position bypass closed, regulation became the rule. The competing
  route is what held v6's rate down.
- **The `r` = 0.1 cells were labelled "bypass open"** by a threshold that was
  set for `r` = 0.3. Every agent there scores exactly what internal memory
  alone predicts. SAT `r` = 0.1 has 7 of 9 regulators, which is descriptive
  only. Correcting that label is post hoc.

Eighth run, option M, a confirmation of v7's open cells on fresh seeds. Each
cell had a non-memory control at the same gain and rate, and a bypass check
matched to the erasure rate:
[results v8](TRACKC_SWAP_RESULTS_v8.md), with its
[frozen protocol](TRACKC_SWAP_PROTOCOL_v8.md).
- **Both claims were CONFIRMED, each with 9 of 9 regulators:** SAT `r` = 0.1
  and GRADED `r` = 0.3. Both cells had 0 of 9 in v5, while the bypass was
  open.
- GRADED `r` = 0.1, where erasure is weak and continues in band, has 3 of 9.
- Pooled over v7 and v8, the confirmed cells stand at 16 of 18 and 15 of 18.
  No yoked partner or control agent has regulated (0 of 108).
- For this learner and world, derived regulation is the rule wherever the
  dependence cannot be routed around and leaving the band costs enough.

Option P: probing the saved v7 and v8 agents, with no training:
[results](TRACKC_PROBE_RESULTS.md), with its
[frozen protocol](TRACKC_PROBE_PROTOCOL.md).
- Regulators' states carry a better current estimate of E than their delayed
  interoceptive input. Part of the reason is that they anticipate the effect
  of their own eating: they lead their yoked partners in 41 of 42 pairs, by
  about 2.6×.
- Scrambling interoception abolishes the eat timing in all 42 regulators.
  This is descriptive: the frozen test of that question was one agent short
  and is UNDETERMINED.
- Yoked partners, whose E does not matter to them, still encode E almost as
  strongly. What fate added is the use of E and the anticipation, not the
  representation itself.
  ([Erratum 1](TRACKC_PROBE_ERRATUM_1.md) corrects a description; no number
  changes.)

Route check requested by the PI:
[TRACKC_ROUTE_ASSESSMENT_v1.md](TRACKC_ROUTE_ASSESSMENT_v1.md). The swap line
has firmly established that dependence produces regulation. The thesis's own
claim, that grounding by dependence matters for what sits above it, has not
been tested yet. The deciding experiment is derived against paid regulators
(option R).

Option Q: causal probes of the saved regulators, with no training:
[results](TRACKC_CAUSAL_RESULTS.md), with its
[frozen protocol](TRACKC_CAUSAL_PROTOCOL.md).
- **Regulation is a closed loop through interoception (holds).** Under their
  own fate, 42 of 42 regulators regulate, and none does with interoception
  scrambled.
- **Anticipation is used, but weakly (frozen claim fails, 26 of 42).** Every
  regulator is less ready to eat after a meal it has not yet sensed, by a
  median 13%.
- **Erasure that tracks E adds little as a signal (frozen claim fails, 22 of
  42).** Erasure of any kind raises in-band time slightly.

Option R: derived against paid regulators, the first run with independent
optimizers: [results](TRACKC_PAID_RESULTS.md), with its
[frozen protocol](TRACKC_PAID_PROTOCOL.md). SAT, `r` = 0.3, 18 fresh seeds.
- **Derived regulation holds without the optimizer coupling (R0).** 18 of 18
  derived agents regulate (0.92 in band) and 0 of 18 yoked agents do. For this
  cell the coupling of erratum 1 had weakened the result.
- **A paid regulator reproduces most of what P and Q found.** Paid agents,
  matched for in-band time, also anticipate, suppress eating after a meal and
  need interoception. They are equally robust to world shifts (R3: no
  difference).
- **Derived agents are ahead on one of three measures (R1, anticipation: 13
  of 16, p = 0.021).** This is the first direct support for the thesis's
  claim, and it is weak: one uncorrected test of three, and it changes with
  the seed set. Post-meal suppression misses its bar by one seed (R2).
- **Each regulation lasts only while its ground does (R4).** Regulation is
  lost in 16 of 16 seeds when the dependence is removed, and in 16 of 16 when
  the payment is removed. Derived regulation goes faster (post hoc).
- **Post hoc:** 7 of 18 derived agents regulate through where they go, with
  no gating of the eat action. No paid agent does.

Option R2: replication of R on 28 fresh seeds, with a relocation control:
[results](TRACKC_PAID2_RESULTS.md), with its
[frozen protocol](TRACKC_PAID2_PROTOCOL.md).
- **Derived regulation is confirmed again (C0).** 28 of 28 derived agents
  regulate and 0 of 28 yoked agents do.
- **R1 did not replicate (C1, primary).** Derived agents are ahead on the
  anticipation index in 12 of 17 pairs (p = 0.14). The thesis keeps no
  support from the state measure.
- **R's post-hoc observation replicated as two pre-stated claims.** After a
  meal they have not yet sensed, derived agents hold back from getting
  another more than matched paid agents do (C3: 21 of 23 pairs, p = 0.0001).
  Eleven of 27 derived agents regulate through where they go, against 1 of
  27 paid (C2: p = 0.002). Both pass after Holm adjustment.
- **Relocation does not explain it (C4).** A paid agent whose relocations
  follow its own body state behaves like any paid agent.
- **Open:** whether the difference comes from the dependence of memory on
  the body state or from the absence of payment. A derived agent that is
  also paid would decide it.

Option R3: a derived agent that is also paid, and a sparse payment, on 28
fresh seeds: [results](TRACKC_PAID3_RESULTS.md), with its
[frozen protocol](TRACKC_PAID3_PROTOCOL.md).
- **Derived regulation is confirmed a third time (E0).** 28 of 28 derived
  agents regulate and 0 of 28 yoked agents do.
- **R2's behavioural difference replicated again (E1).** Derived agents have
  the higher post-meal suppression index K in 23 of 24 pairs (0.90 against
  0.50).
- **An agent that is both dependent and paid behaves like a derived agent
  (E2, primary: DEPENDENCE_SUFFICES).** It is above the paid agent in 21 of
  23 pairs (p < 0.0001) and not below the derived agent. The payment does
  not prevent the behaviour.
- **A rare, random payment with erasure's statistics gives a paid agent's
  solution (E3: SPARSE_NOT_SUFFICIENT).** It is above the dense payment in
  14 of 24 pairs (p = 0.54); derived agents are above it in 20 of 25
  (p = 0.004).
- Both labels hold after Holm adjustment. The protocol named this pair in
  advance as the strongest support for the thesis available at this scale.
- **One alternative remains.** Every arm without the behaviour had its
  memory erased at times set by another agent's body. A paid agent with
  undisturbed memory has not been run, so the difference could still be a
  cost of replayed erasure and not something the dependence adds (option
  R4).

Option R4: a paid agent with undisturbed memory, and a derived agent with
added replayed erasures, on 28 fresh seeds:
[results](TRACKC_PAID4_RESULTS.md), with its
[frozen protocol](TRACKC_PAID4_PROTOCOL.md).
- **Derived regulation is confirmed a fourth time (F0).** 28 of 28 derived
  agents regulate and 0 of 28 yoked agents do.
- **The behavioural difference replicated a third time (F1).** Derived
  agents have the higher K in 22 of 25 pairs (0.88 against 0.53); 81 of 88
  pairs over the four runs.
- **R3's open alternative fails (F2, primary: REPLAY_DOES_NOT_EXPLAIN).** A
  paid agent whose memory is never erased is not above the ordinary paid
  agent (6 of 20; K 0.37 against 0.53), and derived agents are above it in
  17 of 19 (p = 0.0007; holds after Holm adjustment). Most such agents do
  not hold back after an unsensed meal at all. The paid agents' low K was
  not a cost of replayed erasure.
- **A derived agent given the paid agent's erasures on top of its own shows
  less of the behaviour (F3: REPLAY_REMOVES, weak).** Derived agents are
  above it in 14 of 18 (p = 0.031; 0.093 after Holm adjustment). The arm is
  erased 2.4 times as often and regulates less tightly, and its K tracks its
  regulation, so amount of erasure, its timing and looser regulation are not
  separated.
- The anticipation index, which started this line in option R, shows no
  direction here (10 of 19) and no longer separates the arms.
- Still one behaviour in one small world with one learner; the mechanism is
  not known.

Option G (generality): the derived, yoked and paid arms in two new cells, a
128-unit learner (H128) and a two-variable body (B2), 28 fresh seeds each:
[results](TRACKC_GENERAL_RESULTS.md), with its
[frozen protocol](TRACKC_GENERAL_PROTOCOL.md).
- **Derived regulation extends to both cells (G0).** 28 of 28 derived
  agents regulate and 0 of 28 yoked agents do, in each cell.
- **The behavioural difference is found with the larger learner, smaller
  (G1, H128: DERIVED_AHEAD).** Derived agents have the higher K in 19 of 25
  pairs (p = 0.015; 0.91 against 0.77). The median difference is 0.12,
  against 0.24 to 0.40 in the base cell, because paid agents' K rose.
- **It is not found with a two-variable body (G1, B2:
  NO_DIFFERENCE_DETECTED).** Paid agents have the higher K in 17 of 25
  pairs (p = 0.11; 0.88 against 0.85). The cell also has twice the items
  and three times the training, so the run does not say which change
  matters.
- **Most of the post-meal suppression in B2 is not specific to the variable
  that was fed,** in either arm. What K measures is less clear than R2 to
  R4 assumed.
- Overall label: HOLDS_IN_H128_ONLY. The downstream claim is narrower than
  R2 to R4 suggested: paid agents can acquire the behaviour, and how far
  they do depends on the cell. The run was interrupted once and resumed
  from its finished jobs.

Option T (training length): the base cell unchanged, derived, yoked and
paid arms on 28 fresh seeds, trained to 10 800 updates (three times the
base length) and measured at 3600, 7200 and 10 800:
[results](TRACKC_LENGTH_RESULTS.md), with its
[frozen protocol](TRACKC_LENGTH_PROTOCOL.md).
- **Derived regulation lasts (T0).** 28 of 28 derived agents regulate at
  every point and 0 of 28 yoked agents do.
- **The behavioural difference replicated a fifth time at the base length
  (T1: DERIVED_AHEAD).** At 3600 updates derived agents have the higher K
  in 24 of 26 pairs (0.87 against 0.53).
- **It is gone at three times the training (T2: NO_DIFFERENCE_DETECTED).**
  At 10 800 updates derived agents have the higher K in 13 of 27 pairs
  (0.93 against 0.94); the interval for the median difference is −0.06 to
  0.04.
- **It closed from the paid side (T3: NARROWS).** The within-pair
  difference is smaller at the end in 24 of 25 seeds (p = 0.000002). Paid
  agents' median K went from 0.53 to 0.89 to 0.94.
- Overall label: CLOSES. The downstream difference of R2 to R4 is a stage
  of learning: derived agents come to hold back after a meal sooner, and
  paid agents get there with more training. Nothing in the swap line now
  shows a lasting behavioural difference between a derived and a paid
  regulator. The expectation written before the run was that the
  difference would persist (about 40%, against about 15% for this label).

Option G2 (specificity): option G's two-variable cell unchanged, derived,
yoked and paid arms on 28 fresh seeds, measured at 3600, 7200, 10 800
(primary) and 14 400 updates; the claim is option G's post-hoc contrast,
fixed in advance: [results](TRACKC_SPECIFIC_RESULTS.md), with its
[frozen protocol](TRACKC_SPECIFIC_PROTOCOL.md).
- **Derived regulation holds (S0).** 27 then 28 of 28 derived agents
  regulate; 0 of 28 yoked agents do. Paid agents regulate sooner (28 of 28).
- **Derived regulators' post-meal suppression is more specific to the
  variable that was fed (S1: DERIVED_AHEAD).** Own-meal K minus other-meal
  K is larger in the derived agent in 19 of 23 pairs at 10 800 (p = 0.003;
  0.18 against 0.07), with K itself equal.
- **Still there at 14 400 (S2: DERIVED_AHEAD),** in 21 of 25 pairs, with no
  detectable change (S3). Paid agents hold back almost as much after a meal
  of the other kind; at 14 400 their K is slightly the higher.
- Overall label: PERSISTS (not weak). This is the swap line's first
  evidence of a difference in content where K does not favour the derived
  arm. It is a difference of degree; both arms grow more general with
  training, and the pre-stated stage-matched check did not detect a
  difference (18 of 28), so a stage account is not excluded. The run was
  interrupted twice by container restarts and resumed.

Option W (mechanism, no training): the 336 stored two-variable agents of
options G and G2, probed as their behavioural runs probed them; a linear
decoder asks how much the hidden state adds, beyond the agent's inputs,
about which variable was eaten 2-5 steps ago:
[results](TRACKC_MECHANISM_RESULTS.md), with its
[frozen protocol](TRACKC_MECHANISM_PROTOCOL.md).
- **Both arms' states remember which variable was just fed, equally**
  (about 0.2 bits beyond the inputs; derived higher in 13 of 23, 15 of 25
  and 14 of 25 pairs in the three sets). Yoked agents' states do not.
- The memory covers exactly the five steps before the delayed readings
  show the meal, in both arms.
- Overall label: READ_OUT. The difference of options G and G2 is in how
  the policy acts on a memory both arms share, not in what the state
  holds. Every probe reproduced its behavioural run's trajectory.

Option B (benefit, no training): the 252 stored two-variable agents of
options G and G2, with erasure off, in the base world and four fixed
variants (wear doubled or tripled; fewer or more items):
[results](TRACKC_BENEFIT_RESULTS.md), with its
[frozen protocol](TRACKC_BENEFIT_PROTOCOL.md).
- **No benefit of the derived objective when needs rise.** With wear
  doubled both arms lose about a sixth of their in-band time; derived
  agents lose slightly more (B1: derived ahead in 6 of 23 pairs,
  p = 0.035; the same direction, not detected, in the other two sets).
- Paid agents cope better when items are scarcer (all three sets); derived
  agents cope slightly better when items are denser (all three sets).
- Overall label: COST, weak (B1 does not survive Holm adjustment). Paid
  agents eat more when their readings say they need to. Across the swap
  line, no difference between derived and paid regulators has been shown
  to benefit the agent.

## RWM design card (2026-11-01, design only)

[RWM_DESIGN_v1.md](RWM_DESIGN_v1.md) specifies a recurrent workspace /
higher-order monitor / metabolic perception-action architecture as discrete
logic-gate primitives, with exact integration (Phi_s) and causal-density
instruments and a pre-scale gate. Its result is NO_GO: the RWM-8 skeleton
has Phi_s = 0 on all closed-loop stationary mass. No training is authorized.
Reproduce with `python -m unittest test_rwm` and `python verify_rwm.py --out <new dir>`.

## Status at 2026-10-23 hand-off

Open pull requests #3 through #14 are brought onto this branch with merge
commits. The next team should start at
[docs/handoff_2026-10-23/](docs/handoff_2026-10-23/). The lead machine's
working tree and the literature search are in
[archive/local_workspace_2026-10-23/](archive/local_workspace_2026-10-23/).

E1a implements the behavioral and causal gate for acquiring a new maintenance
priority. A learned recurrent memory circuit requires precursor for its actual
recurrent connections. An ordinary online controller learns resource choices.
Read RESEARCH_NOTEBOOK.md for the findings and E1_PROTOCOL.md for the exact scope.

This is a scaffolded research benchmark, not an artificial living or conscious
system. It does not yet implement locally growing neural tissue. The main
controller receives an explicit net-energy-production objective.

## Reproduce E1a

Python 3 and NumPy suffice for training/replay. Matplotlib exports figures.
Actual tested versions are recorded in e1_results/run.json and
e1_results/analysis_environment.json. Run from this directory:

```bash
python -m unittest -v test_e1
python -m e1.experiment --config e1/frozen_config.json --out reproduced_e1
python analyze_e1.py reproduced_e1
python export_e1_figure.py reproduced_e1
python verify_e1.py reproduced_e1
```

The runner refuses to overwrite an existing directory. No GPU, pretrained
models, text dataset, online service, or network access is required. Setting
OPENBLAS_NUM_THREADS=1 can avoid small-matrix thread overhead. Runtime and exact
numerical reproducibility depend on hardware and numerical-library versions.

A short engineering run uses only two seeds:

```bash
python -m e1.experiment --feasibility --out new_feasibility
python analyze_e1.py new_feasibility
```

To observe a trained agent without retraining:

```bash
python replay_e1.py --results e1_results --seed 100 --variant neural_q --stage acquired --world 0 --out replay.csv
```

Other stages: pre, acute, dependency, rescue, sham, lost_usefulness.
Other variants: tabular_q, frozen_neural_q, fixed_drive_q.
Checkpoints load without pickle. Evaluation replay is supported; exact
mid-training resumption is not currently supported.

## Implementation

| File | Purpose |
| --- | --- |
| e1/circuits.py | Sparse recurrent circuit, rewarded exploration, BPTT and Adam |
| e1/environment.py | Fixed grid paths, cues, energy and connection conductance |
| e1/control.py | Neural/tabular Q learning, frozen and assigned-drive controls |
| e1/experiment.py | Paired branches, training, evaluation and checkpoints |
| e1/config.py, e1/frozen_config.json | Default and frozen configuration |
| E1_PROTOCOL.md | Objectives, budgets, gates and departures from developmental tissue |
| E1_FREEZE.json | Hashes recorded before final data collection |
| ENGINEERING_LOG.md | Feasibility findings and baseline correction |
| test_e1.py | Ten numerical, causal, information-leak and geometry tests |
| analyze_e1.py | Seed-level inference, tables and PNG/PDF figures |
| replay_e1.py | Saved-policy evaluation without training |
| verify_e1.py | Frozen-source, coverage and exact-checkpoint-replay audit |

## Evidence

- e1_results/RESULTS.md: all controller/condition means and paired contrasts.
- e1_results/summary.json: seed means, bootstrap intervals and frozen gates.
- e1_results/E1_RESULTS.png and .pdf: exportable research figure.
- e1_results/evaluation.csv: all 4,480 final evaluation episodes.
- e1_results/assays.csv: initial, learned, degraded, lesioned and restored recall.
- e1_results/budgets.csv: planned/realized experience and parameter counts.
- e1_results/run.json: configuration, source hashes, versions and runtime.
- e1_results/VALIDATION.json: data audit and 28 exact checkpoint replays.
- e1_results/seed_100 through seed_119: per-seed adaptation logs, evaluation
  and checkpoints. Seed-100/world-0 traces were selected before evaluation.
- e1_feasibility_v1 and e1_feasibility_v2: exploratory runs, excluded from the
  final sample. V1 also preserves its differing module source.

## Earlier E0 pilot

pilot.py and results/ preserve the original experiment. Its notebook remains
in history/RESEARCH_NOTEBOOK_v0_1.md.

```bash
python pilot.py --out reproduced_e0
```

E2 now partially implements that target in `e2/`: one maintained recurrent
network jointly learns resource choices and delayed recall while local edge
biomass develops under material constraints. See `E2_PROTOCOL.md`,
`e2_results/RESULTS.md`, and `E2_DIAGNOSTIC_PROTOCOL.md`.

E2 found history-sensitive resource preferences and lesion dependencies, but
activity-guided local growth was less reliable than a fixed structural target.
The current frontier is `E3_DESIGN.md`: preserving acquired neural information
without a protected perfect copy. E1a remains the ordinary-learning baseline.


## Repository layout

The repository is a research log with frozen, hash-checked artifacts, so files
are intentionally **not** relocated: scripts import each other as flat modules
and many results/protocols reference paths and hashes verbatim.
See [docs/REPOSITORY_MAP.md](docs/REPOSITORY_MAP.md) for a navigation guide by
filename prefix.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` lists the third-party libraries imported by the code
(NumPy core; Matplotlib for figures; PyTorch only for the `phase3*`/bridge work).
Run scripts and tests from the repository root, e.g. `python -m unittest -v test_e1`.

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing anything.
