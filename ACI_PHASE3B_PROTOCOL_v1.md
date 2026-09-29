---
description: Design-only Phase III-B H5-H7 H9-H10 H13-H14 protocol with six primary comparators and external controls
ms.date: 2026-09-28
---

# ACI Phase III-B protocol v1

## Status, dependency, and single question

This is a **prospective design**, not a frozen executable or a neural result.
It creates no runner, hash, results directory, engineering outcome, or final
verdict. H0-H4 are [transition](PHASE3B_TRANSITION_v1.md),
[channel definition](COMPETITIVE_ACCESS_DEFINITION_v1.md),
[world](PHASE3B_ENVIRONMENT_v1.md),
[specialists](PHASE3B_SPECIALISTS_v1.md), and
[identifiability](PHASE3B_IDENTIFIABILITY_v1.md). H8 is the
[competition signature](PHASE3B_COMPETITION_SIGNATURE_v1.md), H11 the
[reduction review](PHASE3B_REDUCTION_REVIEW_v1.md), and H12 the
[theory mapping](PHASE3B_THEORY_MAPPING_v1.md). They are dependencies, not
results to be inherited from the frozen Phase III experiment.

The single testable hypothesis is conditional: at a fixed training-example
allowance, optimization recipe, **measured** train/inference compute and
parameter caps, a learned port-partitioned competitive-access candidate has
lower held-out-context joint decision loss than the strongest *independently
trained* primary comparator, including the fixed-selector workspace ablation
R4 and all five no-workspace rivals. This is a training-regime/inductive-bias
hypothesis, not an impossibility result for unrestricted encoding. R9 can
simulate every candidate policy at the same wire budget; its constructive
clone is an expressivity control and will tie by design. If an intrinsically
unique occupancy advantage is required, STOP before training.

H5-H14 here freezes *design choices only*. Executable code, instrumentation,
hashes, configuration manifests, and final-run authorization belong to
H15/H16; neither is claimed or preempted by this document.

## H5: the candidate and the information contract

Draw four independent fair latent bits per episode. At sensory ticks 0-7,
publicly scheduled port `j` appears at ticks `j-1` and `j+3` (one-based
`j=1..4`); each reading is a fresh BSC(1/5) copy. Decisions occur at ticks
8-11 with public context `c=t-8` and null common observation. At context
`c`, S1 targets factor `1+c`, S2 targets `2+c`, and S3 targets the parity of
factors `3+c` and `4+c` (indices modulo four, in `1..4`). Each specialist
receives only its own new independent BSC(1/5) local reading of its target
(S3 reads the first parity factor), context, and the *same* three-bit word.
S1 incurs unit immediate error; S2 may bet 0/1 or abstain at loss 0.18,
irrevocably settled one tick later (including a terminal settlement at 12);
S3 incurs unit parity error scored at episode end. No pending truth or prior
local bit is fed back into any arm. Public time, context, schedule, and loss
ledger are identical for all arms.

The candidate learns four separate recurrent port states from their own
port observations; the selector sees those four states and current public
context, but **not** local sensor bits or latent truth. It emits one address
`0..3`; only that port emits a quantized payload bit. On wire the address
is two bits and payload one bit, exactly eight words, overwritten once per
decision tick, no blank word and no sequential reads. All heads are
separate learned, stateless decision processes except S2's pending-action
ledger; no head sees a port state, selector logit, other head's sensor, old
word, actions, rewards, raw common history, or cached belief. Private port
states persist for free in this phase; there is no paid maintenance or
integrity state. Source ports are a supplied inductive bias, not latent
labels learned without structure. Learned content is acquired from noisy
observations; at evaluation neither factors nor evaluator posteriors enter
any forward graph.

## H6: rival identities and comparison status

Every independently trained comparator has the same observation episodes,
public information, local sensors, losses, and permissible learning labels.
Only R4/R9 and the candidate have an eight-word wire; the bypass and
representation bandwidth of other arms are disclosed rather than disguised
as information parity. The following IDs and names are binding throughout
H5-H14. R5/R6/R7 are evaluator-only EXTERNAL controls and optional R10 is
an analytic control; none is an independently trained primary win.

1. R1 unlimited learned broadcast: independently train port-partitioned
   recurrent representations from common observations and broadcast *all*
   learned port states to three separate legal local-input heads. No selector
   or three-bit bottleneck. "Unlimited" describes the read bandwidth, not
   an exemption from matched total parameters, compute, samples, or measured
   memory. Sweep larger uncapped versions separately as Pareto controls.
2. R2 monolithic recurrent: independently train one full-history recurrent
   trunk with three distinct action heads. Each head receives only its own
   legal local bit and public context at decision time; no local bit enters
   the shared trunk or another head. No address or workspace. Include
   matched and separately labeled larger-capacity variants.
3. R3 private-state specialists: independently train three private recurrent
   common-history encoders, one per specialist, with no shared state or word.
   Each also reads only its own legal local bit. Count all three encoders and
   heads against the *whole-arm* cap; disclose a larger private-copy sweep.
4. R4 fixed-selector workspace: independently train four port states,
   one-bit port payloads and local-input heads with the candidate's exact
   three-bit `(address,payload)` channel. Select the address only from public
   context/clock, never from observations or learned states. Sweep all four
   constant addresses, context-specific maps and deterministic clock routes
   (including cyclic/equivariant rotations). Train its encoders and heads
   from scratch with a public, history-independent balanced round-robin of
   the four addresses across the same 8,192 training episodes; then evaluate
   all 4^4 deterministic context maps against the *training* contexts with
   frozen weights. Cache the four per-context source losses once on the
   training histories, then enumerate route scores from that table rather
   than rerunning 256 networks. Pick the best route by engineering scores,
   breaking an
   unobserved-context tie by setting the context-3 address to one plus the
   selected context-2 address modulo four, then lowest address for any
   remaining ties. Do not select context 3 by its held-out loss. Count
   round-robin exposure and route search work.
   This is a fixed-selection *workspace ablation*, not a no-workspace arm;
   do not cripple its learned contents or sweep.
5. R5 oracle belief broadcast EXTERNAL: evaluator-supplied exact four-counter
   posterior with unlimited read bandwidth to each Bayes local-input head.
   It is an information ceiling (risk floor), not an autonomous comparator.
6. R6 oracle selector over learned latents EXTERNAL: freeze a trained
   candidate's four learned port states, quantizers and heads. Using
   evaluator-only conditional expected loss for each legal source word,
   select among the four addresses at fixed latent contents and use the
   selected port's payload. Disclose whether local bits are integrated out
   (selector-compatible oracle) or revealed (stronger clairvoyant diagnostic).
   No posterior, latent truth, or oracle choice enters any learned forward
   path; R6 is a selection-headroom bound, not an autonomous win.
7. R7 independent sufficient-statistic copies EXTERNAL: the evaluator
   supplies a separate exact four-counter belief copy to each specialist,
   with its own legal local bit and Bayes head. There is no shared word or
   learned encoder. This is a full-information guard against treating
   common read access as essential. If copies are instead learned, call
   that a separately budgeted learned variant; do not call it R7 or count
   oracle-supplied copying as an independently learned result.
8. R8 learned shared encoder without bottleneck: independently train one
   recurrent full-history encoder with a shared, unquantized learned vector
   delivered to separate stateless local-input heads. Unlike R1 it learns
   one shared representation rather than broadcasting four port states;
   unlike R2 it does not jointly recurrently process the heads. Matched
   resource and larger-vector sweeps are required; no named occupancy.
9. R9 equal-budget unrestricted learned eight-symbol encoder: independently
   train an unconstrained encoder of the same common history and public
   context into *any* of eight words, received by identical local-input
   heads. Address bits may encode arbitrary aggregate data; no truthful
   source semantics are imposed. Permit the candidate's port partition and
   equivariance as swept subfamilies, with the exact candidate graph as an
   allowed subfamily at the same wire, parameter, compute, sample and search
   caps. Copy a trained candidate into this subfamily and verify identical
   messages and outputs on all discrete observation/context/local-bit inputs
   or with an equivalent certified construction. Report actual resource
   counts. The constructive clone ties by design but is **not** an
   independently trained win; training R9 from scratch is compulsory.
10. Optional R10 analytic bounded-code oracle EXTERNAL: if computationally
    certifiable, optimize an arbitrary eight-symbol code using full
    four-counter belief and public context with both possible values of
    each independent local bit, all three action maps and the actual losses.
    Include costs across all decision ticks if coupling is claimed. Publish
    the codebook and exact certificate or label the solver gap unresolved;
    neither an uncertified number nor a certified oracle is a primary win.

The strongest independently trained primary comparator within each seed
comes from **all six** R1/R2/R3/R4/R8/R9 families at the primary resource
cap. R4's fixed-selector workspace is included as an ablation; the other
five are no-workspace alternatives. R5/R6/R7 and optional R10 are external
guards, not members of that envelope. Inability to implement, train, or
meter a compulsory primary family is an H15/H16 pre-final STOP, not
permission to omit it. A candidate-only structural lesion cannot substitute
for a performance win against these independent comparators.

## H7: training, matching, and locked primary endpoint

Freeze **before any scored results** the primary endpoint: at held-out
context `c=3`, mean per-episode joint loss
`L=(loss_S1+loss_S2+loss_S3)/3` over every planned evaluation episode.
Smaller is better; each component lies in `[0,1]`. Training episodes
terminate after context `c=2` (tick 10), so `c=3` and its feedback never
receive a training gradient. At evaluation run through tick 11 and settle
S2 at tick 12. All arms receive the same public rotation rule; allow
identical parameter tying/equivariance to R1/R2/R3/R4/R8/R9. The held-out test is
generalization of this specific rotation, not a new latent environment.

The feasible primary budget is at most **4,096 trainable parameters**,
**80,000 forward multiply-accumulates per 12-tick episode** (count other
arithmetic, branches, storage, and memory traffic separately), and **8,192
training episodes** per independently trained configuration. Use batch size
32, exactly 256 optimizer updates, the same loss normalization and objective
in every learned arm. Use engineering training seeds 0-3 and a separate
fixed 16-seed final run. Six configurations per family and four engineering
seeds give 24 engineering fits per learned family; candidate plus six primary
families require 168 such fits before the 112 final fits. Final candidates
reuse engineering-selected configurations, not engineering weights. This
bounded plan replaces an infeasible 131,072-episode, 12-configuration,
eight-engineering-seed design; report observed cost before H15/H16 execution.
Count four streams, selector, message construction and all heads for the
candidate, and all private encoders and heads for rivals. Report wall time,
total forward/backward training compute, peak and recurrent memory,
parameter count, inference operations, and trial/search spend. All caps
apply to a *whole* arm, never per specialist. Offer 2,048 and 8,192
parameter levels and 1/4 and 4 times the primary compute/episode caps as
secondary Pareto sweeps, resources permitting; no secondary level replaces
the primary comparison. A non-fitting candidate or R9 at the primary cap
is a design STOP, not grounds to waive R9. Larger information-rich rivals
must be cost-labeled separately from the matched primary result.

All learned arms use AdamW (zero weight decay), no dropout, gradient-norm
clip 1, and the same on-policy likelihood-ratio objective: sample legal
message/action tokens where present, use each specialist's observed scalar
loss as its training signal, and use an exponential-moving-average baseline
per consumer/context (decay 0.9, no learned baseline). Decision evaluation
uses deterministic maximum-probability tokens with the lowest-index tie
break. Score only observed losses, never feed the four truth bits or
posterior to a network. Fix six configurations per learned arm: learning
rate in `{0.0003, 0.001}` crossed with the three largest feasible widths
nearest 50%, 75%, and 100% of that arm's **total** primary parameter cap.
Freeze exact widths, tied dimensions, and counts before engineering. Reject
a configuration above either cap rather than silently granting a larger
budget; if a family has no feasible declared grid or exact R9-clone
subfamily, STOP and version the design. Select one configuration per family
solely by aggregate engineering performance at training contexts `c=0,1,2`,
with the lowest parameter count and then lowest learning rate breaking ties.
Do not select a winner using held-out `c=3` engineering diagnostics or
any final data. The R4 contextual routing sweep is enumerated rather than
weakened to a single arbitrary route; external analytic controls are
reported separately. Engineering may diagnose feasibility,
variance, and wiring; if its results require changing caps, grid, labels,
losses, or the primary endpoint, version and readmit a new protocol before
finals. No oracle posterior or latent labels are inputs to learned agents;
optional training-only supervision requires the same labels for *every*
learned rival and a separately declared equal-budget experiment.

The minimum meaningful primary reduction is **0.02** absolute joint-loss
units (not a percentage of the rival loss). For final seed `s`, let
`d_s=min_{r in {R1,R2,R3,R4,R8,R9}} L_{r,s}-L_{candidate,s}`, with the
rival minimum taken **within** that seed over all six independently
trained families at their preselected primary configurations. No EXTERNAL
control or copied R9 clone enters this empirical envelope. The sole value
gate requires at least 14 of 16 final seeds with `d_s>0.02` *and* a
two-sided exact sign-test `p<=0.01` for improvement over 0.02, with ties
at exactly 0.02 omitted only from the sign-test denominator, not counted
as gate successes. A mean-only improvement, lesion-only separation, or
subset-of-rivals improvement is a failure. To avoid floating-point tie
ambiguity, accumulate per-episode joint loss in integer units of 1/150
(S1/S3 errors = 50, S2 wrong bet = 50, S2 abstain = 9); compare seed means
and the 0.02 threshold (=3/150) by exact integer cross-multiplication.
The endpoint, effect threshold, gate, envelope membership, and loss
weights do not change after seeing engineering or final outcomes.

## H9: seven causal interventions and leakage controls

Use `L` for the four frozen candidate learned port-state vectors and `W`
for the intact three-bit shared word. Replay identical histories, local
signals, parameters and RNG. Before each intervention prove a no-op hook is
byte-identical to intact words, actions and permitted state. Report all
consumer responses (both local-bit values per head), each component loss,
word transitions, and first divergence tick. Counterfactual hooks are
diagnostics *outside* the intact wire alphabet, never new legal messages.

1. I1 occupancy substitution hold L: substitute the two address bits at
   the consumer read point while keeping the original payload bit and all
   four learned states `L` fixed. Compare each other address and the
   context/clock fixed R4 address on H3's prespecified matched histories.
   This address-only test can create off-policy words; report changed action
   maps and regret but do not relabel address bits as semantic source proof.
2. I2 blank W preserve L: withhold `W` from all heads at the read boundary
   while preserving all `L`, selector state, local bits and public context.
   Use a separate out-of-band ablation token/flag on the diagnostic head
   input, **not** a ninth intact message, learned blank symbol, or extra
   on-wire timing event. Train and report a diagnostic no-message readout
   with the same budget when scoring losses; otherwise report responses
   only. The intact protocol still has exactly eight words.
3. I3 force selector: at fixed `L`, context and local bits, force each of
   four selector addresses *upstream* of payload production and recompute
   the legal one-bit payload from that selected port. Score both local-bit
   response maps and three losses. Unlike I1, this tests each intact legal
   source/payload pair, not an address-only read substitution. Compare the
   best fixed R4 route and EXTERNAL R6 selection-headroom diagnostic.
4. I4 capacity expansion frozen representations: freeze `L` and sensory
   encoders; increase the common word from three to four, eight and sixteen
   bits in separately trained diagnostic selector/quantizer/heads with the
   same training episodes and disclosed added resources. Compare all three
   losses and local-to-action maps. Expansion changes the contract and
   never enters the primary eight-word gate.
5. I5 unlimited conversion: freeze the same `L` and bypass the word to
   deliver all four learned states simultaneously to newly trained separate
   heads with legal local bits. Use equal training episodes and report new
   head parameters, computation, memory and read bandwidth. Contrast with
   I4 and R1; this probes retained learned evidence, not an EXTERNAL Bayes
   bound or an intact-channel success.
6. I6 specialist-specific cut: withhold `W` at exactly one specialist's
   read boundary, leaving its local bit/context, upstream `L`, and the
   other two heads' *same* intact `W` unchanged. Use the I2 out-of-band
   no-message diagnostic token only on that cut head; record its readout
   status and assert byte identity for both unaffected heads and `L`.
   Repeat for S1, S2 and S3; no blank ninth intact word is introduced.
7. I7 latent corruption: replace one port's `L_j` with its paired-history
   state (or a prespecified matched-magnitude perturbation) while holding
   other `L`, context and local bits fixed. Recompute the selector and
   `W`; repeat for all four ports, including corruptions that leave `W`
   unchanged. A changed consumer output without a changed word indicates
   a forbidden side path. Report whether the changed local-to-action maps
   agree with the actual new on-wire bits, not decoded latent labels.

Optional leakage tests replay the same `W`, context and local bit while
severing every other upstream link to candidate heads: outputs must remain
byte-identical. Audit prior words/actions, feedback, selector logits,
cached state, timing and other hidden paths. Optional same-word tests inject
one *legal* alternative three-bit word for all heads at a common read event,
then only one head, and verify that the untouched heads read identical bits.
Apply the word substitution also to R4 and R9; ordinary code use is not
candidate-exclusive. Include no-op and negative-control histories where
`W` stays fixed. For rivals without the relevant port or word, mark the
structural lesion **not applicable**, not a loss, and use only a comparable
input perturbation if one exists. Only the H7 gate tests rival-exclusive
value; an intervention cannot overturn a primary rival match.

## H10: coordination, transfer, and diagnostics

Report per-seed and per-context S1, S2 and S3 losses, S2 coverage and
conditional wrong-bet rate, S3 parity errors, total joint loss, and action
disagreements under identical earlier histories and matched local signals.
If shared words produce a coherent but wrong response, count its loss;
zero incoherence by construction is not economic value. Tabulate address
entropy, payload entropy, per-port use, conditional information about each
factor, source-state decoders, and whether two address bits encode aggregate
decisions. Never infer semantics from a decoder alone. Label the I1-I7
counterfactual readouts and I4/I5 capacity changes separately from the
intact endpoint.

As a **secondary**, access-matched transfer diagnostic, freeze every arm's
common-history encoder and original heads, attach an equal-capacity new
read-only head to predict factor 4 with a fresh private BSC(1/5) reading
at context 0. Train only that head on 2,048 separate training episodes;
evaluate on 4,096 disjoint episodes per final seed. Give each new head only
its arm's *intact consumer interface*: candidate/R4/R9 see their three-bit
word, R1 sees its port-state broadcast, R2 its shared trunk, R3 one
declared private representation, and R8 its shared learned vector. A
candidate/R4/R9 read of hidden encoder state is a separately labeled
bypass diagnostic, not an access-matched comparison. R5/R6/R7 and optional
R10 may be reported as EXTERNAL reference controls, never as learned
transfer wins. Report
samples-to-risk, original-head byte identity, and *all* extra read bits,
parameters and training/inference work. Neither zero retraining of a
frozen core nor a candidate-only consumer-cut is a success gate. If a
no-workspace frozen representation matches transfer at no greater cost,
the transfer story reduces to ordinary representation reuse.

## H13: statistics, freeze and stopping rules

Use model seed as independent replication unit, pairing all arms on the
same evaluation histories. Engineering training seeds are **0-3**; final
training seeds are **1000-1015**, disjoint from engineering and from the
prior Phase III final family. Within each final seed use a fixed independent
evaluation RNG stream `20000+s`, 4,096 held-out episodes for context 3,
and separate streams `30000+s` for transfer episodes. Episode draws,
counterfactual histories and local-bit variants are repeated measures,
not additional independent seeds. Record the exact generated seeds,
evaluation denominators, configuration selection and all failed runs.
No engineering seed enters the final hypothesis test.

For each of 16 paired final seeds compare the exact integer loss
accumulators to the threshold as defined in H7. Let `w` be the number with
`d_s>0.02`, `l` the number with `d_s<0.02`, and `t=16-w-l` the exact ties.
The two-sided exact sign-test uses `n=w+l` and
`p=min(1, 2*sum_{k=0}^{min(w,l)} C(n,k)/2^n)`. Pass only if `w>=14`
**of all 16** and `p<=0.01`; ties reduce `n` but never count toward 14.
With 16 non-tied seeds, the smallest two-sided p is
`2/2^16 = 0.000030517578125`; for 14 positive and two negative seeds,
`p=2*(1+16+120)/2^16 = 0.004180908203125`; for 13 positive and three
negative, `p=2*(1+16+120+560)/2^16 = 0.021270751953125` and the gate
fails. With ties report `n` and its minimum possible p (`2/2^n`, for
`n>0`); if `n=0`, report `p=1`. Never report `p=0`. Also report all
per-seed differences, median, mean, 95% exact binomial confidence interval
for the positive fraction, and costs/secondary endpoints without a
retrospective significance gate. The exact sign test addresses the median
under independent seeds and a null sign probability of at least one-half;
it is not a proof of mean superiority or of architectural necessity.
The single primary comparison is preadjusted by the within-seed strongest
rival envelope. Secondary comparisons and seven lesions are descriptive;
no new confirmatory gate may be mined from them.

Before any engineering neural run, validate H3's 27 functions against
implemented losses and both values of each local bit, enforce eight legal
words and zero consumer side channels, and verify R9's simulation
construction. If any fails, STOP and issue a versioned correction, never
train through a failed premise. Engineering is a nonconfirmatory wiring
and feasibility screen, not a preliminary final. H15/H16 must first
implement and verify source and dependency hashes, exact configurations,
declared seeds, dataset generator, resource instrumentation, full I1-I7
plan, gate, and fresh results directory created without overwrite before
any executable/final freeze. This design document supplies no such hashes
or runnable artifact. If equal-budget R9 cannot fit or any of the six
primary comparators cannot be implemented, STOP.
No optional stopping, extra final seeds, changed endpoint, tuned rival
exclusion, or post-result world change is permitted. A protocol change
requires a new version and untouched old record. This v1 document itself
does **not** perform that execution freeze.

## H14: independent audit and verdict boundaries

After H15/H16 an independent audit must verify source hashes and actual
seed families, rederive H3, reconstruct wire alphabets/visibility, reproduce
intact state hashes and sampled runs, recompute all joint losses and exact tests
from raw per-seed data, include every eligible rival in the envelope, and
check the R9 cloning demonstration and resource meter. Report missing
arms, failed byte-identity, R4 sweep gaps, optional R10 solver gaps, or
conditional subgroup selection as failures or limitations, not silent
exclusions. Finals and verdicts are **not authorized or performed here**.

If the primary gate fails, publish a bounded negative and retain the
scarcity proof. If it passes, report only conditional training-regime
value in this environment; R9's function-class inclusion and R5/R7's ideal
full-information bound still hold. No old frozen artifacts are changed.
No N1/N3/N4/N5, O3 workspace-seat, organism, autopoiesis, or
consciousness claim is licensed.

## Ten constitutional admission answers for the experiment phase

These answers admit only the bounded H5-H14 *design* under the
[research constitution](ACI_RESEARCH_CONSTITUTION_v1.md). Every later
execution card must repeat or explicitly inherit and verify all ten;
failure of a prerequisite returns that card without a run.

1. Q1: The ultimate ACI question concerns a realizable N1-N5 cognitive
   organization. This card tests only the acquired competitive-availability
   face of **N2**, not the full ACO or consciousness.
2. Q2: The one hypothesis is lower held-out-context joint loss for the
   acquired access candidate versus the complete independently trained
   R1/R2/R3/R4/R8/R9 envelope under the locked optimization/resource
   regime; R4 is a fixed-selector workspace ablation.
3. Q3: Falsify it if fewer than 14/16 seeds exceed 0.02 against the
   within-seed *best* eligible rival, the exact test misses 0.01, or
   the channel is not three bits. Stronger alternatives winning are
   admissible negative results.
4. Q4: R9 is the decisive equal-budget unrestricted learned eight-symbol
   code and can simulate the candidate; R1/R2/R3/R8 remove workspace,
   R4 fixes selection within it, R5 oracle belief broadcast and R7
   independent sufficient-statistic copies are EXTERNAL full-information
   controls, and R6 oracle selector over learned latents is EXTERNAL.
   Optional R10 is a certified analytic bounded-code oracle only. Sweep
   learned rival families with the candidate; I1-I7 cannot prove they fail.
5. Q5: The [Phase III verdict](PHASE3_VERDICT_v1.md) found a scalar
   broadcast equal or better than learned paid sharing, and the
   [transition](PHASE3B_TRANSITION_v1.md) left acquired multi-factor
   competition open. H3 supplies scarcity but not architectural value.
6. Q6: A positive bounded comparison would justify a new independent
   N2 follow-up testing transfer/resource robustness. It does not release
   Phase IV or revise the frozen Phase III verdict.
7. Q7: Failure promotes the winning independently trained R1/R2/R3/R4/R8/R9
   comparator; record a collapse and block occupancy necessity claims, not
   the task's validity. An EXTERNAL bound is a diagnostic, not a win.
8. Q8: An analytic proof suffices for H3 and R9 inclusion. A minimal
   neural comparison is needed only for the contingent training claim.
   No organism simulation or paid-persistence experiment is required.
9. Q9: This is N2-relevant architectural discrimination *only* if
   primary value survives rivals; cheaper coding or a stable decoder
   alone is robustness/implementation, not a new ACO property.
10. Q10: At most conditional acquired access/sample-efficiency under
    declared resources and optimization. No universal N2 necessity,
    full ACO, theory-specific indicator, consciousness or level-(e)
    inference can follow.
