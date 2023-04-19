import numpy as np
import matplotlib.mlab as mlab
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure, iterate_structure, binary_erosion)
from operator import itemgetter
import matplotlib.pyplot as plt
import hashlib
from time import time


# importing settings
from controllers.tools.settings import (
IDX_FREQ_I,
IDX_TIME_J,
DEFAULT_FS,
DEFAULT_WINDOW_SIZE,
DEFAULT_OVERLAP_RATIO,
DEFAULT_FAN_VALUE,
DEFAULT_AMP_MIN,
PEAK_NEIGHBORHOOD_SIZE,
PEAK_SORT,
FINGERPRINT_REDUCTION,
MIN_HASH_TIME_DELTA,
MAX_HASH_TIME_DELTA)

def get_spectrogram(channel_samples, Fs=DEFAULT_FS, wsize=DEFAULT_WINDOW_SIZE, wratio=DEFAULT_OVERLAP_RATIO):

    # SFFT the signal and extract frequency components
    spectrogram = mlab.specgram(
            channel_samples,
            NFFT=wsize,
            Fs=Fs,
            window=mlab.window_hanning,
            noverlap=int(wsize * wratio))[0]

    # Apply log transform since specgram function returns linear array. 0s are excluded to avoid np warning
    spectrogram = 10 * np.log10(spectrogram, out=np.zeros_like(spectrogram), where=(spectrogram != 0))
    return spectrogram

def get_peaks(spectrogram, amp_min=DEFAULT_AMP_MIN):

    struct = generate_binary_structure(2, 1)

    #  And then we apply dilation using the following function
    #  http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.iterate_structure.html
    #  Take into account that if PEAK_NEIGHBORHOOD_SIZE is 2 you can avoid the use of the scipy functions and just
    #  change it by the following code:
    #  neighborhood = np.ones((PEAK_NEIGHBORHOOD_SIZE * 2 + 1, PEAK_NEIGHBORHOOD_SIZE * 2 + 1), dtype=bool)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our filter mask
    local_max = maximum_filter(spectrogram, footprint=neighborhood) == spectrogram

    # local_max is a mask that contains the peaks we are
    # looking for, but also the background.
    # In order to isolate the peaks we must remove the background from the mask.

    # Applying erosion to create the mask of the background
    background = (spectrogram == 0)


    # a little technicality: we must erode the background in order to
    # successfully subtract it form local_max, otherwise a line will
    # appear along the background border (artifact of the local maximum filter)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # we obtain the final mask, containing only peaks,
    # by removing the background from the local_max mask (xor operation)
    # Boolean mask of spectrogram with True at peaks (applying XOR on both matrices).
    detected_peaks = local_max != eroded_background

    # extract peaks
    amps = spectrogram[detected_peaks]
    freqs, times = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()

    # get indices for frequency and time
    filter_idxs = np.where(amps > amp_min)

    freqs_filter = freqs[filter_idxs]
    times_filter = times[filter_idxs]

    peaks = list(zip(freqs_filter, times_filter))
    return peaks, freqs_filter, times_filter

def generate_hashes(peaks, fan_value=DEFAULT_FAN_VALUE):

    if PEAK_SORT:
        peaks.sort(key=itemgetter(1))

    hashes = []
    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                #prendre la valeur de fréquence de crête actuelle et suivante
                freq1 = peaks[i][0]
                freq2 = peaks[i+j][0]

                #prendre le décalage horaire actuel et suivant
                t1 = peaks[i][1]
                t2 = peaks[i+j][1]

                #la difference de temps
                t_delta = t2 - t1

                if (t_delta >=0 and t_delta <= 200):
                    h = hashlib.sha1(("%s|%s|%s" % (str(freq1), str(freq2), str(t_delta))).encode('utf-8'))
                    hashes.append((h.hexdigest()[0:FINGERPRINT_REDUCTION], t1))
    return hashes

def get_fingerprint(channels, Fs=DEFAULT_FS):
    t = time()
    hashes = set()
    # hashes = list()

    for channeln, channel in enumerate(channels):
        spectrogram = get_spectrogram(channel, Fs=Fs)
        peaks, freqs_filter, times_filter = get_peaks(spectrogram)
        channel_hashes = set( generate_hashes(peaks) )

        # the | operator to concatenate two sets (union in set theory)
        hashes |= channel_hashes
        # hashes.append(list(channel_hashes))

    processing_time = time() - t
    return hashes, processing_time

def plot_spectrogram_peaks(spectrogram, freqs_filter, times_filter, name=""):

    # scatter of the peaks
    fig, ax = plt.subplots()
    fig.set_size_inches(13, 7)

    ax.imshow(spectrogram, cmap="afmhot")

    ax.scatter(times_filter, freqs_filter, s=5, color="black")
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency')
    ax.set_title("Constellation map of " + name)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
