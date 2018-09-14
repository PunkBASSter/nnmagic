import cntk.tests.test_utils
import pandas as pd
import numpy as np
from cntk.ops.functions import load_model
from matplotlib import pyplot as plt
from Common.ModelParameters import ModelParameters
from SampleGenerators.LstmSampleGenerator import LstmSampleGenerator
from Models.ModelEvaluator import ModelEvaluator
from Models.ModelTrainer import ModelTrainer
from DataTransforms.TransformBase import TransformBase, TransformParams
from DataTransforms.DivisionTransform import DivisionTransform, DivisionTransformParams
from DataTransforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from DataTransforms.DiffTransform import DiffTransform, DiffTransformParams
from DataTransforms.LogTransform import LogTransform, LogTransformParams
from DataTransforms.ValueShiftTransform import ValueShiftTransform, ValueShiftTransformParams
from DataTransforms.ValueScaleTransform import ValueScaleTransform, ValueScaleTransformParams
from DataTransforms.ChainedTransform import ChainedTransform
from DataTransforms.TransformDecorators.StatsInfoTransformDecorator import StatsInfoTransformDecorator
import HelperFunctions.StatisticsHelperFunctions as shf

params = ModelParameters()

diff_transform = DiffTransform(DiffTransformParams())
div_transform = DivisionTransform(DivisionTransformParams())
log_transform1 = LogTransform(LogTransformParams())
log_transform2 = LogTransform(LogTransformParams())
shift_transform = ValueShiftTransform(ValueShiftTransformParams())

scale_params = ValueScaleTransformParams(target_abs_level=1)
scale_transform = ValueScaleTransform(scale_params)
chain_transform = ChainedTransform(diff_transform, shift_transform, div_transform, log_transform1, shift_transform, scale_transform)


df = pd.read_csv(params.io_input_data_file)
df.sort_values(params.data_timestamp_column)

plt.figure(figsize=(15, 7))

result = chain_transform.transform(df.Value)
#result.plot()
#result.hist(bins=500)

res_no_nan = result.iloc[2:].tolist()

shf.is_normal(res_no_nan)
shf.is_stationary(res_no_nan)

plt.hist(res_no_nan, bins=500)
plt.show()

print("end")

