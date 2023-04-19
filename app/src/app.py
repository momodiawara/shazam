#!/usr/bin/python3

import controllers.process_songs as ps
import controllers.recognize_microphone as rm
import controllers.recognize_file as rf
import controllers.reset_database as rd
import controllers.show_dbinfo as dbinfo
from pathlib import Path
from texttable import Texttable

def print_recognition_res_as_table(final_results, processing_time, query_time, align_time):
    print("")
    t1 = Texttable()
    t1.set_max_width(125)
    t1.header( ['SONG_ID', 'SONG_NAME', 'INPUT_HASHES', 'HASHES_MATCHED', 'INPUT_CONFIDENCE', 'OFFSET', 'OFFSET_SECS', 'SONG_FILE_HASH'])

    for res in final_results:
        t1.add_row( res.values() )

    print(t1.draw())

    print("")
    t2 = Texttable()
    t2.set_max_width(125)
    t2.header( ['PROCESSING TIME', 'QUERY TIME', 'ALIGN TIME', 'TOTAL TIME'] )
    t2.add_row( [processing_time, query_time, align_time, processing_time+align_time+query_time] )
    print(t2.draw())

def prin_database_info(num_songs, num_fingerprints):
    print("")
    t1 = Texttable()
    t1.set_max_width(125)
    t1.header( ['TABLE_NAME', 'NUMBER_OF_ENTRIES'])

    t1.add_row( ['SONGS', num_songs] )
    t1.add_row( ['FINGERPRINTS', num_fingerprints] )


    print(t1.draw())

def ask_number_of_seconds():
    answer = None
    while( True ):

        print("\nHow many seconds you want to record ?")
        try:
            answer = int(input())
            break
        except:
            print("That's not a valid option!")


    return answer

def ask_if_sure():
    answer = None
    while( True ):

        print("\nThis action will delete all data in your Database.\nDo you want to proceed? [Y/N]\n")
        try:
            answer = str(input())
            if answer not in ['y', 'Y', 'n', 'N'] :
                print("That's not a valid option!")
            else :
                if answer in ['y', 'Y']: answer = 1
                if answer in ['n', 'N']: answer = 0
                break
        except:
            print("That's not a valid option!")

    return answer

def ask_file_path():
    answer = None
    while( True ):

        print("\nWhat is the file path ?\n")
        answer = input()
        filpath = Path(answer)
        if filpath.exists():
            break
        else:
            print("Oops, file doesn't exist!")

    return answer

def ask_user():
    answer = None
    while( True ):

        print("\n1 - Recognize Song From Microphone",
              "\n2 - Recognize Song From File",
              "\n3 - Process Existing Songs To Database",
              "\n4 - Show Details About The Databse",
              "\n5 - Reset Database",
              "\n6 - Quit Program\n")

        try:
            answer = int(input())
            break
        except:
            print("That's not a valid option!")

    return answer

#---------------- Main ----------------#

def start():
    rec_microphone = rm.MicrophoneRecognition()
    rec_file = rf.FileRecognition()
    reset_db = rd.ResetDatabase()
    show_dbinfo = dbinfo.ShowDatabaseInfo()

    option = -1
    while option != 6 :
        option = ask_user()

        if option == 1:
            sec = ask_number_of_seconds()
            final_results, processing_time, query_time, align_time = rec_microphone.recognize(seconds=sec)
            print_recognition_res_as_table(final_results, processing_time, query_time, align_time)
        elif option == 2:
            path = ask_file_path()
            final_results, processing_time, query_time, align_time = rec_file.recognize(path)
            print_recognition_res_as_table(final_results, processing_time, query_time, align_time)
        elif option == 3:
            path = ask_file_path()
            ps.add_songs_to_db(path)

        elif option == 4:
            num_songs, num_fingerprints = show_dbinfo.get_info()
            prin_database_info(num_songs, num_fingerprints)

        elif option == 5:
            sure = ask_if_sure()
            if sure : reset_db.reset()

        elif(option == 6):
            print("Goodbye")
#------------------------------------------------#

start()
