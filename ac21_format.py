"""A parametric rule format, and its proof of reducibility to the frozen one.

Why this exists
---------------
`AC20_BUDGET_v1.md` measured two independent limits of the frozen format:

    slots      9 rules                       -> binds when C + B > 9
    mask width 9 bits (word = 1+9+4 = 14)    -> binds when the observation word exceeds 9 bits

A broader developmental function needs a format wider on **both** axes, at a scale now specified
rather than guessed. This module supplies that width parametrically, and — the part that matters
before anything is built on it — **reduces to the frozen format exactly** at the frozen
parameters. That reducibility is the discipline used throughout this project: an extension must
reproduce its parent bit for bit before a result may rest on it.

What is *not* here: no larger world, no new constituents, no new banks. This is the format only.
The world build (larger C and B, wider observation) is the next step and will be parameterized on
this.

Design, following the frozen conventions
----------------------------------------
The frozen format is `ac5_program`: a 14-bit word per rule, laid out as
`enabled | mask(9) << 1 | action(4) << 10`, nine rules packed into `traces[0,:126]`, interpreted
first-match-wins with action 9 (rest) as the interpreter's fallthrough.

This generalizes exactly that layout:

    word = enabled | mask << 1 | action << (1 + mask_bits)
    word width = 1 + mask_bits + 4
    total program bits = rules * word_width, which must fit the bank

with `rules` and `mask_bits` supplied. At `rules=9, mask_bits=9` every operation reduces to the
frozen one, which is checked here rather than asserted.
"""
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import ac5_program as frozen
import ac4
from ac1 import decode

RULES=9
MASK_BITS=9
ACTION_BITS=4
BANK_BITS=1024          # traces[0] has this many bit-columns available
BANK_OFFSET=0           # where the program starts inside traces[0]


def word_width(mask_bits=MASK_BITS):
    return 1+mask_bits+ACTION_BITS


def program_bits(rules=RULES,mask_bits=MASK_BITS):
    return rules*word_width(mask_bits)


def encode_rule(enabled,mask,action,mask_bits=MASK_BITS,action_bits=ACTION_BITS):
    if enabled not in (0,1): raise ValueError('Invalid enabled flag')
    if not 0<=mask<(1<<mask_bits): raise ValueError('Invalid mask')
    if not 0<=action<(1<<action_bits): raise ValueError('Invalid action')
    width=1+mask_bits+action_bits
    word=int(enabled) | (int(mask)<<1) | (int(action)<<(1+mask_bits))
    return np.array([(word>>k)&1 for k in range(width)],dtype=np.uint8)


def pack(rules,rule_count=RULES,mask_bits=MASK_BITS):
    """Pad or truncate a rule list to exactly `rule_count` rules and concatenate them."""
    out=[]
    for i in range(rule_count):
        if i<len(rules): out.append(encode_rule(*rules[i],mask_bits=mask_bits))
        else: out.append(encode_rule(0,0,9,mask_bits=mask_bits))     # disabled, action = rest
    return np.concatenate(out)


def interpret(rules_bits,observation,rule_count=RULES,mask_bits=MASK_BITS):
    """First-match-wins over the decoded rule list, action 9 as the fallthrough."""
    width=word_width(mask_bits)
    bits=rules_bits.reshape(rule_count,width)
    words=(bits*(1<<np.arange(width))).sum(axis=1)
    for word in words:
        word=int(word)
        if word&1:
            mask=(word>>1)&((1<<mask_bits)-1)
            if observation&mask==mask:
                return (word>>(1+mask_bits))&((1<<ACTION_BITS)-1)
    return 9


def choose(traces,observation,rule_count=RULES,mask_bits=MASK_BITS):
    """Read the program out of a trace bank and interpret it. The bank holds *replicas* per bit,
    so decode before interpreting -- slicing the replicas directly gives shape (bits, 7)."""
    bits=program_bits(rule_count,mask_bits)
    return interpret(decode(traces[0,BANK_OFFSET:BANK_OFFSET+bits]),observation,rule_count,mask_bits)


def install(traces,rules,rule_count=RULES,mask_bits=MASK_BITS):
    bits=program_bits(rule_count,mask_bits)
    if bits>BANK_BITS: raise ValueError(f'program needs {bits} bits, bank has {BANK_BITS}')
    traces[0,BANK_OFFSET:BANK_OFFSET+bits]=pack(rules,rule_count,mask_bits)[:,None]


def fits(rules,mask_bits):
    return program_bits(rules,mask_bits)<=BANK_BITS


def equivalence_at_frozen_parameters():
    """At rules=9, mask_bits=9 this must reproduce `ac5_program` exactly: every observation for
    every acquired permutation, both the chosen action and the installed bit pattern."""
    import itertools
    checked=0; mismatches=[]
    for priority in itertools.permutations(range(4)):
        t=np.zeros((4,1024,7),dtype=np.uint8)
        rules=[(1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8)]+[(1,4<<b,2+b) for b in priority]
        install(t,list(rules))
        # the installed pattern must match the frozen format's bit for bit (compare replicas),
        # and the interpreter must then agree on every observation (compare decoded bits)
        t2=np.zeros((4,1024,7),dtype=np.uint8)
        frozen.install_at_acquisition(t2,list(priority))
        if not np.array_equal(t[0,:126],t2[0,:126]):
            mismatches.append(('bits',priority))
        mine=decode(t[0,:126])
        for o in range(512):
            a=interpret(mine,o); b=frozen.choose(t2,o)
            checked+=1
            if a!=b: mismatches.append(('action',priority,o,a,b))
    return checked,mismatches


if __name__=='__main__':
    checked,mismatches=equivalence_at_frozen_parameters()
    print(f"reducibility check: {checked} (permutation, observation) pairs compared")
    print(f"  mismatches vs ac5_program: {len(mismatches)}")
    if mismatches: print('  first few:',mismatches[:3])
    print()
    print('capacity of the bank at various widths:')
    for mask_bits in (9,11,13,16):
        for rules in (9,13,17,21):
            print(f"  mask_bits {mask_bits:2d} rules {rules:2d}: {program_bits(rules,mask_bits):4d} bits "
                  f"-> {'fits' if fits(rules,mask_bits) else 'DOES NOT FIT'}")
