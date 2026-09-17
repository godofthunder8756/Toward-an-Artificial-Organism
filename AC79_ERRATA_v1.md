# AC79 errata v1: corrected reading of the frozen result, and the next target

2026-09-17. This is a non-frozen correction note. It does **not** edit
`AC79_RESULTS_v1.md`, `AC79_PROTOCOL_v1.md`, `AC78_ENGINEERING_v1.md`, or
`AC76_RESULTS_v1.md` (those are frozen). It records three reporting corrections and
one reframing that change what the AC76/AC79 arc should be taken to establish.

## 1. The frozen cohort is 2/8 / 2/8 / 0/8 — not "12/12"

The AC79 frozen final run (seeds 4004–4007 × 2 histories = 8 individuals per condition):

| final corruption arm | survived entire run |
| --- | --- |
| Maintained description | 2/8 |
| Pristine description | 2/8 |
| Unmaintained description | 0/8 |

Recovery was demonstrated in the **two maintained survivors** (fw=0, description
intact). The "12/12 recovered" figure describes the **engineering** run (12/16
survival, engineering seeds 0–7), not the frozen finals. Any summary that reports
"12/12" as the frozen result is wrong.

## 2. G1 was an outcome-informed endpoint revision, not a prospective gate

`AC79_PROTOCOL_v1.md` (lines 113–132) records that G1 (and G5) were revised
**after the first 4004–4007 run failed**: the population filter was moved from
"alive at t=8192" to "survivors (`completed`)". The reasons are principled (paid
maintenance stops at death, so a dying organism cannot fund re-instantiation), and
the revision is disclosed rather than hidden. But it is still an
**outcome-informed endpoint revision** — the protocol's own "this protocol may not
be edited after the first final seed" line sits uneasily beside the recorded edit.
"Frozen, six predeclared gates passed" therefore overstates the epistemic status.
Conditioning on survival cannot establish reliable recovery across the original
cohort; a fresh prospective study would need to gate on the full planned
denominator.

## 3. AC78's "fails everywhere" inference is not established

`AC78_ENGINEERING_v1.md` (lines 18–19) moves from the measured
fixed-point/path-dependence result to "if self-production fails here, it fails
everywhere the organism lives." That inference is not established: the experiment
uses the AC32/33 six-position ranking world, which the same document distinguishes
from AC76's four-bank controller. Different observations, reversible opportunities,
and recurring environmental changes are not ruled out. Regenerating inherited
organization and discovering better organization are **separate problems** — a
self-producing system need not invent its inherited instructions during its
lifetime. The autopoiesis question concerns production of the *components*
realizing the organization, not optimal-policy discovery (organizational closure,
Montévil & Mossio 2015).

## 4. Reframing what AC79 establishes (the reconstruction recipe is still external)

AC79 froze that the 8-bit priority description's **storage and maintenance** are
endogenous. It did **not** internalize the reconstruction **recipe**:

- `reg_maintained` (ac79.py) computes `target = prog.program(priority)`.
- `prog.program` (ac5_program.py) hard-codes the five resource/production/repair
  rule words `(1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8)`; only the four bank
  rules are derived from the stored permutation.
- The organism's eight stored bits specify bank *ordering* only; the recipe that
  turns 8 bits into the 126-bit program is an external Python function, and the
  regen call is injected **before** `prog.choose`.

The correct restatement: the system funds reconstruction of its controller using a
vulnerable internal priority description and an externally specified reconstruction
recipe. Paying for reconstruction establishes an economic dependency; it does not,
by itself, internalize the information or machinery performing reconstruction. This
does not invalidate the recovery result — it changes its meaning.

## 5. Consciousness disposition is a scheduling decision, not evidence

`CONSCIOUSNESS_BLOCKS_DISPOSITION_v1.md` archives the goal-§7 task because it was
gated on content self-production, which AC78 answered negatively. That gating is a
**project scheduling decision**, not evidence that consciousness-relevant
mechanisms require successful priority learning. Autopoiesis is not an established
prerequisite in the indicator-based framework (Butlin et al. 2023,
arxiv:2308.08708). Theory-specific investigations — e.g. the AC67/71
self-monitoring loop as a candidate indicator — can remain a separate track
provided there is a concrete mechanism worth testing.

## Next target

The decisive question is now: **can the organism replace its controller using
information and functional machinery sustained inside its own organization, once
the host stops supplying the reconstruction recipe?** Three milestones:

1. **Internalize the reconstruction recipe** — store the complete organism-specific
   description (5 rule words + 8-bit permutation, 78 bits) in vulnerable,
   paid-maintained state; replace `prog.program(priority)` with a generic decode
   that reads that state. Inherited initial content allowed; the host function is
   the scaffold to remove.
2. **Replacement across generations** — functional copies constructed, used, and
   replaced using internally retained information; partial losses and multiple
   turnover cycles.
3. **One frozen architecture** — reconstruction + description maintenance +
   environmental adaptation together (AC79 disables route moves; re-enable them),
   with unconditional survival/recovery on fresh seeds.

These are tracked on the `artificial-organism` kanban board.
