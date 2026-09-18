# Closure boundary v2: the settled boundary for the whole organization

Consolidated 2026-09-18, from `AC87_RESULTS_v1.md`, `AC88_RESULTS_v1.md`, `AC89_RESULTS_v1.md`
and their protocols. This supersedes `CLOSURE_BOUNDARY_v1.md` (the AC67/AC68-era boundary, which
AC71 cites by name for its "three closure gaps" and which is preserved unchanged). The internal-state
milestone (AC87) is reached; this document settles the boundary of what that milestone claims and
what it does not, so that the definition of success stops moving.

## Accepted milestone statement

> A simulated organism repeatedly replaces its internally stored controller description (the
> 130-bit description: five rule words, an 8-bit permutation, four bank-rule masks and four
> bank-rule actions) using damageable, resource-maintained coordination state, while surviving a
> corruption-and-route-change challenge across the tested cohort — on both the temporally separated
> schedule (AC87) and the simultaneous, adversarial-priority schedule (AC89).

Qualifiers, stated plainly:

- "Replaces" is turnover of the recipe-bearing storage (a successor copy is verified valid and
  equal to the source, then the pointer switches and the old slot clears), not discovery of a
  better recipe and not content self-production (AC78 still blocked).
- "Survives" is the observed count (8/8 finals, 16/16 engineering on both AC87 and AC89), reported
  as a bimodality-aware lower bound — the AC68 W/C collapse is seed-family dependent (AC39's
  lesson), so it is not a guarantee for every seed family.
- The coordination state is damageable and resource-maintained; the coordinator's *mechanism* (its
  transition logic) is supplied. See below.

## Question 1: the generic substrate vs the organism-specific components

### The generic substrate (supplied, format-level, not to be internalized)

These fixed operations are the laws of the world. They are supplied by the simulator and are not
produced, repaired, or replaced by the organism; nothing in the arc claims otherwise.

| Substrate operation | What it is |
| --- | --- |
| `advance()` transition logic | the succession state machine's fixed sequence copy -> verify -> switch -> remove |
| tick clock | `now`, the host-supplied counter the step reads |
| decode format | the 14-bit word `enabled | mask<<1 | action<<10`, read by majority of 7 replicas |
| write-primitive format | paid write, 1 energy + 1 material per replica, at the frozen per-action cap |
| interpreter fallthrough | `prog.choose` returns action 9 when no rule's mask matches the observation |
| conservation laws | `ac4.balance` (the material/energy/fuel identities and their in-step asserts) |
| observation function | `ac9.observe` (the 9-bit observation the program bank reads) |
| damage model | sticky SET (`|=`) at 1e-4 per replica per tick, independent streams per bank |
| world constants | PORTS, YIELD, TICKS, DEV, REGISTER_THRESHOLD, the trigger constants |

### The organism-specific, produced/replaced components

These are inside the organization: they live in vulnerable state, are damaged, and are
maintained/replaced by paid machinery the organism funds.

- **The 130-bit description** (five rule words + 8-bit permutation + four bank-rule masks +
  four bank-rule actions). It is stored in interchangeable slots, read (not derived) by the generic
  decode, and replaced by succession. This is the component the milestone's verb "replaces" names.
- **The coordinator's working STATE** (active / phase / last-start, 18 bits). It lives in the same
  vulnerable, damage-streamed, paid-maintained substrate as the description and pointer. Source and
  target are *not* stored — they are derived from the maintained generation pointer.
- **The produced constituents** W/C/B and the acquired 126-bit program, which the description's
  production words and bank rules specify.

### What AC87 did and did not internalize — stated plainly

AC87 internalizes the coordinator's working **state**, NOT the coordinator **mechanism**. The
transition logic (`advance()`'s copy -> verify -> switch -> remove) is supplied substrate, exactly as
`prog.choose` is the supplied interpreter for the program bank. The organism stores and maintains
the *values* the state machine runs on; it does not produce the state machine.

Demanding that the mechanism also self-rewrite is an **infinite regress, not a scientific target**:
a mechanism that rewrote its own transition logic would need a second-order transition logic to
coordinate that rewrite, which would in turn need internalizing, ad infinitum. Every formalization
of "self-maintenance" bottoms out in a fixed substrate at some level; the question is only where the
boundary is drawn, and drawing it at the format level (the same level as the interpreter and the
conservation laws) is the defensible choice.

**The fixed transition logic is declared acceptable generic substrate — a modeling choice, not a settled finding. (The review did not affirm this: it explicitly left the boundary unresolved.)** It is format-level machinery operating on vulnerable values, not organism-specific
content. The organism-specific content is the description and the working state, and those are what
are internalized, maintained, and replaced.

## Question 2: necessary maintenance vs optional capability

Two senses must be kept apart: what is load-bearing for *organizational continuity* (cut it and the
organism dies), and what is the *demonstrated capability* the milestone claims.

### Necessary (load-bearing for organizational continuity)

1. **Description maintenance + reconstruction.** The in-place repair (`reg_description`,
   `reg_pointer`) and the re-instantiation (`reg_from_active`) that keep the 130-bit description
   and the derived program correct. Cutting all of it — `unmaintained` — degrades the description
   to 55-74/130 and kills the organism 0/8; cutting the loop — `no_repair` — kills 0/8 (deaths
   514-912). These are the paid, W-catalyzed operations the organism funds out of its own economy.
2. **Recipe replacement (succession).** The replaceable-storage turnover itself: the successor is
   copied, verified (syntactically valid AND equal to the source), the pointer switches, the old
   slot clears. This is what the milestone's central verb "replaces" stands on, and it is verified
   in every survivor (6-7 cycles, `verified_valid == 1`, `target_correct == 1`).
   *Precision, not hidden:* in-place repair alone (`repair` arm, succession off) also survives 8/8
   with the description intact at this horizon, so replacement is the demonstrated capability and
   the milestone's target, not the survival load-bearer in isolation. What is load-bearing for
   survival is the maintenance machinery as a whole; what is load-bearing for the *claim* is that
   replacement actually occurs and is verified.

### Optional (capability / robustness, not load-bearing)

3. **Coordinator-state maintenance (G6).** Cutting it — `ctrl_unmaintained` — still permits
   succession (5-7 cycles) and survival (8/8). The succession is robust to its own state's
   degradation because source and target are derived from the maintained pointer; only the state's
   *cleanliness* degrades (minority 6-10 vs 0-1). This is a state-cleanliness contrast, not a
   survival claim.

**The goal claim rests on (1) and (2), not on (3).** The milestone statement above is supported by
the necessary dependencies: the description is maintained and the recipe is repeatedly replaced,
through damageable, resource-maintained coordination state. The coordinator-state maintenance is
reported as a robustness finding and does not carry the claim.

## The limit set (what the boundary does not claim)

- No recovery from catastrophic recipe-content corruption: a successor is a copy of the active
  slot's majority, so a majority-flipped description bit would be copied faithfully (AC61 one level
  down).
- The four bank rules are still four bank rules: what is internalized is their mask/action *content*
  (storage + maintenance + replacement), not the fact that four bank rules exist (format).
- No content self-production (AC78 blocked). The priority is still acquired at development, not
  produced by the organism's own lifetime.
- Survival is a bimodality-aware lower bound, not a per-seed-family guarantee.
- Nothing here claims autopoiesis, organismal autonomy in the strong sense, or subjectivity. The
  controller's *information* is internalized, maintained, and replaced; the controller's
  *interpreter* and the succession *mechanism* remain supplied substrate.

## How AC89 folds in

AC89 closes AC87's two recorded caveats with no new machinery, so they are limits resolved, not
limits papered over:

- The adversarial priority `[3,0,2,1]` (bank-1 renewal rule last) — AC83's pinned failure — now
  holds both routes 8/8. The failure was an artifact of AC80's non-order-preserving decode (which
  placed the boundary word before the bank rules); the order-preserving decode places the boundary
  word last, so the "boundary preempts renewal" path is structurally gone.
- The simultaneous (coincident-tick) corruption+move — AC82's non-composition — now holds both
  routes 8/8. The material-low hijack (obs bit 1 preempting renewal) is transient under
  erase-on-relinquish: the stale entry drops, re-binds within ~5 ticks, obs bit 1 clears, and
  renewal fires before the unmoved route lapses.

The milestone statement therefore records the *positive* simultaneous/adversarial result, not a
limit. The runner is byte-equivalent to AC88 at the separated schedule (40/40 `state_hash`), so the
only differences are the schedule constant and the seed family.
