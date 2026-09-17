# AC67 results v1: the repair loop is load-bearing — gates G2–G4 pass, G1/G5 falsified by a second mechanism

2026-09-16. Final seeds 2600–2603 (4 seeds × 2 histories = 8 individuals per arm), hashed protocol
`AC67_PROTOCOL_v1.md`. Engineering seeds (0–2) excluded.

## Gate outcomes (prespecified)

| gate | statement | result |
| --- | --- | --- |
| G1 | `no_repair` register degraded in all 8 | **FAIL** (6/8; seed 2601 register stays `[0,0,0,0]` in both histories) |
| G2 | `no_repair` dies in all 8 | **PASS** (8/8, deaths 436–742) |
| G3 | `closed` register intact in all 8 | **PASS** (8/8, `[0,0,0,0]`) |
| G4 | `closed` survives in all 8 | **PASS** (8/8) |
| G5 | `no_repair` register flips before death in all 8 | **FAIL** (seed 2601 has no register flip) |

The claim as written — "cutting the repair degrades the *register* and that propagates to survival" — is
**falsified**: in one of eight individuals the organism dies with the register never reading
"relinquished". The threshold is not moved.

## What survives the falsification, and what it is

The **survival separation is complete and clean**: 8/8 survive with the repair link intact, 8/8 die with
it cut. That is the load-bearing result the line has been reaching for since AC12 — the paid bank-0
repair, funded by core W that the program itself produces, is causally necessary for the organism's
continued functioning under persistent program-bank corruption.

The death has **two paths**, and the register is only the majority one:

1. **Decision-state degradation (6/8).** A register replica is set by the sticky damage, the
   single-replica read flips to "relinquished", the allowance stops renewing that slot, the 64-tick entry
   lapses, and the organism dies with degraded routes. This is the register path G1/G5 captured.
2. **Observation hijack (2/8, seed 2601's two histories).** The sticky damage sets enough replicas in the
   *rules* that observation bit 2 (bank-0 corruption) fires permanently. The program — whose repair
   action is cut — cannot clear it, so it loops on "repair" (action 2, ×152) and "produce W/C"
   (action 6, ×3819), never acquires either route (`routes=[None,None]`, `demand=[0,0]`), and drains
   energy to death at t=594. The register never flips because the damage never happened to land on the
   four register replicas.

Both paths are the same underlying fact — the program bank (rules *and* decision register) is a maintained
constraint, and cutting its repair lets persistent damage propagate to death — but they are distinct
mechanisms, and the protocol's register-specific gates do not cover the second.

## The protected arms are confounded, not clean controls

`protected_closed` (8/8 survive) and `protected_no_repair` (8/8 die) track their live counterparts. But
the protected arm only swaps `choose` to read a shadow bank; the observation is still read from the live,
damaged bank, so the observation-hijack path is **not** shielded by the protected copy. The shadow
register is also outside bank 0, so the paid repair cannot reach it. These arms are therefore not a clean
scaffold control for the loop, and I do not lean on them.

## What this establishes and what it does not

Establishes: under non-self-reversing program-bank damage, cutting the repair link kills the organism in
8/8 individuals while the repair keeps 8/8 alive — the repair loop is **load-bearing**, not inert. This
corrects AC14's "inert loop" conclusion, which was an artifact of the `'_no_repair'` vs `'no_repair'`
substring bug (its `no_repair` arm never cut the repair).

Does not establish: a register-only mechanism (it is 6/8, with observation hijack the other path); full
autopoiesis; consciousness; optimality. The causal chain is measured, not assumed — `first_register_flip`
precedes `first_death` in every individual where the register path fires.

## Artifacts

`ac67.py`, `ac67_results_v1/` (rows.jsonl, results.json, pre_run_snapshot.json), `AC67_ENGINEERING_v1.md`
(the bug discovery), `AC67_PROTOCOL_v1.md`. Next: `audit_ac67.py`, `replay_ac67.py`, `test_ac67.py`.
