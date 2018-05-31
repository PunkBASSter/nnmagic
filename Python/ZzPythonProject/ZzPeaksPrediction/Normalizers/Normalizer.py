class Normalizer:
    """Input sequences must be sorted by timestamp ascending"""
    _params = None
    _scaling_k = 1
    _source_offset = 0

    def get_source_offset(self):
        return self._source_offset

    def __init__(self, params=None):
        self._params = params

    def normalize(self, dataframe, add_padding=False, limit_percentile=100):
        raise NotImplementedError("Subclass must implement abstract method")

    def denormalize(self, dataframe, target_col_name='Normalized', add_padding=False):
        raise NotImplementedError("Subclass must implement abstract method")

    def denormalize_synchronous_len(self, dataframe, col_name='Predicted'):
        raise NotImplementedError("Subclass must implement abstract method")
