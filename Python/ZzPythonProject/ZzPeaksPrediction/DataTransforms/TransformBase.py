import pandas as pd


class TransformParams(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for key, value in kwargs.items():
        #     setattr(self, key, value)

    def __repr__(self):
        # todo implement method
        return f"{type(self)}: {self.__dict__} and {super(TransformParams, self).__repr__()}"

    def __setattr__(self, key, value):
        self.__setitem__(key, value)
        super(TransformParams, self).__setattr__(key, value)

    def __getitem__(self, item):
        v = super(TransformParams, self).get(item)
        return self.__dict__[item] if not v else v


class TransformBase:
    params: TransformParams = None

    def __init__(self, params: TransformParams, **kwargs):
        self.params = params

        for key, value in kwargs.items():
            setattr(self, key, value)

    def transform(self, series: pd.Series) -> pd.Series:
        return series

    def inv_transform(self, series: pd.Series) -> pd.Series:
        return series

    def __repr__(self):
        # todo implement method
        return f"{type(self)}: params:{self.params}"
