from speechbrain.pretrained.interfaces import foreign_class
from speechbrain.pretrained.interfaces import Speech_Emotion_Diarization

def speechMood(audio):
    classifier = Speech_Emotion_Diarization.from_hparams(
        source="speechbrain/emotion-diarization-wavlm-large"
    )

    diary = classifier.diarize_file(audio)
    
    return diary