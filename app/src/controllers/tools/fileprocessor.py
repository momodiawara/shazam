import os
from pydub import AudioSegment
from pydub.utils import audioop
import numpy as np
from hashlib import sha1

from time import time

def generate_file_hash(song_file, blocksize=2**20):
  s = sha1()

  with open(song_file , "rb") as f:
    while True:
      buf = f.read(blocksize)
      if not buf: break
      s.update(buf)

  return s.hexdigest().upper()

def parse_audio(song_file):
    songname, extension = os.path.splitext(os.path.basename(song_file))

    try:
        audiofile = AudioSegment.from_file(song_file)

        data = np.fromstring(audiofile._data, np.int16)

        channels = []
        for channel in range(audiofile.channels):
            channels.append( data[channel::audiofile.channels] )

    except audioop.error:
        print("audioop.error")
        pass

    return {
        "songname": songname,
        "extension": extension,
        "channels": channels,
        "Fs": audiofile.frame_rate,
        "file_hash": generate_file_hash(song_file)
    }
