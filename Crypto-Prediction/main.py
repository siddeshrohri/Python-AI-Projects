from tensorflow import keras
import requests
import pandas as pd
import json

# Requests the data from the API
res = requests.get('https://min-api.cryptocompare.com/data/v2/histoday?fsym=BTC&tsym=USD&limit=500')
# Stored the JSOn response in the variable to avoid multiple calls 
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
else:
    print("Data format is not as expected.")
