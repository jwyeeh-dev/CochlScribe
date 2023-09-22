import sys
import argparse
import tools.utils as pt
import tools.cli as cli
import cv2
import ast 
import pandas as pd

from collections import defaultdict
from models.CochlSense.load import cochlSense
from models.CochlSense.load import cochlSense
from tools.utils import extract_audio
from tools.transcript import get_writer
from tools.visualizer import visualizer
from tools.cli import cli
from models.whisperx.load import whisper_result
from tools.transcript import SubtitlesWriter


def main():
    args = cli()
    audio = extract_audio(args.input_path)
    whispers = whisper_result(audio)
    csv_path, json_path = cochlSense(audio)
    visualizer(csv_path, whispers, args)  

if __name__ == '__main__':
    main()
  
