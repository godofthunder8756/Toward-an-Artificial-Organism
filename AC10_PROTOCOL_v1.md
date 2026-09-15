# AC10 protocol: integrated constituent ablations in the AC9 organism

2026-09-15. Written after engineering validation and before the first final seed.
This closes the outstanding requirement recorded in `AUTONOMY_RESEARCH_STATUS.md`
as INCOMPLETE: "Every constituent dependency isolated in the integrated
architecture". It does not amend, execute or reinterpret the stopped E3 v0.11
experiment, and it makes no full-autopoiesis, new-need or novelty claim.

## Question and claim

AC9 shows that developmental history places acquired entries in one region and
that the regional maintenance demand follows them. AC1–AC4 established, in their
own standalone bodies, that a controller can pay for W repair catalysts (AC2),
C energy converters (AC3) and a B enclosure (AC4). Those constituent
dependencies have never been ablated **inside** the integrated AC9 organism,
where memory allocation, W-gated renewal, C-powered execution and B retention
all share one live body.

Falsifiable claim to be tested:

> In the integrated AC9 maintained organism, each produced constituent (W repair
> catalysts, C energy converters, B enclosure) is causally required for continued
> activity and for preserving the acquired memory organization, and the
> enclosure's contribution is its **retention function** rather than its matter.

Strongest simpler rival, accepted in advance: the ablations starve the body of
a generic resource, and every failure is ordinary starvation that a substituted
supply would remove equally. The retention-rescue arms are designed to attack
that explanation directly, because they preserve function while the enclosure's
matter is absent entirely.

Second rival, accepted in advance: survival is not evidence of organization.
This organism can continue acting by random port sampling after its entries are
gone (AC7, AC8, AC9 v1). Activity and acquired organization are therefore
reported as **separate endpoints** and neither is allowed to stand for the other.

## Causal and information inventory

- Acquired during life: route entries (key/value/validity, seven replicas per
  bit) created only by paid deposition after a productive contact, in a region
  selected by the developmental sensory input; and the acquired program bank
  `traces[0,:126]` (nine rules, installed at acquisition).
- What sustains them: regional interior W gates every replacement write
  (`min(32, 8*interior_W, energy, material)`); energy comes only from
  C-catalysed fuel conversion; material is collected and spent on writes,
  particles and boundary.
- What is protected outside the vulnerable organization: the generic
  interpreter, majority decoding, address-free search, the reaction recipes and
  prices, the 5x5 geometry, transport, the observation encoder, and the
  simulator's random streams. None of them encode an individual's entries.
- Interventions used here touch only: whether a named producing reaction can
  occur, whether the enclosure's blocking is applied, and whether the enclosure
  is restored externally. No price, law, ceiling, observation or random stream
  is modified.

## Arms

All arms run the frozen AC9 v2 priority organism for 2048 ticks (512 development
+ 1536 assay). Interventions are implemented by asserted source surgery on the
frozen `ac9.step` and `ac4.react` text (`ac10.py`); each edit site is asserted to
appear exactly once and the physics of every untouched action is the frozen code.

| Arm | Intervention | Exact edit |
| --- | --- | --- |
| keep | none; calls the frozen `ac9.step` object itself | no surgery |
| no_W | the W-producing reaction cannot occur (continuous) | `birth` returns False |
| no_C | the C-producing reaction cannot occur (continuous) | action 7 group list is empty |
| no_B | the B-producing reaction cannot occur (continuous) | frozen `arm='no_B'` guard |
| permeant | enclosure matter present but does not retain | transport called with an all-false impermeant mask |
| no_B_retention | no B production, and blocking is forced regardless of matter | frozen `retention_rescue` kernel flag |
| B_rescue | no B production, enclosure restored from outside each tick | AC4's `external_B` restoration, reused verbatim |
| no_W_late | W production blocked from tick 512 only | `birth` returns False after onset |
| no_B_late | B production blocked from tick 512 only | `arm='no_B'` guard after onset |

Notes on interpretation. `permeant` removes retention, so the constituent
economy collapses as a consequence (W and C leak out and the W-demand rule then
dominates the stored priority order); it is therefore a compound emergent
intervention, and the mechanistic isolation of retention is carried by the
single-step transport test in `test_ac10.py` and by `no_B_retention`, which
separates retention from matter. `B_rescue` supplies matter from outside; it is
an explicit external intervention and is never counted as internal production.
The late-onset arms test maintenance rather than acquisition.

## Endpoints

Reported per individual: activity fraction of planned ticks and completion;
acquired routes at the endpoint (both entries present?) and their first
acquisition and first loss ticks; occupied entry sites and bound memory matter;
W/C/B births, external B, conversion units, exports, deaths; the acquired
program accuracy `traces[0,:126]` against its acquisition-time reference; the
full resource ledger; final inventory; and the state digest.

## Prespecified gates

G1 keep: at least 7/8 complete and at least 7/8 retain both routes, with zero
particle export in at least 7/8.
G2 no_W: W births are zero in 8/8; **no entry is ever allocated**
(`memory_bound==0` in 8/8); mean activity is at least 0.20 below keep.
G3 no_C: C births are zero in 8/8; conversion stops after the initial endowment
expires (converted at 2048 equals converted at 400); mean activity at least 0.20
below keep.
G4 no_B: B births are zero in 8/8; export occurs in at least 7/8; both routes
are lost in at least 7/8; mean activity at least 0.20 below keep.
G5 permeant: export occurs in 8/8; both routes are lost in at least 7/8; mean
activity at least 0.20 below keep.
G6 no_B_retention: export is zero in at least 7/8; both routes are retained in
at least 7/8; mean activity is within 0.20 of keep, despite zero enclosure matter
at the endpoint in at least 7/8.
G7 B_rescue: external B is supplied in 8/8 with zero internal B births; export
is zero in at least 7/8; both routes are retained in at least 7/8.
G8 no_W_late: W births occur before onset and are zero after it in 8/8; both
routes are lost in at least 7/8; mean activity at least 0.20 below keep.
G9 no_B_late: B births occur before onset and are zero after it in 8/8; both
routes are lost in at least 7/8.

Falsification. If any ablation leaves activity and route retention
indistinguishable from keep over this horizon, that constituent is not causally
required here and the claim fails for that constituent. If the two rescue arms
fail to restore zero export and route retention while enclosure matter is absent,
the retention interpretation is not supported. Means are descriptive over eight
independent individuals; this is same-author engineering evidence, not
independent confirmation.

## Sample

Final individuals: seeds 1300–1303, two developmental sensory histories each, all
nine arms: 72 rows. Disjoint from every earlier seed family (E seeds, AC1 0–31,
AC2–AC4 seeds 0–15, AC5 200–207, AC6 400–431, AC7 700–708, AC8 800–808, AC9
1000–1003 / 1100–1103 / 1200–1203).

## Engineering record (before this protocol)

Engineering seeds 1–2 were run through the full nine-arm grid (36 rows, retained
in `ac10_engineering_v1/`) to make the surgery and the runner function. A single
feasibility probe at seed 7, history 0 was also inspected before the gates were
written; it identified which endpoints discriminate (notably that activity
survives loss of the enclosure while route retention does not, and that the
`permeant` arm's B production collapses). The probe informed only which
endpoints to report and the direction of the gates; its numbers are not evidence
and neither it nor the engineering seeds enter the final sample. No magnitude in
the model, price, law or gate threshold was tuned after inspecting final seeds.

Mechanism tests in `test_ac10.py` (21 methods) verify, among others: the keep arm
is the frozen function object and reproduces the **frozen v2 result rows**
field-for-field including state digests; single-step surgery isolation (the W
ablation removes only the W reaction's 4 material and 2 energy, the C ablation
only the C reaction's 4 and 4, and the B ablation changes nothing else); the
retention-kernel and external-restoration semantics; complete-state erasure
noninterference for every arm; exact replay; and the frozen ledger identity for
every arm. `audit_ac10.py` re-derives the ledger and source-hash checks from the
saved table without rerunning the study.

## Recording

Engineering outputs are retained as `ac10_engineering_v1/` and are excluded from
the final sample. Earlier freezes, results and protocols are unchanged. New
versioned artifacts only; the frozen AC9 v3 directory is not touched.
