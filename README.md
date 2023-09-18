# CochlTranscriptor

CochlTranscriptor is Auto transcriptor which make Closed Caption that include Emotional background sounds.

## 🦾 The Flow of CochlTranscriptor

![2nd flow of Transcriptor](https://github.com/jwyeeh-dev/CochlTranscriptor/assets/99489807/2bbe6ac0-eb6d-4b0f-acaf-c8168ffb6921)


## ⚙️ Setup

### 1. Create Python 3.8 Environment

`conda create --name cochltranscriptor python=3.8`

`conda activate cochltranscriptor`

### 2. Install this repo

`git clone https://github.com/jwyeeh-dev/CochlTranscriptor.git`

If already installed, update package to most recent commit

`git clone https://github.com/jwyeeh-dev/CochlTranscriptor.git --upgrade`

If wishing to modify this package, clone and install in editable mode:

```
$ git clone https://github.com/jwyeeh-dev/CochlTranscriptor.git
$ cd CochlTranscriptor
$ pip install -e .
```

### 3. Install Pre-requisite

`pip install -r requirements.txt`



## How to Use

```
python CochlTranscriptor/cochl_transcriptor.py -iv [input_path] -o [output_path] -ot [output_type] -it [input_type] -f [font_path]
```
