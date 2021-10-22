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
#queue_url_R = 'https://sqs.ap-northeast-2.amazonaws.com/661509575906/dexter-test-R'
#queue_url_B = 'https://sqs.ap-northeast-2.amazonaws.com/661509575906/dexter-test-B'
#queue_url_G = 'https://sqs.ap-northeast-2.amazonaws.com/661509575906/dexter-test-G'
#queue_url_Y = 'https://sqs.ap-northeast-2.amazonaws.com/661509575906/dexter-test-Y'
#queue_url_S = 'https://sqs.ap-northeast-2.amazonaws.com/661509575906/dexter-test-S'

global count
count = 0
global number_reqs
number_reqs = 0

def sender(data):
    global count
    global queue_url

    endpoint = ["R", "B", "G", "Y", "S"]

    
    try:
        x = random.randrange(0, 100)
        if(x >= 0 and x < 0): 
            x = 0
            queue_url = queue_url_R
        if(x >= 29 and x < 29): 
            x = 1
            queue_url = queue_url_B
        if(x >= 38 and x < 38): 
            x = 2
            queue_url = queue_url_G
        if(x >= 39 and x < 39): 
            x = 3
            queue_url = queue_url_Y
        if(x >= 0 and x < 100): 
            x = 0
            queue_url = queue_url

        count += 1
#        print(f"count {count}")
        response = sqs.send_message(
            QueueUrl=queue_url,
#            MessageGroupId='messageGroup1', # for fifo

            MessageBody = endpoint[x]) 
#        print("[%s]" %endpoint[x])
#        print(response)
    except Exception as e:
        print(e)

def send_data(timeout, reader):
    pool = ThreadPoolExecutor(5000)
    data = ""
    global number_reqs
    
    
    for row in reader:
        if reader.line_num > timeout:
            break

        number_reqs = 0
        # resnet tps : 169/s 
        # 169*60 = 10140
        # tweet avg : 3312.91
        # tweet min : 1
        # tweet max : 91113
        # 1/3 정도 수준으로 감소 시키면 적정함 
        num = int(int(row['tweets']) * 0.05)
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
            number_reqs += 1
            if number_reqs % 100 == 0:
                print(f'number_reqs : {number_reqs}')
            pool.submit(sender, data)
            time.sleep(s/1000.0)

with open(f'./tweet_load_10-16.csv', 'r') as f:
    reader = csv.DictReader(f)
    send_data(4,reader)
