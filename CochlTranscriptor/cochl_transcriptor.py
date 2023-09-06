import sys
import argparse
from cochlsense.CochlSense import cochlSense
import tools.processing_tools as pt
import tools.parser_tools as parser_tools
from collections import defaultdict
import cv2
import ast 
import pandas as pd
from cochlsense.CochlSense import cochlSense
from tools.processing_tools import extract_audio
from tools.transcriptor_tools import get_writer
from tools.visualizer import visualizer
from tools.parser_tools import make_parser
from whisperapi.whisper import whisper_result
from tools.transcriptor_tools import SubtitlesWriter


def main():
    args = make_parser()
    
    audio = extract_audio(args.input_path)
    whispers = whisper_result(audio)
    csv_path, json_path = cochlSense(audio)
    with open(json_path, 'w', encoding='utf-8') as json_file:
        cochl = json_file
    SubtitlesWriter.iterate_result(whispers, options, cochl)
    get_writer(args.output_type, args.output_path)    

if __name__ == '__main__':
    main()
  
