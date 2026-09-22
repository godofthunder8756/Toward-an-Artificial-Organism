# Gap analysis v1 — is there a decisive experiment for each A1 dependency? (A2 deliverable)

2026-09-22. A2 deliverable. This answers the A2 question — *for each unresolved
dependency found by A1, is there a decisive experiment that distinguishes loss of a claimed
organizational function from general starvation, missing observations, or added costs?* —
and records the disposition of every gap. It is the input A3 reads before issuing its
verdict, alongside A1's ledger (`DEPENDENCY_AUDIT_v2.md`) and the R2 charter
(`DEFINITIONS_CHARTER_v1.md`).

**Conclusion: no decisive experiment is missing.** Every gap A1 lists is either
(a) already resolved by a frozen experiment, (b) a modeling judgment that no experiment can
resolve, or (c) a robustness/level limit outside the closure track. No new child card is
created.

---

## 1. The test applied

A child experiment is warranted only if it meets all of:

1. **Verdict-changing.** The gap must be one that could change the A3 closure verdict (the
   A2 rationale: "only concrete gaps that could change the A3 closure verdict justify new
   experiments"). A robustness or level-(b)/(c)/(d) limit is out of scope for this track.
2. **Empirically decidable.** The gap must be a question an experiment can settle — i.e.
   there is a *selective intervention* whose outcome differs between "loss of the claimed
   function" and "starvation / missing observation / added cost". A definitional boundary
   is not an experiment's subject.
3. **Not already answered.** If a frozen experiment already isolated the function from those
   confounds, a new study would only re-run it.

Each A1 gap is checked against all three. The disposition per gap is one of: **card** (a
decisive experiment exists and is not yet run) or **no card** (with the reason).

---

## 2. Disposition table

| Gap (A1 §7) | Claimed function at stake | Decidable? | Already answered? | Verdict-changing? | Disposition |
|---|---|---|---|---|---|
| J1 — coordinator mechanism `advance()` + interpreter `prog.choose` supplied | that the coordinator's sequencing and the rule interpreter are produced/replaced organism-specific functions | partly — the *enactment* (transition writes) is; the *control flow / ISA* is not (infinite regress) | the decidable half is | yes | **no card** — see §3.1 |
| J2/J3 — "format-level" asserted, not demonstrated | that decode format + write primitive are generic laws, not supplied services | partly — genericness is decidable; "law vs service" is not | the decidable half is (AC85/AC87) | sub-case of J1 | **no card** — §3.2 |
| Decision-state economics seed-dependent (allowance 33 vs 42; 5603 reconstruction-harm) | that the self-funded decision is seed-independent / universal | yes, but a robustness/operating-range question, not a function-loss question | mapped (AC104/AC105) | no (A1: "not closure-falsifying") | **no card** — §3.3 |
| J5 — no perceptual content in the observation layer | that the organism represents an external world | no (charter's adopted position, level c/d) | n/a | no (bears on level c/d, not closure) | **no card** — §3.4 |
| J4 — boundary "unity in space" (A1 §6, not a §7 verdict gap) | that the boundary constitutes the system as a concrete unity | no (judgment about what counts as a unity) | n/a | A1 did not list it as verdict-changing | **no card** — §3.5 |

---

## 3. Per-gap reasoning

### 3.1 J1 — the coordinator mechanism and interpreter are supplied (the decisive gap)

**What the gap is.** `advance()` (the fixed succession sequence copy → verify → switch →
remove) and `prog.choose` (the fixed rule-matching interpreter) are fixed code with no
production edge. If A3 classifies them as organism-specific functions rather than substrate,
they are components with no C2 and the criterion fails on them; if substrate, C1–C9 are
assessed as listed.

**The gap splits into a decidable half and an undecidable half, and they must not be
conflated.**

*Decidable half — is the coordinator's operation production-dependent?* This is answered
**yes, by frozen experiments**. The AC105 reference architecture runs the `gated` arm
(`ac95.ARM_PARTS['gated']`, `gate_ctrl=True, atomic_switch=True, timer_maintained=True`),
in which every coordinator *write* is W-gated (`_cap = min(32, 8·available_W, energy,
material)`):

- the MODE transition (`write_ctrl`, bits 0–3) is atomic and **refused whole at W = 0**
  (ac95.py `write_ctrl`, `gate=True` branch);
- the rate-limiter timer is a **W-funded unary counter** (`reset_timer` / `increment_timer`
  both write 0 at W = 0 — the counter freezes);
- the reset-in-progress (RIP) bit is a **W-gated** atomic write (`write_rip`);
- the pointer + SWITCH→REMOVE commit is one **atomic W-gated** write (`commit_switch`).

The interruption-and-rescue and observer-discard tests that isolate this from the three
confounds were already run and frozen: AC94-D3/D4 and AC95-D3/D4 block W production (a
birth-block, no added cost) → the timer freezes and the succession cannot arm while the
organism survives with content intact (not starvation, not missing observation, not cost);
a machinery-only W re-seed (labelled EXTERNAL, no content supplied) resumes it; and ordinary
operation turns W over ~766× per 16,384 ticks (AC91). The single-step pin (a transition
write that writes 0 at W = 0 while the organism is otherwise solvent) is the clean
isolation the A2 test asks for. Re-running it would duplicate a freeze.

*Undecidable half — is the fixed control flow (which phase follows which) and the rule
interpreter (the ISA) a component or a law?* This is **not empirically decidable**. Making
the phase-sequence or the rule-matching loop itself a produced component would require a
produced component that *selects* the next phase or *executes* the match — whose own
selection/execution is fixed code — ad infinitum. The R2 charter §5 and
CLOSURE_BOUNDARY_v2 §Q1 state this explicitly ("a mechanism that rewrote its own transition
logic would need a second-order transition logic"); the AC90 review left the boundary
unresolved *because* no code fact settles it. The two readings (fixed transition code =
law, or = an undeclared coordinator) are consistent with every code fact; they differ only
on the definitional line. An experiment cannot distinguish them because the question "is
fixed code a law or a service?" is not an empirical question — it is exactly the §9 J1
modeling judgment the charter names and declines to resolve.

**Disposition: no card.** The decidable half is closed by AC93–AC95; the undecidable half
is a modeling judgment. A new experiment would either re-run the W-gating freeze or chase
the infinite regress. Both are forbidden by the A2 rationale ("do not add a new component
or study after every failed seed"; AC90: "add a distinct coordinator component only if
needed" — and it is not needed, because the coordinator's state, timer, and every transition
write are already internalized and W-gated).

### 3.2 J2/J3 — "format-level" is asserted, not demonstrated

**What the gap is.** Naming the decode format and write primitive "generic machinery" does
not by itself settle whether they are laws or host-supplied functional services (the AC90
review's point).

**The decidable half is answered.** The question a code fact *can* settle — is the decoder
generic over syntax rather than knowing the correct policy? — is closed by AC85/AC87: the
generic `build_program` reads the stored masks/actions and cross-checks them against the
permutation, returning `None` on inconsistency; a flipped-but-syntactically-valid mask/action
decodes *faithfully* (the decoder does not reject a wrong-but-valid controller). The
remaining "law vs service" question is the **same modeling judgment as J1** (the
format-level boundary) and fails the "empirically decidable" test for the same
infinite-regress reason.

**Disposition: no card.** Folded into J1; its decidable half is closed, its residual is a
modeling judgment.

### 3.3 Decision-state economics are seed-dependent

**What the gap is.** The allowance-42 rule reserves material for the decision transition,
but the required reserve is seed-dependent (33 vs 42 on two seeds with identical material,
AC104) and a reconstruction-level harm is retained on a diagnostic marginal economy under
late corruption (5603, `fw 2 vs 0`, AC105).

**Why no card.** A1 classifies this as a *robustness* limit, not a closure-falsifying gap:
"the component is still produced and maintained." It bounds the level-(b) "self-funded
decision" claim; it does not bear on whether C8 satisfies C1–C4 (it is produced, damaged,
and paid-maintained regardless of the allowance's universality). It therefore fails the
A2 **verdict-changing** test. AC104 and AC105 already mapped the operating range (the
33-vs-42 seed dependence and the 5603 harm are recorded findings, retained not tuned), so a
further seed sweep would be a robustness mapping, not "a decisive experiment distinguishing
function-loss from starvation" — the function (the decision) is not being lost in these
cases, only its funding margin varying.

**Disposition: no card.** If a level-(b) robustness claim is ever wanted, that is a
separate (C-track) question, not an A2 closure-gap experiment. Recorded here so it is not
silently dropped and not silently promoted into the closure track.

### 3.4 J5 — no perceptual content in the observation layer

**What the gap is.** The nine observation bits are host-computed thresholds over the
organism's own resources/integrity; there is no content-bearing representation of an
external world.

**Why no card.** This bears on claim levels (c)/(d), not on closure (level a). A1 records
it "so that no level-(d) card silently inherits a representation claim." It fails the
**verdict-changing** test, and the charter (§9 J5) adopts the "no perceptual content"
position as its stated position (a definitional stance, not a measurement). It is the
R3/C1 (consciousness-roadmap) track's concern, not A2's.

**Disposition: no card.** Out of scope for the closure track; already recorded by A1 and the
charter.

### 3.5 J4 — the boundary as "concrete unity in space" (A1 §6; not a §7 verdict gap)

**What it is.** Whether B's retention "constitutes the system as a unity in space"
(Maturana & Varela clause ii) or merely retains particles.

**Why no card.** A1 did not list it among the §7 verdict-changing gaps, and the charter §9
J4 states it is "a judgment about what counts as a unity, not a measurement." The code facts
(retention is real and load-bearing, AC10; B is produced and decays) are established; the
"unity" reading is a modeling judgment no experiment can settle. Recorded for completeness,
not as a gap requiring an experiment.

---

## 4. What this means for the A3 verdict

A2's finding is that **the only verdict-changing gap (J1) is a modeling judgment, not an
empirical gap.** Concretely:

- The closure criterion (charter §8) is assessed over C1–C9 under the §9 J1 substrate
  classification. The decidable production-dependency facts behind J1 are already frozen
  (AC91–AC95: the coordinator's state, timer, and every transition write are W-gated and
  produced-maintained; the interpreter's *content* — the program C9 — is derived from the
  maintained description C4). What remains unproduced is the fixed control flow and the
  fixed ISA, and that is exactly the format-level boundary the charter declares as substrate
  (§5) while the AC90 review left "unresolved."
- Because J1 is a §9 modeling judgment that the charter does not pick a side on, the honest
  verdict mapping (charter §8) is **"unresolved"** if A3 declines to adopt the substrate
  reading, or **"supported" bounded to the substrate classification** if A3 adopts it
  (following CLOSURE_BOUNDARY_v2's declared choice). It is **not "falsified"**: the
  "falsified" verdict requires a component that fails a clause "with no contested judgment
  (§9) that could reclassify it," and J1 is precisely such a contested judgment.
- The remaining gaps (decision economics, J5, J4) are not closure-verdict-changing; A3
  should carry them as robustness/level bounds, not as missing experiments.

No child card is created because none of the three decisive-experiment conditions (§1) is
met by any A1 gap. This card is therefore completed with this written justification, per its
acceptance criterion.

---

## Sources

`DEPENDENCY_AUDIT_v2.md`, `DEFINITIONS_CHARTER_v1.md` (§5, §8, §9), `CLOSURE_BOUNDARY_v2.md`
(Q1), `AC105_RESULTS_v1.md`, `AC105_PROTOCOL_v1.md`, `AC104_RESULTS_v1.md`, `ac95.py`
(ARM_PARTS `gated`, `write_ctrl`, `reset_timer`, `increment_timer`, `write_rip`,
`commit_switch`), `ac105.py` (uses `ac95.ARM_PARTS['gated']`), `ac104.py`, `ac85.py`,
`ac87.py`, `ac91.py`, `ac92.py`, and the AC93/AC94/AC95-D2/D3/D4 references.
