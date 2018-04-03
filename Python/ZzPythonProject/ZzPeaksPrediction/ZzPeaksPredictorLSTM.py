from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import time
import cntk as C
import cntk.tests.test_utils
import ZzPeaksPrediction.LstmHelperFunctions as hlp
cntk.tests.test_utils.set_device_from_pytest_env()


VALIDATION_SAMPLE_PART = 0.2
TEST_SAMPLE_PART = 0.3
WINDOW_SIZE = 5 # input: N subsequent values
FORECAST_SIZE = 2 # output: predict 1 value M steps ahead
DATA = pd.read_csv("Normalized_DzzExportEURUSD.mPERIOD_H1.csv",
                  usecols=["ValueDiffRatio_LogWithMaxAbsBase"], dtype=np.float32).values

WINDOW_SIZE_START = FORECAST_SIZE
WINDOW_SIZE_END = WINDOW_SIZE_START + 1
next_batch = hlp.next_batch_seq


x_all, y_all = hlp.generate_data(DATA, 1, 3, 2)
X = hlp.split_data(x_all, VALIDATION_SAMPLE_PART, TEST_SAMPLE_PART)
Y = hlp.split_data(y_all, VALIDATION_SAMPLE_PART, TEST_SAMPLE_PART)


def create_model(x):
    """Create the model for time series prediction"""
    with C.layers.default_options(initial_state = 0.1):
        m = C.layers.Recurrence(C.layers.LSTM(WINDOW_SIZE_END))(x)
        m = C.sequence.last(m)
        m = C.layers.Dropout(0.2)(m)
        m = C.layers.Dense(1)(m)
        return m


# Training parameters
TRAINING_STEPS = 10000
BATCH_SIZE = 100
EPOCHS = 10

x = C.sequence.input_variable(1)
z = create_model(x)
l = C.input_variable(tuple([FORECAST_SIZE, 1]), dynamic_axes=z.dynamic_axes, name="y")

learning_rate = 0.001
lr_schedule = C.learning_parameter_schedule(learning_rate)
loss = C.squared_error(z, l)
error = C.squared_error(z, l)
momentum_schedule = C.momentum_schedule(0.9, minibatch_size=BATCH_SIZE)
learner = C.fsadagrad(z.parameters,
                      lr = lr_schedule,
                      momentum = momentum_schedule,
                      unit_gain = True)
trainer = C.Trainer(z, (loss, error), [learner])



#train
loss_summary = []
start = time.time()
for epoch in range(0, EPOCHS):
    for x1, y1 in next_batch(X, Y, "train", BATCH_SIZE):
        trainer.train_minibatch({x: x1, l: y1})
    training_loss = trainer.previous_minibatch_loss_average
    loss_summary.append(training_loss)
print("training took {0:.1f} sec".format(time.time() - start))


# A look how the loss function shows how well the model is converging
plt.plot(loss_summary, label='training loss');

# validate
def get_mse(X,Y,labeltxt):
    result = 0.0
    for x1, y1 in hlp.next_batch(X, Y, labeltxt, BATCH_SIZE):
        eval_error = trainer.test_minibatch({x : x1, l : y1})
        result += eval_error
    return result/len(X[labeltxt])

# Print the train and validation errors
for labeltxt in ["train", "val"]:
    print("mse for {}: {:.6f}".format(labeltxt, get_mse(X, Y, labeltxt)))

#z.save('trained_model.cmf')


#pred
results = []
for x1, y1 in next_batch(X, Y, "test", BATCH_SIZE):
    pred = z.eval({x: x1})
    results.extend(pred[:, 0])



# predict
f, a = plt.subplots(3, 1, figsize = (12, 8))
for j, ds in enumerate(["train", "val", "test"]):
    results = []
    for x1, y1 in hlp.next_batch(X, Y, ds, BATCH_SIZE):
        pred = z.eval({x: x1})
        results.extend(pred[:, 0])
    a[j].plot(Y[ds], label = ds + ' raw');
    a[j].plot(results, label = ds + ' predicted');
[i.legend() for i in a];

