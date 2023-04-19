#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 15:46:56 2020

@author: sleek_eagle
"""
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


from pydub import AudioSegment
from pydub.generators import WhiteNoise

# original_filepath = "../Drake - Know Yourself.mp3"
# original_sound = AudioSegment.from_file(original_filepath)
# original_loudness = original_sound.dBFS
#
# print("original_loudness = ", original_loudness)

# Adding real world crowd noise to signal
# talking_filepath = "../crowd_talking.wav"
# talking_sound = AudioSegment.from_file(talking_filepath)
# talking_loudness = talking_sound.dBFS
#
# print("talking_loudness = ", talking_loudness)
#
#
# combined = original_sound.overlay(talking_sound, loop=True)
# combined.export("../Drake - Know Yourself - With Crowd.mp3", format="mp3")

# Adding gaussian white noise to signal
# noise = WhiteNoise().to_audio_segment(duration=len(original_sound)) - 20
# combined = original_sound.overlay(noise)
# combined.export("../Drake - Know Yourself - With Gaussian White Noise.mp3", format="mp3")
#
# noise_loudness = noise.dBFS
# print("noise_loudness = ", noise_loudness)

src_dir = "../trimed_songs/"
dest_dir = "../noised_songs/"

for filename in tqdm(os.listdir(src_dir)):
    if filename.endswith(".mp3"):
        original_filepath = os.path.join(src_dir, filename)
        original_sound = AudioSegment.from_file(original_filepath)
        original_loudness = original_sound.dBFS

        print("original_loudness = ", original_loudness)

        # # Adding real world crowd noise to signal
        # talking_filepath = "../crowd_talking.wav"
        # talking_sound = AudioSegment.from_file(talking_filepath)
        # talking_loudness = talking_sound.dBFS
        #
        # print("talking_loudness = ", talking_loudness)
        # combined = original_sound.overlay(talking_sound, loop=True)

        # Adding gaussian white noise to signal
        noise = WhiteNoise().to_audio_segment(duration=len(original_sound)) - 10
        combined = original_sound.overlay(noise)

        noise_loudness = noise.dBFS
        print("noise_loudness = ", noise_loudness)

        combined.export(dest_dir + filename , format="mp3")
