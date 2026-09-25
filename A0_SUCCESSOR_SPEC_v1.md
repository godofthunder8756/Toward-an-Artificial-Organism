# A0 — The remaining full-autopoiesis gap: the one finite successor requirement

2026-09-24. Successor-design assessment deliverable for the A0 card (t_89213031). It
answers one question: *what is the concrete, minimally scoped successor requirement for a
stronger unity-and-boundary claim — not another repair study?*

It is a definitional/design document. No study is run, no frozen row, hash, or ledger is
touched, and no successor architecture is built. Every code fact is read from the frozen
sources at HEAD e3fae26 (`ac4.py`, `ac4_transport.py`, `ac9.py`) and re-checked at runtime.
Vocabulary is charter v2 (§5 substrate, §7a components, §8 criterion), the K3 verdict
(`CLOSURE_VERDICT_v1.md`), and the A2 verdict (`A2_BOUNDARY_VERDICT_v1.md`). Predecessors:
P0 (`EVIDENCE_INDEX_v3.md`), A1 (`A1_REALIZATION_LEDGER_v1.md`), A2.

---

## 0. The answer, stated first

**The present evidence licenses only the narrower claim** — production closure (M&V clause
(i)) plus a produced boundary whose constitutive role is *retention* of the produced
constituents. **There is exactly one finite, minimally scoped successor requirement** that
would license a stronger (but still bounded) unity-and-boundary claim: make the produced
boundary **the site of the organism–environment exchange**, so that the same paid structure
both retains constituents and mediates what crosses it. That is the only one of A2's three
limitations that is a *successor question* rather than a *permanent substrate fact*. The
remaining clause-(ii) limit is the **non-spatial controller** — a separate full
re-architecture that this card does not build. (I1 correction: "supplied space" is
**permitted substrate**, not a limitation — every formalization bottoms out in supplied
laws; it is struck from the limitation list.)

This document therefore delivers a **concrete, minimally scoped successor specification with
causal tests** (§5–§6), and states precisely what it would and would not establish (§7) and
what stays fixed substrate and why (§8). It is not a repair study: no new repair or
maintenance mechanism is introduced. It is not a full spatial architecture: no position,
particle, or contact site is added, and the controller is not spatialized.

---

## 1. The gap is three limitations, and only one is a successor question

The complete adopted criterion (Maturana & Varela 1980, quoted in charter v1 §2) has two
clauses: (i) production closure — the network regenerates the components that realize it;
and (ii) spatial unity — the components "constitute it as a concrete unity in space… by
specifying the topological domain of its realization as such a network." K3 established
clause (i) under the substrate convention. A2 established that clause (ii) is met only at
the *constituent-retention* level, limited by three modeling declarations. They are not
equal, and the assessment turns on keeping them apart:

| Limitation | What is supplied | Finite successor question? | Why |
| --- | --- | --- | --- |
| **Exchange interface** | `react` actions 0/1 credit fixed intake, decoupled from B | **YES — this is the one finite successor** | A change to the *dependence* of a supplied reaction, expressible inside the frozen conservation identities; not an infinite regress |
| **Space / geometry** | 5×5 lattice, interior/exterior, reflection rule, export bath | **NO — permanent substrate** | Producing the space regresses: a produced space needs a space to be produced in (J1 / `CLOSURE_BOUNDARY_v2`) |
| **Non-spatial controller** | `traces` / `mem.Memory` never passed to `tr.move`; informational core "inside" by declaration | **NO — out of scope here** | Spatializing it is a full re-architecture (A2 §6); this card's remit forbids building it |

The one genuinely open item is the exchange interface. Everything else in this document
serves to say *why* that is so, and to set the ceiling on what fixing it would achieve.

---

## 2. Production closure already supported (not re-litigated)

Per K3 (`CLOSURE_VERDICT_v1.md`), under the accepted substrate convention: every level-(a)
component **{W, C, B, description, derived program}** meets C1–C5, the maintained state
**{pointer, coordination, route memory, decision state}** meets S1–S4, and the
production-dependency network is a single strongly-connected component with no external root.
J1 is resolved as substrate (interpretation and succession semantics retained). This card
does not disturb that verdict; it concerns clause (ii) alone.

---

## 3. The produced boundary's constitutive role (evidence, already frozen)

The boundary's established causal role is **retention**, and it is identified — not refuted —
by the substitution controls (A2 §1):

- B is 20 finite-lived perimeter links (`b.boundary[20]`), each produced by action 8
  (2 M + 2 E, W-anchored) and decayed every tick.
- In the integrated organism every functional constituent is impermeant
  (`ac9.step` line 78 passes `np.ones(20, dtype=bool)`), so `tr.move` blocks any
  interior↔exterior crossing at a live link and `|pos| ≥ 6` is irreversible export.
- Cut B and W/C diffuse out, export, and die (AC10 `no_B`); rescue retention alone
  (`no_B_retention`, kernel reflection with zero boundary matter) or supply B externally
  (`B_rescue`) and the organism survives 8/8. So what the organization depends on is the
  *retention function*, and the organism's own means of realizing it is produced B.

This is the entire constitutive role the present evidence establishes. It is real, it is
load-bearing, and it is narrower than clause (ii) — because retention is only half of what a
biological membrane does.

---

## 4. What is supplied, precisely (the two remaining items)

### 4.1 The exchange interface is a fixed reaction, decoupled from B

`ac4.react` actions 0 and 1 are fixed yields with no boundary term:

```python
if action==0:
    e['in_f']=32; e['overflow_f']=max(0,b.fuel+32-64); b.fuel=min(64,b.fuel+32)
elif action==1:
    e['in_m']=64; e['overflow_m']=max(0,b.material+64-256); b.material=min(256,b.material+64)
```

The contact path (`ac9.step` lines 85–89) reads a port from route memory or a coin, and on a
match calls `react` for the fixed yield. Nothing about `b.boundary` enters the intake
calculation: **nothing is exchanged *through* B.** B is a pure retention wall. A boundary
that retains but does not mediate is a real boundary, but it is not the *semipermeable
exchange interface* a biological membrane is — and that is precisely the clause-(ii) gap.

### 4.2 The controller is non-spatial

The program, description, pointer, coordination state, route memory, and decision state live
in fixed arrays (`traces[0]`, `traces[1]`, `mem.Memory`) that are never positioned and never
passed to `tr.move` — the move call's arguments are `b.pos, inactive, b.boundary, directions,
impermeant` only. The boundary encloses the produced constituents (W/C); the informational
core is "inside" only by declaration. The spatial unity that is produced is a unity of the
*constituent layer*, not of the whole organism.

---

## 5. The minimal successor requirement (specification, not a build)

**SR-1 — make the produced boundary the site of exchange.** Re-specify the supplied exchange
reaction so that the intake credited by contact actions 0/1 is *conditioned on the produced
boundary's state* rather than on a fixed constant. The minimal form is an aggregate integrity
gate:

> `react` actions 0/1 credit `in_f` / `in_m` only while the produced boundary is sufficiently
> intact (e.g. `(b.boundary > 0).sum() >= B_MIN`); otherwise the contact yields nothing
> (intake 0, the failure branch already in the code).

Three properties make this minimal, and each is a constraint on the build, not a free choice:

1. **It is a change to a supplied reaction's dependence, not a new mechanism.** No repair
   process, no new component, no new state item is introduced. B's causal role is *extended*
   (retention → retention + exchange-gating), not augmented by machinery.
2. **It is expressible inside the frozen conservation identities.** `ac4.balance` asserts
   `b.material == M + e['in_m'] − e['overflow_m'] − e['spent_m']` and the same for fuel
   (lines 125–126). Because intake is carried as a *variable*, gating `in_m`/`in_f` down to
   0 satisfies the identity **by construction** — exactly the AC15 lesson's point 1. No law
   patching, no free external matter.
3. **The gate is non-spatial.** No position, particle, or contact site is added; the
   existing port-match contact is unchanged. Only the *yield's* dependence changes. This is
   what keeps it out of "build an entire spatial successor architecture." (A per-channel or
   per-link refinement — associating each contact channel with a declared subset of links —
   would be closer to true semipermeability, but it is **not required** to establish the
   causal separation in §6 and is deliberately left out of the minimal scope.)

The gate constant and the `B_MIN` threshold are supplied world constants (charter §5), of a
piece with `PORTS`, `YIELD`, and the channel→port `mapping` argument that already exists.
They are not content the organism invents.

---

## 6. Causal tests (prespecified; gates to be written in the successor's protocol)

**T1 — retention (continuity, reproduce the frozen result).** `no_B` still exports 8/8 and
dies 8/8. This pins that SR-1 did not disturb the frozen retention function; a run that does
not reproduce AC10's `no_B` row field-for-field (`state_hash` included, at the unchanged
schedule) is invalid.

**T2 — exchange-mediation (the decisive new test).** With SR-1 active, `no_B_retention`
(retention rescued by the kernel reflection flag, boundary matter exactly zero) **still dies
— by income starvation** (material/fuel reservoirs depleted at death, not full), because the
boundary gate admits no intake when boundary matter is zero. If B were only a retention wall,
rescuing retention would rescue the organism; under SR-1 it does not. This is what separates
the two roles causally: **exchange is a B-dependent function, distinct from retention.**

**T3 — unity (the claim the successor earns).** The produced boundary's state is the sole
causal antecedent of *both* retention and exchange; there is no free supply. Control:
`B_rescue` (external B matter, zero internal births) restores *both* functions — confirming
it is the boundary *state* that carries both roles, and labeling the substitute EXTERNAL, not
autonomous. The inside/outside distinction is now realized by a single paid structure for
retention and exchange jointly.

**T4 — inertness (the gate is the only change).** SR-1 with the gate disabled (always-full
yield) must be byte-identical to the frozen world (`state_hash` equality), so the gating is
the only difference between the successor and the reference.

Discipline inherited from the project's own checklist: engineering seeds first, then the
protocol, then disjoint final seeds; report planned-denominator activity and survival as a
bimodality-aware lower bound (AC68); the gate shapes are prespecified, and a predeclared gate
that fails is recorded, not moved (AC16).

---

## 7. The precise ceiling: what SR-1 would establish, and what it would not

If SR-1 passes T1–T4, the licensed wording upgrades by exactly one step:

- **Before:** "the organism produces a finite-lived perimeter that retains its produced
  constituents inside a bounded interior" (A2, constituent-retention level).
- **After:** "the organism produces a finite-lived boundary that specifies the topological
  domain of its realization for the material layer — it retains constituents *and* mediates
  the organism–environment exchange, the intake that funds all production."

That is a genuine strengthening of clause (ii): more of the network (the income source, not
just the constituent pool) is realized through the produced boundary. It is **not** full
clause (ii), and must not be worded as such: the space remains supplied, and the
informational core remains non-spatial (inside by declaration). It is not "alive", not
"autopoietic" unqualified, not a completion of the full two-clause definition. The
non-spatial controller is the honest, named residual that SR-1 deliberately does not touch.

---

## 8. What remains fixed substrate, and why (the explicit non-demands)

The following stay supplied in *any* successor, and this card does not demand their
production:

- **Space / geometry** (lattice, interior/exterior, reflection, export bath) — permanent
  substrate. Producing the space is an infinite regress; this is the J1 / `CLOSURE_BOUNDARY_v2`
  argument, and it is as true of B as of the interpreter.
- **The controller's spatial situation** — out of scope here. Spatializing `traces` /
  `mem.Memory` is a separate, larger architecture; the task's own constraint forbids building
  it, and clause (ii) after SR-1 remains explicitly scoped to the material layer.
- **The exchange reaction's form, once gated** — supplied. The organism *conditions* intake
  through the boundary state it produces; it does not rewrite the reaction. Self-rewriting
  physical laws are not demanded (infinite regress).
- **Content** — the rule words, priority permutation, and the gate's channel association are
  inherited/supplied (charter §6). Lifetime invention of inherited content is not demanded
  (content self-production is AC78-blocked and not required).
- **Interpreter, succession semantics, decode format, write primitive, conservation laws,
  damage model, world constants** — substrate (charter §5).

The single load-bearing requirement the successor adds is causal, not inventive: **the
produced boundary must be the thing the exchange depends on.**

---

## 9. Falsification and stopping

SR-1 is falsifiable at the gate level. If T2 fails — rescuing retention also rescues the
organism under SR-1 — then the boundary is *not* constitutive of exchange, and the successor
is a no-op; record the negative and stop. If T2 passes but T3's "sole antecedent" fails (some
supplied quantity other than B carries exchange), the claim is weaker than specified and must
be reported at the weaker level. This card stops at the specification; the build (a new
`acN.py` plus protocol and frozen run, per the project's extension checklist) is a separate
card that S0 may commission.

---

## Sources

`ac4.py` (`react` actions 0/1, `balance` identities, `available`, action 8),
`ac4_transport.py` (`inside`, `crossing_link`, `move`, 20 links), `ac9.py` (`step` transport
call, contact/deposit path, `observe`), `DEFINITIONS_CHARTER_v2.md` (§5, §7a, §8, §9),
`DEFINITIONS_CHARTER_v1.md` (§2 clause (ii), §5, §6), `CLOSURE_VERDICT_v1.md` (K3),
`A2_BOUNDARY_VERDICT_v1.md`, `A1_REALIZATION_LEDGER_v1.md`, `EVIDENCE_INDEX_v3.md`.
Primary sources: Maturana & Varela 1980 (clauses (i)/(ii)); Montévil & Mossio 2015
(closure of constraints).
