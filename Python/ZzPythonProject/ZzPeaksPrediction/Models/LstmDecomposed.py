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
from DataTransforms.ShiftToPositiveTransform import ShiftToPositiveTransform, ShiftToPositiveTransformParams
from DataTransforms.ChainedTransform import ChainedTransform
from DataTransforms.TransformDecorators.StatsInfoTransformDecorator import StatsInfoTransformDecorator

cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)


params = ModelParameters()

N = params.pred_N
M = params.pred_M

box_cox_transform = BoxCoxTransform(BoxCoxTransformParams())
diff_transform = DiffTransform(DiffTransformParams())
log_transform = LogTransform(LogTransformParams())
shift_to_positive_transform = ShiftToPositiveTransform(ShiftToPositiveTransformParams())

#complex_transform = ChainedTransform(box_cox_transform) #add decorator later

sample_generator = LstmSampleGenerator(params, box_cox_transform)

smp_x, smp_y = sample_generator.generate_samples()

test_df = sample_generator.get_last_test_df()

trainer = ModelTrainer(params)
#trainer.train(smp_x["train"], smp_y["train"])
trainer.load_model()

z = trainer._z #load_model(params.io_trained_model_file)

evaluator = ModelEvaluator(z, params)

for labeltxt in ["train", "val", "test"]:
    print("mse for {}: {:.6f}".format(labeltxt, trainer.get_mse(smp_x[labeltxt], smp_y[labeltxt])))



#df_test_with_predictions, pred_start_timestamp = dfhf.add_list_to_source_df_padding_overlapping(smp_x["test"], eval_res, N)
#denormalized_predictions = normalizer.denormalize_synchronous_len(df_test_with_predictions, scaling_k, predicted_column)
#df_test_with_predictions["Restored"] = pd.Series(ldhf.add_padding(denormalized_predictions), df_test_with_predictions.index)
#df_test_with_predictions.to_csv(params.io_predictions_data_file)


f, a = plt.subplots(3, 1, figsize = (12, 8))
for j, ds in enumerate(["train", "val", "test"]):
    results = evaluator.evaluate(smp_x[ds])
    a[j].plot(smp_y[ds], label=ds + ' raw')
    a[j].plot(results, label=ds + ' predicted')
[i.legend() for i in a]

eval_res = evaluator.evaluate(smp_x["test"])

#TODO Synchronize charts offsets for M > 1!
#TODO Design interface for sample splitting, taking into account reverse transforms.

plt.show()

print("ololo")

#Illustrations
#results = []
#for x1, y1 in next_batch(X["test"], Y["test"], 1):
#    pred = z.eval({z.arguments[0]: x1})
#    results.extend(pred[:, 0])
#
#
#predictedTest = []
#import DataPreProcessing as dpp
#rdat = rawSplitted["test"]
#predictedTest.append(rdat[0])
#for r in range(1, len(results)):
#    val = dpp.calculateNextPeak(rdat[r-1], rdat[r], results[r])
#    predictedTest.append(val)
#
#pos_test = len(Y["train"])+len(Y["val"]) + 2
#full_input_data = pd.read_csv("data\\Normalized_DzzExportEURUSD.mPERIOD_H1.csv")
#time = full_input_data["Timestamp"].values.tolist()
#time = time[pos_test:pos_test+len(predictedTest)]
##d = pd.DataFrame(dict(Timestamp=time,Predicted=predictedTest,Actual=rdat))
##Write output
#lines = [] #["Timestamp,Value,TimeDiffRatio,ValueDiffRatio,ValueDiffRatio_LogWithMaxAbsBase\n"]
#for i in range(0, len(time)):
#    lines.append(str(time[i])+","+str(predictedTest[i])+","+str(rdat[i])+'\n')
#fh = open("data\\"+"Predictions.csv", 'wt')
#fh.writelines(lines)



#Fun with plots
#fig = plt.figure()
#ax0 = fig.add_subplot(311)
#ax0.plot(rdat, label = 'Actual')
#ax0.plot(predictedTest, label = 'Predicted')
#ax0.grid(True)
#
#diff = []
#for p in range(0, len(predictedTest)):
#    diff.append(math.fabs(predictedTest[p]) - math.fabs(rdat[p]))
#
#import TradeEmulator as te
#balance, trades = te.emulate_trading_on_series(N, rdat, predictedTest)
#
#ax2 = fig.add_subplot(312)
#ax2.plot(balance)
#ax2.grid(True)
#ax3 = fig.add_subplot(313)
#ax3.plot(trades)
#ax3.grid(True)
#
#plt.show()


#todo reconsider loss calculation

print("end")