import sys
from time import time

import csv
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

buf = [0]

with open(f'./tweet_load.csv', 'r') as f:
    timeout = 1000000000
    reader = csv.DictReader(f)
   

    for row in reader:
        if reader.line_num > timeout:
            break

        buf.append(int(row['tweets']))
#        print(f'reader.line_num : {reader.line_num}')

        last_step = int(row['tweets'])
        current_load = int(row['tweets'])

#        print(f'last_step : {last_step}')
#        print(f'current_load : {current_load}')

        print(f'buf[{reader.line_num-1}] : {buf[reader.line_num-1]}')


#for index, row in enumerate(buf):
#    print(f'row[{index}] : {row}')


with open(f'./tweet_load.csv', 'r') as fr:
    timeout = 1000000000
    reader = csv.DictReader(fr)

    buf2 = ['']
    with open(f'./tweet_load_predict_1min_predict_52.csv', 'w') as fw:
        fw.write("\"time\",\"tweets_predict\"\n")

    for row in reader:
        if reader.line_num > timeout:
            break

        print(f'reader.line_num : {reader.line_num}')

        with open(f'./tweet_load_predict_1min_predict_52.csv', 'a') as fw:
            if (reader.line_num-2) % 1 == 0:
                buf2 = ['']
#                fw.write("\"" + row['time'] +"\"" + "," + row['tweets'] + ":" + str(buf[reader.line_num-1]) + ":" + str(buf[reader.line_num]) + "\n")
                fw.write("\"" + row['time'] +"\"" + "," + row['tweets'] + "\n")

                last_step = buf[reader.line_num-1]
                current_load = buf[reader.line_num]

                x = [[(current_load - last_step)]]
                last_step = current_load
                x=np.asarray(x)
                x.reshape(-1, 1)
                y = scaler.transform(x)
                forecast = forecast_lstm(model, y)
                forecast_real = inverse_transform(scaler, forecast, current_load)

                for index, value in enumerate(forecast_real):
                    if index > 0:
                        break
                    buf2.append(int(value))
                for val in buf2:
                    print(f'buf2 : {val}')
#                print(f'buf2[3] : {buf2[3]}')

            else:
                fw.write("\"" + row['time'] +"\"" + "," + str(buf2[reader.line_num % 1 -2]) + "\n")

