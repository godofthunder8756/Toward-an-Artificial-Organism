# AC2 engineering protocol: acquired policy and produced repair catalysts

2026-09-14. Written before implementation runs. New engineering study, not an
E3 final experiment or an independently reviewed claim of full autopoiesis.
The preceding goal turn produced verified AC1 evidence: it was progress. The
broader goal remains active; AC1 did not satisfy all autonomy requirements.

## Hypothesis and scope

An acquired, vulnerable controller can sustain locally present, short-lived
repair catalysts through paid production, and those catalysts can sustain the
controller's acquired information. Both generative links must be causally
necessary over many catalyst lifetimes. This addresses the P↔W stage in
AC2_DESIGN_DIRECTION_v0_1.md, not the still-unimplemented converter or boundary.

The mechanism is conventional table acquisition, repetition coding and a
designer-specified catalytic production reaction. A positive result is a
model-relative mutual-maintenance witness, not a new algorithm, spontaneous
chemistry, autonomous goals, full metabolism or a self-produced organism.

## Fixed laws and finite state

Four banks hold 192 bits each with seven copies (5,376 logical trace bits).
Banks 0–1 encode 128 three-bit policy rows; banks 2–3 hold 384 arbitrary
payload bits. The seven observation bits are the AC1 six flags plus low W:
the minimum catalyst population across banks is below two. Table demonstrations
prefer food if energy<=48, precursor if material<=64, otherwise synthesis if W
is low, otherwise repair a flagged bank by a demonstrated permutation, else rest.
Damage flag threshold remains four minority copies. There are only 24 priority
permutations; nominal storage does not imply independent acquired policy entropy.

Each bank has four catalyst slots, each an integer remaining lifetime 0–64.
Initially three catalysts have remaining lifetimes 32,48,64. Every active tick
decrements positive lifetimes. A catalyst catalyzes up to eight trace writes
per action, without being consumed by those writes. Total cap remains 32.
Without catalysts, requested writes have zero effect and zero write cost.
There is NO artificial death threshold on catalyst count.

Action 6 attempts one new catalyst in every bank that has a surviving catalyst
and a free slot. Each birth consumes four free precursor units and two energy
units. Generic reaction: W + 4M + 2E → W + W_new + dissipated energy. Parent W
survives; the product gets lifetime 64. Banks with zero W cannot self-start.
Initial W is an explicit endowment, not claimed to have been self-produced.
Each W binds four material units. Expiry exports those four units as waste.
Fixed bank order is generic reaction scheduling, not a hidden damage allocator.

Every attempted effective trace write consumes one precursor and one energy,
replaces an old site with a new one, and exports one old-site unit as waste.
Trace site mass stays constant. Disabled policy writes are free (no replacement).
Living/decision cost is one energy. Food adds32, precursor adds64; reservoir
ceilings128/256, initial64/128. External supply is open but requires policy actions.

Live state consists only of traces, local catalyst lifetimes, bounded reservoirs
and termination. Teaching targets, original policy, seed, audits and observer
histories stay outside the live step. Generic sensing/decoding, catalytic laws,
clock, spatial addresses and reaction execution remain supplied. Banks are local
well-mixed compartments, not a self-produced spatial boundary or molecular dynamics.

## Causal interventions

| Arm | Change |
| --- | --- |
| self | All live decisions use vulnerable acquired policy |
| no_synthesis | Production is blocked; ineffective production is free |
| no_policy_write | Writes to policy banks blocked and free; catalysts/payload still maintained |
| protected | Explicit protected learned policy chooses actions; same W physics |
| no_synthesis_rescue | Production blocked, but external catalyst additions maintain at least three per bank, fully inventoried |
| self_clamp | Same vulnerable controller, energy/material reset to caps each tick with external inputs counted |
| no_synthesis_clamp | Production blocked, same reservoir clamp as self_clamp |

The clamped contrast isolates catalyst-mediated information preservation from
common energy/material deprivation; compare final policy accuracy, not survival
alone. The catalyst rescue tests whether blocked synthesis acts through W loss.
Direct deterministic tests intervene on the acquired SYNTH action and on W
availability while holding other state fixed. Protecting the interpreter remains
a scope limit even if these generative links pass.

## Pre-run engineering sample and analyses

All seeds0–15, p=0.00025/0.0005/0.001, 4,096 ticks, all seven arms. No shock in
this version: first test sustained production and turnover for 64 nominal W
lifetimes. Retain every outcome; don't select a favorable subset. Separate
streams generate acquisition and corruption; all arms get identical corruption.

Report planned activity, completion, final all-row policy accuracy, arbitrary
payload accuracy, survival-weighted functional accuracies, W births/expiries,
external additions, paid trace writes per bank, energy/material ledgers and
periodic state digests. Raw post-death information is separate from function.

Descriptive paired 95% seed-bootstrap differences (10,000 draws, seed20260914):
self−no_synthesis activity; self−no_policy_write activity;
no_synthesis_rescue−no_synthesis activity;
self_clamp−no_synthesis_clamp policy accuracy. No multiplicity-corrected or
confirmatory claim. Report all three configurations.

Engineering criteria per configuration: self mean activity>=0.9; protected and
catalyst-rescue activity>=0.9; self−no_synthesis activity>=0.2;
clamped policy-accuracy difference>=0.2; each self individual's internally
produced W count exceeds ten times its initial W count and every bank receives
writes; all mechanism/ledger/erasure tests pass. Failing criteria are retained.

## Required invariants and rejection conditions

- No W → no effective writes, despite available substrate/energy.
- No parent W → no internally generated W, despite a SYNTH decision.
- Births require actual paid 4M and2E, expiry causes actual material loss.
- The catalytic parent is retained through synthesis.
- Material: initial free+initial W-bound+collected+clamped+external W-bound =
  final free+final W-bound+trace waste+expired W waste+overflow.
- Energy: initial+collected+clamped = final+living+write+synthesis+overflow.
- Complete erasure includes catalytic state and reservoirs; identical reset
  states/future inputs yield identical actions and states across different
  histories. Original arbitrary information remains unrecoverable.
- Source/test/protocol snapshot before sample; no overwrite of old results.

A failed no_synthesis arm alone is not proof of full closure. It can also reflect
the supplied policy's inability to compensate for lost production. Direct write
gating, material ledgers, catalyst rescue, clamped information loss and policy
interventions provide the narrower mechanistic evidence. Rates and stoichiometry
are model choices, not biological measurements.

## Literature connection

The earlier constraint-closure review motivates identifying maintained enabling
constituents. A fresh primary-source search found [Adamala et al., 2016,
Collaboration between primitive cell membranes and soluble catalysts](https://pubmed.ncbi.nlm.nih.gov/26996603/):
its abstract reports that encapsulated catalyst-driven synthesis can stabilize
model vesicles. That is experimental support for studying coupled catalytic and
boundary functions, not evidence for AC2's laws. Boundary dynamics are deferred
until this production loop is understood; no biological equivalence is claimed.
