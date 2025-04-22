import requests
from api_secrets import API_KEY
import time
import subprocess
import threading



upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

headers = {'authorization': API_KEY}



#convert video to audio
def video_to_audio(input_file, output_file):
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        output_file
    ]

    def show_loading():
        while not done[0]:
            print("⏳ Converting...", end="\r")
            time.sleep(1)

    done = [False]
    thread = threading.Thread(target=show_loading)
    thread.start()

    try:
        subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        done[0] = True
        thread.join()
        print("Video successfully converted to audio!")
    except subprocess.CalledProcessError:
        done[0] = True
        thread.join()
        print("Video to audio conversion failed!")



# upload
def upload(filename):
    def read_file(filename, chunk_size=5242880):
     with open(filename, 'rb') as _file:
      while True:
       data = _file.read(chunk_size)
       if not data:
        break
       yield data

    upload_response = requests.post( upload_endpoint ,
                            headers=headers,
                            data=read_file(filename))

    audio_url = upload_response.json()['upload_url']
    return audio_url

#transcribe

# transcribe
def transcribe(audio_url):
    transcript_request = { "audio_url": audio_url,
                           "speaker_labels": True
                             }
    transcript_response = requests.post(transcript_endpoint, json=transcript_request, headers=headers)
    job_id =  transcript_response.json()['id']
    return job_id



#poll

def poll(transcript_id):
    polling_endpoint = transcript_endpoint + '/' + transcript_id
    polling_response = requests.get(polling_endpoint, headers=headers)
    return polling_response.json()

def get_transcription_result_url(audio_url):
    transcript_id = transcribe(audio_url)
    while True:
     data = poll(transcript_id)
     if data['status'] == 'completed':
        return data, None
     elif data['status'] == 'error':
        return data, data['error']
     
     print('⏳waiting 30 seconds...')
     time.sleep(30)

speaker_map = {}

def get_speaker_label(speaker_num):
    if speaker_num not in speaker_map:
        speaker_map[speaker_num] = chr(65 + len(speaker_map))  # A, B, C...
    return f"Speaker {speaker_map[speaker_num]}"    

#save tarnscript
def save_transcript(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)

    if data:
        text_file = filename + '_with_speakers.txt'
        with open(text_file, 'w') as f:
            if 'utterances' in data:
                # Count how many unique speakers are in the utterances
                unique_speakers = set(utt['speaker'] for utt in data['utterances'])

                if len(unique_speakers) > 1:
                    # Multiple speakers - include speaker labels
                    for utt in data['utterances']:
                        speaker = utt['speaker']
                        text = utt['text']
                        f.write(f"{get_speaker_label(speaker)}: {text}\n")
                else:
                    # Single speaker - combine all utterances into one plain text
                    full_text = ' '.join(utt['text'] for utt in data['utterances'])
                    f.write(full_text)
            else:
                # No utterance info, fallback to plain transcript
                f.write(data['text'])

        print("Transcription saved!")
    elif error:
        print("error", error)
