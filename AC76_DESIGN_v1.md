# AC76 design v1: controller turnover via a dual-copy internal template (§3 scope)

2026-09-17. Scopes the goal's §3 milestone — **endogenous component replacement of the controller** —
the experiment `DEPENDENCY_AUDIT_v1.md` names as the decisive one. Design proposal, not yet frozen.

## The milestone, stated precisely

Every component the organism produces is replaced through its own ongoing activity — W/C/B are born and
die continuously (each W site lives 64 ticks, ~256 turnovers per 16,384-tick run), B decays and is
re-born, routes expire and are re-deposited, the register is written and re-written. The **controller is
the exception**: the 126-bit program is written once at acquisition and only *repaired* (minority replicas
restored to the surviving majority). AC61 showed repair is preventive, not curative — once a rule's
majority flips (4 of 7 replicas), repair **cements** the corruption, because there is no organism-internal
correct reference.

The milestone: does the controller-bearing component **turn over** — get regenerated from an organism-
internal source through the organism's own paid processes — or only persist?

## The smallest structural redesign

Two banks, mutual regeneration:

1. **Store the program twice** — the primary in `traces[0,:126]` (as now) and an internal copy in
   `traces[1,:126]` (currently dead legacy storage, read by nothing). Both are in the organism's own
   vulnerable substrate, damaged by the same stream.
2. **Read across both copies** — the interpreter takes the majority of the **14** replicas (7+7), so full
   corruption of one bank does not change behaviour.
3. **Cross-regenerate on repair** — the paid bank-0 repair action, when the two banks' majorities disagree
   on a bit, regenerates the minority bank from the majority bank (a paid write), rather than restoring to
   the corrupted bank's own majority.

The internal template is the *other* bank. It is not hidden (same damage stream), not free (regeneration
is a paid write through the same vulnerable bank), and not a pristine backup (it is itself repaired by the
same mechanism). This is the AC71 self-monitoring loop generalised from "restore to my majority" to
"regenerate from my twin."

## What this establishes, and what it does not

**Establishes (if it works):** the controller-bearing component is *regenerated* through the organism's
own processes — full corruption of one bank is recovered by re-copying from the other, paid, with no
external reference. That is the §3 turnover test, and it is the step from "maintained program" to
"replaced component."

**Does not establish:** that the *content* of the rules is self-produced. The twin copy holds the same
hand-written template, duplicated. Turnover and content self-production are different properties and will
be reported separately (per the goal's "Separate component production, repair, policy learning, and
historical origin"). Content self-production remains the AC73/AC30–33 open question (self-directed rule
learning, bounded by the single-lifetime information limit).

## The intervention and rival explanations

- **Intervention:** at a declared tick, fully corrupt one bank (all 7 replicas of all 126 program bits
  set to the *opposite* of the twin's value, so the corruption is adversarial, not random). Measure: does
  the organism (a) keep behaving correctly (the twin bank is read), (b) regenerate the corrupted bank
  (paid), and (c) survive the horizon.
- **Rival 1 — the corruption never matters.** If full corruption of one bank changes nothing because the
  twin is always read, the regeneration is theatre. Control: corrupt **both** banks' disagreement-carrying
  bits to confirm the organism then fails (the twin is load-bearing, not vestigial).
- **Rival 2 — hidden pristine backup.** Ruled out by construction: the twin lives in the same damage
  stream and is repaired by the same paid mechanism; there is no `shadow`/`protected` copy in the arm.
- **Rival 3 — more redundancy, not regeneration.** Distinguish by making the intervention *adversarial*
  (corrupt to the opposite value, not random): 14-replica redundancy alone fails adversarial corruption of
  one full bank (7 of 14 flipped → majority flips), whereas cross-regeneration recovers it because the
  twin's 7 replicas are intact. If cross-regeneration survives adversarial one-bank corruption where a
  flat 14-replica bank would not, the mechanism is regeneration, not just wider redundancy.

## Experiment shape (for the eventual freeze)

- Arms: `dual` (cross-regeneration) vs `redundant` (flat 14-replica bank, no twin — the redundancy rival)
  vs `dual_no_repair` (repair cut) vs `single` (the AC71 baseline).
- Endpoint: survival, program correctness (vs the twin's stored content), regeneration writes, and the
  behavioural consequence (routes held, body stable).
- Gates: `dual` survives adversarial one-bank corruption 8/8 and regenerates the bank (content matches the
  twin); `redundant` fails adversarial corruption (content flips); `dual_no_repair` dies (repair still
  load-bearing); unchanged-world control identical to baseline.

## Bounds

Design proposal. Nothing frozen, no claim. The first step is an engineering feasibility probe of the
dual-bank read + cross-regeneration mechanism before any protocol.
