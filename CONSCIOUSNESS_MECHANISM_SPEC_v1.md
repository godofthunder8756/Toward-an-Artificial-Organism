# Consciousness track spec v1: no concrete mechanism is currently testable — closure with a named candidate

2026-09-17. Non-frozen decision note. No experiment run, no seeds, no protocol.
It does not edit the frozen docs, and it does not edit
`CONSCIOUSNESS_BLOCKS_DISPOSITION_v1.md` (which remains the record of the
goal-§7 scheduling archive). It answers the specific question this card asks:
can the AC67/71 self-monitoring loop, or the Butlin et al. 2023 indicator
framework, be turned into a concrete, falsifiable, theory-specific mechanism
worth testing?

**Answer: no concrete consciousness mechanism is currently testable.** The
closure does **not** re-gate on content self-production — `AC79_ERRATA_v1.md` §5
is accepted in full: autopoiesis is not a prerequisite for a theory-specific
investigation. The stop rests on two facts that hold *regardless* of the
self-production result, and are read from frozen code, not from the loop's
description.

## 1. Route A — the AC67/71 self-monitoring loop is a repair reflex, not an indicator instance

What the loop actually is (frozen code, not prose):

- `ac9.observe` (ac9.py:52–67) computes observation bit 2 as a host-side scalar
  over the organism's own live program: `ones = b.traces[0,:126].sum(axis=1)`,
  then `obs |= int(np.minimum(ones, 7-ones).sum() >= 4) << 2`. Bit 2 is a single
  threshold bit meaning "the program bank's total minority-replica count is >= 4".
- `ac5_program.program` (ac5_program.py:29) encodes the bank-0 rule as
  `(1, 4<<0, 2+0)` — mask 4 (bit 2), action 2 = paid bank-0 repair — fired by
  interpreter fallthrough in `prog.choose`.
- So "self-monitoring" is: the host recomputes a 1-bit corruption summary of the
  organism's own program each tick, and the program answers that bit with one
  paid repair action. AC67/71 established the repair is load-bearing (cut it and
  the organism dies; the observation-hijack path is the mechanism).

Why this is not an instance of any Butlin indicator:

1. **The monitoring is external scaffolding.** Bit 2 is recomputed each tick by
   the host `observe` function. The organism neither stores, nor maintains, nor
   produces the monitoring state; it reads it. This is the AC79 errata's
   "recipe is still external" boundary (§4), now appearing at the observation
   layer rather than the reconstruction layer.
2. **It is not a representation.** A 1-bit threshold that always drives one
   fixed action has no content that is flexibly consumed. HOT-2 requires a
   monitoring module whose output a *general* action-selection system can use in
   more than one way; here there is one bit and one reflex.
3. **It is not acquired.** The mapping "bit 2 -> action 2" is a frozen rule word
   and a frozen priority; no part is learned or produced by the organism.
4. **There is no first-order perceptual content for any monitor to be *about*.**
   The monitored quantity is the program's own replica-count corruption — a
   hardware-integrity statistic, not a content-bearing state.

Honest classification: this is a homeostatic repair reflex — the kind of thing
every theory in Butlin et al. treats as *sub-conscious infrastructure* (a
watchdog timer, DNA-repair machinery), not the information-processing the
theories identify with phenomenal content. AC67's own results doc says the same:
it "establishes organismal autonomy, not consciousness." No theory lists "pays
to repair its own corruption" as an indicator, so there is nothing to test — the
loop is definitionally outside the framework.

## 2. Route B — the Butlin et al. 2023 indicator framework presupposes content the organism lacks

The indicator properties (arxiv:2308.08708, Table 1), each of which presupposes
input/perceptual modules carrying content:

- RPT-1: input modules using algorithmic recurrence
- RPT-2: input modules generating organised, integrated perceptual representations
- GWT-1: multiple specialised systems operating in parallel
- GWT-2: limited-capacity workspace (a bottleneck in information flow)
- GWT-3: global broadcast of workspace content to all modules
- GWT-4: state-dependent attention
- HOT-1: generative, top-down or noisy perception modules
- HOT-2: metacognitive monitoring distinguishing reliable perceptual representations from noise
- HOT-3: agency guided by a general belief-formation/action-selection system
- HOT-4: sparse and smooth coding generating a "quality space"
- AST-1: a predictive model of the current state of attention
- PP-1: input modules using predictive coding (entails RPT-1 and HOT-1)

Per-theory assessment of the current organism:

- **RPT:** no input modules, no perceptual representations, no recurrence over
  content. Fails by construction.
- **GWT:** no module architecture, no workspace, no broadcast. The program bank
  is a single 126-bit rule bank routed by fallthrough, not a workspace. Fails by
  construction.
- **HOT:** no first-order perceptual representations to monitor (HOT-1/2/4 are
  vacuous), and the action-selection system is a fixed reflex bank, not a
  general belief-formation system (HOT-3). Fails by construction.
- **PP:** no generative model, no prediction error. Fails by construction.
- **AST:** no model of its own attention — there is no attention to model. Fails
  by construction.

The decisive obstacle is content, and it is structural. The organism's entire
observation space is nine host-computed threshold bits about its *own* resources
and integrity (ac9.py:52–67): fuel-low, material-low, corruption, region-0/1
renewal-urgent, low-core-W, low-converters, low-boundary. None is a
content-bearing perceptual representation of an external world; there is no
sensory module holding a state that could be *integrated*, *broadcast*,
*monitored*, *predicted*, or *attended to*. Applying the rubric therefore
returns 0/N on every theory, and that is known in advance — it is a reading of
the code, not an experiment.

## 3. The one candidate mechanism, and why it is not worth building now

The only theory-specific mechanism the current line could in principle be
extended toward is a minimal HOT-2 metacognitive monitoring: replace the
host-computed bit 2 with a self-produced, paid-maintained representation of the
program's own integrity, and require that representation to be *flexibly*
consumed (guiding more than one downstream decision). Written as a mechanism:

- **Claim.** Under persistent damage, the organism's continued functioning
  depends on a corruption estimate that (a) lives in its own vulnerable state,
  (b) is maintained by its own paid repair machinery, and (c) is the state read
  to schedule repair — not the host observation.
- **Prediction.** Cutting the *maintenance of the estimate* (not the repair
  action) degrades repair timing and survival; scrambling the estimate while
  leaving the host observation intact changes repair scheduling.
- **Measurement.** Repair-timing distribution and survival, paired within seed,
  against a matched hardwired-reflex rival (the frozen loop) and a
  no-maintenance rival.
- **Falsification.** If repair scheduling is statistically unchanged when the
  self-produced estimate is scrambled (the organism was relying on the host
  observation all along), the mechanism is falsified.

Why this is not currently testable, and not worth building now:

1. **It is not present.** The frozen line has the host observation; moving the
   monitor inside vulnerable, maintained state is a new architecture — the
   AC79/80 internalization program applied to a functional-state representation
   rather than the policy description. Nothing in the frozen runner can test it
   today.
2. **Its best-case result is bounded by the framework itself.** Butlin et al.
   are explicit that satisfying indicators is graded and does not establish
   consciousness. A positive result here earns, at most, "meets a candidate
   HOT-2 indicator at the self-monitoring margin" — which `NEW_AGENT_GUIDE.md`
   §8 already maps to a *non*-consciousness claim. A large build whose ceiling
   is a claim the discipline forbids making is not a mechanism worth testing.
3. **It does not answer the subjectivity question.** The gap between "maintains
   a representation of its own integrity" and "there is something it is like" is
   not closed by satisfying HOT-2; the framework's own authors deny the
   inference. Such an experiment would move *organismal autonomy* forward, not
   subjectivity, and should be carded as autonomy work if pursued at all.

## 4. Disposition and re-open conditions

**Closure.** No concrete, falsifiable, theory-specific consciousness mechanism is
currently testable in this organism. This is a justified stop, independent of
the content self-production result (accepted per `AC79_ERRATA_v1.md` §5).

Re-open this track only when one of the following is true:

1. The organism acquires content-bearing input/perceptual modules — sustained
   representations of an external world or an embodied sensory surface that
   could carry "organised, integrated perceptual representations" (RPT-2) or a
   workspace (GWT). Until there is content, every indicator is vacuous and no
   theory-specific experiment is meaningful.
2. A decision is made to build the §3 minimal HOT-2 mechanism *as an
   organismal-autonomy study*, explicitly labeled "meets candidate indicator,"
   never "conscious." That is defensible autonomy work on a separate track; it
   does not require this closure to be lifted.
3. An external theory change supplies an indicator that applies to content-free,
   purely self-referential systems — in which case the first task is to
   re-derive the indicator in computational terms for this organism, not to run
   anything.

The next worker must not: start any consciousness implementation or training;
re-gate this track on content self-production; or relabel the AC67/71 loop, any
feedback loop, or any future HOT-2-marginal result as consciousness.
