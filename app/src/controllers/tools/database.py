import mysql.connector as pymysql
from controllers.tools.settings import (
HOST, USERNAME, PASSWORD, DATABASE,
CREATE_SONGS, DROP_SONGS, CREATE_FINGERPRINTS, DROP_FINGERPRINTS,
INSERT_SONG, INSERT_FINGERPRINT,
GET_MATCH_FINGERPRINTS,
GET_SONG_BY_ID,
GET_SONG_BY_FILEHASH,
COUNT_SONGS, COUNT_FINGERPRINTS)

class MySQLdb():
    m_connection = None
    m_cursor = None

    def __init__(self) :

        self.m_connection = pymysql.connect(host=HOST, user=USERNAME, passwd=PASSWORD, db=DATABASE)
        self.m_cursor = self.m_connection.cursor()
        self.create_songs_table()
        self.create_fingerprints_table()

    def query(self, query, params) :

        self.m_cursor.execute(query, params)
        return self.m_cursor

    def executeOne(self, query, params = []):

        self.m_cursor.execute(query, params)
        return self.m_cursor.fetchone()

    def executeAll(self, query, params = []):

        self.m_cursor.execute(query, params)
        return self.m_cursor.fetchall()

    def create_songs_table(self) :

        self.m_cursor.execute(CREATE_SONGS)

    def create_fingerprints_table(self):

        self.m_cursor.execute(CREATE_FINGERPRINTS)

    def close(self):
        self.m_connection.close()
        self.m_cursor.close()

    def insert_song(self,name,filehash):
        query = INSERT_SONG
        id = -1
        try:
            self.m_cursor.execute(query, (name,filehash))
            self.m_connection.commit()
            id = self.m_cursor.lastrowid
            return id
        except pymysql.Error as err:
            print("PROBLEM : INSERT SONG", err)
            self.m_connection.rollback()


    def insert_fingerprint(self,song_fk,hash,offset):
        query = INSERT_FINGERPRINT
        try:
            self.m_cursor.execute(query,(song_fk,hash,offset))
            self.m_connection.commit()

        except pymysql.Error as err:
            print("PROBLEM : INSERT FINGPRINT", err)
            self.m_connection.rollback()

    def insert_all_fingerprints(self, fingerprint_list):
        query = INSERT_FINGERPRINT
        try:
            self.m_cursor.executemany(query,fingerprint_list)
            self.m_connection.commit()
        except pymysql.Error as err:
            print("PROBLEM : INSERT FINGPRINT", err)
            self.m_connection.rollback()

    def find_match_fingerprints(self, candidate_fingerprint):
        query = GET_MATCH_FINGERPRINTS
        query = query % ', '.join(["""%s"""] * len(candidate_fingerprint))
        res = []
        try:
            res = self.executeAll(query, candidate_fingerprint)
        except pymysql.Error as err:
            print("PROBLEM : find_match_fingerprints", err)
            self.m_connection.rollback()

        return res

    def get_song_by_id(self, song_id):
        query = GET_SONG_BY_ID

        res = []
        try:
            res = self.executeOne(query, [song_id])
        except pymysql.Error as err:
            print("PROBLEM : get_song_by_id", err)
            self.m_connection.rollback()

        return res

    def get_song_by_filehash(self,hash):

        query = GET_SONG_BY_FILEHASH
        self.m_cursor.execute(query,(hash,))
        (number_of_rows,)=self.m_cursor.fetchone()
        return number_of_rows

    def count_songs(self):
        query = COUNT_SONGS

        res = []
        try:
            res = self.executeOne(query)
        except pymysql.Error as err:
            print("PROBLEM : count_songs", err)
            self.m_connection.rollback()

        return res

    def count_fingerprints(self):
        query = COUNT_FINGERPRINTS

        res = []
        try:
            res = self.executeOne(query)
        except pymysql.Error as err:
            print("PROBLEM : count_fingerprints", err)
            self.m_connection.rollback()

        return res

    def free(self):
        self.m_cursor.execute(DROP_FINGERPRINTS)
        self.m_cursor.execute(DROP_SONGS)
        self.create_songs_table()
        self.create_fingerprints_table()
