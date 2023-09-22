import sys
import argparse
import tools.utils as pt
import tools.cli as cli
import cv2
import ast 
import pandas as pd

from collections import defaultdict
from models.CochlSense.load import cochlSense
from tools.utils import extract_audio, transform
from tools.visualize import visualizer
from tools.transcript import subtitlewriter
from tools.cli import cli
from models.whisperx.load import whisper_result


def main():
    args = cli()
    audio = extract_audio(args.input_path)
    
    whispers = whisper_result(audio)
    csv_path, json_path = cochlSense(audio)
    transformed_df = transform(csv_path)
    subtitles = subtitlewriter(transformed_df, whispers, args)

    if args.visualize: visualizer(subtitles, args)
    else: print("No visualization, only transcript") 

if __name__ == '__main__':
    main()
  
