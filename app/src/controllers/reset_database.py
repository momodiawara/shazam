import controllers.tools.database as db

class ResetDatabase():

    def __init__(self):
        pass

    def reset(self):
        music_db = db.MySQLdb()
        music_db.free()
        music_db.close()
        print("DATABASE IS GOOD AS NEW !")
