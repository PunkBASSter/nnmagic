class ModelParameters:

    def __init__(self):
        # Files and folders IO params
        self.io_mt_data_file_prefix = "Dzz"
        self.io_mt_symbol_name = "EURUSD.m"
        self.io_mt_timeframe = "PERIOD_H1"
        self.io_file_name = f"{self.io_mt_data_file_prefix}_{self.io_mt_symbol_name}_{self.io_mt_timeframe}"
        self.io_folder = "C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\"
        self.io_input_data_file = self.io_folder + self.io_file_name + ".csv"
        self.io_predictions_data_file = self.io_folder + "Predictions_" + self.io_file_name + ".csv"
        self.io_trained_model_file = self.io_folder + "Trained_Model_" + self.io_file_name + ".cmf"

        #Sample size parameters
        self.data_validation_sample_part = 0.1
        self.data_test_sample_part = 0.33
        self.data_timestamp_column = "Timestamp"
        self.data_value_column = "Value"
        self.data_normalized_column = "Normalized"

        #Prediction settings    self.
        self.pred_N = 12  # input: N subsequent values
        self.pred_M = 1  # output: predict 1 value M steps ahead (should be always 1 if Diff or Division transforms are used)

        #NN parameters
        self.nn_dropout = 0.15

        # Training parameters
        self.learn_training_steps = 10000
        self.learn_batch_size = 100
        self.learn_epochs = 250
        self.learn_learning_rate = 0.01
