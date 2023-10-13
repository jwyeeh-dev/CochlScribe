from speechbrain.pretrained.interfaces import foreign_class
from speechbrain.pretrained.interfaces import Speech_Emotion_Diarization

def speechMood(audio):
    # If you want to change your extracted audio file, change the audio path below
    audio_path = './dataset/audio/extracted_audio.mp3'

    classifier = Speech_Emotion_Diarization.from_hparams(
        source="speechbrain/emotion-diarization-wavlm-large"
    )

    diary = classifier.diarize_file(audio)
    
    return diary[audio_path]
