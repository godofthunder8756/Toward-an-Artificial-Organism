# AC100 errata v1: corrected reading of the frozen result, moved out of the frozen protocol

2026-09-20. This is a non-frozen correction note. The AC100 wording corrections that were
originally applied in commit 8c082e0 edited `AC100_PROTOCOL_v1.md` in place, which drifted its
recorded hash (frozen `f7990a73…` → `61c12a3d…`). The protocol is a **hashed source**: its bytes
are part of the freeze, so editing it after the first final seed breaks the audit's
"no hash drift" guarantee. This note restores `AC100_PROTOCOL_v1.md` to its exact frozen bytes
(`f7990a73…`) and records the corrections here instead, so the protocol stays byte-frozen and the
corrections remain auditable. `AC100_RESULTS_v1.md` keeps its corrected narrative (it is not a
hashed source); its verification section points here rather than disclosing a live hash drift.

The frozen `ac100_results_v1/rows.jsonl`, `results.json`, and `pre_run_snapshot.json` are
unchanged, and `audit_ac100.py` passes with **no** hash drift after the restore.

## 1. Engineering denominator: seeds 0-7, not 0-15

The protocol and results originally described the engineering 2×2 as running on "engineering
0-15". It ran on **seeds 0-7** (8 seeds), disjoint from the finals and every earlier final family.
Consequences of the corrected denominator:

- The engineering seed-7 harmful combination is **1/8** engineering seeds, not 1/16 (~6%).
- The "engineering seeds (0-7, 4412-4439) are excluded" anti-drift line in the protocol is the
  correct form; the restored protocol (frozen bytes) still says "0-15" because it is the original
  frozen text. The correct denominator is **0-7**.

## 2. Two successful alternatives, not one (bin_res and gray_ctl)

The original narrative credited only `gray_ctl` (Gray, no reserve) as "the consolidated
architecture". The frozen rows show **both** `gray_ctl` (Gray, no reserve) and `bin_res`
(binary + reserve) satisfy the full per-move adaptation criterion (relinquish + re-acquire after
every move + continued W/C/B production + survive) on **all 4 distinct final seeds**. The 2×2
therefore establishes **two successful alternatives** on this cohort: binary+reserve and
Gray-no-reserve. The reserve is *unnecessary for Gray on the tested cohorts* (Q1, answered in the
negative), not *redundant* — "redundant" would imply the reserve carries nothing anywhere, which
the `bin_res` success contradicts.

## 3. The seed-7 failure is downstream of the drop, not a stalled increment

The original wording said the Gray streak "stalls at 5" on engineering seed 7, which reads as the
increment itself failing to fire. The corrected reading from the frozen rows: the second
relinquishment **fires** at t=12335 (drop succeeds, `relinquishments=2`, `relinq_by_move [1,1]`,
register bit set) — it is the organism's last functional act. What fails *after* the drop is the
recovery: W-birth stops entirely after the second move (`W_birth` in window 2 = 0), so (1) the Gray
5→0 reset write (21 replicas) is refused for lack of W (leaving the streak stuck at 5 even though
the drop fired), and (2) re-acquisition cannot happen — the deposit path needs `8·interior_W ≥ 21`
to re-bind key 1, so with W gone a productive blind contact cannot be stored (`reacquire_ticks` has
no move-2 entry). W and C die together, energy drains, and the organism dies at t=12546 with
material still 98 (W/C collapse, not material starvation). The mechanism is "drop fires, then the
W-bound recovery cannot run", not "the streak increment stalls".

## 4. Per-seed table regenerated from the frozen rows

The original per-seed table's drop ticks were approximations. It was regenerated from the frozen
`rows.jsonl` with exact drop/re-acquire ticks. The corrected table (now in `AC100_RESULTS_v1.md`):

| seed | priority    | bin_ctl (binary, no reserve)         | bin_res (binary + reserve)         | gray_ctl (Gray, no reserve)        | gray_res (Gray + reserve)          |
|------|-------------|--------------------------------------|------------------------------------|------------------------------------|------------------------------------|
| 4444 | `[0,3,2,1]` | survive, 1 drop (expiry), reacquires | drop@8209 + drop@12327, survive    | drop@8227 + drop@12316, survive    | drop@8209 + drop@12302, survive    |
| 4445 | `[2,0,3,1]` | survive, 1 drop (expiry), reacquires | drop@8202 + drop@12302, survive    | drop@8223 + drop@12307, survive    | drop@8201 + drop@12311, survive    |
| 4446 | `[1,0,3,2]` | **dies 8448** (streak stuck 5, 0 drops) | drop@8228 + drop@12331, survive  | drop@8232 + drop@12323, survive    | drop@8228 + drop@12330, survive    |
| 4447 | `[0,3,2,1]` | survive, 0 drops (both moves by expiry) | drop@8205 + drop@12300, survive  | drop@8220 + drop@12328, survive    | drop@8216 + drop@12308, survive    |

Key changes from the original: `bin_ctl` rows are described by drop count + expiry status rather
than a single tick, and every drop tick is the exact value from the frozen rows.

## 5. Headline and claim wording

- A headline was added to the results: "Gray encoding without a reserve supports active adaptation
  through two route reversals on four unseen seeds. The reserve is unnecessary on this cohort; one
  of eight engineering seeds exhibits a reserve-associated survival reversal."
- The claim wording was corrected everywhere from "the reserve is *redundant* and, under
  repetition, *harmful*" to "the reserve is **unnecessary for Gray on the tested cohorts** and, on
  one engineering seed, potentially harmful under repetition". The corrected phrasing is what
  `AC100_RESULTS_v1.md` now carries; the restored (frozen) protocol still bears the original
  "redundant and harmful" claim, which is corrected by this note.

## 6. Verification and audit state

`AC100_PROTOCOL_v1.md` is restored to its frozen bytes (`f7990a73…`) and is **not** edited again.
`audit_ac100.py` now passes with no hash drift (all 19 source hashes match the freeze). The frozen
`rows.jsonl`, `results.json`, and `pre_run_snapshot.json` are untouched. `AC100_RESULTS_v1.md`'s
verification section points here instead of disclosing a live protocol-hash drift.
