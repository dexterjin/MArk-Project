import os
import sys
import click
import concurrent.futures
import requests
import imageio
import json
import time
import itertools
import cv2
import numpy as np
import random
import sys
import boto3, json
from botocore.exceptions import ClientError


# Get the service resource
sqs = boto3.client('sqs')
#queue_url = 'https://sqs.us-east-1.amazonaws.com/392434356039/test.fifo'
queue_url = 'https://sqs.us-east-1.amazonaws.com/392434356039/test'
queue_url_R = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_R'
queue_url_B = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_B'
queue_url_G = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_G'
queue_url_Y = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_Y'
queue_url_S = 'https://sqs.us-east-1.amazonaws.com/392434356039/alg3_S'


from validator_collection import checkers

global count
count = 0


@click.command(help="Program for testing the throughput of Cortex-deployed APIs.")
@click.argument("endpoint1", type=str, envvar="ENDPOINT1")
@click.argument("endpoint2", type=str, envvar="ENDPOINT2")
@click.argument("endpoint3", type=str, envvar="ENDPOINT3")
@click.argument("payload", type=str, envvar="PAYLOAD")

@click.option(
    "--processes",
    "-p",
    type=int,
    default=1,
    show_default=True,
    help="Number of processes for prediction requests.",
)

@click.option(
    "--threads",
    "-t",
    type=int,
    default=1,
    show_default=True,
    help="Number of threads per process for prediction requests.",
)

@click.option(
    "--samples",
    "-s",
    type=int,
    default=10,
    show_default=True,
    help="Number of samples to run per thread.",
)

@click.option(
    "--time-based",
    "-i",
    type=float,
    default=0.0,
    help="How long the thread making predictions will run for in seconds. If set, -s option will be ignored.",
)



def main(payload, endpoint1, endpoint2, endpoint3, processes, threads, samples, time_based):
#    print(f"'{payload}' is")

    file_type = None
    if checkers.is_url(payload):
        if payload.lower().endswith(".json"):
            file_type = "json"
            payload_data = requests.get(payload).json()
        elif payload.lower().endswith(".jpg"):
            file_type = "jpg"
            payload_data = imageio.imread(payload)
    elif checkers.is_file(payload):
        if payload.lower().endswith(".json"):
            file_type = "json"
            with open(payload, "r") as f:
                payload_data = json.load(f)
        elif payload.lower().endswith(".jpg"):
            file_type = "jpg"
            payload_data = cv2.imread(payload, cv2.IMREAD_COLOR)
    else:
        print(f"'{payload}' isn't an URL resource, nor is it a local file")
        sys.exit(1)

    if file_type is None:
        print(f"'{payload}' doesn't point to a jpg image or to a json file")
        sys.exit(1)

    if file_type == "jpg":
        data = image_to_jpeg_bytes(payload_data)
    if file_type == "json":
        data = json.dumps(payload_data)

#    print(f"'{data}' is")
#    print(f"'{file_type}' is")
    #processes = (int)(processes/3)
    #threads = (int)(threads/3)
    #endpoint = [endpoint1, endpoint2, endpoint3]
    endpoint = ["R", "B", "G", "Y", "S"]
 #   print(f"endpoint : {endpoint}")
 #   print(f"random : {endpoint[random.randrange(0,3)]}")
    print("Starting the inference throughput test...")
    results = []
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=processes) as executor:
        results += executor_submitter(
            executor, processes, process_worker, threads, data, endpoint, samples, time_based)

    end = time.time()
    elapsed = end - start
    total_requests = sum(results)

    print(f"A total of {total_requests} requests have been served in {elapsed} seconds")
    print(f"Avg number of inferences/sec is {total_requests / elapsed}")
    print(f"Avg time spent on an inference is {elapsed / total_requests} seconds")

def process_worker(threads, data, endpoint, samples, time_based):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor_submitter(executor, threads, task, data, endpoint, samples, time_based)
    return results

def executor_submitter(executor, workers, *args, **kwargs):
    futures = []
    for worker in range(workers):
        future = executor.submit(*args, **kwargs)
        futures.append(future)
    results = [future.result() for future in futures]
    results = list(itertools.chain.from_iterable(results))
    return results





def task(data, endpoint, samples, time_based):
    global count
    timeout = 60

    if isinstance(data, str):
        headers = {"content-type": "application/json"}
    elif isinstance(data, bytes):
        headers = {"content-type": "application/octet-stream"}
    else:
        return

    

    #print(f"count {count}")

    if time_based == 0.0:
        for i in range(samples):
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
                break
            time.sleep(0.1)
        return [samples]
    else:
        start = time.time()
        counter = 0
        while start + time_based >= time.time():
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
         #           MessageGroupId='messageGroup1', # for fifo
                    MessageBody = endpoint[x]) 
                print("[%s]" %endpoint[x])
                print(response)
            except Exception as e:
                print(e)
                break

    #        print(f"req : {requests}")
            #print(f"resp : {resp}")
            time.sleep(0.1)
            counter += 1
        return [counter]



def image_to_jpeg_nparray(image, quality=[int(cv2.IMWRITE_JPEG_QUALITY), 95]):
    """
    Convert numpy image to jpeg numpy vector.
    """
    is_success, im_buf_arr = cv2.imencode(".jpg", image, quality)
    return im_buf_arr


def image_to_jpeg_bytes(image, quality=[int(cv2.IMWRITE_JPEG_QUALITY), 95]):
    """
    Convert numpy image to bytes-encoded jpeg image.
    """
    buf = image_to_jpeg_nparray(image, quality)
    byte_im = buf.tobytes()
    return byte_im


if __name__ == "__main__":
    main()
