import cntk.tests.test_utils
import HelperFunctions.ArrayDataHelperFunctions as adhf
cntk.tests.test_utils.set_device_from_pytest_env() # (only needed for our build system)


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
