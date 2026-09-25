# C2 — the missing storage comparison (identification + study design)

2026-09-24. Identification/design deliverable for the C2 card
(t_04ae4ff3): *what exactly do AC109–AC113 establish about retained state,
and is there a remaining storage comparison not already answered?*
Predecessor t_3eba13c2 (I0, `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`).
Design only: no organism-scale run, no seeds, no protocol freeze. Grounded in
the frozen/engineering sources (`ac109.py`–`ac113.py`, `ac110.py`,
`ac112.py`, `ac107.py`, and their results docs) and in `C2_TASK_DESIGN_v1.md`;
nothing was re-run or re-hashed.

---

## 0. Verdict, up front

AC109–AC113 answer **four** of the five storage questions and leave **one**
comparison open. The open one is the *positive* direction of the very claim
the C2 gate was built to make testable, and no organism-scale run has delivered
it cleanly:

> **In the occluded-`used_held` world (the C2 gate, ε=0), does the maintained
> sufficient-statistic counter (retained history) demonstrate a
> decision-relevant advantage over the *strongest tuned memoryless policy*
> — on a graded endpoint, not a categorical or survival one?**

It is **not** answered by AC109 (which ran the *un*-gated world), **not** by
AC110/AC111 (which ran the gated world but only the repair and composition
contrasts), and **not** cleanly by AC112/AC113 (which added a residual yield
ε>0, ran an *untuned* no-history arm that dies from churn, and read the
stronger memoryless policy only through a *confounded* scramble control). The
specific claim it would resolve is stated in §3. The study design that resolves
it is in §5, with the one design insight that must shape it in §6.

This is a **new study**, not a reanalysis: the decisive arm (a clean,
tuned, hold-on-occluded memoryless rival in the pure gated world) does not
exist in any saved table.

---

## 1. The five dimensions, separated

The card asks for five things about retained state to be kept apart. The
AC109–AC113 arc maps onto them as follows.

| Dimension | Question | Answered by | Result |
|---|---|---|---|
| (1) Useful information retained | Is there info in past observations worth carrying? | AC107; AC109 | Ceiling-accurate *but redundant* in the un-gated world; the sufficient statistic is an integer counter (P2/P4) |
| (2) Causal role of stored content | Does the stored value drive the decision? | AC108 (dir 2); AC113 (V2) | Yes (force/scramble move the drop), but content can be harmful, and is only *weakly* load-bearing at high q |
| (3) Cost/necessity of acquisition writes | Is the update write necessary, and what does it cost? | AC108 (dir 1); AC109 | Necessary for correctness (no_write reads wrong in cut); but in the un-gated world it is *pure cost* (72–141 vs 0–13 renewals) |
| (4) Contribution of ongoing repair | Does paid repair maintain the stored state? | AC110 | Not load-bearing in-window (reacquisition carries it); load-bearing post-window (G4 8/16) |
| (5) Comparative utility vs same-information rivals | Does storage beat rivals with the same current observations? | AC109; AC113 | Un-gated: direct diagnostic ties (inert). Gated+ε: counter ties counter (weighting inert); untuned immediate churns |

The arc has systematically dismantled each *proposed* "storage is
load-bearing" claim — persistence (AC109), repair (AC110), graded/weighted
magnitude (P2/P4/AC113) — but it has **never run the one positive contrast
the C2 gate exists to test**: retained history against the strongest
memoryless policy in the world where the current observation is ambiguous.
Dimension (5) is answered only in the un-gated world and, gated, only through
confounded/untuned arms (§4). That is the gap.

---

## 2. What each study establishes, precisely

**AC109 (C1, engineering, un-gated).** The stored one-bit estimate is
behaviourally equivalent (48/48 cells) to a rival that reads the same
`(bound, used_held, productive)` triple transiently at decision time. The
K4 discriminator is a *pure function of the current triple* (move → `(1,1,0)`,
cut → `(1,0,0)`, disjoint), so there is nothing to remember. Storage is pure
cost. **Scope of this answer: the un-gated world only** — AC109's own docstring
and C2 §2 both state the world is the one where storage is inert *by
construction*. It does not transfer to the gated world.

**AC110 (C3, frozen 6200-6207, gated q=0.5).** Repair (action-2 bank-0 restore)
is *not* load-bearing for the estimate's correctness/use inside the decision
window: correctness is carried entirely by reacquisition (`bel_write` at every
open in-window contact), and a single-bit estimate cannot even reach the
whole-bank repair trigger under ambient damage. Repair *is* load-bearing for
post-window storage protection (maintained 16/16 vs no_repair 8/16). **Scope:
this is a repair-vs-reacquisition contrast, not a storage-vs-no-storage
contrast.** Both arms *have* the estimate; there is no history-free rival.

**AC111 (I1, frozen 6300-6307).** Composition of the estimate with AC105's
reconstruction + allowance. The estimate bit's exclusion from `reg_from_active`
is load-bearing (verified live for the first time), the direct channels
(reconstruction overwrite, budget starvation) are clean, but corruption
perturbs the reacquisition *schedule* on a minority of finals (behavioural,
seed-dependent). **Scope: composition, not storage utility.** No history-free
rival.

**AC112 (P5, engineering) / AC113 (P6, frozen 6400-6407).** The
heterogeneous-LR two-counter does not beat the single integer counter at
organism scale (R1: "no demonstrated advantage", seed-level p≈0.71/0.63).
Three relevant sub-results: (i) the sufficient statistic is an integer
counter, not a graded register or a weighted pair; (ii) the untuned
`immediate` arm (relinquish on *any* unproductive contact) dies under move
from **churn** (4/8, 5/8) — a survival artifact, not a wrong-decision
finding; (iii) the scramble arm at θ=0.6 (read forced to (0,0) ≈
hold-on-occluded) shows the counter's content is only **weakly** load-bearing
at q=0.9 (saves ~1/8 individuals from a late/never drop; the scramble's income
collapses on one seed). **Scope: this is in the ε>0 world, the no-history arm
is untuned, and the "hold-on-occluded" policy appears only as a confounded
scramble read, not as a clean rival.**

---

## 3. The missing comparison, and the claim it resolves

The C2 gate (occlude `used_held` on a Bernoulli(`q`) fraction of channel-1
contacts) was designed to make the current observation ambiguous — at an
occluded unproductive contact both causes read `(bound=1, used_held=occluded,
productive=0)` while the correct action differs. `C2_TASK_DESIGN_v1.md` §8 then
specified the isolating contrast: the maintained estimate (candidate) against
the history-free `direct` rival, with the claim that the direct rival "defaults
to one cause and is wrong for the other" while the estimate is "right for
both". That contrast — **the storage comparison in the gated world** — is the
one thing in the design that no study has run cleanly.

The claim it resolves, stated narrowly:

> **Retained history (an accumulated, vulnerable, paid-maintained counter)
> contributes a decision-relevant difference at organism scale that a
> *tuned* memoryless policy receiving the same current observations cannot
> match.**

This is exactly the claim `C2_TASK_DESIGN_v1.md` §11 left open: "whether the
maintained estimate is required (vs a longer threshold, or a reactive read) is
the implementing study's question, and is deliberately not pre-judged here."
AC109 closed the *un-gated* half of it (storage inert where the observation is
decisive); the *gated* half is open.

**Why the comparison is non-vacuous (the tradeoff it isolates).** In the gated
world the memoryless policy faces a defer-vs-act tradeoff that is not a
strawman. Relinquishing on occluded-unproductive evidence is fast under move
but risks dropping a still-valid entry under cut; holding on it is safe under
cut but slow under move (it must wait for a decisive *open* held-fail contact,
which arrives only with probability `1-q` per contact). Retained history — an
accumulated count of occluded-unproductive contacts, counterweighted by
productive contacts and latched by open blind — is the object that can
relinquish under move *faster* than "wait for an open contact" while still
holding under cut. The comparison is therefore about the **speed of
relinquishment under move at high occlusion, net of the false-drop risk under
cut** — a graded tradeoff, not a categorical right/wrong and not survival.

---

## 4. Why existing artifacts do not answer it

1. **AC109 is the un-gated world.** Its direct rival never sees an occluded
   contact. Its equivalence is a property of the disjoint-triple world (§2);
   it is the *premise* the gate removes, not a result about the gated world.

2. **AC110 and AC111 run the gated world but neither has a history-free arm.**
   AC110 = `maintained` vs `no_repair` (both have the estimate). AC111 =
   `est`/`est_corrupt`/`est_corrupt_budget` (all have it). The storage
   contrast is untouched.

3. **AC112/AC113's memoryless arm is (a) untuned and (b) the wrong extreme.**
   `ImmediateAlloc` is *relinquish-on-any-unproductive* — the p=1 extreme of a
   one-parameter ambiguity response — and it dies under move from **churn**
   (drop → blind re-bind at 1/4 success → drop), not from a wrong decision.
   AC113 claim-boundary (3) says it outright: *one* failed memoryless policy
   is not a proof that memoryless policies fail.

4. **The strong memoryless policy (hold-on-occluded) appears only as a
   confounded scramble.** AC113's scramble at θ=0.6 reads the counters as
   (0,0), which *behaves* like hold-on-occluded — but it forces the read
   through the candidate's own counter machinery rather than removing the
   state, so its writes (and hence its contact schedule) differ from a clean
   no-state policy (the AC109 "storage write perturbs the schedule" effect),
   and at θ=0.5 it degenerates into the candidate (AC113 rule 2). A confounded
   causal-role readout is not a clean storage rival.

5. **AC112/AC113 are in the ε>0 world.** The residual yield ε changes the
   economics of holding a stale route (a held stale entry yields with prob ε),
   which is exactly what makes "always hold" survivable under move there and
   why the scramble survives 8/8. In the pure C2-gated world (ε=0) holding a
   stale route is zero income, so the defer-vs-act tradeoff is sharper and the
   comparison is cleaner. The ε world answers "is weighting load-bearing", not
   "does retained history beat memoryless".

---

## 5. The study design

**World.** The AC110/C2 gated world, ε=0 (no residual yield), `PORTS=4`
(blind fallback 1/4), move/cut at t=8192, cut window W=96. `q` is the run
parameter; the informative end is `q ∈ {0.7, 0.9}` (C4 rule 3: the accumulator
is only load-bearing at high occlusion; q=0.5 is the AC110 anchor used for the
clean control, not for the discriminating gate).

**Candidate.** The single integer counter — the sufficient statistic
(P2/P4/AC113), not the two-counter (tied) and not the one-bit estimate
(§6). Maintained, vulnerable (dead-rule free bits, sticky-SET damaged, W-gated
paid writes, majority read), Gray-coded, with the hold latch on open-blind and
negative productive weight. This *is* retained history: the counter's value
accumulates across contacts.

**Rivals (the card's requirements, met explicitly).**

1. **Strong immediate policy (same current observations, no history).** A
   memoryless policy over the current triple with **one free ambiguity
   parameter `p`** = P(relinquish | occluded-unproductive contact). The open
   contacts are forced by the decisive observations (relinquish on open
   held-fail, hold on open blind/productive) — those are not free. `p=1` is
   AC113's churning immediate; `p=0` is hold-on-occluded (safe, slow). **The
   ambiguity response is not chosen arbitrarily**: `p` is swept on the
   engineering cohort and `p*` (income-maximising) is fixed pre-run for the
   finals (disclosed). This is the "explicit tuning/decision rule".

2. **Simple history-based / sufficient-statistic rival.** The one-bit
   estimate (AC107/110) — retained history *without* accumulation, the C2
   design's original candidate. It documents whether a non-accumulating
   stored state is load-bearing at all (§6 predicts it is not).

3. **Selective intervention on retained history (acquisition cut).** A
   `no_write` arm that disables the counter's paid write (read honest) — the
   AC108 direction-1 intervention. It separates "the accumulated value is
   load-bearing" from "the write machinery is load-bearing".

4. **Causal-role control.** A scramble arm forcing the counter read, run at a
   threshold **strictly above the read point** (θ=0.6, not 0.5 — AC113 rule 2),
   so it is a clean "always-hold" read and does not degenerate into the
   candidate.

   **Repair intervention: deliberately omitted.** The claim is about
   acquisition (accumulating occluded evidence), not repair; AC110 already
   established repair is not load-bearing in-window. Adding a repair cut would
   re-test a settled question and muddy the contrast.

**Endpoints (reported, with only the graded ones gated).**

- *Primary (gated):* post-cause income per channel, and relinquish-under-move
  latency (move onset → drop+re-bind tick). These are graded; they are where
  the defer-vs-act difference lives.
- *Mechanism readout (reported, not gated):* per-channel correct action at
  occluded contacts, and false-drop rate under cut (the counter's safety cost
  vs a memoryless hold).
- *Survival (reported, not gated):* bimodality-aware lower bound only
  (AC45/AC68); survival is confounded by re-acquirability and churn.

**Gates (prespecified, graded-shape-corrected).**

- **G1 clean control.** At q=0.5 the candidate reproduces the frozen AC110
  `maintained` arm byte-for-byte (`state_hash`) — licenses the world.
- **G2 no-cause identity.** All arms byte-identical in `no_cause`.
- **G3 (discriminating).** At fixed parameters (counter `N*`, immediate `p*`,
  both selected on engineering and disclosed), a seed-level paired sign-flip
  test (n=8 seeds, two histories aggregated within seed — R1's correction) on
  the combined post-cause income, **plus** the (move-latency, cut-false-drop)
  Pareto readout. The verdict vocabulary is **"no demonstrated advantage"**,
  never "equivalence" from nonsignificance (R1). No mean-margin gate (AC16),
  no strict per-individual dominance that the ceiling makes unsatisfiable
  (AC17); the counter and the memoryless rival can both reach the correct
  decision, so the graded latency/income is the only resolvable difference.

**Engineering / confirmation separation.** Engineering seeds 0–7 (disclosed,
excluded); finals a fresh untouched family (e.g. 6600–6607), verified disjoint
from 0–7, 6000–6007 (AC107), 6100–6107 (AC108), 6200–6207 (AC110), 6300–6307
(AC111), 6400–6407 (AC113), 6500–6507 (AC114). `p*` and `N*` are selected on
engineering alone, fixed pre-run, hashed into the protocol.

---

## 6. The one design insight this comparison rests on

**The one-bit estimate is not the load-bearing candidate — the counter is.**
The AC107/110 estimate is updated *only at open contacts* and consumed through
the streak (it relinquishes after `STREAK_N=6` unproductive contacts, not
immediately). So under move at high occlusion it is no faster than "wait for an
open held-fail" (the memoryless hold policy), and under cut it wrongly accrues
streak on occluded-unproductive contacts before the first open blind flips it
(P ≈ q⁶ ≈ 0.53 at q=0.9). The one-bit estimate is *dominated by the counter*
(the counter's hold-latch on open blind and negative productive weight are
what hold under cut), and it is not load-bearing against a hold-on-occluded
memoryless rival. C2's §8 framing ("estimate right for both, direct wrong for
one") is only true against the *suboptimal* memoryless default (relinquish on
occluded); against the *tuned* memoryless response (hold on occluded) the
estimate is decision-equivalent, and the only residual load-bearing object is
the counter's **speed** under move. The study must therefore pit the counter
against the tuned memoryless rival, with the one-bit estimate carried only as
the documented non-load-bearing control.

**Honest prior, stated before running.** AC113 rule 3 already measured the
nearest thing to this (candidate vs scramble-θ=0.6 at q=0.9, ε world): the
content is *weakly* load-bearing — it saves ~1/8 individuals from a late/never
drop, and the memoryless hold's income collapses on one seed. In the pure
ε=0 world at n=8 the expected outcome is a thin, possibly sub-resolution
graded advantage. That is exactly why the comparison is worth running *once,
cleanly*: it converts "weakly load-bearing, measured through a confound, in
the wrong world" into a definitive organism-scale statement about whether
retained history beats tuned memoryless at all. If it returns "no demonstrated
advantage", that **closes** the storage line with a real result (retained
history does not demonstrate a decision-relevant edge over the strongest
memoryless policy at organism scale) — a completion, not a failure.

---

## 7. What this unblocks

The comparison is the last open cell in dimension (5). When it lands:

- A **positive** result (counter demonstrates a graded advantage over the
  tuned memoryless rival) is the first organism-scale instance of retained
  history earning its keep over no-history, and it would justify C3's
  reliability question on a *graded* first-order estimate (the counter has an
  error variance the ceiling-accurate one-bit estimate lacked — K8's block).
- A **negative/no-demonstrated result** closes the storage line at the
  organism scale and moves the cognitive track to its remaining open question
  (reliability/meta-d′ per C1, which needs a *sometimes-wrong* first-order
  estimator in a distinguishable-conditions world), rather than re-opening a
  storage contrast that AC109, AC110, AC113 and this study would then have
  jointly settled.

Neither outcome revives the ε-world weighting question (AC113 settled it) nor
the repair question (AC110 settled it).
