import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow import _keras
from keras.layers import Dense, Dropout, LSTM
from keras.models import Sequential

# Type of crypto Currency needed to find the network model
crypto_currency = 'BTC'
# Model against USD to get the values as a model
against_currency = 'USD'
# Start date of the model to predict the data from 
start = dt.datetime(2016,1,1)
# Value to be predicted till the end
end = dt.datetime.now()
# Reads the value from the YAHOO FINANCE API
data = web.DataReader(f'{crypto_currency}-{against_currency}', 'yahoo', start, end)
