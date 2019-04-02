import cntk.tests.test_utils
from cntk.ops.functions import load_model
from matplotlib import pyplot as plt
from Common.ModelParameters import ModelParameters
from SampleGenerators.LstmOwnTransformSampleGenerator import LstmOwnTransformSampleGenerator
from Models.ModelEvaluator import ModelEvaluator
from Models.ModelTrainer import ModelTrainer
from DataTransforms.DivisionTransform import *
from DataTransforms.BoxCoxTransform import *
from DataTransforms.DiffTransform import *
from DataTransforms.LogTransform import *
from DataTransforms.ValueShiftTransform import *
from DataTransforms.ValueScaleTransform import *
import pandas as pd
from DataTransforms.ChainedTransform import *
from DataTransforms.TrimNanLeftTransform import *
import copy
import numpy as np
from HelperFunctions import DataFrameHelperFunctions as dfhf
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
trim_nans_transform = TrimNanLeftTransform()

chained_transform = ChainedTransform(
    diff_transform,
    shift_transform1,
    div_transform,
    log_transform,
    shift_transform2,
    scale_transform,
    trim_nans_transform
)
sample_generator = LstmOwnTransformSampleGenerator(params, chained_transform)
smp_x, smp_y = sample_generator.generate_learning_samples()

trainer = ModelTrainer(params)
trainer.train(smp_x["train"], smp_y["train"])
trainer.load_model()
z = trainer._z

def print_mse(samples_to_process):
    for labeltxt in samples_to_process:
        print("mse for {}: {:.6f}".format(labeltxt, trainer.get_mse(smp_x[labeltxt], smp_y[labeltxt])))
print_mse(["train", "val", "test"])

#evaluator = ModelEvaluator(z, params)
#f, a = plt.subplots(3, 1, figsize=(12, 8))
#for j, sample in enumerate( ["train", "val", "test"] ):
#    results = evaluator.evaluate( smp_x[sample], params.learn_batch_size )
#    a[j].plot( smp_y[sample], label=sample + ' raw' )
#    a[j].plot( results, label=sample + ' predicted' )
#[i.legend() for i in a]
#plt.show()

#EVALUATION
#eval_res = evaluator.evaluate(smp_x["test"])
test_series = sample_generator.test_sample_series #Should be initialized after sample generation :)
test_x, original_y = sample_generator.generate_test_input_sequences(test_series)
interp_results = []
for x in test_x:
    nn_input, trans_seq = sample_generator.generate_nn_input_X(x)
    nn_res = z.eval({z.arguments[0]: nn_input})
    nn_res_unpacked = nn_res[:,0]
    pre_res_concat = pd.concat([pd.Series(trans_seq), pd.Series(nn_res_unpacked)], ignore_index=True)
    inv_transformed_sq = sample_generator._last_used_transform.inv_transform(pre_res_concat) #TODO КАСТЫЛЬ С СОЗДАНИЕМ СЕРИЙ
    interp_results.append(inv_transformed_sq[inv_transformed_sq.__len__()-1]) #TODO ALSO КАСТЫЛЬ АНТИ СИКВЕНС!!!

def write_output(inp_df: pd.DataFrame, interp_results: []):
    test_frame = (inp_df.iloc[inp_df.__len__()-interp_results.__len__():]).copy()
    test_frame = test_frame.assign(Predicted=pd.Series(interp_results).values)
    test_frame.Timestamp.astype(np.int64, copy=False)
    test_frame.Value.astype(np.float32, copy=False)
    test_frame.Predicted.astype(np.float32, copy=False)
    test_frame.set_index('Timestamp')
    test_frame = test_frame.loc[:,['Timestamp','Value','Predicted']]
    test_frame.to_csv(params.io_predictions_data_file, index=False)
    return test_frame
test_frame = write_output(sample_generator.data_frame, interp_results)

f, a = plt.subplots(1, 1, figsize=(12, 8))
a.plot( test_frame.Value.tolist(), label="Actual" + ' raw' )
a.plot( interp_results, label="Predicted1" + ' predicted' )
plt.show()

#plt.plot(test_frame.Value.tolist())
#plt.plot(test_frame.NnResults.tolist())
#plt.show()

#TODO 4) Implement SINE sign extraction transform
#TODO 5) USE Validation sample by Trainer during training
#TODO 6) NaN trimming transform

#todo reconsider loss calculation
print("end")
