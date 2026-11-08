import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from common import assign_ordered_split

def metadata(n=10):
    return pd.DataFrame({'sensor': ['a']*(n*2), 'capture': [i for i in range(n) for _ in range(2)]})

class OrderedSplits(unittest.TestCase):
    def test_capture_groups_stay_intact_and_standard_ratios_preserved(self):
        frame = metadata()
        result = assign_ordered_split(frame, ['sensor'], 'capture')
        self.assertTrue((result.groupby('capture')['split'].nunique() == 1).all())
        self.assertEqual(result['split'].value_counts().to_dict(), {'train':12, 'val':4, 'test':4})
        self.assertNotIn('split', frame.columns)

    def test_three_units_have_three_disjoint_splits(self):
        result = assign_ordered_split(metadata(3), ['sensor'], 'capture')
        self.assertEqual(result.groupby('capture')['split'].first().tolist(), ['train','val','test'])

    def test_too_few_units_fail(self):
        with self.assertRaisesRegex(ValueError, 'at least 3'):
            assign_ordered_split(metadata(2), ['sensor'], 'capture')

    def test_invalid_ratios_fail(self):
        for train, val in [(0,.2),(.8,.2),(.8,.3),(.6,-.1),(float('nan'),.2)]:
            with self.subTest(train=train, val=val), self.assertRaises(ValueError):
                assign_ordered_split(metadata(), ['sensor'], 'capture', train, val)

    def test_incomplete_metadata_fails(self):
        for frame in [metadata().drop(columns='sensor'), metadata().assign(sensor=None), metadata().iloc[:0]]:
            with self.assertRaises(ValueError):
                assign_ordered_split(frame, ['sensor'], 'capture')

    def test_duplicate_indices_fail(self):
        frame = metadata()
        frame.index = [0]*len(frame)
        with self.assertRaises(ValueError):
            assign_ordered_split(frame, ['sensor'], 'capture')

    def test_environment_root_override(self):
        with tempfile.TemporaryDirectory() as d:
            result = subprocess.run([sys.executable, '-c', 'from common import PROJECT_ROOT; print(PROJECT_ROOT)'], env={**os.environ, 'TACVERSE_DATA_ROOT':d}, capture_output=True, text=True, check=True)
            self.assertEqual(Path(result.stdout.strip()), Path(d).resolve())
