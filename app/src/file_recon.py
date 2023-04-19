import controllers.process_songs as ps
import controllers.recognize_microphone as rm
import controllers.recognize_file as rf
import controllers.reset_database as rd
from pathlib import Path
from texttable import Texttable
from tqdm import tqdm
import os


rec_file = rf.FileRecognition()

dest_dir = "../noised_songs/"

hits = 0
exec_time = 0
for filename in tqdm(os.listdir(dest_dir)):
    if filename.endswith(".mp3"):
        original_filepath = os.path.join(dest_dir, filename)
        final_results, processing_time, query_time, align_time = rec_file.recognize(original_filepath)
        exec_time = exec_time + processing_time + query_time + align_time

        print(filename.split(".mp3")[0])
        print(final_results[0]["SONG_NAME"])

        name = final_results[0]["SONG_NAME"]
        name = name.decode("utf-8")

        if filename.split(".mp3")[0] in name :
            hits = hits + 1


print("HITS = " , hits)
print("ACCURACY PERCENTAGE = " , (hits / 50) * 100 )
print("AVERAGE EXEC TIME = " , exec_time / 50)
