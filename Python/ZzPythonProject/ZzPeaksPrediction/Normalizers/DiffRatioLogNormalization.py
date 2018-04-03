from Normalizers.DiffRatioNormalizer import DiffRatioNormalizer
from Normalizers.Normalizer import Parameters
from Normalizers.LogTransformer import LogTransformer

import HelperFunctions.ListDataHelperFunctions as ldhf
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt





params = Parameters()

df = pd.read_csv(params.input_file_path)
df.sort_values(by=['Timestamp'])

time = df['Timestamp'].tolist()
value = df['Value'].tolist()

nrm = DiffRatioNormalizer(params)
normalized_list = nrm.calculate_norms(value)
#denormalized_back = nrm.calculate_peaks(value, normalized_list) #without first two values

#diff = []
#for i in range(0, len(denormalized_back)):
#    diff.append(value[i+2] - denormalized_back[i])
#total_err = sum(diff)

ltr = LogTransformer()
strait_log= ltr.calc_logs(normalized_list)

#reverse_log = ltr.calc_exps(strait_log)
#ldiff = []
#for i in range(0, len(normalized_list_log)):
#    ldiff.append(normalized_list[i] - normalized_list_exp_back[i])
#total_log_err = sum(ldiff)


abs_normalized_list = ldhf.calc_abs(normalized_list)
limit = np.percentile(abs_normalized_list, 90)
limited_amp_normalized_list = ldhf.limit_by_amp(normalized_list, limit)


padded = ldhf.add_padding(normalized_list)



print("Ololo")


def draw_plots():
    fig = plt.figure()
    ax0 = fig.add_subplot(411)
    ax0.plot(limited_amp_normalized_list)
    ax0.grid(True)
    ax2 = fig.add_subplot(412)
    ax2.hist(limited_amp_normalized_list, 500, normed=False, facecolor='g', alpha=0.75)
    ax2.grid(True)
    ax3 = fig.add_subplot(413)
    ax3.plot(abs_normalized_list)
    ax3.grid(True)
    ax4 = fig.add_subplot(414)
    ax4.hist(abs_normalized_list, 500, normed=False, facecolor='g', alpha=0.75)
    ax4.grid(True)

    plt.show()