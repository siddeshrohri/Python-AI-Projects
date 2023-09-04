from tensorflow import keras
import requests
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, LSTM
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Requests the data from the API
res = requests.get('https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=500')
# Stored the JSON response in the variable to avoid multiple calls 
json_data = json.loads(res.content)
# Addition of a condition to check if the expected keys are present in the JSON structure 
if 'Data' in json_data and 'Data' in json_data['Data']:
    # Creating a DataFrame, assuming that the relevant data is nested under the above condition
    hist = pd.DataFrame(json_data['Data']['Data'])
    # This is used to convert the time column to a datetime format
    hist['time'] = pd.to_datetime(hist['time'], unit='s')
    # Sets the time column as the index of the DataFrame
    hist = hist.set_index('time')
    # Closing values
    target_col = 'close'
    # Test print for the first five objects of the API
    # print(hist.head(5))

# Splitting the data set into two sets
# One Set is training 80%
# Second Set is test 20%
# Arguments:- A DataFrame and the test size percentage to be used
def train_test_split(df, test_size=0.2):
    # Calculates the total number of rows that should be in the training set
    split_row = len(df) - int(test_size * len(df))
    # This line selects the rows from the beginning up to the split_row
    train_data = df.iloc[:split_row]
    # This line selects the rows starting from the split_row index to the end of the DataFrame df
    test_data = df.iloc[split_row:]
    # Returns the values
    return train_data, test_data
# Passing the values into the test model
train, test = train_test_split(hist, test_size=0.2)

# Params:- line1 and line2 are data arrays representing the lines to be plotted
# label1 and label2, these are labels for the legend entries of line1 and line 2
# title:- Title of the plot graph
# lw:- Line width of the plot graph line
def line_plot(line1, line2, label1=None, label2=None, title='', lw=2):
    # Creates a single subplot within a figure with a specified size 
    fig, ax = plt.subplots(1, figsize=(13, 7))
    # Plots the first line 
    ax.plot(line1, label=label1, linewidth=lw)
    # Plots the second line
    ax.plot(line2, label=label2, linewidth=lw)
    # Uses Canadian Dollar and a specific fontsize
    ax.set_ylabel('price [CAD]', fontsize=14)
    # Sets the title for the graph
    ax.set_title(title, fontsize=16)
    # Sets the legend of the graph plotted
    ax.legend(loc='best', fontsize=16)
    # Shows the graph on screen
    plt.show()
# Passes the values to the function
line_plot(train[target_col], test[target_col], 'training', 'test', title='')

# Performs zero_based normalization on the data within the DataFrame
def normalise_zero_base(df):
    return df / df.iloc[0] - 1

# Normalizing a function using min_max algorithm
def normalize_min_max(df):
    # Formula for normalizing the function
    return (df - df.min()) / (df.max() - df.min())

# Extracts the windowed data from the DataFrame
# PARAMS:- DataFrame(df), Length of the window to be extracted (window_len), Normalize the rows of data (zero_base)
def windowed_data_extraction(df, window_len = 5, zero_base = True):
    # Creating an empty list which will contain all windows
    windowed_data = []
    # Loop through each entry in the time series dataset
    for idx in range((len(df)-window_len)):
        # Slicing the DataFrame to extract a window of rows with a length of window_len using idx variable as the starting index
        tmp = df[idx: (idx + window_len)].copy()
        # Checks for the condition of the zero_base value
        if not zero_base == False :
            # Normalizes the values of the windowed data using the above function call
            tmp = normalise_zero_base(tmp)
            # Appends the value of the normalized values into the empty list
        windowed_data.append(tmp.values())
    # Converts it back into numpy array format so that we can use it further down
    return np.array(windowed_data)

# Preparing the data to feed into the neural network
# The repeat process of splitting the data into two datasets
# Training dataset - 80% and Testing dataset - 20%
def prepare_data(df, target_col, window_len=10, zero_base=True, test_size=0.2):
    train_data, test_data = train_test_split(df, test_size=test_size)
    # Windowing the training set
    X_train = windowed_data_extraction(train_data, window_len, zero_base)
    # Windowing the testing set
    X_test = windowed_data_extraction(test_data, window_len, zero_base)
    # Slicing the values of the training DataSet 
    y_train = train_data[target_col][window_len:].values
    # Converting them into one-hot encoding format
    y_test = test_data[target_col][window_len:].values
