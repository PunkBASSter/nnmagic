from Normalizers.DiffRatioNormalizer import DiffRatioNormalizer
from Normalizers.Normalizer import Parameters
from Normalizers.LogTransformer import LogTransformer

import HelperFunctions.ListDataHelperFunctions as ldhf
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Common.ModelParameters import ModelParameters


def normalize(dataframe):
    """Consumes a DataFrame containing Timestamp and Value, returns list of transformed values for NN input"""
    zz_values = dataframe['Value'].tolist()

    nrm = DiffRatioNormalizer()
    normalized_list = nrm.calculate_norms(zz_values)
    #denormalized_back = nrm.calculate_peaks(zz_values, normalized_list) #without first two values

    #diff = []
    #for i in range(0, len(denormalized_back)):
    #    diff.append(value[i+2] - denormalized_back[i])
    #total_err = sum(diff)

    #Logarithm_transformation:
    #ltr = LogTransformer()
    #strait_log = ltr.calc_logs(normalized_list)
    #reverse_log = ltr.calc_exps(strait_log)
    #ldiff = []
    #for i in range(0, len(normalized_list_log)):
    #    ldiff.append(normalized_list[i] - normalized_list_exp_back[i])
    #total_log_err = sum(ldiff)
    abs_normalized_list = ldhf.calc_abs(normalized_list)
    limit = np.percentile(abs_normalized_list, 90) #Clipping abs values greater than 90 percentile.
    limited_amp_normalized_list = ldhf.limit_by_amp(normalized_list, limit)
    padded_normalized_ltd = ldhf.add_padding(limited_amp_normalized_list) #add padding instead of first 2 samples to put in the same DF
    scaled_normalized_ltd = ldhf.scale_data(padded_normalized_ltd, limit) #scaling data dividing by max amplitude
    return scaled_normalized_ltd, limit


def denormalize(dataframe, scaling_k, col_name = 'Normalized'):
    """Consumes a DataFrame having Values and Vormalized columns; normalization scaling multipler;
     Returns predicted next peak values."""
    zz_values = dataframe['Value'].tolist()
    normalized_list = dataframe[col_name].tolist()

    nrm = DiffRatioNormalizer()
    descaled_normalized = ldhf.scale_data(normalized_list, 1 / scaling_k)
    denormalized_list = nrm.calculate_peaks(zz_values, descaled_normalized)
    padded = ldhf.add_padding(denormalized_list)
    return padded


##Load and prepare Data
#params = ModelParameters()
#df = pd.read_csv(params.io_input_data_file, index_col="Timestamp")
#df.sort_index()

##Normalization example
#norm_data, scaling_k = normalize(df)
#df["Normalized"] = pd.Series(norm_data, df.index)
#df.to_csv(params.io_normalized_data_file)

##Denormalization example
#predicted_data = denormalize(df, scaling_k)
#df["Predicted"] = pd.Series(predicted_data, df.index)
#df.to_csv(params.io_predictions_data_file)


def draw_data_plots(norm_data):
    fig = plt.figure()
    ax0 = fig.add_subplot(211)
    ax0.plot(norm_data)
    ax0.grid(True)
    ax2 = fig.add_subplot(212)
    ax2.hist(norm_data, 500, normed=False, facecolor='g', alpha=0.75)
    ax2.grid(True)
    #ax3 = fig.add_subplot(413)
    #ax3.plot(abs_normalized_list)
    #ax3.grid(True)
    #ax4 = fig.add_subplot(414)
    #ax4.hist(abs_normalized_list, 500, normed=False, facecolor='g', alpha=0.75)
    #ax4.grid(True)
    plt.show()
#draw_data_plots(norm_data)

print("Data Normalization completed.")


