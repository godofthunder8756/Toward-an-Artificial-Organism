# Autopoiesis assessment v1 — the A3 integrated closure verdict

2026-09-22. A3 deliverable. This issues the verdict the assessment track exists to
produce: *against the R2-frozen criterion (`DEFINITIONS_CHARTER_v1.md` §8, applied
unchanged), does the reference architecture (AC105, commit `8f0218a`) achieve
organizational closure?* It reads A1's ledger (`DEPENDENCY_AUDIT_v2.md`), A2's gap
analysis (`GAP_ANALYSIS_v1.md`), the settled boundary (`CLOSURE_BOUNDARY_v2.md`), and the
R2 charter. It is a derived document; it is not hashed into any study's
`pre_run_snapshot.json`, and it runs nothing.

---

## Verdict

**UNRESOLVED** — the fourth outcome of the frozen criterion (charter §8). The criterion's
`unresolved` clause is triggered verbatim: *a §9 modeling judgment is decisive, the
verdict changes with how that judgment is resolved, and the charter does not pick a side.*

The decisive judgment is **J1** — whether the coordinator mechanism (`advance()`, the fixed
copy → verify → switch → remove sequence) and the interpreter (`prog.choose`, the fixed
rule-matching loop) are acceptable generic substrate, or undeclared coordinators that
assume a functional service without demonstrating its production. J1 is decisive: resolved
one way, the criterion is met component-by-component; resolved the other way, the
organization fails on its two most central constraints. It is unpicked: the charter §9
names J1 "the most likely source of an 'unresolved' verdict," and the AC90 review
explicitly left the boundary unresolved — it did not affirm the substrate reading.

This is **not** "we have not run enough experiments." A2 establishes that no experiment can
settle J1 (the fixed-control-flow question is an infinite regress, not an empirical gap),
and that the decidable half of J1 is already frozen and positive. The verdict is
unresolved because a modeling judgment the criterion itself designates as decisive remains
genuinely contested, not because any empirical fact is missing.

---

## 1. The criterion, applied unchanged

Charter §8 freezes a finite component list **C = {C1…C9}**, a supplied substrate **S** (§5,
which includes `advance()`, `prog.choose`, `ac9.observe`, the decode format, the write
primitive, the conservation laws, the damage model, and the world constants), and four
clauses per component:

- **C1 Existence** — concrete, damageable, finite state in the simulated world.
- **C2 Production/replacement** — a process, funded by self-acquired resources, produces or
  replaces c during ordinary operation (turnover, or derivation from a state that turns
  over). Mere repair is not production.
- **C3 Within-network dependence** — p(c) depends on at least one other component.
- **C4 Content boundary** — initial content may be inherited; the component itself must be
  re-made.

The verdict mapping is: **supported** = every c ∈ C meets C1–C4 *under the §9 substrate
classification*; **partially supported** = a named proper subset meets them; **falsified** =
a necessary component fails a clause *with no §9 judgment that could reclassify it*;
**unresolved** = a §9 judgment is decisive and unpicked.

Two discipline rules of the criterion apply here and are respected verbatim:

1. **The component list is frozen.** No new component may be added after assessment began
   (§8). So the assessment does **not** reclassify `advance()`/`prog.choose` as components
   to make them fail; that would be re-drawing the boundary, which the criterion forbids.
   The `unresolved` verdict does not require it — J1 is decisive *as a classification of
   the frozen substrate list S*, which the charter itself names as contested.
2. **The criterion was not redefined to fit the implementation.** The `unresolved` clause
   is the criterion's own fourth outcome; the charter anticipated exactly this result for
   exactly this reason.

---

## 2. What the composing evidence establishes (the picture under the substrate reading)

If J1 is resolved as substrate (the project's §5 stated choice, inherited from
`CLOSURE_BOUNDARY_v2`), then **every component C1–C9 meets C1–C4**, with composing evidence
as follows. This is the strongest picture the evidence licenses, and it is what a
"supported (bounded to the substrate classification)" verdict would rest on. It is named
here because the acceptance criteria require the composing evidence to be named, and
because the verdict must show precisely where "supported" stops and "unresolved" begins.

| Component | C1 existence | C2 production/replacement | C3 within-network dep. | Composing evidence (frozen) |
|---|---|---|---|---|
| C1 W | `life[:16]`, damageable, conserved | action 6 births; turnover ≈ hundreds/run | autocatalytic (needs live W parent) | AC10 (no-W → no entry, execution dies); AC91 (block W-birth → W depleted t≈63, `_cap`→0, all writes stop, 8/8 die with desc intact at death); AC92 (W=0 → `window_reg_writes==0` while `fw>0`) |
| C2 C | `life[16:20]` | action 7 births | needs live W parent | AC10 (no-C → conversion stops, energy drains); AC91/AC92 (named C cascade) |
| C3 B | `boundary`, decaying | action 8 births + B_expiry | needs live W (position anchor) | AC10 (zero-enclosure + external B preserve routes 8/8 → retention, not mass) |
| C4 description | bank-1 slots, damageable | succession (copy→verify→switch→remove) + repair | needs pointer (C5) + coordinator (C6) + W | AC80/AC85/AC86/AC87 (succession holds desc 130/130; `unmaintained` degrades 23–46/130, dies 8/8; `no_repair` dies 8/8) |
| C5 pointer | bank-1 [520,521], damageable | `write_pointer` + `reg_pointer` | W-catalyzed | AC86 (2-bit + own POINTER_TRIGGER=2); AC87 (source/target derived from maintained pointer) |
| C6 coordination state | bank-1 [522,539], damageable | `write_ctrl`/timer/`write_rip` + `reg_ctrl` | timer/MODE writes W-gated | AC93/AC94-D2/D3/D4 (atomic transitions, W-funded timer freezes at W=0); AC95-D2/D3/D4 (RIP bit in maintained state, observer-discard) |
| C7 route memory | `mem.Memory`, damageable | deposit (bind) + renew | deposit needs W parent; renew needs interior W | AC7/AC8/AC15/AC18 (routes acquired from own contact outcomes); AC75 (erase-on-relinquishment) |
| C8 decision memory | dead-rule free bits in `traces[0]`, damageable | `_drop`/`_restore`/`gray_streak_write` + bank-0 repair | W-gated Gray writes | AC12/AC15/AC75/AC96/AC99/AC100/AC104/AC105 (Gray-coded relinquishment streak + allowance-42) |
| C9 program | `traces[0,:126]`, damageable | derived from C4 (reconstruction) | reconstruction needs C4 + W | AC79→AC80 (generic decode replaces external recipe); AC85 (masks/actions stored); AC87 (order-preserving decode reproduces the acquired layout) |

The load-bearing structural fact behind this table, verified against the frozen code
during this assessment (not merely inherited from A1): `ac105.py` builds its step from
`ac95.ARM_PARTS['gated']` (`gate_ctrl=True, atomic_switch=True, timer_maintained=True`),
and every coordinator *write* (`write_ctrl`, `write_pointer`, `commit_switch`,
`reset_timer`, `increment_timer`, `write_rip`) is W-gated through `_cap = min(32,
8·available_W, energy, material)`; the *mechanism* that sequences them (`ac95.advance`) and
the *interpreter* that reads the rules (`ac5_program.choose`) are fixed Python functions
with no production edge. That split — internalized and W-gated *state* vs supplied and
unproduced *mechanism* — is exactly J1.

---

## 3. Why the verdict is "unresolved" and not "supported" or "falsified"

**Not "falsified."** The charter's `falsified` outcome requires a necessary component to
fail a clause "with no §9 judgment that could reclassify it." The only clause any part of
the organization fails is C2 on `advance()`/`prog.choose` *if and only if* J1 is resolved
against the substrate reading. That failure is therefore contingent on a contested
judgment, not independent of it — so `falsified` is excluded by the criterion's own text.

**Not "partially supported."** Under the substrate reading every one of C1–C9 meets
C1–C4 (table above); there is no named proper subset with a missing clause. Under the
organism-specific reading the components that would fail are not on the frozen list at all
(adding them is forbidden), so that reading is a charter-defect hypothesis (§12), not a
"partial support" finding.

**Not "supported" (bounded to the substrate classification), and this is the judgment
call.** Issuing `supported` requires adopting the §9 substrate classification for the
coordinator mechanism and interpreter — the very classification the AC90 review declined
to affirm and the charter §9 declines to make. A3 declines to make it, for three reasons:

1. **The charter directs it.** §9 names J1 "the most likely source of an 'unresolved'
   verdict" and states plainly that the charter cannot settle it. The §5 "stated choice" is
   the project's earlier declaration, which §9 then characterizes as "a modeling choice,
   not a settled finding," and which the review "did not affirm."
2. **The review did not affirm it.** The single most authoritative external epistemic
   check the project has — the AC90 review — explicitly left the boundary unresolved. A
   "supported" verdict would require this assessment to affirm what the review refused to
   affirm, on no new evidence (A2 established that no experiment can add evidence on the
   undecidable half).
3. **The philosophical substance is not peripheral.** Montévil & Mossio's closure of
   constraints, the operationalization the charter adopts (§2), is precisely the claim that
   *the constraints that hold the organization together are themselves produced*. The
   coordinator's transition logic and the interpreter are the two constraints that hold
   this organization together — one sequences every succession, the other turns the
   program into every action. Whether fixed code may count as "supplied substrate" at that
   exact locus is the closure question, not a side issue; resolving it unilaterally in the
   substrate direction would be the overclaim the track exists to prevent.

The verdict therefore stays at the boundary the charter itself draws: the architecture is
**one contested modeling judgment short of a defensible "supported (bounded)" claim**, and
that judgment is one the charter declines to make and the review left open.

---

## 4. The closure / robustness distinction

The criterion's `unresolved` verdict concerns **organizational closure** only. It must not
be read as a verdict on the architecture's robustness, and the two are separated here as
the acceptance criteria require:

- **Closure (what is at stake):** are the components realizing the organization produced
  and replaced, with within-network dependence, from self-acquired resources? *That* is
  what J1 leaves undecidable.
- **Robustness (separate, and not in question):** the coordinator-state maintenance (C6) is
  a state-cleanliness contrast, not a survival claim (AC87 G6); the decision-state
  economics are seed-dependent (allowance 33 vs 42 on identical-material seeds, AC104; a
  reconstruction-level harm retained on a marginal economy under late corruption, AC105);
  survival is a bimodality-aware lower bound (AC39/AC68); and route-holding is a lower
  bound (the AC89 finals did not exercise AC83's adversarial renewal-last priority). None
  of these is closure-falsifying — each is a bound on the level-(b) adaptive claim or on
  survival, not on whether a necessary component is produced. A1 classifies them correctly
  and A2 confirms none is verdict-changing.

## 5. The necessary / optional distinction

Drawn by ablation (AC10, AC91, AC92), not by prose:

- **Necessary** (cutting them breaks the organization): W (C1), C (C2), B (C3), the
  description and its repair (C4), the pointer (C5, needed to select the active slot), the
  derived program (C9), and the route memory (C7, the income path). These are produced or
  derived from produced state, with within-network dependence — the positive half of the
  closure claim.
- **Optional / capability (demonstrated, not the survival load-bearer at this horizon):**
  recipe *succession* (replacement of C4's storage) — in-place repair alone also survives,
  so replacement is the demonstrated capability and milestone target, not the survival
  load-bearer in isolation. This is a *necessary-property* finding, not a claim that
  replacement is required for survival at the 16,384-tick horizon.
- **Optional / robustness:** coordinator-state maintenance (C6 cleanliness, AC87 G6). A
  state-cleanliness contrast, reported and not folded into closure.

## 6. Bounds and scope of every statement above

The verdict, and the strongest wording it licenses, are bounded exactly as the charter §11
requires: the declared model and operating range (seeds 5800–5807, 2 histories, 80 matched
arm-pairs, 16,384 ticks, the AC105 schedule/priorities/moves); seeds are the replication
unit (N seeds × 2 histories = N units, not 2N); survival is a bimodality-aware lower bound;
oracle/scaffold controls (protected copy, machinery-only re-seed rescues) are labelled
EXTERNAL and never counted as autonomous. The claim under assessment is level (a) —
autopoietic organization — and the charter's strongest wording for it ("meets the finite
closure criterion within the declared model and operating range") is **not** earned today,
because the criterion's `unresolved` clause, not its `supported` clause, is what the
evidence triggers.

## 7. What would change the verdict

- **A resolution of J1** — but A2 established this is a modeling judgment no experiment can
  settle (the infinite-regress argument), so it is resolved by argument/review, not by a
  new study. If a future review affirms the substrate reading, the verdict would become
  "supported (bounded to the substrate classification)" on the composing evidence in §2,
  unchanged. If it affirms the organism-specific reading, the fix is a **v2 charter** (§12)
  re-drawing the component list to include the coordinator mechanism and interpreter —
  which then fail C2 — and the verdict on that criterion would be its own assessment.
- **The closure/robustness, necessary/optional, and composing-evidence distinctions made
  here are stable** under either resolution and carry forward unchanged.

## 8. Disposition

No frozen study is re-run, re-hashed, or edited. This document is derived; the frozen
runners, protocols, results dirs, and hashes are untouched. The verdict is `unresolved`,
and the single, precisely-named reason is J1 — a decisive modeling judgment the criterion
designates as decisive, the charter declines to make, and the AC90 review left open.

## Sources

`DEFINITIONS_CHARTER_v1.md` (§2, §5, §7, §8, §9, §11, §12), `CLOSURE_BOUNDARY_v2.md` (Q1),
`DEPENDENCY_AUDIT_v2.md` (A1 ledger, §5 evidence matrix, §7 gaps), `GAP_ANALYSIS_v1.md`
(A2, §3.1/§4), `BASELINE_v1.md`, `ac105.py` (uses `ac95.ARM_PARTS['gated']`), `ac95.py`
(ARM_PARTS, `advance`, `write_ctrl`, `write_pointer`, `commit_switch`, `reset_timer`,
`increment_timer`, `write_rip`), `ac5_program.py` (`choose`). Frozen-row integrity
re-verified by the R1 predecessor (`audit_ac105.py` passes); this assessment re-simulates
nothing.
