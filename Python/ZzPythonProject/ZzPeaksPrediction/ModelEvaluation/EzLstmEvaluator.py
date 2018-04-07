import math
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import time

import cntk as C
import cntk.tests.test_utils
from cntk.ops.functions import load_model
cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)

isFast = False
train = False
model_file_name = "myEzLstm.cmf"


def split_data(data, val_size=0.1, test_size=0.2):
    pos_test = int(len(data) * (1 - test_size))
    pos_val = int(len(data[:pos_test]) * (1 - val_size))

    train, val, test = data[:pos_val], data[pos_val:pos_test], data[pos_test:]

    return {"train": train, "val": val, "test": test}


def generate_data(data, time_steps, time_shift):
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(dict(a=data[0:len(data) - time_shift], b=data[time_shift:]))
    rnn_x = []
    for i in range(len(data) - time_steps + 1):
        rnn_x.append(data['a'].iloc[i: i + time_steps].as_matrix())
    rnn_x = np.array(rnn_x)

    # Reshape or rearrange the data from row to columns
    # to be compatible with the input needed by the LSTM model
    # which expects 1 float per time point in a given batch
    rnn_x = rnn_x.reshape(rnn_x.shape + (1,))

    rnn_y = data['b'].values
    rnn_y = rnn_y[time_steps - 1:]

    # Reshape or rearrange the data from row to columns
    # to match the input shape
    rnn_y = rnn_y.reshape(rnn_y.shape + (1,))

    return split_data(rnn_x), split_data(rnn_y)


N = 25 # input: N subsequent values
M = 1 # output: predict 1 value M steps ahead

rawData = pd.read_csv("DzzExportEURUSD.mPERIOD_H1.csv",
                  usecols=["Value"], dtype=np.float32).as_matrix().transpose()[0]

normalized = pd.read_csv("data\\Normalized_DzzExportEURUSD.mPERIOD_H1.csv",
                  usecols=["ValueDiffRatio_LogWithMaxAbsBase"], dtype=np.float32).as_matrix().transpose()[0]
X, Y = generate_data(normalized, N, M)
rawSplitted = split_data(rawData)

def create_model(x):
    """Create the model for time series prediction"""
    with C.layers.default_options(initial_state = 0.1):
        m = C.layers.Recurrence(C.layers.LSTM(N))(x)
        m = C.sequence.last(m)
        m = C.layers.Dropout(0.2, seed=1)(m)
        m = C.layers.Dense(1)(m)
        return m


def next_batch(x, y, ds):
    """get the next batch to process"""

    def as_batch(data, start, count):
        part = []
        for i in range(start, start + count):
            part.append(data[i])
        return np.array(part)

    for i in range(0, len(x[ds])-BATCH_SIZE, BATCH_SIZE):
        yield as_batch(x[ds], i, BATCH_SIZE), as_batch(y[ds], i, BATCH_SIZE)


# Training parameters
TRAINING_STEPS = 10000
BATCH_SIZE = 100
EPOCHS = 10 if isFast else 200
LEARNING_RATE = 0.01

# input sequences
x = C.sequence.input_variable(1)
z = create_model(x)
l = C.input_variable(1, dynamic_axes=z.dynamic_axes, name="y")

lr_schedule = C.learning_parameter_schedule(LEARNING_RATE)

# loss function
loss = C.squared_error(z, l)
# use squared error to determine error for now
error = C.squared_error(z, l)

momentum_schedule = C.momentum_schedule(0.9, minibatch_size=BATCH_SIZE)
learner = C.fsadagrad(z.parameters,
                      lr = lr_schedule,
                      momentum = momentum_schedule,
                      unit_gain = True)

trainer = C.Trainer(z, (loss, error), [learner])


# train
if train:
    loss_summary = []
    start = time.time()
    for epoch in range(0, EPOCHS):
        for x1, y1 in next_batch(X, Y, "train"):
            trainer.train_minibatch({x: x1, l: y1})
        if epoch % (EPOCHS / 10) == 0:
            training_loss = trainer.previous_minibatch_loss_average
            loss_summary.append(training_loss)
            print("epoch: {}, loss: {:.5f}".format(epoch, training_loss))

    print("training took {0:.1f} sec".format(time.time() - start))

    # A look how the loss function shows how well the model is converging
    plt.plot(loss_summary, label='training loss');
    z.save(model_file_name)
else:
    z = load_model(model_file_name)


# validate
def get_mse(X,Y,labeltxt):
    result = 0.0
    for x1, y1 in next_batch(X, Y, labeltxt):
        eval_error = trainer.test_minibatch({x : x1, l : y1})
        result += eval_error
    return result/len(X[labeltxt])


# Print the train and validation errors
for labeltxt in ["train", "val"]:
    print("mse for {}: {:.6f}".format(labeltxt, get_mse(X, Y, labeltxt)))


# Print validate and test error
labeltxt = "test"
print("mse for {}: {:.6f}".format(labeltxt, get_mse(X, Y, labeltxt)))


#predict
f, a = plt.subplots(3, 1, figsize = (12, 8))
for j, ds in enumerate(["train", "val", "test"]):
    results = []
    for x1, y1 in next_batch(X, Y, ds):
        #pred = z.eval({x: x1})
        pred = z.eval({z.arguments[0]: x1})
        results.extend(pred[:, 0])
    a[j].plot(Y[ds], label = ds + ' raw')
    a[j].plot(results, label = ds + ' predicted')
[i.legend() for i in a]


#Illustrations
results = []
for x1, y1 in next_batch(X, Y, "test"):
    pred = z.eval({z.arguments[0]: x1})
    results.extend(pred[:, 0])


predictedTest = []
import DataPreProcessing as dpp
rdat = rawSplitted["test"]
predictedTest.append(rdat[0])
for r in range(1, len(results)):
    val = dpp.calculateNextPeak(rdat[r-1], rdat[r], results[r])
    predictedTest.append(val)

pos_test = len(Y["train"])+len(Y["val"]) + 2
full_input_data = pd.read_csv("data\\Normalized_DzzExportEURUSD.mPERIOD_H1.csv")
time = full_input_data["Timestamp"].values.tolist()
time = time[pos_test:pos_test+len(predictedTest)]
#d = pd.DataFrame(dict(Timestamp=time,Predicted=predictedTest,Actual=rdat))
#Write output
lines = [] #["Timestamp,Value,TimeDiffRatio,ValueDiffRatio,ValueDiffRatio_LogWithMaxAbsBase\n"]
for i in range(0, len(time)):
    lines.append(str(time[i])+","+str(predictedTest[i])+","+str(rdat[i])+'\n')
fh = open("data\\"+"Predictions.csv", 'wt')
fh.writelines(lines)



#Fun with plots
fig = plt.figure()
ax0 = fig.add_subplot(311)
ax0.plot(rdat, label = 'Actual')
ax0.plot(predictedTest, label = 'Predicted')
ax0.grid(True)

diff = []
for p in range(0, len(predictedTest)):
    diff.append(math.fabs(predictedTest[p]) - math.fabs(rdat[p]))

import TradeEmulator as te
balance, trades = te.emulate_trading_on_series(N, rdat, predictedTest)

ax2 = fig.add_subplot(312)
ax2.plot(balance)
ax2.grid(True)
ax3 = fig.add_subplot(313)
ax3.plot(trades)
ax3.grid(True)

plt.show()


#todo reconsider loss calculation

print("end")