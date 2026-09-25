# M4 — Monitor-input audit and identifiability verdict

2026-09-25. Audit deliverable for the M4 card (t_6145d172): *which monitor inputs are genuinely
accessible to the organism (sensed, paid, surviving observer-discard, rival-received) vs
experimenter-only, and can the permitted observations distinguish the relevant cases?* This
document runs nothing, freezes nothing, re-hashes nothing, and edits no frozen artifact. It audits
the five inputs M3 (`M3_MONITOR_TARGET_v1.md` §3) listed for the monitor state `m`, against the
AC110/AC116 economics, and returns the identifiability verdict M5 is conditioned on.

One sentence up front: **`m`'s referent — "the decoded first-order estimate `e` is wrong" — is only
PARTIALLY identifiable from the permitted observations: the damage-induced component of wrongness
is identifiable (given two corrections to M3's input list), but the staleness-induced component is
unidentifiable by any observation the organism can make, and in the pure AC110/AC116 decision window
the estimate has no error variance at all (ceiling accuracy), so the monitor is well-posed only in
the post-window damage regime and the corrupted-schedule regime.** M5 can proceed, with a scoped
target and a corrected input list.

---

## 1. The audit table — the five proposed inputs, one row each

Columns: **source** (where the value physically lives); **obtained** (how the organism gets it);
**cost** (does sensing/retaining it incur a modeled cost); **observer-discard** (does it survive the
AC95-D4 discard equivalence); **rival-received** (does the corresponding rival get it); **experimenter-only**
(would supplying it violate the no-hidden-label constraint).

| # | input (M3 §3) | physical/operational source | obtained | cost | observer-discard | rival-received | experimenter-only? |
|---|---|---|---|---|---|---|---|
| 1 | `bel_minority = min(ones,7−ones)` at `bel_off` | the estimate bit's 7 replicas in `traces[0, bel_off]` (`ac106.py:96-110`, `bel_offset`/`bel_read`/`bel_minority`) | a READ of the organism's own program bank — free; the same per-bit disagreement the bank-0 majority-restore (action 2) already computes via `argwhere(traces != majority)` | sensing FREE (reads are not charged in this economy; only writes pay). RETAINING `m` and its write-history = paid W-gated writes + ongoing paid repair | YES for the substrate count itself (a function of `traces[0]`). NO for the runner's host-side log fields (`bel_minority_at_cut_end` etc.) — those are observer bookkeeping and must be re-derived, not read | the locus exists in every arm (frozen program bit, acquired 1), but only the candidate WRITES it to 0; rivals leave it at all-1, so their count is frozen at 7 and silent | NO — it is the organism's own substrate |
| 2 | `obs` bit 2 (whole-bank corruption) | `ac9.observe` (`ac9.py:56`): `int(np.minimum(ones,7-ones).sum()>=4)<<2` over `traces[0,:126]` | already computed every tick by the frozen perception interface (`prog.choose(b.traces, observe(o))`, `ac9.py:84`) — the organism's own observation | sensing FREE (already part of the frozen economy). Retaining a copy costs writes | YES — it is the frozen observe output, not host state | YES — every arm receives the frozen obs bits (it selects the program's action) | NO |
| 3 | repair-write outcomes (starved by W=0/budget) | the shortfall `n > cap` in `bel_write` / the repair, where `cap = _cap(b) = min(32, 8·W, energy, material)` (`ac95.py:336`) | NOT currently an organism signal — the frozen repair writes `min(cap, sites)` and discards the shortfall. It is DERIVABLE from the resource signals (W count, energy, material) the organism already observes; the runner's `bel_refused`/`reg_writes` counters are host-side | deriving it is FREE (a function of already-observed W/energy/material); the host log fields do NOT survive discard | only if re-derived from `available(b)`/`_cap`, NOT read from the Python tally | the resource signals it reduces to (W, energy, material, obs bits 0/1/6) are shared | NO — but it is REDUNDANT with input 5 (see §2) |
| 4 | re-acquisition events (`bel_write` fired) | the organism's own write to the estimate bit (`ac107.py:102-126`); the runner logs `bel_events` host-side | the organism KNOWS when it fires `bel_write` (its own action). The disambiguating content is the WRITE VALUE (0 vs 1), not just "fired" | RETAINING "last write value" as `m`'s input = a paid maintained record (distinct from `e`'s own replicas); the transient "fired" flag is FREE but carries no direction | the retained value must live in maintained state (vulnerable, paid) to survive discard; the host `bel_events` list does NOT | NO — rivals that don't maintain `e` don't fire `bel_write` at all, so this input is candidate-private | NO — it is the organism's own action history, not the cause |
| 5 | resource signals (W count, fuel/material bits) | `ac4.available(b)[:4]` (W); obs bit 0 = `fuel<=8`, obs bit 1 = `material<=64`, obs bit 6 = W<2 / region-catalyst low, obs bit 7 = C<2 (`ac9.py:52-67`) | already computed by the frozen observe every tick | sensing FREE | YES | YES (shared frozen economy) | NO |

**The shared-vs-private split, in one line:** inputs 2 and 5 (and 3, reduced to 5) are the frozen
perception/economy — every arm has them. Inputs 1 and 4 are the CANDIDATE's own maintained estimate
and its write history — a rival only "receives" them by becoming the candidate (or a variant). This
is what makes the reflex (obs bit 2) the correct null and makes P5 ("a fixed duty cycle must fail to
reproduce `m`") non-vacuous: the reflex has 2 and 5 but lacks the estimate-specific content of 1 and 4.

---

## 2. Two corrections to M3's input list

M3 named the right five *sources*; two of the five as named are wrong-shaped for the referent.

**(a) Input 1 must be the DIRECTIONED per-bit count, not the collapsed `bel_minority`.** The
estimate bit under cut is written to 0 and the sticky-SET stream flips replicas 0→1, so `ones =
traces[0,bel_off].sum()` runs 0→7 while `min(ones,7−ones)` runs 0,1,2,3,3,2,1,0. The collapsed
minority is therefore **(i) ambiguous at the boundary** — `min(ones,7−ones)=3` is produced by BOTH
`ones=3` (3 replicas damaged, decoded still 0, correct) and `ones=4` (majority flipped, decoded 1,
wrong) — and **(ii) non-monotone in wrongness** — it returns to 0 at `ones=7`, where the estimate is
maximally wrong (all replicas agree on the wrong value). A monitor that flags "minority>0 ⇒
unreliable" would read "reliable" at the most-wrong state and false-alarm at the still-correct 3-damage
state. The wrongness referent is carried by the **directioned count** (`ones`, or equivalently the
decoded majority together with the disagreement), which the organism can read for free (it is its own
substrate; action 2's restore already reads every replica). This is not a new sensing mechanism — it is
the same read the repair already performs, restricted to the estimate bit.

**(b) Input 3 (repair-write outcomes) is not an independent primitive.** "Was the repair starved" is
a deterministic function of the resource signals in input 5 (`cap = min(32, 8·W, energy, material)`).
Listing it separately invites a hidden second counter; the honest list derives it, or drops it. M5
should keep input 5 and treat "repair will be refused" as a derived predicate over it (which is
exactly P3's leading-indicator form).

**(c) The load-bearing content of input 4 is the write VALUE, not the event.** "`bel_write` fired" is
uninformative (it fires on every open in-window contact). What disambiguates wrongness is "the last
write value was 0 (E_machinery)" — see §4, case (a) vs (d). This is the one input that must be RETAINED
as a maintained record (it is not recoverable from `e`'s own replicas once damage has flipped them),
and it is the organism's own action history, so it is legitimate (not a hidden cause label).

---

## 3. The four discriminating cases

Each case is stated in the AC110/AC116 world (estimate acquired 1 = E_world; cut writes 0 =
E_machinery; sticky-SET `traces[0,:126] |= core_flips` at 1e-4/replica/tick; `e` read by majority ≥4/7;
correctness = `decoded e == cause`, evaluator-scored).

**Case (1) — storage damage while the decoded estimate remains correct.** Under cut, after the
first `bel_write(0)`, 3 of 7 replicas have been sticky-SET to 1: `ones=3`, `bel_minority=3`, decoded
`e=0` (majority intact), so `e` is CORRECT. The directioned read (`ones=3`) says "3 replicas flipped
toward 1, majority still 0". A correct monitor must read **reliable** here (it has not crossed the
4/7 threshold); a monitor that flags on `minority>0` false-alarms. This case pins the READ convention
and the threshold (the AC14/AC69 rule: state rate and read threshold together).

**Case (2) — an intact but stale estimate.** The estimate's storage is untouched (`ones` = its
written value, `bel_minority=0`) but its content is stale: it holds a value that no longer matches
the cause. It occurs (i) at every cause onset — in the pure cut world at t=8192 `e` still reads its
acquired 1 while the correct value is 0, until the first open contact fires `bel_write(0)` (AC110's
measured 2–31-tick re-acquisition latency, AC111's record) — and (ii) whenever re-acquisition is
delayed or omitted (AC111 seed 6306: no open in-window contact, `e` stays 1=E_world, wrong, all
window). No permitted observation distinguishes this from "intact and correct", because the
distinguishing fact is the cause, which is evaluator-only. **This is an unavoidable MISS — the one
case the monitor cannot detect.** It is structurally identical to the move world's correct state
(`e=1`, `ones=7`, `minority=0`).

**Case (3) — an incorrect estimate with little/no generic corruption signal.** Under cut, `ones=4`
(majority flipped, `e` reads 1, wrong), but a single bit contributes `min(4,3)=3 < 4` to obs bit 2's
whole-bank sum, so the corruption reflex stays silent (the AC76 single-bit rule). A correct monitor
flags **unreliable** by reading the per-bit directioned count (`ones≥4` + last-write 0); the reflex
misses it. This is P2, and it is the monitor's discriminating value over the reflex.

**Case (4) — a correct estimate despite resource shortage / a refused write.** Under cut, W has
collapsed or the budget is exhausted (`cap=0`), so `bel_write`/repair is refused, but the estimate's
majority is still correct (`ones≤3`). The resource signals (W count, obs bit 0/1/6, derived "repair
refused") fire while `e` is correct. A correct monitor reads **unreliable here as a LEADING
indicator** (it warns that repair is about to fail and `e` will drift — P3, "m leads e"), and this is
a FALSE ALARM relative to current wrongness. Under move the same resource signals fire while `e` is
correct *and can never become wrong* (damage inert), so a monitor that maps resource signals directly
onto "e is wrong now" is wrong by construction in the move world (P1's decoupling test).

**Can the permitted observations distinguish the four?** {1,3,4} are mutually distinguishable and
distinguishable from "correct + undamaged" by the directioned count + the retained write-value +
the resource signals. Case {2} is observationally identical to "correct + undamaged" — it cannot be
distinguished. The four cases therefore exercise: 1 = the read-threshold convention (false alarm vs
miss); 2 = the declared blind spot (record it, do not infer more); 3 = the P2 catch (value over the
reflex); 4 = the P3 lead (value over a concurrent damage read).

---

## 4. Identifiability verdict

**PARTIAL identifiability. The referent "P(decoded `e` is wrong)" splits into two components with
different observability, and a third regime with no variance at all.**

1. **Damage-induced wrongness — IDENTIFIABLE.** Wrongness arising from the estimate's majority being
flipped after a write to 0 (the AC110 post-window drift: `maintained` holds 16/16, `no_repair`
drifts 8/16) is a function of the directioned per-bit count, disambiguated by the organism's own
write-value history. Under the frozen sticky-SET model the damage direction is fixed (0→1) and the
acquired value is 1, so "last write was 0 AND `ones≥4`" is the full, observable condition for
damage-wrongness. The direction knowledge is the organism's own action history, not the cause: the
organism wrote 0 (E_machinery) at the open contact, so it knows "a flip toward 1 is toward error".
This is not a hidden label; it is the semantics its own discriminator already implements.

2. **Staleness-induced wrongness — UNIDENTIFIABLE.** Wrongness with intact storage (case 2) has no
substrate or resource signature. It is indistinguishable from "correct" by every observation the
organism can make, because the separator is the cause. This is a structural limit, not a tuning miss;
no added sensing mechanism within the economy's read interface can close it (any input that could
would be the cause label, which is evaluator-only by constraint).

3. **The pure decision window has no error variance — the target is vacuous there.** In the
un-composed AC110/AC116 world the discriminator fires `bel_write` on the same contact that consumes
`e` (AC110 `GatedEstimator.outcome`: the discriminator writes at lines 146-158 before the consumption
reads `self._bel(o)` at 167/171), so at every decision time `e` is correct — AC110's G2 "16/16
accuracy equality" is exactly this. The monitor is only well-posed where `e` is *sometimes wrong at a
decision time*, which requires the post-window damage regime (AC110 G4) or the corrupted-schedule
regime (AC111). This is K8's "no error variance to predict" block re-entering, and it is the single
most important fact for M5's harness: **the monitor must be exercised in a regime where `e` is wrong
for implementation reasons, and the pure primary window is not that regime.**

**Consequence for M5.** The target is identifiable and worth freezing, PROVIDED the referent is
scoped to the **damage component** of `e`'s wrongness, exercised in the post-window (or
corrupted-schedule) regime, with the staleness component recorded as an unidentifiable residual and
the pure-window ceiling accuracy stated as a non-vacuity condition. If instead the referent is left as
the unqualified "P(`e` wrong)", the monitor is unfalsifiable-as-correct (it will miss case 2 by
construction) and the gates P1–P3 must be scored against the damage component only. M5 must also adopt
the two §2 corrections: the directioned per-bit count (not `bel_minority`), and the retained
write-value (not a bare "re-acquisition fired" flag); and it must not read `bel_refused`/`bel_events`
from host logs (re-derive from substrate).

---

## 5. Experimenter-only (the constraint audit)

These are evaluator-only and MUST NOT be exposed to `m` or any rival, directly or by derivation:

- the hidden cause label (`move`/`cut`; `ac110._true_cause`, `ac107._true_cause` — used only to
  score `bel_wrong_ever`/`bel_wrong_in_window`/`first_wrong_read`, `ac110.py:341, 399-410`);
- the corruption masks / challenge schedules (`MOVE_TICK`/`CUT_TICK`/`WINDOW`, the read-cut window
  boundaries, the gate RNG stream);
- pristine templates / the reconstruction target (`build_program(description)`), except as the
  organism's own already-internalized description (AC80/AC85);
- the diagnostic logs (`bel_wrong_ever`, `first_wrong_read`, `bel_minority_at_cut_end`,
  `occluded_reads_1`, the host-side `bel_events`/`counter_events`/`tuned_events` lists).

None of inputs 1–5 exposes these. The one item that *looks* borderline — the damage-model DIRECTION
(sticky-SET 0→1) — is a fixed-law fact, the same status as the renewal law or the balance identity the
organism's program already embodies; knowing "damage sets toward 1" is not knowing the cause, and the
direction is carried by the organism's own writes, not supplied.

---

## 6. What this hands to M5

M5 freezes a harness whose referent is the **damage component** of "`e` is wrong", with: the
directioned per-bit count and the retained write-value as `m`'s estimate-specific inputs; obs bit 2,
the resource signals, and the derived repair-refused predicate as the shared inputs; the state-blind
fixed-duty and the obs-bit-2 reflex as the nulls (they share inputs 2/5 but lack 1/4); the regime
specified so `e` is wrong at decision times (post-window damage, and/or corrupted-schedule with the
staleness blind spot declared); and P1–P3 scored against the damage component with case 2 recorded as
an unidentifiable residual. Referent, once, for the record: **the correctness of the first-order
estimate `e`, identifiable for its damage component only.**

---

## Sources

`ac9.py` (observe, `ac9.py:52-67`; obs bit 2, `:56`), `ac95.py` (`_cap`, `:336`; `maintain`,
`:729-748`), `ac106.py` (`bel_offset`/`bel_read`/`bel_minority`/`bel_write`, `:96-126`),
`ac107.py` (`bel_write` with attempt/refused, `:102-126`; discriminator order, `:243-302`),
`ac110.py` (damage stream `:357`; GatedEstimator discriminator `:145-162`; evaluator-only scoring
`:341,399-410`), `ac116.py` (`CounterAlloc`, hold latch = estimate bit, `:121-198`),
`M3_MONITOR_TARGET_v1.md`, `references/ac110.md`, `references/ac111.md`, `references/ac95-d4.md`.
This document is derived and is NOT hashed into any study's `pre_run_snapshot.json`.
