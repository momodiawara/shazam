#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import controllers.tools.recorder as rec
import controllers.tools.audioprocessor as ap
import controllers.tools.database as db
import controllers.tools.fileprocessor as fp
import matplotlib.pyplot as plt
from time import time

import math
from collections import Counter
import numpy as np


def get_cmap(songs_path, filename):
    peaks_list, freqs_filter_list, times_filter_list = [], [], []

    parsed_song = fp.parse_audio(songs_path + filename)

    for channeln, channel in enumerate(parsed_song['channels']):
        t = time()
        spectrogram = ap.get_spectrogram(channel, Fs=parsed_song['Fs'])
        spec_time = time() - t

        t = time()
        peaks, freqs_filter, times_filter = ap.get_peaks(spectrogram)
        peaks_time = time() - t
        name = filename.split(".mp3")[0] + " channel " + str(channeln)
        # plot_spectrogram(spectrogram, freqs_filter, times_filter, name=filename.split(".mp3")[0] + " : channel " + str(channeln))
        ap.plot_spectrogram_peaks(spectrogram, freqs_filter, times_filter, name=name)
        print("Spectrogram len = ", spectrogram.shape)
        print("Peaks len = ", len(peaks))
        print("spec_time = ", spec_time)
        print("peaks_time = ", peaks_time)

        peaks_list.append(peaks)
        freqs_filter_list.append(freqs_filter)
        times_filter_list.append(times_filter)

    return peaks_list, freqs_filter_list, times_filter_list

def plot_spectrogram(spectrogram, freqs_filter, times_filter, name=""):

    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.title("Spectrogram of " + name)
    plt.imshow(spectrogram, cmap="afmhot")
    # plt.colorbar()
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

#--------------- Fingerprint Example ---------------#
songs_path = "../"
original_filename = "Drake - Know Yourself.mp3"

original_peaks, original_freqs, original_times = get_cmap(songs_path, original_filename)

c1 = Counter(original_peaks[0])
c2 = Counter(original_peaks[1])

channels_similitude = counter_cosine_similarity(c1, c2)
print("channels_similitude = ", channels_similitude)

# fig, ax = plt.subplots()
# fig.set_size_inches(13, 7)
#
# ax.scatter(original_times, original_freqs, s=100, color="black")
# ax.scatter(crowd_times, crowd_freqs, s=25, color="green", marker='o')
#
# ax.set_xlabel('Time')
# ax.set_ylabel('Frequency')
# ax.set_title("Constellation map of Drake - Know Yourself")
# # plt.gca().invert_yaxis()
# plt.legend(['Original', 'GWN'], loc='upper right', framealpha=1)
#
# plt.tight_layout()
# plt.show()


# n, k = np.argwhere(crowd_cmap == 1).T
# ax.scatter(k, n, color='cyan', s=20, marker='o')
