import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
import json
import time
from os.path import abspath, dirname, join
from base64 import b64encode, b64decode

import requests

import numpy as np

upper_folder = abspath(dirname(dirname(__file__)))


sender = lambda data: requests.post(
    f'http://{args.host}:{args.port}/predict/{args.name}',
    headers={"Content-type": "application/json"},
    data=json.dumps({ 
        'type':'image',
        'data': data
    })
)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=7001)
    parser.add_argument('--name', type=str, default='mx')
    parser.add_argument('--timeout', type=int, default=490)
    parser.add_argument('--burst', type=float, default=0.5)
    return parser.parse_args()

def get_data():
    with open(f'{upper_folder}/resources/test.jpg', 'rb') as f:
        raw_data = f.read()
        base64_bytes = b64encode(raw_data)
        base64_string = base64_bytes.decode('utf-8')
        return base64_string

def send_data(args, reader):
    pool = ThreadPoolExecutor(5000)
    data = ""
    #get_data()

    for row in reader:
        if reader.line_num > args.timeout:
            break

        num = int(int(row['tweets']) * 1.8)
        num1 = int(row['tweets'])
        print(f'row[tweets] : {num1}')
        print(f'num : {num}')
        lam = (60 * 1000.0) / num
        samples = np.random.poisson(lam, num)
        print(f'line: {reader.line_num}; sample_number: {num}')
        for s in samples:
            pool.submit(sender, data)
            # sender(data)
            # print(f'Send request after {s} ms')
            time.sleep(s/1000.0)

with open(f'./tweet_load.csv', 'r') as f:
    args = get_args()
    reader = csv.DictReader(f)
    send_data(args, reader)
