# C1 — Correct the reliability disposition: the collapse holds only for the ideal observer, and the actual estimator is a valid monitoring target

2026-09-24. Reanalysis + disposition deliverable for the C1 card (t_2b306a9f). It
reassesses C0 (`C0_FEASIBILITY_v1.md`) against the primary literature that distinguishes
first-order decisions from evaluations of those decisions, corrects the five inference
errors the card names, retains the one valid caution, and delivers **outcome (a): a
discriminating candidate question about monitoring the actual estimator.** Predecessor:
t_3eba13c2 (I0, `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`), which fixed the architecture baseline
at AC105 with AC110/AC113 as the cognitive sub-studies. This document runs nothing,
re-hashes nothing, and edits no frozen artifact.

One sentence up front: **C0's collapse is correct only under the ideal-observer
assumption — the "same internal state supports both the decision and its confidence
readout" model — and that assumption is false in the AC architecture by construction.**
The organism's first-order estimate is a damaged, resource-constrained, sometimes-wrong
implementation, stored in a substrate spatially and temporally separated from the machinery
that maintains it. The metacognition literature shows those are exactly the conditions
under which a second-order (monitoring) computation is *distinct*, not a re-encoding. The
corrected disposition is therefore **not "not identifiable / closed"**: it is
*identifiable in principle as a question about the actual estimator*, and the card's
outcome is the candidate question that makes it discriminating.

---

## 0. What is retained, unchanged

**Estimating ε does not automatically establish metacognition.** This is C0's load-bearing
warning, and the literature itself enforces it: sensitivity to uncertainty is a central
aspect of *first-order* Bayesian computation, and "alone it is not evidence for
metacognition." An ε-estimate (or a q / P_YIELD estimate) parameterizes a first-order
likelihood; calling it "second-order cognition" because it feeds another computation is the
labeling error. C0 was right to say this, and the corrected disposition does not undo it.
What is wrong is C0's *further* step — that because ε-estimation is not metacognition,
*there is no third referent at all*, and therefore the reliability tier collapses.

---

## 1. The five inference errors, corrected

### (1) Equal marginal productivity rates do not imply identical full observation histories

C0's F1 demonstrates a *marginal* confound: the rate `r = P(productive | occluded) =
P(move)·ε + P(cut)·(1/4)` is satisfied by a continuum of `(ε, P(move))` pairs
(0.02/0.435, 0.08/0.588, 0.125/0.80 all give r = 0.15), and concludes "no label-free
observation separates them."

That conclusion over-reaches. The marginal rate is an *aggregate*; the organism's actual
observation is the **full history** — the ordered sequence of `(bound, used_held,
productive)` triples, including the **open** (non-occluded) contacts and their temporal
positions. Two `(ε, P(move))` pairs that produce the same marginal r do **not** produce the
same history: they differ in the pattern of open-vs-occluded contacts, in which open
contacts land, and in the timing of decisive (F1/F2) events. Equal marginal productivity is
a *lossy projection* of the history, and a projection's being non-identifying is not a
history non-identifiability result. The correction: F1 establishes a *marginal* confound
only; the full-history identifiability question was never analyzed.

### (2) Open diagnostic observations and persistent latent causes must be included in identifiability analysis

C0's F1 treats the cause as perpetually latent and analyzes only the occluded marginal
stream. But the AC113 world contains **open diagnostic observations** — F1 (open held-fail,
one-sided ⇒ move) and F2 (open blind-while-bound, one-sided ⇒ cut) — and the cause is
**persistent** (the mapping flips once at t=8192 and stays; the read-cut is a fixed window).
Those two facts make the cause *identifiable* from the organism's own history: an open
contact resolves it, and persistence lets that resolution be carried forward.

Once the cause resolves, ε becomes identifiable *conditional on it*: under a resolved
`move`, the organism counts occluded productive-vs-unproductive contacts to estimate ε;
under a resolved `cut`, the occluded-productive rate is the *known* blind fallback 1/4. So
the "joint hierarchical inference over (cause, ε)" that C0 invoked as a *collapse* is in fact
the standard structure of latent-variable identifiability: the latent cause is identified
first (by open observations + persistence), then the parameter is identified conditional on
it. C0's conclusion "ε is entangled with, not upstream of, the first-order inference" rests
on having dropped the observations (open contacts) and the property (persistence) that break
the entanglement.

### (3) An ideal sufficient statistic is not automatically equivalent to a damaged, resource-constrained implementation

C0's F2: "confidence = tanh(|L|/2) is a deterministic function of the sufficient statistic
(n_u, n_p), so it carries nothing the first-order state lacks," and the deeper claim "in a
faithful Bayesian agent the posterior IS its own reliability." This is true *for an ideal
observer whose sufficient statistic is exactly and losslessly maintained*. It is false for
the AC organism, whose counters are **damaged** (sticky-SET `|=` on 7 replicas), whose
writes are **W-gated and budgeted** (the decision allowance reserves 42; W=0 zeroes the
write cap), and whose estimate can be corrupted or starved of repair *independently of the
world evidence* (AC110: `no_repair` drifts 8/16 post-window; AC68/AC71: sticky corruption
flips the register read).

The literature makes exactly this point via meta-d′: the type-1 decision variable (d′) and
the type-2 confidence variable (meta-d′) access *different* information, and `meta-d′ = d′`
is the **special case** in which "the cognitive mechanisms responsible for making type 1 and
type 2 decisions access the same source of information" (Maniscalco & Lau 2012). `meta-d′
< d′` arises when noise/decay is introduced in the confidence readout; `meta-d′ > d′` when
the confidence computation draws on *additional* information. Fleming & Daw (2017) state the
general point directly: second-order computation is contrasted against "first-order models
in which the **same internal state** supports both decisions and confidence estimates," and
it "may ensue whenever there is a separation between internal states supporting decisions
and confidence estimates over space and/or time." C0's "the posterior IS its own
reliability" is precisely the *first-order model* of that contrast — an assumption, not a
theorem — and the AC architecture violates it by construction (the estimate at `bel_off`,
its repair by the bank-0 restore, its reacquisition by `bel_write`, and the corruption
signal obs bit 2 are four distinct computations in distinct substrates).

### (4) A computation's reuse of first-order evidence does not by itself rule out a distinct monitoring function

C0's F2/F3: confidence is a *function* of (n_u, n_p), hence "a re-encoding, predicts nothing
new"; the monitor that predicts first-order errors "IS an eps-estimator = (a)." The error is
the elision "is a deterministic function of X" ⇒ "has the same functional role as X."
Second-order computation *reuses* the first-order evidence — Fleming & Daw (2017) cast it as
"inverting a generative model of one's own action" — but it answers a **different question**
("was my decision correct?" rather than "what is the world state?") and has a **distinct
downstream role** (error detection, regulating trust, adjusting strategy, communicating
confidence). A state that reads the same inputs but is *consumed by a different rule* is a
distinct function; the functional role, not the input overlap, is what distinguishes them.
The type-1/type-2 distinction (Galvin et al. 2003) is exactly this: the type-2 task —
discriminating one's own correct from incorrect decisions — is defined by its *target*
(one's own responses), not by its inputs.

### (5) AC110's repair intervention did not test an organism's estimate of its own computational integrity

C0's collapse case 3 asserted: "'is my substrate intact?' — this IS AC110's question, and
AC110 already answered it." That is a false attribution. AC110 cut action 2's bank-0
majority-restore (the **repair path**) while leaving reacquisition (`bel_write`) intact, and
measured whether the estimate's correctness/use degrades under ambient damage. That is a
**third-person ablation of a maintenance mechanism** — it answers "does ongoing repair
maintain the estimate?", to which AC110 answers: not in the decision window (reacquisition
carries it), but yes for post-window storage (maintained 16/16 vs no_repair 8/16).

It says **nothing** about whether the organism possesses a *second-order representation* of
its own integrity — a state whose content is "my estimate/substrate is (un)reliable" and
whose causal role is to regulate maintenance in response to that content. No AC110 arm gave
the organism such a state, let alone tested it. The experimenter's ablation of a mechanism
and the organism's representation of that mechanism's state are different objects; C0
conflated them, and case 3 of the collapse therefore rests on an answered question that was
never asked.

---

## 2. The corrected disposition

**C0's "NOT identifiable / closed" is withdrawn in favor of a conditional result.** The
collapse is *valid as a scoped non-identifiability result* — it proves that under the
ideal-observer assumption (one internal state supports both the decision and its confidence
readout, with lossless maintenance and no readout noise), "reliability of my own estimate"
has no referent separate from (a) the channel parameter ε or (b) the cause posterior. That
is C0's real, correct core, and it matches the literature's own statement of when confidence
is *not* second-order.

**But the assumption does not hold here**, and the conditions the literature identifies as
necessary and sufficient for a distinct second-order computation — *separation between the
decision state and the confidence state over space and/or time* (Fleming & Daw 2017), with
the confidence readout accessing *different* information than the decision (Maniscalco & Lau
2012) — are present in the AC architecture by construction:

- **Spatial separation.** The first-order estimate lives at `bel_off` (the dead rule's
  action bit), the decision state (streak/reserve) in the dead rule's mask bits, the program
  in bank 0, the description in bank 1. The substrate that would hold a monitor is distinct
  from the substrate that holds the estimate.
- **Temporal separation.** Repair (action 2, on the corruption signal) and reacquisition
  (`bel_write`, on open contacts) fire on different triggers at different times; the estimate
  is sometimes wrong *for implementation reasons* (corruption, starved repair — AC110's
  post-window drift; AC68/AC71's sticky corruption) that are temporally and causally
  independent of the world evidence.
- **Differential information.** The maintenance bookkeeping the organism already receives —
  the corruption signal (obs bit 2, `min(ones, 7-ones).sum() >= 4`), the renewal-urgency
  bits, the energy/material starvation bits, and its own repair/renewal write outcomes — is
  information about the **implementation's** degradation, not about the world cause. The
  first-order estimator conditions on `(bound, used_held, productive)`; the maintenance
  signals are *outside* its sufficient statistic. That is exactly the "additional
  information" whose presence licenses a genuinely second-order readout.

Therefore the honest disposition is: **the reliability tier is identifiable in principle —
but only as a question about monitoring the actual (damaged, maintained, sometimes-wrong)
estimator, never about the ideal posterior.** C0's error was to run the identifiability
analysis on the ideal sufficient statistic and the marginal stream, and to conclude
"structural, not a tuning miss" from that special case.

---

## 3. Outcome (a): the discriminating candidate question

> **Does the organism maintain a second-order state `m` — in a substrate distinct from the
> first-order estimate `e` — whose content is "`e` is currently unreliable (corrupted /
> stale / starved of repair)", computed from the organism's own *maintenance bookkeeping*
> (the corruption signal obs bit 2, the renewal/repair write outcomes, the reacquisition
> events), and whose causal role is to regulate *maintenance* (repair / renewal /
> reacquisition), such that `m` and `e` can be dissociated by selective damage?**

The question is discriminating because it is pinned to three properties that distinguish
`m` from both (a) an ε-estimate and (b) a function of the cause posterior:

1. **Content.** `m` is a function of the *maintenance bookkeeping*, not (only) of the cause
   evidence. A state whose value depends on obs bit 2, on whether a repair write was
   starved by the budget or W=0, or on whether `bel_write` recently fired, is reading the
   *implementation's* degradation — the referent C0's case 3 claimed did not exist.
2. **Dissociation.** Because `m` and `e` sit in separate substrates with separate
   damage/maintenance, they can come apart: `m = "unreliable"` while `e` is correct (repair
   starved but content survived — a false alarm), and `m = "reliable"` while `e` is
   corrupted (the corruption never crossed obs bit 2's `>= 4` threshold — a miss). These
   dissociations are the organism-scale analogue of `meta-d′ ≠ d′`, and they are impossible
   in C0's single-substrate ideal model. They are the *signature* that `m` is a distinct
   computation, not a re-encoding.
3. **Causal role.** `m` acts on the maintenance direction, not the decision direction:
   scrambling or cutting `m` changes repair/renewal/reacquisition behaviour while leaving
   the first-order relinquish-vs-hold decision intact; scrambling or cutting `e` changes the
   first-order decision. The two directions being separable is what shows `m` is a monitor
   and not a re-parameterization of the decision threshold (AC11's "optimum is a level"
   lesson, at the maintenance layer).

**Where it is testable.** The question is only well-posed where the estimate is *sometimes
wrong for implementation reasons* — i.e. in the C2-gated / AC113 world with the damage
stream and the repair budget active (the AC110 post-window drift regime, and the AC68/AC71
sticky-corruption regime), not in the un-gated world where the estimate is ceiling-accurate
and a monitor has nothing to predict (K8's still-valid block).

**Rivals that must be implemented (not strawmen).** (i) a state-blind fixed maintenance
policy (always repair/renew at fixed duty) — the AC11 lesson generalized to maintenance; (ii)
the first-order-only reflex (obs bit 2 → one fixed repair action, no stored `m`) — which is
the existing AC9/AC110 watchdog and the null against which `m` must add content; (iii) an
ε-estimator arm, to show `m` is not just (a). The candidate must be *stored, maintained, and
flexibly consumed* (≥2 distinct maintenance behaviours) — the same test the roadmap already
uses to separate its chosen mechanism from the AC67/71 reflex — or it collapses back into
the watchdog.

**Falsification.** `m` is falsified if scrambling/cutting it leaves maintenance behaviour
unchanged while the first-order decision still works (the organism is using the raw obs-bit-2
reflex, not a stored monitor), or if a state-blind fixed policy reproduces `m`'s maintenance
behaviour (the content is inert — AC109's lesson, one level up).

---

## 4. Claim discipline

This is a **disposition and a candidate question, not an experiment.** Per the card, no
organism-scale metacognition study is authorized here: the deliverable is the corrected
disposition plus the named discriminating question, exactly the "identifiability-before-
organism-run" step the C2/C4 line prescribes. Nothing here licenses "metacognitive,"
"conscious," or any level-(e) wording; the strongest wording the eventual study could earn
remains "meets candidate indicator HOT-2 at degree Y" — and only after the maintenance/
monitor dissociation is demonstrated, which is not claimed and not run here. The level-(d)/(e)
boundary is untouched.

The track is **reopened** from "closed" (C0) to "identifiable in principle, with a named
discriminating question," but **not** to "authorized." The ideal-observer scoped
non-identifiability (C0's valid core, outcome (c)) survives as the boundary of the claim:
it is what the candidate question must *not* be, because the actual estimator is not the
ideal one.

---

## 5. What this hands to W0 (flagged, not edited here)

The collapse wording lives in documents owned by the W0 reconciliation card; per I1's scope
discipline these are flagged, not edited, here:

- `C0_FEASIBILITY_v1.md` §4–5 — "NOT identifiable … the block is structural" (superseded in
  part by this document; a banner is added to that file pointing here).
- `CONSCIOUSNESS_ROADMAP_v1.md` §5 and §12 — "the reliability tier is closed (C0), not
  blocked-with-reopening-conditions (K8)."
- Any synthesis/evidence-index wording that carries "the reliability tier is closed as a
  second-order cognition track."

The corrected wording for those is: the reliability tier is **identifiable in principle as a
question about monitoring the actual estimator** (spatially/temporally separated from the
estimate, reading the maintenance bookkeeping, dissociable from it by selective damage),
**not yet demonstrated**, and gated on an estimate that is sometimes wrong for
implementation reasons; estimating ε alone still does not establish metacognition.

---

## Sources

Primary literature (first-order vs second-order / metacognitive computation):

- Fleming, S. M., & Daw, N. D. (2017). Self-evaluation of decision-making: A general
  Bayesian framework for metacognitive computation. *Psychological Review, 124*(1), 91–114.
  — second-order computation as "inference on a coupled but distinct decision system,"
  arising "whenever there is a separation between internal states supporting decisions and
  confidence estimates over space and/or time," contrasted with first-order models in which
  "the same internal state supports both."
- Maniscalco, B., & Lau, H. (2012). A signal detection theoretic approach for estimating
  metacognitive sensitivity from confidence ratings. *Consciousness and Cognition, 21*(1),
  422–430. — type-1 (world states) vs type-2 (own correct/incorrect decisions); meta-d′
  expressed in type-1 units; meta-d′ = d′ iff the two mechanisms "access the same source of
  information."
- Galvin, S. J., Podd, J. V., Drga, V., & Whitmore, J. (2003). Type 2 tasks in the theory
  of signal detectability. *Psychonomic Bulletin & Review, 10*(4), 843–876. — the
  type-1/type-2 distinction itself.
- Barrett, A. B., Dienes, Z., & Seth, A. K. (2013). Measures of metacognition on
  signal-detection theoretic models. *Psychological Methods, 18*(4), 535–552. — meta-d′
  robustness and the ideal-observer meta-d′ = d′ benchmark.
- Fleming, S. M., & Lau, H. (2014). How to measure metacognition. *Frontiers in Human
  Neuroscience, 8*, 443. — the 2×2 confidence-accuracy table; type-2 SDT.
- Yeung, N., & Summerfield, C. (2012). Metacognition in human decision-making: confidence
  and error monitoring. *Phil. Trans. R. Soc. B, 367*, 1310–1321. — confidence vs error
  monitoring as distinct computations.

Repo sources: `C0_FEASIBILITY_v1.md`, `_c0_reliability_identifiability.py`,
`CONSCIOUSNESS_ROADMAP_v1.md`, `K8_DISPOSITION_v1.md`, `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`
(I0), and the frozen runners `ac110.py`, `ac9.py` (`observe`, obs bit 2), `ac107.py`/`ac111.py`
(`bel_off`), plus the skill references `ac107.md`, `ac110.md`, `ac111.md`, `ac113.md`,
`c0-reliability.md`, `c4-uncertainty.md`.
