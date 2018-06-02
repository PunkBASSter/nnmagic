from DataTransforms.TransformBase import TransformBase


class ChainedTransform(TransformBase):

    _transformation_sequence = []

    def __init__(self, *args :TransformBase):
        for arg in args:
            self._transformation_sequence.append(arg)


    def transform(self, series, **kwargs):
        length =  len(self._transformation_sequence)
        if length < 2: raise ValueError("Sequence must contain at least 2 elements.")

        res = self._transformation_sequence[0].transform(series, kwargs)
        for i in range(1,length):
            res = self._transformation_sequence[i].transform(res, kwargs)

        return res

    def inv_transform(self, series, **kwargs):
        length = len(self._transformation_sequence)
        if length < 2: raise ValueError("Sequence must contain at least 2 elements.")

        sequence = self._transformation_sequence.reverse()
        res = sequence[0].inv_transform(series, kwargs)
        for i in range(1, length):
            res = sequence[i].inv_transform(res, kwargs)

        return res
