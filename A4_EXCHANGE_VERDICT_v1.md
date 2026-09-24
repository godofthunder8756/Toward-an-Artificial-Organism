# A4 — The successor's bounded autopoiesis assessment

2026-09-24. Assessment deliverable for the A4 card (t_83513108): *against the
predeclared criterion, what does the successor (SR-2, `ac114.py`) establish about
exchange, boundary function, and composition?* It issues the bounded verdict. It
re-runs and re-hashes nothing; every code fact below is read from the frozen
sources and the frozen AC114 rows, and the AC114 audit is re-executed as the
verification step.

Vocabulary: `DEFINITIONS_CHARTER_v2.md` (the predeclared criterion: §7a components,
§7b maintained state, §8 C1–C5 + S1–S4, §9 J1/J4), `CLOSURE_VERDICT_v1.md` (K3),
`A2_BOUNDARY_VERDICT_v1.md`, `A1_EXCHANGE_SPEC_v1.md` (SR-2), `AC114_PROTOCOL_v1.md`
+ `AC114_RESULTS_v1.md` (the frozen confirmation). Predecessor: t_d753dfba (A3, the
frozen AC114 run).

---

## 0. The verdict, stated first

**Part (a) — production closure (M&V clause (i)): SUPPORTED, unchanged, and now
extended.** The K3/A2 production-closure verdict stands; the successor does not
disturb it. The diff is confined to the admission decision (`ac4.react` actions 0/1),
and G1 (keep == reference == rival byte-identical) proves nothing else changed.

**Part (b) — exchange and boundary function: NEWLY ESTABLISHED at the material
layer — the stronger result, not "boundary-dependent intake."** The successor does
not stop at SR-1's ceiling (intake tracks the *count* of live links). It establishes
**local exchange mediation and reciprocal production support**: intake is admitted at
the *local* live-state of a produced gate link, and the same produced links that
retain the constituents are the sites at which the resources that fund all production
are admitted. A2's limitation "the exchange interface is supplied, not
boundary-mediated" is resolved — for the material layer.

**Part (c) — the complete criterion (clauses (i)+(ii), full autopoiesis): STILL NOT
ESTABLISHED.** A2 named three limitations; the successor removes one (supplied
exchange) at the material layer. Two remain, unchanged, and neither is an empirical
gap: the **space/geometry is supplied**, and the **controller is non-spatial**. The
produced spatial unity is a unity of the **material (constituent) layer**; the
**whole organization's** unity is not established, because its informational core is
inside only by declaration.

Neither part implies consciousness; levels (c)/(d)/(e) are untouched. The strongest
wording licensed is unchanged from the charter's own ceiling, with the exchange role
added at the material layer.

---

## 1. What was previously supported, and why it is reused (not re-derived)

K3 (`CLOSURE_VERDICT_v1.md`) and A2 (`A2_BOUNDARY_VERDICT_v1.md` §0a/§2) establish,
under the accepted substrate convention (J1 resolved substrate):

- **Production closure (clause (i))** over the component set **{W, C, B, description,
  derived program}** (charter v2 §7a), each meeting C1–C5.
- **Maintained state** {pointer, coordination, route memory, decision state} meeting
  S1–S4 (§7b).
- **B's production closure** specifically (A2 §2): exists as `boundary[20]`,
  produced by action 8 (W-anchored, program-selected, 2 M + 2 E), ~10× turnover,
  on the W → B → W cycle.

**Reuse rationale (the constraint's explicit requirement).** The successor's entire
diff, read from `ac114.py`, is two source surgeries: (i) `ac4.react` actions 0/1 wrap
their intake in `if ADMIT(b,c)` (the `INTAKE_BLOCK → INTAKE_BLOCK_GATED` replacement),
and (ii) the puncture arms add `& ~PUNCTURE` to the action-8 candidate set. No birth
reaction, no succession step, no reconstruction, no maintained-state write, and no
conservation identity is touched; the `reference` arm calls the frozen `ac9.step`
object itself, and `ac4.balance` carries `in_m`/`in_f` as variables so gating them to 0
satisfies every identity by construction. The empirical seal is **G1**: `keep`,
`rival`, and `reference` are byte-identical (`state_hash`, `ledger`, `final_inventory`)
in 16/16 individuals. A change that leaves the ordinary-operation trajectory
byte-identical cannot have altered any other component's production or replacement path.

Therefore the C1–C5 evidence for **W, C, description, and program** is reused without
re-examination (their production edges — actions 6/7, succession, reconstruction — are
not in the diff), and the S1–S4 evidence for the maintained state is likewise reused.
The one component the successor *does* affect is **B**, and only by adding a causal role
to it, not by changing its production. B's C1–C5 evidence (§2 of A2) is re-confirmed
against `ac114.py` here: action 8 is untouched, so B still exists, turns over, is
W-anchored and program-selected, and sits on the W → B → W cycle. The new role is §2.

---

## 2. What is newly demonstrated: local exchange mediation (the stronger result)

The successor makes each contact channel's intake a function of the **local live-state
of a declared set of produced boundary links** (`GATE_LINKS = {0:(0,), 1:(1,)}`), rather
than of the aggregate count. On a productive contact of channel c: intake is credited
iff a gate link of c is live; if every gate link is a hole, the contact takes the frozen
failure branch (1 energy paid, no intake). A dead interface is therefore *strictly
costly*, which is what makes its renewal load-bearing.

Three discriminating predictions, all prespecified (A1 §6 D1/D2/D3) and all passing
16/16 on untouched seeds 6500–6507:

| Prediction | Meaning | Frozen result (AC114) |
| --- | --- | --- |
| **D1 — site vs count (decisive)** | puncture the gate link (0), leave 19 live: site gate zeroes channel-0 admission; count gate keeps it | G4: `puncture` `assay['in_f']==0` vs `rival_puncture` 320–480, paired 16/16 |
| **D2 — admission is local** | puncture a non-gate link (5): admission unchanged | G5: `puncture_non_gate` both channels admit, 16/16 |
| **D3 — semipermeability** | the *same* links retain and admit | `keep`: `particle_export==0` AND `in_f>0` AND `in_m>0`, 16/16 |

D1 is decisive because the aggregate rival cannot express "this link is the interface" —
no site enters its condition. On the identical puncture the two models disagree exactly
as SR-2 predicts, so the successor has **not** collapsed back into SR-1's count gate.
This is the empirical content of "the produced link at the crossing site is the thing
the exchange depends on" (A1 §9).

**The production boundary of this claim is precise and stated.** What the organism
produces is the **state** that makes the interface present or absent — the finite-lived
gate links, born by action 8, W-anchored, program-selected, turning over ~10× per run
(D5: `keep` B_birth 204–207). What remains **supplied** is the *reaction form* that
gates admission on that state (the gated `react` actions 0/1), the `GATE_LINKS`
association, and the yields. This is exactly the A1 §3.8 supplied/produced split: the
interface's presence is produced; the spatial distinction and the admission reaction are
substrate. No new component is introduced — the exchange interface is the boundary
component B itself, with its causal role extended from retention to retention +
exchange.

---

## 3. Evidence that the functions COMPOSE (reciprocal production support)

Composition is the claim that retention, exchange, and production ride one structure
and close a cycle at the material layer. The frozen evidence, per arm:

- **`keep` (D3 + D5 + production).** Zero export (retention intact) *and* full intake
  (exchange active) *and* B_birth 204–207, W_birth 188, C_birth 31, converted ≥ 613
  (production running) — in 16/16. The same produced links that retain the constituents
  are the sites at which the intake that funds production is admitted.
- **The gate-only twin (G3/T2).** `no_B_retention` (site gate) and
  `no_B_retention_ref` (no gate) are identical except the gate: both have zero B
  production, zero export, and gate links dead at t≈133. The site gate then zeroes
  post-onset admission (16/16) and the organism dies at t≈379–383 with fuel 0, energy 0;
  the twin keeps admitting (416–448 post-onset) and survives 16/16. Retention rescued
  does **not** restore exchange — the two roles are separable functions, and in `keep`
  they are coupled through the one produced structure.
- **The permeant mirror.** `permeant` (exchange present, retention broken) dies by
  export (11–93) in 16/16 — retention is needed independently.
- **Renewal (D5).** The gate links turn over like every other link and are continuously
  re-established by action 8, so the interface is *renewed*, not a one-shot endowment.

Assembled: **B is both product and condition of the production network.** Production
(action 8, W-anchored, program-selected) makes B; B sustains the interior through two
coupled roles — retaining W/C (outward barrier) and admitting intake (inward gate); and
the intake funds the W/C/B production that renews B. That is the material-layer closure
cycle **B → (retention + exchange) → production → B**, and it is established by ablation
(G3, `permeant`, `no_B`), not asserted.

**Bound of the composition claim.** It is established **at the material layer only**.
It does not extend to the informational core, which neither retains nor admits anything
spatially (§5).

---

## 4. Organizational functions still supplied externally

Unchanged from A2 §4.2 except for the exchange item, which this successor moves from
"supplied" to "boundary-mediated (material layer)":

1. **Space and geometry.** Lattice, interior/exterior, reflection rule, export bath,
   `crossing_link` — supplied substrate. The organism produces boundary *state*; it
   does not produce the spatial distinction (charter v2 §5; A2 §4.2 item 1). Producing
   the space is the infinite-regress point (J1 convention).
2. **The admission reaction form** — the gated `react` actions 0/1 — supplied. The
   organism conditions intake on the boundary state it produces; it does not rewrite
   the reaction (A1 §9). The exchange *function* is boundary-mediated, but its *law* is
   supplied.
3. **World constants and associations.** `GATE_LINKS`, `YIELD`, `B_MIN`, `PORTS`,
   reservoir caps, damage model, conservation laws — supplied.
4. **The non-spatial controller** — §5.

All four are declared substrate (charter v2 §5), not produced components. Nothing in
the successor claims otherwise.

---

## 5. The non-spatial controller and the informational-storage limitation

The informational core — the derived 126-bit program, the 130-bit description, the
route memory (`mem.Memory`), the generation pointer, and the decision state — lives in
fixed arrays (`traces`, `mem.Memory`) that are **never positioned and never passed to
`tr.move`**. The transport call (verified in `ac114.py`'s frozen `STEP_SRC`) is
`tr.move(b.pos, inactive, b.boundary, directions, impermeant_mask)` — positions,
inactivity, boundary, and the impermeability mask, and nothing else. The controller is
"inside" only by declaration, not by spatial realization.

The successor does nothing to change this. SR-2 realizes the exchange interface for the
**material layer** only (A1 §9, stated before engineering). The produced spatial unity —
the semipermeable perimeter — encloses the produced constituents W/C; it does **not**
enclose, position, or otherwise spatially realize the informational core. This is a
**modeling limitation** of the declared substrate (A2 §4.2 item 3), not an empirical gap,
and it is the second reason the complete criterion is not met.

---

## 6. Material-layer unity vs. whole-organization unity (the required distinction)

The successor sharpens this distinction rather than dissolving it:

- **Material (constituent) layer.** W, C, and B have positions on the lattice; B is a
  produced, finite-lived, decaying perimeter of 20 links; W/C cross the perimeter only
  where it is a hole, and export is irreversible. After SR-2, this layer constitutes
  itself as a **produced, semipermeable, self-renewing unity**: the produced perimeter
  retains the constituents (outward barrier) *and* admits the resources that fund
  production (inward gate), and is renewed by the production it enables. This is the
  material layer's spatial unity, and it is now established in the strong sense A2
  withheld.
- **Whole organization.** The whole organization is the material layer *plus* the
  informational core (program, description, route memory, pointer, decision state). That
  core is non-spatial (§5), and the space itself is supplied (§4 item 1). The
  organization as a whole therefore does **not** constitute itself as a concrete unity
  in space: the unity that is produced is a unity of the constituent layer, not of the
  whole organism (A2 §4.2 item 3, restated with the exchange role now added).

Clause (ii) — "constitute it as a concrete unity in space" — is therefore met **only at
the material layer**, and the complete two-clause criterion is **not** met for the whole
organization.

---

## 7. Exact scope of every statement above

- **Bounded to the declared model and operating range:** seeds 6500–6507 (8 independent
  units × 2 histories = 16 individuals; seeds are the replication unit, AC88), horizon
  2048 ticks, the SR-2 site gate with `GATE_LINKS={0:(0,),1:(1,)}`, `B_MIN=10`,
  `YIELD={0:32,1:64}`, `ONSET=512`.
- **Not** a universal or per-seed-family survival guarantee; survival is a bimodality-
  aware lower bound, reported as a SEPARATE outcome (7 arms 16/16, 4 arms 0/16).
- **Route holding is a lower bound, not a gate:** 3/16 `rival_puncture` and 3/16
  `puncture_non_gate` lose one or both routes while surviving; the puncture leaks
  (export 0–46). D1/D2 concern admission; the leak is a disclosed side effect.
- **`B_rescue`** (external B matter, `external_B=160`, zero internal births) is labelled
  EXTERNAL and never counted as autonomous production.
- **Content** (rule words, priority, `GATE_LINKS`) is inherited/supplied (charter v2 §6);
  content self-production is AC78-blocked and not required.
- **The verdict carries the substrate classification.** J1 (interpreter + succession
  mechanism as substrate) is resolved by the accepted convention (K3), not by measurement;
  a "supported" verdict is conditional on that classification (charter v2 §8, v1 §11).

---

## 8. What changes and what does not (disposition against the record)

- **Production closure (clause (i))** — status unchanged from K3/A2: SUPPORTED, under
  the substrate convention. The successor extends its *content* (the exchange interface
  is now a produced function of B) without disturbing its verdict.
- **The exchange limitation** — A2 §4.2 item 2 ("the exchange interface is supplied, not
  boundary-mediated") is **resolved at the material layer** by AC114. The boundary is no
  longer a pure retention wall; it is the produced site of intake.
- **The complete criterion (clauses (i)+(ii))** — still NOT ESTABLISHED, now for exactly
  two reasons: supplied space and the non-spatial controller. The substitution fact
  (A2 §4.1) remains struck from the reasoning; the rescue controls identify B's function,
  they do not refute it.
- **No frozen artifact is touched.** This document is derived. The AC114 audit re-passes
  (176 rows, 10 source hashes, G1/G3/G4/G5/G6 all green); nothing is re-run or re-hashed.
- **Unblocks S0.** The successor establishes the produced exchange interface at the
  material layer and reciprocal production support; it does not complete clause (ii) for
  the whole organization. That is the bounded verdict S0 must carry forward verbatim.

---

## Sources

`ac114.py` (diff: `make_react` intake gate, puncture candidate restriction, `reference`
= frozen `ac9.step`; `STEP_SRC` transport call), `DEFINITIONS_CHARTER_v2.md` (§5, §7a,
§7b, §8, §9 J1/J4), `CLOSURE_VERDICT_v1.md` (K3), `A2_BOUNDARY_VERDICT_v1.md`,
`A1_EXCHANGE_SPEC_v1.md` (SR-2, D1–D5, T1–T6, §3.8, §9), `AC114_PROTOCOL_v1.md`,
`AC114_RESULTS_v1.md`. Verification re-executed: `audit_ac114.py` (PASS — 176 rows,
10 source hashes valid, ledger identities, G1/G3/G4/G5/G6). Frozen rows:
`ac114_results_v1/rows.jsonl`.
