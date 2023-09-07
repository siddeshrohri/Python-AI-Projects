import pandas as pd
import requests
import matplotlib as plt
import numpy as np
import json

# Using the API to extract the data
# Requests the data from the API with the specified parameters "BTC and CAD, limit 500"
# Creating a DataFrame to access the values parsed as JSON data
# JSON formatted text being converted to Python Dictionary using "Data" for the DataFrame to access 
# Set the index of the DataFrame to "time"
# Convert the values of the key 'date' to datetime format in seconds
# Removing the columns from the DataFrame
# Prints all the values from High to Low of the currency 
api = 'https://min-api.cryptocompare.com/data/histoday'
requests_input = requests.get(api + '?fsym=BTC&tsym=CAD&limit=500')
hist = pd.DataFrame(json.loads(requests_input.content)['Data'])
hist = hist.set_index('time')
hist.index = pd.to_datetime(hist.index, unit='s')
hist.drop(["conversionType", "conversionSymbol"], axis = 'columns', inplace = True)
print(hist.head(5))