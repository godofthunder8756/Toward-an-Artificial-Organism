---
title: E3 B06 analytical evaluation
description: Design-only erasure assurance, H1 headroom, H2 source budgets, and freeze obligations
ms.date: 2026-09-10
status: Complete analytical research - qualified design closure; no freeze
---

## Scope and research questions

Read the selected evaluation, policy, physical, control, and protocol contracts.
Use local evidence and exact scalar mathematics only. Do not implement or run
E3, draw targets, run Monte Carlo, consult external sources, or modify contracts.

* Determine canonical-reset output and missingness laws, and prospective
  containment assurance for the selected 32-individual, eight-panel design.
* Establish useful H1 financial/information ceilings without claiming an
  unproved adaptive advantage over competent periodic correction.
* Determine what sourcewise accounting does and does not establish at H2 g=36.
* Separate prospective design checks, later implementation conformance, and
  hypotheses whose positive outcomes must remain experimental questions.

## Executive conclusions

1. The selected canonical-empty negative has a tractable output law. Under the
   ideal independent input law and conforming services, emitted-bit accuracy is
   exactly chance, expected planned recall is 0.497509980020, and funded activity
   and completion are one. A sufficient-event bound gives at least 0.996306
   containment assurance per representation with the current 32 x 8 design,
   including coverage. This exceeds B05's 0.80 target without changing n.
2. Generic reset noninterference alone would not justify that precision. A
   fixed-per-cue output sensitivity has much poorer n=32 precision. A prospective
   n=256 variant is recommended only if the design is to tolerate that broader
   output law, and requires explicit versioning and bootstrap-weight audit.
   Neither 128 nor 256 individuals are silently selected here.
3. A clean-parent H1 reference leaves less than five points above competent
   always-due periodic correction. Its analytic expected-margin ceiling is about
   0.0164 after query loss. The actual trained-parent adaptive contrast remains
   unknown; the protocol's five-point hypothesis is not guaranteed or proved
   impossible for the full experiment.
4. H2 g=36 guarantees conditional financial liveness and REP full-service
   affordability, not successful recall. Full REP correction and all ordinary
   learning bookkeeping can precede conditioner rejection. Fixed REP policies
   can afford all conditioning and maximal correction. Scarcity is partly a
   learning/automatic-conditioning cost, not a forced useful-versus-obsolete
   choice of code-write targets.
5. Positive H1/H2 results are experimental questions, not prerequisites for
   allowing a falsifiable design. Pre-code specification and static reviews
   remain mandatory. Implementation conformance and scripted functional checks
   belong after separately authorized implementation, before final draws.
   Literal B05 wording that demands proof of positive performance before design
   freeze needs prospective clarification, not an invented success theorem.

## Local evidence and authority

Read in full:

* E3_EVALUATION_CONTRACT_v0_7.md, especially complete erasure, randomness,
  estimands, named gates, B06 targets, and freeze dependencies
* E3_POLICY_CONTRACT_v0_5.md, especially action/task return, Q learning,
  fixed policies, conditioning, and population-level engineering ranking
* E3_PHYSICAL_CONTRACT_v0_4.md, especially domains, ordered conditioning,
  simultaneous faults, full-source entry, and sourcewise budgets
* E3_CONTROL_CONTRACT_v0_6.md, including two prepaid CONTROL budgets and its
  explicitly unclosed ROM/scan/RESPONSE/TERMINAL/upkeep trace obligations
* E3_PROTOCOL_v0_1.md, including falsifiable claims, scripted controls before
  final seeds, negative controls, gates, and two freezes
* E3_STATE_CONTRACT_v0_2.md and E3_OPERATION_CONTRACT_v0_3.md, to resolve exact
  query-slot lifetime, missingness, paid prefixes, and reset semantics
* NEW_AGENT_GUIDE.md, for experiment/failure discipline

Also read .copilot-tracking/research/subagents/2026-09-10/e3-b05-evaluation-research.md
and .copilot-tracking/research/subagents/2026-09-10/e3-b03-selection.md.
They are supporting evidence, not overrides. The v0.6 controller prices and v0.7
evaluation choices supersede the corresponding older candidate statements.
No result tables or external sources were consulted. Incorporated control
trace/review documents were not independently re-audited in this B06 task.

## Complete erasure output and missingness law

### Empty code is an invariant

Start all eighty code symbols at 10. Ordinary sign flips and the challenge
swap only 00/01, never populate 10/11. Erasure leaves 10. Every live correction
scan is empty, so scrub abstains. A readout guess cannot write a repair sign.
No teacher, ecological return, callback, or Q-to-code action exists in the reset
phases. Corrupt Q can change resource-action selection but cannot make an empty
scan authorize correction. Induction therefore keeps the entire code bank empty.

This proof relies on the protected executor and selected operation interface,
not on the chance statistic. A malformed implementation that copies a response
guess into code would violate it even if an accuracy interval happened to pass.

### Funding and five-fault query validity

Canonical activation, paid ISOLATE, recovery g=47, and assay g=28 satisfy the
selected full-start bounds, including all conditioning, auxiliary retirement,
and post-fault leakage. The additional controller C is already in v0.6 recovery
prices and absent from the assay. Code emptiness does not make RESPONSE free;
fault-created valid slots can require its full scan and guess.

Conditional on trace conformance, every scheduled assay admission and decode is
financially affordable, all domains are reset before every fault, h=0.001 and
e=0. This holds despite age-bit corruption because each next conditioner writes
its age before the next simultaneous fault. Death or admission rejection is not
an expected random event in this supported reset path. It would require a
contract/input/implementation violation, not a label-dependent exception.

A query admitted at t is read at t+5, after faults t through t+4. Its valid bit
starts at one and survives when an even number of five independent flips occur:

$$
s=\frac{1+(1-2\cdot0.001)^5}{2}=0.995019960039984,
\qquad q_v=1-s=0.00498003996001595.
$$

Different admitted queries use disjoint physical-bit/time fault coordinates,
including successive uses of the same slot. Thus each panel's planned-emission
count M has law Binomial(256,s). Expected missing rows are 1.27489023 per panel.
Reserved bits are not an additional integrity check. All sixteen stored cue
encodings are legal; address corruption changes a scan address, not validity.
On empty code, every such address still leads to a fresh fair guess.

Warm-up and recovery spurious responses are unscored service events. A guess
key belongs to phase/planned service tick/slot, not emitted-response ordinal,
actual corrupted cue, action count, or previous guess consumption. Spurious
draw consumption cannot shift a later planned response's random input. The
scorer pairs a planned emitted bit with the original scheduled cue, never uses
that cue to repair the worker address, and never invents an output on an invalid
slot. This is the relevant meaning of a forced guess: forced choice on a funded
valid decode, not forced completion of a missing planned row.

### Correctness and selection independence

Condition on all targets, schedules, validity faults, and non-guess inputs.
The remaining emitted guesses are independent fair bits. Guess values change
neither memory, future funding, availability, timing, nor feedback in this
negative assay. Repeated comparison with one fixed target therefore yields
independent fair correctness bits conditional on that target. There is no
sixteen-label bottleneck for this particular independently randomized output law.

Consequently:

$$
\mathbb E[R_{\rm planned}]=s/2=0.497509980019992,
\qquad \mathbb E[C/M\mid M>0]=1/2.
$$

The raw planned statistic is slightly below one half, as required when missing
rows score zero. B05's containment gate instead uses each panel's C/M, averaged
equally across eight panels and then individuals. No evaluator guess, pooling
of emissions in place of panel averaging, or survivor deletion is needed.

Without supported funding, raw chance could fall far below 0.45. For example,
a constant unconditioned age fifteen would give valid survival
(1+0.968^5)/2, before lane erasure, and lower coverage. That is not the selected
reset path. Death could make raw recall zero without showing negative
information; it must not be relabeled emitted-bit chance accuracy.

### A rigorous sufficient-event bound for the selected bootstrap

Let B be the event that every one of the 32 x 8 panels emits at least 244 bits.
This is stronger than B05's mean coverage >=0.95 guard since 244/256=0.953125.
The exact finite binomial sum gives

$$
p_{\rm low}=\sum_{k=13}^{256}{256\choose k}q_v^k(1-q_v)^{256-k}
=9.00860987833\cdot10^{-10},
\qquad P(B^c)\le256p_{\rm low}.
$$

For individual i, write A_i=(1/8) sum_p C_ip/M_ip. On B its correctness-bit
weights are 1/(8M_ip), and their squared sum is

$$
\sum_{p,r}w_{ipr}^2=\frac1{64}\sum_p\frac1{M_{ip}}
\le\frac1{8\cdot244}.
$$

Conditional weighted Hoeffding and a union bound over individuals give

$$
P\{\exists i:|A_i-1/2|>0.05\mid B\}
\le64\exp[-2(0.05)^2(8)(244)]
=0.00369373581665.
$$

If all A_i are in [0.45,0.55], every bootstrap resample mean is in that band.
Therefore both declared empirical percentile order statistics are in the band
for ANY fixed resampling index list, including the selected public analysis
key. This avoids pretending the percentile bootstrap itself has exact coverage
or treating its 10,000 dependent replicates as new observations.

The resulting joint containment-and-guard probability is at least

$$
1-256p_{\rm low}-64e^{-9.76}=0.996306033562934.
$$

Activity and completion are one under the funding argument. A union bound across
REP and BLOCK gives at least 0.992612067126 without assuming independence between
their paired guesses or faults. The all-history children add no independent
sample size. The bound applies to the prespecified primary subset, not an
undeclared requirement that every diagnostic interval pass simultaneously.

This closes prospective erasure precision for the current mathematical design,
conditional on audited ideal input ownership and service conformance. CNG/HMAC
is a computational implementation of independence, not a new mathematical proof
that deterministic pseudorandom bytes are truly independent. B07 and production
tests remain required, but their future execution is not needed to derive this law.

## Dependence sensitivity and prospective sample alternatives

### Fixed-per-cue outputs are a different law

Hold G and all future target-independent inputs fixed after reset. Let w_ij be
the total normalized weight of cue j for individual i, and d_ij the signed
difference of its one-prediction weight minus its zero-prediction weight. Conditional on those
outputs and weights, fair independent target bits imply

$$
A_i=\tfrac12+\sum_{j=1}^{16}d_{ij}(Y_{ij}-\tfrac12),
\qquad \operatorname{Var}(A_i\mid G,Z)=\tfrac14\sum_jd_{ij}^2
\le\tfrac14\sum_jw_{ij}^2.
$$

With no missing rows and equal cue counts, w_ij=1/16 and variance is at most
1/64=0.015625. Fixed output per cue attains that bound even if the output vector
is common across panels or across individuals. After conditioning on that
target-independent vector, all 16n label-match bits remain independent. Then
the total is exactly Binomial(16n,1/2), not Binomial(2048n,1/2).

If w is arbitrary and can concentrate on one cue, the variance bound becomes
1/4. Target independence proves mean one half, not equal weights or narrow
intervals. A marginal 0.95 mean coverage guard alone does not bound every
individual's weights. On the stronger M_ip>=244 event, w_ij<=16/244, giving
sum_j w_ij^2<=16/244 rather than silently reusing 1/16.

For the complete-coverage fixed-per-cue law, the following exact binomial sums
refer to an ILLUSTRATIVE fixed normal-width interval, not B05's empirical
individual-bootstrap interval. Set h_n=1.96/sqrt(64n) and count integer K with
16n(0.45+h_n)<=K<=16n(0.55-h_n).

| Individuals n | Illustrative half-width | Accepted K | Exact probability for that fixed-width rule |
|---------------|-------------------------|------------|--------------------------------------------|
| 32 | 0.04331029 | 253-259 of 512 | 0.24291697 |
| 128 | 0.02165515 | 966-1082 of 2048 | 0.99028912 |
| 256 | 0.01531250 | 1906-2190 of 4096 | 0.99999160 |

The n=32 sensitivity explains the earlier approximately 24% warning. It is
neither the current canonical-empty assurance nor an exact calculation of its
bootstrap. Replacing fresh guesses by repeated guesses would invalidate the
0.996306 proof and require a new prospective analysis before final draws.

### Concentration targets are not interchangeable with intervals

For equal cue weights and arbitrary fixed target-independent outputs,

$$
P(|\bar A-1/2|>\epsilon)\le2e^{-32n\epsilon^2},
\qquad h_H=\sqrt{\log(40)/(32n)}.
$$

For the alternative interval [bar A-h_H,bar A+h_H], containment has lower bound
1-2 exp[-32n(0.05-h_H)^2] when h_H<0.05, truncated below at zero.

| n | Hoeffding 95% half-width h_H | Containment lower bound for that interval |
|---|----------------------------|------------------------------------------------|
| 32 | 0.06002017 | 0, uninformative |
| 128 | 0.03001009 | 0.61077611 |
| 185 | 0.02496240 | 0.95110060 |
| 256 | 0.02122034 | 0.99773919 |

Merely bounding the point-estimate error by 0.05 at 95% confidence requires
n>=47, but does not make a 95% interval fit inside the same 0.10-wide band.
Allocating 0.025 to interval radius and 0.025 to center error requires n>=185.
Chebyshev alone with Var(bar A)<=1/(64n) would require n>=500 for a 0.025
center margin with 95% assurance. These are different explicit design criteria,
not competing estimates from E3 results. None silently replaces the selected
bootstrap or authorizes an observed-sample-size stopping rule.

### Conditional bootstrap hardening at n=256

A prospective 256-individual version can retain the original empirical
bootstrap and be audited analytically. Let K_bi be counts of individual i in
bootstrap replicate b and kappa_b=(sum_i K_bi^2)/n. With equal cue weights,
conditional target concentration bounds either tail of replicate b by
exp[-0.08n/kappa_b]. On M_ip>=244 replace kappa_b by
kappa_b(256/244). This holds for arbitrary fixed target-independent output
vectors and uses independent labels, not independent bootstrap replicates.

If the PREDECLARED 10,000-row resampling matrix has max_b kappa_b<=3, linearity
of expectation and Markov's inequality give failure probability at most

$$
\left(\frac{10000}{250}+\frac{10000}{251}\right)
\exp\left[-\frac{0.08n}{3(256/244)}\right]+8n p_{\rm low}.
$$

The denominators follow exactly from one-based percentile positions 250 and
9750: lower failure needs at least 250 values below 0.45, upper failure at
least 251 above 0.55. At n=256 the containment-and-coverage lower bound is
0.88076019. With complete coverage it is about 0.91341546. This is a sufficient
conditional guarantee for the actual percentile rule, unlike the normal-width
illustration. No independence between resamples is invoked.

The kappa condition has NOT been evaluated: no bootstrap indices were generated
here, and v0.7 only defines n=32 indexing. If broader dependence protection is
desired, recommend prospectively versioning n=256, the distinct final IDs,
bootstrap tuple/mapping, row products, and archive counts, then auditing the
fixed matrix or its exact sum of tail bounds. Do not search for a favorable
analysis seed or force balanced guesses/labels. The current eight panels stay.
This recommendation is optional hardening, not evidence that the current
canonical-empty n=32 design is blocked. No contract or sample was changed.

## H1 financial and information ceilings

### Correct reconstruction is funded, not assured

Recovery g=47 and the full-source induction pay the maximal REP/BLOCK scrub,
spurious RESPONSE, age services, every conditioner, and leakage on every
supported recovery tick. The 128 balanced offers visit each cue eight times.
Reconstructing the two erased REP layers from a correct surviving majority
needs 32 total paid writes, not 32 new answer bits. A wrong unique majority
can instead reconstruct the wrong sign. Q is not refreshed or protected.

Post-challenge assay has no correction or learner and wears for all 261 ticks.
Let A_3(p)=1-3p^2+2p^3 and A_5(p)=1-10p^3+15p^4-6p^5. For response t=6..261,
five perfectly correct replicas immediately before challenge give effective
error p_t=(1-0.8(0.998)^(t-1))/2. Hence the correct-address ceiling is

$$
U_5=\frac1{256}\sum_{t=6}^{261}A_5(p_t)=0.943681192267601.
$$

For p_t<1/2, an initially correct five-symbol repetition group maximizes
majority accuracy; retaining fewer observed symbols cannot increase that
maximum. Conditioning on any fixed pre-assay state does not avoid the future
independent flips. Accounting for valid-bit loss gives the generous universal
planned-recall ceiling s U_5=0.938981622221. It ignores additional address error
and remains an upper bound rather than an attainable promise.

If all three initial survivors are correct and no writes occur for 128 recovery
ticks, the analogous perfect-survivor correct-address mean is

$$
N_3=\frac1{256}\sum_{t=6}^{261}
A_3\left(\frac{1-0.8(0.998)^{128+t-1}}2\right)
=0.830589554945185.
$$

In this ideal label-symmetric reference, each address bit is correct with
probability s, so the four-bit original-address probability is s^4. A wrong
address yields mean one-half against an independent original-cue label. Thus
the reference no-write planned recall is s[1/2+s^4(N_3-1/2)]=0.819949370551.
This does not estimate actual developed parents. It shows meaningful
maintenance-versus-no-write room under the complete wearing assay, rather than
reusing the old isolated-challenge gain 0.01944 or recovery-only 0.08641.

### Competent periodic correction leaves little adaptive room

Consider a mathematical clean-parent reference: all three post-lesion survivors
per cue equal their independent target, future schedules/faults are independent,
and the supported I=1 periodic rule scrubs every offer. Resource bins are high
throughout H1 recovery, so I=1 really is always due. It is an existing candidate,
not a new oracle or a policy that sees correctness.

For one cue, its eight positions form a uniform eight-subset of 1..128.
The nine empty gaps X before, between, and after those positions sum to 120;
each has the exact marginal law

$$
P(X=x)=\frac{{127-x\choose7}}{{128\choose8}},\quad x=0,\ldots,120.
$$

Write q_d=(1-0.998^d)/2. At the first scrub there have been X pre-response
faults on three survivors. At each later scrub the inter-scrub fault count is
X+1 on five symbols. A union bound for ever taking a wrong majority is

$$
\eta=\mathbb E[1-A_3(q_X)]+7\mathbb E[1-A_5(q_{X+1})]
=0.000909988649092+7(0.000102081276004)
=0.001624557581121.
$$

This uses the same fault coupling to a process corrected to truth at every
scheduled offer UNTIL its first miscorrection. It does not pretend that process
is an allowed agent or that gap events are independent. At the last scrub,
the remaining recovery faults are X+1, including that scrub tick's fault.
The hypothetical always-correct last-decode reference averages to

$$
L_{\rm ideal}=\mathbb E_X\left[\frac1{256}\sum_{t=6}^{261}
A_5\left(\frac{1-0.8(0.998)^{X+t}}2\right)\right]
=0.937436182681630.
$$

Subtracting eta bounds the real periodic code accuracy below by 0.935811625101.
With validity/address corruption, target symmetry in this clean reference gives
periodic planned recall at least 0.922577356414. Compared with the same clean
parent's no-write value 0.819949370551, this establishes at least 0.102627985863
expected maintenance gain for this paid conventional reference. It is not an
RL prediction or a test pass, but demonstrates that useful paid reconstruction
and the five-point maintenance effect are not excluded by the selected assay.
The generous upper bound for
ANY adaptive pre-assay REP state then gives

$$
\mathbb E[R_{\rm adaptive}-R_{I=1}]
\le0.938981622221-0.922577356414
=0.016404265807<0.05.
$$

This is a conditional no-go for an EXPECTED five-point advantage in the stated
clean-parent reference. It is not a deterministic bound on every realized
finite sample, nor a theorem for trained parents. PERIODIC's actual developed
state may contain preexisting errors, its H1-family selection may choose another
I, and finite engineering ranking need not select the population-optimal I=1.
Learned RL and periodic parents have different acquisition/development histories.
The intact >=0.90 prerequisite is a recall gate, not a clean-all-replicas guarantee.

More quantitatively, couple an actual periodic parent to the clean reference
using the same future inputs. If beta is the probability that their relevant
post-lesion whole banks differ, bounded recall implies an extra at most beta
in this loose margin bound. An expected five-point advantage would need
beta>=0.033595734193 or some other violation of the clean-reference assumptions.
This is only necessary under that coupling and comparison to I=1, not sufficient
for success or a beta estimate. No parent-state distribution was drawn here.

### Objective alignment does not prove an RL advantage

In supported frozen recovery a forage attempt is fully accepted: prior charged
work leaves more than 64 energy below cap. It contributes a=16; scrub contributes
a=-W. The immediate return gap is 16+W, or 16..21 for REP and 16..36 for BLOCK,
before discount scaling by 1/256. In the recovery-only resource-return problem,
foraging every tick attains the pointwise maximum 16 and funded survival, so
correction is not required to optimize that isolated action return.

But RL is not trained to optimize a recovery-only objective; it carries frozen,
wearing Q learned under development feedback. Current recovery reward is not
used for TD. The observation omits cue identity and recovery phase, and may alias
development states. Development/ecology b can reward maintained information, but
the due query normally belongs to an earlier, different offer. Discount gamma
has scale sixteen ticks, gamma^5=0.724196434, and a long tail, not a hard cutoff.
No convergence theorem or optimal action follows from this scalar incentive gap.

Therefore H1-MAINT has plausible analytic room, H1-ADAPT has a strong conventional
rival and a clean-reference ceiling warning, and neither positive gate is proved.
Keep the gates. A negative adaptive result is scientifically meaningful and must
not be avoided by weakening periodic tuning, selecting a different challenge,
or requiring a positive engineering outcome as permission to study it.

## H2 sourcewise feasibility and actual scarcity at g=36

### Prefix accounting and energy liveness

For each source use accepted, not offered, grants. Every prefix obeys stock
balance AND the current gate's componentwise c+L+T+rho bound. Initial phase entry
is P=242 after paid ISOLATE, and the first g=36 grant caps it at 255. Later live
tick starts have at least 36 per source, even after a preceding zero stock.
No external mid-phase refill is assumed for H2-D/C/N.

The maximal block learning energy envelope at g=36 is
29394-4(66-36)+1=29275, including the final leakage and conservatively both
admission and TERMINAL. It is below the 30000 offer even if the previous E is
small. Optional failures cost no more than this envelope. Thus energy is not
the scarcity constraint on an eligible, conforming H2 path.

Ordinary per-source material before code or optional conditioning is bounded by:

| Work | Per source |
|------|------------|
| Old transition retirement | 4 |
| Current transition store | 4 |
| Admitted Q update | 2 |
| Valid-record reward finalization | 2 |
| Query-slot retirement | 1 |
| Successful admission | 1 |
| Mandatory age increments | 10 |
| Total, before conditioning/code/leakage | 24 |

These are successful-path maxima, not all mandatory minima. Dropped TD saves
two; absent record finalization or rejected DECIDE saves additional work.
Conditioning never precedes this work and cannot consume its earlier reserved
tail. At the final drain tick, remove admission one and add at most six for
TERMINAL, giving 29. Conditioning gates reserve that TERMINAL tail.

Even a maximal REP scrub adds only five at its single source, hence at most
29 ordinary or 34 terminal per source before optional conditioning. Both fit
36. All its optional code/Q/admission work and mandatory tails are therefore
fundable from each tick's grant alone, conditional on the selected traces;
actual valid-slot existence and correct decoding remain separate. A BLOCK
maximal scrub instead reaches 44 ordinary or 49 terminal at its source, so it
may stop at the first needed-write gate. Public minimum tails are still funded.

This proves a sourcewise live path induction for H2 code-only ecology, including
ordered optional rejections and zero end-of-tick P. It does not restore a dead
parent, promise decoded outputs from invalid slots, or establish useful recall.
For REP, lack of total material cannot by itself force a choice to skip a
needed five-symbol scrub on these ordinary paths. Its consequential trade-off
is largely what happens to later automatic conditioning, not immediate repair.

### Why 40 is not mandatory upkeep

All twenty conditioners add fifteen per source, so the ordinary all-success
learning path with leakage costs 24+15+1=40 before code writes. Without TD this
is 38. Fixed/frozen no-record paths cost 28 before code. These are different
actual obligations, not matched spending. A fixed REP path with maximal five
code writes needs at most 33 at its busiest source and 28 elsewhere. At g=36
it remains fully conditioned by the same full-start induction, even if it
scrubs every offer. A frozen REP allocator shares that financial advantage.
BLOCK's maximum twenty writes can exceed that margin.

Only automatic affordability chooses which domains condition, in order 0..19.
The learner has no conditioning action or free age observation. Calling this
"the policy allocates eleven chosen domains" would invent an interface.
At a low-stock ordinary learning tick, start with 36 each, complete the 24
preconditioning debits, and inspect the resulting fixed-order vector worksheet:

| Earlier code writes at source 0 | Available before conditioning | Automatically admitted domains | End vector before leakage |
|--------------------------------|-------------------------------|--------------------------------|---------------------------|
| 0 | (12,12,12,12) | 0,1,2,3,4,5,6,7,8,9,10,11,12,13,15 | (0,0,0,3) |
| 5 | (7,12,12,12) | 0,1,2,3,5,6,7,9,11,13,15,17 | (0,5,1,1) |

Each admitted body subtracts exactly
b(d)=v_floor(d/5)+v_((924+2d) mod 4)+v_((925+2d) mod 4). These are two static
20-domain prefix worksheets, not simulated trajectories or a promise that a
particular low-stock vector occurs. They show real source contention and an
immediate change from fifteen to twelve admitted bodies when five code writes
consume source 0. There is no universal "about eleven conditioners" count:
retained stocks, drops, collection, terminal tails, and cross-source age writes
change it. Leaked residuals and unused material stay in the ledger.

Lapsed domains have incremented age at least one before faults, hence h>=0.002
and e>=0.0001 instead of the conditioned 0.001/0. Some cover code, others Q or
query/age storage. The fixed ordering can shift hazards across unrelated U/O
regions; it is not usefulness-guided domain protection. Which loss matters
functionally cannot be inferred from body count alone.

### A rigorous full-conditioning resource exclusion

There is a stronger aggregate check that already grants the worker MORE
collection than its one-action rule permits. Suppose every tick admits DECIDE,
every current record is finalized, all 507 queries are admitted, and all twenty
domains condition. Let U be the number of admitted Q-update bodies across
ordinary controller TD and final TERMINAL, W total code writes, and Lambda
total material leakage. Sources have at most

$$
P^{\rm passive}_{j,\max}=255+511(36)=18651
$$

available during the phase, because the first grant overflows the full cap.
Ignoring subsequent overflow, even accepting eight collection units on EVERY
tick would supply at most 4(18651)+4096=78700 total material. Without Q updates,
code or leakage, the stated work costs

$$
4[512(36)+507+4]=75772.
$$

Here 36 per source is old clear/store/reward/retirement plus fully conditioned
upkeep, 507 counts actual admissions, and four is final mandatory record clear.
Thus a NECESSARY condition for that full-service, all-conditioned path is

$$
8U+W+\Lambda\le2928.
$$

Even with W=Lambda=0, U<=366. An ideal one-update-per-tick path plus final
TERMINAL has 512 updates (first controller has no old record), requiring 4096
material, already too much under this generous upper supply bound. Full
conditioning with every update is impossible even before repair and despite
granting maximal collection every tick. Actual collecting precludes scrub on
that tick and often overflows, so cannot invalidate the exclusion.

This does NOT prove all-conditioned operation impossible for legal policies:
faults can invalidate old records, TD can drop, DECIDE/finalization can fail,
and fixed/frozen policies omit those costs. Removing such work weakens the
inequality's premise. It establishes a genuine processing/conditioning
opportunity cost, not inevitable mortality or selective useful retention.
With all 80 symbols occupied and conditioned, expected code-flip EVENTS over
512 faults are only 80(512)(0.001)=40.96 globally, not forty code writes per
tick. Events are not completed repairs: flips can cancel, multiple damaged
symbols can be handled together, wrong signs can be copied, and lapses add
erasures and larger hazards. Do not mix the per-source 40 housekeeping figure
with this unrelated global expected event count.

### Comparator denominators and what remains empirical

Code-write counts cannot have a deterministic positive lower bound: the
finite-horizon no-code-fault event has positive probability, and clean scrubs
write nothing. Empty/tied regions also abstain. Positive EXPECTED O-write
counts are supportable conditional on a live, nonempty, correct developed bank:
there is a positive-probability single-symbol fault followed by an O offer and
an admitted unique correction. RL selects scrub with at least 1/48 probability
on any admitted selection, independent of its current Q row. For a periodic
candidate, every selected I has a due tick in 257..512, and an O offer at that
tick has positive probability. These show a possible nonzero denominator,
not a lower-confidence guarantee or a learned response to usefulness.

Under actual trained-state mixtures those premises must be checked. A zero
aggregate C or periodic-D O denominator remains undefined and cannot pass;
retain zero individuals and add no epsilon. Low obsolete spending through
empty storage, invalid queries, blanket forgetting, or failure is not H2.
R_U, intact prerequisites, activity/completion, and C-minus-D noninferiority
remain independent gates. Feedback-enabled ecology can include relearning.

The design is financially testable, but g=36 has not established the protocol's
strong functional statement that viable selective retention is attainable while
all-region retention is prevented. For REP fixed policies the stated resource
exclusion is actually false: they can fund all maintenance work. Retain the
matched opportunity comparison and disclose the twelve-per-source learning
overhead. Before calling H2 a validated scarcity mechanism, require an
authorized engineering control to check useful recall and the actual causal
conditioning/code-spend trade-off. Do not invent a new final policy product;
any extra scripted diagnostic needs a prospective version and accounting.

## Prospective power and interval sensitivity

These are stated-alternative calculations, not estimates from E3 or claimed
exact power for B05's percentile bootstrap. For an individual paired recall
difference with mean delta and standard deviation sigma, a normal planning
model gives SE=sigma/sqrt(n), half-width 1.96 SE, and approximate joint power
for the five-point point-estimate gate and positive lower interval:

$$
P_{\rm plan}\approx\Phi\left(
\frac{\delta-\max(0.05,1.96\,SE)}{SE}\right).
$$

Use this separately for H1-MAINT and H1-ADAPT; their effect/variance need not
match. No acquisition, functional, or activity prerequisites are included in
these contrast-only probabilities.

| n | Assumed paired sigma | 95% half-width | Power at delta=0.05 | delta=0.08 | delta=0.10 |
|---|----------------------|----------------|---------------------|------------|------------|
| 32 | 0.05 | 0.01732 | 0.500 | 1.000 | 1.000 |
| 32 | 0.10 | 0.03465 | 0.500 | 0.955 | 0.998 |
| 32 | 0.20 | 0.06930 | 0.293 | 0.619 | 0.807 |
| 256 | 0.05 | 0.00613 | 0.500 | 1.000 | 1.000 |
| 256 | 0.10 | 0.01225 | 0.500 | 1.000 | 1.000 |
| 256 | 0.20 | 0.02450 | 0.500 | 0.992 | 1.000 |

The threshold effect itself is not an alternative guaranteeing 80% power; its
point-estimate condition is near a coin flip even with a narrow interval. An
0.08 adaptive effect may also conflict with the clean-parent ceiling above.
Statistical power cannot create mechanistic headroom. The normal model ignores
boundedness, atoms/deaths, and nonnormal mixtures and must not be sold as exact
individual-bootstrap calibration.

For H2 let X_i be comparator O writes, Z_i D O writes, D_i=X_i-Z_i, and q the
required reduction fraction (0.5 for SELECT; 0.1 for PERIODIC). The ratio gate
requires mean X>0 and mean(D-qX)>=0. The lower interval uses D itself. Thus
general planning needs the joint law of X and D, including
Var(D-qX)=Var(D)+q^2 Var(X)-2q Cov(D,X). A mean ratio and Var(D) alone do not
specify power. With an explicitly illustrative FIXED X=40 per individual,
the cutoff becomes max(40q,1.96 sigma_D/sqrt(n)).

| n=32 assumed sigma_D | Absolute interval half-width | SELECT alternative 60% reduction, delta_D=24 | PERIODIC alternative 20% reduction, delta_D=8 |
|---------------------|------------------------------|-----------------------------------------------|------------------------------------------------|
| 10 | 3.4648 | 0.988 | 0.988 |
| 20 | 6.9296 | 0.871 | 0.611 |
| 40 | 13.8593 | 0.714 | 0.198 |

No actual comparator mean of forty is asserted. Normal approximations to write
counts are especially rough when variance is large or zeros common. At exactly
50%/10% effect, the ratio point-estimate rule again supplies no high-power
guarantee. Keep aggregate ratios and the positive-denominator rule unchanged.

For H2-RETAIN, with true mean loss ell=C R_U-D R_U and paired SD sigma_L,
approximate probability that its upper interval is <=0.05 is
Phi((0.05-ell-1.96 sigma_L/sqrt(n))/(sigma_L/sqrt(n))). At n=32, ell=0 and
sigma_L=0.10 or 0.20 give about 0.807 or 0.293; ell=0.05 gives 0.025, not
0.95 assurance. Joint H2 success cannot exceed its weakest required gate and
also depends on useful-recall/viability/prerequisite distributions not supplied
by the design. This is a genuine sensitivity result, not an omitted E3 power run.

## Gate disposition and freeze sequencing

| Item | Analytical disposition | What cannot be claimed here |
|------|------------------------|------------------------------|
| B06 reset expectation/missingness | Closed under canonical-empty and ideal indexed inputs | Production noninterference or generator audit passed |
| B06 32 x 8 erasure assurance | >=0.996306 per representation including guards | Generic dependent-output guarantee or exact bootstrap coverage |
| H1 supported finance | Conditional sourcewise funding established | Accurate acquisition, Q stability, or paid beneficial writes observed |
| H1 five-point maintenance | Wearing-assay reference has room | A positive RL contrast |
| H1 five-point adaptive increment | Clean-parent I=1 reference limits expected gap to about 0.0164 | Full trained-parent no-go, positive headroom, or selected periodic performance |
| H2 g=36 liveness/REP prefixes | Fundable with automatic conditioner lapses | Useful recall >=0.80 or intact recall >=0.90 |
| H2 scarcity mechanism | Full learning/update/conditioning combination excluded; fixed REP fully affordable | Forced U/O code-write scarcity or selective retention theorem |
| H2 denominators | Positive-probability correction under stated nonempty premises | Positive observed aggregate or valid ratio on every history |
| Gate power | Explicit variance/effect sensitivity supplied | Guaranteed joint power absent outcome-distribution assumptions |
| G-INFO / erasure structure | Finite-state induction specified | B07 review and runtime tests completed |
| Static operational closure | Outside this B06 scope; v0.6 lists pending traces | Full linked-ROM or every-service conformance |

The current contracts literally call genuine H1/H2 headroom a design-freeze
dependency. This note does not silently waive it. Recommended prospective
clarification: require financial/interface/estimand feasibility, analytical
ceiling warnings, fixed tests, and honest failure interpretation before design
freeze, NOT proof that RL will beat a competent periodic policy or meet every
functional gate. If the owner instead requires demonstrated positive attainable
headroom before that freeze, mark H1-ADAPT and functional H2 validation unresolved
and revise the process; do not label them analytically complete.

The consistent sequence is:

1. Finish static ROM/scan/RESPONSE/TERMINAL/AGE/CONDITION traces and B07 ownership,
   independent-input/reset specification. Resolve the narrow H2 scarcity claim
   and the performance-versus-procedure wording in a prospective contract.
2. Freeze the design and prespecified engineering/failure criteria. Preserve
   all existing scientific thresholds unless a separately justified prospective
   version changes the scientific question before data.
3. Separately authorize implementation. Validate actual service prefixes,
   scratch/scalar limits, simultaneous faults, row products, input ownership,
   and exact reset/replay. No engineering evidence may precede those gates.
4. Execute only the authorized engineering catalog; retain every failure and
   assess prerequisites/functional controls. Finite four-bit acquisition-to-reset
   tests do not cover the full sixteen-bit production model. Check all fields,
   each target-bit perturbation, cross-block histories, corrupt Q/body/ring/
   reserve, queued events, and dead histories with the compositional proof.
5. Freeze source/configuration/tests/analysis and selected H1/H2 configurations
   before independent final targets/roots. If a functional hypothesis fails,
   report failure or a new transparently versioned attempt, not repeated tuning
   until positive and no alteration of final sample after outcomes.

No freeze, implementation, engineering run, or final draw occurred here. Large
raw products and repeated negative histories are archival obligations, not
independent n or substitutes for noninterference. Full runtime validation cannot
be claimed before code exists; declaring that absence a perpetual pre-code
test failure would create an unnecessary circular requirement.

## Validation and computation provenance

Read-only PowerShell evaluated finite binomial recurrences (normalized at the
mode), majority polynomials, exact combinatorial gap sums, fixed four-source
debit worksheets, exponentials, and explicitly labeled normal-CDF approximations.
The binomial/gap expressions are exact finite mathematical laws; printed
decimal values are floating-point evaluations, not arbitrary-precision proofs.
No PRNG or bootstrap-index generation, Monte Carlo, simulator, target draw,
E3 implementation, experiment, or external data file was used.

During arithmetic checking, corrected PowerShell pipeline and array-expression
syntax and explicitly used floating-point arguments for Math.Max; an unintended
integer overload initially rounded a concentration bound. Only corrected,
rechecked numbers are reported above. One terminal response contained unrelated
output and was not used as B06 calculation evidence. All code was ephemeral
read-only arithmetic; the sole written artifact is this research note.

## Remaining research and decisions

* [ ] Independently review the canonical-empty induction and sufficient-event
  concentration proof against the final linked RESPONSE/guess input trace.
* [ ] Finish remaining static service/ROM and B07 ownership reviews; specify
  production conformance tests without claiming pre-code runtime passes.
* [ ] Prospectively clarify design-freeze wording: accept falsifiable performance
  hypotheses with disclosed headroom limitations, or explicitly retain the
  unresolved positive-headroom requirement.
* [ ] Decide whether H2 is a matched-opportunity allocation test with disclosed
  learner overhead, or requires a redesigned uniform scarcity mechanism.
* [ ] Only if broader fixed-output hardening is desired, version n=256 and audit
  the prespecified bootstrap weight matrix and all scaled products before draws.
* [ ] After separate authorization, run implementation conformance and the full
  engineering catalog; use new versions for any result-motivated redesign.

No further empirical fact can resolve the two design-interpretation choices
without an owner decision. No user clarification is needed to finish this
analysis. The decision questions for a subsequent version are whether to
freeze falsifiable H1/H2 failure possibilities and whether broader erasure
dependence protection is worth an eightfold final cohort. They do not authorize
editing any other file or running E3 in this session.