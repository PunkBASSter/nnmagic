import math
from matplotlib import pyplot as plt
import numpy as np
import os
import pandas as pd
import time

import cntk as C
import cntk.tests.test_utils
from cntk.ops.functions import load_model

import HelperFunctions.DataFrameHelperFunctions as dfhf
import HelperFunctions.ListDataHelperFunctions as ldhf
from Common.ModelParameters import ModelParameters
cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)


#settings
params = ModelParameters()
train = False
normalized_column = "Normalized"
predicted_column = "Predicted"

print("Loading and preparing raw data.")
df = pd.read_csv(params.io_input_data_file, index_col="Timestamp")
df.sort_index()

print("Normalizing data and adding to DataFrame.")
norm_list, scaling_k = nrm.normalize(df, add_padding=True)
df[normalized_column] = pd.Series(norm_list, df.index)

N = params.pred_N
M = params.pred_M

print("Splitting DataFrame to Train/Validation/Test samples.")
df_train, df_val, df_test = dfhf.split_df_by_size(df, params.size_validation, params.size_test, N, M)

print("Transforming normalized data from splitted samples to collections with LSTM NN-compatible structure.")
train_X, train_Y = dfhf.generate_data_by_df(df_train, N, M)
val_X, val_Y = dfhf.generate_data_by_df(df_val, N, M)
test_X, test_Y = dfhf.generate_data_by_df(df_test, N, M)

X = {"train": train_X, "val": val_X, "test": test_X}
Y = {"train": train_Y, "val": val_Y, "test": test_Y}


def create_model(x):
    """Create the model for time series prediction"""
    with C.layers.default_options(initial_state=0.1):
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
TRAINING_STEPS = params.learn_training_steps
BATCH_SIZE = params.learn_batch_size
EPOCHS = params.learn_epochs


# input sequences
x = C.sequence.input_variable(1)
z = create_model(x)
l = C.input_variable(1, dynamic_axes=z.dynamic_axes, name="y")
learning_rate = 0.01
lr_schedule = C.learning_parameter_schedule(learning_rate)

# loss function
loss = C.squared_error(z, l)
# use squared error to determine error for now
error = C.squared_error(z, l)

momentum_schedule = C.momentum_schedule(0.9, minibatch_size=BATCH_SIZE)
learner = C.fsadagrad(z.parameters,
                      lr=lr_schedule,
                      momentum=momentum_schedule,
                      unit_gain=True)

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
    plt.plot(loss_summary, label='training loss')
    z.save(params.io_trained_model_file)
else:
    z = load_model(params.io_trained_model_file)


# validate
def get_mse(X,Y,labeltxt):
    result = 0.0
    for x1, y1 in next_batch(X, Y, labeltxt):
        eval_error = trainer.test_minibatch({x : x1, l : y1})
        result += eval_error
    return result/len(X[labeltxt])


# Print the train and validation errors
for labeltxt in ["train", "val", "test"]:
    print("mse for {}: {:.6f}".format(labeltxt, get_mse(X, Y, labeltxt)))


#predict
f, a = plt.subplots(3, 1, figsize=(12, 8))
results = {"train": [], "val": [], "test": []}
for j, ds in enumerate(["train", "val", "test"]):
    for x1 in X[ds]:
        pred = z.eval({z.arguments[0]: x1})
        results[ds].extend(pred[:, 0])
    a[j].plot(Y[ds], label=ds + ' raw')
    a[j].plot(results[ds], label=ds + ' predicted')
[i.legend() for i in a]
#plt.show()

##Illustrations
#test_results = []
#for x1 in X["test"]:
#    pred = z.eval({z.arguments[0]: x1})
#    test_results.extend(pred[:, 0])
res = results["test"]
df_test_with_predictions, pred_start_timestamp = dfhf.add_list_to_source_df_padding_overlapping(df_test, res, N)
denormalized_predictions = nrm.denormalize_synchronous_len(df_test_with_predictions, scaling_k, predicted_column)
df_test_with_predictions["Restored"] = pd.Series(ldhf.add_padding(denormalized_predictions), df_test_with_predictions.index)
df_test_with_predictions.to_csv(params.io_predictions_data_file)

#Predictions.csv #KOSTYL'
timestamps = df_test_with_predictions.index.tolist()[27:]
predicted = df_test_with_predictions["Restored"].tolist()[27:]
values = df_test_with_predictions["Value"].tolist()[27:]
lines = []
for i in range(0, len(timestamps)):
    lines.append(str(timestamps[i])+","+str(predicted[i])+","+str(values[i])+'\n')
file = open(params.io_folder+"Predictions.csv", 'wt')
file.writelines(lines)



#original_values = df_test_with_predictions["Value"].tolist()[2:]
#
#fig = plt.figure()
#ax0 = fig.add_subplot(111)
#ax0.plot(original_values, label='Actual')
#ax0.plot(denormalized_predictions, label='Predicted')
#ax0.grid(True)
#plt.show()


#todo reconsider loss calculation

print("end")