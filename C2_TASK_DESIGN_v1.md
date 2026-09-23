# C2 task design v1 — a task where current observations are identical but histories differ

2026-09-23. **Design document, not a study.** No organism-scale run, no seeds, no
protocol freeze. This is C2's deliverable (task t_a5ef427b): the minimally-changed task
whose identifiability-from-permitted-histories is demonstrated *before* any
organism-scale run, together with the history-based rival. It answers the card's
question and names the separating history feature, so C3/C4 implement against a
*known-ambiguous-but-history-identifiable* task rather than rediscovering AC107's
disjointness.

Everything below is derived from the frozen/engineering sources already in the repo
(`ac107.py`, `ac106.py`, `ac9.py`, `ac9_memory.py`, `ac12.py`, `AC107_PROTOCOL_v1.md`,
`TASK_IDENTIFIABILITY_v1.md`, `AC109_ENGINEERING_v1.md`) and the diagnostic
`_c2_identifiability.py` (run; output reproduced in §7). No frozen artifact was edited,
re-run, or re-hashed.

---

## 1. The question

Is there a task where the **current** observation is identical across the two causes
while their **histories** differ, so that a *maintained* (persistent) function is
load-bearing?

**Answer: yes, after one minimal, declared change.** In the AC107/108 two-cause world the
K4 discriminator is a *pure function* of the current `(bound, used_held, productive)`
triple (the two causes produce **disjoint** tuples), which is exactly why C1 (AC109)
measured the stored cause-estimate to be inert — there is nothing for a stored bit to
remember. The minimal change that makes history load-bearing is to **occlude the
`used_held` observation intermittently**, so the two causes now produce an **identical
ambiguous observation** (an unproductive contact whose retrieval-success is occluded),
and only the **accumulated open-gate history** separates them.

---

## 2. C1's disposition, restated (what this design must change)

AC109 (`AC109_ENGINEERING_v1.md`, engineering 0–7) showed the AC107 stored one-bit
cause-estimate is behaviourally equivalent to a rival that reads the same triple
transiently (48/48 cells identical on every decision endpoint), while the stored
estimate costs *more* (a 7-replica write plus a persistence-driven stream of redundant
proactive renewals). The reason, in one line: **the discriminator is a pure function of
the current observation**, so the current observation already determines the cause and
there is nothing to remember between contacts.

The three hypothesis conditions C1 tested, and their answer in this world:

- (a) adds information unavailable in the current observation — **no**;
- (b) supports decisions between diagnostic observations — **no** (decision granularity
  equals diagnostic granularity);
- (c) alters behaviour/cost beyond direct use — **no benefit, only cost**.

To make maintained history load-bearing, the design must create a contact where (a)
holds: a decision-time observation that is **identical** across the causes while the
correct action differs, so a stored bit carries information the current observation no
longer contains. The card's named mechanisms — intermittent diagnostic access, delayed
consequences, temporarily unavailable observations — are three ways to say the same
thing: make one discriminative observation bit **intermittently available**.

---

## 3. The two causes (unchanged from AC107/108)

Both causes produce the identical immediate failure: a channel-1 contact yields nothing.

- **E_world (`move`).** At tick T=8192 the channel-1 mapping flips. The route-1 entry is
  intact but *stale*; contacts use the stale port and fail **deterministically, forever**,
  until the entry is relinquished and re-bound blind. Correct response: **relinquish**.
- **E_machinery (`cut`).** At tick T the organism's *read* of the route-1 entry is
  suppressed for [T, T+W) (W=96) (`ac106.ReadCut` forces `memory.read(1) -> None`). The
  entry's replicas are untouched and its content correct; contacts fall back to blind
  search (success 1/4) and resume without re-binding when the read is restored. Correct
  response: **hold** (and maintain the still-valid entry through the outage).

The cut is a *read-machinery* cut, not a memory-bank cut: it shims only the contact's
`selected`, and the organism's introspection read (`o.memory.read(1)`) stays **bound**
throughout the window. This asymmetry is what makes the task identifiable (§4).

---

## 4. The minimal change: an intermittent `used_held` observation gate

The one change is a **declared observation-gate on `used_held`**, not a new cause and not
a physics change.

`used_held` is the K4 §3 interface change that forwards the contact's retrieval result to
the allocator (`alloc.outcome(o, action, e, int(selected is not None))`, `ac107.py` line
~327). In AC107/108 it takes two values — `used_held=1` (the contact used the held entry)
vs `used_held=0` (the contact fell back to blind) — and **this one bit is what separates
the two causes' unproductive signatures**: a move produces `(bound=1, used=1,
productive=0)` (held-fail), a cut produces `(bound=1, used=0, productive=0)` (blind).

The gate occludes this bit on a Bernoulli(`q`) fraction of channel-1 contacts, so the
organism observes

    used_held ∈ {held, blind, occluded}

instead of `{held, blind}`. On an **occluded unproductive contact** both causes read

    (bound=1, used_held=occluded, productive=0)

— **identical** — yet the correct action differs (move → relinquish, cut → hold).

The gate satisfies the card's constraints by construction:

- **No hidden cause label.** The gate does not reveal which cause is active; it only
  withholds one observation bit. The cause is never supplied to any arm.
- **No schedule access.** The gate is i.i.d. Bernoulli(`q`) per contact and is **not
  synchronized** with the cause onset (t=8192). The organism observes "occluded" as it
  happens; it is never told *when* the cause lands.
- **No privileged read path.** `used_held` and `bound` are the organism's own retrieval
  result and its own introspection (K4 §3 justification), available to **every** arm that
  possesses the route memory; the gate is applied uniformly to the candidate, the direct
  rival, and the history-based rival alike. An arm denied `bound`/`used_held` is an arm
  that cannot read its own memory, which is not a coherent rival here.
- **Balance-identity-safe.** The gate changes only the *forwarded* `used_held` value —
  never `selected`, never `productive`, never the memory, never any conservation quantity.
  The `ac4.balance` identities hold unchanged because nothing physical is altered (the
  same construction K4 §3 used for the original forwarding).

### Why this creates overlap where the AC107 gate did not

K4 §4's separation rests entirely on `used_held`: F1 (held-fail) and F2 (blind) are
disjoint precisely because `used_held` is always observed. Occluding it intermittently
removes the bit exactly at the contacts where the relinquishment decision is made, so a
transient discriminator cannot match either rule and falls through to a default that is
wrong for one cause — while a maintained accumulator of the last open-gate conclusion is
right for both. The overlap is *decision-relevant* (it lands on unproductive contacts),
not merely a shared productive observation.

---

## 5. The observation interface (allowed observations, all justified)

Per channel-1 contact the organism observes the triple

    (bound, used_held, productive)

- **`productive`** — did the contact yield (`e['productive'] = int(in_m + in_f > 0)`).
  Frozen, unchanged.
- **`bound`** — does my memory hold a live entry (`o.memory.read(key) is not None`).
  The organism's own introspection, unshimmed by the cut, so it reads **bound** through
  the window. Frozen, unchanged.
- **`used_held`** — did the contact use the held entry or fall back to blind. Now
  **three-valued**: `held` / `blind` / `occluded`, where `occluded` is the gate's output
  on a Bernoulli(`q`) fraction of contacts. This is the *only* change.

`bound` remains load-bearing and is never occluded (the two causes are still separable by
F2's `bound` at open contacts); the gate targets the one bit that separates the two
*unproductive* signatures.

---

## 6. The distinguishing histories (named features)

Under the C1/K4 **hold-and-observe** probe (withhold relinquishment, keep contacting
channel 1), three features carry the separation. The first two are K4's, now read only on
**open-gate** contacts; the third is the overlap.

**F1 — held-entry failure (one-sided ⇒ E_world).** An **open** contact with
`(bound=1, used_held=held, productive=0)` occurs **only** under a move. Presence of F1 is
diagnostic of E_world.

**F2 — blind-while-bound (one-sided ⇒ E_machinery).** An **open** contact with
`(bound=1, used_held=blind, productive=0)` occurs **only** under a cut (the read is
suppressed while the entry stays bound). Presence of F2 is diagnostic of E_machinery.

**O — the occluded unproductive contact (the overlap, both-sided).**
`(bound=1, used_held=occluded, productive=0)` occurs under **both** causes, and there the
current observation is identical while the correct action differs.

The maintained separator is then the *earliest* open unproductive contact's `used_held`:

    H = 'held'  ⇒ E_world  ⇒ relinquish
    H = 'blind' ⇒ E_machinery ⇒ hold

H is a function of the **past** (the accumulated open-gate history), not of any single
current observation. With `q < 1` an open contact occurs with probability `1-q` per
contact, so H is reached almost surely within a few contacts of the cause onset — the
memory need only survive from one open contact to the next.

### Why the memory is load-bearing, mechanically

At an occluded unproductive contact the transient discriminator (AC109's `_cause`) cannot
match `bound & not used` (needs `used=blind`) or `used & not productive` (needs
`used=held`), so it falls through to its default and is wrong for exactly one cause. The
maintained estimate (AC107's `Estimator`) reads its **stored** `e` — last set at the most
recent open contact — and is correct for both. The storage carries the open-gate
conclusion *across* the occluded gaps; that is the load-bearing role C1's world lacked.

---

## 7. Diagnostic result (small harness, run)

`_c2_identifiability.py` does two things, both against the frozen modules (import only,
no re-run of any study):

1. **Frozen-primitive assertions — all pass** (deposit no-op while bound; `ReadCut` shims
   only the contact read; blind fallback rate 1/4; `ac107` forwards
   `used_held=int(selected is not None)`).
2. **Hold-and-observe simulation** of the observation tuple under each cause with the
   gate (`q=0.5`, 400 contacts), reporting the three features:

   | cause | open F1 (held-fail) | open F2 (blind) | occluded-unproductive (ambiguous) |
   |---|---|---|---|
   | move | True  | False | 190 |
   | cut  | False | True  | 40  |

   The three identifiability claims, computed:
   - **Overlap** — `(bound=1, used_held=occluded, productive=0)` occurs under both causes,
     so the current observation is identical while the correct action differs.
   - **Non-separability by current observation** — no function of that single tuple names
     the cause.
   - **Separability by history** — the maintained separator H reads `held` under move and
     `blind` under cut (asserted), identifying the cause with certainty.

Identifiability from permitted histories is **demonstrated**, not assumed.

---

## 8. Rivals (the card's requirements)

- **Direct diagnostic rival (`direct`, AC109).** Reads `(bound, used_held, productive)`
  transiently, no stored estimate. This is the *history-free* arm: at an occluded
  unproductive contact it cannot match any discriminator rule and defaults to E_world —
  correct under move, **wrong under cut** (it counts a machinery outage as a stale route
  and relinquishes a still-valid entry). This is the contrast that isolates the storage.
- **Simple history-based rival (`r4`, the raw failure counter).** The
  `CONSCIOUSNESS_ROADMAP_v1.md` §4 "simple history-based rival": a per-key raw counter of
  **all** unproductive contacts (threshold HOLD_N), **no cause attribution**. It *has*
  history (it accumulates failures) but cannot tell a blind failure from a held failure;
  under cut it counts the intermittent blind failures and eventually drops the valid
  entry. This is the arm that separates "any history helps" from "attributed history
  helps": if `r4` matches the candidate, the candidate's *content* is inert even though
  history is present.
- **Candidate (`candidate`, AC107).** Maintains the one-bit cause estimate `e`; its
  discriminator fires only on open contacts (updating `e`), and its consumption reads the
  **stored** `e` at every unproductive contact — so at occluded contacts it acts on the
  last open-gate conclusion and is correct under both causes.

**Baseline success is admissible** (the card's constraint): the design's claim is that
maintained history *contributes a decision-relevant difference* (the right action at
occluded contacts), **not** that a mechanism named "belief" beats every alternative or
survives better. Whether the candidate's advantage is behavioural or survival-level is an
open question for the implementing study, not a design premise.

---

## 9. Interface changes declared; previous task preserved

- **Declared change:** `used_held` gains a third value `occluded`, emitted by a
  Bernoulli(`q`) gate applied uniformly to all arms. No new sensor, no new read path, no
  physics change — the same kind of declared interface change K4 §3 made when it first
  forwarded `used_held`.
- **Preserved:** AC107/108 and their frozen results, protocols, and hashes are untouched.
  This is a **new** task (new study identifier, AC110+), not a re-run or re-hash of the
  AC107/108 world. C1's AC109 result stands as the record of the *un*-gated world.

---

## 10. What this hands to C3 and C4

**C3 (ongoing repair after acquisition).** The load-bearing stored function now exists: at
an occluded unproductive contact the correct action is carried by the maintained estimate
`e`. C3 can therefore run the repair-vs-reacquisition contrast on *this* task — begin from
an acquired, correct `e`, cut the paid repair of its vulnerable storage while leaving
diagnostics available, and ask whether the estimate's correctness/use degrades
independently of re-acquisition. The occluded-gap structure gives the repair a genuine
window to matter (the estimate must survive from one open contact to the next).

**C4 (uncertainty).** The same overlap structure is C4's "overlapping/incomplete
evidence" task: at an occluded contact the organism *cannot tell* which cause is active
from the current observation, so a first-order uncertainty estimate (how confident am I
that `e` is still correct, given I have not seen an open contact for `k` contacts) has a
natural, decision-relevant target. The `q` parameter is C4's noise/evidence-completeness
knob; the theory connection is HOT-2 metacognitive monitoring (the roadmap §5), with the
estimate grading the reliability of its own first-order content.

---

## 11. Claim discipline

- This is a **level-(c) representational** design: it establishes that the cause
  distinction is *representable from the organism's own history* and that the history is
  *necessary* (not derivable from the current observation) at occluded contacts. It makes
  no claim that any organism *does* maintain it, no level-(d) claim, no metacognition
  claim.
- "History-identifiable" means "the accumulated open-gate history separates the causes
  given the stated (gated) observation interface" — not "the organism will succeed" and
  not "the estimate is load-bearing in the implemented organism". Whether the maintained
  estimate is *required* (vs a longer threshold, or a reactive read) is the implementing
  study's question, and is deliberately not pre-judged here.
- The two causes being identical at occluded contacts is a property of the task (the
  gate), and the separability at open contacts is a property of the interface (F1/F2);
  AC109's equivalence was a property of the *un*-gated world. The three must not be
  conflated.
