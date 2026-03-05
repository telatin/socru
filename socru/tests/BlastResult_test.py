import unittest
from socru.BlastResult import BlastResult


class TestBlastResult(unittest.TestCase):

    def _make_result(self, subject_start, subject_end):
        return BlastResult('query1', '3', 99.5, 1000, 5, 0, 1, 1000,
                           subject_start, subject_end, 1e-50, 500.0)

    def test_is_forward_when_start_less_than_end(self):
        br = self._make_result(100, 1100)
        self.assertTrue(br.is_forward())

    def test_is_reverse_when_start_greater_than_end(self):
        br = self._make_result(1100, 100)
        self.assertFalse(br.is_forward())

    def test_equal_subject_coords_is_forward(self):
        # degenerate single-base hit: start == end, treated as forward
        br = self._make_result(500, 500)
        self.assertTrue(br.is_forward())

    def test_str_has_twelve_tab_separated_fields(self):
        br = self._make_result(100, 1100)
        fields = str(br).split('\t')
        self.assertEqual(12, len(fields))

    def test_str_preserves_query_name_and_subject(self):
        br = self._make_result(100, 1100)
        fields = str(br).split('\t')
        self.assertEqual('query1', fields[0])
        self.assertEqual('3', fields[1])

    def test_numeric_fields_are_correct_types(self):
        br = self._make_result(100, 1100)
        self.assertIsInstance(br.identity, float)
        self.assertIsInstance(br.alignment_length, int)
        self.assertIsInstance(br.mismatches, int)
        self.assertIsInstance(br.gap_openings, int)
        self.assertIsInstance(br.bit_score, float)
        self.assertIsInstance(br.e_value, float)

    def test_numeric_fields_are_parsed_from_strings(self):
        # Constructor receives strings (as they come from BLAST tabular output)
        br = BlastResult('q', 's', '98.7', '500', '3', '1',
                         '10', '509', '200', '699', '1e-100', '450.5')
        self.assertAlmostEqual(98.7, br.identity)
        self.assertEqual(500, br.alignment_length)
        self.assertAlmostEqual(450.5, br.bit_score)
