# SUB_A analytic admission check v1

2026-10-01. Solver-free, design-level checks of the candidate in the
[draft](SUB_A_PROTOCOL_v1.md). No fit, seed-level experiment or final result.

## A. Shrinkage is not necessarily information damage

For sign-decoded association `b = 1[w > 0]`, positive uniform shrinkage gives
`1[a w > 0] = b` for any finite `a > 0` in exact arithmetic and nonzero `w`.
Repeated shrinkage leaves classifications unchanged. A normalized classifier
can similarly cancel a uniform scale at its decision surface. This does not
cover arbitrary biased nonlinear recurrent networks, additive drift, erasure
or finite-precision underflow. It excludes pure shrinkage as a sufficient
justification of the proposed associative regime.

## B. Live repetition repair is ordinary error correction

If an acquired scalar is represented as `(w,w,w)`, destruction of any one
replica to zero leaves `median(w,w,0) = w`, for either sign. Setting all three
to that live median recovers the scalar without a clean copy. Two agreeing
wrong replicas can instead cement the wrong value. This is a three-copy
repetition code with a supplied decoder, not a discovery about neural
maintenance. Stochastic drift is not guaranteed correctable.

For an independent uniform table B of K bits, an exact decoder of *every*
table requires at least `2^K` distinguishable acquired states: fewer states
merge two tables whose differing cue is eventually queried. This finite-bit
storage argument supplies no neural necessity or real-valued dimension bound.
The table/code rival is explicitly retained, not excluded as "too simple."

## C. External-schedule identity (induction over the entire lifetime)

Let S contain ALL live task, replay and repair traces. D_t is an arbitrary
externally generated damage map, potentially uneven, nonstationary,
correlated or history-dependent under coupled histories. R computes repair
solely from the damaged live S. The diagnostic candidate applies R every tick:

`S_(t+1) = R(D_t(S_t))`.

An external fixed every-tick schedule using the SAME vulnerable banks and
operation has exactly the same transition. Starting from the same S_0 and
using the same D_t, induction gives equality of every S_t, query response,
retention endpoint and operation count. It needs no clean template, readable
damage meter or external task truth. It works under any chosen damage law.
**The all-tick candidate has no comparative advantage over this legal simpler
schedule.** This is not proof that a future adaptive schedule cannot differ.

## D. Yoked identity and its precise scope

If the yoke starts from the same state, receives the same damage and replays
the donor's action decisions using the same local operation, the same induction
gives equality. The yoke stores action timing, not donor clean weights or
repair targets. For the present fixed all-tick donor this is simply C.

A mismatch of initial states, observations, effective repair operation,
transferred target content or applied lesions breaks the premises. Such a
contrast is not automatically information/resource matched. In Phase B a
controlled counterfactual that decouples donor regulation from recipient
damage can be useful; that is a new contrast, not an interpretation of C.

## E. Complete information loss

If all task, replay and repair traces are erased and no answer-bearing source
remains, two different original association tables yield identical live state
and future maintenance input. Any deterministic reconstruction must output the
same table for both, so it cannot recover both. With uniformly random unknown
bits, expected query accuracy is 1/2. This is an information-loss test, not a
per-seed exact-accuracy threshold.

The fixture cannot resurrect erased task values by restoring only its generic
repair gain. A test checks this separately.

## F. Vulnerable data is not vulnerable performing machinery

The fixture damages the gain and replay bank. Nevertheless the host computes
median, addresses entries and performs consolidation correctly even when
those banks are damaged. A gain lesion demonstrates a vulnerable gate, not
reconstruction of the machinery performing those operations.

This fails the stipulated full repair-machinery vulnerability as a neural
implementation. Its declared primitive substrate cannot be relabeled after a
positive result to claim production closure. A real neural candidate needs a
separate performing-circuit specification and lesion test.

## Disposition and replay

**STOP this candidate before any empirical engineering run.** C rules out its
candidate-exclusive comparative H1; F blocks the mandatory closure design.
Neither is a global impossibility theorem about self-repair, nor evidence
against a narrower causal role for ordinary coding.

The [diagnostic tests](sub_a_v1/test_skeleton.py) instantiate C/D under uneven
fault events, test B, E, hidden-integrity aliasing, no extra stored template,
input validation and irreversible tick ordering:

```powershell
python -m pytest sub_a_v1\test_skeleton.py -q
```

Floating-point equality tests are implementation checks of the algebraic
identity, not independent laboratory replication. They use engineering fixture
seeds only, generate no trained checkpoints and cannot authorize a freeze.
