# CochlTranscriptor


### ⚙️ Setup 
---
```
pip install -U requirements.txt
```



### 💬 Usage 
---
#### cochl_transcriptor.py
```
python CochlTranscriptor/cochl_transcriptor.py -iv [input_path] -o [output_path] -ot [output_type] -it [input_type] -f [font_path]
```

#### youtube_tools.py
```
python CochlTranscriptor/tools/youtube_tools.py -url [url]
```



### 🏛️ Structure of Modules
---

```
CochlTranscriptor
├── CochlSenseAPI
│   ├── CochlSense.py
├── README.md
├── WhisperAPI
│   ├── whisper.py
│   └── whisper_tools.py
├── api_key.json
├── cochl_transcriptor.py
├── default_path.yaml
├── fonts
│   └── NanumGothic.ttf
├── requirements.txt
├── setup.py
├── tools
│   ├── get_playlists_data.py
│   ├── parser_tools.py
│   ├── processing_tools.py
│   ├── transcriptor_tools.py
│   └── youtube_tools.py
└── whisperx
    ├── __init__.py
    ├── __main__.py
    ├── alignment.py
    ├── asr.py
    ├── assets
    │   └── mel_filters.npz
    ├── audio.py
    ├── diarize.py
    ├── transcribe.py
    ├── types.py
    ├── utils.py
    └── vad.py
```