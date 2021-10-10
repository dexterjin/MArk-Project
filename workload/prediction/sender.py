import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import json
import time
from os.path import abspath, dirname, join
from base64 import b64encode, b64decode
import random
import requests
import boto3, json


import numpy as np

# Get the service resource
sqs = boto3.client('sqs')

queue_url = 'https://sqs.us-east-1.amazonaws.com/392434356039/test'
queue_url_R = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_R'
queue_url_B = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_B'
queue_url_G = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_G'
queue_url_Y = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_Y'
queue_url_S = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_S'

global count
count = 0


def sender():
    global count

    endpoint = ["R", "B", "G", "Y", "S"]

    
    try:
        x = random.randrange(0, 100)
        if(x >= 0 and x < 29): 
            x = 0
            queue_url = queue_url_R
        if(x >= 29 and x < 38): 
            x = 1
            queue_url = queue_url_B
        if(x >= 38 and x < 39): 
            x = 2
            queue_url = queue_url_G
        if(x >= 39 and x < 98): 
            x = 3
            queue_url = queue_url_Y
        if(x >= 98 and x < 100): 
            x = 4
            queue_url = queue_url_S

        count += 1
        #print(f"count {count}")
        response = sqs.send_message(
            QueueUrl=queue_url,
#            MessageGroupId='messageGroup1', # for fifo

            MessageBody = endpoint[x]) 
        print("[%s]" %endpoint[x])
        print(response)
    except Exception as e:
        print(e)

def send_data(timeout, reader):
    pool = ThreadPoolExecutor(5000)
    data = ""
    
    for row in reader:
        if reader.line_num > timeout:
            break

        num = int(int(row['tweets']) * 1.8)
        num1 = int(row['tweets'])
        print(f'row[tweets] : {num1}')
        print(f'num : {num}')
        lam = (60 * 1000.0) / num
        samples = np.random.poisson(lam, num)
        print(f'line: {reader.line_num}; sample_number: {num}')
        print(f'lam : {lam}')
        print(f'samples : {samples}')
        print(len(samples))
        for s in samples:
            pool.submit(sender, data)
            time.sleep(s/1000.0)

with open(f'./tweet_load.csv', 'r') as f:
    reader = csv.DictReader(f)
    send_data(reader)
