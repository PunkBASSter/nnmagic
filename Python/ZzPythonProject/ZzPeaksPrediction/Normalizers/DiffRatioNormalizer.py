from Normalizers.Normalizer import Normalizer


class DiffRatioNormalizer(Normalizer):

    _source_list = None
    _normalized_list = None

    def calculate_norm(self, currentZz, prevZz, preprevZz):
        sign = -1 if currentZz < prevZz else 1
        diff2 = currentZz - prevZz
        diff1 = prevZz - preprevZz
        div = diff2/diff1*sign
        return div

    def calculate_peak(self, currentZz, prevZz, nnPredicted):
        sign = 1 if currentZz < prevZz else -1
        div = nnPredicted
        diff1 = currentZz - prevZz
        diff2 = div*diff1/sign
        nextZz = diff2 + currentZz
        return nextZz

    def calculate_norms(self, values):
        # To calculate 1 item it's required 3 consequent peaks, so overall length is 2 items shorter
        self._normalized_list = []
        for i in range(2, len(values)):
            self._normalized_list.append(self.calculate_norm(values[i], values[i - 1], values[i - 2]))
        return self._normalized_list

    def calculate_peaks(self, values, normalized_list = None):
        # Returns list of denormalized peaks based on 2 peaks and 1 normalization (originally based on 3 peaks)
        if normalized_list is None:
            normalized_list = self._normalized_list
        denormalized_list = []
        for i in range(0, len(normalized_list)):
            denormalized_list.append(self.calculate_peak(values[i + 1], values[i], normalized_list[i]))
        return denormalized_list
