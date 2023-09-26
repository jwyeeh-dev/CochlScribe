import sys
import json
import re
import sys
import zlib
from typing import Callable, Optional, TextIO
import numpy as np
import pandas as pd
import cv2
import os

import tools.utils as pt
import tools.cli as cli
from collections import defaultdict
from models.CochlSense.load import cochlSense
from tools.utils import extract_audio, extract_audio_segment, transform, trim_audio
from tools.cli import cli
from models.whispers.load import whisper_result
from PIL import Image, ImageDraw, ImageFont
from models.CochlMood.load import predict_sound_mood



def smi_generator(filename, transcript, output_dir="dataset/output/"):
    output_path = output_dir + filename

    # SMI 파일 생성
    with open(output_path, "w") as f:
        f.write("<SAMI>\n")
        f.write("<HEAD>\n")
        f.write("<Title>Sample SMI file</Title>\n")
        f.write("</HEAD>\n")
        f.write("<BODY>\n")
        for time, text in transcript:
            f.write(f"<SYNC Start={time}>\n")
            f.write(f"<P Class=KRCC>{text}</P>\n")
            f.write("</SYNC>\n")
        f.write("</BODY>\n")
        f.write("</SAMI>\n")

def srt_generator(filename, transcript, output_dir="dataset/output/"):
    output_path = output_dir + filename

    # SRT 파일 생성
    with open(output_path, "w") as f:
        subtitle_number = 1
        for (start_time, end_time), text in enumerate(transcript):
            f.write(f"{subtitle_number}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{text}\n\n")
            subtitle_number += 1


def txt_generator(filename, text_content, output_dir="dataset/output/"):
    output_path = output_dir + filename

    # 텍스트 파일 생성
    with open(output_path, "w") as f:
        f.write(text_content)


def emotion_to_text(emotion):
    """Convert emotion code to text description."""
    emotion_mapping = {
        'h': 'happy',
        'n': 'neutral',
        'a': 'angry',
        's': 'sad'
    }
    return emotion_mapping.get(emotion, 'unknown')

def SubtitlesWriter(audio, tags_df, whispers, speechbrain_results, args):
    # 자막 저장을 위한 리스트 초기화
    subtitles = []

    # 태그 및 whispers 처리
    for index, row in tags_df.iterrows():
        start_time = row['start_time']
        end_time = row['end_time']
        tag_name = row['name']

        sound_mood = ''
        if "Music" in tag_name or "Instrument" in tag_name:
            # 해당 구간의 오디오를 임시 파일로 추출
            temp_audio_file = "temp_audio_segment.wav"
            extract_audio_segment(audio, start_time, end_time, temp_audio_file)
            sound_mood = predict_sound_mood(temp_audio_file) + ' | '
            os.remove(temp_audio_file)

        whisper_text = ''
        for segment in whispers['segments']:
            if segment['start'] <= start_time and segment['end'] >= end_time:
                whisper_text = segment['text']
                break

        speech_text = ''
        if 'Speech' in tag_name:
            for result in speechbrain_results.get(audio, []):
                if result['start'] <= start_time and result['end'] >= end_time:
                    speech_text = emotion_to_text(result['emotion'])
                    break

        subtitle_text = f"[ {sound_mood} {tag_name} {speech_text} ] <br> {whisper_text}"
        subtitles.append((int(start_time * 1000), int(end_time * 1000), subtitle_text))

    # 출력 유형에 따라 자막 파일 생성
    if args.output_type == "all":
        smi_generator(args.output_path, subtitles)
        srt_generator(args.output_path, subtitles)
        txt_generator(args.output_path, subtitles)
    elif args.output_type == "smi":
        smi_generator(args.output_path, subtitles)
    elif args.output_type == "srt":
        srt_generator(args.output_path, subtitles)
    elif args.output_type == "txt":
        txt_generator(args.output_path, subtitles)
    else:
        print("Do not support this type of output file.")

    return subtitles



    
def format_time(seconds):
        # 시간을 SRT 형식 (hh:mm:ss,ms)으로 포맷팅
        hours = int(seconds // 3600)
        seconds %= 3600
        minutes = int(seconds // 60)
        seconds %= 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"