import tensorflow as tf
import numpy as np
import pandas as pd
from tools.utils import extract_audio
import librosa

def features_extractor(file_name):
    audio = extract_audio(file_name)
    y, sr = librosa.load(file_name, sr=None)
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram, ref=np.max)
    input_data = log_mel_spectrogram.T[np.newaxis, :, :, np.newaxis]
    return input_data

def predict_sound_mood(file_name, mood_label_path = "./models/CochlMood/music_mood.tsv"):
    input_data = features_extractor(file_name)
    model = tf.keras.models.load_model('./models/CochlMood/model_main.h5', compile=False)
    mood_label = pd.read_csv(mood_label_path, delimiter='\t')
    result = model.predict(input_data)
    predicted_mood = mood_label['name'][result[0].argmax()]
    return predicted_mood
