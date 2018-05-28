import math
from matplotlib import pyplot as plt
import pandas as pd

import cntk.tests.test_utils
from cntk.ops.functions import load_model
cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)

from Common.ModelParameters import ModelParameters
from SampleGenerators.DefaultSampleGenerator import DefaultSampleGenerator
from Models.EasyLstmTrain import Trainer
import HelperFunctions.ArrayDataHelperFunctions as adhf
import HelperFunctions.DataFrameHelperFunctions as dfhf

params = ModelParameters()
sample_generator = DefaultSampleGenerator(params)

smp_x, smp_y = sample_generator.generate_samples()

#trainer = Trainer(params)
#trainer.train(smp_x["train"], smp_y["train"])
z = load_model(params.io_trained_model_file)


class ModelEvaluator:

    _params = None
    _z = None
    _last_result = None

    def __init__(self, model, params):
        self._params = params
        self._z = model

    def evaluate(self, sample, batch_size=1):
        res = []
        for x in adhf.next_value(sample, batch_size):
            predicted = self._z.eval({self._z.arguments[0]: x})
            res.extend(predicted[:, 0])

        self._last_result = res
        return res


evaluator = ModelEvaluator(z, params)
#eval_res = evaluator.evaluate(smp_x["test"])


f, a = plt.subplots(3, 1, figsize = (12, 8))
for j, ds in enumerate(["train", "val", "test"]):
    results = evaluator.evaluate(smp_x[ds])
    a[j].plot(smp_y[ds], label=ds + ' raw')
    a[j].plot(results, label=ds + ' predicted')
[i.legend() for i in a]

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