# AC108 protocol v1 — cognitive-organizational coupling, both directions, selective interventions (K7)

Written before any final-seed run. This is the K7 deliverable (task t_c57abbd1): test, separately and with
selective interventions plus matched comparisons, the two coupling directions between the K6-maintained
cause-estimate (the "cognitive"/representational machinery) and the organism's organizational maintenance.

The K6 freeze (`ac107.py`, finals 6000-6007) established: the one-bit maintained cause-estimate e in
{E_world=1, E_machinery=0} discriminates the two causes at decision times with 0 mistakes, and the
discrimination depends on the maintained storage's content (observer-discard state sufficiency 16/16 +
no-cause identity 16/16). K6's negative: the causal role (scramble) and the survival advantage (vs r2/r4)
did NOT transfer to the fresh family — the cut's death bite is specific to priority [3,0,2,1] (engineering
seed 4 only), so a survival contrast is seed-bounded. K7 answers the coupling question with the mechanism
now real and maintained, WITHOUT resting any gate on a survival contrast that only bites on the
priority-corner seed.

---

## 1. The question, two directions (separate)

- **Direction 1 — organizational maintenance -> representational accuracy and use.** Does the organism's
  own paid maintenance of the representation sustain its accuracy and use?
- **Direction 2 — representational function -> adaptation / production / viability.** Does the
  representation's content causally drive adaptation and affect production/viability, above what an
  externally supported fixed threshold achieves?

Causal dependence (a forced content / cut maintenance changes behaviour per individual) is gated (G1-G4)
and reported SEPARATELY from superior performance (the candidate's survival/adaptation edge over the
externally supported rivals r2/r4, reported not gated — K6's lesson).

## 2. Integration decision (deliverable 1, stated not assumed)

The K6 mechanism already runs on the K3-assessed autonomy baseline's machinery: `ac95.maintain`
(succession, reconstruction, description/pointer/ctrl repair) and the W-gated paid writes are inherited
UNCHANGED by `ac107.py`. The only AC105-specific features absent from the AC107 world are the corruption
challenge and the allowance-42/persistent-trigger decision-spending refinements; both are orthogonal to the
maintenance<->representation coupling, and a corruption event at the same tick as the cut/move would be a
THIRD cause confounding the two-cause discrimination. The existing AC107 configuration therefore suffices.
This is re-verified empirically by G6: the new runner reproduces the frozen arms byte-for-byte
(`state_hash`), so the extension is inert for them.

## 3. Arms (6) and conditions (3)

Conditions: `no_cause` (neither cause), `move` (E_world: channel-1 mapping flips at t=8192, route stale),
`cut` (E_machinery: the organism's read of route-1 is suppressed for [8192, 8192+96), entry intact).

| arm | what it is | role |
| --- | --- | --- |
| `candidate` | the maintained cause-estimate (K6 mechanism, unchanged) | both directions: baseline |
| `no_write` | the estimate's paid W-gated write is disabled; the read stays honest | **direction 1**: selective maintenance disruption |
| `scramble` | the estimate's READ is forced E_world; the write stays intact (K6's scramble) | **direction 2**: content intervention |
| `force_machinery` | the estimate's READ is forced E_machinery; the write stays intact | **direction 2**: content intervention |
| `r2` | frozen Gray streak (STREAK_N=6), no representation | **direction 2**: externally supported comparison |
| `r4` | longer raw counter (HOLD_N=24), no representation | **direction 2**: externally supported comparison |

The frozen arms (candidate/r2/r4/scramble) resolve through `ac107`'s own factory, so they are
byte-identical to the K6 freeze by construction (G6 re-verifies it). `no_write` and `force_machinery`
differ from the candidate ONLY in one flag each (write disabled / read forced), so any contrast is
attributable to that flag.

A disclosed asymmetry of the one-bit design: the acquired value is E_world (1) and the cut's correct value
is E_machinery (0), so (a) the paid write is load-bearing exactly in the cut, and (b) forcing E_world
(`scramble`) is inert absent a cause while forcing E_machinery (`force_machinery`) activates the
proactive-renewal consumption even absent a cause. Both are stated, not hidden (G5 encodes them).

## 4. Endpoints (registered separately; none implies another)

- **Accuracy** (direction 1): `bel_at_cut_end` (cut) / `bel_at_first_drop` (move), per individual.
- **Use** (direction 1): relinquishments, route retention, re-acquisition ticks, per individual.
- **Adaptation** (direction 2): relinquishments, re-acquisition, route retention, per individual.
- **Production** (direction 2): W/C population, energy, material, total writes, proactive writes, per
  individual (the production collapse of holding a stale route is read off W/C/energy at death).
- **Viability** (both): `completed` / `first_dead`, reported as a bimodality-aware lower bound, NOT gated.

## 5. Gates (prespecified)

- **G1 maintenance→accuracy (robust):** candidate reads E_machinery (bel=0) at cut end in 16/16; no_write
  reads E_world (bel=1) at cut end in 16/16; no_write `bel_writes == 0` and `bel_attempts == 0` in 16/16
  (the intervention actually cut the write).
- **G2 maintenance→use (non-vacuity declared):** candidate holds (0 relinquishments) in cut 16/16; no_write
  relinquishes in cut on >=1 individual where the candidate holds. The relinquishment bites only where the
  streak reaches 6 within the 96-tick window (K6's priority-corner condition). If no final individual
  exhibits it, G2 fails vacuously and is recorded, not moved.
- **G3 content→adaptation, move side (robust):** candidate relinquishes >=1 in move 16/16; force_machinery
  holds (0 relinquishments) in move 16/16 — the forced E_machinery content reverses the adaptation.
- **G4 content causal, cut side (non-vacuity declared):** candidate holds in cut 16/16; scramble
  (E_world content) relinquishes in cut on >=1 individual. Same non-vacuity note as G2.
- **G5 clean control:** no_write and scramble are byte-identical (`state_hash`) to the candidate in no_cause
  16/16; force_machinery differs from the candidate in no_cause ONLY by the proactive-renewal spend, with
  identical survival, routes, relinquishments and demand (the forced E_machinery content's disclosed
  consequence).
- **G6 frozen-copy reproduction:** ac108's candidate/r2/r4/scramble reproduce ac107's runs byte-for-byte
  (`state_hash`) on the sampled cells (all final seeds x both histories x move/cut). The extension is inert
  for the frozen arms.
- **G7 completeness/determinism:** row count == 8 seeds x 6 arms x 3 conditions x 2 histories = 288, and a
  re-run of the first row reproduces its `state_hash`.

Reported, NOT gated (superior performance): per-arm survival counts and the candidate-vs-r2/r4
per-individual dominance table. A survival contrast that only bites on the priority-corner seed is vacuous
on a fresh family (K6), so viability is reported as a lower bound, not gated.

## 6. Cohort selection

Final seeds **6100-6107** (8 seeds x 2 histories = 16 individuals), fresh and disjoint from every prior
family (engineering 0-7; 4412-4950; 5100-5508; 5600-5607; 5700-5707; 5800-5807; 5900-5907; 6000-6007).
Engineering seeds 0-7 are excluded from the final sample (AC39).

## 7. Stopping rule

A clean negative on any gate is a finding, not a program failure (the card's FALSIFICATION clause). Do not
move a prespecified gate after seeing the result; record the failure and supersede on fresh seeds only if
the mechanism changes (K6's constraint). Both directions are answered when G1-G7 are evaluated and the
per-direction causal-dependence vs superior-performance tables are written.

SOURCES (declared): ac108.py ac107.py ac106.py ac99_d2.py ac99.py ac97.py ac96.py ac95.py ac76.py ac71.py ac12.py ac12_memory.py ac9.py ac9_priority_v2.py ac9_memory.py ac5.py ac5_program.py ac4.py ac4_transport.py ac1.py AC108_PROTOCOL_v1.md
