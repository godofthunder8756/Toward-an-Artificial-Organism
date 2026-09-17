# Dependency audit v1 — what the organism actually is, verified against code

2026-09-17. Grounded in the frozen runners, not in status summaries. Every mechanism below is traced to
the code that realizes it (`ac1.py` → `ac4.py` → `ac5.py`/`ac5_program.py` → `ac9.py`/`ac9_memory.py` →
`ac12.py` → `ac71.py`), with the distinction the goal demands: **demonstrated** / **diagnostic** /
**untested interpretation** / **external scaffold**.

## 1. The physical substrate

`ac4.Body` (`ac4.py`) holds the persistent state:

| field | shape | what it is |
| --- | --- | --- |
| `traces` | (4, 1024, 7) | 4 banks × 1024 bits × 7 replicas. The controller is `traces[0,:126]`; the rest is legacy AC1/AC4 policy-table storage, present and repairable but **not read** by the interpreter |
| `life` | (20,) | 20 particles: 16 W sites (`[:16]`, 4 banks × 4) + 4 C sites (`[16:20]`) |
| `pos` | (20, 2) | particle positions (grid −2..2) |
| `boundary` | (20,) | 20 boundary sites (values 128…242, decay to 0) |
| `energy/material/fuel` | scalars | the resource ledger, capped (128 / 256 / 64) |

`mem.Memory` (`ac9_memory.py`) holds the acquired routes: (2,2,3,7) — 2 regions × 2 slots × 3 bits
(valid,key,value) × 7 replicas, plus matching `life`.

## 2. Causal inventory

For each component: realization → what produces/replaces it → required resources → dependents → external
status.

| component | realized by | produced/replaced by | requires | depends on it | status |
| --- | --- | --- | --- | --- | --- |
| **energy** | scalar | fuel→energy conversion (passive, `ac9.step`), 8 per C site per tick | live C sites + fuel | everything (action cost, `b.dead` when <1) | generic law |
| **fuel** | scalar | action 0 (contact), +32 | program chooses action 0 | energy conversion | generic law |
| **material** | scalar | action 1 (contact), +64 | program chooses action 1 | W/C/B birth, repair, renewal | generic law |
| **W** (production machinery) | `life[:16]` | action 6 (birth), each costs 4 M + 2 E | **a live W parent** (`parents=…a[bank*4:…]`) | C birth, B birth, deposit, repair capacity (`8*interior_W`) | **produced by the program's action** |
| **C** (converters) | `life[16:20]` | action 7 (birth), 4 M + 4 E | a live W parent | energy conversion (passive) | **produced by the program's action** |
| **B** (boundary) | `boundary` | action 8 (birth), 2 M + 2 E | live W (position anchor) | retention (transport: particles outside boundary export) | **produced by the program's action** |
| **program** (controller) | `traces[0,:126]` | **nothing produces it**; repaired (action 2) restores replicas to their stored majority | repair = 1 M + 1 E per changed replica | chooses every action (incl. all production) | **EXTERNALLY SUPPLIED, maintained not produced** |
| **register** (decision state) | 4 bits in a dead rule's mask bits, inside `traces[0,:126]` | written by `_drop` (relinquish) / `_restore`, repaired by bank-0 repair | paid per replica | allocation decision (which slot to renew) | stored in the program's own substrate; semantics inverted so zero = frozen |
| **routes** (acquired function) | `mem.Memory` | deposit path (`mem.deposit`, binds key/port on productive contact) | `grow` flag + `activation[region]` + a **live W parent** + paid 21 M/E | the organism's income (contact uses stored port) | **acquired by the organism's own contact outcomes**, but the deposit *gate* is externally scheduled |
| **interpreter** | `prog.choose` | fixed law | — | — | **generic simulator law** (a fixed ISA reading mutable rules) |
| **sensing** | `ac9.observe` | fixed law | — | — | generic law (includes the self-monitoring corruption bit 2) |
| **repair** | `ac4.react` actions 2–5 | majority repair of a bank, paid | program chooses the action | program integrity | generic primitive, **invoked by the program on itself** |

## 3. What is demonstrated, what is not

**Demonstrated (frozen protocol + audit + replay, re-verified this session for AC67/68/71):**

- The organism's own program chooses the actions that birth W, C and B, so the maintenance machinery and
  boundary are **self-produced** given the program. `ac4.balance` conservation identities hold exactly.
- The paid bank-0 repair is **causally necessary for survival** under non-self-reversing (sticky) damage:
  AC67/AC71 `no_repair` dies 8/8, `closed` survives 8/8. The load is carried by the program's *self-
  monitoring* (obs bit 2 reads the program's own corruption), not by redundancy alone.
- Majority-read register (threshold 4) closes the route-lapse / body-bimodality / register-degradation
  triplet at 16,384 ticks (AC71, 5/5 gates).
- Routes are acquired during the lifetime from the organism's own contact outcomes (AC7/AC8/AC15/AC18,
  frozen).

**Diagnostic (reported, not a frozen study):**

- AC72: the AC71 config is a steady state at 65,536 ticks (4 seeds). Reported in `AC72_FINDING_v1.md` as
  "diagnostic, not frozen"; not independently re-verified in this session.

**Untested interpretations / overreach in the summaries:**

- "Self-producing" is stated about W/C/B, but the *program* that drives production is externally supplied.
  The production network is bootstrapped by an external controller; the organism regenerates its body,
  not its mind.
- "Closure" (AC67→AC72) is a **fixed-world** property. AC74 (this session) shows a post-development route
  move is fatal to 4/6 as-is and the re-acquisition path is gated externally (grow/activation) and blocked
  by a stale-route persistence window.
- "One gap remains" (AC72) names the controller, but understates that the controller is not *learned* even
  at development: the priority is a random permutation and the rules are a hand-written `demonstration()`.

**External scaffolds (correctly labelled in code, never autonomous):**

- `target`/`target_policy` (the teacher's table) — used only by `protected`/`fixed` arms.
- `shadow` (pristine program copy) — the `protected` arm only.
- The oracle scoring in the AC30–33 order world (12-seed mean) — the "self-directed" line's comparator.

## 4. The production-dependency map (causal, from AC10 ablations + code)

W is the hub: C birth, B birth, deposit and repair capacity all require live W. C is required for energy
(conversion). B is required for retention (particles otherwise export). The program is required for every
one of these (it chooses the actions) — but the program has **no incoming production edge**. The register
and routes are written and repaired through the program's substrate, but their *content* originates from
the organism's own contact outcomes (routes) and relinquishment logic (register), not from a template.

So the dependency graph has exactly one source: the program. And that source is external. Every edge the
organism "owns" (W→C, W→B, W→deposit, program→everything) is downstream of a component the organism does
not produce.

## 5. Generic law vs organism-specific machinery (the section-2 boundary)

**Generic (may stay fixed, does not do organism-specific work):** the tick loop (damage XOR/sticky, life
decay, transport, passive conversion), `ac4.balance` (conservation asserts), `prog.choose` (a fixed
interpreter of mutable rules — the analog of a CPU/ISA), `ac9.observe` (sensing), `mem.age/renew/deposit`
(memory primitives), `ac4.react` (action effects: contact yields, majority repair, birth).

**Organism-specific and currently external:** the program's *content* (rules + priority) — installed at
acquisition from a hand-written template, never produced by the organism. This is the one component that
fails the section-3 test: it is maintained (repaired) but not turned over; if all 7 replicas of a rule
corrupted, repair would cement the corruption (AC61: repair is preventive, not curative) because there is
no organism-internal correct reference.

The interpreter is not "secret repair on the organism's behalf" — it reads, it does not write. The repair
primitive is generic and is *invoked* by the program; the load-bearing work is the program's own choice.
That part of the architecture is clean.

## 6. The one structural gap, restated precisely

The organism regenerates its **body** (W/C/B), its **boundary** (B), its **function** (routes) and its
**decision state** (register) through its own ongoing activity. It does **not** regenerate its
**controller** (the 126-bit program): that component is installed once, externally, and only restored
against damage. Everything the organism demonstrably does is downstream of a component it never produced.

This is the precise, verified distance to the operational definition of autopoiesis in §2 of the goal —
a network of processes that regenerates *the components realizing the network*. The controller realizes
the network but is not regenerated by it.
