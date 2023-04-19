from ctypes import *
import pyaudio
import wave
import numpy as np
from controllers.tools.settings import (DEFAULT_FS, DEFAULT_CHUNKSIZE, DEFAULT_CHANNELS)

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')

class Recorder():

    def __init__(self, FORMAT = pyaudio.paInt16, CHANNELS = DEFAULT_CHANNELS, RATE = DEFAULT_FS, CHUNK = DEFAULT_CHUNKSIZE):
        self.FORMAT = FORMAT
        self.RATE = RATE
        self.CHANNELS = CHANNELS
        self.CHUNK = CHUNK
        self.SAMPWIDTH = 0
        asound.snd_lib_error_set_handler(c_error_handler)


    def record(self, RECORD_SECONDS = 5):
        # instantiate PyAudio
        audio = pyaudio.PyAudio()

        # open audio stream
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)

        # read data
        print("\nRECORDING...")
        frames = []
        data = [[] for i in range(self.CHANNELS)]

        for i in range(0, int(self.RATE / self.CHUNK * RECORD_SECONDS)):
            raw_data = stream.read(self.CHUNK)

            nums = np.fromstring(raw_data, np.int16)
            for j in range(self.CHANNELS):
              data[j].extend(nums[j::self.CHANNELS])

            frames.append(raw_data)
        print("FINISHED RECORDING")

        # close audio stream
        stream.stop_stream()
        stream.close()

        self.SAMPWIDTH = audio.get_sample_size(self.FORMAT)


        # close PyAudio
        audio.terminate()

        return frames, data

    def save(self, frames, WAVE_OUTPUT_FILENAME = "output"):
        WAVE_OUTPUT_FILENAME += ".wav"
        waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.SAMPWIDTH)
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print(f"file {WAVE_OUTPUT_FILENAME} saved")
