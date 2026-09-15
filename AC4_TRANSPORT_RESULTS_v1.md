# AC4 transport prerequisite: measured retention and leakage

2026-09-14. This is a transport-kernel result, not a self-produced boundary.

An explicit 20-link perimeter changes the motion of particles crossing it.
The model tracks positions in the interior and exterior, allows return from
outside, and separately accounts for export to an absorbing bath. Boundary
absence does not directly change health, energy or a mortality variable.

All 96 declared rows ran: 16 seeds, six paired arms, 512 particles and 256 ticks.

| Arm | Mean fraction inside at endpoint | Mean fraction not exported |
| --- | ---: | ---: |
| Open | 0 | 0 |
| Intact membrane | 1 | 1 |
| Membrane expires at step 32 | 0.000122 | 0.000488 |
| One missing perimeter link | 0.354492 | 0.384033 |
| Permeant particles, intact membrane | 0 | 0 |
| External retention rescue, no membrane | 1 | 1 |

Every intact trajectory retained all particles. Permeant and open trajectories
matched exactly, as did externally imposed reflection and intact-membrane
trajectories. All decaying-membrane trajectories retained their particles for
the first 31 steps and then allowed crossings after expiry. A single hole
permits substantial leakage: closure cannot be represented just by counting
most segments as present without tracking where transport can occur.

These are consequences of deliberately specified reflection/selectivity laws,
not discoveries of physical membrane chemistry. Perfect impermeability and an
absorbing external bath are modeling assumptions. No claim of boundary production,
organizational closure or biological adequacy follows from these tracer results.

Three mechanism tests verify every perimeter link in both crossing directions,
species selectivity, irreversible export, paired interventions and expiry.
The audit checked source hashes, unique coverage and exact replay of all 96
rows. Interior, exterior and exported inventories balance every tick.

## Required integration before an autonomy claim

1. Apply particle positions, motion, age and export to actual W and C. Tracers
   alone cannot establish a maintenance dependency.
2. Produce boundary constituents using precursor and C-derived usable energy,
   with W-mediated reactions. Record material bound in boundary and expiry waste.
3. Store boundary-maintenance decisions in the same vulnerable acquired policy.
   A protected low-boundary override would bypass the central research question.
4. Make reaction locality explicit. A particle outside must not remotely repair
   internal controller traces; exported components must not remain active in a
   hidden slot count. Daughter constituents need declared birth positions.
5. Test production ablation, external boundary rescue and matched retention
   rescue under paired transport inputs. Measure W/C loss and controller
   information alongside activity. Account for all externally supplied matter.
6. Extend whole-state erasure to positions, species, lifetimes and membrane state.
   Keep seeds and observer histories outside live dynamics.

Controller acquisition remains a separate open issue. Adding another demonstrated
maintenance rule cannot count as discovering a new need autonomously.

[Protocol](AC4_TRANSPORT_PROTOCOL_v1.md), [model](ac4_transport.py),
[tests](test_ac4_transport.py), [data](ac4_transport_results_v1/results.json),
[audit](ac4_transport_results_v1/audit.json).

Reproduce with `py -3.12-arm64 -B -m unittest -v test_ac4_transport`.
The original runner refuses an existing output directory; preserve its artifacts.
