from Normalizers.Normalizer import Normalizer
import HelperFunctions.ListDataHelperFunctions as ldhf
import numpy as np


class DiffRatioNormalizer(Normalizer):

    value_column = 'Value'
    predictions_column = 'Predicted'
    _source_list = None
    _normalized_list = None
    _source_offset = 2

    def _calculate_norm(self, currentZz, prevZz, preprevZz):
        sign = -1 if currentZz < prevZz else 1
        diff2 = currentZz - prevZz
        diff1 = prevZz - preprevZz
        div = diff2/diff1*sign
        return div

    def _calculate_peak(self, currentZz, prevZz, nnPredicted):
        sign = 1 if currentZz < prevZz else -1
        div = nnPredicted
        diff1 = currentZz - prevZz
        diff2 = div*diff1/sign
        nextZz = diff2 + currentZz
        return nextZz

    def _calculate_norms(self, values):
        # To calculate 1 item it's required 3 consequent peaks, so overall length is 2 items shorter
        self._normalized_list = []
        for i in range(2, len(values)):
            self._normalized_list.append(self._calculate_norm(values[i], values[i - 1], values[i - 2]))
        return self._normalized_list

    def _calculate_peaks(self, values, normalized_list = None):
        # Returns list of denormalized peaks based on 2 peaks and 1 normalization (originally based on 3 peaks)
        if normalized_list is None:
            normalized_list = self._normalized_list
        denormalized_list = []
        for i in range(0, len(normalized_list)):
            denormalized_list.append(self._calculate_peak(values[i + 1], values[i], normalized_list[i]))
        return denormalized_list

    def normalize(self, dataframe, add_padding=False, limit_percentile=100):
        """Consumes a DataFrame containing Timestamp and Value, returns list of transformed values for NN input"""
        zz_values = dataframe[self.value_column].tolist()

        normalized_list = self._calculate_norms(zz_values)

        abs_normalized_list = ldhf.calc_abs(normalized_list)
        limit = np.percentile(abs_normalized_list, limit_percentile)  # Clipping abs values greater than 90 percentile.
        limited_amp_normalized_list = ldhf.limit_by_amp(normalized_list, limit)
        padded_normalized_ltd = ldhf.add_padding(
            limited_amp_normalized_list) if add_padding else limited_amp_normalized_list  # add padding instead of first 2 samples to put in the same DF
        scaled_normalized_ltd = ldhf.scale_data(padded_normalized_ltd, limit)  # scaling data dividing by max amplitude

        self._scaling_k = limit
        return scaled_normalized_ltd

    def denormalize(self, dataframe, target_col_name='Normalized', add_padding=False):
        """Consumes a DataFrame having Values and Normalized columns; normalization scaling multipler;
         Returns predicted next peak values."""
        zz_values = dataframe[self.value_column].tolist()
        normalized_list = dataframe[target_col_name].tolist()

        descaled_normalized = ldhf.scale_data(normalized_list, 1 / self._scaling_k)
        denormalized_list = self._calculate_peaks(zz_values, descaled_normalized)
        padded = ldhf.add_padding(denormalized_list) if add_padding else denormalized_list
        return padded

    def denormalize_synchronous_len(self, dataframe, col_name='Predicted'):
        zz_values = dataframe[self.value_column].tolist()
        predictions = dataframe[col_name].tolist()

        descaled_normalized = ldhf.scale_data(predictions, 1 / self._scaling_k)
        denormalized_predictions = self._calculate_peaks(zz_values, descaled_normalized[2:])
        return denormalized_predictions
