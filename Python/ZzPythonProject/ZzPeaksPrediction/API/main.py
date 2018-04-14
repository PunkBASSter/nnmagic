import numpy as np
from cntk.ops.functions import load_model
from eve import Eve
from flask import request

from Normalizers.DiffRatioNormalization import DiffRatioNormalizer

app = Eve()
model_nn = 0


@app.route("/ololo")
def hello():
    return "Hello World!"


@app.route('/flaskforecast', methods=['POST'])
def forecast():

    req = request.get_json()
    data = req['data']

    normalizer = DiffRatioNormalizer(DiffRatioLogNormalizerParameters(len(data))) #25+2
    normalized_data = normalizer.normalize(data)

    transformed_normalized_data = np.asarray(normalized_data, float).reshape(len(normalized_data), 1)

    predicted = model_nn.eval({model_nn.arguments[0]: transformed_normalized_data})[0]

    denormalized_prediction = normalizer.denormalize_single(predicted[0])

    return str(denormalized_prediction)


if __name__ == '__main__':

    model_nn = load_model("myEzLstm.cmf")

    app.run(port=80)
