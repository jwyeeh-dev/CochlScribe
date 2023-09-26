# CochlScribe

CochlTranscriptor is Auto transcriptor which make Closed Caption that include Emotional background sounds.

## 🦾 The Flow of CochlScribe

![2nd flow of Transcriptor](https://github.com/jwyeeh-dev/CochlScribe/assets/99489807/bea6fe03-787d-4ed9-a259-451766d57217)



## ⚙️ Setup

### 1. Create Python 3.8 Environment

`conda create --name cochlscribe python=3.8`

`conda activate cochlscribe`

### 2. Install this repo

`git clone https://github.com/jwyeeh-dev/CochlScribe.git`

If already installed, update package to most recent commit

`git clone https://github.com/jwyeeh-dev/CochlScribe.git --upgrade`

If wishing to modify this package, clone and install in editable mode:

```
$ git clone https://github.com/jwyeeh-dev/CochlScribe.git
$ cd CochlScribe
$ pip install -e .
```

### 3. Install Pre-requisite

`pip install -r requirements.txt`



## How to Use

```
python cochlscribe.py -iv [input_path] -o [output_path] -ot [output_type] -it [input_type] -f [font_path]
```
