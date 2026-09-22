# Dependency audit v2 — the integrated production and maintenance network (reference: AC105)

2026-09-22. A1 deliverable. This is the **causal ledger** the A3 closure verdict and the
C1/C2 tracks stand on. It supersedes `DEPENDENCY_AUDIT_v1.md` (2026-09-17, pre-AC79), whose
"one structural gap = the controller is not regenerated" (§6) was closed by the AC80–AC89
internal-state line and is therefore **superseded**, not restated. Every row below is traced
to the frozen runner chain (`ac1 → ac4 → ac5_program → ac9 → ac9_memory → ac12 → ac12_memory →
ac71 → ac76 → ac95 → ac96 → ac99 → ac99_d2 → ac104 → ac105`), not to a status summary.

Vocabulary is the R2 charter's (`DEFINITIONS_CHARTER_v1.md`): the finite component list
**C = {C1…C9}**, the supplied substrate **S** (§5), and the four closure clauses
**C1 existence / C2 production-replacement / C3 within-network dependence / C4 content
boundary** (§8). The boundary-vs-substrate line is a modeling choice (charter §9, J1–J5);
this audit **records** it, it does not resolve it.

Frozen reference: AC105 (seeds 5800–5807, 2 histories, 2 arms, 5 conditions, 160 rows,
16,384 ticks; all 6 gates). The architecture is the AC85–AC89 internal-state substrate
(ac95 gated arm) + the AC96/AC99-D2 Gray-coded relinquishment streak + the AC104
allowance-42 spending rule. `ac99`'s reserve is **not** part of the architecture
(`reserve=False` throughout; AC105_RESULTS_v1 "the reserve still not part of the
architecture").

---

## 1. The reference architecture, stated plainly

**World constants.** TICKS=16384, CORRUPT_TICK=8192, CORRUPT_BITS=8 (the majority of the
first 8 program bits — rule 0, the fuel rule — is flipped), DEV=512, PORTS=4,
YIELD_M=YIELD_F=64, STREAK_N=6, REGISTER_THRESHOLD=4. The world is a contact channel
yielding +32 fuel (action 0) and +64 material (action 1) against a channel mapping that
flips channel 1 on a per-condition schedule (ac100.mapping_at / ac105.CONDITIONS).

**Damage model.** Sticky SET (`|=`) at 1e-4 per replica per tick, independent streams:
the program bank (`traces[0,:126]`, stream seeded `[seed,1509]`) and the internal-state
bank 1 (description slots + pointer + CTRL word, stream seeded `[seed,1609]`). Sticky SET
means 0→1 only: a bit never self-reverses, so majority-restore cements flips (AC61) and
every paid repair is load-bearing against persistent corruption (AC67/AC71).

**Banks.** `traces` is (4, 1024, 7): bank 0 = the 126-bit program + decision state; bank 1 =
the 130-bit description (4 interchangeable slots) + 2-bit pointer + 18-bit CTRL word;
banks 2–3 and the remainder of banks 0–1 are legacy AC1/AC4 policy-table storage, present
and damageable but **not read** by the interpreter. `life` (20,), `pos` (20,2), `boundary`
(20,), energy/material/fuel (capped 128/256/64).

**Two arms.** `persistent` (no spending rule) and `persistent_budget` (allowance-42). The
candidate differs from the control by exactly one change: the reconstruction's per-tick
spend is `budget = max(0, material − 42)`, applied throughout life, a pure function of
current material and the declared constant, no challenge-time knowledge.

---

## 2. The finite component ledger

Columns: **component → function enabled → production/maintenance process → required
machinery & resources → causal evidence → unresolved dependency**.

### C1 — W (production/repair catalysts)

| | |
|---|---|
| **Realized by** | `life[:16]` — 16 sites (4 banks × 4), finite-lived (life 64, decays each tick). |
| **Function enabled** | Gates **every** paid write on the coordination/reconstruction path via the per-action capacity `_cap = min(32, 8·available_W, energy, material)`; also the parent for C/C-birth, B-birth, and the memory deposit. |
| **Production/maintenance process** | action 6 (W-birth): cost 4 M + 2 E, **requires a live W parent** (`parents = np.flatnonzero(a[bank*4:bank*4+4])`) — autocatalytic. Turnover ≈ hundreds of births per 16,384 ticks (AC91/AC95). |
| **Required machinery & resources** | live W parent (autocatalysis), 4 M + 2 E per birth, an action-6 choice by the program. |
| **Causal evidence** | AC10 (no-W ablation: no entry ever allocated, execution dies); AC91 (block W-birth → W depleted at t≈63, `_cap`→0, all reconstruction/coordination writes stop, 8/8 die with description intact at death); AC92 (interrupt at W=0 → `window_reg_writes==0` while `fw>0`). |
| **Unresolved dependency** | none — produced, autocatalytic, load-bearing. (Its initial endowment is inherited content, permitted under C4.) |

### C2 — C (energy converters)

| | |
|---|---|
| **Realized by** | `life[16:20]` — 4 sites, finite-lived (life 128). |
| **Function enabled** | passive fuel→energy conversion, 8 energy per C site per tick (the organism's entire energy income after contact). |
| **Production/maintenance process** | action 7 (C-birth): cost 4 M + 4 E, requires a live W parent. |
| **Required machinery & resources** | live W parent, 4 M + 4 E, an action-7 choice. |
| **Causal evidence** | AC10 (no-C: execution dies — energy conversion stops, energy drains); AC91/AC92 named cascade (C dies with W, conversion stops, energy drains while fuel stays full). |
| **Unresolved dependency** | none. |

### C3 — B (boundary)

| | |
|---|---|
| **Realized by** | `boundary` (20 sites, values 128…242 at acquisition, decay toward 0). |
| **Function enabled** | **retention** — particles outside the boundary export (`ac4_transport.tr.move` zeroes `life` for particles that leave the enclosure). Also observed (obs bit 8, boundary ≤ 64). |
| **Production/maintenance process** | action 8 (B-birth): cost 2 M + 2 E, requires live W as position anchor (`wp = b.pos[:16][a[:16]]`); decays each tick (B_expiry). |
| **Required machinery & resources** | live W, 2 M + 2 E, an action-8 choice. |
| **Causal evidence** | AC10: forced retention with **zero** enclosure matter and external B supply both preserve routes 8/8 — the enclosure's causal role is **retention, not mass**. |
| **Unresolved dependency** | **J4** — whether retention "constitutes the system as a concrete unity in space" (Maturana & Varela clause ii) is a modeling judgment, not a measurement. See §6. |

### C4 — Controller description (130-bit)

| | |
|---|---|
| **Realized by** | 4 interchangeable slots in bank 1 (`traces[1, 0:520]`), 130 bits each = 5 rule words (14 bits each) + 8-bit permutation + 4 bank-rule masks (9 bits each) + 4 bank-rule actions (4 bits each). 7 replicas/bit. |
| **Function enabled** | the **only** internal source of the 126-bit program: `build_program(desc)` reads the five words verbatim, derives the four bank rules from the stored permutation, masks, and actions. |
| **Production/maintenance process** | (a) **in-place repair** `reg_description_active` (majority-restore of the active slot's replicas, paid, W-catalyzed); (b) **succession**: copy active slot → successor slot, verify, switch pointer, clear old slot (see C5/C6). |
| **Required machinery & resources** | W-catalyzed `_cap` (repair); W for the succession copy; the pointer (C5) to select the active slot; the coordinator (C6) to sequence the copy→verify→switch→remove. |
| **Causal evidence** | AC80/AC85/AC86: description repair + succession holds desc 130/130; `unmaintained` degrades (desc 23–46/130) and dies 8/8; `no_repair` dies 8/8. |
| **Unresolved dependency** | **content** is inherited at development (the five words + permutation), permitted under C4 (production-vs-invention, charter §6). Content self-production is blocked (AC78) and **not required**. |

### C5 — Generation pointer (2-bit)

| | |
|---|---|
| **Realized by** | bank 1, `PTR_OFFS = [520, 521]` (2 bits × 7 replicas), majority-read. *(Charter C5 cites "offset 312–313 (AC86)"; in the AC105 architecture ac95 re-implements the layout — pointer at 520–521, description at 0–519, CTRL at 522–539. Recorded as a charter discrepancy, §7.)* |
| **Function enabled** | selects the active description slot (the one read by the decoder, repaired, and copied-from). |
| **Production/maintenance process** | `write_pointer` (paid, W-catalyzed, ≤ 2×7 replicas) at the succession switch; `reg_pointer` (majority-restore, paid) repairs minority damage. |
| **Required machinery & resources** | W-catalyzed `_cap`; the coordinator's SWITCH phase. |
| **Causal evidence** | AC86 (2-bit pointer + own POINTER_TRIGGER=2 repair; the whole-bank repair was far too slow for a 2-bit state, which drifted); AC87 (source/target **derived** from the maintained pointer). |
| **Unresolved dependency** | none — it is a vulnerable, paid-maintained component; source and target are derived from it, not stored. |

### C6 — Coordination state (MODE + W-funded timer + RIP)

| | |
|---|---|
| **Realized by** | bank 1, `CTRL_OFFS = 522…539` (18 bits × 7 replicas): bit 0 ACTIVE, bits 1–3 PHASE (5 states), bits 4–16 the W-funded unary rate-limiter timer (TIMER_BITS=13), bit 17 the RIP (reset-in-progress) bit. |
| **Function enabled** | sequences the succession state machine (copy → verify → switch → remove) and rate-limits it (SUCC_MIN_SPACING ≈ 2600 ticks via the timer). |
| **Production/maintenance process** | `write_ctrl` (MODE transition atomic, W-gated; see ac95); `reset_timer`/`increment_timer` (the W-funded counter, paid); `write_rip` (the RIP bit, atomic W-gated); `reg_ctrl` (majority-restore, paid, CTRL_TRIGGER=2). |
| **Required machinery & resources** | W for the MODE transition and the timer counter (the D3 finding: at W=0 the timer freezes — machinery-dependent); energy+material for the mode/timer writes. |
| **Causal evidence** | AC93/AC94-D2/D3/D4: multi-field transitions are atomic, the W-funded timer freezes under W-cut and resumes under machinery-only rescue; AC95-D2 moved the reset-progress flag into maintained state (RIP bit), byte-identical trajectory (observer-discard). |
| **Unresolved dependency** | **J1** — the coordinator's *mechanism* (`advance()`, the transition sequence itself) is supplied; only its *state* (C6) is internal. See §3/§7. |

### C7 — Route memory (acquired function)

| | |
|---|---|
| **Realized by** | `mem.Memory` (2 regions × 2 slots × 3 bits (valid,key,value) × 7 replicas) + per-replica `life`. |
| **Function enabled** | stores the acquired key/port entry; a contact action reads the stored port (avoiding blind search). This is the organism's **income** (fuel/material). |
| **Production/maintenance process** | **deposit** (`mem.deposit`): on a productive contact with `selected is None`, binds key/port, 21 M + 21 E, gated on `grow` and `activation[region]` and a live W parent; **renewal** (`ac12_memory.renew_alloc`): paid refresh of surviving replicas, per-slot under the allocation register. |
| **Required machinery & resources** | live W parent (deposit); interior W (renewal cap `min(32, 8·W, …)`); the program's contact action. |
| **Causal evidence** | AC7/AC8/AC15/AC18: routes acquired from the organism's own contact outcomes; AC75: erase-on-relinquishment (drop also clears the entry) makes the architecture world-accommodating under a post-development move. |
| **Unresolved dependency** | the deposit *gate* (`grow = t < DEV` in the frozen `ac9.step`, and `activation`) is externally scheduled — a route acquired after the growth window cannot re-bind (AC16's finding). This is a **process gate**, not a component; it bears on re-acquisition, not on the closure criterion per se. |

### C8 — Decision memory (allocation register + Gray-coded relinquishment streak)

| | |
|---|---|
| **Realized by** | the **free bits of the dead rule** (the bank-3 rule, mask 32, which `ac9.observe` can never match because it never sets observation bit 5), inside `traces[0,:126]`. Ten free bits total: **4-bit allocation register** (mask bits 0–3, word bits 1–4 — `resolve_offsets`) + **6-bit Gray streak** (mask bits 4/6/7/8 + action bits 1/3, word bits 5/7/8/9/11/13 — `ac96.streak_offsets`), 2 × 3-bit per-key counters. *(Charter C8 names only "relinquishment streak" as one component; the code holds **two** decision sub-states — the register flags which slots are relinquished, the streak counts failures toward the next drop. Recorded as a charter precision, §7.)* |
| **Function enabled** | decides allocation: the register read (majority ≥ 4) says "relinquished → don't renew this slot"; the Gray streak (decoded count ≥ STREAK_N=6) triggers `_drop` (write the register bit, erase the entry) and `_restore` (clear it on a productive contact). |
| **Production/maintenance process** | written **only by the organism's own outcomes**: `_drop` (register 0→1), `_restore` (1→0), `gray_streak_write` (Gray increment/reset, atomic W-gated); repaired by the paid bank-0 majority-restore (action 2); excluded from `reg_from_active` (reconstruction must not clobber decision state). |
| **Required machinery & resources** | W-catalyzed `_cap` for each Gray write (the Gray code makes every increment a 1-bit = 7-replica transition, affordable at W≥1 — AC99-D2); the program's contact outcomes as the signal. |
| **Causal evidence** | AC12/AC15/AC75/AC96/AC99/AC100: relinquishment/restore driven by realized contact outcomes, stored in vulnerable state, paid-maintained; AC104/AC105: the Gray streak + allowance-42 is the decision whose transition the budget reserves. |
| **Unresolved dependency** | **decision-state economics** — the paid streak/register writes are starved when material collapses (AC96-D2/D3, AC99's reserve was the failed attempt to fix this before the Gray code and the allowance). The allowance-42 rule (see §2 "allowance") is the current, partial answer; seed-dependent (AC104/AC105). |

### C9 — Derived 126-bit program

| | |
|---|---|
| **Realized by** | the decoded majority read of `traces[0,:126]` — 9 rules × 14-bit words (`enabled | mask<<1 | action<<10`). |
| **Function enabled** | the controller: chooses every action (contact, repair, birth, boundary) from the observation. |
| **Production/maintenance process** | **derived, not stored** — `reg_from_active` reconstructs it from the description (C4) via the generic `build_program` decode, paid (1 E + 1 M per replica), W-catalyzed, excluding the decision-state offsets. Also repaired in place by bank-0 majority-restore (action 2). |
| **Required machinery & resources** | the maintained description (C4) as the reference; W-catalyzed `_cap`; the allowance budget (candidate arm). |
| **Causal evidence** | AC79→AC80: `prog.program(priority)` (the external recipe) replaced by a generic decode that reads stored state; `rebuild == prog.program` bit-for-bit (unit test); AC87: order-preserving decode reproduces the **acquired** layout, not `prog.program` order. |
| **Unresolved dependency** | **J1/J3** — the *content* the program is rebuilt from is the inherited description (permitted); the *interpreter* that executes it is supplied (§3). C9's production edge is the reconstruction process reading C4 — it is "derived from a state that turns over", which is the charter's stated bar. |

---

### "Account for" items — not components (fixed code over vulnerable state, or supplied laws)

These are the items the task requires the ledger to account for explicitly. Per the
charter §7 note, they are **substrate operations or process logic**, not components:
they are fixed code that operates on vulnerable values; none is damaged-and-maintained
state, so none enters the closure criterion's component list.

| Item | Where | Classification | What it does |
|---|---|---|---|
| **Observation** | `ac9.observe` (9-bit) | **Substrate** (charter §5; J5) | nine host-computed threshold bits over the organism's own resources/integrity: fuel-low (bit 0), material-low (bit 1), corruption (bit 2, the self-monitoring minority count ≥ 4 over the program bank), renewal-urgent per region (bits 3–4), low-W (bit 6), low-C (bit 7), low-B (bit 8). Bit 5 is never set — this is what makes the bank-3 rule dead and frees C8's storage. |
| **Decoding / interpretation** | `ac1.decode` (majority of 7), `prog.choose` (fallthrough → action 9) | **Substrate** (charter §5 "decode format", "interpreter fallthrough"; J1) | the 14-bit word format and the rule-matching loop. Reads mutable rules, writes nothing. |
| **Reconstruction comparison** | `ac104.program_incomplete` → `ac95.build_program` | **Process logic** (fixed code over vulnerable values) | the "is the decoded program still wrong vs the description-derived target" test that arms the persistent trigger. `build_program` is the generic, order-preserving decode; `program_incomplete` is the comparison. Neither is stored/damaged/maintained. |
| **Timing** | `now` (tick clock) + `reset_timer`/`increment_timer` + `rip` | **substrate** (`now`) + **component C6** (the counter bits) | the tick clock is supplied; the **rate-limiter timer is internal state** (C6), W-funded, paid, resumable, atomic. This split is the AC93–95-D3 point: the *clock* is substrate, the *rate-limiter* is a produced, maintained constraint. |
| **Allowance computation** | `ac104.budget_rule = max(0, material − DECISION_ALLOWANCE)` | **Process logic** (fixed code; a pure function of current material + a declared constant) | the internal spending policy that reserves 42 material for the decision transition. No stored state of its own; it is the *logic* of the reconstruction process. The `DECISION_ALLOWANCE = STREAK_N × 7 = 42` is a declared world constant (substrate-level). |

---

## 3. Supplied-operations classification (per the R2 charter)

The charter §5 lists the substrate S; §7's note fixes the vocabulary. Applied here:

| Operation | Classification | Justification |
|---|---|---|
| `advance()` transition logic (copy → verify → switch → remove) | **Substrate** — *contested* (J1) | Fixed sequence machine; operates on vulnerable values (pointer, CTRL word). CLOSURE_BOUNDARY_v2 declares it substrate "a modeling choice, not a settled finding"; the AC90 review left the boundary **unresolved**. This is the single most likely source of an "unresolved" A3 verdict. |
| `prog.choose` (interpreter) | **Substrate** — *contested* (J1) | A fixed ISA reading mutable rules; the analog of a CPU. Reads, never writes. |
| `ac9.observe` (observation) | **Substrate** (J5) | Host-computed threshold bits; bears on level (c)/(d), not on closure. |
| decode format (14-bit word, majority-of-7) | **Substrate** (J2) | Format-level law. |
| write primitive (paid, 1 E + 1 M/replica, per-action cap) | **Substrate** (J2) | The price/capacity law; the *capacity term* `8·W` is what ties every paid write to the produced machinery. |
| conservation laws (`ac4.balance`) | **Substrate** | material/energy/fuel identities + in-step asserts; the world's bookkeeping. |
| damage model (sticky `|=`, 1e-4/replica/tick) | **Substrate** | the environment's corruption. |
| world constants (PORTS, YIELD, TICKS, DEV, thresholds, DECISION_ALLOWANCE) | **Substrate** | declared parameters. |
| `program_incomplete` (reconstruction comparison) | **Process logic** | fixed code, not a component; reads vulnerable state. |
| `budget_rule` (allowance) | **Process logic** | fixed code, not a component; reads current material. |
| `build_program` (generic decode) | **Process logic** (J2/J3) | the generic decoder that replaced the external recipe; reads stored description; cross-checks the permutation and stored masks/actions (returns None on inconsistency). Not itself damaged/maintained. |

**The decisive line.** Everything the organism *stores, damages, and paid-maintains* is on
C1–C9. Everything that is *fixed code operating on those values* is substrate or process
logic. The only component whose status changes the verdict is the **coordinator mechanism
(`advance()`) and the interpreter (`prog.choose`)**: if substrate, C1–C9 are assessed as
listed; if they are organism-specific functions, they are components with **no production
edge** and the criterion fails on them (J1). This audit does not pick that side.

---

## 4. Dependency graph

```
                    ┌──────────────────────────────────────────────────┐
                    │  world: tick clock, reservoirs, contact channel,  │
                    │  damage stream, conservation laws, world constants │
                    └───────────────┬──────────────────────────────────┘
                                    │ observe (substrate), contact income
                                    ▼
        ┌───────────────────────────────────────────────────────────────┐
        │  C9 derived program (traces[0,:126])  ──choose──▶ every action │
        └───────▲───────────────────────────────┬───────────────────────┘
                │ rebuild (process logic)        │ actions 6/7/8 (births)
                │ reads                          ▼
        ┌───────┴──────────┐      ┌──────────────┴──────────────────────────┐
        │ C4 description    │      │ C1 W ──parent──▶ C2 C, C3 B, deposit,    │
        │ (130-bit, slots)  │      │         _cap 8·W ──▶ every paid write    │
        └───────▲──────────┘      └──────────────▲───────────────────────────┘
                │ succession copy/verify/switch/remove       │ energy (C2 conversion)
                │ (paid, W-catalyzed)                        │
        ┌───────┴──────────┐      ┌──────────────┴───────────┐
        │ C5 pointer        │◀────▶│ C6 coordination state     │
        │ (2-bit, selects)  │      │ (MODE + W-timer + RIP)    │
        └───────────────────┘      └───────────────────────────┘
                                    ▲
                ┌───────────────────┴───────────────────────────┐
                │ C7 route memory  ◀──deposit (W-gated)── contact│
                │   ──renew_alloc──▶ (register-gated)             │
                │ C8 decision memory (register + Gray streak)     │
                │   ──_drop/_restore/gray_streak_write──▶ income  │
                └─────────────────────────────────────────────────┘
```

Production edges (what replaces what):

- **W → C, W → B, W → deposit, W → every paid write** (via `_cap`'s `8·W` term). W is
  autocatalytic (W → W). This is the mutual-constraint hub: the machinery that pays for
  maintenance is itself produced by the program (C9), which is rebuilt from the description
  (C4), which is maintained by W-catalyzed writes.
- **C4 → C9** (reconstruction, the generic decode). C9 has no independent existence; its
  production edge *is* the reconstruction process reading C4.
- **C5 → C4, C6** (the pointer selects the active slot; source/target derived from the
  pointer; the coordinator sequences the copy). C5 and C6 co-maintain each other and C4.
- **C7 ↔ C8** (route memory feeds contact outcomes; decision memory decides which routes
  are renewed/relinquished). C8's writes are paid, W-catalyzed.
- **C3 (boundary)** retains the particles that realize C1/C2 — retention, not mass (AC10).

The one *source* in the older v1 audit ("the program is external") is now closed: the
program (C9) is derived from C4, and C4 is stored, damaged, repaired, and replaced by
succession. The remaining external dependency is the **substrate** (the interpreter, the
transition logic, the observation, the decode format, the laws), which is exactly J1.

---

## 5. Evidence matrix (component × clause)

Clauses: **C1** existence (concrete damageable finite state), **C2** production/replacement
(turnover or derivation from turnover, not mere repair), **C3** within-network dependence
(p(c) depends on another component), **C4** content boundary (initial content permitted;
component must be re-made).

| Component | C1 existence | C2 production/replacement | C3 within-network dep. | C4 content boundary |
|---|---|---|---|---|
| C1 W | `life[:16]`, damageable, conserved | action 6 births; turnover ≈ hundreds/run (AC91/AC95) | W-birth needs live W parent (autocatalytic) | initial W endowment inherited; replaced endogenously |
| C2 C | `life[16:20]` | action 7 births | needs live W parent | initial C inherited; replaced endogenously |
| C3 B | `boundary` (decaying) | action 8 births, B_expiry | needs live W (position anchor) | initial B inherited; replaced endogenously |
| C4 description | bank-1 slots, damageable | succession (copy→verify→switch→remove) + repair | succession needs pointer (C5) + coordinator (C6) + W | content (5 words + perm) inherited — permitted |
| C5 pointer | bank-1 [520,521], damageable | `write_pointer` + `reg_pointer` | write is W-catalyzed | value derived from active-slot arithmetic, not inherited content |
| C6 coordination | bank-1 [522,539], damageable | `write_ctrl` + timer + `reg_ctrl` | timer/MODE writes W-gated (D3) | state, not content |
| C7 route memory | `mem.Memory`, damageable | deposit (bind) + renew (refresh) | deposit needs W parent; renew needs interior W | content (key/port) acquired from own outcomes — the one genuinely *acquired* content |
| C8 decision memory | dead-rule free bits in `traces[0]`, damageable | `_drop`/`_restore`/`gray_streak_write` + bank-0 repair | writes W-gated | initial value zero (relinquish semantics inverted) — content inherited, state produced |
| C9 program | `traces[0,:126]`, damageable | derived from C4 (reconstruction) | reconstruction needs C4 + W | content inherited (C4); replaced via derivation |

**Necessary vs optional (charter §8).** Ablation evidence (AC10, AC91, AC92) establishes
W/C/B and the program/description/repair as **necessary** (cutting them kills the
organism or halts the network's core function). Succession (C4 replacement) is the
demonstrated capability and milestone target; in-place repair alone also survives at this
horizon, so replacement is reported as the capability, and the necessary/optional line is
drawn by ablation, not prose.

---

## 6. Boundary constitution check

The boundary (C3/B) **constitutes and supports** the organization in exactly one,
code-verifiable sense: **retention**. `ac4_transport.tr.move` exports particles that leave
the enclosure; AC10's ablation shows forced retention with **zero** enclosure matter
preserves routes 8/8, so the boundary's causal role is holding the produced particles in
place, not providing mass. B is produced (action 8), decays (B_expiry), requires live W,
and is observed (obs bit 8).

Whether that retention satisfies Maturana & Varela's second clause — "constitute it as a
concrete unity in space" — is **J4**, a modeling judgment about what counts as a spatial
unity. The audit records the retention fact and the produced-boundary fact; it does not
resolve whether retention = unity. A "boundary label" reading (B does nothing causal) is
falsified by the code and by AC10; the stronger "unity in space" reading is not established
by anything in the frozen record and must not be asserted.

---

## 7. Concrete gaps (only those that could change the closure verdict)

1. **J1 — the coordinator mechanism and interpreter are supplied.** `advance()` and
   `prog.choose` are fixed code with no production edge. If the A3 assessment classifies
   them as organism-specific functions rather than substrate, the criterion fails on them
   (they would be components with no C2). This is the **decisive** gap and the most likely
   source of an "unresolved" verdict. The charter names it; this audit records it as the
   one gap whose resolution flips the verdict.

2. **J2/J3 — "format-level" is asserted, not demonstrated.** Naming the decode format and
   write primitive "generic machinery" does not by itself settle whether they are laws or
   supplied functional services (the AC90 review's point). This is a sub-case of J1.

3. **The decision-state economics are seed-dependent.** The allowance-42 rule reserves
   material for the decision transition, but the required reserve is seed-dependent (33 vs
   42 on identical-material seeds, AC104) and a reconstruction-level harm is retained on a
   diagnostic marginal economy under late corruption (5603, `fw 2 vs 0`, AC105). This is a
   *robustness* limit on the decision mechanism, not a closure-falsifying gap — the
   component is still produced and maintained — but it bounds the "self-funded decision"
   claim and must not be read as universal.

4. **The observation layer carries no perceptual content (J5).** Bears on claim levels (c)
   and (d); does not change the closure (level a) verdict. Recorded so that no level-(d)
   card silently inherits a representation claim.

No other gap in the ledger is verdict-changing. In particular, the pre-AC79 "the program is
not regenerated" gap is **closed** (C9 is derived from the maintained C4); the reserve
machinery is **disabled, not a gap**; and the deposit *gate* (grow/activation schedule) is a
re-acquisition window, not a production/closure dependency.

---

## 8. Charter discrepancies recorded (not gate-changing, but the audit is code-accurate)

- **C5 offset:** the charter says "bank 1, offset 312–313 (AC86)". The AC105 architecture
  (ac95) re-implements the layout: pointer at `PTR_OFFS=[520,521]`, description at `0:520`,
  CTRL word at `522:540`, and (in the disabled reserve lineage) `RESERVE_OFFS=540`. The
  *component identity* is unchanged; the *offset* is implementation-specific.
- **C6 shape:** the charter says "MODE/LAST". In the AC105 architecture the 18-bit CTRL word
  is MODE (ACTIVE + PHASE, bits 0–3) + the **W-funded rate-limiter timer** (bits 4–16) + the
  **RIP bit** (bit 17); the AC88 "LAST timestamp" was replaced by the W-funded counter in
  AC94-D3, and the reset-progress flag was moved into maintained state in AC95-D2.
- **C8 decomposition:** the charter names "decision register (relinquishment streak)" as one
  component. The code holds **two** decision sub-states in the dead rule's free bits: the
  4-bit allocation register (which slots are relinquished) and the 6-bit Gray-coded failure
  streak (per-key count toward the next drop). Both are damaged-and-maintained, written only
  by the organism's own outcomes, and excluded from reconstruction. A3 should treat C8 as
  this pair, not as a single register.

---

## Sources

`ac1.py, ac4.py, ac4_transport.py, ac5_program.py, ac9.py, ac9_memory.py,
ac9_priority_v2.py, ac12.py, ac12_memory.py, ac71.py, ac76.py, ac95.py, ac96.py, ac99.py,
ac99_d2.py, ac100.py, ac104.py, ac105.py`, `AC104_RESULTS_v1.md`, `AC105_PROTOCOL_v1.md`,
`AC105_RESULTS_v1.md`, `AC105_ERRATA_v1.md`, `DEFINITIONS_CHARTER_v1.md`,
`CLOSURE_BOUNDARY_v2.md`, `DEPENDENCY_AUDIT_v1.md` (superseded). Frozen-row integrity was
re-verified by the R1 predecessor (`audit_ac105.py` passes, no hash drift); this audit does
not re-simulate.
