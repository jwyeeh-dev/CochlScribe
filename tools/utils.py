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
import pandas as pd
import ast

import cochl_sense_api as sense
import cochl_sense_api.api.audio_session_api as sense_api
from cochl_sense_api.model.audio_chunk import AudioChunk
from cochl_sense_api.model.audio_type import AudioType
from cochl_sense_api.model.create_session import CreateSession      


def split_audio(file_path, segment_length_ms, output_folder):
    """
    file_path: 오디오 파일의 경로 (예: "sample.mp3")
    segment_length_ms: 나눌 각 부분의 길이 (밀리초 단위)
    output_folder: 출력할 폴더의 경로
    """
    
    audio = pydub.AudioSegment.from_file(file_path, format="mp3")
    total_length = len(audio)
    
    for i in range(0, total_length, segment_length_ms):
        segment = audio[i:i+segment_length_ms]
        segment.export(f"{output_folder}/segment_{i//segment_length_ms}.mp3", format="mp3")
        print(f"Saved: segment_{i//segment_length_ms}.mp3")
    
    print("All segments saved!")


def mp3towav(mp3_path, wav_path):
    """
    mp3_path : 입력 오디오 파일의 경로
    wav_path : 출력 오디오 파일의 경로
    """
    sound = pydub.AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")


def get_duration(audio_path):
    
    audio = wave.open(audio_path)
    frames = audio.getnframes()
    rate = audio.getframerate()
    duration = frames / float(rate)
    return duration



def extract_audio(input_file, output_file = 'test.mp3'):
    
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-vn',
        output_file
    ]
    subprocess.call(cmd)

    return output_file

def extract_audio_segment(input_video, start_time, end_time, output_file = 'temp_audio_segment.wav'):
    command = [
        'ffmpeg', '-i', input_video, '-q:a', '0', '-map', 'a',
        '-ss', str(start_time), '-to', str(end_time), output_file
    ]
    subprocess.run(command)
    return output_file



def trim_video(input_file, start, end, output_file = 'output.mp4'):

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-ss', start,
        '-to', end,
        '-c copy', output_file
    ]
    subprocess.call(cmd)
    
    return output_file

def trim_audio(input_file, start, end, output_file = 'output.mp3'): 
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-ss', start,
        '-to', end,
        '-c copy', output_file
    ]
    subprocess.call(cmd)
    
    return output_file

def transform(csv_path):

    results = pd.read_csv(csv_path)

    transformed_data = []
    
    for idx, row in results.iterrows():
        tags = ast.literal_eval(row['tags'])
        for tag in tags:
            transformed_data.append({
                'probability': tag['probability'],
                'name': tag['name'],
                'start_time': row['start_time'],
                'end_time': row['end_time']
            })

    transformed_df = pd.DataFrame(transformed_data)
    transformed_df['name_code'] = transformed_df['name'].astype('category').cat.codes

    return transformed_df