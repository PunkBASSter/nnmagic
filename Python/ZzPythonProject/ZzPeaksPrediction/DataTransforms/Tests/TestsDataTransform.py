import unittest
import pandas as pd
from DataTransforms.TransformBase import TransformBase
from DataTransforms.BoxCoxTransform import BoxCoxTransform
from DataTransforms.DiffTransform import DiffTransform
from DataTransforms.LogTransform import LogTransform


class TestsDataTransform(unittest.TestCase):

    def _steps_transform_reverse(self, inst :TransformBase):
        df = pd.DataFrame(data={'Timestamp': [1, 3, 4, 8, 15], 'Value': [2, 4, 8, 16, 32]})
        df["Transformed"]= inst.transform(df.Value)
        self.assertTrue(len(df.Transformed.tolist())>0, "Transformed sequence length is not greater than 0")

        df["Restored"]=inst.inv_transform(df.Transformed)
        self.assertTrue(abs(df.Value.min() - df.Restored.min()<0.00001), "Not equal minimums")
        self.assertTrue(abs(df.Value.max() - df.Restored.max()<0.00001), "Not equal maximums")

    def test_tr_boxcox(self):
        self._steps_transform_reverse(BoxCoxTransform())

    def test_tr_diff(self):
        self._steps_transform_reverse(DiffTransform())

    def test_tr_log(self):
        self._steps_transform_reverse(LogTransform())


if __name__ == '__main__':
    unittest.main()