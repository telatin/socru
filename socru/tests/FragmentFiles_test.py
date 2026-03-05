import unittest
import os
import shutil
import tempfile
from Bio.Seq import Seq
from socru.FragmentFiles import FragmentFiles
from socru.Fragment import Fragment


class TestFragmentFiles(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def _make_fragment(self, seq_str):
        f = Fragment([[0, len(seq_str)]])
        f.sequence = Seq(seq_str)
        return f

    # --- ordering ---

    def test_largest_fragment_is_ordered_first(self):
        f_small = self._make_fragment('A' * 10)
        f_large = self._make_fragment('A' * 100)
        f_mid   = self._make_fragment('A' * 50)
        ff = FragmentFiles([f_small, f_large, f_mid], self.temp_dir, False)
        sizes = [len(f.sequence) for f in ff.ordered_fragments]
        self.assertEqual(100, sizes[0])

    def test_ordering_preserves_all_fragments(self):
        frags = [self._make_fragment('A' * n) for n in [30, 100, 60, 10]]
        ff = FragmentFiles(frags, self.temp_dir, False)
        self.assertEqual(4, len(ff.ordered_fragments))

    def test_fragments_numbered_sequentially_from_one(self):
        f1 = self._make_fragment('A' * 10)
        f2 = self._make_fragment('A' * 100)
        ff = FragmentFiles([f1, f2], self.temp_dir, False)
        numbers = [int(f.number) for f in ff.ordered_fragments]
        self.assertEqual([1, 2], sorted(numbers))
        self.assertEqual(1, numbers[0])

    def test_single_fragment_gets_number_one(self):
        ff = FragmentFiles([self._make_fragment('ACGT' * 10)], self.temp_dir, False)
        self.assertEqual(1, ff.ordered_fragments[0].number)

    # --- FASTA file creation ---

    def test_create_fragment_fastas_writes_one_file_per_fragment(self):
        f1 = self._make_fragment('ACGT' * 25)  # 100 bp (largest)
        f2 = self._make_fragment('TTTT' * 5)   # 20 bp
        ff = FragmentFiles([f1, f2], self.temp_dir, False)
        ff.create_fragment_fastas()
        self.assertEqual(2, len(ff.output_filenames))
        for fname in ff.output_filenames:
            self.assertTrue(os.path.exists(fname))

    def test_create_fragment_fastas_files_are_nonempty(self):
        f1 = self._make_fragment('ACGT' * 25)
        f2 = self._make_fragment('TTTT' * 5)
        ff = FragmentFiles([f1, f2], self.temp_dir, False)
        ff.create_fragment_fastas()
        for fname in ff.output_filenames:
            self.assertGreater(os.path.getsize(fname), 0)

    # --- split_fragment_order ---

    def test_split_fragment_order_plain(self):
        frags = [self._make_fragment('A' * n) for n in [100, 50, 20]]
        ff = FragmentFiles(frags, self.temp_dir, False, fragment_order='1-2-3')
        self.assertEqual(['1', '2', '3'], ff.split_fragment_order())

    def test_split_fragment_order_with_prime_notation(self):
        frags = [self._make_fragment('A' * n) for n in [100, 50, 20]]
        ff = FragmentFiles(frags, self.temp_dir, False, fragment_order="1-2'-3")
        self.assertEqual(["1", "2'", "3"], ff.split_fragment_order())

    # --- prime notation reversal ---

    def test_prime_notation_marks_fragment_as_reversed(self):
        # Size order after sorting: 100 → index 0, 40 → index 1, 20 → index 2
        f1 = self._make_fragment('ACGT' * 25)   # 100 bp
        f2 = self._make_fragment('ACGT' * 10)   # 40 bp
        f3 = self._make_fragment('ACGT' * 5)    # 20 bp
        ff = FragmentFiles([f1, f2, f3], self.temp_dir, False,
                           fragment_order="1-2'-3")
        # index 1 corresponds to the "2'" token
        self.assertTrue(ff.ordered_fragments[1].reversed)

    def test_non_prime_fragment_not_marked_reversed(self):
        frags = [self._make_fragment('A' * n) for n in [100, 50, 20]]
        ff = FragmentFiles(frags, self.temp_dir, False, fragment_order='1-2-3')
        for frag in ff.ordered_fragments:
            self.assertFalse(hasattr(frag, 'reversed'))
