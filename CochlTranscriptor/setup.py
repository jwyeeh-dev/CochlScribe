import os

import pkg_resources
from setuptools import setup, find_packages

setup(
    name="CochlTranscriptor",
    py_modules=["CochlTranscriptor"],
    version="1.0.0",
    description="Time Accurate Transcriptor using Cochl.Sense and ASR(Whisper)",
    readme="README.md",
    python_requires=">=3.8",
    author="Jaeyeong Hwang",
    url="https://github.com/jwyeeh-dev",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ] + ["pyannote.audio @ git+https://github.com/pyannote/pyannote-audio@11b56a137a578db9335efc00298f6ec1932e6317"],
    entry_points = {
        'console_scripts': ['cochltranscriptor=CochlTranscriptor.cochl_transcriptor:main'],
    },
    include_package_data=True,
    extras_require={'dev': ['pytest']},
)
