import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd

def cochlMood(args, model_path = "model_main.h5"):
    model = keras.models.load_model(model_path)
    mood = model.predict(args)
    return mood
