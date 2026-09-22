# Task identifiability v1 — K4: the two causes are separable, and here is the observation that separates them

2026-09-22. **Analysis document, not a study.** No experiment run, no seeds, no protocol,
no freeze. This is K4's deliverable (task t_1b995c9c): the identifiability analysis that
must precede K5's estimator. It answers the card's question and names the distinguishing
history features, so K5 implements an estimator against a *known-separable* task rather
than re-discovering AC106's confound.

Everything below was derived from the frozen/engineering sources already in the repo
(`ac9.py`, `ac9_memory.py`, `ac12.py`, `ac106.py`, `MAINTAINED_BELIEF_TASK_v1.md`,
`AC106_ERRATA_v1.md`), and the diagnostic `_ac106_k4_identifiability.py` (run, output
below). No frozen artifact was edited, re-run, or re-hashed.

---

## 1. The question

Is there a partially-observed task whose action-observation histories distinguish
**environmental change** (route move, E_world) from **impaired access machinery**
(read suppression, E_machinery), *without supplying the hidden cause or challenge
schedule to the candidate*?

**Answer: yes.** The task is identifiable, and the separating observation is already in
the organism's own state — it was simply never handed to the estimator. AC106's estimator
failed (the K1 confound) because it observed `productive` alone; the cause distinction
lives one observation deeper, in whether the organism's memory entry was still *bound*
when productivity resumed.

---

## 2. The hidden causes (unchanged from C1 §2 / AC106)

Both causes produce the identical immediate failure: a channel-1 contact yields nothing.

- **E_world (`move`).** At tick T the channel-1 mapping flips (`mapping[1] -> 1-mapping[1]`).
  The route-1 entry is intact but *stale* — it stores the port that was correct before the
  move. Contacts use the stored port and fail **deterministically, forever**, until the
  entry is relinquished and re-bound blind.
- **E_machinery (`cut`).** At tick T the organism's *read* of the route-1 entry is
  suppressed for [T, T+W) (`ReadCut` forces `memory.read(1) -> None`). The entry's
  replicas are untouched and its content is correct; contacts fall back to blind search
  and fail at the blind rate (1/PORTS), then resume succeeding **without re-binding** when
  the read is restored.

The cut is a *read-machinery* cut, not a memory-bank cut: it shims only the contact's
`selected` (`ac106.py` READ_LINE replacement, line 262), and touches nothing else. This
asymmetry is what makes the task identifiable (§4).

---

## 3. The observation interface (allowed observations, all justified)

Per channel-1 contact the organism can observe the triple

    (bound, used_held, productive)

- **`productive`** — did the contact yield income (`e['productive'] = int(in_m + in_f > 0)`).
  Already in the frozen event. Nothing new.
- **`bound`** — does my memory hold a live entry for the contacted key
  (`o.memory.read(key) is not None`). This is the organism's *own* introspection read. It
  is **not** shimmed by the cut (only the contact's `selected` is), so in E_machinery it
  reads **bound** throughout the window. This is the load-bearing observation.
- **`used_held`** — did the contact actually use the held entry or fall back to blind
  (`selected is not None`, the shimmed value). This is the organism's own *retrieval
  success* on the contact. It is the observation that *directly* records the cut's
  mechanism (the read returns None); `productive` changes only as a consequence of the
  port having been drawn blind instead of taken from the entry.

Justification and matched-rival availability (the card's constraint): none of the three
supplies the hidden cause or the schedule. `bound` and `used_held` are the organism's own
memory state and its own retrieval result — introspectively available to **any** rival
that possesses the same route memory (the frozen streak r2, a longer-threshold rival, a
state-blind rival). A rival that is *denied* `bound`/`used_held` is a rival that cannot
read its own memory, which is not a coherent rival in this architecture. `used_held` is
already computed in the frozen step (`selected`, `ac9.py` line 86) and merely not
forwarded to the allocator; forwarding it is an interface change, not a new sensor.

The observation is **action-dependent** (§6): the organism must *choose* to keep
contacting channel 1 to receive the distinguishing tuple. A reflex that relinquishes at
the first failure never observes the resumption and cannot separate the causes — exactly
C1 §6's point.

---

## 4. The distinguishing histories (named features)

The two causes produce disjoint observation tuples under the C1 §4 **hold-and-observe**
probe (withhold relinquishment, keep contacting channel 1). Three features carry the
separation:

**F1 — held-entry failure (one-sided ⇒ E_world).** A contact that used a held entry and
failed — `(bound=1, used_held=1, productive=0)` — occurs **only** under a move: the
stored port is stale, so the held entry fails deterministically. Under a cut, every
in-window contact is blind (`used_held=0`), so a held-entry failure is never observed.
Presence of F1 is diagnostic of E_world; its absence (a failure phase that is entirely
blind) is diagnostic of E_machinery.

**F2 — productivity-resumption via bound vs unbound (two-sided).** At the first productive
channel-1 contact following a run of failures, read `bound`:
- `bound=1` — productivity returned while the entry was still held ⇒ **E_machinery**
  (the read was restored on a valid entry; or a blind success landed during the window
  while the entry stayed bound).
- `bound=0` — productivity returned only after the entry went unbound ⇒ **E_world**
  (the stale entry was dropped and re-acquired blind).

F2 is the C1 §4 "re-bind-and-compare" probe, stated in terms of the organism's own bound
flag. It is the *two-sided* discriminator: it labels both causes, not just one.

**F3 — route retention / re-acquisition (behavioral consequence, corroborating).**
E_machinery never requires relinquishment — the entry is valid, so a correct estimator
holds the route throughout (no drop, no re-acquisition). E_world requires relinquishment
then re-acquisition (deposit fires only when `selected is None` and the key is unbound,
`ac9_memory.py` line 62). Relinquishment and deposit events are the organism's own
actions and corroborate F1/F2.

### Why these are separable, mechanically

The discriminator rests on one asymmetry, verified against the frozen code:

- `ReadCut` shims **only** the contact's `selected` (`ac106.py` line 262). The organism's
  introspection (`observe`, `o.memory.read`, renewal) reads the raw memory and sees the
  entry **bound** during the whole window.
- Therefore in E_machinery the organism observes `bound=1` while its contacts are blind
  (`used_held=0`) and intermittently productive (blind success, 1/4) — the pair
  `(bound=1, productive=1)`.
- In E_world the held entry is stale, so while `bound=1` productivity is **impossible**
  (a stale port never equals the new mapping); productivity returns only after the drop,
  when `bound=0`, as a blind re-bind `(bound=0, productive=1)`.

The two "productivity resumption" events that AC106 collapsed are therefore
**distinguishable by `bound`**: E_machinery resumes while bound; E_world resumes only
after unbinding.

---

## 5. The AC106 confound, restated precisely (K1's P2, and the fix)

AC106's update rule (`ac106.py` lines 203-216) fired `e = E_machinery` on **any**
productive contact-1 that followed a failure (`if cur > 0 and self.now >= DEV`), with no
read of `bound`. In E_world the blind re-bind (`bound=0, productive=1`) follows a failure
and trips the rule — mislabelling the re-acquisition of a dropped stale route as
"productivity resumed without re-binding". The estimator observed `productive` alone and
threw away the bound flag that separates the two resumption signatures.

**The fix (what K5 implements):** gate the E_machinery conclusion on `bound==1` at the
productive event — i.e. consult the organism's own memory, not just the outcome. This is
the C1 §4 probe, and it is exactly the "action/outcome history sufficient to avoid
confusing re-acquisition with restored access" the K5 card names.

---

## 6. Deliverable checklist (the card's named items)

- **Blind success.** In E_machinery the 1/4 blind success during the window is
  `(bound=1, used_held=0, productive=1)` — it keeps `bound=1` and therefore *fires* F2
  toward E_machinery. In E_world the blind success is `(bound=0, productive=1)` — the
  re-bind that *fires* F2 toward E_world. Same raw outcome, opposite `bound`.
- **Re-acquisition.** E_world recovers by re-acquisition (`bound` 1→0 at the drop, 0→1 at
  the blind re-bind). E_machinery has **no** re-acquisition (`bound` stays 1 throughout;
  `deposit` is a no-op while the key is bound). Re-acquisition events are the organism's
  own and corroborate F2.
- **Route retention.** E_machinery retains the route (no drop); E_world loses it (drop
  required). This is a *consequence* of correct attribution, not an independent signal.
- **Intervention duration.** W = 96 vs entry life 64. The identifiability of E_machinery
  is **conditional on the entry surviving the window** — if the entry expires mid-window
  (`bound` 1→0), the history degrades into re-acquisition and the causes become
  indistinguishable. The reactive renewal (action 3/4) reads the *unshimmed* memory and
  therefore *can* fire during the cut, so the entry survives when the program chooses
  renewal; this is the AC74 attention-hijack exposure that AC106's proactive renewal
  existed to close. Boundary and minimal revision in §8.
- **Action-dependent observations.** F2 exists only if the organism holds and keeps
  contacting. The distinguishing observation is the contingent outcome of the organism's
  own intervention, not a passive read — the C1 §6 requirement, met.

---

## 7. Diagnostic result (small harness, run)

`_ac106_k4_identifiability.py` does two things, both against the frozen modules (import
only, no re-run of any study):

1. **Frozen-primitive assertions** — all pass:
   - `ac9_memory.deposit` is a no-op while the key is bound (line 62);
   - `ac106.ReadCut` shims only the contact read and only in-window, while the
     introspection read stays bound;
   - blind fallback is uniform over PORTS=4 (measured success rate 0.25 ± 0.005).

2. **Hold-and-observe simulation** of the contact tuple under each cause (200 contacts):

   | cause | held-failing F1 `(1,1,0)` | productive-while-bound `(1,·,1)` | ever-unbound |
   |---|---|---|---|
   | move | **True** | **False** | False (holds forever, never yields) |
   | cut  | **False** | **True** | False (stays bound, yields intermittently) |

   The two causes produce disjoint observation tuples on `(bound, used_held, productive)`;
   F1 separates E_world and F2 separates E_machinery. Separability is demonstrated, not
   assumed.

---

## 8. Verdict and boundary conditions

**Identifiable: yes.** The distinguishing history features are **F1** (held-entry failure,
one-sided ⇒ E_world) and **F2** (resumption-via-bound vs -unbound, two-sided), read from
the organism's own `(bound, used_held, productive)` observation.

Two boundary conditions must be stated, or the "yes" over-reaches:

1. **Entry survival through the window.** If the entry expires mid-window, E_machinery
   degrades to re-acquisition and is unobservable. This is met either by reactive renewal
   firing (economy-dependent) or by the estimator's own proactive renewal (the E_machinery
   branch). K5 must *measure* entry survival at the window end per individual, not assume
   it — an individual whose entry lapsed mid-window is a non-vacuity case, not a
   discriminator failure.
2. **The cut must remain a *read* cut.** Identifiability depends on the cut suppressing
   only the contact read while leaving the introspection read and the entry intact. If the
   cut were broadened to erase the entry (a memory-bank cut), `bound` would read 0 during
   the window and the two causes would be indistinguishable — a genuinely unidentifiable
   task. The C1 §2 definition already pins the cut as read-only, so no revision is needed;
   this is stated as the boundary beyond which the answer flips.

**Minimal justified revision (only if the entry does not reliably survive W = 96):**
shorten the window to W ≤ 64 (the entry life), so the entry survives the window without
any renewal. This is a *declared world constant* change — the same kind AC11→AC12 and
AC106's own PORTS=4 were — not a new observation and not a law patch. It is offered, not
required; the AC106 candidate's proactive renewal already keeps the entry alive in 14/16
individuals, so W = 96 is serviceable where the estimator maintains the entry.

---

## 9. What this hands to K5

K5 implements an estimator against a task now known to be separable. The concrete
specification it inherits:

1. **Observation:** forward `bound` (and optionally `used_held`) to the estimator's
   update rule. `bound = (o.memory.read(key) is not None)`; `used_held = (selected is
   not None)`. Both are the organism's own state/retrieval, available to every rival.
2. **Discriminator:** on a productive channel-1 contact, read `bound`. `bound=1` ⇒
   E_machinery (hold + proactive renewal); `bound=0` ⇒ E_world (relinquish). This is the
   re-bind-and-compare rule AC106 never built (K1's P2).
3. **Measure discrimination at decision times** (`drop_ticks`, `restore_ticks`), not only
   `bel_at_horizon` — K1's P3.
4. **Fix the rival defect:** a genuinely longer threshold needs its own counter state
   (the 3-bit Gray streak saturates at 7; `HOLD_N == STREAK_N` was K1's P1). The
   longer-window rival must also receive `bound`, or it is not a matched rival to the
   estimator.
5. **Non-vacuity:** report, per individual, whether the entry survived the window (an
   individual whose entry lapsed mid-window never had a discrimination opportunity).

---

## 10. Claim discipline

- This is a **level-(c) representational** analysis: it establishes that the cause
  distinction is *representable from the organism's own state*, nothing more. It makes no
  claim that any organism *does* represent it, no level-(d) claim, no metacognition claim.
- "Identifiable" means "the action-observation histories separate the causes given the
  stated observation interface" — not "the organism will succeed" and not "the estimator
  is load-bearing". Whether a maintained estimate is *required* (vs a longer threshold, or
  a reactive read of `bound`) is K5's question, and it is deliberately not pre-judged here.
- The two causes being separable is a property of the task; AC106's failure was a property
  of its estimator's observation choice (it read `productive` and dropped `bound`). The
  two must not be conflated: K1's P2 correction ("the distinction is untested, not
  unrepresentable") is confirmed, not overturned.
