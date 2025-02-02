import sys
from time import time

from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
from pandas import datetime
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
#from sklearn.externals import joblib
import joblib
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
# from keras.callbacks import TensorBoard
from math import sqrt
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot
from numpy import array

import numpy as np
import tensorflow.keras as ks
import pandas as pd

import logging


def forecast_lstm(model, X):
        X = X.reshape(1, 1, len(X))
        forecast = model.predict(X, batch_size=1)
        # return an array
        return [x for x in forecast[0, :]]

def inverse_difference(last_ob, forecast):
    inverted = list()
    inverted.append(forecast[0] + last_ob)
    for i in range(1, len(forecast)):
        inverted.append(forecast[i] + inverted[i-1])
    return inverted

def inverse_transform(scaler, forecast, current_load):
    forecast = array(forecast)
    forecast = forecast.reshape(1, len(forecast))
    # invert scaling
    inv_scale = scaler.inverse_transform(forecast)
    inv_scale = inv_scale[0, :]
    inv_diff = inverse_difference(current_load, inv_scale)
    return inv_diff


model = ks.models.load_model(sys.argv[1]+"_my_model_32.h5")
scaler = joblib.load("my_scaler.save")


n_lag = 1 #given 1 current data, forcast the next 3. must be 1 to support online
n_seq = 50
n_test = 1000 #size of test set
n_epochs = 3
n_batch = 1 #must be 1 because we want online prediction
n_neurons = 32

last_step = 3513
current_load = 4263

X = [[(current_load - last_step)]]
last_step = current_load
X=np.asarray(X)
X.reshape(-1, 1)
Y = scaler.transform(X)
forecast = forecast_lstm(model, Y)
forecast_real = inverse_transform(scaler, forecast, current_load)
print(forecast_real)
print(len(forecast_real))
print(sys.argv[1]+"_my_model_32.h5")
print(type(forecast_real))

for index, value in enumerate(forecast_real):
    print(value)
