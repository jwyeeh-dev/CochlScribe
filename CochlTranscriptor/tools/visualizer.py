import sys
import argparse
import cv2
import ast 
import pandas as pd
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
from tools.transcriptor_tools import smi_generator, srt_generator, txt_generator
from PIL import Image, ImageDraw, ImageFont


def visualizer(csv_path, whisper_result, args):

    args = make_parser()
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
        else: combined_text = tag_text + "\n" + whisper_sent  # Whisper 결과와 태그 함께 표시
    
        smi_data.append((int(current_time * 1000), combined_text))

        textsize = cv2.getTextSize(tag_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        textX = (frame.shape[1] - textsize[0]) // 2
        textY = frame.shape[0] - 60  # 첫 번째 텍스트의 Y 위치
        cv2.putText(frame, tag_text, (10, textY), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        if whisper_text:
            # OpenCV 이미지를 PIL 이미지로 변환
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(frame_pil)
            
            # 폰트 설정 (폰트 파일의 경로와 크기를 지정)
            font = ImageFont.truetype(args.font, 30)

            textsize = cv2.getTextSize(tag_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            textX = (frame.shape[1] - textsize[0]) // 2
            textY = frame.shape[0] - 50 # 두 번째 텍스트의 Y 위치
            
            draw.text((10, textY), whisper_text, font=font, fill=(255, 255, 255, 0))
            
            frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
    

        # 쓰기 및 출력
        out.write(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_counter += 1  # 프레임 카운터 증가

    # 자원 해제
    cap.release()

    if args.output_type=="smi": smi_generator(smi_data, args.output_path) 
    elif args.output_type=="srt": srt_generator(smi_data, args.output_path)
    else: txt_generator(smi_data, args.output_path)

    out.release()
    cv2.destroyAllWindows()
