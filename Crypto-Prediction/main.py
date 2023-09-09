import pandas as pd
import requests
import matplotlib.pyplot as plt
import numpy as np
import json

from sklearn.model_selection import train_test_split

''' FETCHING THE DATA '''

# Using the API to extract the data
# Requests the data from the API with the specified parameters "BTC and CAD, limit 500"
# Creating a DataFrame to access the values parsed as JSON data
# JSON formatted text being converted to Python Dictionary using "Data" for the DataFrame to access 
# Set the index of the DataFrame to "time"
# Convert the values of the key 'date' to datetime format in seconds
# Removing the columns from the DataFrame
# Prints all the values from High to Low of the currency 
close = 'close'
api = 'https://min-api.cryptocompare.com/data/histoday'
params ={
    'fsym' : 'BTC',
    'tsym' : 'CAD',
    'limit': 500
}
response = requests.get(api, params=params)
data = response.json()['Data']
hist = (
    pd.DataFrame(data)
    .set_index('time')
    .assign(time=lambda x: pd.to_datetime(x.index, unit='s'))
    .drop(columns=["conversionType", "conversionSymbol"])
)
print(hist.head(5))

''' SPLITTING THE DATA '''

# Splitting the dataset into 2 seperate datasets
# First dataset is for training and the second dataset for testing 
# Calculating the row index at which the DataFrame should be split
# Storing a DataFrame for Training
# Storing the DataFrame for Testing
# Returning the values
# Included an Alternative implementation as well
def train_test_split(df, test_size=0.2):
    row = len(df) - int(test_size * len(df))
    # Alternative calculation
    # row = int(len(df) * (1 - test_size))
    train_data = df.iloc[:row]
    test_data = df.iloc[row:]
    return train_data, test_data
train, test = train_test_split(hist, test_size=0.2)

# Alternative Method for splitting the data into two sets 
# def train_test_split(df, test_size=0.2):
#     train_data, test_data = train_test_split(df, test_size=test_size, shuffle = False)
#     return train_data, test_data

''' PLOTTING THE GRAPH '''

# Creating a figure with 1 subplot adn 13 units wide and 7 units tall
# Adds a line to the graph line1
# Adds a line to the graph line2
# Sets the Title of the graph
# Sets the y-axis of the graph to the desired title
# Displays the legends with the labels on the screen
# Displaying the Graph
def graph(line1, line2, label1=None, label2=None, title=''):
    fig, ax = plt.subplots(1, figsize = (13, 7))
    ax.plot(line1, label = label1, color = "Green")
    ax.plot(line2, label = label2, color = "Red")
    ax.set_title(title, fontsize = 16)
    ax.set_ylabel('PRICE [CAD]', fontsize = 14)
    ax.legend(loc = "best", fontsize = 16)
graph(train[close], test[close], 'training', 'test', title="")
plt.show()

''' NORMALIZING THE DATA '''

# Using the ZERO BASELINE normalization technique
# This part of the code divides every value in the dataframe by the first element 
# Essentially it calculates the relative change of each data point compared  to the initial values, centers around zero
# Subtracting one from the resultant value , this step is done to represent the relative change as a percentage change
def normalization_zero_baseline(df):
    normalizing = df / df.iloc[0] - 1
    return normalizing

# Using the MIN MAX SCALING normalization technique
# Subtracting the minimum value of the dataframe from every datapoint
# Dividing each point by its maximum value minus it's minumum value
def normalization_min_max_scaling(df):
    normalizing = (df - df.min()) / (df.max() - df.min())
    return normalizing

''' EXTRACTING WINDOWED DATA '''

# Extracts windowed sequences of data from the DataFrame
# Creating input samples for a LSTM neural network model
# Initializing an empty array where the extracted windowed sequences of data will be stored
# Iterating through a DataFrame over the rows of the DataFrame to create the sliding windows
# Slicing the DataFrame according to the index
# If the zero_base is true, normalization is performed on the dataset
# The normalized values are appended to the array
# Converts the windowed sequences of data into numpy array 
def extract_windowed_data(df, window_len=5, zero_base=True):
    windowed_sequences = []
    for idx in range(len(df) - window_len):
        window = df[idx : (idx + window_len)].copy()
        if zero_base:
            window = normalization_min_max_scaling(window)
        windowed_sequences.append(window.values)
    return np.array(windowed_sequences)

''' PREPARING THE DATA FOR TRAINING '''

# Splitting the data into training and testing sets
# Extracting windowed sequences for training and testing
# Extracting target values for training and testing
# Optionally applying zero baseline normalization to target values
# Returning prepared datasets
def preparing_the_data(df, close, window_len = 10, zero_base = True, test_size = 0.2):
    train_data, test_data = train_test_split(df, test_size=test_size)
    X_train = extract_windowed_data(train_data, window_len, zero_base)
    X_test = extract_windowed_data(test_data, window_len, zero_base)
    y_train = train_data[close][window_len:].values
    y_test = test_data[close][window_len:].values
    if zero_base:
        y_train = y_train / train_data[close][:-window_len].values - 1
    return train_data, test_data, X_train, X_test, y_train, y_test
