# dirpath = "/home/thorium90/projet_synthese/app/songs/"
# destdir = "/home/thorium90/projet_synthese/app/trimed_songs"
for file in *.mp3; do
  echo "poop"
  ffmpeg -i "$file" -ss 00:01:00 -to 00:01:03 -c copy "/home/thorium90/projet_synthese/app/trimed_songs/$file"
done
