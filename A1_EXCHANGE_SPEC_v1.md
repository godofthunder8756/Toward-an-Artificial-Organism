# A1 — SR-2: an explicit exchange model whose ceiling is a produced interface

2026-09-24. Deliverable for the A1 card (t_395079ed): *replace SR-1's claim and test
specification.* It answers one question — *what is the smallest explicit exchange model
whose claim ceiling is a PRODUCED interface (not a global B-count gate), and what tests
identify it?* — and freezes that model's claim ceiling and discriminating predictions
before any engineering.

This is a specification document. No study is run, no frozen row/hash/ledger is touched,
and no successor runner is built. Every code fact is read from the frozen sources at HEAD
`57ca900` (`ac4.py`, `ac4_transport.py`, `ac9.py`, `ac10.py`); the link indexing is
re-derived at runtime (`_a1_verify_links.py`). Vocabulary is charter v2 (§5 substrate, §7a
components, §8 criterion), the K3 verdict (`CLOSURE_VERDICT_v1.md`), the A2 verdict
(`A2_BOUNDARY_VERDICT_v1.md`), and the SR-1 spec (`A0_SUCCESSOR_SPEC_v1.md`), whose claim
and test ceiling this document replaces. Predecessor: B0 (`BASELINE_v3.md`).

---

## 0. The answer, stated first

SR-1's aggregate integrity gate — `react` actions 0/1 credit `in_m`/`in_f` only while
`(b.boundary > 0).sum() >= B_MIN` — is a **global B-count gate**. Its ceiling is correctly
**"B-dependent intake"**: intake is a non-decreasing function of *how many* links are alive,
with no site, no crossing, no semipermeability. It does **not** establish transport through
a produced interface, and SR-1's §5–§6 over-sold it as though it did.

The smallest successor that *does* earn the produced-interface ceiling is **SR-2**, and it
is barely larger than SR-1: make each contact channel's intake a function of the **local
live-state of a declared set of boundary links** (the channel's *gate links*), rather than
of the aggregate count. The 20 perimeter links are already positioned, finite-lived,
produced (action 8, W-anchored, program-selected) and renewed; the transport law already
maps a crossing to a specific link. SR-2 adds exactly one thing: **the admission decision
reads the link at the crossing site, not the global sum.** The aggregate gate is kept, but
**demoted to a comparison arm** whose ceiling is explicitly "B-dependent intake."

If SR-2 passes its prespecified gates, the licensed wording upgrades by one step — from
"the boundary retains constituents" (A2) to "the same produced links that retain the
constituents are the sites at which the resources that fund production are admitted." It
does **not** complete clause (ii), is **not** the only possible successor, and does **not**
promise autopoiesis. Those are non-claims, stated in §5 and §9.

---

## 1. Why SR-1's ceiling was too high (the defect being corrected)

Three properties distinguish "transport through a produced interface" from "B-dependent
intake," and SR-1's gate has none of them:

| Property | Meaning | SR-1 (aggregate gate) | SR-2 (site gate) |
| --- | --- | --- | --- |
| **Localization** | exchange happens at a defined boundary site | none — the sum has no position | channel c is assigned a site set `GATE_LINKS[c]` |
| **Local admission** | intake is a function of the *local* link state at the site | no — only the global count matters | intake iff the assigned links are live |
| **Crossing semantics** | outside resource crosses a live link into the interior; the same link blocks the constituents' exit | no — intake is decoupled from any crossing | declared; the gate link is the crossing site, semipermeable |

Because SR-1 lacks all three, its tests were mis-shaped: T1 demanded unchanged `no_B`
trajectories (impossible once `no_B` also cuts intake), T2 read a death scalar ("reservoirs
depleted at death") instead of measuring admission, and T3 asserted "B is the sole causal
antecedent" — a claim no single factor in a network can satisfy. §6–§7 replace all of it.

---

## 2. The produced site structure already exists (code facts, verified)

The model does not need a new spatial layer. The frozen physics already contains a set of
20 positioned, finite-lived, produced crossing sites:

- `b.boundary` is 20 integer link lifetimes (charter §7a C3). Each link is a fixed
  perimeter **edge** of the 5×5 interior `|pos| ≤ 2`; `ac4_transport.crossing_link`
  maps an interior↔exterior cardinal crossing to a link id 0–19 (both inward and outward).
  Verified at runtime (`_a1_verify_links.py`): links 0–4 are the right edge (x:+2→+3,
  y=−2…+2), 5–9 the left edge (x:−2→−3), 10–14 the top edge (y:+2→+3), 15–19 the bottom
  edge (y:−2→−3). `ENDPOINTS[i]` is exactly link i's interior endpoint (same indexing).
- **Production.** Action 8 sets an expired link's lifetime to 256 for 2 M + 2 E, anchored
  by a live interior W within Manhattan distance 1 of the link's interior endpoint
  (`near = (|ENDPOINTS − wp|.sum(axis=2) <= 1)`), and selected by the program (C9). It
  targets the most-depleted producible link (`np.argmin(b.boundary[candidates])`), so the
  organism preferentially heals the links nearest death. B turns over ~10× per 2,048-tick
  run (A2 §2).
- **Decay.** Every link decrements each tick; lifetime 0 is a **hole**. A hole is the
  absence of a crossing site.
- **Semipermeability, half-present.** A live link already blocks the produced W/C
  constituents from exiting (retention, A2 §1; `tr.move` reflects impermeant particles at
  `links[edge] > 0`). The missing half is the *inward* direction: nothing currently crosses
  a live link into the interior, because `react` credits intake without consulting any link.

The interface is therefore **the boundary component B itself** — no new component is
introduced. SR-2 extends B's causal role (retention → retention + exchange) exactly as A0's
SR-1 property 1 required, but the extension is **site-specific** rather than aggregate.

---

## 3. The explicit exchange model (SR-2)

### 3.1 Exchange sites

World constant `GATE_LINKS: {0: S0, 1: S1}`, each `Sc` a non-empty subset of link ids
{0…19}, supplied (charter §5) exactly as the channel→port `mapping` already is. The minimal
default is a **singleton** per channel (`S0 = {g0}`, `S1 = {g1}`) for the sharpest
discrimination; the protocol fixes the actual indices. The *structure* frozen here — not the
indices — is: **channel c's intake is a function of the local live-state of `Sc` alone, and
no other link.**

The channel→port association is orthogonal and unchanged: the port still says *which key
matches*; the gate link adds *where the resource enters*. Both are supplied.

### 3.2 Environmental availability

The exterior holds an infinite bath of material and fuel (the environment is not a finite,
tracked reservoir; it is a declared source, of a piece with the frozen constants `in_m=64`,
`in_f=32`). Availability is the yield: `YIELD = {0: 32 fuel, 1: 64 material}`, the frozen
values, unchanged.

### 3.3 Admission / transport

On a productive contact of channel c (program selects action c, the matched port equals
`mapping[c]`, as frozen):

- if at least one gate link `j ∈ Sc` is **live** (`b.boundary[j] > 0`): the resource crosses
  at the live link and `in_c = YIELD[c]` is credited — the frozen `react` branch, unchanged;
- if **every** gate link is a hole: `in_c = 0`, and the contact takes the **failure branch
  already in the code** (`ac9.step` lines 87–88: energy −1, no intake) — the same branch a
  port mismatch takes today.

So a dead interface is *strictly costly*: the organism keeps paying the 1-energy contact
cost and receives nothing. That cost asymmetry is what makes the interface's renewal
load-bearing, not a decoration.

### 3.4 Interior credit, overflow/loss

A crossed resource is credited to the interior reservoir (`b.material` / `b.fuel`) subject to
its cap, with the excess returned to the outside bath as `overflow_m`/`overflow_f` — the
frozen `react` overflow computation, unchanged.

### 3.5 Transport cost (declared, not hidden)

The interface is **passive**: there is no per-crossing cost beyond the existing 1-energy
contact cost (paid whether or not admission succeeds, as in the frozen failure branch). The
produced interface's cost is its *production* cost — action 8's 2 M + 2 E per link birth,
W-anchored — amortized over the crossings it admits. This is a declared model choice, stated
so a later economy check can be done honestly (the capability's payoff vs its maintenance
cost, per the project's economy-check rule).

### 3.6 Which produced component realizes the interface, and its production dependence

The interface is realized by the **boundary links B** (charter §7a C3), the same produced
constituent that realizes retention. Its production is unchanged and already established
(A2 §2, C1–C5): action 8 pays 2 M + 2 E, requires a live interior W within Manhattan
distance 1 of the link's interior endpoint (C3: W → B), is selected by the program (C9 →
B), turns over ~10× per run (C2), and sits on the W → B → W cycle (C5). The interface
therefore depends on the organization in exactly the way B already does — no new dependence,
no new component, no new content.

### 3.7 Inside / outside / crossing

- **Inside** = the 5×5 interior, holding the produced constituents W/C and the
  material/fuel reservoirs.
- **Outside** = the exterior, holding the infinite resource bath.
- **Crossing (inward)** = a resource admitted at a live gate link (exchange). **Crossing
  (outward)** = a W/C exiting (blocked at live links — retention; unblocked at a hole —
  export and death). The link is **semipermeable**: barrier to the constituents' exit, gate
  to the resources' entry.

### 3.8 Supplied spatial substrate vs produced organization

| Supplied (substrate, charter §5) | Produced (the organization) |
| --- | --- |
| lattice, interior/exterior, `crossing_link`, export bath | the 20 link lifetimes (the interface's presence/absence) |
| port-match contact, channel→port `mapping`, `YIELD` | W/C/B constituents and their production network |
| channel→link `GATE_LINKS` association, reservoir caps, conservation identities | the program's choice to produce/renew links (C9 → action 8) |
| action-8 reaction form, damage model, world constants | — |

The organism produces the **state** that makes the interface present or absent; it does not
produce the spatial distinction itself (unchanged from A2 §4.2 and A0 §8).

### 3.9 Expressible inside the frozen conservation identities (no law patching)

`ac4.balance` asserts `b.material == M + e['in_m'] − e['overflow_m'] − e['spent_m']` (and
the fuel/energy analogues), with `in_m`/`in_f` carried as *variables*. Gating `in_c` down
to 0 when the gate link is a hole satisfies every identity **by construction** — the same
AC15-lesson point SR-1 already made (§5 property 2). No external matter is injected, no
identity is modified. The per-link "punch" intervention (§6 D1) is likewise a *restriction*
of the frozen action-8 candidate set (exclude one link index), of the same shape as AC10's
`no_B` (which excludes all), so the boundary-count identity
`(b.boundary>0).sum() == B + B_birth + external_B − B_expiry − B_discard` still holds.

---

## 4. The aggregate rival (comparison arm), demoted

SR-1's aggregate gate survives as a **comparison arm**, not as the successor. Its form:
intake admitted iff `(b.boundary > 0).sum() >= B_MIN`, `B_MIN` a supplied threshold. Its
ceiling is stated on the tin: **"B-dependent intake"** — intake tracks the *count* of live
links and is spatially indifferent to *which* links are live. The decisive test (§6 D1)
turns on the fact that the rival cannot express "this link is the interface," because no
site enters its condition.

The rival is not a strawman: it is SR-1's own design, and it is a genuinely weaker but
non-trivial dependence (B still matters, just count-wise). The successor's job is to show
the *site* dependence that the rival lacks.

---

## 5. The frozen claim ceiling (stated before engineering)

| Level | Wording | Status |
| --- | --- | --- |
| **Retention (established)** | the organism produces a finite-lived perimeter that retains its produced constituents inside a bounded interior | A2, frozen |
| **B-dependent intake (rival)** | intake is a non-decreasing function of the aggregate count of live boundary links | comparison arm's ceiling, not the claim |
| **Produced interface (SR-2)** | the organism produces and renews a finite-lived perimeter whose live links are the sites at which the environmental resources that fund production are admitted into the interior — the same links that retain the constituents admit the intake that funds all production | **what SR-2 would establish**, if D1–D5 and T1–T6 pass |
| **Full clause (ii) / autopoiesis** | — | **not claimed**; see §9 |

The SR-2 wording is the ceiling, and it is deliberately one step above A2 and one step below
full clause (ii). It is **not** "alive", not "autopoietic" unqualified, not a completion of
the two-clause M&V definition, and **not** "the only possible successor." These are
non-claims, and the successor runner's protocol must repeat them.

---

## 6. Discriminating predictions (prespecified, frozen before engineering)

The predictions are about **which links** matter to intake. They are stated so that each is
a falsifiable gate, not a description.

- **D1 (site sensitivity vs count sensitivity — the decisive prediction).** Hold the program,
  coin, mapping, and all else fixed. Puncture **all** of channel c's gate links (`Sc`) — set
  each to lifetime 0 and exclude them from action-8 candidates — while leaving at least one
  non-gate link live (so the aggregate live-link count stays high). Under SR-2, channel c's
  admission `in_c` is **0** for the intervention's duration; under the aggregate rival (with
  `B_MIN` below the surviving count), channel c's admission is **unchanged**. The two models
  disagree on the same intervention, and the disagreement is the site/count distinction.

- **D2 (admission is local).** Puncture a **non-gate** link of channel c under SR-2: channel
  c's admission is **unchanged**, while the retention endpoint (export count) changes only
  trivially (19/20 links still retain). A single gate-link hole cuts a whole channel's
  intake; a single non-gate hole does not. This is what "local" means and what the rival
  cannot reproduce.

- **D3 (semipermeability: one structure, two roles).** In the `keep` arm, the *same* links
  that reflect W/C (retention, measured as blocked crossings and zero export) are the gate
  links through which intake is credited. There is no arm in which retention is intact while
  exchange is decoupled from the same link set — the two roles ride one paid structure.

- **D4 (production dependence).** Block W-birth (AC10 `no_W`): with no W anchor, action 8
  cannot produce any link, so the link lifetimes decay toward holes and the gate links lose
  their live-state — the interface's absence is produced by the loss of the W catalyst, not
  by a host-side cut. This arm carries the AC13/AC91 attention-hijack confound (obs bit 6
  stays set, the blocked W-birth rule preempts other actions, death ≈ t 251), so D4 is a
  *mechanism trace read before death*, and the gate-link-vs-death timing must be verified in
  engineering, not asserted. The confound-free production-dependence evidence is D1, which is
  the primary gate; D4 inherits B's already-established C3 dependence (A2 §2), not a new
  empirical claim.

- **D5 (renewal).** Over the horizon, the gate links turn over like every other link (~10×,
  per the A2 count); their live-state is continuously re-established by action 8, so the
  interface is *renewed*, not a one-shot endowment.

The numeric constants (`GATE_LINKS` indices, `B_MIN`, `YIELD`) are supplied world constants
fixed at protocol time; D1–D5 hold for any non-empty `Sc` and any `B_MIN` below the
post-puncture surviving count. The predictions, not the constants, are what freeze here.

---

## 7. Corrected tests (replace SR-1's T1–T4)

Each correction is named against the SR-1 defect it fixes.

- **T1 — retention continuity, with the intake mechanism DISABLED or MATCHED.**
  (Corrects SR-1 T1's "unchanged no-B trajectories.") To show SR-2 does not disturb
  retention, run the retention-rescue arm (`no_B_retention`: B production suppressed, kernel
  reflection forced) with the exchange gating **disabled** (a `GATE` flag off), and confirm
  it reproduces the frozen `no_B_retention` result (8/8 survive, zero export, routes held,
  `state_hash` equality at the matched schedule). Do **not** require the `no_B` arm to match
  the frozen `no_B` arm: under SR-2, `no_B` now also cuts intake (no B ⇒ no gate links ⇒ no
  admission), so its trajectory legitimately changes. Retention continuity is established by
  the disabled-exchange retention-rescue arm, not by unchanged no-B trajectories.

- **T2 — exchange mediation, measured directly.**
  (Corrects SR-1 T2's "dies by income starvation.") With retention rescued (`no_B_retention`)
  but the gate links dead, read the ledger: **`in_m == 0` and `in_f == 0` every tick**. The
  causal chain is the ledger, not a death scalar: admission 0 → reservoir depletion
  (trajectory) → production (W/C/B births) stops → energy drains → death. If B were only a
  retention wall, rescuing retention would restore admission; under SR-2 it does not. Death
  is the terminus; the **admission ledger** is the mechanism.

- **T3 — a precise conditional-dependence claim (not "sole antecedent").**
  (Corrects SR-1 T3.) The claim is: *conditioned on the program selecting action c and the
  contact being productive (port match), intake is admitted iff a gate link of channel c is
  live; intervening on a gate link's lifetime while holding the program, coin, mapping, and
  all other links fixed changes `in_c` from `YIELD[c]` to 0, and intervening on a non-gate
  link under the same conditions leaves `in_c` unchanged.* "B is the sole causal antecedent"
  is dropped — the program, the port match, and the W anchor are also antecedents, and the
  honest claim is a conditional dependence on the gate link's state.

- **T4 — discrimination against the aggregate rival.**
  (New; this is the test that identifies SR-2.) Implement the rival as an arm and assert D1's
  disagreement: on the punctured state, the interface arm has `in_c = 0` and the rival has
  `in_c = YIELD[c]`. If the two arms' admission is identical on every punctured state, SR-2
  has collapsed back into SR-1 and the successor is a no-op.

- **T5 — inertness (the site gate is the only change).**
  (Kept, sharpened.) With the exchange gating disabled, or with all gate links held live,
  SR-2 must be byte-identical to the frozen world (`state_hash` equality at the unchanged
  schedule). Because in ordinary operation the gate links are essentially always live
  (action 8 preferentially heals the most-depleted links), `keep` under SR-2 should be
  byte-identical to frozen `keep` — the exchange function is exercised only when the
  boundary is challenged, which is exactly when the produced-interface claim is tested.

- **T6 — external rescues labeled external.**
  (Kept, corrected.) `B_rescue` (external B matter, zero internal births) restores **both**
  retention and the gate links, hence restores admission — and is labeled **EXTERNAL**, never
  counted as autonomous (AC10 convention). It confirms the boundary *state* carries the
  interface role; it does not demonstrate the organism produces it.

**Measurement discipline (applies to all tests):** admission (`in_m`/`in_f` per tick),
retention (blocked crossings, export count), production (W/C/B births), and depletion
(reservoir trajectories) are reported as **separate ledger endpoints**; death alone
identifies no mechanism. Planned-denominator activity and survival are reported as a
bimodality-aware lower bound (AC68). Engineering seeds first, then the protocol, then
disjoint final seeds; a predeclared gate that fails is recorded, not moved (AC16).

---

## 8. Falsification and stopping

SR-2 is falsifiable at the gate level. **D1 is the decisive prediction**: if puncturing the
gate links fails to zero channel c's admission (admission continues from elsewhere), then
intake is not a function of the local link state and SR-2's "produced interface" ceiling is
not earned — record the negative and stop. If D1 passes but D4 fails (admission does not
depend on W-anchored link production), the interface is produced by the world, not the
organization, and the claim must be reported at the weaker "B-dependent intake" level. If T5
fails (the gating changed the frozen economy even with the gate held live), the successor is
not inert and the build is defective. This card stops at the frozen specification; the build
(a new `acN.py` per the extension checklist, plus protocol and frozen run) is a separate card
for S0's successor to commission.

---

## 9. What remains substrate, and the explicit unresolved limitation

- **The non-spatial informational core is the named, unresolved residual.** The program,
  description, route memory, pointer, and decision state remain in fixed arrays that are
  never positioned and never passed to `tr.move` (A2 §4.2). SR-2 realizes the exchange
  interface for the **material layer** only; the controller's situation is still "inside by
  declaration." This is a separate re-architecture, out of scope, and clause (ii) after SR-2
  remains explicitly scoped to the material layer.
- **Supplied space / geometry** (lattice, interior/exterior, reflection, export bath) —
  permanent substrate; producing the space is an infinite regress (J1 / A0 §8).
- **The exchange reaction's form, once gated** — supplied. The organism conditions intake on
  the boundary state it produces; it does not rewrite the reaction.
- **Content** — rule words, priority, and the `GATE_LINKS` association are inherited/supplied
  (charter §6); content self-production is AC78-blocked and not required.
- **Interpreter, succession semantics, decode format, write primitive, conservation laws,
  damage model, world constants** — substrate (charter §5).

The single load-bearing requirement SR-2 adds is causal and local, not inventive: **the
produced link at the crossing site must be the thing the exchange depends on.**

---

## Sources

`ac4.py` (`react` actions 0/1, action 8, `balance`, `ENDPOINTS`), `ac4_transport.py`
(`inside`, `crossing_link`, `move`), `ac9.py` (`step` contact path lines 85–89, `observe`),
`ac10.py` (surgery sites for `no_B`/`no_B_retention`/`B_rescue`/`no_W`), `A0_SUCCESSOR_SPEC_v1.md`
(SR-1), `A2_BOUNDARY_VERDICT_v1.md`, `BASELINE_v3.md`, `DEFINITIONS_CHARTER_v2.md` (§5, §7a,
§8, §9), `CLOSURE_VERDICT_v1.md` (K3). Runtime verification: `_a1_verify_links.py`
(crossing-link indexing). Primary sources: Maturana & Varela 1980 (clauses (i)/(ii));
Montévil & Mossio 2015 (closure of constraints).
