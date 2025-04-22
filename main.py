import sys
import os
from api_communication import *

filename = sys.argv[1]

# Determine extension
ext = os.path.splitext(filename)[1].lower()

# If video, convert to audio
if ext in [".mp4", ".mov", ".mkv"]:
    audio_filename = os.path.splitext(filename)[0] + "_converted.mp3"
    video_to_audio(filename, audio_filename)
    filename = audio_filename  # use converted audio file

audio_url = upload(filename)
save_transcript(audio_url, filename)
