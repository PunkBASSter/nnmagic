import cntk.tests.test_utils
import cntk as C
import HelperFunctions.ArrayDataHelperFunctions as adhf
cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)


class ModelEvaluator:
    _params = None
    _z = None
    _last_result = None
    _evaluator = None


    def __init__(self, model, params):
        self._params = params
        self._z = model
        self._evaluator = C.Evaluator(C.squared_error(self._z, C.input_variable(1, dynamic_axes=self._z.dynamic_axes, name="y")))

    def evaluate(self, sample, batch_size=1):
        res = []
        for x in adhf.next_value(sample, batch_size):
            predicted = self._z.eval({self._z.arguments[0]: x})
            error = self._z.test
            res.extend(predicted[:, 0])

        self._last_result = res
        return res

    def get_mse(self, X, Y):
        result = 0.0
        for x1, y1 in adhf.next_batch( X, Y, self._params.learn_batch_size ):
            eval_error = self._evaluator.test_minibatch( {self._z.arguments[0]: x1, self._z.arguments[1]: y1} )
            result += eval_error
        return result / len( X )
