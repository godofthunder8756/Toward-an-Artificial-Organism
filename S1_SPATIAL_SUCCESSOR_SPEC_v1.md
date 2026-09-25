# S1 — The spatial informational-core successor: specification (design-only)

2026-09-25. Successor-design deliverable for the S1 card (t_5380f752): *turn the A0
clause-(ii) requirement (R1–R4, tests T1–T5) into a concrete successor architecture and a
frozen proposed protocol, marked AWAITING separate execution authorization.*

This is a definitional/design document. No study is run, no runner is built, no seed is
frozen, no results directory is created, and no frozen artifact, hash, or ledger is touched.
Every code fact is read from the frozen sources at HEAD bd26525 (`ac4.py`, `ac4_transport.py`,
`ac9.py`, `ac5_program.py`, `ac95.py`, `ac9_memory.py`) and re-checked against their line
numbers below. Vocabulary is `DEFINITIONS_CHARTER_v2.md` (§5 substrate, §7a components,
§7b maintained state, §8 C1–C5/S1–S4), `CLOSURE_VERDICT_v1.md` (K3),
`A0_AUTONOMY_VERDICT_v1.md` (§4–§6), `I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md`.
Predecessor: S0 (`S0_CONTINUATION_DECISION_v1.md`); the spec-form precedent is SR-1
(`A0_SUCCESSOR_SPEC_v1.md`).

---

## 0. The answer, stated first

**The successor realizes the informational core as a produced, finite-lived, position-bearing
component class "I", read and written only through produced, position-mediated machinery, and
keeps the frozen conservation identities untouched by construction.** One new component class
plus one role-extension (W gains a reader/writer head), a re-architecture of the supplied
physics exactly as A0 §5 anticipates — not a run inside the frozen model, not a coordinates/
`tr.move`-passing gesture (A0 §4 rules that out), and not full autopoiesis.

The informational core named by A0 §5 and I5 §5 is:

| Item | Frozen realization (non-spatial) | Clause |
| --- | --- | --- |
| program + decision register | `traces[0,:126]` (126 bits × 7 replicas) | C9 / C8 |
| description (active slot) | `traces[1,:130]` (130 bits × 7 replicas) | C4 |
| generation pointer | `traces[1, 520:522]` (2 bits) | C5 |
| coordination state | `traces[1, 522:540]` (18 bits) | C6 |
| route memory | `mem.Memory` (2×2×3×7) | C7 |

The frozen transport call is `tr.move(b.pos, inactive, b.boundary, directions,
np.ones(20, dtype=bool))` (ac9.py:78) — positions, inactivity, boundary, directions,
impermeability, and nothing else. None of the five items above is positioned or passed through
it; each is read by host dereference (`prog.choose(b.traces, observe(o))`, ac9.py:84; the
interpreter itself dereferences `traces[0,:PROGRAM_BITS]`, ac5_program.py:35). The successor
moves the *realization* of these bits from declared arrays into produced substrate, and moves
the *access* from host dereference to position-mediated machinery.

---

## 1. The successor architecture

### 1.1 Component class I (the informational substrate)

**I is a new finite-lived particle bank**, added to the body alongside W/C (which occupy
`life[:16]` and `life[16:20]` respectively; the frozen body is constructed at
ac4.py:49–51). Each I-particle has a lattice
position (`pos`, extended beyond the current 20 rows) and a finite lifetime (`life`, decays
one per tick like every other particle, ac9.py:75). I is a produced component, not declared
state:

- **Production.** I-particles are born by the frozen action-6 birth machinery (`birth`,
  ac9.py:42–49), extended to birth into the I bank alongside the W banks. A birth requires a
  live W parent (autocatalytic, `parents=np.flatnonzero(a[bank*4:bank*4+4])`), costs
  `pay(b,e,4,2)` = 4 material + 2 energy, and is booked as `e['W_birth']+=1` — so its births
  are already inside the frozen balance identities with **no new term** (§1.4). Because the
  same action 6 that maintains W also maintains I, I's production is within-network (C3) and
  on the W cycle (R4). A distinct `I_birth_enabled` gate on the I-bank portion of action 6 —
  never on the W banks — is what makes T3/T4's directed production cut clean (the AC92
  `block_W` pattern, inverted: the cut is machinery-only, content untouched).
- **Turnover.** I-particles decay every tick and export when transport carries them past
  `|pos|≥6` (ac4_transport.py:39); births replace them. Turnover is observed as birth/expiry
  events, exactly as for W/C/B (R1, C1/C2).
- **Bit encoding (positional).** Each logical bit is a *site* of two adjacent cells, a
  "0-cell" and a "1-cell." One I-particle occupies one cell; which cell it occupies *is* the
  bit value. Redundancy keeps the frozen convention: 7 I-particles per site, majority = which
  cell holds ≥4 (the AC71 majority-read, now spatial). A transport step that carries a
  particle across its site boundary, or a puncture that exports it, flips or degrades the bit —
  the substrate is *in* the transport and damage streams by construction (R3).

### 1.2 The localized read/write reaction (R2)

**Read.** A read of site s is performed by a live W catalyst co-located with s (a produced
reader head). The reader observes how many of s's 7 I-particles sit in each cell and reports
the majority bit. A site with no co-located live reader returns *unreadable* (`None`), not a
value. The interpreter `prog.choose` — which remains supplied substrate (J1) — consumes the
vector of per-rule read results; a rule word containing any unreadable bit does not match
(fallthrough). So **there is no host dereference of an informational array**: the only path
from a bit to the interpreter runs through the produced reader. The host's `traces[0,:126]`
etc. are gone as the source of truth.

**Write.** A bit write is a paid, W-gated *move* of an I-particle from the wrong cell to the
correct cell. The move costs 1 energy + 1 material per particle, is gated by the frozen write
capacity `_cap = min(32, 8·available_W, energy, material)` (ac95.py:336–338), and is booked as
`e['writes']` — again, already inside the frozen balance. The *direction* of the repair (which
cell is "correct") is carried by a retained write-value / directional-knowledge state — the
AC117 CONTROL finding composed forward as the R2 primitive the S0 decision named — and per
AC116 the endpoints separate causal load-bearing (does the write happen, does the read fail)
from economic payoff (income), which is **not** gated.

### 1.3 Mutual constraint (R4)

The directed production cycle holds through the local coupling, extended to I:

```
I (the program) --selects--> action 6 --births--> W  --gates--> I read/write + I birth
        ^                                                            |
        +----------------- W co-located reader ---------------------+
```

Production maintains I (action 6 births I, W powers I's paid writes), and I constrains
production (the program realized in I selects which births happen). I and W/C/B lie on the
same strongly-connected production-dependency network, so C5 is satisfied with I included.

### 1.4 Conservation (no law patching, no free external matter)

The frozen identities (ac4.py:122–129) are satisfied **by construction**, term for term:

- I-births are booked `W_birth` (same `pay(b,e,4,2)`), so
  `spent_m == writes + 4·(W_birth + C_birth) + 2·B_birth` is unchanged.
- I-writes (moves) are booked `writes` (1 M + 1 E each), so the same identity and
  `b.material == M + in_m − overflow_m − spent_m` hold.
- I-particles are ordinary rows in `life`, so
  `(b.life>0).sum() == N + W_birth + C_birth − particle_expiry − particle_export` holds
  (N simply counts them; their births are W_birth and their deaths are expiry/export).

No conservation identity is edited, no law is patched, and no matter arrives except through
the organism's own paid contact intake and production. The only "supplied" changes are world
constants of the permitted-substrate kind (geometry/lattice size, and the site layout) — the
same category as `PORTS`, `GATE_LINKS`, `B_MIN` (A0 §3, charter §5).

---

## 2. The gate set (T1–T5, shapes chosen per claim)

Carried verbatim from A0 §6 as the falsification gates, with gate shapes fixed by the
AC16/AC17 rule: every claim is **categorical**, so every gate is dominance, separation-of-
minima, or exact equality — never a mean margin. Satisfiability is checked against the bounds
before freezing (§2.6).

### T1 — localized read (R2). Gate = dominance, per individual.

Ablate the produced reader at one program bit's site. Gate: in **every** individual, during
the ablation window the ablated rule cannot fire and action selection **differs** from the
intact arm; after the organism restores the reader endogenously (no content supplied), action
selection **returns to** the intact arm. Shape: per-individual binary `differs ∧ restores`,
N/N. Satisfiable: there is no ceiling tie — "differs" is a categorical behavioural divergence,
not a score to maximize.

### T2 — retention vulnerability (R3). Gate = separation of minima, per individual.

Puncture the boundary (the AC114 `puncture_gate` pattern). Gate: in **every** individual, the
spatial arm's informational-correct drops below threshold under puncture **and** the
transport-exempt contrast arm's stays at full (does **not** degrade). Shape:
`spatial_min < bar ∧ exempt_min == full`, N/N. Satisfiable by construction: the exempt arm is
transport-exempt (its bits are never passed to `tr.move`), so "stays full" is its ceiling, not
a tie.

### T3 — production dependency (R4, production→I). Gate = dominance, per individual.

Block I-bank production (`I_birth_enabled=False`) timed to interrupt while the informational
function is underway — the AC92 functional-interruption pattern, **not** a t=0 kill; the cut
lands ~one I-lifetime before the function tick so the substrate depletes naturally. Gate: in
**every** individual, the informational function (action selection / reconstruction) stalls
while the organism is alive and content is intact at interruption, **and** a machinery-only
EXTERNAL restoration (re-seed the I bank, no content supplied — the AC92 direct-restore shape)
resumes it. Shape: per-individual binary `stalls ∧ content_intact ∧ resumes`, N/N.

### T4 — mutual-constraint directionality (R4). Gate = separation, per individual.

Two directed cuts with separable effects: (i) informational→production read cut (scramble/
remove the reader at the program sites) — production ceases while the informational state
itself survives; (ii) production→informational maintenance cut (`I_birth_enabled=False`) — the
informational state degrades while W/C/B production continues until the state is lost. Gate: in
**every** individual the two cuts produce **separable** effects — (i) kills production with the
I-state intact, (ii) kills the I-state with production intact. Shape: per-individual
`cut_i_effect ≠ cut_ii_effect` (a categorical separation), N/N. This is the AC108
both-direction pattern at the organizational layer.

### T5 — no hidden backup (observer-discard). Gate = exact equality, per individual.

The host discards its record of the bits and re-reads them only through the local machinery.
Gate: the trajectory is **byte-identical** (`state_hash` equality) to the un-discarded run, at
two discard points per individual (mid-function and terminal), matching the AC95-D4
observer-discard discipline (prove the swap fired, not a silent no-op). Shape: exact equality,
N/N.

### 2.6 Satisfiability and falsification (prespecified, carried verbatim)

Falsification (A0 §6, verbatim): the successor is falsified if (i) a hidden host array still
reproduces the trajectory under T5, or (ii) removing the local reader leaves action selection
unchanged under T1, or (iii) a transport-exempt informational core behaves identically to the
spatially realized one under T2. Each maps to a gate above: (i)→T5, (ii)→T1, (iii)→T2. The
T2 contrast arm *is* the transport-exempt core (the frozen declared-array representation),
which is why (iii) is a live falsifier and not a strawman.

---

## 3. The frozen proposed protocol

World constants, interventions, rival/control arms, seed families, and the
engineering-vs-finals split are specified in the companion document
`S1_SPATIAL_CORE_PROTOCOL_v1.md`, which is **AWAITING separate execution authorization** —
it freezes nothing and licenses no run. This document stops at the specification.

---

## 4. The precise ceiling

If the successor passes T1–T5 on untouched finals, the licensed wording upgrades by exactly
one step:

- **Before:** "the organism produces a finite-lived perimeter that retains its produced
  constituents, while the informational core lives in declared arrays that are inside only by
  declaration" (I5 §5 — clause (ii) met at the material layer only).
- **After:** "the informational core's realization is part of the produced-and-maintained
  causal network — its substrate is produced and turns over, its reads and writes are
  position-mediated through produced machinery, its retention is earned (paid, W-gated,
  transport-vulnerable), and it lies on the production-dependency cycle with W/C/B."

That moves clause (ii) for the informational core from **"declared" to "produced"** — one
step, and **not** full autopoiesis, **not** "alive", **not** content self-production (AC78
blocked), **not** a claim that space or geometry is produced (that is permanent substrate,
J1 / `CLOSURE_BOUNDARY_v2`), and **not** a survival guarantee (survival stays a
bimodality-aware lower bound, AC39/AC68). The interpreter (`prog.choose`), succession
semantics, decode format, reaction forms, conservation laws, damage model, and initial content
all remain supplied. What is newly earned is the *realization and access* of the informational
core — the causal relationship R1–R4, nothing more.

---

## 5. What remains fixed substrate (the explicit non-demands)

- **Geometry / lattice** (enlarged to hold the bit-sites) — permanent substrate; producing the
  space is the J1 infinite regress.
- **The interpreter, decode format, succession semantics, reaction forms, conservation laws,
  damage model, tick clock** — substrate (charter §5, I5 §5).
- **Initial content** (the specific program/description/pointer/coordination bits, the rule
  words, the priority permutation) — inherited/supplied at acquisition (charter §6, C4 content
  boundary); content self-production is not required.
- **The reader head's existence as a role** — the W class is extended, not re-invented; no new
  physical law, no self-rewriting of laws (infinite regress).

The single load-bearing requirement added is **causal**: the informational bits must be
produced substrate, accessed through produced machinery, vulnerably retained, and mutually
constrained with the constituents.

---

## Sources

`ac4.py` (balance identities 122–129; `available` 55–56; `pay` 76–79; action-6 birth 97–106),
`ac4_transport.py` (`inside` 11–12; `move` 29–42; export 39), `ac9.py` (`acquire` 24; step
transport call 78; `observe` program-bank damage 55; core damage 74; action selection 84;
`birth` 42–49), `ac5_program.py` (`choose` 33–41, dereference of `traces[0,:126]` at 35),
`ac95.py` (description/pointer/control layout 59–89; `_cap` 336–338), `ac9_memory.py` (Memory
`(2,2,3,7)` 12–14; `deposit` 55–71; `renew` 74–90), `DEFINITIONS_CHARTER_v2.md` (§5, §7a,
§7b, §8), `CLOSURE_VERDICT_v1.md` (K3), `A0_AUTONOMY_VERDICT_v1.md` (§4–§6),
`I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` (§5), `A0_SUCCESSOR_SPEC_v1.md` (SR-1 form),
`S0_CONTINUATION_DECISION_v1.md` (decision c). Frozen results read, never re-run or re-hashed.
This document is derived and is not hashed into any study's `pre_run_snapshot.json`.
