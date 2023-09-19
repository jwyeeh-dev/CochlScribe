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
from tools.parser_tools import cli
from whisperapi.whisper import whisper_result
from tools.transcriptor_tools import SubtitlesWriter


def main():
    args = cli()
    audio = extract_audio(args.input_path)
    whispers = whisper_result(audio)
    csv_path, json_path = cochlSense(audio)
    visualizer(csv_path, whispers, args)  

if __name__ == '__main__':
    main()
  
