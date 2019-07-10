import cntk.tests.test_utils
from matplotlib import pyplot as plt
from LstmOwnTransformDzzRegressionParameters import ModelParameters
from LstmSampleGenerator import LstmSampleGenerator
from Models.ModelEvaluator import ModelEvaluator
from ModelTrainer import ModelTrainer
from DivisionTransform import DivisionTransform
from BoxCoxTransform import BoxCoxTransform
from DiffTransform import DiffTransform
from LogTransform import LogTransform
from ValueShiftTransform import ValueShiftTransform
from ValueScaleTransform import ValueScaleTransform
import pandas as pd
from ChainedTransform import ChainedTransform

cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)

params = ModelParameters()

N = params.pred_N
M = params.pred_M

box_cox_transform = BoxCoxTransform()
diff_transform = DiffTransform()
div_transform = DivisionTransform()
log_transform = LogTransform()
shift_transform1 = ValueShiftTransform()
scale_transform = ValueScaleTransform(target_abs_level=0.9)
shift_transform2 = ValueShiftTransform()

#no_transform = TransformBase()

chained_transform = ChainedTransform(diff_transform, shift_transform1, div_transform, log_transform, shift_transform2, scale_transform)
transform = chained_transform

sample_generator = LstmSampleGenerator(params, transform)

#DEBUGGING CRUTCH
df = pd.read_csv( params.io_input_data_file )
df.sort_values( by=params.data_timestamp_column )
dbg_x, dbg_y = sample_generator.generate()#df.Value)

smp_x, smp_y = sample_generator.generate_samples()
data_frames = sample_generator.samples_cached

trainer = ModelTrainer(params)
trainer.train(smp_x["train"], smp_y["train"])
trainer.load_model()

z = trainer._z #load_model(params.io_trained_model_file)

for labeltxt in ["train", "test"]:
    print("mse for {}: {:.6f}".format(labeltxt, trainer.get_mse(smp_x[labeltxt], smp_y[labeltxt])))

evaluator = ModelEvaluator(z, params)
f, a = plt.subplots(3, 1, figsize=(12, 8))
for j, ds in enumerate(["train", "val", "test"]):
    results = evaluator.evaluate(smp_x[ds],params.learn_batch_size)
    a[j].plot(smp_y[ds], label=ds + ' raw')
    a[j].plot(results, label=ds + ' predicted')
[i.legend() for i in a]
plt.show()

eval_res = evaluator.evaluate(smp_x["test"])
test_res = sample_generator.add_output_list_to_df(eval_res, "test")

test_res["RestoredNormalized"] = transform.inv_transform(test_res.Normalized).values
plt.figure(figsize=(15, 7))
test_res.Value.plot()
test_res.ResInvTransformed.plot()
test_res.RestoredNormalized.plot()

#TODO 4) Implement SINE sign extraction transform
#TODO 5) USE Validation sample by Trainer during training
#TODO 6) NaN trimming transform

print("ololo")

#todo reconsider loss calculation

print("end")
