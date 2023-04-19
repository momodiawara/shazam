import controllers.tools.database as db

class ShowDatabaseInfo():

    def __init__(self):
        self.num_songs = -1
        self.num_fingerprints = -1


    def get_info(self):
        music_db = db.MySQLdb()
        self.num_songs = music_db.count_songs()[0]
        self.num_fingerprints = music_db.count_fingerprints()[0]
        music_db.close()

        return self.num_songs, self.num_fingerprints
