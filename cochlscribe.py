import sys
import argparse
import tools.utils as pt
import tools.cli as cli
import cv2
import ast 
import pandas as pd

from collections import defaultdict
from models.CochlSense.load import cochlSense
from models.whispers.load import whisper_result
from models.CochlMood.load import predict_sound_mood
from models.SpeechBrain.load import speechMood

from tools.utils import extract_audio, transform, trim_audio
from tools.visualize import visualizer
from tools.transcript import SubtitlesWriter
from tools.cli import cli


def main():
    args = cli()
    audio = extract_audio(args.input_path)
    
    whispers = whisper_result(audio)
    speechbrain = speechMood(audio)
    csv_path, _ = cochlSense(audio)
    transformed_df = transform(csv_path)

    subtitles = SubtitlesWriter(audio, transformed_df, whispers, speechbrain, args)

    if args.visualize: visualizer(subtitles, args)
    else: print("No visualization, only transcript") 

if __name__ == '__main__':
    main()
  
