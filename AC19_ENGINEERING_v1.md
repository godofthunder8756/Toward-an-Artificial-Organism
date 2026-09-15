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

## Confound 4, diagnosed: the corruption was reaching the *observation*, not just the decision

The trace answered it. Under the `register_only` cut, the cut arms die of **energy** exhaustion
(E 122 → 11 → 0) while repeatedly choosing action 6 (produce W), and the **protected arm dies
identically** — so the cause is not the register read. The reason, measured directly:

`ac9.observe` summarises each bank with a disagreement bit,
`min(ones[bank], 7-ones[bank]).sum() >= 4` per rule row. My spread corruption set 2 replicas on
each of the four register bits, which pushed rule 4's row disagreement to 7 and **set bank 0's
disagreement bit in the observation**. The organism therefore *saw* a disagreement it could
never repair (the repair was reverted), kept choosing the repair and W-production actions, and
died. Protecting the register *read* cannot protect the *observation*, which is computed from
the body's traces regardless of which register a decision consults. That is why the protected
control was not clean.

Measured, `ac12.acquire(0)`, observation bit 2 (bank 0 disagreement):

| corruption | obs | bank-0 disagreement | register bit reads relinquished |
| --- | ---: | ---: | --- |
| pristine | 0 | 0 | — |
| 2 replicas on each of the 4 register bits | 4 | **1** | no |
| 4 of 7 replicas on **one** bit | 0 | **0** | **yes** |
| 3 of 7 replicas on one bit | 0 | 0 | no |

So there is a corruption model that changes the decision and nothing else: **a 4-of-7 flip of a
single decision bit**, whose rule row contributes only 3 to the disagreement sum. That is now
the declared model (`FLIP_REPLICAS=4`, one bit per 128 ticks after the move, round-robin), and
the spread model is retained in the code only as the confounded variant it was.

## The clean screen, and the first attributable signal

Same seeds (0-3), no global damage, clean flip corruption, `register_only` cut:

| arm | alive | mean moved | mean relinquished bits | mean kept |
| --- | ---: | ---: | ---: | ---: |
| `two_way` (live register, repair on) | 4/4 | 0.864 | 3.0 | **0.68** |
| `two_way_protected` (shadow, repair on) | 4/4 | 0.886 | 4.0 | **0.97** |
| `two_way_no_repair` | **0/4** | 0.798 | 3.5 | 0.85 |
| `two_way_protected_no_repair` | **0/4** | 0.774 | 4.0 | 0.90 |

**The uncut pair gives the first clean attribution in this line.** Both arms are damaged
identically in the body (the protected arm ends with *more* set replicas, 28 against 18-21,
because the live arm repairs some when it chooses the repair action). Their behaviour differs
only through the decision state: the live arm's register reads 3 of 4 bits relinquished and its
kept-channel productivity falls to **0.68**, while the protected arm's decisions read a shadow
the corruption never touches and its kept-channel stays at **0.97-1.00**. So corruption of the
decision state **does** propagate into what the organism maintains — the first half of the
closure claim, with a control that isolates it.

The second half — that the organism's *own funded repair* is what prevents it — is still not
shown cleanly, because both cut arms die for a reason not yet identified (the cut arms' mean
relinquished-bit counts, 3.5 and 4.0, are not meaningfully different from the uncut arms', so
the cut is acting through something else once more).

## The next measurement, revised

The cut itself is now the only unresolved element. Compare, under the clean flip model and
`register_only`, an arm whose register repair is cut against one whose register repair is cut
*and* whose flip events are suppressed: if both survive, the flips plus the cut are jointly
fatal by a route unrelated to the decision; if only the flip-free arm survives, the flips are
the cause and the cut is irrelevant. In parallel, log the action histogram for a single cut
individual: the trace showed action 6 (produce W) dominating to energy exhaustion, which
suggests the cut costs the organism resources in a way that starves W production rather than
corrupting the decision.

## Status of the framework question

Partly advanced, and honestly partial. Corruption of the decision state is now demonstrably
able to change the organism's maintenance behaviour (uncut pair), which is the propagation half
of the closure claim and the first attributable result in this line. The maintenance half —
that the funded repair is what holds the decision state correct — remains unshown, blocked on
one unresolved effect of the cut. Nothing is claimed, no protocol exists, and no final seeds
were run.


## Artifacts

`ac19.py` (engineering harness: two damage modes, three cut modes, targeted corruption),
`AC19_ENGINEERING_v1.md` (this record). No results directory, no protocol.
