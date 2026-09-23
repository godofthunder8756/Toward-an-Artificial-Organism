# A2 — Boundary verdict: causal role, spatial unity, and the two closure verdicts

2026-09-23. Assessment deliverable for the A2 card (t_3d75b49d). It answers one
question: *what is the produced boundary's ordinary causal role in constituting and
sustaining the organization, and what does the model establish about spatial unity?*

It is a definitional/code-trace document. No study is re-run and no frozen row, hash,
or ledger is touched. Every claim below is read from the frozen sources at HEAD 77ace95
(`ac4.py`, `ac4_transport.py`, `ac9.py`, `ac10.py`) and the frozen results
(`AC4_RESULTS_v1.md`, `AC4_TRANSPORT_RESULTS_v1.md`, `AC10_RESULTS_v1.md`), with the
geometry re-derived at runtime (`_a2_verify_boundary.py`). Vocabulary is charter v2
(§5 substrate, §7a components, §8 criterion, §9 J4) plus the K3 verdict
(`CLOSURE_VERDICT_v1.md`). Predecessor: `A1_REALIZATION_LEDGER_v1.md`.

---

## 0. The two verdicts, stated first (they are separate, and neither stands in for the other)

**(a) Production closure — SUPPORTED** (unchanged from K3). The boundary component B
satisfies C1–C5 within the declared model and operating range: it exists as concrete
damageable state, it is produced and replaced (turns over), its production depends on
other components, its content boundary is the permitted inherited endowment, and it lies
on a production cycle (W → B → W). This verdict is not re-litigated here; §2 restates
the code evidence it stands on.

**(b) The complete adopted autopoiesis criterion (production closure *and* spatial
unity, M&V clauses (i)+(ii)) — NOT ESTABLISHED.** Clause (ii) — "constitute the system
as a concrete unity in space" — is met only in a bounded, constituent-level sense
(produced spatial retention, §1), and is limited by three modeling declarations, not by
any empirical gap (§4). The full two-clause criterion is therefore not met, and this
document does **not** present the narrower production-closure result as completion of
the full goal. The two verdicts are issued separately and the boundary requirement is
not excluded, not assumed, and not declared satisfied.

The reason (b) is not established is **not** the one the record has been citing. §4
corrects that.

---

## 1. The boundary's ordinary causal role: retention of the produced constituents

The boundary's role is **retention** — it keeps the produced W and C constituents inside
the enclosure so they can keep catalysing writes and converting fuel — and this role is
**identified, not refuted, by the external-substitution controls**.

Code facts (verified at runtime, `_a2_verify_boundary.py`):

- The organism's functional constituents W and C have positions (`b.pos`, 20 particles on
  an integer lattice). The interior is the 5×5 square `|pos| ≤ 2`; the exterior is
  `|pos| > 2`; a particle whose position reaches `|pos| ≥ 6` is exported to an absorbing
  bath and can never act again.
- The boundary is 20 discrete perimeter **links** (edges), one per interior↔exterior
  crossing of the square's perimeter (5 per side; the 4 corner cells each serve two links,
  so 20 edges over 16 unique coordinates). Each link carries a lifetime in `b.boundary[20]`.
- `ac4_transport.move` blocks a crossing proposal when the particle is impermeant **and**
  the link's lifetime is positive (`links[edge] > 0`). An expired link (lifetime 0) is a
  hole. In the integrated organism every functional constituent is impermeant
  (`ac9.step` calls `tr.move(..., np.ones(20, dtype=bool), ...)`), so the boundary is a
  pure retention barrier over W and C.
- Export is lethal to the exported particle: `lost = inactive & ~old;
  b.life[lost] = 0` (`ac9.step`, `ac4.step`), so a W/C that leaves the enclosure dies.
- The boundary decays: `b.boundary[b.boundary > 0] -= 1` each tick, so every link is
  finite-lived and must be re-produced.

The causal role, stated without the substitution fallacy:

> The boundary's function is to retain W and C in the interior. It is load-bearing:
> cut boundary production and W/C diffuse out, export, and die, and the acquired
> organization collapses (AC10 `no_B`: export 8/8, routes lost 195–279, death 8/8 at
> 472–1153; AC4 no-B: activity −79.3/−80.9 points, 25–109 W/C exported, all terminate).

The **rescue controls identify the function**, they do not refute it. `no_B_retention`
(forced reflection by the kernel flag while boundary matter is exactly zero) is
indistinguishable from `keep` (8/8 complete, both routes, zero export), and `B_rescue`
(external B matter, zero internal births) likewise retains 8/8. Together these show that
what the acquired organization depends on is the *retention function*, not the boundary's
*mass* — and the organism's own means of realizing that function in the frozen world is
its produced boundary B. A rescue control that substitutes boundary supply does not show
the boundary "does nothing"; it shows precisely what the boundary does. §4 uses this
correction to remove the substitution fact from the spatial-unity verdict.

---

## 2. Production closure for B (verdict (a)) — the code evidence, restated

B is the third produced constituent (charter v2 §7a C3), and it meets every production
clause:

| Clause | Requirement | B's evidence (code + frozen rows) |
| --- | --- | --- |
| **C1 existence** | concrete, damageable, finite state | `b.boundary[20]`, 20 lifetimes, decayed every tick, constrained by the `ac4.balance` identity `(b.boundary>0).sum() == B + B_birth + external_B − B_expiry − B_discard` |
| **C2 production/replacement** | turns over during ordinary operation | action 8 (2 M + 2 E, at most one per action) sets an expired link to 256; AC4 self conditions produce 205–209 B over 2048 ticks against a 20-link complement, i.e. ~10× turnover; AC10 `no_B` produces 0 |
| **C3 within-network dependence** | production depends on another component | action 8 requires a live interior W within Manhattan distance 1 of the link's interior endpoint (`near = (|ENDPOINTS − wp|.sum(axis=2) <= 1)`), plus a program choice of action 8 — edges W → B and C9 → B |
| **C4 content boundary** | initial content may be supplied | the initial 20 lifetimes (`arange(128,248,6)`) are the inherited B endowment, permitted, then replaced endogenously |
| **C5 on a cycle** | production transitively enabled by itself | W → B (W anchors B-birth) and B → W (retention preserves W): B sits on the W → B → W cycle; it also preserves C (B → C) |

This is exactly the K3 verdict's B row (`CLOSURE_VERDICT_v1.md` §1), re-confirmed against
the code here. **Verdict (a) is SUPPORTED and unchanged.** No re-examination of the other
four components (W, C, description, program) is performed; the A2 boundary question does
not disturb their C1–C5 evidence.

---

## 3. Operational meaning of "spatial unity" in this model

"Spatial unity" can only mean what the model's spatial layer can express. That layer is
narrow, and naming it precisely is the point:

1. **A bounded interior.** The 5×5 square `|pos| ≤ 2`, distinct from the exterior and
   from the absorbing export bath at `|pos| ≥ 6`. This distinction is **supplied**
   (`tr.inside`, `tr.move`, `crossing_link` are substrate, charter §5).
2. **A produced, finite-lived perimeter.** 20 links, each present iff its lifetime is
   positive, each produced by action 8 and each decaying. This state is **produced** by
   the organism.
3. **Selective reflection.** Whether a crossing proposal is reflected depends on the
   particle's impermeability and the link's lifetime. In the integrated organism all
   functional constituents are impermeant, so the boundary is a *retention* barrier, not
   a species-selective membrane (the transport prerequisite AC4 tested selectivity on
   tracers; the integrated AC9/AC10 organism collapsed the mask to `ones(20)`).
4. **Irreversible export.** A particle that crosses the whole exterior is absorbed and
   dies. The enclosure is therefore the difference between "inside and functioning" and
   "outside and gone."

So, operationally, "the system constitutes itself as a concrete unity in space" means:
**the organism produces a finite-lived perimeter that retains its functional
constituents inside a bounded interior, distinguishing inside from outside by its own
paid production.** That much the model establishes (§1). What it does **not** establish —
and cannot, without changing the supplied physics — is in §4.

---

## 4. Verdict (b): the complete criterion, and the correction of the record

### 4.1 The correction (removes the substitution fact from the spatial-unity verdict)

The record — charter v2 §9 J4, `CLOSURE_VERDICT_v1.md` §2, and the closure-criterion
reference — treats the *substitution* of retention by substrate (kernel flag / external B
matter reproduce `keep` with zero internal boundary) as the reason clause (ii) is
"unresolved". **That is a category error.** A rescue control that substitutes boundary
supply *identifies the function* (retention, §1); it does not show that the organism fails
to constitute itself as a unity in space. In the frozen world the organism **does** produce
B and B **does** retain the interior; the availability of a substrate substitute in a
*different* arm of the experiment says nothing about what the organism does in `keep`.
The substitution fact is therefore **struck from the spatial-unity verdict** — it bears on
the *function* of B, which §1 already accounted for, and on nothing else.

### 4.2 The genuine limitation (why (b) is not established)

Clause (ii) is limited by three modeling declarations, each of which is a property of the
declared substrate, not an empirical gap:

1. **The space is supplied.** The 5×5 geometry, the lattice, the interior/exterior
   distinction, the reflection rule, and the absorbing bath are substrate laws the
   organism does not produce. The organism produces boundary **state** (link lifetimes);
   it does not produce the spatial distinction itself. This is the same substrate
   boundary drawn everywhere else (the J1 convention), and it is as true of B as it is of
   the interpreter — but it means "constitutes itself in space" is true only of the
   *state*, not of the *space*.
2. **The exchange interface is supplied, not boundary-mediated.** Material and fuel intake
   (`react` actions 0 and 1: `in_m`/`in_f` with overflow) and all energy accounting are
   fixed reactions, decoupled from the boundary's transport. The boundary retains W/C; it
   does **not** mediate the organism's material exchange with its environment. A boundary
   that is a pure retention wall is a real boundary, but it is not the *semipermeable
   exchange interface* a biological membrane is — and in this model nothing is exchanged
   *through* B.
3. **The controller is non-spatial.** The program, description, route memory, pointer,
   and decision state live in fixed arrays (`traces`, `mem.Memory`) that are never
   positioned and never passed to `tr.move` (verified: the move call's arguments are
   `b.pos, inactive, b.boundary, directions, …` only). The boundary encloses the produced
   constituents (W/C), but the organism's informational core is "inside" only by
   declaration, not by spatial realization. The spatial unity that is produced is a unity
   of the *constituent layer*, not of the whole organism.

### 4.3 What is established vs. not, stated plainly

- **Established:** the organism produces, maintains, and turns over a finite-lived
  perimeter that spatially retains its produced constituents inside a bounded interior,
  and this retention is load-bearing for the acquired organization and on the production
  cycle (W → B → W).
- **Not established:** that the organism constitutes *itself* as a concrete unity in space
  in the fuller sense — the space, the exchange interface, and the controller's spatial
  situation are all supplied. Clause (ii) is met at the constituent level only.

**Verdict (b): NOT ESTABLISHED.** The complete two-clause criterion is not met, and the
residual is a modeling limitation (supplied space + supplied exchange + non-spatial
controller), not an unresolved empirical question and not the substitution fact.

---

## 5. Evidence inventory (what existing evidence establishes, per the five named items)

| Item | What the model establishes | Named evidence (frozen) |
| --- | --- | --- |
| **Localization** | B occupies explicit perimeter links; production requires interior W within Manhattan distance 1 of the link; W/C have positions, daughters born at parents' positions; interior `|pos|≤2`, export `|pos|≥6` | `ac4.py` action 8, `ac4_transport.move`; AC4 "boundary production cost and spatial accessibility" mechanism test |
| **Retention** | the enclosure retains impermeant particles; one hole leaks substantially; retention is load-bearing and separable from matter | AC4 transport (intact 100% vs one-hole 35.4% vs open 0%); AC10 `no_B` / `no_B_retention` / `B_rescue` (§1) |
| **Transport** | explicit lattice transport: unbiased cardinal steps, reflection at live links, return from exterior, irreversible export, per-tick inventory balance | AC4 transport prerequisite (96 rows, 6 arms, `n_in+n_out+n_export==512` invariant) |
| **Boundary production** | B is paid (2 M + 2 E), W-anchored, finite-lived (256), and turns over ~10×/run | AC4 self: 205–209 B births, 252–256 W, 31 C, zero export, 100% accuracy; AC10 `no_B`: 0 births |
| **Reciprocal dependence** | B is both product and condition of the interior: W anchors B-birth; B retains W and C; the program (C9) selects action 8 | AC10 `no_B` exports 8/8 and dies 8/8; `no_W` dies before any entry is ever allocated; AC4 no-B terminates all |

The boundary is **both product and condition of the enclosed organization**: it is made
by the interior (W-anchored, program-selected) and it sustains the interior (retains W/C).
That mutual dependence is what places B on the closure cycle — and it is established by
ablation, not asserted.

---

## 6. The one finite discriminating question, and why no child experiment is created

The A2 instruction: if evidence is insufficient, identify **one** finite discriminating
question, and create a child experiment only if it can change the verdict, else record the
precise modeling limitation.

The single question that would move verdict (b) is:

> Does the organism's boundary **mediate** the organism–environment exchange
> (semipermeability), or is it a pure retention wall with exchange supplied separately?

This is a *modeling* question, not a *measurement* question. Answering it "yes" would
require the boundary to be the site of material/energy intake and outflow — which means
changing the supplied `react` actions 0/1 and the transport law to route exchange through
B. That is a new architecture (a changed supplied physics), not an experiment inside the
frozen model. The same holds for the other two limitations: producing the space itself is
the infinite-regress substrate point (already settled by the J1 convention), and making
the controller spatial is a re-architecture, not a run.

Therefore: **no child experiment is created.** The verdict is a modeling limitation and is
recorded as such. This is the honest stopping point, not a deferral: within this model the
boundary requirement can only ever be met at the constituent-retention level, and that is
exactly what the evidence shows.

---

## 7. Consequence for the downstream tasks (I1, P1, S1) and the charter

- **Production closure (a) stands**, and its wording is unchanged: "meets the finite
  closure criterion within the declared model and operating range, under the accepted
  substrate convention."
- **The complete criterion (b) is NOT met**, and the reason is now correctly stated as a
  three-part modeling limitation (supplied space, supplied exchange, non-spatial
  controller), with the substitution fact removed from the reasoning. The full autopoiesis
  goal is **not** declared complete; the boundary requirement is neither excluded nor
  presented as satisfied.
- **Charter amendment (definitional, matching A1's):** charter v2 §9 J4 should drop the
  "substitution ⇒ unresolved" clause and instead record that clause (ii) is limited by the
  three supplied items in §4.2, with the substitution fact reclassified as a function-
  identification fact (§1). This is the same kind of explicitness amendment A1 handed to
  the charter's §5 (name the storage arrays); here it is §9's J4 wording.
- **Downstream:** I1, P1, S1 may cite verdict (a) with its exact scope; none may cite the
  full two-clause criterion as satisfied, and none may cite "spatial unity unresolved
  because substitutable" — that phrase is now wrong.

---

## Sources

`ac4.py` (Body.boundary, action 8, `balance`, `step`), `ac4_transport.py` (`inside`,
`crossing_link`, `move`, export), `ac9.py` (`Organism`, `step` transport call), `ac10.py`
(surgery sites for `no_B`/`permeant`/`no_B_retention`/`B_rescue`), `DEFINITIONS_CHARTER_v2.md`
(§5, §7a, §8, §9), `CLOSURE_VERDICT_v1.md`, `CLOSURE_CRITERION_CONSISTENCY_v1.md` §4,
`AC4_RESULTS_v1.md`, `AC4_TRANSPORT_RESULTS_v1.md`, `AC4_PROTOCOL_v1.md`,
`AC4_TRANSPORT_PROTOCOL_v1.md`, `AC10_RESULTS_v1.md`, `AC10_PROTOCOL_v1.md`,
`A1_REALIZATION_LEDGER_v1.md`. Runtime verification: `_a2_verify_boundary.py`.
