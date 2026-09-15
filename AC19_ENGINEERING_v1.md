# AC19 engineering screen: persistent corruption, and a fourth confound I have not cleared

2026-09-15. **Engineering only — no protocol, no final seeds, no claim.** AC19 is exploratory.
Everything below is a screen, not a result.

## Why AC19 exists

AC14 asked whether the organism's own decision state is a maintained constraint in the loop

    allocation register in traces[0,:126]
      -> repaired only by the paid bank-0 repair action
      -> whose capacity is core W
      -> which the program itself produces

and could not answer, because the frozen damage stream is `b.traces[0,:126] ^= core_flips` —
an XOR, so a flip **self-reverses**. Over 4096 ticks the bank accumulated 3 differing replicas
of 882 and the register never changed. AC14's recorded requirement was **persistent
corruption**: a flip that stays flipped until repaired. AC19 is the attempt to supply it.

## Confound 1: sticky damage, globally applied

One asserted surgery on the frozen step: `^= core_flips` becomes `|= core_flips`. Damage can
then only *set* a replica, and only the paid bank-0 repair clears it. Screen, seed 0, global
damage at the frozen 1e-4:

| arm | alive | register replicas set | program replicas differing | moved | kept |
| --- | --- | ---: | ---: | ---: | ---: |
| `two_way` (repair on) | yes | 0 | 141 | 0.888 | 0.949 |
| `two_way_protected` | yes | 0 | 141 | 0.888 | 0.949 |
| `two_way_no_repair` | **no** | 6 | 189 | 0.615 | 0.375 |
| `two_way_protected_no_repair` | **no** | 6 | 189 | 0.615 | 0.375 |

Two findings, both negative for the closure question:

- **The register still never flipped.** 6 set replicas spread over 4 register bits is 1-2 per
  bit, and a bit needs 4 of its 7 replicas to read as relinquished. Persistent damage at this
  rate still cannot corrupt a *decision*.
- **The protected control is identical to the live arm** (`two_way_protected_no_repair` matches
  `two_way_no_repair` in every field) and both die. Cutting the bank-0 repair therefore acts
  through the *rest of the program*, not through the decision state. The falsifier fired: the
  decision state is not what the repair is protecting here.

## Confound 2: the metric was wrong

`program_replicas_differing` compared against `ac9.acquire(seed)`, which is a **different
program variant** from the one the organism carries (`ac12.acquire` wraps `ac9_priority_v2`).
It therefore reported ~140-190 "differences" in *every* arm, including the uncut ones, where
the damage stream alone accounts for very little. Fixed to compare against
`ac12.acquire(seed)` — the program the organism actually carries.

## Confound 3: concentrated corruption still cannot flip the decision state

To give the register a chance, the corruption was made **targeted**: only the register offsets
are hit, at a declared rate (2.5e-4 per replica per tick, so each replica takes ~1 hit over the
horizon), leaving the rest of the program's damage at the frozen rate. Screen:

- `regRelinq` was still **0** in the uncut arms, and the cut arms died early (through confound
  1's route) before corruption could accumulate. So the test never reached the state it exists
  to observe.

## Confound 4, unresolved: cutting the register's repair destroys the organism

With global damage switched **off** and only the register corrupted — the cleanest form of the
question — the cut was narrowed a third time: `cut_mode='register_only'` lets the bank-0 repair
run normally but reverts it on the four register offsets, so the decision state is the only
thing left unrepaired. Screen, seeds 0-2:

| arm | alive | register replicas set | moved | kept | final demand |
| --- | --- | ---: | ---: | ---: | --- |
| `two_way` | yes x3 | 2, 0, 0 | 0.876-0.912 | 0.947-1.000 | [42,0] |
| `two_way_protected` | yes x3 | 0, 0, 0 | 0.876-0.912 | 0.947-1.000 | [42,0] |
| `two_way_no_repair` | **no x3** | 4, 8, 4 | 0.797-0.844 | 0.643-1.000 | [0,0] |
| `two_way_protected_no_repair` | **no x3** | 8, 12, 8 | 0.733-0.868 | 0.700-0.846 | [0,0] |

**Every cut arm loses both entries and dies — including the protected arms, whose renewal
decisions never read the register at all.** Reverting the repair on four rows of the program
bank should be almost a no-op for those arms, and it is not. So the cut has an effect I have
not identified, and it is not the effect the closure claim is about.

Positives that are real: with the repair running, the register is held effectively clear
(0-2 stray replicas, never a flipped bit) and behaviour is preserved; under the cut the register
does accumulate. So the repair *is* doing something to the decision state. But because the cut
also destroys the organism by an unidentified route, **the closure question remains open**, and
the protected control cannot currently be used to attribute anything.

## The next measurement, named

Per-tick instrumentation of a single `register_only` `two_way_no_repair` individual, logging
energy, material, regional W availability, `demand`, and the action histogram every 64 ticks,
against the uncut arm from an identical seed and identical RNG draws. The question is concrete:
**why do the entries lapse in an arm whose decisions read a shadow the corruption never
touches?** Candidate routes to check, in order: (1) the reverted rows are not the only ones
`action==2` writes, so the wrapper may be reverting more than intended; (2) the register offsets
sit inside bank 0, and a partially corrupted *word* may decode to a different rule than
intended — verify by decoding the rule each tick and comparing against the pristine program;
(3) the corruption interacts with the memory-consistency bits in `ac9.observe`, which would
reach the program through observations rather than through the register.

## Status of the framework question

Unchanged from AC14: **the decision state has not been shown to be a maintained constraint in
the loop.** AC19 has improved the instrument — persistent corruption is now expressible, and
targeted at the decision state — and has found a fourth confound rather than an answer. Nothing
here is claimed, and no final seeds were run.

## Artifacts

`ac19.py` (engineering harness: two damage modes, three cut modes, targeted corruption),
`AC19_ENGINEERING_v1.md` (this record). No results directory, no protocol.
