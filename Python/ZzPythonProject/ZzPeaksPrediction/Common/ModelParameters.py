class ModelParameters:

    #Files and folders IO params
    io_mt_data_file_prefix = "Dzz"
    io_mt_symbol_name = "EURUSD.m"
    io_mt_timeframe = "PERIOD_H1"
    io_data_file_ext = ".csv"
    io_file_name_base = io_mt_data_file_prefix + "_" + io_mt_symbol_name + "_" + io_mt_timeframe
    io_folder = "C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\"
    io_input_data_file = io_folder + io_file_name_base + io_data_file_ext
    io_normalized_data_file = io_folder + "Normalized_" + io_file_name_base + io_data_file_ext
    io_predictions_data_file = io_folder + "Denormalized_" + io_file_name_base + io_data_file_ext
    io_trained_model_file = io_folder + "Trained_Model_" + io_file_name_base + ".cmf"

    #Sample size parameters
    size_test = 0.2
    size_validation = 0.1

    #Prediction settings
    pred_N = 25  # input: N subsequent values
    pred_M = 1  # output: predict 1 value M steps ahead

    # Training parameters
    learn_training_steps = 10000
    learn_batch_size = 100
    learn_epochs = 200
    learn_learning_rate = 0.01

    # Normalization params
    norm_high_amp_limit = None
    norm_logarithm_base = None