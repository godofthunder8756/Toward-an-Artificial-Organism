"""AC22: the scaled world's declarative layer — observation, demonstration, acquired target.

Where this sits
--------------
`AC20_BUDGET_v1.md` measured the requirement for a broader developmental function and
`ac21_format.py` supplies the format, proven to reduce to the frozen one. What is missing is the
world those apply to. This module builds its **declarative** layer: what the world shows the
organism, what the demonstration demands, and what the acquired target program is at the larger
scale. It does not build the body: no additional banks in `ac4.Body`, no extra constituents in
`ac9.step`, no organism simulation. That integration is the next step and is stated as such.

The declared scale
------------------
Chosen from the two measured axes, both of which must be >= C + B (`AC20_BUDGET_v1.md`):

    C = 6 constituent needs          (fuel, material, W, C, B, plus one more)
    B = 6 banks                      (four in the frozen body; six declared here)
    observation word = C + B = 12 bits
    rules >= C + B = 12
    mask_bits >= 12
    slots used = 12 rules x 17 bits = 204 bits, well inside the bank's 1024 bit-columns

Acquired structure, compared with the present design:

    frozen design   B = 4  ->  log2(4!)  =  4.58 bits
    scaled design   B = 6  ->  log2(6!)  =  9.49 bits

so the demonstration conveys more than twice the acquired information, which is the substance of
"a broader developmental function", and the rule budget is no longer a knife-edge.
"""
from pathlib import Path
from types import SimpleNamespace
import math
import numpy as np
import ac21_format as fmt
import ac5_program as frozen
import ac4
from ac1 import decode

# declared world scale
C=6
B=6
OBS_BITS=12
RULES=C+B
MASK_BITS=OBS_BITS

# Observation LAYOUT. Note carefully what these positions ARE, because my first version of this
# module got it wrong and AC23 corrected it: bits 2-5 are the MASK positions the frozen program's
# four bank rules use (`4<<bank`), but in `ac9.observe` they are NOT four bank disagreements --
# bit 2 is the whole program bank's disagreement, bits 3 and 4 are memory-urgency bits (one per
# region), and bit 5 is never set at all, which is exactly why AC12's mask-32 rule is permanently
# dead. That confusion came from reading `ac4.observe`, which does put a disagreement bit per bank
# at bits 2-5; `ac9.observe` is a different function. The reducibility check below still passes
# because it compares installed program BITS, and the frozen program's masks are `4<<bank` either
# way -- the masks matched while the semantics I had written down did not.
FROZEN_CONSTITUENT_BITS=(0,1,6,7,8)
FROZEN_BANK_BITS=(2,3,4,5)
# ...and the constituent ACTIONS are not `range(C)` either: the frozen mapping is fuel->0,
# material->1, W->6, particles->7, boundary->8. Both the bit positions and the action numbers are
# supplied conventions of the frozen world, so this module carries them as data. Getting that wrong
# twice (first the bit layout, then the action numbering) is the lesson: re-deriving a convention
# instead of reading it is how this module produced two rounds of false mismatches.
FROZEN_CONSTITUENT_ACTIONS=(0,1,6,7,8)
SCALED_CONSTITUENT_BITS=tuple(range(C))
SCALED_BANK_BITS=tuple(range(C,C+B))
SCALED_CONSTITUENT_ACTIONS=tuple(range(C))

# the frozen world's scale, for the reducibility check
FROZEN_C=5
FROZEN_B=4
FROZEN_RULES=9
FROZEN_MASK_BITS=9


def constituent_actions(C_=C):
    """One action per constituent need, in the fixed order the demonstration uses."""
    return list(range(C_))


def bank_action(bank):
    """Bank-repair actions start after the constituent actions in the frozen numbering
    (action 2 is bank 0 there), so the offset is preserved rather than re-invented."""
    return 2+bank


def demonstration(observation,order,constituent_bits=SCALED_CONSTITUENT_BITS,
                  bank_bits=SCALED_BANK_BITS,constituent_actions=SCALED_CONSTITUENT_ACTIONS):
    """The world's demand: satisfy a constituent need if one is signalled, else repair the
    disagreeing banks in the acquired order. Which observation bit carries which need, which
    carries which bank's disagreement, and which action serves which need are all declared
    layout data -- taken from the world, not re-derived."""
    for c,bit in enumerate(constituent_bits):
        if observation&(1<<bit): return constituent_actions[c]
    for bank,bit in enumerate(bank_bits):
        if bank in order and observation&(1<<bit): return bank_action(bank)
    return 9


def target_rules(order,constituent_bits=SCALED_CONSTITUENT_BITS,bank_bits=SCALED_BANK_BITS,
                 constituent_actions=SCALED_CONSTITUENT_ACTIONS,mask_bits=None):
    """The acquired target as a rule list, one rule per constituent need then one per bank.

    Masks are clamped to the declared mask field. A rule cannot test a bit outside its field, so
    when the observation word is wider than the mask the affected rules become untestable and the
    loss shows up as a coverage shortfall rather than an encoding error -- which is how the
    mask-axis finding (`AC20_BUDGET_v1.md`) manifests inside a world."""
    lim=(1<<mask_bits)-1 if mask_bits is not None else None
    def clamp(m): return m if lim is None else (m&lim)
    rules=[(1,clamp(1<<bit),constituent_actions[c]) for c,bit in enumerate(constituent_bits)]
    rules+=[(1,clamp(1<<bank_bits[bank]),bank_action(bank)) for bank in order]
    return rules


def install_target(traces,order,constituent_bits=SCALED_CONSTITUENT_BITS,
                   bank_bits=SCALED_BANK_BITS,constituent_actions=SCALED_CONSTITUENT_ACTIONS,
                   rules=None,mask_bits=None):
    rules_=rules if rules is not None else len(constituent_bits)+len(bank_bits)
    mask_=mask_bits if mask_bits is not None else OBS_BITS
    fmt.install(traces,target_rules(order,constituent_bits,bank_bits,constituent_actions,mask_),
                rule_count=rules_,mask_bits=mask_)
    return traces


def coverage(order,constituent_bits=SCALED_CONSTITUENT_BITS,bank_bits=SCALED_BANK_BITS,
             constituent_actions=SCALED_CONSTITUENT_ACTIONS,rules=None,mask_bits=None,
             obs_bits=None):
    """How many of the 2^obs_bits observations the installed target reproduces."""
    obs_bits=obs_bits if obs_bits is not None else OBS_BITS
    rules_=rules if rules is not None else len(constituent_bits)+len(bank_bits)
    mask_=mask_bits if mask_bits is not None else obs_bits
    t=np.zeros((4,1024,7),dtype=np.uint8)
    install_target(t,order,constituent_bits,bank_bits,constituent_actions,rules_,mask_)
    bits=decode(t[0,:fmt.program_bits(rules_,mask_)])
    hit=sum(1 for o in range(1<<obs_bits)
            if fmt.interpret(bits,o,rules_,mask_)
            ==demonstration(o,order,constituent_bits,bank_bits,constituent_actions))
    return hit,1<<obs_bits


def acquired_bits(B_=B):
    return math.log2(math.factorial(B_))


def capacity_check():
    bits=fmt.program_bits(RULES,MASK_BITS)
    return dict(rules=RULES,mask_bits=MASK_BITS,program_bits=bits,bank_bits=fmt.BANK_BITS,
                fits=fmt.fits(RULES,MASK_BITS))


def reducibility_check():
    """At the frozen scale **with the frozen layout** the same construction must reproduce
    `ac5_program` exactly: the frozen format is five fixed constituent rules plus four ordered
    bank rules over the frozen observation layout, which is what this module builds with
    C=5, B=4, the frozen bit positions, and the frozen word layout."""
    import itertools
    mismatches=[]
    for order in itertools.permutations(range(FROZEN_B)):
        mine=np.zeros((4,1024,7),dtype=np.uint8)
        install_target(mine,list(order),FROZEN_CONSTITUENT_BITS,FROZEN_BANK_BITS,
                       FROZEN_CONSTITUENT_ACTIONS,FROZEN_RULES,FROZEN_MASK_BITS)
        theirs=np.zeros((4,1024,7),dtype=np.uint8)
        frozen.install_at_acquisition(theirs,list(order))
        if not np.array_equal(mine[0,:FROZEN_RULES*14],theirs[0,:FROZEN_RULES*14]):
            mismatches.append(('bits',order))
        mine_bits=decode(mine[0,:FROZEN_RULES*14])
        for o in range(1<<9):
            if (fmt.interpret(mine_bits,o,FROZEN_RULES,FROZEN_MASK_BITS)
                !=frozen.choose(theirs,o)):
                mismatches.append(('action',order,o))
    return mismatches


if __name__=='__main__':
    print(f"declared scale: C={C} constituents, B={B} banks, observation word {OBS_BITS} bits,")
    print(f"                rules={RULES}, mask_bits={MASK_BITS}")
    cap=capacity_check()
    print(f"capacity: {cap['program_bits']} of {cap['bank_bits']} bank bits -> "
          f"{'fits' if cap['fits'] else 'DOES NOT FIT'}")
    print()
    print(f"acquired structure: frozen B=4 -> {acquired_bits(4):.2f} bits; "
          f"scaled B=6 -> {acquired_bits(6):.2f} bits")
    print()
    hit,total=coverage(tuple(range(B)))
    print(f"scaled target reproduces its demonstration: {hit}/{total} = {100*hit/total:.1f}%")
    bad=reducibility_check()
    print(f"reducibility at the frozen scale: {len(bad)} mismatches over 24 permutations x 512 "
          f"observations")
    if bad: print('  first few:',bad[:3])
