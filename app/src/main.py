import controllers.tools.recorder as rec
import controllers.tools.audioprocessor as ap
import controllers.tools.database as db
import controllers.tools.fileprocessor as fp
import matplotlib.pyplot as plt
from time import time

import math
from collections import Counter
import numpy as np
# music_db = db.MySQLdb()
# music_db.free()
# music_db.close()

#--------------- Recording Example ---------------#
# recorder = rec.Recorder()
# frames, data = recorder.record(RECORD_SECONDS=10)
#
# for channeln, channel in enumerate(data):
#     spectrogram = ap.get_spectrogram(channel)
#     peaks, freqs_filter, times_filter = ap.get_peaks(spectrogram)
#     ap.plot_spectrogram(spectrogram, freqs_filter, times_filter)

def get_cmap(songs_path, filename):
    peaks, freqs_filter, times_filter = [], [], []

    parsed_song = fp.parse_audio(songs_path + filename)

    for channeln, channel in enumerate(parsed_song['channels']):
        t = time()
        spectrogram = ap.get_spectrogram(channel, Fs=parsed_song['Fs'])
        spec_time = time() - t

        t = time()
        peaks, freqs_filter, times_filter = ap.get_peaks(spectrogram)
        peaks_time = time() - t

        plot_spectrogram(spectrogram, freqs_filter, times_filter, name=filename.split(".mp3")[0])
        ap.plot_spectrogram_peaks(spectrogram, freqs_filter, times_filter, name=filename.split(".mp3")[0])
        print("Spectrogram len = ", spectrogram.shape)
        print("Peaks len = ", len(peaks))
        print("spec_time = ", spec_time)
        print("peaks_time = ", peaks_time)

        break
    return peaks, freqs_filter, times_filter

def gey_haches(songs_path, filename):

    parsed_song = fp.parse_audio(songs_path + filename)
    hashes, processing_time = ap.get_fingerprint(parsed_song['channels'], parsed_song['Fs'])



def plot_spectrogram(spectrogram, freqs_filter, times_filter, name=""):

    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.title("Spectrogram of " + name)
    plt.imshow(spectrogram, cmap="afmhot")
    # plt.colorbar()
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_constellation_map(Cmap, Y=None, xlim=None, ylim=None, title='',
                           xlabel='Time (sample)', ylabel='Frequency (bins)',
                           s=5, color='r', marker='o', figsize=(7, 3), dpi=72):
    """Plot constellation map

    Notebook: C7/C7S1_AudioIdentification.ipynb

    Args:
        Cmap: Constellation map given as boolean mask for peak structure
        Y: Spectrogram representation (Default value = None)
        xlim: Limits for x-axis (Default value = None)
        ylim: Limits for y-axis (Default value = None)
        title: Title for plot (Default value = '')
        xlabel: Label for x-axis (Default value = 'Time (sample)')
        ylabel: Label for y-axis (Default value = 'Frequency (bins)')
        s: Size of dots in scatter plot (Default value = 5)
        color: Color used for scatter plot (Default value = 'r')
        marker: Marker for peaks (Default value = 'o')
        figsize: Width, height in inches (Default value = (7, 3))
        dpi: Dots per inch (Default value = 72)

    Returns:
        fig: The created matplotlib figure
        ax: The used axes.
        im: The image plot
    """
    if Cmap.ndim > 1:
        (K, N) = Cmap.shape
    else:
        K = Cmap.shape[0]
        N = 1
    if Y is None:
        Y = np.zeros((K, N))
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    im = ax.imshow(Y, origin='lower', aspect='auto', cmap='gray_r')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    Fs = 1
    if xlim is None:
        xlim = [-0.5/Fs, (N-0.5)/Fs]
    if ylim is None:
        ylim = [-0.5/Fs, (K-0.5)/Fs]
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    n, k = np.argwhere(Cmap == 1).T
    ax.scatter(k, n, color=color, s=s, marker=marker)
    plt.tight_layout()
    return fig, ax, im

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

#--------------- Fingerprint Example ---------------#
songs_path = "../"
original_filename = "Drake - Know Yourself.mp3"
crowd_filename = "Drake - Know Yourself - With Gaussian White Noise.mp3"

original_peaks, original_freqs, original_times = get_cmap(songs_path, original_filename)







# crowd_peaks, crowd_freqs, crowd_times = get_cmap(songs_path, crowd_filename)
#
# c1 = Counter(original_peaks)
# c2 = Counter(crowd_peaks)
#
# original_crowd_similitude = counter_cosine_similarity(c1, c2)
# print("original_crowd_similitude = ", original_crowd_similitude)
#
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
