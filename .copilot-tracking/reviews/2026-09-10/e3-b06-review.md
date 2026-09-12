---
title: Independent E3 B06 mathematical review
description: Contract-grounded review of erasure assurance, H1 bounds, H2 budgets, and freeze claims
ms.date: 2026-09-10
status: Complete - qualified mathematical pass with two localized corrections; not freeze approval
---

## Scope

Review .copilot-tracking/research/subagents/2026-09-10/e3-b06-analysis.md
against the actual physical v0.4, policy v0.5, evaluation v0.7, and control
v0.6 contracts and their operative dependencies. Use deterministic closed-form
arithmetic only. Do not simulate, draw targets, modify contracts, or write any
other artifact.

## Questions under review

* Is canonical code erasure invariant, and is the asserted output law exact?
* Does the finite-event proof establish 0.996306 containment for the selected
  equal-panel, 32-individual, 10,000-resample procedure?
* Are the H1 adaptive ceiling, periodic lower bound, and query-gap indexing valid?
* What does H2 g=36 establish sourcewise, including gate fees and conditioner age?
* Are future randomness, paired suffixes, and freeze obligations stated accurately?

## Findings

Qualified mathematical pass. The main erasure bound, H1 reference calculations,
ordinary H2 prefix bounds, and aggregate resource exclusion reproduce. Two
localized corrections are required in any subsequent analytical revision.
Neither changes the primary 32-by-8 erasure-assurance result.

| ID | Severity | Disposition |
|----|----------|-------------|
| AN-001 | Moderate | Narrow H2 final-TD affordability: conditioning protects mandatory TERMINAL clearing, not its optional update |
| AN-002 | Minor | Correct two illustrative H2 PERIODIC normal-planning probabilities |
| AN-003 | Informational | Accept canonical-empty output law and finite-event bootstrap assurance, conditional on ideal inputs and service conformance |
| AN-004 | Informational | Accept H1 upper/lower expectations only in their stated REP and clean-reference scopes |
| AN-005 | Informational | Accept remaining H2 accounting; it proves financial opportunity costs, not selective-retention success |
| AN-006 | Acceptance condition | Preserve primary subset and future-input identity in any v0.8 revision; do not count reused suffixes as new observations |
| AN-007 | Acceptance condition | Analytical review completion is not design-freeze approval or evidence of positive H1/H2 outcomes |

No critical numerical or logical defect was found in the 0.996306 assurance
claim under its stated assumptions. That is a sufficient lower bound, not an
exact pass probability, a production-generator theorem, or a guarantee of a
future realized pass. The original analysis is unchanged by this review.

## AN-001 Mandatory terminal tail versus optional TD

Evidence: .copilot-tracking/research/subagents/2026-09-10/e3-b06-analysis.md,
lines 484-493; E3_OPERATION_CONTRACT_v0_3.md, lines 190-207 and 371-395;
E3_PHYSICAL_CONTRACT_v0_4.md, section "CONDITION-d and affordability-dependent
lapse"; E3_CONTROL_CONTRACT_v0_6.md, "Payment and mandatory remainder rules".

The quoted 29 ordinary / 34 final per-source REP envelope is a conservative
sum of potentially successful work, but the ordering matters. TERMINAL's
mandatory record clear consumes four material per source. Its optional Q
update consumes another two. The public future tail contains the mandatory
path, including the paid TD gate, not every optional future body. Gate fees
consume energy, not material. The controller's own terminal-shaped TD and the
separately scheduled end-of-phase TERMINAL are distinct services.

Thus, before conditioning on the final drain tick:

* Current work without code costs at most 23 per source, because there is no admission.
* Maximal conservatively quoted REP code work adds five at its selected source.
* Reserving mandatory TERMINAL clearing raises the busiest-source bound to 32.
* Reserving its optional TD too would raise that bound to 34, but the contract
  does not require conditioners to preserve those extra two units.

The statement that all ordinary preconditioning code/Q/admission work is
fundable at g=36 is sound. Extending it to guaranteed final optional TERMINAL
TD is not justified. "Conditioning gates reserve that TERMINAL tail" needs to
identify the mandatory tail rather than the six-unit full-success envelope.

A deterministic local gate worksheet exposes the distinction. Start a final
drain tick with 36 at each source and suppose the current learning work uses
23 each and no code writes. Conditioning begins at (13,13,13,13), protecting
four each for the mandatory clear. Applying the actual ordered body vectors
admits domains 0,1,2,3,4,5,6,7,9,11,13 and leaves (4,5,4,6). Optional terminal
TD would need six each including its later clear and must reject. Mandatory
clearing still succeeds. This is a static prefix worksheet, not a simulated
512-tick trajectory or an assertion that this starting vector must occur.

Required correction: retain conditional energy liveness, ordinary REP
correction/current-TD affordability, and mandatory terminal retirement. State
that final optional TD remains conditional on validity and post-conditioning
stock. Do not silently promote its two material units into the public reserve:
that would change the selected conditioning process. The aggregate inequality
in AN-005 already counts only actually admitted terminal updates and survives.

## AN-002 Two H2 planning-table values

Evidence: .copilot-tracking/research/subagents/2026-09-10/e3-b06-analysis.md,
lines 652-663. The displayed formula uses fixed comparator X=40, PERIODIC
fraction q=0.1, alternative mean reduction 8, and n=32. Therefore

$$
z=\frac{8-\max(4,1.96\sigma_D/\sqrt{32})}{\sigma_D/\sqrt{32}}.
$$

| Paired SD | z | Recomputed probability | Required three-decimal value | Current value |
|-----------|---|------------------------|------------------------------|---------------|
| 20 | 0.3027416997969522 | 0.6189566418647077 | 0.619 | 0.611 |
| 40 | -0.8286291501015239 | 0.2036571439600874 | 0.204 | 0.198 |

Two independent numerical CDF evaluations, a standard polynomial approximation
and deterministic composite-Simpson integration of the normal density, agree
at the displayed rounding. The SELECT column and SD=10 PERIODIC value reproduce.
These are corrections to an explicitly illustrative normal model, not revised
claims of exact bootstrap power or E3 observations.

## AN-003 Exact erasure law and bootstrap sufficient event

### Invariant and supported service path

Evidence: analysis lines 80-209; E3_STATE_CONTRACT_v0_2.md, code encodings and
delayed-query sections; E3_PHYSICAL_CONTRACT_v0_4.md, lines 261-297 and the
HS-AC support section; E3_POLICY_CONTRACT_v0_5.md, independent ranks and
readout-only guessing; E3_EVALUATION_CONTRACT_v0_7.md, lines 383-438 and
541-565; E3_OPERATION_CONTRACT_v0_3.md, RESPONSE and query-admission sections.

Canonical code is eighty 10 symbols. Sign faults and challenge faults swap
only 00 and 01; they never turn 10 or 11 into an observed binary symbol.
An erasure makes 10. More generally, an all-unobserved bank of 10/11 cannot
be populated by these faults or by legal empty-scan correction. The selected
reset starts with 10 specifically. Both REP and BLOCK scans abstain on the
empty bank, and a forced readout guess does not become a repair sign.
Corrupt Q changes action selection but cannot override this rule. No teacher,
ecological packet, Q-to-code operation, or retained callback supplies an answer.

Recovery g=47 and assay g=28, with canonical activation and paid boundary
ISOLATE, fund every required prefix and every conditioner under the v0.6
prices. The additional 256 controller energy applies to recovery, not assay.
This is conditional on service-trace conformance, not evidence of a completed
implementation. It gives activity and completion one on this reset path.

All twenty ages are reset before each simultaneous fault. A fault to an age
word cannot alter another fault probability at that same boundary. The next
fully funded pass again resets that word before probabilities are selected.
Consequently all relevant assay auxiliary bits have h=0.001 and lane erasure
e=0. No extra age-fault or auxiliary-erasure survival multiplier belongs in
the query-validity formula on this supported path.

### Exact missingness and conditional correctness

Admission at t sets valid=1; its response at t+5 precedes that tick's fault.
Exactly five independent valid-bit flips, at t through t+4, intervene:

$$
s=\frac{1+0.998^5}{2}=0.995019960039984,
\qquad q_v=1-s.
$$

Successive slot uses are overwritten and use disjoint bit/time fault indices.
Within a panel, $M\sim\operatorname{Binomial}(256,s)$ exactly under the ideal
law. Reserved bits do not authenticate a query, all sixteen cue addresses are
legal, and a corrupted address still scans empty code. Thus address errors do
not introduce an additional emission filter in this negative control.

Condition on targets, all planned schedules, validity events, and non-guess
inputs. Each emitted readout uses a different independent fair guess. Because
the bank stays empty and H1 has no feedback or controller, guess values do not
change availability, resources, later answers, or timing. Comparing repeated
fresh guesses with the same fixed label still gives independent fair correctness
bits conditional on that label. This is stronger than noninterference alone.

Hence, for every positive m,

$$
C\mid M=m\sim\operatorname{Binomial}(m,1/2),\qquad
\mathbb E[C/M\mid M>0]=1/2,\qquad
\mathbb E[C/256]=s/2=0.497509980019992.
$$

Guesses are indexed by planned service tick/slot, not emitted ordinal or
corrupted cue. Warm-up and recovery spurious responses cannot consume a later
planned response's guess. No missing output is filled by an evaluator guess.

### Finite-event assurance for n=32 and 10000 resamples

Let B require at least 244 emitted rows in every one of 32 x 8 primary panels.
This implies every panel's coverage is at least 0.953125, stronger than the
selected mean-coverage guard. Sum the upper missing-count tail directly:

$$
p_{\rm low}=P(M\le243)
=\sum_{k=13}^{256}{256\choose k}q_v^k(1-q_v)^{256-k}
=9.0086098783305\times10^{-10}.
$$

The independently evaluated recurrence used
$b_0=s^{256}$ and $b_{k+1}=b_k(256-k)q_v/((k+1)s)$, accumulating the tail
instead of subtracting a nearly-one CDF. Its total mass was 1 to reported
binary64 precision. No independence across panels is needed for
$P(B^c)\le256p_{\rm low}$.

For the actual equal-panel individual statistic
$A_i=(1/8)\sum_p C_{ip}/M_{ip}$, conditioning on each realized validity mask
on B leaves independent fair correctness bits with weights $1/(8M_{ip})$.
The squared weights sum to at most $1/(8\cdot244)$. Integrating this uniform
conditional bound over masks, then taking a union over 32 individuals, gives

$$
P(\exists i:\lvert A_i-1/2\rvert>0.05\mid B)
\le64e^{-2(0.05)^2(8)(244)}=64e^{-9.76}.
$$

When all 32 individual means lie in [0.45,0.55], every bootstrap resample mean
is a convex combination of those means and lies in the same interval. This
holds for any resampling-index matrix, including the future fixed 10000-row
matrix and its one-based order statistics 250 and 9750. Generating the matrix
is unnecessary for this proof. Its replicates need not be independent.

$$
P(\text{primary containment and guards})
\ge1-256p_{\rm low}-64e^{-9.76}
=0.9963060335629337.
$$

The exact finite expression supports the conservatively rounded claim
"at least 0.996306". The long decimal is a floating-point evaluation, not a
directed-rounding certificate for its last digit. A union bound for REP and
BLOCK together gives 0.9926120671258674; it assumes no cross-code independence.
There is no universal future-pass guarantee and no claim of exact nominal
coverage for the percentile-bootstrap method.

### Dependence sensitivity remains a different null law

If each cue instead always receives one fixed target-independent answer,
repeated queries do not add independent correctness bits. With complete
balanced coverage the total uses 16n independent label matches. The
illustrative fixed-normal-width containment probabilities reproduce:

| n | Probability |
|---|-------------|
| 32 | 0.2429169694558324 |
| 128 | 0.9902891179794220 |
| 256 | 0.9999916041869706 |

These are not exact percentile-bootstrap probabilities. The alternative
Hoeffding-width table also reproduces, including n>=47 for point accuracy
versus n>=185 for the split 0.025-center/0.025-radius criterion. The optional
n=256 fixed-bootstrap-weight bound reproduces as 0.880760186919946 with
coverage and 0.913415464269398 without missingness, conditional on the
unverified maximum kappa<=3 assumption. Its 250/251 tail counts are correct.
No change from n=32, no fixed-weight audit, and no new sample are authorized.

## AN-004 H1 expectations and the clean-reference scope

Evidence: analysis lines 315-450; E3_PHYSICAL_CONTRACT_v0_4.md, injury and H1
timing sections; E3_POLICY_CONTRACT_v0_5.md, fixed policy and clock sections;
E3_CONTROL_CONTRACT_v0_6.md, lines 274-300; E3_EVALUATION_CONTRACT_v0_7.md,
four H1 measurement stages and balanced schedules.

### The upper bound tolerates adaptive, correlated, wrong-address storage

For REP, condition on the entire arbitrary prechallenge bank, the target
table, and the realized scheduled and corrupted query addresses. Future
challenge/ordinary code flips remain independent of those quantities and of
routing faults on the fully conditioned assay. At response t,

$$
p_t=\frac{1-0.8(0.998)^{t-1}}2<1/2.
$$

Fix the scheduled target bit y. Each live symbol in whichever group the
damaged address selects has probability at most $1-p_t$ of equaling y.
The probability that majority decoding emits y, with a fair tie guess, is
coordinatewise increasing in these match probabilities. Setting every live
initial symbol to y therefore maximizes it. This pointwise argument does not
assume that a wrong-address group's stored value is independent of y.

For n observed symbols, fair ties give $A_0=1/2$, $A_2=A_1=1-p$,
$A_4=A_3=1-3p^2+2p^3$, and
$A_5=1-10p^3+15p^4-6p^5$. Moreover

$$
A_3-A_1=p(1-p)(1-2p)\ge0,\qquad
A_5-A_3=3p^2(1-p)^2(1-2p)\ge0.
$$

So partial erasure, invalid symbols, deliberately biased storage, cross-cue
correlations, and adaptive pre-assay compression cannot exceed the five-correct-
symbol upper bound for a single scheduled bit. The bank cannot realize the
best choice for every conflicting target/routed group simultaneously; ignoring
that restriction only makes the bound looser. It is not a BLOCK-code ceiling.

Averaging over 256 response times gives $U_5=0.9436811922676014$.
Independent valid-bit survival yields the generous planned-recall ceiling
$sU_5=0.9389816222205932$. The analysis does not need to assert wrong-address
chance accuracy for arbitrary adaptive storage, and it must not do so.

### Periodic I=1 reference and fault-count indexing

The reference stipulates independent fair target labels and three correct
post-lesion survivors at each cue. It is not the distribution obtained by
conditioning actual trained parents on an observed high-recall event. With
full-source H1 recovery, local P=255 at sensing and the v0.6 conservative E
bound is 60266, not the older one-C bound 60522. Both exceed every grid cut.
Thus I=1 actually scrubs every offer; it does not unexpectedly forage because
of low resources. Q corruption is irrelevant to the fixed rule.

For each cue, its eight positions are a uniform eight-subset of 1..128.
The nine empty gaps are uniformly distributed over nonnegative compositions
of 120, with marginal

$$
P(X=x)=\frac{{127-x\choose7}}{{128\choose8}},\quad 0\le x\le120.
$$

The first scrub has X preceding faults on three survivors. Between scrubs
there are X+1 faults on five symbols. After the last scrub, there are X+1
recovery faults, including the last scrub tick's fault. Adding t-1 assay
faults gives X+t in the final polynomial. These offsets reproduce exactly.

The clean-reference coupling is to a hypothetical truth-corrected process
only until the first miscorrection. Summing per-cue scrub-error probabilities
is a union bound, not an assumption of independent gaps or an allowed oracle:

$$
\eta=0.000909988649092265
+7(0.000102081276004102)=0.001624557581120977.
$$

Subtract eta once from each cue's expected ideal final accuracy, then average.
No factor of sixteen is required unless the claim is whole-bank correctness,
which is not this recall bound.

In this reference, fixed correction is label-complement symmetric and each
group's dynamics use its own target and target-independent faults/offers.
No resource shortage or Q-mediated selection couples target values into the
policy. A wrong-address group is consequently independent of the original
cue's label and has expected correctness one-half. This is a reference-only
argument, not a property of arbitrary learned parents. The four independent
address bits give original-address probability $s^4$, independent of validity.

| Quantity | Independent recomputation |
|----------|---------------------------|
| No-write correct-address mean N3 | 0.8305895549451855 |
| No-write planned recall | 0.8199493705509089 |
| Hypothetical last-scrub ideal mean | 0.9374361826816327 |
| Real periodic code lower bound | 0.9358116251005116 |
| Real periodic planned lower bound | 0.9225773564136511 |
| Periodic minus no-write expected lower bound | 0.1026279858627422 |
| Adaptive minus I=1 expected upper bound | 0.0164042658069421 |

The last bound is below 0.05 for this comparison of expectations. It is not a
pathwise bound on a realized cohort, a proof that future G-H1-ADAPT must fail,
or a statement about the actual selected periodic candidate. Trained parents
differ, intact recall >=0.90 is not all-replicas-correct, and finite engineering
ranking need not choose I=1. The analysis already gives these qualifications.
Its beta coupling threshold 0.0335957341930579 is a necessary condition under
the stated I=1 coupling, not an empirical bound on parent defects.

## AN-005 H2 financial bounds and their limits

Evidence: analysis lines 454-616; E3_OPERATION_CONTRACT_v0_3.md, transaction
admission and ledger; E3_PHYSICAL_CONTRACT_v0_4.md, conditioning and material
laws; E3_POLICY_CONTRACT_v0_5.md, frozen-work savings; E3_EVALUATION_CONTRACT_v0_7.md,
H2 budget and windows.

The first g=36 grant restores the post-ISOLATE P=242 to cap 255. Subsequent
live ticks have at least 36 per source. Optional gates cannot spend public
mandatory tails. Conditioning follows ordinary actions/response/admission
and paid age increments. A rejected body still pays its gate/control/clear
energy, but consumes no material; age increments still consume ten per source.

The full BLOCK energy envelope, including final leakage and conservatively
both final TERMINAL and admission, is
$29394-4(66-36)+1=29275<30000$. Lower material can reject optional work, not
invalidate this energy upper bound. Mandatory age/retirement work stays funded
on eligible code-only H2 paths, including zero residual material and typed
leakage $\min(P_j,1)$. This is not revival after death or an injury guarantee.

The ordinary learning maximum before optional conditioning is 24 per source:
old clear 4, store 4, current Q update 2, reward finalization 2, slot clear 1,
admission 1, age increment 10. A conservatively quoted REP five-write scrub
raises only its source to 29. BLOCK's twenty-write quote can reach 44 and
its prefix may stop. These are safe upper envelopes, not claims every quoted
maximum is simultaneously reachable. Apply AN-001 for the final update.

At full conditioning, ordinary no-code learning consumes 40 each including
leakage; dropping current TD reduces this to 38; fixed/frozen no-record paths
consume 28. A fixed/frozen REP path with the conservative five-write maximum
costs at most 33 at the busiest source. Since 33<=36, its full-start induction
pays all maintenance and all conditioning every tick. This disproves forced
financial all-region maintenance scarcity for that comparator, not guarantees
accurate recall or absence of miscorrection.

Both reported ordinary low-stock conditioner worksheets reproduce exactly:

| Earlier code debits at source 0 | Admitted domain IDs | Final vector before leakage |
|--------------------------------|---------------------|-----------------------------|
| 0 | 0,1,2,3,4,5,6,7,8,9,10,11,12,13,15 | (0,0,0,3) |
| 5 | 0,1,2,3,5,6,7,9,11,13,15,17 | (0,5,1,1) |

They use the actual cross-source age-write vectors, not a three-unit pooled
price or eleven policy-chosen domains. Domain choice is automatic, fixed-order
affordability. A lapsed domain retains its paid incremented age, at least one
before the fault, so h>=0.002 and e>=0.0001 there. No hidden condition action
or free vector of ages is assumed.

For a path with every DECIDE, current-record finalization, all 507 admissions,
and all twenty conditioners, maximum passive supply is 18651 per source.
Even allowing eight collected material on every tick, ignoring incompatibility
with scrub and all later cap losses, total supply is at most 78700. Required
work excluding Q updates, code writes and leakage is
$4[512(36)+507+4]=75772$. Therefore

$$
8U+W+\Lambda\le2928.
$$

This necessary inequality excludes all 512 possible Q updates plus full
conditioning: 8(512)=4096>2928 even before code and leakage. It does not
exclude all-conditioned fixed/frozen policies or learning paths that drop
updates/records. The twelve-per-source ordinary learner overhead is real.

No-code-fault paths have positive probability, so positive realized obsolete
write denominators are not deterministic. Positive expected writes require
the stated live/nonempty-bank premises and a positive-probability fault,
offer, scrub-selection, and admitted correction sequence. RL's exploration
gives scrub at least 1/48 on an admitted selection; periodic candidates have
due opportunities in 257..512. These support possibility, not denominator
confidence, learned selectivity, or useful-retention success. Zero aggregate
comparators must remain undefined, without epsilon or deleted individuals.

## AN-006 Shared reset suffixes and prospective v0.8 compatibility

The primary erasure subset in E3_EVALUATION_CONTRACT_v0_7.md, lines 416-438,
is the H1-family RL developed-boundary child: eight panels for each of 32
individuals, reported separately for REP and BLOCK. Every other history's
negative is structural/diagnostic, not another independent label table.

At fixed G, individual, panel, and canonical target-independent future Z,
different parent histories must produce identical reset state trajectories
and predictions. Their scores agree when evaluated against the same labels;
under target counterfactuals the predictions stay fixed but scores can differ.
Parent equality checks therefore cannot be replaced by generating independent
post-reset noise for each parent. Reusing the canonical suffix supplies no
additional n or bootstrap precision.

The in-progress B05 revision note proposes reset representatives and narrower
workload. No completed v0.8 contract was available at the inspection point.
The primary proof remains valid prospectively if that revision:

* Keeps all 32 independent final target tables and all eight distinct primary
  panels, with independent ideal planned guess coordinates across those panels.
* Preserves the powered statistic, zero-emission rule, guards, 10000 paired
  individual resamples, and percentile positions.
* Constructs and checks every required parent reset against the same canonical
  state and future-input identity before reusing an identical suffix result.
* Does not reuse one panel's guesses across all eight primary panels or add
  parent/candidate-outcome IDs to reset-future keys to manufacture independence.
* Keeps G fixed for each counterfactual, freezes engineering-selected constants
  before independent final targets, and keeps target/future roots inaccessible.

The ideal probability proof is not a claim that deterministic HMAC bytes are
information-theoretically independent. Actual CNG provenance, unbiased mapping,
namespace separation, and execution conformance remain B07/implementation
obligations. No target or root was generated in this review.

## AN-007 Freeze disposition and unresolved scientific claims

The review answers the mathematical questions; it does not waive the literal
v0.7 design-freeze dependencies. E3_EVALUATION_CONTRACT_v0_7.md, lines 858-920,
still requires B06-H1/B06-H2 closure and static/ownership review before freeze.
E3_PROTOCOL_v0_1.md requires scripted functional controls before final seeds,
not proof of positive results before implementation exists.

The analysis correctly distinguishes:

* Financial and input-law feasibility from useful recall, accurate acquisition,
  adaptive superiority, or selective obsolete spending
* Static specified traces from future implementation conformance and runtime tests
* A technically valid, scientifically negative experiment from a technical failure
* A prospective clarification of procedural acceptance from silently relaxing
  the original numerical scientific gates

No positive RL-versus-periodic effect, H2 useful-retention outcome, or future
bootstrap pass is established here. Conversely, failure to prove those positive
outcomes analytically is not proof that all trained-parent hypotheses must fail.
If prospective v0.8 separates procedural design acceptance from experimental
performance, that change must be explicit. Preserve independent final data,
both freezes, full failure reporting, and the existing scientific thresholds
unless a separately justified prospective version changes the question.

## Numerical evidence and provenance

All principal finite binomial/gap sums and polynomials were recomputed using
ephemeral read-only PowerShell. Additional checks covered all dependence-
sensitivity tables, bootstrap kappa bounds, H1 planning rows, H2 SELECT rows,
and useful-retention normal-planning values. Only AN-002 differed at reported
rounding. Normal planning remains an approximation; none of these calculations
is a simulation, target draw, empirical observation, or executed service trace.

The first arithmetic command failed to parse a method call on an ordered
hashtable. Parenthesizing the hashtable expression fixed it; only the completed
rerun supplied numerical evidence. No output from the failed call is used.
This syntax pitfall is recorded here, not in another memory/file, to honor the
single-artifact write constraint.

The review read the full analysis and seven baseline contracts (state,
operation, physical, policy, control, evaluation, protocol). B05 revision and
B07 review status were inspected only for coordination; their in-progress
conclusions are not substitutes for independent mathematics. Incorporated
instruction-by-instruction service traces were not independently re-audited.

Read-only SHA-256 evidence identities, not a freeze manifest:

| Workspace-relative input | SHA-256 |
|--------------------------|---------|
| .copilot-tracking/research/subagents/2026-09-10/e3-b06-analysis.md | C7ECD3D39A227A73C1B433EA35318C84667626BCC416552AB6F66E0EC6396303 |
| E3_PHYSICAL_CONTRACT_v0_4.md | F0F05D57B5F98C171FF2956CA4BDFD00A59EDFB3579D3FBE05FB74C8001E1DC8 |
| E3_POLICY_CONTRACT_v0_5.md | FE174D0BDB8D8D22583E426CF74EBB680D8D471A8C447F906A104819DED791CF |
| E3_CONTROL_CONTRACT_v0_6.md | 198C96C610D0FD89F9990836AD8B6D68ACA13580B9ECAD80B55CB5BE962AF060 |
| E3_EVALUATION_CONTRACT_v0_7.md | EA3698BDB595B66EEEBF8F50A75B6514166BDFDB7BBAAA16C6392E7EF6E0DAE3 |

No simulator, PRNG, bootstrap-index generator, target generator, E3 code,
experiment, or external data source was run. Only this review document was
created/edited; the analysis and all contracts were left unchanged.

## Recommended next work and clarifying questions

* [ ] Incorporate AN-001's mandatory/optional terminal distinction and AN-002's
  two numeric corrections in a separately authorized analytical revision.
* [ ] Verify the completed prospective v0.8 text preserves AN-006's primary
  subset, canonical future-input identity, and no-fake-independence conditions.
* [ ] Finish/adopt the separate static service/ROM and B07 ownership reviews;
  do not treat this mathematical review as their replacement.
* [ ] Resolve procedural design-freeze wording explicitly before claiming
  closure; retain performance hypotheses and failure outcomes as experimental.
* [ ] After separate implementation authorization, validate exact service/input
  conformance and execute only the prespecified engineering controls/catalog.
* [ ] Audit n=256 bootstrap weights only if broader fixed-output protection is
  prospectively selected; it is not required by the reviewed canonical null.

No user clarification is required to finish this review. The downstream owner
decision is whether a new version accepts falsifiable H1/H2 performance with
disclosed financial and clean-reference limitations, or retains a stronger
positive-headroom design requirement. Neither choice is made by this review.