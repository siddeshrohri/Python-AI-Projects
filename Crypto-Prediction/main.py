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
    print(hist.head(5))

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