from time import time
from itertools import groupby
import controllers.tools.database as db
from controllers.tools.settings import (TOPN, DEFAULT_FS, DEFAULT_WINDOW_SIZE, DEFAULT_OVERLAP_RATIO)

def find_matches(sample_hashes):
    music_db = db.MySQLdb()

    t = time()
    matches, dedup_hashes = return_matches(sample_hashes, music_db)
    query_time = time() - t

    music_db.close()

    return matches, dedup_hashes, query_time

def align_matches(matches, dedup_hashes, queried_hashes):
    music_db = db.MySQLdb()

    t = time()
    songs_result = return_alignes(matches, dedup_hashes, queried_hashes, music_db)
    align_time = time() - t

    music_db.close()

    return songs_result, align_time

def return_matches(sample_hashes, music_db, batch_size=10000):

   # """
   #      Searches the database for pairs of (hash, offset) values.
   #      return: a list of (sid, offset_difference) tuples and a
   #      dictionary with the amount of hashes matched (not considering
   #      duplicated hashes) in each song.
   #          - song id: Song identifier
   #          - offset_difference: (database_offset - sampled_offset)
   #  """

    # Create a dictionary of hash => offset pairs for later lookups
    mapper = {}
    values = []

    for hsh, offset in sample_hashes:
        hsh_bytes = bytes.fromhex( hsh )
        values.append(hsh_bytes)

        if hsh in mapper.keys():
            mapper[hsh].append(offset)
        else:
            mapper[hsh] = [offset]

    # values = list(mapper.keys())

    # in order to count each hash only once per db offset we use the dic below
    dedup_hashes = {}

    results = []

    db_res = music_db.find_match_fingerprints(values)

    for hsh, sid, offset in db_res:
        try:
            hsh = hsh.hex()
        except :
            continue;

        if sid not in dedup_hashes.keys():
            dedup_hashes[sid] = 1
        else:
            dedup_hashes[sid] += 1
        #  we now evaluate all offset for each  hash matched
        for song_sampled_offset in mapper[hsh]:

            results.append((sid, offset - song_sampled_offset))

    return results, dedup_hashes


def return_alignes(matches, dedup_hashes, queried_hashes, music_db, topn = TOPN):
    # count offset occurrences per song and keep only the maximum ones.
    sorted_matches = sorted(matches, key=lambda m: (m[0], m[1]))
    counts = [(*key, len(list(group))) for key, group in groupby(sorted_matches, key=lambda m: (m[0], m[1]))]
    songs_matches = sorted(
        [max(list(group), key=lambda g: g[2]) for key, group in groupby(counts, key=lambda count: count[0])],
        key=lambda count: count[2], reverse=True
    )

    songs_result = []

    for song_id, offset, _ in songs_matches[0:topn]:  # consider topn elements in the result
        song = music_db.get_song_by_id(song_id)
        song_name = song[0]
        song_hash = song[1]
        nseconds = round(float(offset) / DEFAULT_FS * DEFAULT_WINDOW_SIZE * DEFAULT_OVERLAP_RATIO, 5)
        hashes_matched = dedup_hashes[song_id]

        song = {
            'SONG_ID': song_id,
            'SONG_NAME': song_name.encode("utf8"),
            'INPUT_HASHES': queried_hashes,
            # 'FINGERPRINTED_HASHES': song_hashes,
            'HASHES_MATCHED': hashes_matched,
            # Percentage regarding hashes matched vs hashes from the input.
            'INPUT_CONFIDENCE': round(hashes_matched / queried_hashes, 2),
            # Percentage regarding hashes matched vs hashes fingerprinted in the db.
            # 'FINGERPRINTED_CONFIDENCE': round(hashes_matched / song_hashes, 2),
            'OFFSET': offset,
            'OFFSET_SECS': nseconds,
            'SONG_FILE_HASH': song_hash.encode("utf8")
        }

        songs_result.append(song)
        songs_result.sort(key= lambda x: x['INPUT_CONFIDENCE'], reverse=True)
    return songs_result
