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
    with open(f'./tweet_load_predict_5min.csv', 'w') as fw:
        fw.write("\"time\",\"tweets_predict\"\n")

    for row in reader:
        if reader.line_num > timeout:
            break

        print(f'reader.line_num : {reader.line_num}')

        with open(f'./tweet_load_predict_5min.csv', 'a') as fw:
            if (reader.line_num-2) % 5 == 0:
                buf2 = ['']
#                fw.write("\"" + row['time'] +"\"" + "," + row['tweets'] + ":" + str(buf[reader.line_num-1]) + ":" + str(buf[reader.line_num]) + "\n")
                fw.write("\"" + row['time'] +"\"" + "," + row['tweets'] + "\n")

                y = scaler.transform(x)
                forecast = forecast_lstm(model, y)
                forecast_real = inverse_transform(scaler, forecast, current_load)

                for index, value in enumerate(forecast_real):
                    if index > 4:
                        break
                    buf2.append(int(value))
                for val in buf2:
                    print(f'buf2 : {val}')
                print(f'buf2[3] : {buf2[3]}')

            else:
                fw.write("\"" + row['time'] +"\"" + "," + str(buf2[reader.line_num % 5 -2]) + "\n")

