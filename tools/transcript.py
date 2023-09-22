import sys
import json
import re
import sys
import zlib
from typing import Callable, Optional, TextIO
import numpy as np
import pandas as pd
import cv2

import tools.utils as pt
import tools.cli as cli
from collections import defaultdict
from models.CochlSense.load import cochlSense
from tools.utils import extract_audio
from tools.utils import transform
from tools.cli import make_parser
from models.whisperx.load import whisper_result
from PIL import Image, ImageDraw, ImageFont


class OutputWriter():
    def smi_generator(self, filename, transcript, output_dir="dataset/output/"):
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

    def srt_generator(self, filename, transcript, output_dir="dataset/output/"):
        output_path = output_dir + filename

        # SRT 파일 생성
        with open(output_path, "w") as f:
            subtitle_number = 1
            for index, (start_time, end_time, text) in enumerate(transcript):
                f.write(f"{subtitle_number}\n")
                f.write(f"{format_time(start_time)} --> {format_time(end_time)}\n")
                f.write(f"{text}\n\n")
                subtitle_number += 1


    def txt_generator(self, filename, text_content, output_dir="dataset/output/"):
        output_path = output_dir + filename

        # 텍스트 파일 생성
        with open(output_path, "w") as f:
            f.write(text_content)


    def SubtitlesWriter(self, transformed_df, result, args):
        interval_tags = defaultdict(list)
        for i in range(transformed_df.shape[0]):
            start_time = transformed_df['start_time'][i]
            end_time = transformed_df['end_time'][i]
            tag_name = transformed_df['name'][i]
            interval_tags[(start_time, end_time)].append(tag_name)
        
        subtitles = []
        cap = cv2.VideoCapture(args.input_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_counter = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            current_time = frame_counter / fps
            tag_names = set()
            whisper_text = None
            
            for (start_time, end_time), names in interval_tags.items():
                if start_time <= current_time <= end_time:
                    tag_names.update(names)

            for segment in result['segments']:
                whisper_sent = segment['text']
                for word in segment['words']:
                    try:
                        if word["start"] <= current_time <= word["end"]:
                            whisper_text = word["word"]
                    except len(word) == 1:
                        pass

            tag_text = ' | '.join(tag_names)
            tag_text = '[ ' + tag_text + ' ]'

            if any(tag in ["cough", "laughter", "sigh", "throat clear", "knock"] for tag in tag_names):
                if whisper_text: 
                    combined_text = whisper_text
                else: 
                    combined_text = tag_text
            else: 
                combined_text = tag_text + "\n" + (whisper_text if whisper_text else "")
            
            subtitles.append((int(current_time * 1000), combined_text))
            frame_counter += 1
        
        if args.output_type == "smi": self.smi_generator(subtitles, args.output_path)
        elif args.output_type == "srt": self.srt_generator(subtitles, args.output_path)
        elif args.output_type == "txt": self.txt_generator(subtitles, args.output_path)
        else : print("Do not support this type of output file.")

        cap.release()
        return subtitles
    

    
def format_time(seconds):
        # 시간을 SRT 형식 (hh:mm:ss,ms)으로 포맷팅
        hours = int(seconds // 3600)
        seconds %= 3600
        minutes = int(seconds // 60)
        seconds %= 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"