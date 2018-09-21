import cntk.tests.test_utils
from cntk.ops.functions import load_model
from matplotlib import pyplot as plt
from Common.ModelParameters import ModelParameters
from SampleGenerators.LstmOwnTransformSampleGenerator import LstmOwnTransformSampleGenerator
from Models.ModelEvaluator import ModelEvaluator
from Models.ModelTrainer import ModelTrainer
from DataTransforms.TransformBase import TransformBase, TransformParams
from DataTransforms.DivisionTransform import DivisionTransform, DivisionTransformParams
from DataTransforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from DataTransforms.DiffTransform import DiffTransform, DiffTransformParams
from DataTransforms.LogTransform import LogTransform, LogTransformParams
from DataTransforms.ValueShiftTransform import ValueShiftTransform, ValueShiftTransformParams
from DataTransforms.ValueScaleTransform import ValueScaleTransform, ValueScaleTransformParams
import pandas as pd
from DataTransforms.ChainedTransform import ChainedTransform
from DataTransforms.TransformDecorators.StatsInfoTransformDecorator import StatsInfoTransformDecorator

cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)

params = ModelParameters()

N = params.pred_N
M = params.pred_M

box_cox_transform = BoxCoxTransform(BoxCoxTransformParams())
diff_transform = DiffTransform(DiffTransformParams())
div_transform = DivisionTransform(DivisionTransformParams())
log_transform = LogTransform(LogTransformParams())
shift_transform1 = ValueShiftTransform(ValueShiftTransformParams())
scale_transform = ValueScaleTransform(ValueScaleTransformParams(target_abs_level=0.9))
shift_transform2 = ValueShiftTransform(ValueShiftTransformParams())

#no_transform = TransformBase()

chained_transform = ChainedTransform(diff_transform, shift_transform1, div_transform, log_transform, shift_transform2, scale_transform)
transform = chained_transform

sample_generator = LstmOwnTransformSampleGenerator(params, transform)

#DEBUGGING CRUTCH

smp_x, smp_y = sample_generator.generate_learning_samples()

trainer = ModelTrainer(params)
trainer.train(smp_x["train"], smp_y["train"])
trainer.load_model()

z = trainer._z #load_model(params.io_trained_model_file)

def print_mse(samples_to_process):
    for labeltxt in samples_to_process:
        print("mse for {}: {:.6f}".format(labeltxt, trainer.get_mse(smp_x[labeltxt], smp_y[labeltxt])))

print_mse(["train", "val", "test"])

evaluator = ModelEvaluator(z, params)
f, a = plt.subplots(3, 1, figsize=(12, 8))
for j, sample in enumerate( ["train", "val", "test"] ):
    results = evaluator.evaluate( smp_x[sample], params.learn_batch_size )
    a[j].plot( smp_y[sample], label=sample + ' raw' )
    a[j].plot( results, label=sample + ' predicted' )
[i.legend() for i in a]
plt.show()

eval_res = evaluator.evaluate(smp_x["test"])
#test_res = sample_generator.add_output_list_to_df(eval_res, "test")

#test_res["RestoredNormalized"] = transform.inv_transform(test_res.Normalized).values
#plt.figure(figsize=(15, 7))
#test_res.Value.plot()
#test_res.ResInvTransformed.plot()
#test_res.RestoredNormalized.plot()

#TODO 4) Implement SINE sign extraction transform
#TODO 5) USE Validation sample by Trainer during training
#TODO 6) NaN trimming transform

#todo reconsider loss calculation

print("end")