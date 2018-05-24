#Может быть хуйня с генерацией данных - начало ь(У) выборки начинается с М? - продебажить
#Сид у Дэнс лэйера захардкожен. Проверить хардкоды сидов

import math
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import time

import cntk as C
import cntk.tests.test_utils
from cntk.ops.functions import load_model

import Normalizers.DiffRatioNormalization as nrm
import HelperFunctions.DataFrameHelperFunctions as dfhf
import HelperFunctions.ListDataHelperFunctions as ldhf
from Common.ModelParameters import ModelParameters
cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)


#settings
params = ModelParameters()
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
df_train, df_val, df_test = dfhf.split_df_by_size(df, params.size_validation, params.size_test, N, nrm.source_offset)

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
        m = C.layers.Dropout(0.2)(m) #, seed=1
        m = C.layers.Dense(1)(m)
        return m


def next_batch(x, y):
    """get the next batch to process"""

    def as_batch(data, start, count):
        part = []
        for i in range(start, start + count):
            part.append(data[i])
        return np.array(part)

    for i in range(0, len(x)-BATCH_SIZE, BATCH_SIZE):
        yield as_batch(x, i, BATCH_SIZE), as_batch(y, i, BATCH_SIZE)


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
loss_summary = []
start = time.time()
for epoch in range(0, EPOCHS):
    for x1, y1 in next_batch(X["train"], Y["train"]):
        trainer.train_minibatch({x: x1, l: y1})
    if epoch % (EPOCHS / 10) == 0:
        training_loss = trainer.previous_minibatch_loss_average
        loss_summary.append(training_loss)
        print("epoch: {}, loss: {:.5f}".format(epoch, training_loss))
print("training took {0:.1f} sec".format(time.time() - start))
# A look how the loss function shows how well the model is converging
plt.plot(loss_summary, label='training loss')
z.save(params.io_trained_model_file)