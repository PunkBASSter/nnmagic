import cntk.tests.test_utils
from cntk.ops.functions import load_model
from matplotlib import pyplot as plt
from Common.ModelParameters import ModelParameters
from Normalizers.DiffRatioNormalizer import DiffRatioNormalizer
from SampleGenerators.LstmSampleGenerator import LstmSampleGenerator
from Models.ModelEvaluator import ModelEvaluator
from Models.ModelTrainer import ModelTrainer
import HelperFunctions.DataFrameHelperFunctions as dfhf
from DataTransforms.TransformBase import TransformBase, TransformParams
from DataTransforms.BoxCoxTransform import BoxCoxTransform, BoxCoxTransformParams
from DataTransforms.DiffTransform import DiffTransform, DiffTransformParams
from DataTransforms.LogTransform import LogTransform, LogTransformParams
from DataTransforms.ValueShiftTransform import ValueShiftTransform, ValueShiftTransformParams
from DataTransforms.ValueScaleTransform import ValueScaleTransform, ValueScaleTransformParams

from DataTransforms.ChainedTransform import ChainedTransform
from DataTransforms.TransformDecorators.StatsInfoTransformDecorator import StatsInfoTransformDecorator

cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)

params = ModelParameters()

N = params.pred_N
M = params.pred_M

box_cox_transform = BoxCoxTransform(BoxCoxTransformParams())
diff_transform = DiffTransform(DiffTransformParams())
log_transform = LogTransform(LogTransformParams())
shift_transform = ValueShiftTransform(ValueShiftTransformParams())
scale_transform = ValueScaleTransform(ValueScaleTransformParams(target_abs_level=0.9))

#no_transform = TransformBase()

chained_transform = ChainedTransform( diff_transform, shift_transform, log_transform)
transform = chained_transform

sample_generator = LstmSampleGenerator(params, transform)
smp_x, smp_y = sample_generator.generate_samples()
data_frames = sample_generator.samples_cached

trainer = ModelTrainer(params)
#trainer.train(smp_x["train"], smp_y["train"])
trainer.load_model()

z = trainer._z #load_model(params.io_trained_model_file)

for labeltxt in ["train", "test"]:
    print("mse for {}: {:.6f}".format(labeltxt, trainer.get_mse(smp_x[labeltxt], smp_y[labeltxt])))

evaluator = ModelEvaluator(z, params)
f, a = plt.subplots(3, 1, figsize = (12, 8))
for j, ds in enumerate(["train", "val", "test"]):
    results = evaluator.evaluate(smp_x[ds],params.learn_batch_size)
    a[j].plot(smp_y[ds], label=ds + ' raw')
    a[j].plot(results, label=ds + ' predicted')
[i.legend() for i in a]
plt.show()

#Divergence hypothesis testing
#train_eval_res = evaluator.evaluate(smp_x["train"])
#train_actual_res = sample_generator.add_output_list_to_df(train_eval_res, "train")
#train_eval_res["RestoredNormalized"]=transform.inv_transform(train_eval_res).values
#plt.figure(figsize=(15, 7))
#train_eval_res.Value.plot()
#train_eval_res.ResInvTransformed.plot()
#train_eval_res.RestoredNormalized.plot()

#Div_test_end

eval_res = evaluator.evaluate(smp_x["test"])
test_res = sample_generator.add_output_list_to_df(eval_res, "test")

test_res["RestoredNormalized"]=transform.inv_transform(test_res.Normalized).values
plt.figure(figsize=(15, 7))
test_res.Value.plot()
test_res.ResInvTransformed.plot()
test_res.RestoredNormalized.plot()


#TODO 1) Implement SCALE_TO_1 transform,
#TODO 2) Resolve BOXCOX Index_Out_Of_Range! On Validation sample
#TODO 3) FIND Out WHY DIFF + LOG LINEARLY FALLS
#TODO 4) Implement SINE sign extraction transform
#TODO 5) USE Validation sample by Trainer during training

print("ololo")

#todo reconsider loss calculation

print("end")