# AC93 design v1: coordinator transitions enacted by produced machinery (write_ctrl becomes W-gated)

STATUS: **design only.** No code, no protocol, no freeze. This document is the specification D2
implements (`ac93.py`). It is not a frozen artifact; D2 may return it with an errata note if an
engineering fact contradicts a declaration, but any change to the *decisions* below must be recorded
as an errata entry, not a silent edit.

## What AC93 claims, in one sentence

The succession coordinator's own transition write (`write_ctrl`) — the last paid substrate write on
the reconstruction/coordination path that is *not* enacted by the produced W repair catalyst — is
made dependent on that same finite-lived, autocatalytically produced machinery, so that coordinator
state transitions become a service the organization's produced components perform, not a host
operation that is always available for energy and material alone.

This is a **new architecture**, not a defect-fix. AC88's "distinct resource" declaration for the
controller register (reviewer's option (c)) was correct *for the frozen AC87/AC88 design* and is
left untouched there. AC93 revokes that declaration on the NEXT architecture and measures the
consequence. Frozen AC88/AC92 rows are never edited; they are the comparator (section 6).

## Decision 1 — the machinery: reuse the W repair catalyst, do not declare a new component

The coordinator-transition machinery is the **W repair catalyst** (bank 0, `body.life[:4]`):

- **finite-lived**: life 64, decremented each tick (`ac4` particle accounting).
- **produced**: born by action 6 (`ac9.step` action-6 branch; `ac9.birth`), paid 4 material + 2
  energy per birth (`ac4.pay`).
- **autocatalytic**: a bank-0 birth requires a live bank-0 parent (`parents=np.flatnonzero(a[:4])`),
  so W=0 is irreversible without an external re-seed (AC91/AC92).
- **the write-capacity term**: every content write on the coordination path is already capped by
  `_cap(b) = min(32, 8*available_W, b.energy, b.material)` where
  `available_W = int(ac4.available(b)[:4].sum())` (live bank-0 catalysts inside the boundary). W=0
  ⇒ cap 0 ⇒ no content write; W=3 (the deterministic steady state, AC91) ⇒ cap 24.

**Justification for reuse over a distinct component.** A distinct "coordinator component" would
require naming a new production rule, lifetime, and write cap, and would *weaken* the experiment:
the open question the AC91→AC92→AC93 arc is answering is whether the produced finite-lived machinery
that already enacts reconstruction and content repair also enacts the coordinator's transitions. If
the coordinator got its own dedicated component, the test would become "can a second piece of
machinery be produced", which does not answer that question. Reuse also preserves the clean-control
identity (section 5): with W at its steady-state 3, `8*W = 24 >= 21` (the largest mode transition),
so the gated and ungated arms are byte-identical — a property a new component with a different cap
would not give us for free.

Consequence, declared consistently: **`write_ctrl` becomes gated by the same `_cap` as
`write_toward_slot`, `write_pointer`, `reg_from_active`, `reg_description_active`, `reg_pointer`,
and `reg_ctrl`.** The coordinator register is no longer a distinct resource; it is paid content on
the produced-machinery path. Its *size* bound (18 bits × 7 = 126 replicas) is unchanged and remains
an upper bound only (the mode transition itself is ≤ 21 replicas, well under it).

## Decision 2 — the gating rule: atomic MODE, budgeted LAST, both under `_cap`

`write_ctrl` keeps the AC88 field split and gains the W term in both fields. The rule, written
against the AC88 implementation (`ac88.py:270-312`):

1. **MODE field (bits 0-3: active + phase) — atomic, all-or-nothing, now under `_cap`.**
   Compute `mode_sites` (replicas whose value differs from the target). If
   `len(mode_sites) > _cap(b)`, refuse the whole transition and write nothing (retried next tick).
   Otherwise write all `mode_sites` replicas. This is the AC88 atomicity rule with one added
   condition: the W-capacity term. A mode transition changes at most 3 of the 4 bits (≤ 21
   replicas; the largest is SWITCH 011 → REMOVE 100). With W=3 the added term `8*W=24` never binds,
   so the gated MODE write coincides with the ungated one whenever energy/material also suffice —
   which is exactly the clean-control property. With W < 3 the term binds and the transition is
   refused: this is the intended load-bearing behaviour D3 exercises.

2. **LAST field (bits 4-17: start timestamp) — budgeted, now under `_cap`.**
   `n_last = min(len(last_sites), _cap(b))`. The timestamp is rate-limit bookkeeping (read only by
   the `SUCC_MIN_SPACING` check while idle, ~300+ ticks after a start); a partially-updated
   timestamp is still a valid 14-bit integer and cannot corrupt the state machine (AC88), so it
   proceeds in budgeted increments exactly like `write_toward_slot`. The W term only changes the
   *budget* here, not the atomicity.

3. **Which field a partial write truncates (verified, not assumed).** `encode_ctrl` places the
   timestamp LSB at `c[4]` (`c[4+k] = (last>>k)&1`), and `np.argwhere` over `CTRL_OFFS[4:]` lists
   sites in increasing index order, i.e. **least-significant-first**. A budget-limited LAST write
   therefore truncates the *low-order* bits of the timestamp and leaves the high-order bits at their
   previous value; the MODE field is never partially written (atomic). D2 must pin both facts with
   unit tests, the AC88 way (test_ac88.py (i)/(ii) already pin MODE atomicity; add the W=0 and the
   low-bit-first assertions).

4. **Conservation is untouched by construction.** `write_ctrl` still pays 1 energy + 1 material per
   replica into `e['spent_e']/e['spent_m']` and `e['ctrl_writes']`, and the balance-line splice
   already folds `ctrl_writes` into `e['writes']`, so `ac4.balance`'s
   `spent_m == writes + 4*(W_birth+C_birth) + 2*B_birth` and the energy identity hold unchanged. The
   W-gating only changes *whether/how many* replicas are written, never the per-replica price.

## Decision 3 — what remains W-independent (re-classified honestly)

After this change, every paid substrate write on the reconstruction + coordination path is gated by
the W repair catalyst (bank 0, `8*W`). What stays outside the bank-0 `8*W` term, and why:

1. **Memory-region renewal (`mem.renew`, `ac9.step` actions 3-5).** Gated by the *region catalysts*
   (banks 1-2), via the capacity argument `a[4*(r+1):4*(r+2)].sum()` passed to `mem.renew`, not by
   bank-0 W. This is still produced finite-lived machinery (same family: life 64, born by action 6),
   but it is a *different population* with its own per-action capacity. So it is
   produced-machinery-gated, bank-0-W-independent. It is not part of this experiment and is
   unchanged.

2. **The production reactions themselves (`ac4.react`: W/C births, B birth, energy conversion).**
   These *produce* the W catalyst (and C, B, region catalysts). They are paid at fixed physical
   prices through `ac4.pay` (4 m + 2 e per W/C birth, 2 m + 2 e per B birth, 8 fuel → energy per
   conversion) and gated by their own prerequisites (a live parent catalyst, boundary presence,
   material/energy/fuel). They **cannot** be gated by `8*W` without circularity: W produces W, so the
   production step itself must not require W-catalyzed write capacity. This is the principled
   boundary of "produced machinery enacts writes": it applies to every *write the machine performs*,
   not to the *reactions that produce the machinery*.

3. **Environmental decay (damage stream, memory aging/expiry).** Not writes; they consume nothing and
   are gated by nothing. Unchanged.

So the honest statement is not "everything is now W-gated" but: **every paid write the coordinator
and reconstruction machinery performs is W-gated; the only non-W-gated paid activity is the
production of the machinery itself and the region-catalyst renewal, both of which are enacted by
produced catalysts under their own physical prerequisites.** D2 must record this re-classification
verbatim in the runner docstring so the claim cannot later be read as "all writes are W-gated".

## Prior-art checks (each answered against the frozen code)

- **AC87 (atomic multi-field transitions):** respected. MODE remains all-or-nothing; the W term is
  added to the *refusal condition*, not to a partial-write path. A torn controller word is still
  impossible by construction.
- **AC88 (distinct resource; atomic mode + budgeted LAST):** the field split (atomic MODE / budgeted
  LAST) and the low-bit-first partial-write fact are carried forward unchanged; only the "distinct
  resource, not gated by 8*W" declaration is revoked, and only for the new architecture. The frozen
  AC88 rows remain the comparator.
- **AC91/AC92 (W=0 autocatalytically irreversible; rescue must precede the last W death or be a
  direct external re-seed):** carried forward. Any AC93 interruption that blocks W-birth must either
  un-block before the last W dies (endogenous) or re-seed `life[:4]`/`pos[:4]` directly (EXTERNAL,
  machinery-only, no content — AC92's `restore_W` shape). A late restore is byte-identical to no
  restore (AC91's `W_restore_late`), so the interruption timing in D3 is constrained exactly as in
  AC92: block at `(target tick) − 63` so W depletes to 0 on the target tick.

## Planned arms

D2 implements the runner with all arms below (engineering seeds 0-7); D3 fixes the interruption
timing; D4 finalizes the protocol and gates. The arm set is:

- `gated` — the AC93 architecture: `write_ctrl` W-gated (Decision 2). All other primitives already
  W-gated, unchanged. Baseline mechanism arm (corresponds to AC92 `intact` / AC91 `succession`).
- `ungated` — the frozen comparator: `write_ctrl` NOT W-gated (the AC88/AC92 distinct-resource
  model). Reproduced byte-for-byte from the frozen AC88 rows (seeds 4028-4031) to prove the runner
  is a correct extension; equivalently, `gated` under a never-binding gate must equal `ungated`
  state-for-state (section 5).
- `W_block` — `gated` + bank-0 W production cut, timed (D3) so W depletes to 0 during an *actual
  succession cycle*, stalling the coordinator MODE transition (`_cap` = 0 ⇒ mode refused) while the
  organism is alive. The measured effect is per-field: `ctrl_writes` stops, the phase freezes
  mid-cycle, content writes also stop (already W-gated), and the organism then dies via the AC13
  attention-hijack cascade.
- `W_rescue` — `gated` + the same cut, then a machinery-only rescue (AC92 `restore_W` shape:
  re-seed `life[:4]`/`pos[:4]`, label EXTERNAL; or an endogenous un-block before the last W dies —
  D3 chooses). The stalled succession then completes from its frozen phase.

D4 may add the load-bearing control `no_repair` (loop cut via `no_policy_write`) to assert the
produced machinery is what is doing the work, matching AC88/AC92's control set. This is D4's call
and is out of D2's scope except that the runner must retain the `ac_arm`/cut plumbing already
present in ac92.py so the arm can be added without a structural change.

## Clean-control / equivalence expectation (declared up front)

Because W is at a deterministic steady state of 3 throughout normal operation, `8*W = 24 >= 21` (the
largest possible MODE transition), so the added W condition in the MODE refusal never binds and the
budgeted LAST write's `_cap` is never below its ungated energy/material budget. Therefore, with no
interruption, **`gated` and `ungated` must be state_hash-identical on every (seed, history, damage,
corrupt, transition) condition.** This identity is the proof that the gating is inert when the
machinery is healthy and that any difference observed in `W_block`/`W_rescue` is attributable to the
gating alone. D2 verifies it on engineering seeds against the frozen AC88 rows and against the
in-runner `ungated` arm; it is the primary clean-control gate for the final study.

## Source files this builds on (frozen; hashed only at D4 freeze)

`ac93.py` will be a new file derived from `ac92.py` (which is itself derived from `ac91.py` /
`ac88.py`). The frozen dependencies it must reproduce the comparator from: `ac88.py` (or its frozen
results), `ac76.py`, `ac71.py`, `ac12.py`, `ac12_memory.py`, `ac9.py`, `ac9_priority_v2.py`,
`ac9_memory.py`, `ac5.py`, `ac5_program.py`, `ac4.py`, `ac4_transport.py`, `ac1.py`. The exact
`SOURCES` list is settled at D4, per the frozen-version discipline.

## Explicitly deferred (not decided here)

- The exact interruption/rescue ticks (D3).
- The gate list and final seeds (D4, disjoint from all prior final families).
- Whether to include `no_repair`/`unmaintained` in the final arm set (D4).
- The `SOURCES` hash list and protocol freeze (D4).

## Errata (D2 engineering, 2026-09-18)

**E1 — the section-5 clean-control expectation is falsified.** Section 5 declares that with W at the
steady state 3, `8*W = 24 >= 21` (the largest MODE transition) so the added W term never binds and
`gated == ungated` state_hash-identical on every condition. Engineering (ac93.py, seeds 0-7) found
this is false on every damage=True condition. The error is that section 5 reasoned only about the
MODE field's 21-replica bound; the **LAST field is a separate 14-bit timestamp whose succession-start
write is bounded by the timestamp *delta*, not by 21.** Going from the previous start tick to the new
one differs in 35-69 replicas (traced), which exceeds `8*W = 24`. Under the gate the budgeted LAST
write truncates the timestamp to its low ~3 bits on *every* succession, so `last` reads back as a
small number, `now - last >= SUCC_MIN_SPACING` is satisfied ~immediately after each succession, and
successions fire as fast as the damage trigger allows (~80-130 ticks apart) instead of ~2400:
**86-137 successions vs 6-7 (ungated), ctrl_writes 7.8k-13k vs 0.72k-0.84k, and seed 1 dies at
t=13079 (energy -7) in both histories.** The ungated comparator reproduces frozen AC92 byte-for-byte
(32/32 state_hash), so the divergence is attributable to the gate alone. The MODE field is fine: at
W=3 the gated MODE refusal never binds, exactly as section 5 claimed.

The deeper point: Decision 2 item 2 carried AC88's claim that "a partially-updated timestamp cannot
corrupt the state machine". That is true of a *torn* timestamp (valid 14-bit integer), but false of a
*permanently truncated* one: a small `last` disables the succession rate limiter, which is
load-bearing (it prevents the organism spending itself to death on continuous succession). The AC88
"distinct resource" declaration was load-bearing for the rate limiter's integrity, not a modeling
convenience.

**E2 — Decision 2 item 2 amended: the LAST field is NOT W-gated (D3, 2026-09-18).** Resolution of E1.
The rate-limit timestamp is BOOKKEEPING, not a coordinator state transition: its succession-start
write is bounded by the timestamp VALUE DELTA (~35-69 replicas), not by any fixed transition size, so
the W cap `8*W=24` structurally cannot fund it (verified: 49/69/56/57-replica starts). The fix is
option (b) from `AC93_ENGINEERING_v1.md`: the MODE field (active + phase) remains W-gated (atomic under
`_cap`); the LAST field (timestamp) keeps the AC88 distinct-resource budget (energy + material alone,
never 8*W). This is a Decision 2 change, recorded as an errata not a silent edit. With it, the rate
limiter is restored in the gated arm (6-7 successions per 16,384 ticks, matching ungated), the ungated
comparator remains byte-identical to frozen AC92, and the clean-control failure of E1 is gone.

**E3 — the clean control is not byte-identical: W oscillates 2↔3 and the gate binds at W=2 (D3,
2026-09-18).** Section 5 declares W is "at a deterministic steady state of 3". The steady state is
DYNAMIC: W oscillates between 2 and 3 as catalysts die (life 64) and are re-born. The 21-replica
SWITCH→REMOVE transition (the largest mode transition) therefore exceeds `8*W=16` whenever W dips to 2,
and the gated MODE write is refused (retried 1-2 ticks later when W returns to 3). Measured: the
divergence appears on ~4/8 engineering seeds (1, 2, 4, 5 of 0-7) on every damage=True condition (e.g.
seed 1: 6 vs 7 successions, ctrl_writes 742 vs 825; seed 4: 776 vs 748), always at W=2 during
SWITCH→REMOVE, always a 1-2 tick delay — never a structural change. Consequence: the section-5
byte-identity clean control is REFRAMED, not repaired:

- Runner correctness is established by the **equivalence check** (ungated == frozen AC92 `intact`,
  byte-for-byte state_hash) — this holds 32/32.
- The **gate-inertness clean control** is replaced by a **quantified near-equivalence**: gated == ungated
  on every condition where W=3 at every transition; where they differ, the difference is fully explained
  (traced) by W=2 gate-binding at the 21-replica SWITCH→REMOVE transition, and is bounded (1-2 ticks).
  This is itself a signature of the graded W-dependency (the gate binds at W=0 for all transitions, W=1
  for >8-replica transitions, W=2 for the >16-replica SWITCH→REMOVE only), not a defect to eliminate.

No Decision is changed by E3 (the gate is `_cap`, exactly as decided); E3 records that the clean-control
*expectation* was stated too strongly because "steady state 3" was read as a constant rather than a
dynamic fixed point.
