import argparse
import os
import random
import warnings
import glob
from collections import OrderedDict
from pathlib import Path

def cli():
    parser = argparse.ArgumentParser("parameters about captioning")

    # Input/Output Parameters
    parser.add_argument("-iv", "--input_path", type=str, default=None)
    parser.add_argument("-o", "--output_path", type=str, default='output.smi')
    parser.add_argument("-ot", "--output_type", type=str, default='smi', choices=['smi', 'srt', 'txt'])
    parser.add_argument("-it", "--input_type", type=str, default='mp4', choices=['mp4', 'mov', 'avi'])
    parser.add_argument("-f", "--font", type=str, default='CochlTranscriptor/fonts/NanumGothic.ttf')

    # whisperX Inference Parameters
    parser.add_argument("-d", "--device", type=str, default='cpu', choices=['cpu', 'cuda', 'mps'])
    parser.add_argument("-c", "--compute_type", type=str, default='int8', choices=['int8', 'float16'])
    parser.add_argument("-b", "--batch_size", type=int, default=16)

    # Subtitle Parameters
    parser.add_argument("-vis", "--visualize", type=bool, default=False)
    parser.add_argument("-h", "--highlight_words", type=bool, default=False)


    return parser.parse_args()




