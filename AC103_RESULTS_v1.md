# AC103 results v1: persistent triggering restores reconstruction in five of six staged-recovery failures; recovery and survival remain separable, and neither tested spending policy resolves every combined-challenge failure

Parent: AC102. Frozen per `AC103_PROTOCOL_v1.md` (hashed before the first final seed). Runner
`ac103.py` (a parametrized copy of `ac102.py`'s `both` arm, with the reconstruction's TRIGGER and
per-tick SPEND as the only changes). Seeds **5600-5607** (fresh, untouched, disjoint from every
prior family), 2 histories, 5 arms, 80 rows, 16,384 ticks.

**Headline:** Persistent triggering restores reconstruction in five of six staged-recovery failures.
Recovery and survival remain separable: some organisms reconstruct successfully and still die.
Neither tested spending policy resolves every combined-challenge failure. The staged reconstruction
fails because the program's majority repair (action 2) cements the corruption and removes the
reconstruction's trigger — a **premature termination** of repair, not a price problem — and a
persistent trigger (fire until the decoded program matches the description-derived target) restores
`fw == 0` on five of the six seeds where `current_staged` stalls (5601, 5602, 5604, 5605, 5606).
But the fix is not universal: on one seed (5607) the slow budget-8 reconstruction is still starved
before completion (`fw == 1`), and the **resource shortage** — the reconstruction and the paid
decision write sharing one material budget — remains a distinct survival failure that neither
persistence nor a state-dependent defer closes. See `AC103_ERRATA_v1.md` for the corrected
recovery denominator and the defer's scope.

## Verdict

**Three of six gates pass; G2, G3, G4 fail, recorded not moved.** The question — "is the staged
reconstruction failure resource shortage or premature termination of repair?" — is answered by
separating two levels:

- **Premature termination is the RECOVERY failure, and persistence mostly closes it (G2 FAIL on
  1/8).** `current_staged` fails to recover (`fw > 0`) and dies on **6/8** seeds (5601, 5602,
  5604, 5605, 5606, 5607; fw 1-4), each with 18-22 cementing writes (`action2_cementing`).
  `persistent_staged` recovers `fw == 0` on **7/8** (14/16), but two of those — 5600 and 5603 —
  already recovered under `current_staged` (`fw == 0`) and are not staged-recovery failures. Of the
  six seeds where `current_staged` actually stalls, persistence closes the cementing stall on five
  (5601, 5602, 5604, 5605, 5606). On 5607 it does NOT: the persistent budget-8
  reconstruction is starved (dies 8408 with `fw == 1`), because the slow reconstruction cannot
  outrun the cementing and the material drain. G2's universal-recovery predicate is falsified by
  exactly this one seed.
- **Resource shortage is a SURVIVAL failure, distinct (G3/G4 FAIL).** The marginal seed
  5603 (material 65 at the corruption tick) dies under every arm: `current`, `persistent`,
  `current_staged` and `persistent_staged` all die 8409 with `fw == 0` (reconstruction complete,
  yet the organism still dies), and `persistent_defer` dies 8410 with `fw == 2` (the
  defer stalls the reconstruction to fund the decision write, and the decision still cannot
  complete). Persistence does NOT rescue the marginal death; the defer does NOT rescue it either
  (G3, G4 fail). The defer's rescue is seed-dependent: it rescued the engineering marginal seed 1
  but not the final marginal seed 5603.

The two failure modes are therefore **distinct and bite at different levels**: premature
termination is a recovery failure (the trigger disappears, `fw > 0`), closed by persistence on
most but not all seeds; resource shortage is a survival failure (the organism dies with `fw == 0`,
or starves the reconstruction mid-flight), not closed by either persistence or a simple defer.

## Per-seed outcome (both histories identical)

| seed | priority   | mat@8192 | current (imm)  | current_staged (budget 8) | persistent (imm) | persistent_staged | persistent_defer |
|------|------------|----------|----------------|---------------------------|------------------|-------------------|------------------|
| 5600 | `[2,1,3,0]`| 120      | S, fw0         | S, fw0                    | S, fw0           | S, fw0            | S, fw0           |
| 5601 | `[1,0,3,2]`| 127      | S, fw0         | **D8292, fw4**            | S, fw0           | S, fw0            | S, fw0           |
| 5602 | `[2,1,3,0]`| 102      | S, fw0         | **D8275, fw1**            | S, fw0           | D8408, fw0 (streak 5) | S, fw0    |
| 5603 | `[1,2,3,0]`| 65       | **D8409, fw0** | **D8409, fw0**            | **D8409, fw0**   | **D8409, fw0**     | **D8410, fw2**   |
| 5604 | `[1,3,0,2]`| 112      | S, fw0         | **D8284, fw1**            | S, fw0           | S, fw0            | S, fw0           |
| 5605 | `[3,0,1,2]`| 105      | S, fw0         | **D8308, fw4**            | S, fw0           | D12541, fw0       | S, fw0           |
| 5606 | `[1,0,2,3]`| 125      | S, fw0         | **D8285, fw2**            | S, fw0           | S, fw0            | S, fw0           |
| 5607 | `[2,3,1,0]`| 83       | S, fw0         | **D8294, fw1**            | S, fw0           | **D8408, fw1**    | S, fw0           |

"S" = survives; "D< tick>" = dies at < tick>; "fw N" = `flipped_still_wrong` (corrupted bits still
wrong at end / at death). Recovery: `current` 16/16, `current_staged` 4/16, `persistent` 16/16,
`persistent_staged` 14/16, `persistent_defer` 14/16. Survival: 14/16, 2/16, 14/16, 8/16, 14/16.

## The two failure modes, measured

1. **Premature termination (cementing removes the trigger) — a recovery failure.** On every
   `current_staged` stall seed, `action2_cementing` is 18-22 (vs 0-6 under `current`): the
   program's action-2 majority restore writes correct replicas toward the wrong majority, cementing
   the 4/7 flip, and drops obs bit 2's minority count to zero — so the current trigger goes silent
   mid-reconstruction. The persistent trigger (`reg_trigger OR program_incomplete`, where
   `program_incomplete` is "the decoded program still differs from the description-derived target")
   keeps firing until completion, which is why `persistent_staged` recovers `fw == 0` on 5601/5602/
   5604/5605/5606. This quantifies the AC102 "majority repair reverses reconstruction progress"
   question directly: the cementing write is present and is what the persistent trigger overcomes.

2. **Resource shortage (the shared material budget) — a survival failure, and a starvation of the
   slow reconstruction.** On 5603 the immediate reconstruction already completes (`fw == 0`) but the
   organism dies 8409 — the material spend crosses the obs-bit-1 threshold, the material contact on
   the stale route is unproductive, the paid Gray streak stalls (4 < 6), and W/C collapses. On 5607
   the same budget bites the recovery itself: the budget-8 reconstruction is 4× slower than
   immediate, the cementing (18 writes) keeps re-corrupting, material drains, and the organism dies
   8408 with the reconstruction still one bit short (`fw == 1`). Resource shortage can therefore
   present as EITHER `fw == 0` (complete-but-dies) OR `fw > 0` (starved-mid-reconstruction); in both
   cases the trigger was fine — persistence does not help.

3. **The state-dependent defer is seed-dependent (G3/G4), and its scope is narrower than a
   budget-preservation policy.** Deferring the reconstruction while `material ≤ 64` frees material
   for the paid decision write: on the engineering marginal seed 1 this let the streak reach the
   drop threshold and the organism re-acquire. On the final marginal seed 5603 it did not — the
   defer stalled the reconstruction (dies 8410 with `fw == 2`) and the decision still did not
   complete. Two scope limits (see `AC103_ERRATA_v1.md`): the defer is gated on
   `now >= CORRUPT_TICK` (advance knowledge of the challenge tick, not a fully internal policy), and
   it defers only *while material is already at/below 64* — it does not cap total spend to keep the
   decision budget, so an organism just above 64 can still spend its way below the threshold. Its
   failure therefore tests "stop once scarce," NOT "limit spending to preserve a decision budget,"
   and does not reject the budget-preservation hypothesis.

## Gates (prespecified in the protocol)

- **G1 arm identity — PASS 16/16.** `current` is byte-identical to AC102 `both` and
  `current_staged` to AC102 `staged` on every final individual (the frozen references).
- **G2 persistent staging completes reconstruction — FAIL.** `persistent_staged` recovers on 7/8
  seeds, not 8/8: 5607 dies with `fw == 1` (the persistent reconstruction is starved before
  completion). Recorded, not moved.
- **G3 the state-dependent defer preserves adaptation resources — FAIL.** `persistent_defer` dies
  on 5603 with `fw == 2` (recovery incomplete). Recorded, not moved.
- **G4 the two failure modes are distinct — FAIL.** On 5603 `persistent_staged` dies (`fw == 0`)
  and `persistent_defer` also dies (`fw == 2`), so the defer does not rescue every
  persistence-residual death. Recorded, not moved.
- **G5 state sufficiency (observer-discard) — PASS 16/16.** Per-tick observer-discard on `current`
  byte-identical. The persistent arms add no host-side state by source inspection (the trigger is
  derived from the maintained program + description); the direct per-tick observer-discard test was
  run on `current`, not the persistent arms (see `AC103_ERRATA_v1.md`).
- **G6 completeness + determinism — PASS.** 80 rows; sampled exact rerun byte-identical.

## Reported, not gated

- **The budget trace** (per tick: material, `reg_writes`, `streak_writes`, `action2_writes`,
  `action2_cementing`, obs, fw) — the quantitative reversal measurement, recorded per row.
- **The persistence speedup.** `persistent` (immediate) recovers at t≈8193 where `current` is
  cementing-delayed (t≈8226-8273); the immediate schedule's OUTCOME (survival) is unchanged.
- **The second-move death** (5605 persistent_staged dies at 12541, AC102's second-move mode).
- **Seed-dependent defer.** The defer rescued the engineering marginal seed 1 and survived the
  other engineering seeds, but fails on the final marginal seed 5603 — AC39's transfer lesson in
  the unfavourable direction for a sub-finding.
- The material level at the corruption tick and each seed's priority — measured covariates,
  reported not prespecified (untouched seeds).
- Survival is a bimodality-aware lower bound (AC68). No autopoiesis claim; `advance()` and
  `prog.choose` remain supplied format-level machinery.

## Verification

- `audit_ac103.py` passes: source hashes no drift; the six gates re-derived from the saved table
  WITHOUT simulating and matching the recorded result (including the G2/G3/G4 failures);
  seed-disjointness; per-arm invariants (corruption applied and recovered, `persistent_staged`
  recovers 14/16, cementing write present on every staged stall, every `persistent_staged` death
  is a recovery-complete `fw == 0` or the 5607 starvation).
- `replay_ac103.py` passes: first-row rerun byte-identical; arm-identity matches recorded on all
  individuals; observer-discard per-tick byte-identical on the sample.
- `test_ac103.py` green: arm identities, the persistent trigger (inert on the marginal immediate
  schedule, load-bearing where cementing stalls), the majority-level completion condition, the
  resource-shortage / premature-termination distinction, the defer gating (byte-identical before
  the corruption tick), and the cementing counter.
- Core AC1-9 suite (56 tests) green. No frozen runner modified (`ac102.py`, `ac101.py` and every
  earlier freeze untouched).

## Boundary and next step

The answer to AC102's open question is that the staged failure is **premature termination at the
recovery level** (cementing removes the trigger), closed by a persistent trigger on five of six
staged-recovery failures. Recovery and survival are separable: some organisms reconstruct
successfully and still die (5602, 5605). Neither tested spending policy resolves every
combined-challenge failure — the observed failures persist under both the persistent trigger and a
state-dependent defer, and on one seed (5607) the reconstruction is starved mid-flight. An
unavoidable funding limit has NOT been established: the defer in particular tests "stop once
scarce," not a spending policy that caps total spend to preserve the decision budget. What
persistence establishes is that the reconstruction's completion condition is internally determinable
and sufficient to outrun the cementing on five of six stalled seeds; what it does not establish is
that a budget-8 reconstruction can always be funded on a marginal economy. The next step is not a
better trigger but a reconstruction whose per-tick spend is itself governed by the organism's
internal state so that it neither crosses the obs-bit-1 threshold nor starves the paid decision
write — a state-dependent budget priority, out of scope here. Boundary unchanged: no autopoiesis
claim; `advance()` + `prog.choose` supplied; the reserve still not part of the architecture. All
earlier results preserved untouched.
