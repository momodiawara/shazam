import process_songs as ps
# import recognize_microphone as rm
import tools.database as db


# music_db = db.MySQLdb()
# id = music_db.insert_song("test name", "haaaaash7594631")
# song_fk,hash,offset = id, "pocdcnv", 552
# music_db.insert_fingerprint(song_fk, hash, offset)
ps.add_songs_to_db("../../songs/")
