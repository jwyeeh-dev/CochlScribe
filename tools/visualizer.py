import sys
import argparse
import cv2
import ast 
import pandas as pd
import numpy as np

import tools.utils as pt
import tools.cli as cli
from collections import defaultdict
from cochlsense.CochlSense import cochlSense
from cochlsense.CochlSense import cochlSense
from tools.utils import extract_audio
from tools.utils import transform
from tools.cli import cli
from whisper.load import whisper_result
from tools.transcript import smi_generator, srt_generator, txt_generator
from PIL import Image, ImageDraw, ImageFont


class SubtitlesWriter:

    def __init__(self, csv_path, whisper_result, args):
        self.csv_path = csv_path
        self.whisper_result = whisper_result
        self.args = args

    def visualizer():
        return

    def subtitleWriter(self, csv_path, whisper_result, args):

        args = cli()
        transformed_df = transform(csv_path)
        interval_tags = defaultdict(list)

        for i in range(transformed_df.shape[0]):
            start_time = transformed_df['start_time'][i]
            end_time = transformed_df['end_time'][i]
            tag_name = transformed_df['name'][i]
            interval_tags[(start_time, end_time)].append(tag_name)

        # Whisper 결과
        result = whisper_result  # `whisper_result`는 실제 Whisper API로부터 받은 결과
        smi_data = []

        cap = cv2.VideoCapture(args.input_path)

        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v') if args.input_type == 'mp4' else \
                    cv2.VideoWriter_fourcc(*'dvix') if args.input_type == 'avi' else \
                    cv2.VideoWriter_fourcc(*'hevc')

        out = cv2.VideoWriter(args.output_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

        # 비디오 처리 부분
        frame_counter = 0  # 현재 프레임 번호

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            current_time = frame_counter / fps
            tag_names = set()
            whisper_text = None  # 초기값을 None으로 설정
            
            for (start_time, end_time), names in interval_tags.items():
                if start_time <= current_time <= end_time:
                    tag_names.update(names)
            
            # exception about non-expected values
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

            # 특정 태그에 대한 자막 생성
            if any(tag in ["cough", "laughter", "sigh", "throat clear", "knock"] for tag in tag_names):
                if whisper_text: combined_text = whisper_text  # Whisper 결과 텍스트 사용
                else: combined_text = tag_text  # 특정 태그만 표시
            else: combined_text = tag_text + "\n" + whisper_text  # Whisper 결과와 태그 함께 표시
        
            smi_data.append((int(current_time * 1000), combined_text))

            if args.visualize: SubtitlesWriter.visualizer()
            if not args.visualize: continue

            # 쓰기 및 출력
            out.write(frame)

            frame_counter += 1  # 프레임 카운터 증가

        # 자원 해제
        cap.release()

        if args.output_type=="smi": smi_generator(smi_data, args.output_path) 
        elif args.output_type=="srt": srt_generator(smi_data, args.output_path)
        else: txt_generator(smi_data, args.output_path)

        out.release()
        cv2.destroyAllWindows()

