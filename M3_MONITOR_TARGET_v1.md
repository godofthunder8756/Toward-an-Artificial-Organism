# M3 — The monitor's single testable target: the correctness of the first-order estimate `e`

2026-09-25. Definitional deliverable for the M3 card (t_20b842d2): *what is the single,
testable referent of the monitor state `m`, replacing the "separate substrate ⇒ second-order
computation" argument?* This document runs nothing, re-hashes nothing, freezes nothing, and
edits no frozen artifact. It pins the referent, the precise definitions the card demands, and
the claim ceiling + discriminating predictions for ONE chosen target. M6 carries the scientific
claims; this card only defines.

One sentence up front: **`m`'s referent is the correctness of the organism's own first-order
cause estimate `e` — "is my current reading of the world (through this damaged, maintained
substrate) right?" — not the estimate's physical damage, not its staleness, not whether the
downstream action will fail.** That is the type-2 referent of the metacognition literature
(Galvin et al. 2003; Maniscalco & Lau 2012): the second-order judgment is about *one's own
type-1 response*, not the world state and not the substrate.

---

## 1. The move this document makes

C1's candidate question (`C1_RELIABILITY_DISPOSITION_v1.md` §3) argued for `m` structurally: a
second-order computation arises "whenever there is a separation between internal states
supporting decisions and confidence estimates over space and/or time" (Fleming & Daw 2017),
and the AC architecture has that separation by construction. That argument is *necessary* but
not *sufficient*, and the card's whole question is that it cannot be the load-bearing reason:

- A separate substrate can hold a **damage sensor** (a flag = "replica 3 of bit 17 flipped").
  A sensor refers to the substrate; a monitor refers to the organism's *own judgment*. Spatial
  separation does not tell you which one you built.
- The dissociation test (`meta-d′ ≠ d′`, Maniscalco & Lau 2012) needs the separation, but the
  separation does not supply the *referent* that the dissociation is about.

So the "separate substrate ⇒ second-order" argument is demoted to what the literature actually
makes it: a **necessary enabling condition**. What makes `m` second-order is **what it refers
to**. Galvin et al. (2003) define the type-2 task by its *target* — "one's own responses" —
not by its inputs or its substrate. This document supplies that target.

---

## 2. The four candidate targets, separated (and one chosen)

The card names four things `m` might refer to. They are not interchangeable; they sit on
different tiers, and only one is the second-order referent.

**(1) Physical damage to storage** — a property of the substrate: the estimate's 7 replicas
have minority flips. This is an **observation/input** to `m`, not `m`'s referent. Decisively,
in the AC110 world damage and wrongness are *anti-aligned in one condition and aligned in the
other*: the estimate's acquired value is 1 and the sticky-SET stream sets 0→1, so under `move`
damage is inert (the estimate is already all-1s and cannot be damaged into error), while under
`cut` damage pushes the estimate toward the wrong value. "Damaged" and "wrong" therefore come
apart by construction — a state that reports damage is reporting the substrate, not the
estimate's error status. Conflating them is exactly the card's warning that "selective damage"
is not automatic metacognition: it is the `obs`-bit-2 reflex (the AC9/AC110 watchdog), the null
against which `m` must add content.

**(2) Staleness of an estimate** — a property of the content-vs-world relation: `e` was true
when written but the world has since changed. This is **first-order**. It is what re-acquisition
(`bel_write`, fired on open diagnostic contacts) already handles; the current observation still
carries it. A staleness report is content-tier, not a monitor.

**(3) Probability the decoded estimate is wrong** — P(decoded `e` ≠ true cause). This is the
type-2 referent. Galvin et al. (2003) / Maniscalco & Lau (2012): type 1 = the objective stimulus
(world); type 2 = the correctness of the type-1 *response*. In the AC world the type-1 response
is the binary estimate `e` ("E_world" vs "E_machinery"); its correctness is the thing a monitor
of one's own cognition is about.

**(4) Probability a decision based on it will fail** — P(the action `e` selects is wrong). This
is **downstream** of `e` through the streak rule and the world economics, and it is confounded:
in the AC116 world a false relinquishment merely re-binds the entry (`life=64`), so "the decision
failed" is nearly economically invisible (AC113's rule). It is also not the literature's type-2
target — the type-2 task is about the *response* `e`, not the *consequence* of the response.

**CHOSEN TARGET — (3) only.** `m`'s intended referent is the **correctness of the first-order
response `e`**, i.e. a degree of belief that the decoded estimate is currently wrong. Target (1)
is `m`'s *observation*, target (2) is first-order, target (4) is a confounded downstream
consequence. None of the three may be folded in; combining (1)+(3)+(4) into an undefined
"unreliable" label is exactly the move the card forbids.

---

## 3. The precise definitions (the card's deliverable list)

**First-order estimate `e`.** The AC107/AC110 one-bit cause estimate, stored in the dead rule's
action bit at `bel_off` (`traces[0, bel_off]`, 7 replicas), majority-read (≥4 of 7). Acquired
value 1 = E_world (the channel-1 mapping moved; the route entry is stale), 0 = E_machinery (the
read is suppressed; the entry is valid). It is written by `bel_write` (re-acquisition, from open
diagnostic contacts), damaged by the frozen sticky-SET stream (`traces[0,:126] |= core_flips`,
1e-4/replica/tick), repaired only by action 2's bank-0 majority-restore (it is excluded from
`reg_from_active`), and consumed by the allocator every time a channel-1 contact is processed.

**The decision/prediction made using `e`.** On each channel-1 contact the decoded `e` gates the
relinquishment machinery: `e = 0` (E_machinery) → withhold relinquishment + proactive renewal
(HOLD the entry); `e = 1` (E_world) → arm the frozen streak relinquishment, DROP the route-1
entry when the streak reaches `STREAK_N`. So `e` is a binary type-1 response ("the world cause
is E_world / E_machinery") consumed as a hold-vs-drop gate on the route-1 memory entry. (In the
AC116 world `e` at `bel_off` appears as the hold-latch component; the 3-bit counter is a second
first-order state — retained history — that the decision also consumes. The monitor's single
referent is `e`'s correctness; the counter is explicitly *not* a second target.)

**Correctness at specified decision times.** `e` is correct at tick `t` iff
`decoded e(t) == cause(t)`, where `cause(t) = 1` under `move` and `0` under `cut` for
`t ≥ 8192`; before the cause onset correctness is undefined (no decision to be correct). Decision
times = the ticks at which `e` is read and consumed on a channel-1 contact, `t ≥ 8192`. Two
sub-windows, both from AC110's own instrumentation: the primary window `[8192, 8288)` (where
`bel_wrong_in_window` is measured and re-acquisition carries correctness), and the post-window
horizon `[8288, 16384)` (where AC110 found repair load-bearing for storage: `maintained` 16/16
vs `no_repair` 8/16). The regime where `e` is *sometimes wrong for implementation reasons* — and
therefore the only place the monitor is well-posed — is the `cut` condition post-window (the
discriminator writes 0, sticky-SET degrades it toward 1); under `move`, `e` is never wrong (its
acquired value is already 1 and sticky-SET is inert). This asymmetry is exploited by P1 below.

**Monitor state `m` and its intended referent.** A stored, maintained state in a locus distinct
from `bel_off` (a dead-rule / recipe-bank free-bit locus), majority-read, W-gated paid writes,
whose content is a degree of belief that `e` is currently wrong: `m ≈ P(e ≠ cause | bookkeeping)`.
Its referent is target (3) — the correctness of the first-order response — and nothing else. It
is *not* a re-encoding of `obs` bit 2 and *not* a damage flag; a minimal implementation is a
thresholded readout (a coarse reliable/unreliable latch), and the graded version is the fuller
form. The gradedness is an implementation detail, not the referent — the card's caution that "a
confidence variable is not automatic proof of metacognition" is honoured by fixing the referent,
not the granularity.

**The observations available to `m`** (maintenance bookkeeping only; no cause access, no
first-order cause evidence beyond what drives `bel_write`):
 1. the estimate's **own replica minority count** `bel_minority = min(ones, 7−ones)` at `bel_off`
    — the per-bit statistic the repair machinery already computes to do the majority-restore, and
    the single most informative observation about `e`'s wrongness;
 2. **`obs` bit 2** — the whole-bank corruption signal (`Σ_bits min(ones, 7−ones) ≥ 4` over the
    126 bank-0 bits), the input the frozen watchdog reflex consumes;
 3. **repair-write outcomes** — whether action 2 actually funded the estimate's minority restore
    this tick, or was starved by the W-gate/budget (`W = 0` zeroes the `min(32, 8·W)` cap);
 4. **re-acquisition events** — whether `bel_write` recently fired (a fresh diagnostic overwrote
    `e`, resetting the damage clock);
 5. **resource signals** — W count, fuel/material starvation bits (`obs` bits 0 and 1: fuel ≤ 8,
    material ≤ 64).

**Actions influenced by `m`.** `m` modulates the **maintenance direction only**: scheduling /
prioritising repair of `e`, triggering re-acquisition (open-contact diagnostics), and allocating
the repair/renewal budget. `m` does **not** feed the hold-vs-drop decision — that is `e`'s job.
The two directions being separable is the causal-role test (P4).

---

## 4. Theoretical grounding in the actual mechanism (why target (3), and not (1))

The load-bearing fact is the **asymmetry of the damage model in the AC110 world**, which turns
"physical damage" into an observation and "wrongness" into a distinct referent:

- Under `move` the estimate is acquired as 1 and sticky-SET (0→1) is a no-op, so `e` **cannot**
  be damaged into error. Yet the rest of bank 0 keeps accumulating corruption, so `obs` bit 2
  fires while `e` is always correct. A damage-referent state reads "unreliable" here; a
  correctness-referent monitor reads "reliable". The two referents give *opposite* answers in
  the move world — that is what makes the distinction testable, not verbal.
- Under `cut` the discriminator writes 0 and sticky-SET degrades `e` toward 1. `e` becomes wrong
  at exactly 4/7 replicas set (majority flips). But a single bit contributes
  `min(4, 3) = 3` to `obs` bit 2's sum, and the threshold is ≥ 4 over the *whole bank* — so a
  single corrupted bit **never triggers** `obs` bit 2 (the AC76 finding). The estimate can be
  wrong while the watchdog is silent. A correctness-referent monitor reads `e`'s own minority
  (`bel_minority ≥ 4`) and flags it; the reflex misses it.

This is the meta-d′ structure in organism-scale form, and it is the correction C0's case 3
needed (C1 §1 item 5): AC110 tested *repair* (a third-person ablation of a maintenance
mechanism), not the organism's *representation* of its estimate's error status. Target (3) is
the referent whose existence AC110's ablation could not address, and the move/cut asymmetry is
the property that makes it well-posed.

The relevant primary literature, cited as the definition's warrant (not as proof of
metacognition): Galvin et al. (2003) for the type-1/type-2 distinction by *target*; Maniscalco &
Lau (2012) for `meta-d′ = d′` iff the type-1 and type-2 mechanisms "access the same source of
information" (the ideal-observer special case C0 assumed); Fleming & Daw (2017) for second-order
computation as inference on a coupled-but-distinct decision system, requiring spatial/temporal
separation; Yeung & Summerfield (2012) for confidence vs error monitoring as distinct
computations. Fleming & Daw's separation is retained here as a **necessary condition**; the
referent is what the separation is *for*.

---

## 5. Claim ceiling

If `m` passes every gate M6 can build, the strongest wording the result earns is:

> The organism maintains a second-order state whose referent is the correctness of its own
> first-order cause estimate, computed from its maintenance bookkeeping, dissociable from the
> estimate by selective damage, and causally effective on maintenance behaviour — **meets
> candidate indicator HOT-2 at degree Y** (Butlin et al. 2023, "metacognitive monitoring
> distinguishing reliable representations from noise", adapted to interoceptive route-level
> content as `CONSCIOUSNESS_ROADMAP_v1.md` §5 already flags).

Not licensed, at any degree Y: "metacognitive" unqualified, "monitors its own reliability" (the
undefined label this card forbids), "second-order cognition" as a re-labelling of the estimate,
or any level-(e) wording. The level-(d)/(e) boundary is untouched. The referent is **one thing** —
"is `e` wrong?" — and the ceiling names that one thing and nothing more.

---

## 6. Discriminating predictions (a negative outcome must concern THIS design and THIS target)

P1 — **Referent separates from damage (the m-vs-reflex test).** Under `move`, `e` is correct at
every decision time while `obs` bit 2 fires on other bank-0 corruption. A correct target-(3)
monitor reads `m = reliable` throughout the move world; a damage-referent state reads
`unreliable` whenever `obs` bit 2 fires. Prediction: `m` is decoupled from `obs` bit 2 in the
move world. If `m` tracks `obs` bit 2 there, its referent is damage, not correctness → target
(3) falsified.

P2 — **The single-bit miss.** In the cut world there exist ticks where `e` is wrong (majority
flipped) and `obs` bit 2 does **not** fire (single-bit minority contribution 3 < 4). A correct
monitor flags "unreliable" at exactly those ticks, by reading `bel_minority`. If `m` reads
reliable there (it only watches `obs` bit 2), it is the reflex, not a monitor. Measurable
against the frozen AC110 rows (`bel_minority` vs the corruption signal per tick).

P3 — **The false-alarm (m leads e).** When repair is starved (W=0 zeroes the cap, or the
allowance is exhausted) while `e`'s majority is still correct, a correct monitor reads
`m = unreliable` *before* `e` flips — it warns of future wrongness, not of damage already done.
Prediction: `m`'s unreliable transitions precede or coincide with, but never systematically lag,
the moments `e`'s minority crosses the repair-starved threshold, and there exist ticks with
`m = unreliable` and `e` still correct.

P4 — **Causal role on maintenance, not the decision.** Scrambling/cutting `m` changes
repair/renewal/re-acquisition behaviour while the hold-vs-drop decision is unchanged;
scrambling/cutting `e` changes the decision while maintenance is unchanged. If the two
directions are not separable, `m` is a re-parameterization of the decision threshold (AC11's
"optimum is a level" lesson, at the maintenance layer).

P5 — **Content inertness (the AC109 lesson).** A state-blind fixed maintenance duty cycle must
fail to reproduce `m`'s maintenance behaviour. If a fixed policy reproduces it, `m`'s stored
content is inert → falsified.

**Negative-outcome scope.** A negative result is precisely: *in the AC110/AC116 world, with this
stored `m` targeting `e`'s correctness, the organism's maintenance behaviour is fully reproduced
by the `obs`-bit-2 reflex (P1/P2) or a fixed duty cycle (P5), or `m`'s referent collapses to
damage/staleness (P1).* That concerns THIS design and THIS target. It does **not** "close the
reliability tier for real" — that over-reach was C0's error, already corrected in C1, and this
architecture cannot host perceptual-content HOT-2 anyway (charter §7).

---

## 7. What this hands to M6

M6 implements, on the AC110/AC116 world: `m` in a distinct maintained locus; the five
observations of §3 as `m`'s only inputs; ≥2 distinct maintenance behaviours `m` selects among;
the three rivals (state-blind fixed duty, the raw `obs`-bit-2 reflex, an ε-estimator arm); the
damage model stated with rate and read threshold together (AC14/AC69); and gates P1–P5, gated on
maintenance behaviour with survival reported as a bimodality-aware lower bound (AC68). The
referent, once, for the record: **the correctness of the first-order estimate `e`.**

---

## Sources

Primary literature: Fleming & Daw (2017, *Psychological Review* 124, 91–114); Maniscalco & Lau
(2012, *Consciousness and Cognition* 21, 422–430); Galvin, Podd, Drga & Whitmore (2003,
*Psychonomic Bulletin & Review* 10, 843–876); Barrett, Dienes & Seth (2013, *Psychological
Methods* 18, 535–552); Yeung & Summerfield (2012, *Phil. Trans. R. Soc. B* 367, 1310–1321);
Butlin et al. (2023, Table 1 HOT-2).

Repo: `C1_RELIABILITY_DISPOSITION_v1.md`, `C0_FEASIBILITY_v1.md`, `M0_BASELINE_EVIDENCE_INDEX_v1.md`,
`CONSCIOUSNESS_ROADMAP_v1.md` (§4–5), `DEFINITIONS_CHARTER_v1.md`, `ac110.py` (the estimate, the
damage model, the repair cut, `bel_minority`), `ac107.py` (`bel_off`, `bel_read`/`bel_write`),
`ac116.py` (the counter/hold first-order states), `ac9.py` (`observe`, `obs` bit 2). This
document is derived and is **not** hashed into any study's `pre_run_snapshot.json`.
