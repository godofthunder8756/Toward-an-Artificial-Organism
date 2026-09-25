# A0 — Preserve the autonomy trajectory: the corrected verdict and the finite spatial-successor requirement

2026-09-25. Assessment deliverable for the A0 card (t_29785c9c): *what is the corrected
autonomy verdict, and what finite causal relationship would a future spatial successor need
to demonstrate?* It re-runs and re-hashes nothing; it edits no frozen artifact. Every
outcome classification is read from the frozen AC115 rows and the M1 errata
(`AC115_ERRATA_v1.md`), which this document folds into the autonomy verdict at the clause
level. The finite-successor requirement (§4–§6) is a design direction — not built, not
blocked, not solved.

Vocabulary: `DEFINITIONS_CHARTER_v2.md` (§5 substrate, §7a components, §7b maintained
state, §8 C1–C5 + S1–S4, §9 J1/J4), `CLOSURE_VERDICT_v1.md` (K3),
`A2_BOUNDARY_VERDICT_v1.md`, `A4_EXCHANGE_VERDICT_v1.md`,
`I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md`, `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`,
`AC115_RESULTS_v1.md`, `AC115_ERRATA_v1.md` (M1). Predecessor: t_db58b389 (M1).

---

## 0. The corrected autonomy verdict, stated first

Three judgments, none standing in for another, each carrying M1's corrections:

**(a) Production closure (M&V clause (i), the finite criterion) — SUPPORTED, unchanged.**
Inherited by composition (AC115 G1 byte-identity), not re-derived. The K3 five-component
verdict over {W, C, B, description, program} and the S1–S4 verdict over {pointer,
coordination, route memory, decision state} carry forward intact. AC115 adds a role to B
(retention + exchange), not a component; it changes no production edge.

**(b) Composition of the six integrated functions — SUPPORTED at the mechanism level;
NOT CONFIRMED at the survival level.** The six functions are present and exercised in the
same organisms (keep arm, 16/16), with G1 (byte-identity), G2 (link-specific admission),
G3 (local admission), G8 (completeness) passing 16/16. The four survival-bundled gates
(G4–G7) FAIL on a minority of finals and are RETAINED as failed. M1 corrected *what*
failed, without moving any gate:

- **G4/G5 — FAIL 2/16 = 1/8 (seed 6602 only), category DEATH.** `no_B_retention_ref`
  dies t=347 (W=0 at t=127, C=0 at t=223) — an **early W/C collapse under B suppression
  in challenge-free arms**, NOT the AC68 long-horizon bimodality. Admission/retention
  discriminations hold in the failing individual.
- **G6 — FAIL 4/16 = 2/8 (6602, 6606), two categories.** **RETENTION** (6606: `keep`
  leaks 1 particle in *each* history, `particle_export == 1`, organism completes) +
  **DEATH** (6602: `B_rescue` dies t=347; external B cannot rescue the collapsed
  converter). Export is zero on **14/16 individuals = 7/8 seeds**, not 15/16.
- **G7 — FAIL 6/16 = 3/8 (6601, 6602, 6605), category DEATH only.** `rival_puncture_simult`
  dies t=15276 / 9589 / 16336 (48 ticks short) via the puncture W/C leak under `simult`.
  `description_correct_at_death == 130` in every failing individual — the end-of-run
  `desc` 129/80 are post-mortem (AC79). **No failure is a description-integrity failure.**

Net: three seeds (6601, 6602, 6605) die — 6 of 16 individuals, a survival miss; seed
6606 leaks a single particle in each history and survives; and **zero** failures are
description-integrity failures. The per-gate counts (2/16, 2/16, 4/16, 6/16) collapse onto
these four seeds because 6602 fails G4, G5, G6 and G7 (the same two histories) and 6606
fails G6 only. Every correction is toward *more precisely scoped* failure, never toward a
pass.

**(c) Whole-organism unity (M&V clause (ii)) — NOT ESTABLISHED.** The produced unity is a
unity of the material (constituent) layer — a produced, semipermeable, self-renewing
perimeter. The whole organization (material layer + informational core) does not
constitute itself as a concrete unity in space, because the informational core is
non-spatial (§3). This is the **sole** remaining genuine clause-(ii) limitation, and it
is a finite successor question, not a permanently untestable fact (§4–§6).

Neither part implies consciousness; levels (c)/(d)/(e) are untouched. The strongest
wording licensed is unchanged from the charter's ceiling, with the exchange role shown to
compose at the mechanism level.

---

## 1. What AC115 demonstrates (the increment, unchanged by M1)

The integrated successor (`ac115.py`, frozen finals 6600–6607, 208 rows, untouched seeds)
is the first run showing AC114's SR-2 link-specific admission gate composed with the AC105
five-mechanism closure in one organism. The six functions are present AND actually
exercised in the same individuals (keep arm, 16/16), each backed by its firing record:

| function | firing record (keep arm) |
| --- | --- |
| exchange admission | site gate active; G2/G3 discriminations hold through reconstruction + succession |
| retention | impermeant boundary; `particle_export == 0` on 14/16 (7/8 seeds; 6606 leaks 1 particle in each history) |
| boundary renewal / production | `B_births` 1674–1679 (≥10× the 20-link complement) |
| reconstruction | `fw` 8→0, recovery 8193–8202 |
| succession | 6 cycles, `desc` 130/130 |
| paid updates | `reg` 2327–2460 / `succ` 2671–2699 / `ctrl` 1672–1689 writes |

The composition claim that is licensed, at the mechanism level: **one organism renews its
produced exchange boundary while the admission gate is byte-inert at the intact boundary
(G1), admission is link-specific (G2) and local (G3), and the five internalization
mechanisms are preserved byte-for-byte (G1) and recorded exercised (keep arm).** This is
exactly I2's frozen ceiling — one step above AC114, one step below clause (ii).

---

## 2. What failed under intervention (corrected classification, M1)

The four gates that prespecified a survival/completion clause fail on a minority of
finals and are RETAINED (not moved, not re-shaped). The failures are **not** one
category:

| gate | result | failing seeds | category |
| --- | --- | --- | --- |
| G4 T2 boundary-supports-entry | FAIL 2/16 | 6602 | DEATH — early W/C collapse under B suppression (challenge-free), not a horizon effect |
| G5 retention-vs-admission | FAIL 2/16 | 6602 | DEATH — same t=347 completion miss |
| G6 endogenous-vs-external | FAIL 4/16 | 6606, 6602 | RETENTION (6606 leak, completes) + DEATH (6602) |
| G7 composition-under-stress | FAIL 6/16 | 6601, 6602, 6605 | DEATH only — description intact at death |

Three corrections from M1, carried verbatim:

1. **Export is 14/16 individuals (7/8 seeds), not 15/16.** Seed 6606 leaks 1 particle in
   *each* of its two histories (2 individuals, not 1), and completes. A single-particle
   leak at 16,384 ticks breaks an exact `export == 0` clause without touching anything
   else (inherited from AC105, G1 byte-identity holds).
2. **G7 is a death-only failure, not "death + description-integrity."**
   `description_correct_at_death == 130` in every failing individual; the end-of-run
   `desc` 129/80 are the sticky damage stream writing after death (AC79). The gate's
   `description_correct == 130` clause is read at end-of-run, so it is confounded by
   post-mortem degradation — a gate-design note, not a live-organism failure.
3. **The t=347 deaths are NOT a long-horizon effect.** Seed 6602's G4/G5/G6 deaths are an
   early W/C collapse under B suppression in challenge-free arms (W empty t=127, C empty
   t=223, death t=347 — the first ~2% of the horizon). Only G7's deaths (t=9589–16336)
   are the AC68 W/C bimodality re-entering through the long horizon under `simult`. Seed
   6603 shares 6602's priority `(2,0,1,3)` and survives, so the collapse is seed-specific
   trajectory, not priority-determined.

Mechanisms **exercised before failure** hold in all 16 individuals (reconstruction,
succession, paid updates, relinquishment, and the G2/G3/G4/G5 discriminations);
mechanisms **sustained to the horizon** do not. "Exercised" is not "sustained."

---

## 3. Which dependencies remain supplied (unchanged by AC115, and unchanged by any future successor)

The supplied substrate inventory — declared by the simulator and never produced by the
organism — with its clause-(ii) status:

**Permitted substrate (I1/J1; NOT counted against the verdict):**
- Lattice, interior/exterior distinction, `crossing_link`, export bath, reflection rule —
  supplied coordinates and geometry. Every formalization bottoms out in supplied laws
  (the infinite-regress point).
- Conservation laws (`ac4.balance`), damage model, tick clock, world constants, yields.
- The admission reaction form (gated `react` actions 0/1), `GATE_LINKS`, `B_MIN`.
- The interpretation machinery: `prog.choose` (14-bit rule interpreter), `advance()`
  (succession transition semantics), the decode format, the observation function. These
  are J1's substrate concession (K3 resolved J1 = substrate; `advance()` is the larger
  concession, `prog.choose` the smaller).

**Inherited/supplied content (charter §6):** rule words, priority permutation,
`GATE_LINKS` association. Content self-production is AC78-blocked and **not required**.

**The genuine clause-(ii) limitation:** the informational core is **non-spatial**. The
transport call is `tr.move(b.pos, inactive, b.boundary, directions, impermeant_mask)` —
positions, inactivity, boundary, directions, impermeability, and nothing else (verified
at ac9.py:78). The informational core — program `traces[0,:126]` (also the decision
register), description `traces[1,:130]`, generation pointer `traces[1,520:522]`,
coordination state `traces[1,522:540]`, route memory `mem.Memory` — lives in fixed arrays
that are **never positioned and never passed to `tr.move`**. It is "inside" only by
declaration. The produced semipermeable perimeter encloses the produced constituents W/C;
it does not enclose, position, or spatially realize the informational core.

---

## 4. What would make the informational core's realization part of the produced organizational domain

The clause-(ii) gap is **not** that the informational bits lack coordinates, and **not**
that they are never passed through transport. Assigning coordinates to `traces`, or
adding `traces` to the `tr.move` call, while leaving the read/write path host-mediated,
would change nothing: the host would still dereference the array directly, and the
organism's retention of the controller would still be a declared fact rather than an
earned one. Those are symptoms of a deeper property.

The property the successor must demonstrate is that the informational core's
**realization** is part of the produced-and-maintained causal network — that it is a
**produced, locally-accessed, vulnerably-retained, mutually-constrained component** of
the same organization, not a declared array. Concretely, four coupled sub-relations
together constitute the causal relationship (this is Montevil & Mossio's organizational
closure applied to the controller's substrate):

1. **Realization-by-production.** Each informational element (program bit, description
   bit, pointer, coordination, route-memory entry) is instantiated in finite-lived
   material substrate that the organism produces — it turns over (born/decays) like W/C/B
   — rather than persisting in a declared array.
2. **Local access.** Every read of an informational bit, and every paid write to it, is a
   position-mediated interaction with a produced component (a reader/writer catalyst);
   there is no host dereference. A bit at position p is readable only where/when a
   produced component is co-located, and the read fails if that component is removed.
3. **Retention-vulnerability.** The informational substrate decays and exports like the
   constituents, and its retention is paid for by the organism's own W-gated spending. Its
   continued presence is *earned*; a boundary puncture that leaks constituents also
   degrades it; there is no hidden pristine backup.
4. **Mutual constraint (causal closure).** The informational state constrains production
   (selects which births happen) *and* production maintains the informational state,
   through the same local machinery — so the informational realization and the material
   constituents lie on the same directed production cycle (the C5 network criterion,
   extended to include the informational substrate).

The negative test, stated so the successor cannot satisfy it trivially: **a realization
that the observer could still read or restore from a hidden host array fails (2) and
(3); a realization whose read/write is not performed by produced machinery fails (2);
a realization exempt from transport fails (3).** The current architecture fails all four
by construction (declared array, host dereference, transport-exempt, host-maintained).
A successor that only adds coordinates or passes arrays fails (2)–(4) and earns nothing.

---

## 5. The finite successor requirement (design direction, not built)

The successor must demonstrate the causal relationship of §4 for the informational core.
Stated as a requirement the successor's frozen study must establish, minimally:

- **R1 (realization).** The informational core's substrate is a produced component class
  (or an extension of W's role) with positions, finite lifetimes, and observed turnover —
  `C1`-existence and `C2`-production hold for it, exactly as for W/C/B.
- **R2 (local access).** Read and paid write of informational bits are position-mediated
  through produced machinery; no host dereference; a read fails where the local reader
  component is absent.
- **R3 (retention vulnerability).** The informational substrate is in the transport and
  damage streams; a puncture degrades it; its renewal is paid and W-gated.
- **R4 (mutual constraint).** The informational substrate lies on the production-dependency
  cycle with W/C/B (C5 extended): production maintains it and it constrains production,
  through the local coupling.

This is a **re-architecture of the supplied physics** (a new component class plus a
localized read/write reaction), not a run inside the frozen AC9 model. It is **finite**
(four checkable properties), it does **not** require eliminating supplied substrate
(geometry, laws, reaction forms, interpreter, initial content all stay supplied per §3),
and it is **not** the same as "full autopoiesis" — it would move clause (ii) for the
informational core from "declared" to "produced", one step, not declare the organism
alive.

---

## 6. Candidate tests (finite, prespecified — no full spatial rewrite)

Each test is a single-flag intervention on the successor's produced informational
substrate, following the established patterns (AC92 functional interruption; AC108
both-direction coupling; AC95/AC115 observer-discard; AC114 puncture ablation). Together
they operationalize §4 without building the full architecture:

- **T1 — localized read.** Ablate the produced reader component at a program bit's
  position. Assert: the bit is unreadable while the reader is absent (action selection
  differs from the intact arm), and readable again after the organism restores the reader
  endogenously (no content supplied). A hidden host array would be unaffected by removing
  a reader — this separates local realization from declared array.
- **T2 — retention vulnerability.** Puncture the boundary so the informational substrate
  exports/decays. Assert: informational state degrades alongside the constituents and is
  restored only by paid renewal. Contrast arm: an "informational core exempt from
  transport" control must NOT degrade — showing the effect is the spatial realization,
  not the damage model.
- **T3 — production dependency.** Block production of the informational-substrate
  component class, timed to interrupt while the function is underway (the AC92
  pattern, not a t=0 kill). Assert: the informational function (action selection /
  reconstruction) fails while the organism is alive and its content is intact at the
  interruption; a machinery-only restoration (EXTERNAL, no content supplied) resumes it.
- **T4 — mutual-constraint directionality.** Two directed cuts with distinct effects:
  (i) cut the informational→production read (remove/scramble the reader) — production
  ceases while the informational state itself survives; (ii) cut production→informational
  maintenance (block the producer of the informational substrate) — the informational
  state degrades while W/C/B production continues until the state is lost. Two separable
  effects is the signature of a constraint mutually maintained with the constituents,
  not a free-floating supplied controller (the AC108 both-direction pattern at the
  organizational layer).
- **T5 — no hidden backup (observer-discard).** The host discards its record of the bits
  and re-reads them only through the local machinery; the trajectory is byte-identical.
  There is exactly one copy of the informational state — the spatially realized one.

**Falsification (prespecified):** the successor is falsified if (i) a hidden host array
still reproduces the trajectory under T5, or (ii) removing the local reader leaves action
selection unchanged under T1, or (iii) an informational core exempt from transport
behaves identically to the spatially realized one under T2 — any of which means the
realization is still declared, not produced.

---

## 7. Scope and disposition

- **Bounded to the declared model and operating range.** AC115: seeds 6600–6607 (8
  independent units × 2 histories), 16,384 ticks, `GATE_LINKS={0:(0,),1:(1,)}`, yields
  64/64, `DECISION_ALLOWANCE=42`. The successor requirement (§5) is out of the frozen
  model's scope — it is a re-architecture, named and bounded, not executed here.
- **Not** autopoiesis unqualified, not "alive", not a universal or per-seed-family
  survival guarantee, no content self-production (AC78 blocked), no optimal-allocation
  claim. No frozen artifact, protocol, result, or hash is touched.
- **The successor requirement is a design direction** — open, not permanently blocked
  (the non-spatial core is finite and addressable), and not automatically solved
  (assigning coordinates or passing arrays through transport does not by itself satisfy
  §4/§5; the causal relationship R1–R4 must be demonstrated).
- **Unblocks S0.** S0 must carry forward: clause (i) SUPPORTED (five-component,
  inherited by composition); composition SUPPORTED at the mechanism level only (G4–G7
  retained as failed, classified per §2); clause (ii) NOT ESTABLISHED, limited solely by
  the non-spatial informational core — a finite successor question with a named causal
  requirement (§5) and candidate tests (§6), not a permanently untestable fact and not a
  run inside the frozen model.

---

## Sources

`DEFINITIONS_CHARTER_v2.md` (§5, §7a, §7b, §8, §9), `CLOSURE_VERDICT_v1.md` (K3),
`A2_BOUNDARY_VERDICT_v1.md`, `A4_EXCHANGE_VERDICT_v1.md`,
`I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md`, `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`,
`AC115_PROTOCOL_v1.md`, `AC115_RESULTS_v1.md`, `AC115_ERRATA_v1.md` (M1),
`ac115.py`, `ac9.py` (step transport call), `ac4_transport.py` (`move`).
Frozen results read, never re-run or re-hashed: `ac115_results_v1/` (208 rows). This
document is derived and is not hashed into any study's `pre_run_snapshot.json`.
