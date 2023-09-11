import json
import requests
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, LSTM
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

def fetch_crypto_data():
    close = 'close'
    api = 'https://min-api.cryptocompare.com/data/histoday'
    params = {
        'fsym': 'BTC',
        'tsym': 'CAD',
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
    return hist

def split_data(df, test_size=0.2):
    row = len(df) - int(test_size * len(df))
    train_data = df.iloc[:row]
    test_data = df.iloc[row:]
    return train_data, test_data

def plot_graph(line1, line2, label1=None, label2=None, title=''):
    fig, ax = plt.subplots(1, figsize=(13, 7))
    ax.plot(line1, label=label1, color="Green")
    ax.plot(line2, label=label2, color="Red")
    ax.set_title(title, fontsize=16)
    ax.set_ylabel('PRICE [CAD]', fontsize=14)
    ax.legend(loc="best", fontsize=16)
    plt.show()

def normalize_data_zero_baseline(df):
    if isinstance(df, pd.DataFrame):
        df = df.select_dtypes(include=[np.number])  # Select numeric columns
        normalizing = df / df.iloc[0] - 1
        return normalizing
    else:
        raise ValueError("Input should be a pandas DataFrame.")

def extract_windowed_data(df, window_len=5, zero_base=True):
    windowed_sequences = []
    for idx in range(len(df) - window_len):
        window = df[idx: (idx + window_len)].copy()
        if zero_base:
            window = normalize_data_zero_baseline(window)
        windowed_sequences.append(window.values)
    return np.array(windowed_sequences)

def prepare_data(df, target_col, window_len=10, zero_base=True, test_size=0.2):
    train_data, test_data = split_data(df, test_size=test_size)
    X_train = extract_windowed_data(train_data, window_len, zero_base)
    X_test = extract_windowed_data(test_data, window_len, zero_base)
    y_train = train_data[target_col][window_len:].values
    y_test = test_data[target_col][window_len:].values
    if zero_base:
        y_train = y_train / train_data[target_col][:-window_len].values - 1
        y_test = y_test / test_data[target_col][:-window_len].values - 1

    return train_data, test_data, X_train, X_test, y_train, y_test

def build_lstm_model(input_data, output_size, neurons=100, activ_func='linear',
                     dropout=0.2, loss='mse', optimizer='adam'):
    model = Sequential()
    model.add(LSTM(neurons, input_shape=(input_data.shape[1], input_data.shape[2])))
    model.add(Dropout(dropout))
    model.add(Dense(units=output_size))
    model.add(Activation(activ_func))

    model.compile(loss=loss, optimizer=optimizer)
    return model

def main():
    np.random.seed(42)
    window_len = 5
    test_size = 0.2
    zero_base = True
    lstm_neurons = 100
    epochs = 20
    batch_size = 32
    loss = 'mse'
    dropout = 0.2
    optimizer = 'adam'
    close = 'close'

    hist = fetch_crypto_data()
    train, test, X_train, X_test, y_train, y_test = prepare_data(
        hist, close, window_len=window_len, zero_base=zero_base, test_size=test_size)
    model = build_lstm_model(
        X_train, output_size=1, neurons=lstm_neurons, dropout=dropout, loss=loss,
        optimizer=optimizer)
    history = model.fit(
        X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size, verbose=1, shuffle=True)

    targets = test[close][window_len:]
    preds = model.predict(X_test).squeeze()
    mae = mean_absolute_error(preds, y_test)

    preds = test[close].values[:-window_len] * (preds + 1)
    preds = pd.Series(index=targets.index, data=preds)

    plot_graph(targets, preds, 'actual', 'prediction')

if __name__ == "__main__":
    main()
