#Files and folders
folder = "C:\\Users\\PunkBASSter\\AppData\\Roaming\\MetaQuotes\\Terminal\\Common\\Files\\"
data_file_ext = ".csv"
input_data_file = folder + "Dzz_EURUSD.m_PERIOD_H1" + data_file_ext
normalized_data_file = folder + "Normalized_" + input_data_file
predictions_data_file = "Denormalized_" + input_data_file
trained_model_file = "Trained_Model"

#Prediction options
N = 25  # input: N subsequent values
M = 1  # output: predict 1 value M steps ahead

# Training parameters
TRAINING_STEPS = 10000
BATCH_SIZE = 100
EPOCHS = 200 #if isFast else 200
LEARNING_RATE = 0.01
