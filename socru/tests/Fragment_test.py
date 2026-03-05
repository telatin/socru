import unittest
import os
import shutil
from socru.Fragment  import Fragment

class TestFragment(unittest.TestCase):

    def test_fragment_seq_name_one_coord(self):
        f = Fragment([[10,123]])
        self.assertEqual(str(f), '0 10_123')

    def test_fragment_seq_name_two_coords(self):
        f = Fragment([[10,123],[555,999]])
        self.assertEqual(str(f), '0 10_123__555_999')

    def test_num_bases_empty_sequence(self):
        f = Fragment([[0, 100]])
        self.assertEqual(0, f.num_bases())

    def test_num_bases_with_sequence(self):
        f = Fragment([[0, 10]], sequence='ACGTACGTAC')
        self.assertEqual(10, f.num_bases())

    def test_output_filename(self):
        f = Fragment([[0, 100]])
        f.number = 3
        self.assertEqual('3.fa', f.output_filename())

    def test_operon_direction_str_forward_operon(self):
        f = Fragment([[0, 100]], number=2, operon_forward_start=True)
        self.assertEqual('--> 2', f.operon_direction_str())

    def test_operon_direction_str_reverse_operon(self):
        f = Fragment([[0, 100]], number=2, operon_forward_start=False)
        self.assertEqual('<-- 2', f.operon_direction_str())

    def test_operon_direction_str_reversed_fragment(self):
        f = Fragment([[0, 100]], number=3, reversed_frag=True, operon_forward_start=True)
        self.assertEqual("--> 3'", f.operon_direction_str())

    def test_operon_direction_str_with_dnaa(self):
        f = Fragment([[0, 100]], number=1, dna_A=True, operon_forward_start=True)
        self.assertEqual('--> 1(Ori)', f.operon_direction_str())

    def test_operon_direction_str_with_dif(self):
        f = Fragment([[0, 100]], number=4, dif=True, operon_forward_start=False)
        self.assertEqual('<-- 4(Ter)', f.operon_direction_str())
        