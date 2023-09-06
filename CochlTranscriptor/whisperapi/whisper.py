import whisper
import json
import whisperx
from CochlTranscriptor.tools.parser_tools import make_parser

def whisper_result(audio_path, language = 'ko', api_keys = 'CochlTranscriptor/api_key.json'):
    args = make_parser()
    global result

    # Get the huggingface user token
    with open(api_keys, 'rb') as fr:
        apifile = json.load(fr)
    my_token = apifile['hf_token'] 

    # whisper inference options
    options = dict(language=language, beam_size=5, best_of=5)
    transcribe_options = dict(task="transcribe", **options)
    
    # whisper reference model inference
    model = whisperx.load_model("large-v2", device=args.device, compute_type=args.compute_type)
    audio = whisperx.load_audio(audio_path)


    # Align whisper output
    result = model.transcribe(audio, batch_size=args.batch_size)
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=args.device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device=args.device, return_char_alignments=False)

    '''
    # Assign speaker labels
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=my_token, device=args.device)
    # add min/max number of speakers if known
    diarize_segments = diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    '''

    return result

