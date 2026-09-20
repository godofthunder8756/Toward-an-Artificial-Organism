# AC100 protocol v1: consolidation — binary/Gray streak × reserve/no-reserve under repeated route changes

STATUS: **frozen before the first final seed.** Written 2026-09-20. AC99 froze the Gray-coded
streak (cheaper transitions) + the AC98/AC99 revised reserve and passed all five gates on unseen
seeds 4440-4443 (G1 unconditional adaptation 4/4, G2 no-harm 4/4, G3 per-tick observer-discard 8/8,
G4 endogenous reserve, G5 completeness/determinism). The load-bearing direction was real: the
binary control (the AC98/AC99 architecture) died on 4442 and Gray flipped it. Three questions were
left open about whether that success depends on the *combination*, and none is answered by AC99
alone:

1. **Is the reserve necessary?** Every final Gray run includes it, and on 4440/4441 it is armed and
   never released (D2's near-redundancy prediction). Redundancy has NOT been shown — it requires a
   Gray-without-reserve comparison.
2. **Does the cheaper transition generalize, or only shift the failure?** Gray changes write costs,
   reset costs, and damage responses wherever the counter operates; it is not guaranteed harmless
   before a move.
3. **Is the acquired function sustainable across successive disruptions, or does the dearer Gray
   reset (drop 7 + reset 21 = 28 replicas > RESERVE_LEVEL 21) compound under repeated route changes?**

This protocol freezes the consolidation: a **2×2 factorial — {binary, gray} streak ×
{no-reserve, reserve}** — in the AC96/97/98/99 relinquishment world, with a **move schedule**
(repeated route changes) instead of a single move, on an **unseen** cohort.

SOURCES (declared): ac100.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC100_PROTOCOL_v1.md

## The claim and the three questions

AC99 located the maintenance/adaptation conflict's resolution in the decision-state *encoding*
(a Gray-coded counter), and showed it works on unseen seeds. AC100 consolidates that result by
asking whether the success depends on the *reserve* that every AC99 run also carried. The claim is:

**The Gray-coded streak, NOT the reserve, is what carries AC99's success — and the consolidated
architecture (Gray, no reserve) sustains the acquired function across successive route changes,
while the reserve is redundant and, under repetition, harmful.**

The three questions are answered by the factorial:

- Q1 (reserve necessary?) — compare `gray_res` (Gray + reserve) against `gray_ctl` (Gray, no
  reserve). The reserve is *necessary* iff some seed's gray_ctl fails while gray_res succeeds
  (never observed in engineering); *harmful* iff some seed's gray_ctl succeeds while gray_res dies.
- Q2 (generalize or shift?) — compare the Gray arms against the binary arms. Gray *generalizes*
  iff it survives/relinquishes where a binary arm dies; it *shifts* iff a binary arm survives where
  a Gray arm dies.
- Q3 (sustainable?) — does the Gray streak relinquish + re-acquire + keep producing at EVERY move,
  with the dearer 28-replica reset exercised repeatedly.

## World, arms, seeds

World constants unchanged from AC98/AC97/AC96/AC99: PORTS=4, YIELD_M=64, YIELD_F=64, TICKS=16384,
sticky 1e-4 damage on both banks (independent streams), STREAK_N=6, STREAK_THRESHOLD=4,
REGISTER_THRESHOLD=4, RESERVE_LEVEL=21, RESERVE_OFFS=540, RESERVE_THRESHOLD=4, RESERVE_TRIGGER=2,
the order-preserving generic-over-syntax decoder, AC75's erase-on-relinquishment. `corrupt=False` for
every condition (the moves are the sole events; the "reconstruction challenge" is carried forward as
the state-sufficiency observer-discard gate, exactly as in AC99, where `corrupt=False`).

**The move schedule** (the only change from AC99): channel 1's port flips at **t=8192** (base[1] →
1−base[1], AC99's move) and flips **back** at **t=12288** (→ base[1]). Two successive disruptions,
each followed by a 4096-tick window for relinquish + re-acquire, and a final 4096-tick survival
window. This exercises the Gray reset's 28-replica drop+reset twice. At the single-move schedule
`[(8192, 'flip')]` each arm reproduces its AC99 runner **byte-for-byte** (state_hash) — that
equivalence is what licenses attributing any difference to the schedule change alone (AC89's rule).

Four arms per individual (the 2×2):

- `bin_ctl`  — binary streak, no reserve  (= `ac99.run(reserve=False)`, byte-identical to ac96 maintained)
- `bin_res`  — binary streak + reserve     (= `ac99.run(reserve=True)`, the AC98/AC99 architecture)
- `gray_ctl` — Gray streak, no reserve     (= `ac99_d2.run(reserve=False)`)
- `gray_res` — Gray streak + reserve       (= `ac99_d2.run(reserve=True)`, the AC99 success arm)

32 rows = 4 seeds × 2 histories × 4 arms. History is a trivial repeated measure (the runner gates
`activation=[True,True]` and the RNG seeds depend on seed, not history), so the two histories are
identical per seed; the criterion is stated per distinct seed, with history identity verified per seed.

Final seeds `4444, 4445, 4446, 4447` (4 seeds × 2 histories = 8 individuals), **unseen**: disjoint
from engineering 0-15, from the D1/D2/D3 seeds 4412-4415/4436-4439, from the AC96 screening sweep
4412-4431, from every prior final family ≤ 4443 (… AC97 4432-4435, AC98 4436-4439, AC99 4440-4443),
and from the separate 4600-4871 order-line and 5100-5507 confirmatory families. **No screening of
this final family** — the gates below were shaped by the engineering 2×2 on the disjoint seeds 0-7
(disclosed below), and the final family itself is untouched.

## Screening disclosed (before this protocol was frozen)

The engineering 2×2 ran on seeds **0-7** (both histories; histories identical per seed) under the
repeated-move schedule, and is recorded in `ac100_engineering_v1/` (no freeze). Measured there:

- **The Gray encoding alone is sufficient and sustainable.** `gray_ctl` satisfies the full per-move
  adaptation criterion (relinquish + re-acquire after every move + continued W/C/B production +
  survive) on **8/8** seeds.
- **The reserve is never necessary for Gray.** No seed where gray_ctl fails and gray_res succeeds
  (0/8). On 7/8 seeds gray_ctl and gray_res agree; the reserve's release triggers are near-redundant
  (D2's prediction, now under repeated moves).
- **The reserve is harmful under repetition.** On seed **7**, `gray_res` dies at t=12546 (both
  histories) with the streak stuck at 5, while `gray_ctl` survives (drop@12296, re-acquire@12297,
  W=3, C=2). The reserve's 21-material withholding at t≈525 phase-shifts the second post-move build
  into a W-death window, re-introducing the exact W-bound stall (streak stuck at 5) the Gray encoding
  removes — the AC97/AC98 failure mode now caused by the reserve *combined with* repetition.
- **Both factors are alternative fixes for the same stall.** `bin_ctl` (binary, no reserve) dies on
  5/8 seeds (1, 2, 4, 5, 7); both `bin_res` (reserve) and `gray_ctl` (encoding) rescue all five —
  confirming AC99-D3's "the two fixes are alternatives, not complements."
- **The AC99 load-bearing direction reverses under repetition.** On seed 7, `bin_res` survives while
  `gray_res` dies — the opposite of AC99's 4442 (where gray_res survived and bin_res died). So the
  Gray+reserve *combination* is not a strict improvement over binary+reserve under repeated moves.

Consequences, all reflected in the gate shapes below: G1 is the consolidated success arm's own
per-individual criterion on **gray_ctl** (not a margin over a rival); G2 and G3 are the two no-harm
directions (encoding and reserve), which are exactly what detect the seed-7 harmful combination; G4
is the trajectory-level observer-discard on gray_res; G5 is the endogeneity invariant; the load-bearing
direction (gray_ctl survives where bin_ctl dies) is reported, not gated (AC97's gate-shape lesson).

## Gates (prespecified, categorical per distinct seed)

- **G1 (sustained adaptation WITHOUT the reserve).** For every distinct final seed, the **gray_ctl**
  arm satisfies, at EVERY move in the schedule: (A1) relinquishment — ≥1 drop with the register bit
  set in each post-move window; (A2) re-acquisition — ≥1 None→bound transition of key 1 in each
  post-move window; (A3) continued machinery production — W, C and B births all > 0 in every
  post-move window; and (A4) survival — `completed`. Both histories must satisfy it (identity verified
  per seed). No external rescue.
- **G2 (no-harm, encoding direction).** No distinct final seed where `bin_res` survives and `gray_res`
  dies. (Gray encoding does not harm the AC98/AC99 architecture.)
- **G3 (no-harm, reserve direction).** No distinct final seed where `gray_ctl` survives and `gray_res`
  dies. (The reserve does not harm the Gray architecture.)
- **G4 (state sufficiency, per-tick observer-discard, on gray_res).** Every final individual: the
  gray_res run with the succession observer AND the alloc (clearing the vestigial host streak dict)
  discarded at a mid-streak tick is **byte-identical at every tick** (`per_tick_identical`,
  trajectory-level), non-vacuously (`status != 'no_mid_streak'`, `swap_applied`, `streak_at_swap == 2`).
  The Gray streak and the reserve must be recovered from maintained state alone (carry AC99's G3).
- **G5 (endogenous reserve, no external rescue).** Every final reserve-arm individual (`gray_res`,
  `bin_res`): `reserve_m > 0` and `reserve_released_m <= reserve_m` (the reserved material is the
  organism's own withheld intake). No rescue arm.
- **G6 (completeness + determinism + arm identity).** Row count == seeds × 2 histories × 4 arms (32);
  a sampled exact rerun of the first row is byte-identical (state_hash); and each arm reproduces its
  AC99 runner **byte-for-byte** (state_hash) at the single-move schedule `[(8192, 'flip')]` — proving
  the schedule change is the only change in the runner.

A gate failure is recorded, not moved (AC16/17). G2 and G3 are prespecified as real no-harm gates;
if the seed-7 phenomenon transfers to the finals they will FAIL, and that failure is the finding
(the reserve is harmful under repetition), not a licence to amend the gate.

## Reported, not gated

- **The load-bearing direction** (gray_ctl survives/relinquishes where bin_ctl dies) — reported per
  seed, not gated (a positive-only contrast would be AC97's mistake).
- **The interaction mechanism** — on seed 7 the reserve's early withholding (t≈525) phase-shifts the
  second post-move build into a W-death window; the streak stalls at 5 and the organism dies of the
  W/C collapse (material still 98 at death, so it is not material starvation).
- **The reserve's maintenance trade-off** — reserve_m 21 (or 63 with re-arm), released 0-42, its paid
  writes a small fraction of bank-1 repair.
- **Survival is a bimodality-aware lower bound** (AC68).
- **Priorities** — the final family's acquired priorities are reported, not prespecified (unseen
  seeds); the relinquishment is a streak/register decision, not a renewal-contention decision.
- **Supplied machinery remains** — `advance()` and `prog.choose` are still host-supplied format-level
  machinery; no autopoiesis claim. The reserve is still a fixed minimum reserve, not an acquired
  allocation decision (AC96-D4's open item).

## Anti-drift rules

- The runner creates `ac100_results_v1/` with `mkdir(exist_ok=False)`.
- Pre-flight parses the `SOURCES (declared):` line above and asserts it equals the runner's hashed
  set (which includes this protocol file).
- `test_ac100.py`, `audit_ac100.py`, `replay_ac100.py` are NOT hashed into the frozen snapshot
  (AC17's rule).
- Engineering seeds (0-15, 4412-4439) are excluded from the final sample and are disjoint from the
  final family.
- The arm identity (declared, verified before finals): each arm reproduces its AC99 runner
  byte-for-byte at `[(8192, 'flip')]`, so the schedule is the only change in the runner.
- If a gate fails, record the failure and do NOT move it; supersede with a new version on fresh seeds.
- The frozen AC99 results and every earlier freeze are untouched.

## Source hashes (computed before the first final seed)

    (recorded in ac100_results_v1/pre_run_snapshot.json at freeze time)
