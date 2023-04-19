
#----------------- DATABASE CONFIG -----------------#
HOST = "localhost"
USERNAME = "phpmyadmin"
PASSWORD = "phpmyadmin"
DATABASE = "music_rec_min"

#----------------- DATABASE QUERIES -----------------#
CREATE_SONGS ="""CREATE TABLE IF NOT EXISTS SONGS (
                    id MEDIUMINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
                    name  varchar(250) NOT NULL,
                    filehash  varchar(60))
                    ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

DROP_SONGS ="""DROP TABLE IF EXISTS SONGS;"""

CREATE_FINGERPRINTS = """CREATE TABLE IF NOT EXISTS FINGERPRINTS (
                            song_fk MEDIUMINT UNSIGNED NOT NULL,
                            hash BINARY(10) not null,
                            offset int unsigned not null,
                            UNIQUE(song_fk, offset, hash),
                            INDEX(hash),
                            FOREIGN KEY (song_fk) REFERENCES SONGS (id)
                            ON UPDATE CASCADE ON DELETE CASCADE)
                            ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

DROP_FINGERPRINTS ="""DROP TABLE IF EXISTS FINGERPRINTS;"""

GET_SONG_BY_ID = """SELECT name, filehash FROM SONGS WHERE id = %s"""

GET_SONG_BY_FILEHASH = """SELECT count(*) FROM SONGS WHERE filehash = %s"""

GET_MATCH_FINGERPRINTS = """SELECT hash, song_fk, offset FROM FINGERPRINTS WHERE hash IN (%s)"""

INSERT_FINGERPRINT = """INSERT INTO FINGERPRINTS (song_fk,hash,offset) VALUES (%s,UNHEX(%s),%s)"""

INSERT_SONG = """INSERT INTO SONGS (name,filehash) VALUES (%s,%s)"""

COUNT_SONGS = """SELECT count(*) FROM SONGS"""
COUNT_FINGERPRINTS = """SELECT count(*) FROM FINGERPRINTS"""

#----------------- RECORDER CONFIG -----------------#
DEFAULT_CHUNKSIZE = 8192
DEFAULT_CHANNELS = 2

#----------------- AUDIO PROCESSOR CONFIG -----------------#
IDX_FREQ_I = 0
IDX_TIME_J = 1

# Sampling rate, related to the Nyquist conditions, which affects
# the range frequencies we can detect.
DEFAULT_FS = 44100

# Size of the FFT window, affects frequency granularity
DEFAULT_WINDOW_SIZE = 4096

# Ratio by which each sequential window overlaps the last and the
# next window. Higher overlap will allow a higher granularity of offset
# matching, but potentially more fingerprints.
DEFAULT_OVERLAP_RATIO = 0.5

# Degree to which a fingerprint can be paired with its neighbors. Higher values will
# cause more fingerprints, but potentially better accuracy.
DEFAULT_FAN_VALUE = 15

# Minimum amplitude in spectrogram in order to be considered a peak.
# This can be raised to reduce number of fingerprints, but can negatively
# affect accuracy.
DEFAULT_AMP_MIN = 10

# Number of cells around an amplitude peak in the spectrogram in order
# to consider it a spectral peak. Higher values mean less
# fingerprints and faster matching, but can potentially affect accuracy.
PEAK_NEIGHBORHOOD_SIZE = 20

# If True, will sort peaks temporally for fingerprinting;
# not sorting will cut down number of fingerprints, but potentially
# affect performance.
PEAK_SORT = True

# Number of bits to grab from the front of the SHA1 hash in the
# fingerprint calculation. The more you grab, the more memory storage,
# with potentially lesser collisions of matches.
FINGERPRINT_REDUCTION = 20

# Thresholds on how close or far fingerprints can be in time in order
# to be paired as a fingerprint. If your max is too low, higher values of
# DEFAULT_FAN_VALUE may not perform as expected.
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200

#----------------- SONG FINDER CONFIG -----------------#

# Number of results being returned for file recognition
TOPN = 4
