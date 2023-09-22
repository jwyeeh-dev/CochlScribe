import base64
import json
import os
import pydub
import wave
import csv
import librosa
import numpy as np
import soundfile as sf
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import subprocess

import tools.utils as tools
import cochl_sense_api as sense
import cochl_sense_api.api.audio_session_api as sense_api
from cochl_sense_api.model.audio_chunk import AudioChunk
from cochl_sense_api.model.audio_type import AudioType
from cochl_sense_api.model.create_session import CreateSession      

def cochlSense(filename, api_key = './assets/api_key.json'):
    with open(api_key, 'rb') as fr:
        apifile = json.load(fr)

    apikey = apifile['cochl_key']

    
    configuration = sense.Configuration()
    configuration.api_key['API_Key'] = apikey

    client = sense.ApiClient(configuration)
    api = sense_api.AudioSessionApi(client)

    f = open(filename, "rb")
    size = os.stat(filename).st_size

    #create a new audio session
    session = api.create_session(CreateSession(
        content_type="audio/" + os.path.splitext(filename)[1][1:],
        type=AudioType("file"),
        total_size=size,
    ))
    
    results_list = []

    #upload file per 1Mib chunks
    seq = session.chunk_sequence
    while True:
        chunk = f.read(2**20)
        if not chunk:
            break
        encoded = base64.b64encode(chunk).decode("utf-8")

        print("uploading")
        uploaded = api.upload_chunk(session_id=session.session_id, chunk_sequence=seq, audio_chunk=AudioChunk(encoded))
        seq = uploaded.chunk_sequence


    # read inference result
    next_token = ""
    while True:
        resp = api.read_status(session_id=session.session_id, next_token=next_token)
        for result in resp.inference.results:
            result_dict = result.to_dict()
            print(json.dumps(result_dict))
            results_list.append(result_dict)

        if "next_token" in resp.inference.page:
            next_token = resp.inference.page.next_token
        else:
            break

    # list to json file
    json_path = 'dataset/data/result_' + str(filename[:-5]) + '.json'
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(results_list, json_file, ensure_ascii=False, indent=4)

    # list to csv
    keys = results_list[0].keys() 
    csv_path = 'dataset/data/result_' + str(filename[:-4]) + '.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        for row in results_list:
            writer.writerow(row)
        
    return csv_path, json_path