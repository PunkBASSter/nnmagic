from matplotlib import pyplot as plt
from cntk.ops.functions import load_model
import time
import cntk as C
import cntk.tests.test_utils
import HelperFunctions.ArrayDataHelperFunctions as adhf


cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)


class ModelTrainer:
    _params = None
    _x = None
    _l = None
    _z = None
    _trainer = None

    def __init__(self, params, z = None):
        self._params = params
        self.init_model()
        if not z is None: self._z = z
        self.init_trainer()


    def create_model(self):
        """Create the model for time series prediction"""
        with C.layers.default_options(initial_state=0.1):
            m = C.layers.Recurrence(C.layers.LSTM(self._params.pred_N))(self._x)
            m = C.sequence.last(m)
            m = C.layers.Dropout(self._params.nn_dropout)(m)  # , seed=1
            m = C.layers.Dense(1)(m)
            return m

    def init_model(self):
        self._x = C.sequence.input_variable(1)
        self._z = self.create_model()
        self._l = C.input_variable(1, dynamic_axes=self._z.dynamic_axes, name="y")

    def init_trainer(self):
        learning_rate = 0.01
        lr_schedule = C.learning_parameter_schedule(learning_rate)

        # loss function
        loss = C.squared_error(self._z, self._l)
        # use squared error to determine error for now
        error = C.squared_error(self._z, self._l)

        momentum_schedule = C.momentum_schedule(0.9, minibatch_size=self._params.learn_batch_size)
        learner = C.fsadagrad(self._z.parameters,
                              lr=lr_schedule,
                              momentum=momentum_schedule,
                              unit_gain=True)

        trainer = C.Trainer(self._z, (loss, error), [learner])
        self._trainer = trainer

    def train(self, train_x, train_y):
        # train
        loss_summary = []
        start = time.time()
        for epoch in range(0, self._params.learn_epochs):
            for x1, y1 in adhf.next_batch(train_x, train_y, self._params.learn_batch_size):
                self._trainer.train_minibatch({self._x: x1, self._l: y1})
            if epoch % (self._params.learn_epochs / 10) == 0:
                training_loss = self._trainer.previous_minibatch_loss_average
                loss_summary.append(training_loss)
                print("epoch: {}, loss: {:.5f}".format(epoch, training_loss))
        print("training took {0:.1f} sec".format(time.time() - start))
        # A look how the loss function shows how well the model is converging
        plt.plot(loss_summary, label='training loss')
        self._z.save(self._params.io_trained_model_file)

    def load_model(self):
        self._z = load_model(self._params.io_trained_model_file)

    def get_mse(self, X, Y):
        result = 0.0
        for x1, y1 in adhf.next_batch( X, Y, self._params.learn_batch_size ):
            eval_error = self._trainer.test_minibatch( {self._x: x1, self._l: y1} )
            result += eval_error
        return result / len(X)
