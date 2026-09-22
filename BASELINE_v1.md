# Baseline v1 — the authoritative state of the project

2026-09-22. Bookkeeping note, not a scientific claim. Nothing is re-run, re-frozen,
re-hashed, or edited here; this document only names what already exists so that
downstream planning stops silently inheriting claims demonstrated in an earlier
architecture. Frozen artifacts (runners, protocols, results dirs, hashes) are untouched.

## Reference commit and architecture

- **Reference commit:** `8f0218adccb7ce2ddca7d359321ce06c4de8e247` (short `8f0218a`),
  "AC105: operating-range test — allowance-42 budget rescues a new marginal priority
  (5804), never harms, improves late-corruption relinquishment; move-first boundary kills
  both arms (all six gates pass)". HEAD of `master` at baseline time.
- **Reference architecture** (the AC105 body, inherited from AC99–AC104):
  1. `gray_ctl` — a Gray-coded relinquishment failure-streak with **no reserve**
     (established AC100: the Gray encoding, not the reserve, carries AC99's adaptation).
  2. **Persistent reconstruction trigger** — `reg_from_active` fires while
     `reg_trigger OR program_incomplete`, where completion is derived from maintained
     state (the decoded program still differs from the description-derived target)
     (established AC103).
  3. **Allowance-42 material budget** — the reconstruction budget is
     `max(0, spendable_material − DECISION_ALLOWANCE)`, `DECISION_ALLOWANCE = STREAK_N × 7 = 42`,
     applied throughout life with no challenge-time knowledge (established AC104,
     operating range tested AC105).

The earlier architecture generations (binary streak + reserve, AC97–AC99 era) are
superseded and are **not** the reference. The internal-state substrate (130-bit
description in vulnerable slots + maintained coordination state, AC85–AC89) is carried
into the reference architecture unchanged.

## Accepted milestones (each mapped to its frozen study in `EVIDENCE_INDEX_v1.md`)

1. **Internal-state milestone** — internally stored controller information is maintained,
   reconstructed, and repeatedly transferred to successor storage, through vulnerable,
   damageable, resource-maintained coordination state (AC85/AC86/AC87; simultaneous +
   adversarial schedule AC89).
2. **Gray encoding carries adaptation** — a Gray-coded decision counter, not a reserve,
   resolves the W-denominated maintenance/adaptation conflict (AC99/AC100).
3. **Composition (internal-state)** — internal memory, controller reconstruction,
   machinery turnover, and adaptation compose in the same organism; the behavioural arm
   of the composition (survival of one unseen final) fails (AC101, recorded not moved).
4. **Premature-termination vs resource-shortage separation** — persistent triggering
   distinguishes recovery failure from survival failure; neither tested spending policy
   resolves every combined-challenge failure (AC102/AC103).
5. **Internal spending rule** — an explicit material budget coordinates reconstruction
   with the paid decision write; holds across the AC105 operating range and rescues a new
   marginal priority (AC104/AC105).

Earlier accepted foundations (not re-derived here, carried as frozen records): the
integrated body (AC1–AC4), the AC9 developmental line and integrated ablations (AC10),
graded access with a real economic decision (AC15/AC18), load-bearing self-monitoring and
erase-on-relinquishment (AC67/AC71/AC75), controller turnover (AC76), description
maintenance and internalization (AC79/AC80/AC84/AC85/AC86), and the production-dependencies
phase (AC91–AC96). Full detail in the evidence index.

## Stale directives (flagged, not silently inherited)

1. **`RESUME_RESEARCH.md` is AC10-era and badly out of date.** Its "Current stopping point"
   names AC10 as the latest completed study and its "What to do next" points at the
   AC11/AC13/AC18 allocation line. The arc has since reached AC105. Treat its *frozen-version
   discipline* and *command* sections as still valid; treat its *current-state* and
   *next-target* sections as historical. Do not resume work from it without checking
   `AUTONOMY_RESEARCH_STATUS.md` (the live narrative).
2. **`DEPENDENCY_AUDIT_v1.md` predates the internal-state milestone.** Its central claim —
   the controller content is "externally supplied, maintained not produced", "never turned
   over" — was superseded by AC79–AC89: the 130-bit description now lives in vulnerable,
   paid-maintained state and is reconstructed and replaced by succession. Still valid:
   the *interpreter* (`prog.choose`) and the succession *transition logic* (`advance()`) are
   supplied substrate. Read the audit for its component/causal inventory; do not quote its
   section-6 gap as the current state.
3. **`CLOSURE_BOUNDARY_v1.md` is superseded** by `CLOSURE_BOUNDARY_v2.md` (AC87/88/89-era).
   v2 is the settled boundary; v1 is the AC67/68-era boundary, preserved for AC71's citation.
4. **The consciousness gate is archived, and stays archived.** `CONSCIOUSNESS_BLOCKS_DISPOSITION_v1.md`
   (goal §7 archived) and `CONSCIOUSNESS_MECHANISM_SPEC_v1.md` (no concrete testable mechanism;
   closure with a named candidate) both stand. Do not relabel the AC67/71 self-monitoring loop
   as a consciousness result, and do not re-open the track on content self-production (the
   mechanism spec accepts AC79-errata §5: autopoiesis is not a prerequisite).

## Unresolved claims / open items

- **Full autopoiesis, strong organismal autonomy, and subjectivity remain UNESTABLISHED.**
  The controller's *information* is internalized; the *interpreter* and the succession
  *mechanism* are supplied. The AC90 modeling judgment — whether fixed `advance()` code is
  acceptable substrate or an always-available coordinator — is explicitly left unresolved by
  review, not settled.
- **Content self-production is blocked** (AC78): the production signal is a locked,
  path-dependent fixed point; no within-life signal ranks priorities. Distinct from
  regenerating inherited organization.
- **The reserve is not part of the architecture** (dropped in AC100 as unnecessary for Gray;
  the "acquired allocation" framing remains an open item, AC96-D4).
- **Allowance-42 generalization** is established on one fresh marginal economy (5804) and
  no-harm everywhere else, not universal. AC105's two named boundaries: `move_first` (5802,
  both arms die via the re-acquisition path — not budget-specific) and `late` on a marginal
  economy (5603 diagnostic, reconstruction-harm).
- **External peer review** remains open (AC1–AC4 confirmatory review done; independent peer
  review not yet).

## Controls / confounds / limits (carried into every downstream card)

- Distinguish **demonstrated in the current (AC105) architecture** from **demonstrated in an
  earlier version and inherited by claim**. The evidence index marks which architecture each
  capability was frozen under.
- **The 160 arm-runs of AC105 are 80 matched comparisons**, not 160 independent observations:
  8 seeds × 2 histories × 5 conditions, each scored on both arms (control vs candidate). Treat
  the arm-run pair as the unit of comparison.
- Survival is a **bimodality-aware lower bound** (AC68 W/C collapse is seed-family dependent,
  AC39). Engineering-seed statistics do not transfer to final seeds.
- Seeds are the replication unit; worlds/episodes/ticks are repeated measures. "N seeds ×
  2 histories" is N independent units, not 2N.
- Oracle/scaffold controls (protected copy, externally supplied correct state, machinery-only
  rescues) are labeled EXTERNAL and never counted as autonomous results.

## Disposition

No frozen study is restarted, re-hashed, or re-run merely because it is named here. The
frozen artifacts remain authoritative for their own claims; this baseline and the evidence
index are derived documents and are **not** hashed into any study's `pre_run_snapshot.json`.
