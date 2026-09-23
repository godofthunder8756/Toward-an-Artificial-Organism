# Organizational-closure verdict v1 (K3) — the bounded verdict, with exact scope

2026-09-22. Definitional/evaluative deliverable. Applies the corrected closure criterion
(`DEFINITIONS_CHARTER_v2.md` §8) to the reference architecture at commit `db0ef2f` (AC105
body), under the accepted substrate convention. It issues the verdict; it does not run,
re-hash, or edit any frozen artifact. Supersedes the BASELINE_v2 / S1_SYNTHESIS line
"level (a) unresolved on J1" **only** in the specific sense stated in §4: K3 resolves J1.

## The verdict

**SUPPORTED — organizational closure (production closure, Maturana & Varela clause (i))
within the declared model and operating range, under the accepted substrate convention.**

Every necessary level-(a) component — **{W, C, B, description, derived program}** —
satisfies C1–C5; the maintained state — **{pointer, coordination, route memory, decision
state}** — satisfies S1–S4; and the production-dependency network is a **single
strongly-connected component with no external root**.

This is a bounded claim. The strongest wording it earns is exactly the charter's own
ceiling for level (a): "meets the finite closure criterion within the declared model and
operating range." It is **not** "autopoietic" unqualified, not "alive", not a universal
survival or optimal-allocation claim.

## 1. What is established per component (the composing evidence, named)

The C1–C5 verdict per component, resting on `DEPENDENCY_AUDIT_v2_CORRECTION.md`'s
corrected matrix and `CLOSURE_CRITERION_CONSISTENCY_v1.md` §3 (both code-traced, not
asserted):

| Component | C1 existence | C2 production/replacement | C3 within-network dep. | C4 content | C5 on a cycle | Named evidence |
| --- | --- | --- | --- | --- | --- | --- |
| **W** | `life[:16]` | action 6 birth, autocatalytic, turnover ≈766×/16,384 ticks | live W parent + program C9 | inherited endowment, replaced endogenously | C4→C9→W→C4; W→W | AC10 (no-W dies), AC91 (block W-birth → W=0 → 8/8 die, description intact at death), AC92 (W=0 interrupt) |
| **C** | `life[16:20]` | action 7 birth | live W parent + C9 | inherited, replaced | C9→C→energy→C9; W→C→energy→W | AC10 (no-C → execution dies), AC91/AC92 named cascade |
| **B** | `boundary`, decaying | action 8 birth, B_expiry | live W anchor + C9 | inherited, replaced | W→B→W (retention) | AC10 (no-B exports 8/8, dies 8/8; retention is load-bearing) |
| **description** | bank-1 slots | succession copy→verify→switch→remove (turnover) | W + pointer C5 + coordinator C6 + own content | content inherited (permitted) | C4→C9→W→C4 | AC80/85/86 (desc 130/130 held; unmaintained degrades 23–46 and dies), AC87/89 (verified_valid, cycles 6–7) |
| **program** | `traces[0,:126]` | derived from C4 (reconstruction) | C4 + W | content inherited (C4) | C4→C9 | AC79→AC80 (generic decode replaces `prog.program`, `rebuild == prog.program` bit-for-bit), AC87 (order-preserving decode) |

Maintained state S1–S4 (internalized: in-world, damage-reachable, paid-maintained,
correctness-neutral) — established, not "produced":

| Item | Named evidence |
| --- | --- |
| pointer | AC86/AC87 (2-bit pointer + own trigger; source/target derived from it) |
| coordination (MODE + W-funded timer + RIP) | AC87/88, AC93, AC94-D2/D3/D4, AC95-D2/D3 |
| route memory | AC7/AC8/AC15/AC18/AC75 (acquired from own outcomes) |
| decision state (register + Gray streak) | AC12/15/75, AC96, AC99-D2, AC100, AC104/AC105 |

**Evidence split (stated, not hidden).** AC105 (the reference run) composes *turnover,
description persistence, reconstruction completeness, succession count, and decision
operating range* in one run. Necessity-by-ablation (AC10/91/92), replacement verification
(`verified_valid`/cycles, AC87/89), timer machinery-dependence (AC95-D3), and streak
internalization (AC96/99-D2/100) are **inherited from earlier frozen versions**, not
re-tested by AC105. The correct composition — AC105 (operating range) *plus* the
AC10–AC95 ablation/turnover/verification record — is what this verdict cites; AC105 alone
is the wrong study for the production claims (`CLOSURE_CRITERION_CONSISTENCY_v1.md` §5).

## 2. The two contested judgments, resolved (not deferred)

**J1 (substrate/component boundary) — RESOLVED, substrate.** The charter names two
resolutions; the verdict must pick one rather than hide behind "the review left it open."
It resolves J1 in favour of **substrate**: `prog.choose` (interpretation) and `advance()`
(succession semantics) are retained as supplied substrate, exactly as the accepted
substrate convention (CLOSURE_BOUNDARY_v2 §5) declares. This is a modeling choice, not a
measurement — the infinite-regress argument that any self-maintenance formalization
bottoms out in a fixed substrate applies here, and no empirical experiment could settle
it. The verdict therefore carries this classification with it (charter v2 §8 and v1 §11:
"a verdict of 'supported' carries that classification"). The one qualification the
ledger records is retained: `advance()` (a prescribed copy→verify→switch→remove procedure
with a built-in verify gate) is a **larger** substrate concession than `prog.choose` (a
passive rule interpreter). Both are retained; they are not equal.

**J4 (boundary spatial unity) — UNRESOLVED, and outside the criterion's scope.** B is
produced and on the closure cycle, and its retention is load-bearing (AC10). But
retention is substitutable by substrate (kernel flag / external B matter reproduce
`keep` with zero internal boundary). So clause (i) — production closure — is met for B,
while clause (ii) — "constitute the system as a concrete unity in space" — is **not
established**. This verdict's "organizational closure" is the production-closure
criterion C1–C5 + S1–S4, which operationalizes clause (i) only. It does **not** assert
spatial unity, and it does not claim the full two-clause Maturana & Varela definition.
Full autopoiesis in that complete sense remains an unresolved, stronger claim (J4).

**J2/J3/J5** are sub-cases of J1 or of the charter's own adopted positions, and do not
change the verdict: J2 (format-level vs service) is resolved by the same substrate
convention; J3 (inherited content) is the charter's stated position (inherited content
permitted; content self-production blocked at AC78 and **not required**); J5
(observation layer) bears on levels (c)/(d), not on closure.

## 3. Exact scope (part of the verdict, not a footnote)

1. **The claim is production closure, not spatial unity and not consciousness.** Level
   (a) production closure is SUPPORTED within the declared model and operating range.
   M&V clause (ii) (spatial unity) is UNRESOLVED (J4). Levels (c)/(d)/(e) are untouched:
   level (c) representation PARTIAL (interoceptive/route content only); the level-(d)
   cognition track (AC106 maintained-belief) FALSIFIED on its own measured, structural
   grounds; level (e) NOT ASSESSABLE.
2. **The substrate is supplied, and the verdict says so.** Interpretation
   (`prog.choose`), succession semantics (`advance()`), decode format, observation,
   conservation laws, damage model, and world constants are supplied substrate. The
   verdict is conditional on and carries this classification.
3. **Bounded to the declared operating range.** AC105: seeds 5800–5807 (fresh,
   untouched), 2 histories, 2 arms (`persistent` / `persistent_budget`), 5 conditions
   (`simult`, `simult3`, `corrupt_first`, `move_first`, `late`), 160 rows = 80 matched
   comparisons, 16,384-tick horizon, all 6 gates pass. Not universal; seeds are the
   replication unit (8 independent units, not 16).
4. **Survival is a bimodality-aware lower bound** (AC68); it is not gated to a uniform
   N/N.
5. **Inherited content is permitted** (C4, charter §6); initial content supplied at
   development does not defeat closure, and content self-production is not required.

## 4. What this supersedes

BASELINE_v2.md and S1_SYNTHESIS_v1.md record level (a) as "unresolved on J1". This
verdict supersedes that status **in exactly one respect**: J1 is now resolved (substrate,
per the accepted convention), so level (a) moves from "unresolved on J1" to "supported
within the declared model and operating range, under the substrate convention." The
BASELINE_v2 levels (b)/(c)/(d)/(e) statuses are unchanged, and no frozen artifact is
touched. K9 (synthesis) should carry this update into the authoritative status.

## 5. Robustness limits are NOT redesign requirements

Three limits are on the record and must not be converted into automatic
architecture-redesign mandates:

- **Seed-dependent decision-state economics** — allowance-42 rescues 5804 (new marginal
  priority) and retains a reconstruction-level harm on diagnostic 5603 under `late`. This
  bounds the level-(b) decision claim; it does not bear on whether any component is
  produced (charter v2 §9, the "decision-state economics" reclassification).
- **The `move_first` boundary** — 5802 dies under both arms via the re-acquisition path,
  independent of the spending rule. An operating-range boundary, not a closure gap.
- **Bimodality** — survival splits by seed (AC68); reported as a lower bound.

None of these is a production/closure failure; all are robustness/operating-range limits
reported separately.

## 6. No unresolved empirical dependency remains

The verdict rests on (a) C1–C5 per component and S1–S4 per maintained-state item, each
established in the frozen record and named in §1; (b) the substrate resolution of J1,
which is a modeling judgment the accepted convention settles (not an empirical gap);
and (c) J4, which is outside the criterion's scope. **No empirical dependency that could
change the verdict is left unassessed, so no child experiment is created.** The one item
whose resolution flips the verdict (J1) is resolved here by the convention, not by a
measurement, and is not empirically settleable (infinite regress).

## 7. Publication independence (stated plainly)

Level (b) adaptive autonomy is ESTABLISHED and publishable as such, independent of any
reviewer permission and independent of this closure verdict. Level (a) closure is
publishable only with its exact scope attached: "meets the finite closure criterion
within the declared model and operating range, under the accepted substrate convention,"
with J4 (spatial unity) flagged unresolved. Neither claim is "alive" or "autopoietic"
unqualified.
