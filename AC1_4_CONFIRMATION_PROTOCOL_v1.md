# AC1–AC4 foundational-claims confirmation protocol (confirmatory v1)

Date: 2026-09-17. Written before the confirmatory run. This study re-runs the
decisive contrasts of the four foundational constituent claims — AC1 (a
vulnerable acquired controller paying for its own repair), AC2 (produced W
repair catalysts), AC3 (produced C energy converters), AC4 (a produced B
boundary with measured transport, and long-horizon controller-repair
dependence) — on **fresh seeds disjoint from every engineering and follow-up
seed** used to produce the original evidence. It is a same-author confirmatory
study, not external preregistration, not independent scientific review, and not
a claim of full autopoiesis.

## Why this study

The four claims that AC1–AC4 establish are the foundational constituents of the
whole AC line (status item 28: "Independent review and new confirmatory
protocol — NOT DONE"). Their original evidence is engineering-only: the seeds
that fixed the arm definitions and the rates were also the seeds reported.
Every later study in the line (AC9 controls v3, AC10, AC15, AC18, AC67, AC71,
AC75, AC76) was frozen on fresh, disjoint seed families; AC1–AC4 were not. This
study supplies that missing step by re-running each claim's decisive contrast
and its validity controls on new seed families, with the gates written down
before any confirmatory seed is run.

The frozen simulation code is reused **unmodified** (`ac1.py`, `ac1_followup.py`,
`ac2.py`, `ac3.py`, `ac4.py`, `ac4_transport.py`). No physical parameter,
reaction law, representation, or arm is changed. A confirmatory failure here
would mean the engineering result does not transfer to fresh seeds (AC39's
lesson); a pass means each foundational claim now stands on a frozen,
audit-verified, fresh-seed sample as well as its engineering sample.

## Fresh seed families

All families are disjoint from every AC1–AC4 engineering/follow-up seed
(0–7, 0–15, 0–3, 100–107, 1000–1031) and from every later AC-line seed family.
Seeds are the replication unit; rates and arms are repeated conditions, not
independent individuals.

| Study | Seeds | Count |
| --- | --- | --- |
| AC1 confirm | 5100–5107 | 8 |
| AC2 confirm | 5200–5215 | 16 |
| AC3 confirm | 5300–5307 | 8 |
| AC4 short (transport) | 5400–5407 | 8 |
| AC4 long (repair dependence) | 5500–5507 | 8 |

## Configurations (rates) and arms

Rates are the configurations at which the corresponding original claim was
robust; they are fixed here, not selected after seeing these results.

**AC1 confirm** — frozen `ac1` + `ac1_followup`, 3,000 ticks, `pulse=False`,
p ∈ {0.0005, 0.001}. Arms: `self`, `no_policy_write` (paid controller-write
ablation), `free_policy_ablation` (controller-write cost refunded), `protected`.

**AC2 confirm** — frozen `ac2`, 4,096 ticks, p ∈ {0.00025, 0.0005}. Arms:
`self`, `no_synthesis`, `no_synthesis_rescue`, `protected`, `self_clamp`,
`no_synthesis_clamp`.

**AC3 confirm** — frozen `ac3`, 4,096 ticks, p ∈ {0.0001, 0.0002, 0.0004}.
Arms: `self`, `no_C`, `no_C_rescue`, `no_C_energy`, `protected`, `self_energy`,
`no_W_energy`.

**AC4 short (transport)** — frozen `ac4`, 2,048 ticks, p ∈ {0.00005, 0.0001}.
Arms: `self`, `no_B`, `no_B_rescue`, `no_B_retention`, `protected`.

**AC4 long (repair dependence)** — frozen `ac4`, 8,192 ticks,
p ∈ {0.00005, 0.0001}. Arms: `self`, `no_policy_write`, `protected`,
`no_B_retention`.

## Gates

Gates are prespecified per study and per rate. A **claim gate** failing at any
declared rate falsifies that study's confirmatory claim; the result is then
recorded and the protocol is not amended. **Control gates** (marked "scope
note") validate the arm setup and are reported, but a scope-note failure does
not falsify the claim (it signals a harness problem to diagnose). Contrasts use
the paired per-individual difference with a descriptive 95% percentile
bootstrap (10,000 resamples, generator seed 20260914); the "lower bound > 0"
condition uses the bootstrap interval's 2.5th percentile.

### AC1 confirm gates (per rate)

- **G1 self viability (claim):** all 8 `self` individuals complete; mean `self`
  active fraction ≥ 0.90.
- **G2 paid repair dependence (claim):** `self − no_policy_write` active
  fraction, mean ≥ 0.20 and interval lower bound > 0.
- **G3 free-ablation independence (claim):** `self − free_policy_ablation`
  active fraction, mean ≥ 0.20 and interval lower bound > 0.
- **G4 protected control (scope note):** all 8 `protected` individuals complete;
  mean `protected` active fraction ≥ 0.90.
- **G5 turnover (claim):** every `self` individual has positive paid writes to
  all four banks (`bank_writes[k] > 0` for k = 0..3) — persistence by
  replacement, not survival of untouched initial storage.

### AC2 confirm gates (per rate)

- **G1 self viability (claim):** all 16 `self` complete; mean activity ≥ 0.90.
- **G2 synthesis dependence (claim):** `self − no_synthesis` activity, mean
  ≥ 0.20 and lower bound > 0.
- **G3 catalyst rescue (scope note):** `no_synthesis_rescue` mean activity
  ≥ 0.90 and ≥ 14 of 16 complete.
- **G4 information under clamp (claim):** `self_clamp − no_synthesis_clamp`
  policy accuracy, mean ≥ 0.20 and lower bound > 0 (resource abundance preserves
  execution but not the acquired information).
- **G5 turnover (claim):** every `self` individual produces > 120 W
  (`ledger["births"] > 120`) and writes every bank (`bank_writes[k] > 0`).
- **G6 protected control (scope note):** `protected` mean activity ≥ 0.90.

### AC3 confirm gates (per rate)

- **G1 self viability (claim):** all 8 `self` complete; mean activity ≥ 0.90.
- **G2 C dependence (claim):** `self − no_C` activity, mean ≥ 0.20 and lower
  bound > 0.
- **G3 C rescue (scope note):** `no_C_rescue` completes 8/8; mean activity
  ≥ 0.90.
- **G4 W dependence under energy clamp (claim):** `self_energy − no_W_energy`
  policy accuracy, mean ≥ 0.20 and lower bound > 0.
- **G5 energy rescue restores activity only (scope note):** `no_C_energy` mean
  activity ≥ 0.90 (execution restored by external energy; the information
  contrast in G4 shows it is not organizational rescue).
- **G6 turnover (claim):** every `self` individual produces > 120 W, > 30 C,
  converts fuel (`converted > 0`), and writes every bank.

### AC4 short (transport) gates (per rate)

- **GA1 self viability (claim):** all 8 `self` complete; mean activity ≥ 0.90.
- **GA2 B dependence (claim):** `self − no_B` activity, mean ≥ 0.20 and lower
  bound > 0; and every `no_B` individual exports W/C
  (`ledger["particle_export"] > 0`).
- **GA3 rescues (scope note):** `no_B_rescue` and `no_B_retention` mean activity
  ≥ 0.90.
- **GA4 turnover (claim):** every `self` individual produces > 40 B
  (`ledger["B_birth"] > 40`).

### AC4 long (repair dependence) gates (per rate)

- **GB1 self viability (claim):** all 8 `self` complete; mean activity ≥ 0.90;
  mean `self` policy accuracy ≥ 0.99.
- **GB2 repair dependence (claim):** `self − no_policy_write` activity, mean
  ≥ 0.20 and lower bound > 0; and `no_policy_write` completes the horizon in at
  most 2 of 8 individuals (the repair ablation must break sustained activity in
  a clear majority — the follow-up observed 0/8; the ≤2 allowance keeps the gate
  off the survival-boundary knife-edge at the lowest rate, where a body without
  repair is genuinely near the boundary rather than far below it).
- **GB3 protected control (scope note):** all 8 `protected` complete; mean
  activity ≥ 0.90.

## Verification plan

- `pre_run_snapshot.json` records the sha256 of the protocol, the confirmatory
  runner, and every frozen source, **before** the confirmatory seeds run.
- `rows.jsonl` is written incrementally (one row per line) so an interruption
  cannot erase finished evidence; `results.json` aggregates.
- `audit_ac1_4_confirm.py` re-derives coverage, means, contrasts and every gate
  from the saved table **without simulating**, and checks the source hashes.
- `replay_ac1_4_confirm.py` performs sampled exact reruns (first seed of each
  study, every arm and rate) and compares against the saved rows.
- Verification tools are **not** hashed into the frozen snapshot (per the
  AC16/AC17 lesson); their hashes are recorded separately in `results.json`.

## Claim boundaries

A full pass confirms, on fresh seeds, the four foundational constituents:
acquired controller information drives and receives paid maintenance (AC1); that
maintenance requires produced, decaying W catalysts (AC2); energy for
maintenance requires produced C converters (AC3); and the produced B boundary
retains the machinery via transport while controller repair enables sustained
activity at the long horizon (AC4). It does not establish autonomous need
acquisition, a self-produced controller, rich development, full autopoiesis or
subjectivity. Those remain governed by the later frozen studies and the
structural gap recorded in `DEPENDENCY_AUDIT_v1.md`.
