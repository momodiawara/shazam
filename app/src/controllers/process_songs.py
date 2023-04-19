import os
import controllers.tools.audioprocessor as ap
import controllers.tools.database as db
import controllers.tools.fileprocessor as fp
from tqdm import tqdm

def add_songs_to_db(songs_path):
    music_db = db.MySQLdb()

    for filename in tqdm(os.listdir(songs_path)):
        if filename.endswith(".mp3"):
            parsed_song = fp.parse_audio( os.path.join(songs_path, filename) )

            song = music_db.get_song_by_filehash(parsed_song['file_hash'])

            if song :
                continue

            song_name = filename.split('.mp3')[0]
            song_id = music_db.insert_song(song_name, parsed_song['file_hash'])
            hashes, processing_time = ap.get_fingerprint(parsed_song['channels'], parsed_song['Fs'])
            # new_hashes = [hash for sublist in hashes for hash in sublist]

            fingerprints = []
            for hash, offset in hashes:
                fingerprints.append( (song_id, hash, int(offset)) )

            # a_set = set(fingerprints)
            # contains_duplicates = len(fingerprints) != len(a_set)
            #
            #
            # print("SONG FILE ", filename, " \t NUM OF HASHES = ", len(fingerprints), " \t SIMILAR ELEMENTS = ", contains_duplicates)
            music_db.insert_all_fingerprints( fingerprints )
    music_db.close()
