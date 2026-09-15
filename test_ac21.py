"""AC21 tests: the parametric rule format and its reducibility to the frozen one.

Run with: .venv/bin/python -B -m unittest test_ac21
"""
import itertools
import unittest
import numpy as np
import ac21_format as fmt
import ac5_program as frozen
from ac1 import decode


class TestReducibility(unittest.TestCase):
    """The extension must reproduce its parent bit for bit before anything rests on it."""

    def test_frozen_parameters_reproduce_ac5_program_exactly(self):
        checked,mismatches=fmt.equivalence_at_frozen_parameters()
        self.assertEqual(checked,24*512)
        self.assertEqual(mismatches,[],f'{len(mismatches)} mismatches vs ac5_program')

    def test_installed_bits_match_the_frozen_installer(self):
        for priority in itertools.permutations(range(4)):
            rules=[(1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8)]
            rules+=[(1,4<<b,2+b) for b in priority]
            t1=np.zeros((4,1024,7),dtype=np.uint8); fmt.install(t1,rules)
            t2=np.zeros((4,1024,7),dtype=np.uint8); frozen.install_at_acquisition(t2,list(priority))
            np.testing.assert_array_equal(t1[0,:126],t2[0,:126])


class TestFormatMechanics(unittest.TestCase):
    def test_encode_decode_round_trip(self):
        for mask_bits in (9,11,13,16):
            for enabled,mask,action in ((1,0,0),(1,1,9),(0,511,15),(1,(1<<mask_bits)-1,3)):
                want=mask&((1<<mask_bits)-1)
                bits=fmt.encode_rule(enabled,mask,action,mask_bits=mask_bits)
                self.assertEqual(len(bits),fmt.word_width(mask_bits))
                # a single-rule program returns its action on a matching observation, and the
                # interpreter's rest fallthrough when the rule is disabled
                t=np.zeros((4,1024,7),dtype=np.uint8)
                fmt.install(t,[(enabled,want,action)],rule_count=1,mask_bits=mask_bits)
                got=fmt.interpret(decode(t[0,:fmt.program_bits(1,mask_bits)]),want,1,mask_bits)
                self.assertEqual(got,action if enabled else 9)

    def test_rest_fallthrough(self):
        t=np.zeros((4,1024,7),dtype=np.uint8)
        fmt.install(t,[(1,1,0)])                       # only rule: fuel low
        self.assertEqual(fmt.choose(t,1),0)
        self.assertEqual(fmt.choose(t,0),9,'unmatched observation must fall through to rest')

    def test_disabled_rules_are_skipped(self):
        t=np.zeros((4,1024,7),dtype=np.uint8)
        fmt.install(t,[(0,1,7),(1,2,3)])
        self.assertEqual(fmt.choose(t,1),9,'a disabled rule must never fire')
        self.assertEqual(fmt.choose(t,2),3)

    def test_wider_mask_reaches_conditions_the_frozen_width_cannot(self):
        wide=(1<<12)|(1<<10)                            # two conditions beyond the 9-bit field
        t=np.zeros((4,1024,7),dtype=np.uint8)
        fmt.install(t,[(1,wide,5)],rule_count=1,mask_bits=16)
        self.assertEqual(fmt.interpret(decode(t[0,:fmt.program_bits(1,16)]),wide,1,16),5)

    def test_capacity_and_overrun(self):
        self.assertTrue(fmt.fits(9,9))
        self.assertTrue(fmt.fits(21,16),'the bank has 1024 bit-columns; 441 must fit')
        self.assertFalse(fmt.fits(64,16),'64 rules x 21 bits exceeds the bank')
        with self.assertRaises(ValueError):
            t=np.zeros((4,1024,7),dtype=np.uint8)
            fmt.install(t,[(1,0,0)],rule_count=64,mask_bits=16)

    def test_frozen_occupancy_and_headroom(self):
        """The frozen format occupies 126 of the bank's 1024 bit-columns, which is why the
        extension needs no storage change -- an earlier claim of mine that it did was wrong."""
        self.assertEqual(fmt.program_bits(9,9),126)
        self.assertEqual(fmt.BANK_BITS,1024)
        self.assertGreater(fmt.BANK_BITS,fmt.program_bits(13,9))


if __name__=='__main__':
    unittest.main()
