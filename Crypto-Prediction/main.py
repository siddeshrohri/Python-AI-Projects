import pandas as pd
import requests
import matplotlib as plt
import numpy as np
import json

from sklearn.metrics import train_test_split

# Using the API to extract the data
# Requests the data from the API with the specified parameters "BTC and CAD, limit 500"
# Creating a DataFrame to access the values parsed as JSON data
# JSON formatted text being converted to Python Dictionary using "Data" for the DataFrame to access 
# Set the index of the DataFrame to "time"
# Convert the values of the key 'date' to datetime format in seconds
# Removing the columns from the DataFrame
# Prints all the values from High to Low of the currency 
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

# Splitting the dataset into 2 seperate datasets
# First dataset is for training and the second dataset for testing 
# Calculating the row index at which the DataFrame should be split
# Storing a DataFrame for Training
# Storing the DataFrame for Testing
# Returning the values
def train_test_split(df, test_size=0.2):
    row = len(df) - int(test_size * len(df))
    train_data = df.iloc[:row]
    test_data = df.iloc[row:]
    return train_data, test_data
