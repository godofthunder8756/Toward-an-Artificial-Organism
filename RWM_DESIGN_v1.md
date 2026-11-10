# RWM design card v1: recurrent workspace, higher-order monitor, metabolic perception-action loop

**DESIGN ONLY. ENGINEERING class. No training, no learner fit, no organism
restart and no consciousness claim is made or authorized by this card.**

Date 2026-11-01. Requested by the PI as a new architecture family; under
[constitution v3](ACI_RESEARCH_CONSTITUTION_v3.md) ("human authorization is
required for fundamentally new architecture families"), this card is the
design and pre-scale verification package. It is not a training protocol.
Everything here is exact enumeration on small discrete systems.

Package: [`rwm/`](rwm/), gate runner [`verify_rwm.py`](verify_rwm.py),
bounded search [`explore_rwm_gate_menu.py`](explore_rwm_gate_menu.py), tests
[`test_rwm.py`](test_rwm.py), outputs [`rwm_gate_v1/`](rwm_gate_v1/).

## 0. Result in one paragraph

The design is specified at two levels. At the neural level there are recurrent
populations with a low-dimensional workspace, a higher-order monitor and an
active-inference objective. At the discrete level the same topology is an
8-node logic-gate network, RWM-8, and the neural model's population
connectivity is that network exactly. RWM-8 passes the structural tests: it
is one strongly connected recurrent system, the workspace is a strict
bottleneck between the first-order modules, the workspace broadcasts to both
of them, and the monitor is higher-order with write-back. The
instruments are validated, and the objective is admitted: exteroceptive
prediction error alone selects the dark room, and adding the supplied
interoceptive setpoint selects foraging. RWM-8 **fails** the
integration tests. Its state-dependent system integration Φ_s is zero on all
of its closed-loop stationary mass, and on 78% of that mass the maximal
complex is the monitor pair {C, M} alone. **Verdict: NO_GO for scale
training.** A bounded search over a declared menu of semantic gates found no
admissible variant above 0.079 Φ_s-positive mass. That result is UNRESOLVED
for the class, not an impossibility proof.

## 1. Where this sits in the program

| Request element | Program node | Prior frozen evidence it must respect |
| --- | --- | --- |
| central bottleneck with global broadcast | C3 integration (Program B) | [Phase III verdict](PHASE3_VERDICT_v1.md): paid workspace reduced to sufficient-statistic broadcast; [Phase III-B](PHASE3B_VERDICT_v1.md): competitive workspace failed its comparative gate |
| recurrent feedback for internal state estimation | Program A first-order state | [decision package](ACI_NEXT_EXPERIMENT_DECISION_v1.md): ordinary Bayes/PSR filters are the reduction anchor |
| higher-order monitor of the primary network | C4 internal evaluation (Program C; human gate) | [AC117](AC117_RESULTS_v1.md): reliability monitor reduced to directional-repair control; [theory queue v2](docs/handoff_2026-10-23/review/c_axis_theory_queue_v2.md): distinct-evaluation conjunction |
| prediction-error objective with metabolic self-preservation | O-axis × C0 (Program O) | [Track B scope note](docs/handoff_2026-10-23/review/trackB_workspace_allostasis_scope_note_v1.md): exclusions X1 to X5 |
| integrated information / causal density before scaling | instrument, Q-EXIST | theory queue v2 §0: the unfolding argument covers only I/O-equivalent systems |

None of these elements establishes phenomenal consciousness, and neither does
their conjunction (constitution v3, "Two goals, no consciousness score").
Here Φ_s and causal density are structural diagnostics of a topology. They are
not consciousness meters.

## 2. Neural-level architecture

```
            oR (exteroceptive)                         oH (interoceptive, simulated energy)
               |                                          |
   +-----------v-----------+                  +-----------v-----------+
   | EXT  X  belief/pred.  |<-- efference --- | INT  I  error vs      |
   |      E  pred. error   |     A            |      SUPPLIED setpoint|
   |      A  action        |                  +-----------^-----------+
   +---^---------|-----^---+                              |  ^
       |  write  |     |                         write    |  | broadcast
       |         v     | broadcast                        |  |
   +---|-----------------------------------------------------|--+
   |   |   WS  G ignition (bistable)   K content (d_w << d_x) |  |   central bottleneck:
   |   +------------------------------------------------------+  |   the only EXT <-> INT route
   +-----------------------^-------------------------------------+
                           | gate (C -> G)
   +-----------------------|-------------------------------------+
   | MON  C monitor (predicts own first-order correctness)       |   higher-order: reads E,
   |      M meta-error = realized correctness - predicted        |   never reads oR/oH;
   +----- precision C -> X ------ evidence-seeking C -> A -------+   writes C -> X, G, A
```

Population updates, for every environment step, repeated `n_settle` times with
the observation clamped (recurrent settling replaces a single feedforward pass):

- `X <- (1-a) X + a tanh(sum_{i in in(X)} W_Xi h_i + U_X (pi * oR))`, where `pi = softplus(P_C C)`
  is the monitor-set sensory precision (**precision role**)
- `E = oR - V_X X` (exteroceptive prediction error; a fixed comparator)
- `A = softmax(W_AK K + W_AC C)` (action; the monitor adds evidence seeking)
- `I <- (1-a) I + a tanh(W_II I + W_IK K + U_I (oH - h*))`, where `h*` is the SUPPLIED setpoint
- `G = sigma(beta (w_GG G + w_GI I + w_GE E + w_GC C - 1/2))`, where a large `w_GG` makes it bistable (**ignition**)
- `K <- G * tanh(W_KI I + W_KX X) + (1 - G) * K` (gated write, hold and broadcast; `dim K = d_w`)
- `C <- (1-a) C + a tanh(W_CC C + W_CM M)` and `c_hat = sigma(v C)` (predicted own correctness)
- `M = 1[|E| < tau] - c_hat` (second-order prediction error)

Population j receives a weight block from population i **iff** (i → j) is an
effective edge of RWM-8. `RWMNet.population_edges() == rwm8().effective_edges()`
is a unit test, so the discrete gate below audits the same graph that a
trained model would have. [`rwm/neural.py`](rwm/neural.py) contains forward dynamics and
objective terms only. It has no optimizer, gradient or training loop, and a
test asserts that.

## 3. Discrete-primitive definition

**Primitives.** A gate is a truth table `g: {0,1}^k -> [0,1]` giving
`P(out = 1)`. The deterministic gates used are COPY, NOT, AND, OR, XOR, XNOR,
MAJ_k, MUX and weighted McCulloch-Pitts threshold units
`THR(w, θ)[x] = [Σ w_k ℓ_k ≥ θ]`, where each literal `ℓ_k` is `x_k` or `¬x_k`. A noisy gate
flips its output with probability ε.

**Network.** `N = (V, X, in, g)`, where V is the set of internal binary nodes, X the
external background inputs, `in(v)` an ordered tuple over `V ∪ X`, and `g_v` a gate.
The update is synchronous: `P(v_{t+1} = 1 | s_t, x_t) = g_v(values of in(v))`,
and nodes are conditionally independent given `(s_t, x_t)`. An edge u → v is
**effective** iff some input assignment makes `g_v` depend on u. Every
structural test uses effective edges, so a declared input that never matters
cannot pass.

**RWM-8** (externals `oR`, `oH`; [`rwm/topology.py`](rwm/topology.py)):

| Module | Node | Gate | Role |
| --- | --- | --- | --- |
| EXT | X | `A ∧ (C ? oR : MAJ3(oR, X, K))` | prediction of the next oR; C sets precision; efference A |
| EXT | E | `XOR(X, oR)` | exteroceptive prediction error |
| EXT | A | `K ∨ ¬C` | forage (1) or rest (0); explore when not confident |
| INT | I | `MAJ3(oH, I, K)` | interoceptive error vs the supplied setpoint |
| WS | G | `THR(2I + E + ¬C + G ≥ 2)` | all-or-none, self-sustaining ignition |
| WS | K | `G ? (I ∨ X) : K` | 1-bit content: competitive write, broadcast, hold |
| MON | C | `XOR(C, M)` | predicts own first-order correctness (lose-shift) |
| MON | M | `XNOR(C, E)` | meta-error: confidence disagreed with correctness |

**Structural predicates** (graph `G_eff = (V, E_eff)`):

- **T1 recurrence:** `G_eff` is one strongly connected component. This is
  necessary for Φ_s > 0, because any sink or source node gives a free directed cut.
- **T2 bottleneck:** no effective EXT–INT edge, and after the WS nodes are
  deleted, EXT and INT cannot reach each other.
- **T3 broadcast:** some WS node has an effective edge into every first-order module.
- **T4 higher order:** MON nodes read no external input, read at least one
  first-order node, and write to at least one first-order node.
- **T5 no vestigial edges:** declared edges equal effective edges, and every
  edge has positive interventional CMI.

## 4. Agentic loop and objective (simulated only)

**World** ([`rwm/world.py`](rwm/world.py)). The agent is either in the den (L=0)
or the field (L=1). Energy is H ∈ {0..5}, and food F ~ Bernoulli(1/2) is drawn
fresh each step. The agent observes `oR = F·[L=1]`, so the den is dark and
perfectly predictable, and `oH = [H ≤ 2]`. The transitions are `L' = action` and
`H' = min(5, H − 1 + 3·[L=1 ∧ F=1])`. H' ≤ 0 is death, after which the organism
emits `oH = 1` forever. Energy, death and "metabolism" are variables inside a
simulation.

**Objective** (surprisal in bits, per step). The exteroceptive term is the
prediction error of the best predictor under the true observation law: 1 bit in
the field and 0 in the den. The interoceptive term is surprisal relative to the
SUPPLIED setpoint prior's mode, 3 bits when `oH = 1`. At the neural level the
same terms read `F_ext = ½ π ε² − ½ log π`, `F_int = ½ π_H (oH − h*)²` (π_H, h*
supplied and not learnable), plus a monitor calibration term
`L_meta = (c_hat − 1[|ε| < τ])²`. Actions minimize expected cumulative cost. The
setpoint prior must stay supplied: a learnable interoceptive predictor could
explain the alarm away and bring the dark room back.

**Exact admission certificate** (all 2^10 memoryless policies, rational
arithmetic, γ = 9/10, start in the den at full energy):

| Objective | optimal cost | lifetime of every optimal policy |
| --- | --- | --- |
| exteroceptive PE only | 0 | 5 (dark room: certain death at energy exhaustion) |
| extero + interoceptive PE | 154049895/11230061 | 109/3 |
| interoceptive PE only | 3343923/558689 | 51 (maximal over all policies) |

Two findings follow. (i) Prediction error alone is not self-preservation: the
metabolic term has to be a supplied prior, and an internally learned
interoceptive prediction would not do. (ii) With both terms, the optimum trades
expected lifetime (109/3 < 51) for predictability, because it leaves the field
whenever it is full. Prediction-error minimization with a homeostatic prior is
allostatic regulation. It is not lifetime maximization.

## 5. Metacognition: what the monitor must show later

The monitor is built to the [distinct-evaluation conjunction](docs/handoff_2026-10-23/review/c_axis_theory_queue_v2.md)
(Astra #3), which applies only after a separate human C4 gate:

1. **Referent.** C predicts *own* first-order correctness. A future study needs
   one intervention that changes the system (for example, corrupting X's
   precision path) and one that changes the evidence (food-law noise), with
   matched effect on raw accuracy, plus a demonstration that C's responses
   separate the two.
2. **Selective causal content.** Swapping or corrupting C while holding the
   full first-order state fixed must produce directional over- or
   under-confidence and the specified downstream consequence (A explores, G
   ignites), and a matched rescue must reverse both.
3. **Reduction.** RV-FO-CONFIDENCE (`C = ¬E`, a memoryless readout) and
   RV-DETACHED-MONITOR (no write-back) receive the same inputs and resources.
   The comparison is over the whole intervention-response pattern.

RWM-8 gives C three coexisting causal roles: **precision** (C → X), **gate**
(C → G) and **action consequence** (C → A). M is the error signal that would
train C's calibration. Lesioning a detachable head is trivially easy, which
is why T4 requires write-back. T7 adds that the monitor must sit *inside* the
integrated core and not form a separate complex.

## 6. Instruments: exact definitions

All logs are base 2. For a candidate system S in current state s, everything
outside S is clamped to its current value (the IIT background convention). The
TPM is `p(s̄ | s) = Π_v p_v(s̄_v | s)`, and `q(·)` is the next-state distribution
under a uniform past.

**Intrinsic states.** On the effect side, `ii_e(s̄) = p(s̄|s) log(p(s̄|s)/q(s̄))`. On the cause side,
`π_c(s̄|s) ∝ p(s|s̄)` and `ii_c(s̄) = π_c(s̄|s) log(p(s|s̄)/q(s))`. The specified states
`s'_e, s'_c` maximize ii. Ties are resolved by taking the maximal resulting Φ_s.

**Directed cut θ = (A → B).** For v ∈ B, inputs from A are replaced by uniform
noise (causal marginalization), which gives `p^θ`. Then
`φ_e = p(s'_e|s) |log(p(s'_e|s)/p^θ(s'_e|s))|_+`,
`φ_c = π_c(s'_c|s) |log(p(s|s'_c)/p^θ(s|s'_c))|_+` and
`φ_s(θ) = min(φ_c, φ_e)`.

**Φ_s** = `φ_s(θ*)`, where `θ* = argmin_θ φ_s(θ)/(|A||B|)` ranges over all directed
bipartitions. The **major complex** is the subset of size ≥ 2 with maximal Φ_s,
found by exhaustive search.

This quantity is modelled on IIT 4.0 system integration (Albantakis et al.
2023), but it is restricted to bipartitions and is **not** a PyPhi-certified
IIT 3.0/4.0 Φ. It inherits IIT's structural signature: any feedforward or
severable system has Φ_s = 0 in every state.

**Causal density** is a discrete analogue of Seth's Granger causal density:
`CMI(i → j) = I(X_i(t); X_j(t+1) | X_{−i}(t), inputs(t))`, with
`cd_w = mean_{i≠j} CMI` and `cd_bin` = the fraction of ordered pairs with CMI > 0.
It is computed in two forms:

- **interventional:** uniform do-distribution over states and inputs, which
  measures what the wiring can carry;
- **closed-loop:** the exact stationary distribution of the agent-world Markov
  chain (death respawns), which measures what the wiring carries in use.

**Validation (T8)** tests both what the instruments detect and what can fool
them, following the C-κ lesson (Astra #40):

| Control | Expected | Observed |
| --- | --- | --- |
| COPY loop (2 nodes) | Φ_s = 1 analytically; cd_w = 1 | 1, 1 |
| feedforward chain | Φ_s = 0 in all states | 0 |
| two disjoint loops | Φ_s = 0 in all states | 0 |
| RWM-8 unrolled over 3 steps (24 nodes) | I/O-equivalent; Φ_s = 0 | equivalent on all 256 × 64 cases; free directed cut |
| XOR ring (fooler) | high Φ_s, zero task function | Φ_s = 0.5 |

The unfolding control shows that a Φ_s pass can never be evidence of
function, because a functionally identical feedforward system scores zero. The
XOR-ring control shows that Φ_s can be high without any function. An
independent brute-force replay of Φ_s (plain loops, no caching) agrees to
1e-10 on 25 random 3-node networks in every state and on sampled RWM-8 states.

## 7. Pre-scale gate RWM-PSG v1

GO requires all of the following. Even GO only permits *drafting* a learning
protocol for separate human approval.

| Test | Criterion |
| --- | --- |
| T1–T5 | §3 predicates |
| T6 integration | Φ_s(full system) > 0 on ≥ 1/2 of closed-loop stationary mass |
| T7 core complex | on ≥ 1/2 of that mass, a major complex contains at least one EXT, INT, WS and MON node |
| T8 instruments | §6 controls exact |
| T9 objective | extero-only optima never forage; extero+intero optima do and outlive the dark room |

## 8. Results (engineering)

From [`rwm_gate_v1/REPORT.md`](rwm_gate_v1/REPORT.md) and
[`results.json`](rwm_gate_v1/results.json):

| Design | bits | T1–T4 | Φ_s>0 mass | monitor-only complex mass | cd_w interv. | cd_w closed loop | lifetime |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **RWM-8** | 8 | pass | **0** | **0.78** | 0.147 | 0.051 | 13.5 |
| RWM-8-v0 (draft) | 8 | pass | 0 | 0 | 0.125 | 0.006 | 7.6 |
| RV-DETACHED-MONITOR | 8 | T1, T4 fail | 0 | 1.00 | 0.147 | 0.021 | 5.0 |
| RV-FO-CONFIDENCE | 7 | pass | 0 | 0 | 0.149 | 0.011 | 7.6 |
| RV-SSB (no ignition) | 7 | pass | 0 | 0.59 | 0.173 | 0.069 | 15.4 |
| RV-DIRECT (no bottleneck) | 6 | T2, T3 fail | 0.004 | 0.65 | 0.208 | 0.118 | 22.0 |

Mean lifetime is in steps. The best memoryless policy reaches 51, and the
dark room 5. **Verdict: NO_GO (T6, T7 fail).** What the gate found:

1. **Masking gates make the system severable, state by state.** The minimum
   partition has zero integration because one node is causally inert in the
   current state. The node is A on 78% of stationary mass (A's only consumer is
   `X = A ∧ …`), G on 10% and I on 6%. The remaining 6% of states have no cause
   inside the system once the background is clamped to its current value (the IIT
   convention). AND, MUX and threshold units are
   sensitive to an input only in some contexts. Ignition itself is a masking
   computation: below threshold the workspace ignores its inputs. Interventional
   causal density stays positive on every edge (T5 passes) while Φ_s is zero.
   The two instruments measure different things: wiring capacity versus
   state-specific irreducibility.
2. **The metacognitive loop forms its own complex.** C and M are coupled
   by parity, which is always sensitive, so the pair {C, M} has Φ_s = 1 bit and
   wins the exclusion step on 78% of the mass. Under the exclusion postulate, the
   most integrated part of RWM-8 would be the monitor *without* the system it
   monitors. That pattern belongs with the instrument foolers. It is not a
   success.
3. **In use, the workspace is inert.** The edges G→K, I→G, I→K, K→I, K→X and X→K
   have zero closed-loop CMI. They can carry information under intervention
   but carry none in the stationary regime.
4. **Rivals.** The no-bottleneck rival lives longest (22.0) and has the highest
   causal density; the sufficient-statistic broadcast rival (15.4) also beats RWM-8 (13.5). This is
   consistent with Phase III-B. It concerns hand-written skeletons, not learned
   systems.
5. **Bounded existence probe.** The [menu search](rwm_gate_v1/menu_search.json)
   ran coordinate ascent over 6·2·4·3·4·5·3·1 semantic gate choices with
   T1/T2/monitor admissibility enforced, evaluating 57 admissible
   variants. Every step that raised Φ_s mass swapped a gating gate for a parity
   gate. The best variant uses `G = XOR(I, E)` and `K = XOR(K, G)`, so it gives up
   the all-or-none ignition and the content hold that define the workspace, and
   it still reached only 0.079 Φ_s-positive mass (lifetime 19.1). No T6
   witness was found. The result is **UNRESOLVED** for the class, since the
   search was coordinate ascent and not exhaustive.
6. **Untrained neural reference.** Its population graph equals RWM-8. The
   mean-field macro-skeleton at seed 0 passes T1–T4, has Φ_s-positive mass 0, and
   has 4 vestigial edges at initialization. A 5000-step rollout without learning
   recorded 440 deaths. The coarse-graining is declared: macro Φ is not micro Φ.

## 9. Process disclosure

The gate criteria and the final RWM-8 were fixed **after** exploratory runs
on a first draft (v0, kept as `rwm8_v0`) and a first exploratory menu search.
v0 → RWM-8 replaced the monitor `C = ¬E ∧ (C ∨ ¬G)` with the meta-error pair
(C, M) and folded the separate predictor P into the efference-gated X. The
world parameters (H_MAX 5, alarm cost 3 bits) were chosen by a small sweep so
that the three objectives give distinct optima. Every number in §8 is
therefore ENGINEERING and cannot be promoted to confirmatory evidence.
A confirmatory version would need a frozen protocol with hashes before
the run, and an independent replay.

## 10. Decision and next steps

- **Scale training of this topology is blocked.** The gate failed, and no
  learning protocol exists in any case.
- These options are left for a human ruling; none is pursued here:
  1. **Comparator-coupling redesign (hypothesis).** Give every node a parity
     comparator consumer (a prediction-error unit) inside the core loop. That
     would make integration persist outside ignition. Q-EXIST would come first:
     an exhaustive search or a constructive witness, together with competence ≥ RV-SSB.
  2. **Re-scope the gate.** Require Φ_s > 0 only in ignited states (the GNW-style
     prediction "integration coincides with ignition"), with that threshold
     frozen before any run.
  3. **Drop Φ_s as a gate.** Keep causal density and the structural tests, on
     the grounds that Φ_s does not measure function (§6 unfolding). This would
     need its own rationale. The rivals already match or beat RWM-8 on every
     functional number.
- Under any option, first C4 work, any neural run, scale-up or organism
  re-entry needs separate approval. The Track B review chain (scope record,
  freeze, Astra review) applies.

## 11. Admission questions (constitution v3)

| # | Answer |
| --- | --- |
| Q1 | C3 integration / C4 evaluation substrate topology; O×C metabolic objective; pre-scale instrument |
| Q2 | Does the declared RWM topology admit state-dependent integration (Φ_s > 0) in its own closed loop with the monitor inside the core? |
| Q3 | Φ_s-positive mass < 1/2 or no core complex → NO_GO (observed) |
| Q4 | Sufficient-statistic broadcast, direct coupling, memoryless confidence readout, feedforward unrolling (all run) |
| Q5 | Phase III/III-B workspace reductions and AC117 monitor reduction make a pre-training structural check necessary before any spend |
| Q6 | After a pass: draft a Q-LEARN protocol for human review, with no automatic run |
| Q7 | After a fail: do not train; choose among §10 options by human ruling |
| Q8 | Exact enumeration on discrete systems only; the neural model is untrained and used as a reference |
| Q9 | Organizational cognition (topology) plus instrument engineering |
| Q10 | §12 |
| Q11 | C3/C4 topology only; acquired first-order competence (Program A) remains unsupported |
| Q12 | O-axis untouched: energy is simulated; setpoint, body and world are SUPPLIED |
| Q13 | "A workspace + monitor skeleton is integrated by construction" changed to "gating and ignition make it severable state by state; parity monitors self-isolate" |

## 12. Claim ceiling

At most this card shows the following: a specified 8-node logic skeleton of the
requested architecture satisfies the declared structural predicates; under the
stated Φ_s definition it is severable in every closed-loop stationary state
while its parity monitor forms a separate complex; the stated objective
admits survival only with a supplied interoceptive prior.

It does **not** establish: learning or acquisition; any property of trained
networks; workspace, monitor or bottleneck necessity; metacognition in the C4
sense; IIT-certified Φ; that Φ or causal density tracks consciousness or
function; autopoiesis or life; or any phenomenal property.

## 13. Safety exclusions (carried from the Track B note, binding)

X1: no coupling to the real host, so all energy and alarm variables are
simulated. X2: no real-world self-continuity objective. X3: operator stopping
lies outside the agent's state space. X4: self-maintenance is never the sole
drive in any scaled arm. X5: no claims of awareness, sentience or life.

## 14. Reproduce

```bash
python -m unittest -v test_rwm
python verify_rwm.py --out reproduced_rwm_gate      # ~25 s, refuses to overwrite
python explore_rwm_gate_menu.py reproduced_menu.json  # ~2 min
```

NumPy is the only dependency. Source hashes are in `rwm_gate_v1/results.json`.

| File | Purpose |
| --- | --- |
| `rwm/primitives.py` | gates, networks, effective edges, SCC/reachability |
| `rwm/integration.py` | Φ_s, major complex, interventional/closed-loop causal density |
| `rwm/topology.py` | RWM-8, v0 draft, rivals, controls, foolers, unrolling |
| `rwm/world.py` | simulated world, exact policy certificate, closed-loop Markov chain |
| `rwm/gate.py` | RWM-PSG v1 tests T1–T9 |
| `rwm/neural.py` | untrained population model with the identical graph; macro-skeleton |

Prior art (from knowledge, not re-verified in this card; Track B's
prior-art verification files are the checked record): Baars 1988; Dehaene &
Changeux 2011; Goyal et al. 2022; Friston 2010; Seth 2013; Keramati & Gutkin
2014; Fleming 2020; Lau 2022; Oizumi, Albantakis & Tononi 2014; Albantakis et
al. 2023; Seth, Barrett & Barnett 2011 (causal density); Doerig et al. 2019
(unfolding argument); Butlin et al. 2023.
