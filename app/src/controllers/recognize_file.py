import controllers.tools.audioprocessor as ap
import controllers.tools.fileprocessor as fp
import controllers.tools.songfinder as sf
from pathlib import Path


class FileRecognition():

    def __init__(self):
        self.name = ""
        self.processing_time = -1.0
        self.query_time = -1.0
        self.align_time = -1.0
        self.final_results = []
        self.hashes = set()

    def recognize(self, filepath):
        filename = Path(filepath)

        if (filename.exists() and filename.suffix == ".mp3"):
            parsed_song = fp.parse_audio(filename)

            self.hashes, self.processing_time = ap.get_fingerprint(parsed_song['channels'], parsed_song['Fs'])
            matches, dedup_hashes, self.query_time = sf.find_matches(self.hashes)
            self.final_results, self.align_time = sf.align_matches(matches, dedup_hashes, len(self.hashes))
        else :
            print("Path Problem !")

        return self.final_results, self.processing_time, self.query_time, self.align_time

    def get_all_relevant_data(self):
        matching_data = {
            'QUERY TIME': self.query_time,
            'ALIGN TIME': self.align_time,
            'SPECTROGRAM': self.spectrogram,
            'FINAL RESULATS': self.final_results,
        }

        return matching_data
