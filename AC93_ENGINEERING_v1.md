# AC93 engineering v1: gating write_ctrl breaks the succession rate limiter — clean control fails

2026-09-18. Engineering only — no protocol freeze, no final seeds, no claim. `ac93.py` (seeds 0-7,
16,384 ticks), derived from `ac92.py` per AC93_DESIGN_v1.md Decision 2. Comparator equivalence
against frozen AC92 passed; the declared clean-control identity (design section 5) is falsified and
the cause is identified.

## What was implemented

`ac93.py` adds a `gate_ctrl` toggle to `write_ctrl` (and threads it through `advance`/`maintain`
via `cfg['gate_ctrl']`). When `gate_ctrl=True` (the `gated` arm, the AC93 architecture):

1. **MODE field (bits 0-3)** is written all-or-nothing under `_cap` — if `len(mode_sites) > _cap(b)`
   the whole transition is refused (nothing written); otherwise all mode_sites are written.
2. **LAST field (bits 4-17)** is budgeted under `_cap` — `n_last = min(len(last_sites), _cap(b))`.

When `gate_ctrl=False` (the `ungated` arm, the frozen comparator), `write_ctrl` is byte-identical to
the frozen AC88/AC92 distinct-resource model (MODE refused only on energy/material shortfall, LAST
budgeted by energy/material alone). `_cap = min(32, 8*available_W, energy, material)`.

Arms: `gated` (gate on) and `ungated` (gate off); both otherwise share the AC92 `intact` world
(regen + repair + succession + ctrl_maintain, corruption at t=8192, sticky damage). The
W_block/W_rescue interruption arms and the no_repair control are D3/D4.

## Comparator equivalence — PASSED

`ungated` reproduced the frozen AC92 `intact` arm **byte-for-byte (state_hash) on all 32
conditions** (seeds 4300-4303 × 2 histories × damage {T,F} × corrupt {T,F}). The runner is a
correct extension of ac92, and the gate is a no-op when disabled.

## Clean control — FAILED (the finding)

Design section 5 declares: with W at the steady state 3, `8*W = 24 >= 21` (the largest MODE
transition), so the added W condition never binds and `gated` == `ungated` state_hash-identical on
every condition. **This is false on every damage=True condition.** `gated` diverges from `ungated`
dramatically (per-seed, damage+corrupt, history 0; 8 seeds × 2 histories all agree):

| seed | ungated successions | gated successions | ungated ctrl_writes | gated ctrl_writes | gated outcome |
|------|--------------------:|------------------:|--------------------:|------------------:|---------------|
| 0    | 7                   | 86                | 844                 | 8194              | survives       |
| 1    | 7                   | 48                | 825                 | 49916             | **dies t=13079**|
| 2    | 6                   | 81                | 758                 | 7794              | survives       |
| 3    | 6                   | 123               | 719                 | 11871             | survives       |
| 4    | 6                   | 83                | 748                 | 7930              | survives       |
| 5    | 7                   | 105               | 844                 | 10115             | survives       |
| 6    | 6                   | 132               | 742                 | 12549             | survives       |
| 7    | 6                   | 137               | 760                 | 12986             | survives       |

(seed 1 gated dies with energy -7 in BOTH histories; every other individual survives.)

The clean control holds **only trivially** where the succession machinery never runs: with
`damage=False` the description is never hit, so no succession fires, and `gated` == `ungated`
(0 successions each). With `damage=True` the succession machinery runs and the divergence appears
universally (8/8 seeds). This is consistent with the mechanism below: the divergence requires a
succession to actually start, which requires the damage trigger.

### Mechanism (verified by per-write tracing, `_ac93_probe_gate.py`)

The clean-control claim only examined the MODE field. The **LAST field is a 14-bit timestamp whose
succession-start write is much larger than 21 replicas**: going from the previous start tick to the
new one (e.g. 0 → 2413, then 2413 → 4819) differs in **35-69 replicas** (n_last 49/69/56/57 in the
trace). The W cap is 24. So under the gate, the budgeted LAST write truncates the timestamp to its
low ~3 bits every succession:

- **ungated**: `n_last = min(len(last_sites), energy, material)`, and at succession start
  energy/material are ~60/27, so the timestamp is written (fully, or truncated only at the top bit
  when material briefly drops — a rare, self-correcting glitch: one 87-tick gap in the frozen trace,
  then normal ~2400 pacing resumes).
- **gated**: `n_last = min(len(last_sites), 24)`, so the high-order timestamp bits are NEVER
  written. `last` reads back as a small number (13, 189, 182, 184 …), so the rate limiter
  `now - last >= SUCC_MIN_SPACING (2400)` is satisfied ~immediately after every succession.

Successions then fire as fast as the damage trigger (desc minority >= 2) allows — ~80-130 ticks
apart instead of ~2400 — giving 81-123 successions vs 6-7. Each succession is a full 910-replica
slot copy plus controller writes, so the runaway drains the material/energy economy; seed 1 runs it
to energy -7 and death at t=13079.

### The MODE field is fine

Confirmed: a MODE transition changes at most 3 of 4 bits (<= 21 replicas), so at W=3 the gated MODE
refusal never binds and MODE writes coincide with the ungated ones (unit test `test_gated_mode_*`).
The clean-control failure is entirely the LAST-field budget.

## Consequences for D3/D4 (not decided here)

1. **The design's section 5 clean-control expectation is an errata.** It reasoned about the largest
   MODE transition (21) and overlooked that the LAST field's budget is bounded by the timestamp
   *delta* (~35-69 replicas at succession start), which exceeds 8*W=24. The "partially-updated
   timestamp cannot corrupt the state machine" claim (Decision 2 item 2, carried from AC88) is true
   of a *torn* timestamp but false of a *permanently truncated* one: a small `last` disables the
   succession rate limiter, which IS load-bearing (it prevents the organism spending itself to
   death on continuous succession).
2. **The distinct-resource declaration in AC88 was load-bearing for the rate limiter's integrity,**
   not a modeling convenience. Removing it without also providing a way to fund a full timestamp
   write breaks the coordinator.
3. **Options to carry into D3** (not chosen here): (a) make the LAST field atomic like MODE (refuse
   unless the full timestamp write is affordable), at the cost of a larger all-or-nothing write;
   (b) give the timestamp its own (larger or W-independent) budget while keeping MODE gated — which
   re-splits the resource model; (c) store the rate-limit bookkeeping in a form whose per-write
   delta is <= 24 replicas (e.g. a coarse counter), so the W cap never truncates it; (d) accept the
   divergence and gate the study on it (the load-bearing effect is real, but the "no interruption,
   gate is inert" clean control cannot be used to isolate the W_block/W_rescue effect).
4. The `gated`-vs-`ungated` divergence is itself a mechanistic signature — under healthy W the
   coordinator's bookkeeping write already needs more capacity than the produced machinery's
   8*W=24 per-action cap supplies, so "the machinery enacts the coordinator transition" has a
   measurable cost the frozen distinct-resource model was absorbing. Whether that cost is the
   intended load-bearing effect or a rate-limiter artefact is the design decision D3 must settle.

## Files

- `ac93.py` — new runner (gated/ungated arms, gate toggle threaded through write_ctrl/advance/maintain).
- `test_ac93.py` — 8 unit tests: arm config, gated-MODE-refuses-at-W=0, ungated-MODE-writes-at-W=0,
  MODE atomicity under cap (W=1), LAST budget difference (24 vs 98), low-bit-first truncation
  (both directions), gate toggle flips with W=0.
- `ac93_engineering_v1/` — engineering rows + snapshot + clean-control flag.
- `ac93_engineering_v1_partial_timeout/` — the first (timed-out at seed 5) partial run, preserved.
- `_ac93_probe_gate.py`, `_ac93_probe_rows.py` — diagnostics (untracked scratch).
