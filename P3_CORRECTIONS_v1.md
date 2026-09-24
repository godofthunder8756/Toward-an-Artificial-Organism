# P3 corrections v1 — reconciling the N-program claims to the scope the frozen results license

2026-09-24. Corrections note for the P3 card (t_5308450a): *which N-program claims
overreach, and what scope do the frozen results actually license?* It addresses the eight
named points, each as (what overreaches) / (what the artifacts license) / (corrected
wording). No frozen artifact (runner, protocol, results dir, hash, ledger) is edited,
re-run, or re-hashed. Every number below is read from the frozen rows and the results
documents, not recomputed; the sources are listed at the end.

It supersedes nothing: it is a reconciliation note, applied downstream to
`S1_SYNTHESIS_v2.md`, `EVIDENCE_INDEX_v3.md`, `P1_MANUSCRIPT_DRAFT_v1.md`, and
`CONSCIOUSNESS_ROADMAP_v1.md`, and it carries forward (does not revoke) the N1 and A2
corrections. The valid positives and negatives are unchanged; these corrections narrow
overreaching *framing*.

---

## 1. AC109 licenses sufficiency of immediate diagnosis in its tested clean task — not the universal uselessness of history

**What overreaches.** "Persistent history FALSIFIED" / "storage is inert" / "the estimate
is a selector, not a memory", read without its qualifier, states that accumulated history
adds nothing in general. AC109 does not license that.

**What the artifacts license.** AC109 is **engineering-only** (seeds 0–7, 16 individuals,
48 cells; no protocol, no freeze, no finals). In the AC107/108 clean two-cause world,
where K4's perfect identifiability makes the discriminator a **pure function of the
current** `(bound, used_held, productive)` **triple** (disjoint action-observation
histories), a direct-diagnostic rival that reads the triple transiently matches the stored
estimate on 48/48 behavioural endpoints at lower cost (the stored estimate pays a 7-replica
write plus 72–141 redundant proactive renewals). This licenses exactly: **in the tested
clean task, immediate diagnosis suffices and storage is inert.** It says nothing about
worlds where the observation is partial, noisy, delayed, or ambiguous — the C2 occluded-gate
design demonstrates (by construction, before any run) that occluding `used_held` makes the
two causes produce an identical current observation while their histories differ, so
maintained history *is* load-bearing there.

**Corrected wording.** "In the AC107/108 clean task, where the discriminator is a pure
function of the current observation, the stored estimate adds nothing over a direct
diagnostic (storage inert, content load-bearing — engineering). Whether history earns its
keep in a partial/ambiguous-observation world is open (C2, design-level)." The sentence
"storage is inert" may never be detached from "in the clean task."

---

## 2. AC110 addresses repair's contribution in the tested decision window — not repair dependence in general, and not post-window storage protection

**What overreaches.** "Ongoing representation-repair dependence — FALSIFIED" (S1 item 5
header; EVIDENCE_INDEX table row "Ongoing repair dependence … FALSIFIED") states that repair
is not load-bearing, full stop. AC110 does not license that, and its own G4 is evidence in
the opposite direction for one specific period.

**What the artifacts license.** AC110 (frozen 6200–6207, 96 rows) distinguishes **three**
separate facts:

- **(a) In the decision window** (the 96 ticks the estimate is decision-relevant), repair is
  **not load-bearing for correctness/use**: cutting the estimate's only repair path leaves
  correctness (G2 16/16) and use (G3 16/16) unchanged, because correctness rides
  reacquisition (`bel_write` at open in-window contacts).
- **(b) Post-window, repair IS load-bearing for storage protection**: the maintained arm
  holds the estimate at 0 in 16/16 (action 2 restores the minority flips the ambient
  sticky-SET stream keeps introducing); the `no_repair` arm drifts to a majority read of 1
  in 8/16 (G4, the Binomial(7, ~0.55) coin flip). That is a measured case of repair
  *doing* load-bearing work — on storage, after the window.
- **(c) This says nothing about repair dependence elsewhere in the lineage**: AC67/71
  established that the program-bank repair is load-bearing under non-self-reversing (sticky)
  damage. AC110's falsification is specific to *the single-bit estimate in this world's
  decision window*.

**Corrected wording.** "Repair is not load-bearing for the estimate's correctness/use in
the decision window (correctness rides reacquisition); repair is load-bearing for the
estimate's post-window storage protection (G4: maintained 16/16 vs no_repair 8/16).
'Repair is not load-bearing' may never be stated without the window/storage qualifier, and
never generalized to 'repair dependence is falsified.'"

---

## 3. "Structurally unreachable" repair is conditional on ambient damage and the window — damage elsewhere in the program reaches it

**What overreaches.** "The repair path is structurally unreachable" (S1 item 5;
EVIDENCE_INDEX item 1 AC110 bullet), stated without its conditions, reads as an absolute:
the estimate can never be repaired by action 2.

**What the artifacts license.** The estimate's repair is unreachable *under the frozen
ambient 1e-4/replica/tick damage within the 96-tick window*, for two specific reasons:
(i) a single estimate bit contributes at most 3 minority replicas and can never trigger the
whole-bank obs-bit-2 trigger (≥4 minority over all 126 bank-0 bits) *on its own*; (ii) the
ambient program damage accumulates too slowly to reach that trigger within 96 ticks
(diagnostic: action 2 fires 0 times in the cut window, both arms). But it is **not**
structurally unreachable in general: damage **elsewhere in the program** that accumulates
≥4 minority over the 126 bits — an elevated rate, the AC111 corruption, or a longer window —
would fire action 2, and action 2 **also restores the estimate bit** (the estimate is part
of bank 0). That is exactly what G4 measures: over the remaining ~8000 ticks the ambient
stream does fire action 2, and the maintained arm holds the estimate at 0 in 16/16.

**Corrected wording.** "Under the frozen ambient damage rate within the 96-tick decision
window, the estimate's own damage can never trigger its repair (one bit contributes ≤3
minority replicas against a ≥4-over-126-bits trigger) and ambient damage is too slow — so
repair never fires in the window. This is conditional: damage elsewhere in the program at an
elevated rate triggers the whole-bank repair, which also restores the estimate bit (bank 0).
'Structurally unreachable' must be replaced by 'unreachable under ambient damage within the
window'."

---

## 4. AC111 demonstrates aspects of composition — while retaining its failed gates and the named behavioural interference

**What overreaches.** "Composition SUPPORTED" as a clean one-word verdict (S1 item 7 header;
EVIDENCE_INDEX item 1 and table row "Composition … SUPPORTED, named interference").

**What the artifacts license.** AC111 (frozen 6300–6307, 144 rows) demonstrates **aspects**
of composition: the two *direct* channels the protocol named are clean — reconstruction
never overwrites the estimate bit (the `bel_off` exclusion from `reg_from_active` is
load-bearing and verified under a live reconstruction), and the allowance-42 budget never
starves reacquisition (G1 48/48, G2 48/48, G4 16/16, G6 48/48 pass). But **two prespecified
gates fail and are retained, not moved**: G3 (cut: estimate discriminates + holds) 12/16 and
G5 (reacquisition untouched, `bel_writes == 7` in both arms) 12/16. The named residual is a
seed-dependent **behavioural interference** — the corrupted contact rule re-schedules
reacquisition, producing a never-biting cut on 6306 and a spurious-then-recovered
relinquishment on 6307, both survival-neutral and absent from engineering seeds (AC39
unfavourable).

**Corrected wording.** "The two direct composition channels are clean (reconstruction
overwrite absent, spending starvation absent). The full composition retains two failed gates
(G3/G5, 12/16) as a named seed-dependent behavioural interference. 'Composition' may be
described only as 'direct channels compose; full composition not established (two failed
gates retained).'"

---

## 5. Function-specific spending caps are a policy shape, not an absence of shared resource competition

**What overreaches.** "The allowance-42 budget never starves reacquisition" read as "the
decision write and the reconstruction do not compete for resources."

**What the artifacts license.** The allowance-42 budget is a **spending policy**: it is
defined to defer only `reg_from_active` (reconstruction), while `bel_write` (the
acquisition/update write) is gated by `_cap` (the W-catalyzed write cap), not by the
allowance. This is a property of the *policy's shape* — the allowance is a reservation on
the reconstruction's **own** spend, not a global material floor (AC104 rule 2: competing
writes — action-2 repair, W/C/B births, memory renewal, the streak write itself — still
consume material below the allowance). It does **not** mean the two functions do not compete:
both `bel_write` and `reg_from_active` draw on the same material, energy, and W-catalyst
pools, and the shared per-action cap `min(32, 8·W)` is a common ceiling. The function-
specific cap is the **resolution** of that shared competition, not its absence.

**Corrected wording.** "The allowance-42 policy never starves reacquisition (it defers only
reconstruction, and `bel_write` is W-gated not allowance-gated). This is a property of the
spending *policy*; the decision write and reconstruction still compete for the shared
material/energy/W pools, and the cap is what resolves that competition."

---

## 6. Acquisition-write dependence is not ongoing representation-repair dependence

**What overreaches.** "Causally coupled to its maintenance machinery in both directions" /
"maintenance → accuracy/use", read as an exercised ongoing-repair loop.

**What the artifacts license.** The maintenance that is load-bearing is the **paid
acquisition/update write** — `bel_write`, one atomic 7-replica flip at cause-onset — not an
ongoing repair loop. No repair loop that keeps an already-correct estimate correct against
continuing damage exists or runs in this world (N1 point 3; AC108 `no_write` removes exactly
that write; AC110 G4 is a post-window drift, not an in-window repair). "Direction 1:
maintenance is load-bearing" therefore means "the paid acquisition/update write is
load-bearing", and **sustained representation-repair coupling is NOT established**.

**Corrected wording.** "Causally coupled to its maintenance (the paid acquisition/update
write) in both directions", with the explicit note that ongoing representation-repair
dependence is unrun and unclaimed. The bare phrase "causally coupled to its maintenance
machinery" is acceptable only with this qualifier attached.

---

## 7. Supplied space alone is not a refutation of autopoiesis — the limitations are boundary, exchange interface, and controller realization

**What overreaches.** Any compressed "the space is supplied, therefore not autopoietic"
reading (and the earlier, already-corrected "retention is substitutable ⇒ unresolved"
reading).

**What the artifacts license.** Clause (ii) is not established because of **three concrete
modeling limitations**, none of which is "space is supplied" alone (A2 §4.2):

1. **The boundary is a pure retention wall, not a semipermeable exchange interface.** B
   retains the produced W/C inside the interior; nothing is exchanged *through* B — the
   exchange interface is absent from the boundary.
2. **The exchange interface is supplied, not boundary-mediated.** Material/fuel intake
   (`react` actions 0/1) and all energy accounting are fixed reactions, decoupled from
   boundary transport.
3. **The controller is non-spatial.** The program, description, route memory, pointer, and
   decision state live in fixed arrays (`traces`, `mem.Memory`) never positioned and never
   passed to transport; the produced spatial unity is a unity of the *constituent layer*,
   not of the whole organism.

"Supplied space" is the J1 substrate boundary (true of every component, including the
interpreter), and by itself it is not a *refutation* — it is one of three concrete
limitations that together scope clause (ii) to the constituent-retention level. The
substitution fact (rescue controls reproduce `keep` with zero boundary mass) is a
function-identification fact, struck from the verdict (A2 §4.1).

**Corrected wording.** "Clause (ii) is met only at the constituent-retention level, limited
by three modeling declarations — supplied space, supplied (non-boundary-mediated) exchange
interface, non-spatial controller — none of them an empirical gap." Never "the space is
supplied ⇒ not autopoietic" as a standalone refutation.

---

## 8. No "only remaining experiment" and no "track terminal" — a bounded disposition

**What overreaches.** "Authorize exactly one named continuation" / "the one live line"
(S1, EVIDENCE_INDEX) read as "the graded-posterior study is the only remaining experiment";
"the autonomy track is terminal" read as "the research is finished."

**What the artifacts license.** The graded-posterior study is **one** named continuation —
the one being authorized to start now — not the only open experiment. Other open
continuations on record, each equally legitimate: the AC110 scope note's longer-horizon or
second-cause world (which would make the post-window storage drift decision-relevant); the
I1 named interference (re-scheduled reacquisition) as a robustness question; the C3
"isolate ongoing repair after successful acquisition" in a world where the damage actually
flips replicas in-window; the reliability (second-order) tier (gated on the graded-posterior
result); and the roadmap's remaining tier. N1 point 7 already made this for three-cause
integration; it generalizes. "Autonomy track terminal" means only that the two autonomy
verdicts (production closure SUPPORTED bounded; full criterion NOT ESTABLISHED) are **stable
within the current model** — no experiment inside the model moves them, and moving them
requires changing the supplied physics (a re-architecture, not a run). It is not a claim
that the research is exhausted.

**Corrected wording.** "The autonomy verdicts are stable within the current model (moving
them requires a re-architecture, not a run). The cognition track has several open
continuations on record; one (the graded-posterior study) is authorized next." Never "the
only remaining experiment"; never "terminal" without "within the current model."

---

## What is NOT changed (retained positives and negatives)

- Discrimination at decision times: 0/32 mistakes on the untouched 6000–6007 family
  (AC107). Retained.
- Coupling, both directions, each isolated by single-flag intervention, with the paid
  acquisition/update write (not ongoing repair) as the load-bearing maintenance (AC108, N1).
  Retained.
- Storage maintenance in the content sense: observer-discard 16/16, no-cause identity 16/16
  (AC107). Retained.
- AC109's equivalence is real (48/48) *in the clean task*; AC110's window falsification is
  real (G2/G3); AC110's post-window storage dependence is real (G4); AC111's direct-channel
  cleanliness is real (G2/G4/G6) and its G3/G5 failures are real. All retained.
- Survival advantage did not transfer (seed-bounded); reliability tier blocked-by-success
  (K8), narrowed not universal (N1 point 6). Retained.
- A2 verdicts: production closure SUPPORTED bounded; full two-clause criterion NOT
  ESTABLISHED (three modeling limitations). Retained.

## Sources

`AC109_ENGINEERING_v1.md` (C1), `AC110_RESULTS_v1.md` (C3), `AC111_RESULTS_v1.md` (I1),
`AC107_RESULTS_v1.md`, `AC108_RESULTS_v1.md`, `N1_CORRECTIONS_v1.md`,
`A2_BOUNDARY_VERDICT_v1.md`, `C2_TASK_DESIGN_v1.md`, `C4_TASK_DESIGN_v1.md`,
`AC104_RESULTS_v1.md`, `S1_SYNTHESIS_v2.md`, `EVIDENCE_INDEX_v3.md`,
`P1_MANUSCRIPT_DRAFT_v1.md`, `CONSCIOUSNESS_ROADMAP_v1.md`. Frozen dirs: `ac107_results_v1`
(240 rows), `ac108_results_v1` (288 rows), `ac110_results_v1` (96 rows), `ac111_results_v1`
(144 rows). This note is derived and is not hashed into any study's `pre_run_snapshot.json`.
