# AC11 design controls v2: the allocation question is not well posed here

2026-09-15. Engineering controls only. **No final seeds were run.** The AC11
claim is not established and is not claimed; `AC11_PROTOCOL_v1.md` is unfrozen
and its falsification clause has fired. The broader autonomy goal remains active.

## What was tested

AC11 asked whether an organism can acquire the need to allocate or relinquish
maintenance spending under a post-development port relabelling, with no protected
copy and no externally fixed correct state. Before running any final seed, two
controls decide whether the question is well posed at all. Six engineering
individuals per condition (seeds 0–2, both developmental histories); all outputs
retained in `ac11_design_controls_v2/` (v1 holds the first, smaller sweep).

## A. Single port relabelled — a state-blind policy matches or beats the learner

| condition | alive | mean activity | deaths |
| --- | ---: | ---: | --- |
| fixed duty 1/1 (= `preserve`) | 1/6 | 0.715 | 1272–1500 |
| fixed duty **1/2** | **4/6** | 0.912 | 1500–1519 |
| fixed duty 1/3 | 0/6 | 0.620 | 1255–1279 |
| fixed duty **1/4** | **4/6** | 0.893 | 1279–1500 |
| fixed duty 1/6 | 1/6 | 0.699 | 1248–1476 |
| fixed duty 1/8 | 1/6 | 0.686 | 1272–1279 |
| random p=1.0 (= `preserve`) | 1/6 | 0.715 | 1272–1500 |
| random p=0.5 | 3/6 | 0.809 | 1255–1274 |
| random p=0.25 | 2/6 | 0.786 | 1240–1648 |
| random p=0.125 | 1/6 | 0.587 | 472–1763 |
| adaptive N=2 | 3/6 | 0.833 | 1278–1533 |
| adaptive N=4 | 3/6 | 0.812 | 1273–1279 |
| adaptive N=8 | 3/6 | 0.812 | 1273–1279 |
| adaptive N=16 | 3/6 | 0.812 | 1273–1279 |
| adaptive N=32 (= never relinquishes) | 1/6 | 0.715 | 1272–1500 |
| `relinquish` (no maintenance at all) | 2/6 | 0.566 | 472–986 |

Two internal consistency checks pass: fixed duty 1/1 and random p=1.0 reproduce
`preserve` (1/6, 0.715, same death interval) exactly, and adaptive N=32
reproduces it too, as it must when the streak never crosses.

**Verdict A.** Every configuration of the adaptive arm — including four
thresholds spanning 16× — is matched or beaten by a *state-blind* fixed duty
cycle, with no experience, no decision and no stored allocation state
(4/6 versus 3/6). The AC11 falsification clause therefore fires: the outcome is
reachable without an acquired decision, so no "need to allocate" has been
demonstrated.

## B. Both ports relabelled — relinquishment is not viable either

| condition | alive | mean activity | deaths |
| --- | ---: | ---: | --- |
| `preserve` | 0/6 | 0.624 | 1266–1297 |
| adaptive | 0/6 | 0.622 | 1263–1279 |
| `relinquish` | 2/6 | 0.566 | **472–986** |

**Verdict B.** When the whole region goes stale at once, nothing survives the
horizon. Relinquishing scores best only because it starves *before* the
intervention (deaths 472–986 are all in the valid-route phase): it is choosing
which phase to die in, not remaining viable. So there is no "need to relinquish"
here either — only a difference in death timing.

## Diagnosis: the tension is structural, and it is measured

1. **The allocation unit is coarser than the usefulness boundary.** Renewal is
   region-granular in the frozen `ac9_memory` primitive, and both acquired
   entries share one region. With one key stale and one still valid, the optimal
   maintenance *level* is intermediate and **constant** — a level a fixed duty
   cycle reaches without any decision. The measurements show exactly that shape:
   duty 1/2 and 1/4 win, duty 1/1 and 1/8 lose, and the adaptive arm's
   experience-dependent switch lands between them.
2. **Blind access cannot fund even a reduced metabolism.** In the AC11 regime,
   `relinquish` dies at 472–986 of energy starvation with material and fuel still
   in store and zero converters available: at 1/4 blind success the organism
   cannot raise the fuel to keep C alive, so conversion stops and energy drains.
   Relinquishment buys delay, not viability.
3. **The two requirements are in tension across regimes.** In the frozen economy
   (ports 2, yields 64/32) relinquishment was viable but preservation was not
   necessary. In the AC11 regime (ports 4, yields 16/16) preservation is
   necessary but relinquishment is not viable. No single regime in this
   architecture satisfies both, so no world here makes "acquire the need to
   relinquish" both necessary and survivable.

## What would make the question well posed

The missing piece is an architectural primitive, not a threshold:

1. **Per-slot (per-entry) renewal**, so maintenance can be allocated at the
   granularity where usefulness actually differs. This is a supplied-mechanism
   change to `ac9_memory` and therefore a new versioned study with its own
   protocol and freeze; it must not alter any frozen AC1–AC11 result.
2. A world in which the usefulness boundary **aligns** with the allocation unit
   (either per-entry renewal, or a region whose entries share one fate) — Part B
   shows that making the whole region stale at once is not sufficient on its own
   because of (2) below.
3. An economy in which post-relinquishment blind access **funds** the reduced
   metabolism, so relinquishment is survivable rather than merely slower. This
   requires the blind success rate and the non-renewal metabolic cost to be set
   together, and it must be measured, not assumed.
4. Rivals redefined at that granularity: a spending-matched per-entry schedule,
   and a random per-entry allocator, both on the same observation stream.
5. The decision must still live in vulnerable, paid, repairable state — the
   AC11 requirement that no protected copy and no externally fixed correct state
   exists is unaffected by any of the above.

## What this establishes, and what it does not

Establishes: a bounded negative design result with a measured diagnosis. AC11's
question cannot be answered in the AC9 architecture, and the reason is the
granularity mismatch plus the blind-access economy, not the learner's threshold
(four thresholds, same outcome) and not a shortage of rivals.

Also recorded, as side-findings worth carrying forward:

- The lineage's optimum level of memory maintenance is **intermediate**, not
  all-or-nothing. This explains AC6's earlier "no net material saving" result and
  sharpens why AC9 v1→v2's stored rule-order change mattered so much: it moved
  the organism between two bad levels, not from "no maintenance" to "maintenance".
- AC10's constituent ablations are unaffected: they removed whole constituents,
  whereas this concerned the *level* of memory maintenance, which AC10 never
  varied.

Does not establish: any acquired allocation, any new maintenance need, any
autopoiesis, and nothing about consciousness. The AC11 claim remains
NOT ESTABLISHED in `AUTONOMY_RESEARCH_STATUS.md`.

## Artifacts

`AC11_PROTOCOL_v1.md` (unfrozen design, falsified by these controls),
`ac11.py` (working harness: allocation arms, shadow-read control, streak logic;
no final seeds), `ac11_design_controls.py`, `ac11_design_controls_v1/` (first
sweep), `ac11_design_controls_v2/` (complete sweep), `ac11_feasibility_v1/` and
`ac11_feasibility_v2/` (regime search). The first `ac11.py --engineering` grid was
discarded as superseded before it was committed; its numbers are reproduced
exactly by Part A of these controls (`preserve` 1/6, adaptive 3/6, `relinquish`
2/6).
