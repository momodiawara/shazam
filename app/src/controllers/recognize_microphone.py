import controllers.tools.recorder as rec
import controllers.tools.audioprocessor as ap
import controllers.tools.songfinder as sf

class MicrophoneRecognition():

    def __init__(self):
        self.processing_time = -1.0
        self.query_time = -1.0
        self.align_time = -1.0
        self.final_results = []
        self.hashes = set()
        self.recorder = rec.Recorder()
        self.spectrogram = []

    def recognize(self, seconds = 10):
        frames, data = self.recorder.record(RECORD_SECONDS=seconds)

        self.hashes, self.processing_time = ap.get_fingerprint(data)
        matches, dedup_hashes, self.query_time = sf.find_matches(self.hashes)
        self.final_results, self.align_time = sf.align_matches(matches, dedup_hashes, len(self.hashes))

        return self.final_results, self.processing_time, self.query_time, self.align_time

    def get_all_relevant_data(self):
        matching_data = {
            'QUERY TIME': self.query_time,
            'ALIGN TIME': self.align_time,
            'SPECTROGRAM': self.spectrogram,
            'FINAL RESULATS': self.final_results,
        }

        return matching_data
