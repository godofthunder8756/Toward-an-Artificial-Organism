# The missing gap v1: every study ran where self-reference has no referent

2026-10-01. Analytic + synthesis card. Additive; no historical verdict, protocol,
freeze or result is changed. No learner, neural run or organism simulation.
Exact evidence: [scarcity_v1/certificate.py](scarcity_v1/certificate.py),
[certificate.json](scarcity_v1/certificate.json),
[independent tests](scarcity_v1/test_certificate.py).
Governance: [constitution v3](ACI_RESEARCH_CONSTITUTION_v3.md). No consciousness claim.

## 0. One-paragraph answer

Every closed study placed the agent in the **sufficiency regime**. In that regime
the agent's state can hold a sufficient statistic of everything its consumers will
ever be asked, either exactly or close to it. In that regime a theorem-level fact
(Blackwell sufficiency, §2) guarantees the program's recurring outcome. Any
workspace, selector, reliability monitor, self-state or access representation is a
relabelling of the first-order world posterior and can add no value. The "sufficient
statistic wins" verdicts were therefore **predictable from the task regime before any
run**. They are correct, but they are not informative about the mechanisms tested.
Every functionalist consciousness theory locates its distinctive seat in what a
**bounded** agent must do when it *cannot* hold the sufficient statistic: what
to admit (GWT), how to control limited processing (AST), and how far to trust its own
lossy representations (HOT-2). The program has never run that regime with
non-trivial headroom. Below sufficiency, the agent's posterior differs from the world's
posterior by an amount set by **its own encoding**. That difference is a referent
that belongs to the agent, not to the world, and it is the first thing in this record
that a self-model could be about. The exact certificate in §5 shows the collapse and
its lifting in the smallest solvable world. §6 shows why paid maintenance, the
program's one robust positive (N1), is the natural way to create this scarcity
inside an organism. That would make this the O/C intersection the synthesis says is
missing.

## 1. The pattern in the record

| Study | What reduced | Why, in regime terms |
| --- | --- | --- |
| AC67/71 self-monitoring | Host 1-bit corruption threshold + fixed repair | The integrity statistic is computed and supplied by the host |
| AC107/108 → [C0](C0_FEASIBILITY_v1.md) | Reliability tier "has no referent" beyond ε or `(n_u,n_p)` | C0's own premise: collapse holds *under the ideal-observer assumption* |
| [AC109](AC109_ENGINEERING_v1.md) | Stored estimate = transient diagnostic, 48/48 | Current observation is already sufficient; storage remembers nothing |
| AC112/113 + [R2](R2_P2_PROOF_CORRECTION_v1.md) | Graded posterior = integer counter, exact | The sufficient statistic is one integer; any capacity holds it |
| [AC116](AC116_ERRATA_v1.md) | Counter vs memoryless rival at resolution floor | Little history headroom remains to separate them |
| [AC117](AC117_RESULTS_v1.md) monitor | PREDICTION fails: transient `ones>=4` predicts wrongness perfectly | The wrongness statistic is directly readable; the monitor holds nothing extra |
| [Phase II](BRIDGE_PHASE2_VERDICT_v1.md) | Integrity readable from age; threshold reaches oracle | Hidden state was not hidden; one cue, no competition for upkeep |
| [Phase III](PHASE3_VERDICT_v1.md) | Free scalar LLR broadcast beats paid workspace | Its own scope note: "not about where the statistic is not closed-form" |
| [Phase III-B](PHASE3B_R10_CERTIFICATION_v1.md) | R9 code beats competitive workspace | Capacity *was* binding but shallow: certified penalty 0.0205 joint loss, about equal to the 0.02 gate margin; the 0.16 learning gap dominated |
| [Sub A](SUB_A_ANALYTIC_CHECK_v1.md) | Live repair = repetition code + host median | Redundant copies hold the whole table; disagreement aliases correct/wrong |
| [Proposed next node](ACI_NEXT_EXPERIMENT_DECISION_v1.md) | (not run) | 4-state world; its "marginals + covariance suffice" signature is built to succeed, giving another sufficiency confirmation |

C1 already found the key: the reliability tier is identifiable only where the
ideal-observer assumption is **violated** ([C1](C1_RELIABILITY_DISPOSITION_v1.md)).
No later study made that violation the controlled variable. III-B came closest, but it
made capacity bind by roughly one gate-margin. It then failed at Q-LEARN before the
question could be asked (0/1,024 state-dependent switches).

## 2. Proposition: Blackwell collapse, and its lifting

Let `h` be the agent's history, `S(h)` a sufficient statistic for every query and
consumer decision in the task, and `m = g(h)` the agent's internal state of capacity `K`.

**Collapse (K ≥ |range S|).** Storing `S` is optimal for every downstream decision
problem (Blackwell). Then `P(world | m) = P(world | h)` on every reachable state. So
every optimal decision is a function of the ideal-observer posterior. Any internal
variable Z, whether a confidence, access tag, monitor, attention state or self-state,
can be replaced by a function of that posterior without loss. No behavioural, value or
lesion contrast over these consumers can identify Z as being *about the agent* rather
than about the world. Selection and bottleneck mechanisms have zero value. C0's collapse
is an instance, and each §1 reduction follows without running anything.

**Lifting (K < |range S|).** `g` is then a strict garbling. Whenever two histories
with different decision-relevant posteriors share a state on positive mass,
`P(world | m)` is the ideal posterior averaged over the agent's own encoding cell. The
gap between the agent's confidence and the world's is then a function of `g`, which is
something the agent did: what it kept, dropped or merged. It is not a fact about the
world. Three things become non-redundant:

1. **Selection.** Which content to keep, conditional on goals: the GWT admission problem.
2. **Access representation.** A state-dependent record of *what this state lets me
   answer*: the minimal AST/HOT referent.
3. **Self-induced uncertainty.** Confidence that departs from the ideal observer in
   ways set by the agent's own encoding: the HOT-2 "reliability of my own
   representation" referent C0 could not find.

This is not an exotic mechanism. It is ordinary bounded-optimal state estimation,
which is the constitution's own reduction anchor. That is the point. Theory-distinctive
roles can survive this program's rival discipline only as variables that are ordinary
yet **non-redundant**, and non-redundancy needs scarcity.

## 3. Why this blocks the consciousness track specifically

The [theory-indicator matrix](ACI_THEORY_INDICATOR_MATRIX_v1.md) names D1 (HOT),
D2 (GWT), D3 (PP) and D4 (AE) as discriminating contrasts, with RPT, the recurrent
sufficient-statistic floor, as the null. By §2, **in the sufficiency regime D1, D2 and
the confidence half of D3 can only return the null.** The bottleneck has nothing to
choose. The higher-order state has nothing distinct to evaluate. Precision weighting
adds nothing over the exact posterior. The program has repeatedly confirmed the
RPT/sufficient-statistic null because those were the only experiments it ran. To
discriminate the theories, run them where the null is *not* guaranteed:
`log K < H(S)`, with the scarcity ratio `ρ = log K / H(S)` swept as a declared
level family.

## 4. Second gap: the success criterion does not match a novelty goal

The goal is novelty, not performance. Yet the binding gates are comparative loss
margins. III-B, for example, required a 0.02 margin over the best rival in 14/16 seeds.
Constitution v3 already separates causal role, necessity and engineering advantage, and
it states that worse scalar loss does not falsify an organizational role. Two
corrections follow:

- **Capacity parity removes the free sufficient-statistic rival by construction.**
  The rule "rival matches information and resources" was always enforced. But the
  resource never bound, so an exact counter or broadcast entered for free. In the
  scarcity regime, every rival gets the same `K`. The strongest rivals become static
  allocation, ideal-observer-confidence wagering, cue-blind encoding and a same-capacity
  monolithic learner, and none of them can hold `S`.
- **The primary claim type becomes identifiability plus within-system contrast**
  (Baars' contrastive method), not cross-architecture loss. The claim: an agent-referent
  variable exists in the bounded-optimal organization, is acquired, is causally used, and
  produces dissociations that collapse exactly at `ρ ≥ 1`. Value margins are reported but
  are not the gate.

## 5. Exact certificate: the smallest world where the collapse lifts

**World** (grid frozen in source before enumeration; all 72 cells reported). Three
uniform binary items, observed *cleanly*, so the ideal observer is always certain. A goal
cue predicts the later query with validity `v ∈ {1/3, 1/2, 3/4}`, where 1/3 is
uninformative. There are `K ∈ 1..8` memory states. On a query the agent answers
(reward 1 or 0) or opts out (sure reward `r ∈ {1/2, 5/8, 3/4}`). `K = 8` is sufficiency.

**Method.** Each memory state is identified with its codeword, meaning its action for
every query (27 codewords). The global optimum over all deterministic encoder/decoder
pairs is then an exact facility-location problem. It is solved by integer
branch-and-bound and compared at equal `K` across four classes: `full`; `static`, where
opt-out may depend on the query but never on the state; `no_opt`, which wagers by
ideal-observer confidence; and `cue_blind`, which uses fixed allocation.

**Results** (exact; `python -B -m unittest scarcity_v1.test_certificate`, 11 tests):

| Fact | Count / value |
| --- | --- |
| Sufficiency `K=8`: selection value, access value, self-induced uncertainty | **0 in 9/9 cells** (collapse) |
| Scarcity `K<8`: self-induced uncertainty mass > 0 | **63/63 cells** (pigeonhole; proven) |
| Goal-dependent selection strictly optimal | 24/63 scarcity cells (0 when cue uninformative), max 1/8 |
| State-dependent **access representation** strictly optimal over `static` | **14/63** cells, max 1/24; never at `K ∈ {1,2,4}` or `r = 1/2` |
| Selection and access both strictly optimal | only 2/63: they **compete for the same capacity** |
| Forced-choice accuracy on opted-out trials | exactly 1/2 everywhere: **no** "processed but not accessed" signature in a clean world |

Two slices (`value` columns are exact expected reward):

| K | full | static | cue_blind | access value | selection value | self-induced uncertainty | optimal codebook (`-` = opt out) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| *v=1/3, r=3/4* | | | | | | | |
| 3 | 7/8 | 5/6 | 7/8 | 1/24 | 0 | 1/2 | `0-- 10- 11-` |
| 4 | 11/12 | 11/12 | 11/12 | 0 | 0 | 1/3 | `00- 01- 10- 11-` |
| 6 | 23/24 | 11/12 | 23/24 | 1/24 | 0 | 1/6 | `00- 01- 100 101 110 111` |
| 8 | 1 | 1 | 1 | 0 | 0 | 0 | all eight value vectors |
| *v=3/4, r=1/2* | | | | | | | |
| 2 | 7/8 | 7/8 | 3/4 | 0 | 1/8 | 1 | `000 111` |
| 4 | 15/16 | 15/16 | 5/6 | 0 | 5/48 | 2/3 | `000 001 110 111` |
| 8 | 1 | 1 | 1 | 0 | 0 | 0 | all eight value vectors |

Read `00- 01- 100 101 110 111` at `K=6`. When item 0 is 1, the agent keeps everything.
When it is 0, the agent keeps item 1 and *knows it does not hold item 2*. Whether
item 2 is accessible is a fact about the agent's own state; the world was fully observed.
No same-capacity policy without that state-dependent access record does as well (1/24).

**What this does not show.** The magnitudes are small. Access value vanishes when `K`
aligns with whole items (`K = 2^j` lets "store j items" make access static), so a larger
or graded world is needed to judge robustness. The clean world yields no partial-access
dissociation. Exhaustive brute-force replay covers `K ≤ 3`. Optimality for `K ≥ 4` rests
on the branch-and-bound argument (a valid per-input upper bound), and the stored
codebooks attain the stored values. Nothing here is learned, neural, organismal,
metacognitive in the C4 sense, or conscious.

## 6. The novelty route for this program: scarcity made by its own maintenance

The surviving positive is N1: paid persistence is causally necessary under decay
(Phase II, III). It was judged to "buy nothing" only because there was always budget to
keep the whole sufficient statistic alive. Invert that. Let **the maintenance budget be
smaller than the cost of keeping all acquired content alive**, with hidden, uneven decay:

- Maintenance allocation *is* selection. The organism's capacity at each moment is
  whatever it chose to keep alive, not a fixed width.
- "What I am keeping alive" is then both an **organizational fact** (O-axis: which
  machinery and content persist) and the **referent of an access self-model** (C-axis:
  what I can currently answer). One variable has two roles. That is the proposed
  intersection the constitution names as a hypothesis.
- It closes the missing [O3 arrows](ACI_RESEARCH_SYNTHESIS_v1.md): content (predicted
  relevance) → maintenance allocation → which future content survives → future decisions.
  Phase II's allocation reduced to a threshold rule because there was one cue and age was
  readable. Many contents competing for a budget below demand removes both shortcuts.

If this held, it would be a genuine first: an artificial organism whose access
self-model is non-reducible and whose referent is its own self-maintenance. It would
not be a consciousness claim, but it would be the first result in this record where a
theory-distinctive organization survives the strongest same-resource rival because
the rival *cannot* hold the sufficient statistic either.

## 7. Proposed next node (design only; human gate required)

Proceed in stages. Each stage is admitted only if the previous one passes. All parameters
must be frozen before computing, and every grid cell reported.

1. **Analytic, graded evidence.** Extend this certificate to two noisy looks per item, so
   the ideal observer's confidence varies. Prospective signatures:
   - (S1) Collapse: every agent-referent quantity is 0 at `ρ ≥ 1`. Failure means a bug,
     not a result.
   - (S2) A partial-access dissociation: opted-out trials with above-chance forced choice
     **on trials where the ideal observer was certain**. Plain opt-out with above-chance
     forced choice also occurs in noisy ideal observers, so that alone does not
     discriminate.
   - (S3) The optimal agent's metacognitive efficiency (meta-d′/d′ against its *own*
     first-order accuracy) falls below the ideal observer's only for `ρ < 1`.
   - (S4) A strictly positive access value at capacity parity on a declared `ρ` family,
     not one favourable cell.
2. **Analytic, paid maintenance.** Replace fixed `K` with a refresh budget under hidden
   decay (§6). Test whether optimal allocation depends on predicted relevance, and whether
   an access record of *what is being maintained* is non-redundant. Rivals: fixed duty
   schedule, threshold-on-observables, a same-budget random-allocation yoke.
3. **Lesion dissociation in the optimum.** Factor the optimal state into a content part
   and an access part where possible. Damaging access with content intact should give
   blindsight-type behaviour (above-chance forced choice, opt-out). Damaging content
   with access intact should give confident errors. Both should be undefined or
   indistinguishable at `ρ ≥ 1`.
4. **Only then Q-LEARN.** A prospective learner at equal `K` or budget, with the analytic
   optimum as its R10-style ceiling, so learning failure and representability stay
   separate. III-B's lesson is binding: certify headroom large relative to the gate before
   training.

On the [pending decision package](ACI_NEXT_EXPERIMENT_DECISION_v1.md): its two-factor
world is a fine first-order competence check. As frozen, though, it sits in the
sufficiency regime, and its strong-reduction signature is designed to pass. Adding a
capacity axis below `ρ = 1` is the difference between another confirmation and a
discriminating test.

## 8. Thirteen admission answers

| Q | Answer |
| --- | --- |
| 1 | C-axis prerequisite: when can C3/C4/C5-type roles be non-redundant at all; O3 bridge via maintenance scarcity |
| 2 | Agent-referent variables are behaviourally unidentifiable at sufficiency and can be strictly optimal below it |
| 3 | Falsified if any agent-referent quantity is non-zero at `K=8`, or if access/selection value is zero in every scarcity cell; both checked |
| 4 | Ordinary bounded-optimal coding/control at equal capacity, included as `static`, `no_opt`, `cue_blind` |
| 5 | C0's ideal-observer premise, C1's violation condition, Phase III scope note, R10's shallow penalty, AC117 readable wrongness |
| 6 | Graded-evidence and paid-maintenance certificates (§7.1–7.2) before any learner |
| 7 | If graded/maintenance worlds also show zero access value, park the access-self-model line with an exact reason |
| 8 | Analytic exact enumeration only; stdlib, about 3 min CPU |
| 9 | Organizational cognition (identifiability of a role), not engineering advantage |
| 10 | Exact optimal-policy facts for one finite problem. NOT learning, neural, organism, C4, self-model or consciousness |
| 11 | C2/C3 boundary; C4/C5 remain unadmitted and need a human gate |
| 12 | O0: capacity is supplied. §6 proposes making it organism-produced via maintenance |
| 13 | "Sufficient statistic wins" is reclassified: correct and predictable in-regime, uninformative about scarcity-seated mechanisms |

## 9. Boundary

No phenomenal claim, and no claim that any C/O conjunction would establish one. The
strongest wording any successor could earn is "meets candidate indicator X at degree Y,
non-reducibly at capacity parity". First C4/C5 studies, organism re-entry and any neural
training remain separately gated by the constitution.
