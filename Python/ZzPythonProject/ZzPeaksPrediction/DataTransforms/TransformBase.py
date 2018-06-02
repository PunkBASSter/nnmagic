class TransformBase:

    def transform(self, series, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")

    def inv_transform(self, series, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")
