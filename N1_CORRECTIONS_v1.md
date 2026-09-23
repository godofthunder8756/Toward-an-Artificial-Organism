# N1 corrections v1 — scoping the AC107/AC108 coupling claims to what the artifacts license

2026-09-23. Corrections note for the N1 card (t_cb679061). It corrects the scope of
claims made in `AC107_RESULTS_v1.md`, `AC108_RESULTS_v1.md`, `K9_SYNTHESIS_v1.md`,
`AUTONOMY_RESEARCH_STATUS.md`, and `CONSCIOUSNESS_ROADMAP_v1.md` §10, without editing any
frozen artifact (no runner, protocol, results dir, or hash is touched). Every correction
below was verified against the source (`ac107.py`, `ac108.py`, `ac106.py`) and the frozen
rows (`ac107_results_v1/rows.jsonl` 240 rows, `ac108_results_v1/rows.jsonl` 288 rows).

The valid positives are retained unchanged: discrimination (0/32 mistakes), storage
maintenance (state sufficiency + no-cause identity), behavioural causality, and the
coupled content -> adaptation direction. The valid negative is retained unchanged: the
survival advantage did not transfer to the fresh families (AC107 Q4; the cut-side bite is
priority-corner-specific). These corrections narrow overreaching *framing*; they invent no
positive and revoke no measured result.

---

## 1. `no_write` cuts acquisition/update, not ongoing repair (AC108 direction 1)

**What the code does.** `ac108.py` `CouplingEstimator._bel_write` (lines 113-116) returns
`(0, 0, 0)` when `self.write is False`; `_bel` (the read) is unchanged. The only paid write
on the estimate is the cause-onset acquisition/update write: frozen AC107 rows show
`bel_writes == 7`, `bel_attempts == 1` in `cut` (one atomic flip of 7 replicas from the
acquired E_world=1 to the correct E_machinery=0), and `bel_writes == 0`,
`bel_attempts == 0` in `move` (the acquired value is already E_world, nothing to write).
The `no_write` rows confirm the intervention only removed that write: `bel_writes == 0`,
`bel_attempts == 0`, `bel_at_cut_end == 1` in 16/16 (the bit stays E_world and is wrong).

**The correction.** `no_write` prevents the *acquisition/update* of the estimate — the
single paid flip from E_world to E_machinery that establishes cut-side accuracy. It does
**not** selectively disable ongoing repair of an already-correct estimate, because no such
repair loop exists or runs in this world: the maintenance is a single paid write at
cause-onset and the 96-tick window is far shorter than the 1e-4/replica/tick sticky damage
rate (the AC13 wall, disclosed in `AC107_RESULTS_v1.md` §3). "Direction 1: maintenance is
load-bearing for accuracy" must therefore be read as **"the paid acquisition/update write is
load-bearing for accuracy"** — not "ongoing repair is load-bearing." The phrase
"maintenance -> accuracy/use" in `AC108_RESULTS_v1.md` §1 and `K9_SYNTHESIS_v1.md` §1.1
carries this narrower meaning; it should be stated, not left implicit.

## 2. The AC107 diagnostic interface is an explicit `bound`/`used_held` split

**What the code does.** `ac107.py` line 250 reads `bound = (o.memory.read(1) is not None)` —
an **unshimmed** introspection read of the organism's own route memory. Line 251 reads
`used = bool(used_held)`, where `used_held` is the **shimmed retrieval result** (`selected`)
forwarded to the allocator by the injected line `alloc.outcome(o,action,e,int(selected is not None))`
(`ac107.py` line 327). The read-cut (`ac106.py` `ReadCut.read`, lines 143-146) suppresses
`selected` for key 1 in-window while leaving the entry in `o.memory` — so during the cut
`bound == 1` but `used_held == 0`.

**Information access.** Two signals about the *same* contact: (a) the organism's own memory
introspection (`bound`, intact, never shimmed), and (b) the outcome of the retrieval the
organism just performed (`used_held`, subject to the cut). The discriminator fires
E_machinery on the *discrepancy* `bound and not used` ("my memory still holds the entry, but
the contact did not actually use it"), which is the cut signature.

**Assumptions (stated, not hidden).** (i) `bound` is a genuine introspection read and is not
shimmed by the intervention; (ii) the read-cut is the *only* mechanism in this world that can
produce `(bound=1, used_held=0)` — under E_world a bound entry is always used (`used_held=1`)
and fails, so the signature is unambiguous; (iii) this is K4's task-property (disjoint
action-observation histories), not a new sensor — `used_held` is an interface change
(forwarding the shimmed retrieval result), and the interface's discriminator is correct only
*conditional on* assumptions (i) and (ii) holding. Any future world that can suppress a
retrieval by another path, or that shims the introspection read, breaks the interface's
unambiguity.

## 3. Paid diagnostic state with behavioural consequences — but sustained repair coupling is NOT yet evidenced

**What is established.** The estimate is a **paid** state: `bel_write` is W-gated through
`ac95._cap` (`ac107.py` lines 102-126), costs energy + material per replica, and is excluded
from `reg_from_active`. Its content **causally selects behaviour**: E_world -> the frozen
Gray-streak relinquishment; E_machinery -> withhold relinquishment + paid proactive renewal
(`ac107.py` lines 286-302). Single-flag interventions show the read is behaviourally causal
(`scramble` relinquishes a valid route on 6001/6006 where the candidate holds; `no_write`
does so on 6100/6101/6104/6105) and the content forces the adaptation (`force_machinery`
holds the stale route 16/16 where the candidate relinquishes 16/16).

**What is NOT established.** **Sustained representation-repair coupling** — an ongoing,
load-bearing repair loop that keeps an already-acquired estimate correct against continuing
damage — has not been run. The repair loop is not exercised (single write; damage too slow in
the window). "Maintenance sustains function" holds only in the storage-content sense
(`AC107_RESULTS_v1.md` §3): the function depends on the maintained storage's *content*; the
ongoing *repair* of that storage is not load-bearing and is not claimed. This is the boundary
the C3 card (isolate ongoing repair after successful acquisition) exists to cross; it needs
separate evidence (a damage model that actually flips replicas within the window, plus a
repair arm that restores them).

## 4. Adaptation reversal is 16/16; the survival reversal is 12/16

**Row-verified.** In `ac108_results_v1/rows.jsonl` (finals 6100-6107):

- **Adaptation reversal (behavioural, clean):** candidate relinquishes >=1 in `move` in
  16/16; `force_machinery` relinquishes 0 in 16/16. This 16/16 is the *adaptation* reversal.
- **Survival reversal (partial):** `force_machinery` dies 16/16 in `move` (0 survivors);
  the candidate survives **12/16**, dying on 6100 and 6107 (the re-acquisition boundary, the
  AC83/AC74 path — a starved re-bind, not a coupling failure). `r4` survives 6/16 (dies
  6100, 6102, 6103, 6104, 6107).

**The correction.** The phrase "representation content -> adaptation/production/viability
16/16 in the move" (`AC108_RESULTS_v1.md` §1/§6, `K9_SYNTHESIS_v1.md` §1.1,
`AUTONOMY_RESEARCH_STATUS.md`, `CONSCIOUSNESS_ROADMAP_v1.md` §10) correctly reports that
`force_machinery`'s *collapse* is 16/16 — but it must not be read as a 16/16 survival
reversal. The survival reversal is **12/16** (candidate survives 12/16 where force_machinery
dies 16/16); the candidate still dies on 2/8 seeds. State the two numbers separately:
adaptation reversal 16/16, survival reversal 12/16, collapse (force_machinery) 16/16.

## 5. Partial results are independent of the failed survival gates

A failed survival gate does not erase a measured behavioural contrast or a storage-
maintenance confirmation. This is already the practice in `AC107_RESULTS_v1.md` (Q1/Q3 pass
recorded alongside Q2/Q4 fail) and `AC108_RESULTS_v1.md` (survival reported, not gated).
The corrections note reaffirms it as a standing rule for this line: the behavioural
causality (`no_write` relinquishes 4/8, `scramble` relinquishes 4/8 where the candidate
holds; `force_machinery` holds 16/16) and the storage-maintenance result (observer-discard
16/16, no-cause identity 16/16) stand regardless of whether the survival contrast bites.
Downstream summaries must not let "survival advantage did not transfer" absorb the
behavioural and storage positives.

## 6. Ceiling accuracy limits THIS reliability task; it is not a universal wall

K8 blocks because the first-order estimate is ceiling-accurate (0 mistakes) **in this
world**, where K4's perfect identifiability (disjoint action-observation histories) makes
misattribution structurally impossible. That is a property of the *current task design*, not
a general impossibility and not an established universal "structural wall." The K9 §3.1
phrase "the ceiling-accuracy reliability wall" and §2's cataloguing of it as a fourth
"structural wall" overreach in exactly this way: the ceiling is reversible by any of the
three named reopening routes (relax identifiability, degrade the observation interface, add
a third cause), each of which introduces a non-zero error rate. It is "blocked by success,"
a vacuity of the current task — the mirror of C3's vacuity — not a demonstrated limit on
reliability monitoring in general.

## 7. Three-cause integration is ONE composition study, not the only legitimate continuation

`K9_SYNTHESIS_v1.md` §4 names the three-cause integration "the one gated follow-on
experiment." It is *one* candidate composition, warranted only if the survival/composition
question is judged load-bearing — not the only legitimate continuation. The board's own
planning graph lists several others, each open and equally legitimate: C1 (compare against a
direct diagnostic controller), C2/C3 (establish a task where history has a testable role /
isolate ongoing repair after acquisition), C4 (uncertainty as a separate question), I1
(composition without conflating uncertainty). Three-cause integration is a *possibility*,
not the uniquely-authorized next step.

## 8. "First demonstrated coupling" is scoped to THIS project

The "first" claims — `K9_SYNTHESIS_v1.md` §1.1 "the first time a level-(c) representation
is shown causally coupled to the level-(a/b) machinery", §2(iii) "the first demonstrated
causal coupling", `AC108_RESULTS_v1.md` §8, and `AUTONOMY_RESEARCH_STATUS.md` "the first
causal coupling of a level-(c) representation to the level-(a/b) maintenance machinery" —
assert empirical priority over all prior work. `K9_SYNTHESIS_v1.md` §2 establishes "no
conceptual novelty" against Maturana & Varela, Montevil & Mossio, Di Paolo, Butlin et al.,
and the maintenance prior art, but it does **not** establish empirical priority: no
primary-literature search for prior demonstrations of representation<->maintenance coupling
in simulated organisms supports "first demonstrated." Until such a comparison exists, the
claim is **"first demonstrated in this project's lineage"** (or "to our knowledge within
this project"), not a field-level first. This matches the project's own standing discipline:
an honest novelty statement must be scoped to what a primary-literature comparison supports.

---

## What is NOT changed (the retained positives and negatives)

- Discrimination at decision times: 0/32 mistakes on the untouched 6000-6007 family
  (`AC107_RESULTS_v1.md` §1). Retained.
- Storage maintenance in the content sense: observer-discard per-tick byte-identity 16/16,
  no-cause identity 16/16, vulnerable-storage audit (`AC107_RESULTS_v1.md` §3). Retained.
- Behavioural causality of the read (`scramble`/`no_write`) and the content
  (`force_machinery`/`scramble`), gated G1-G4 in `AC108_RESULTS_v1.md`. Retained.
- Survival advantage did not transfer (AC107 Q4 seed-bounded; cut-side bite
  priority-corner-specific). Retained as the honest negative.
- K8 reliability tier is BLOCKED, not falsified, with reopening conditions on record.
  Retained.

## Verification

Numbers in this note were recomputed from the frozen rows (not the docs' prose):

- `no_write` cut: `bel_writes == 0`, `bel_attempts == 0`, `bel_at_cut_end == 1` (16/16);
  candidate cut: `bel_at_cut_end == 0` (16/16).
- AC107 candidate cut: `bel_writes == 7`, `bel_attempts == 1`; move: `bel_writes == 0`,
  `bel_attempts == 0`; mistakes == 0.
- AC108 move: force_machinery survivors 0/16; candidate survivors 12/16 (deaths 6100, 6107);
  r4 survivors 6/16 (deaths 6100, 6102, 6103, 6104, 6107); candidate relinquishes >=1 in
  16/16, force_machinery relinquishes 0 in 16/16.
- AC107 move: candidate survivors 14/16 (death 6002); r4 survivors 10/16 (deaths 6002, 6003,
  6007); scramble cut survivors 16/16.

No frozen artifact was edited. This note is a derived successor document and is not hashed
into any study's `pre_run_snapshot.json`.
