import sys
import pandas as pd
import json
import os
import re
import sys
import zlib
from typing import Callable, Optional, TextIO
import numpy as np

import tools.processing_tools as pt
import tools.parser_tools as parser_tools
from collections import defaultdict
from cochlsense.CochlSense import cochlSense
from cochlsense.CochlSense import cochlSense
from tools.processing_tools import extract_audio
from tools.processing_tools import transform
from tools.parser_tools import make_parser
from whisperapi.whisper import whisper_result
from PIL import Image, ImageDraw, ImageFont


def smi_generator(filename, transcript = "output.smi"):

    output_path = "dataset/output/" + filename

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

def srt_generator(filename, transcript="output.srt"):
    output_path = "dataset/output/" + filename

    # SRT 파일 생성
    with open(output_path, "w") as f:
        subtitle_number = 1
        for index, (start_time, end_time, text) in enumerate(transcript):
            f.write(f"{subtitle_number}\n")
            f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
            f.write(f"{text}\n\n")
            subtitle_number += 1

def format_time(seconds):
    # 시간을 SRT 형식 (hh:mm:ss,ms)으로 포맷팅
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"


def txt_generator(filename, text_content, output_dir="dataset/output/"):
    output_path = output_dir + filename

    # 텍스트 파일 생성
    with open(output_path, "w") as f:
        f.write(text_content)
