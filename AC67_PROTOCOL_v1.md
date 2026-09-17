# AC67 protocol v1: the repair loop is load-bearing under non-self-reversing damage

Hashed before the final run. Fresh seed family. The engineering run (`AC67_ENGINEERING_v1.md`)
informed the endpoints but is excluded from the final sample.

## Claim

With non-self-reversing (sticky) program-bank damage and a single-replica register read, the organism's
own paid repair maintains its own decision state against persistent corruption; cutting the repair link
degrades the register and the degradation propagates to the organism's survival.

This is a "cannot hold without repair" claim, so it is gated categorically on complete separation
(separation of minima/dominance), not on a mean margin.

## The one declared change from the frozen physics

`b.traces[0,:126] ^= core_flips` → `b.traces[0,:126] |= core_flips` (sticky SET, not toggle). The memory
bank's damage is untouched. Register read convention: `REGISTER_THRESHOLD = 1` (single designated
replica). Everything else — the register's location in the dead rule's mask bits, the paid bank-0 repair,
the core-W funding, the action-6 production, the conservation laws — is the frozen AC12/AC9 machinery.

## World constants

- `PORTS=4`, `YIELD_M=64`, `YIELD_F=64`, `TICKS=4096`, `DEV=512`.
- No post-development move (`MOVE_KEYS=()`, `MOVE=10**9`).

## Arms

- `closed`: the loop intact (repair enabled).
- `no_repair`: the program-bank repair link cut via the frozen `no_policy_write` guard.
- `protected_closed`, `protected_no_repair`: scaffold controls — the program `choose` and the register
  read use a protected shadow copy of the program bank. Their shadow register is **not** in bank 0, so
  the paid repair cannot reach it; they are recorded for completeness and are **not** part of the primary
  gates.

## Endpoints (per individual)

- `register` (final 4-bit read), `register_any_flip`, `first_register_flip`.
- `first_dead`, `activity`, `completed`.
- `routes`, `demand`, `program_bits_damaged`, `rules_touched`.
- `state_hash`, `ledger`, `final_inventory`.

## Prespecified gates (8 individuals = 4 seeds × 2 histories, per arm)

- **G1** — `no_repair`: `register_any_flip` is True in **all 8** individuals.
- **G2** — `no_repair`: `first_dead` is not None in **all 8** individuals.
- **G3** — `closed`: `register_any_flip` is False in **all 8** individuals.
- **G4** — `closed`: `first_dead` is None in **all 8** individuals.
- **G5** — causal order: in every `no_repair` individual, `first_register_flip < first_dead`.

The claim passes iff G1–G5 all pass. A single failing individual on any of G1–G5 falsifies the claim;
thresholds will not be moved.

## Seeds

Finals: `2600, 2601, 2602, 2603`. Engineering seeds (0,1,2) are excluded and disjoint.

## Verification

`audit_ac67.py` recomputes gates and invariants from the saved table without simulating;
`replay_ac67.py` does sampled exact reruns; `test_ac67.py` pins the gate shape and the recorded outcomes.
The frozen source of truth is this protocol plus the runner and its frozen dependencies.
