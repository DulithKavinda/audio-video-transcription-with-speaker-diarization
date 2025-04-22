
🎙 Audio/Video Transcription with Speaker Diarization
=====================================================

This project converts a **video** or **audio** file into a **text transcript** using [AssemblyAI's Speech-to-Text API](https://www.assemblyai.com/). If the input is a video, it is first converted into audio using `ffmpeg`. The transcript can also include **speaker labels** if multiple speakers are detected.

* * *

Features
----------

*   Converts video files (`.mp4`, `.mov`, `.mkv`) to `.mp3` audio automatically.
    
*   Uploads audio to AssemblyAI.
    
*   Transcribes speech to text.
    
*   Identifies multiple speakers and labels them (e.g., Speaker A, Speaker B).
    
*   Saves the transcript to a `.txt` file.
    
    *   If only one speaker: plain transcript.
        
    *   If multiple speakers: labeled by speaker.
        
*   ⏳ Shows progress while converting or waiting for the transcription.

* * *

Technologies Used
--------------------

*   **Python 3**
    
*   **AssemblyAI API** for transcription and speaker diarization
    
*   **ffmpeg** for video-to-audio conversion
    
*   **Requests** library for HTTP communication
    
*   **Threading** and **subprocess** for process handling and clean CLI output

* * *

Project Files
----------------

*   `main.py` – The entry point. Determines file type and runs the transcription pipeline.
    
*   `api_communication.py` – Handles video-to-audio conversion, API communication, polling, and transcript saving.
    
*   `api_secrets.py` – Stores your AssemblyAI API key (`API_KEY`).
    
*   Transcript output – A `.txt` file with the same name as your input will be generated in the current directory.

* * *

Setup
---------

1.  **Install ffmpeg**
    
    *   On Windows: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) and add it to system PATH.
        
    *   On Linux/Mac:
        
        bash
        
        CopyEdit
        
        `sudo apt install ffmpeg     # Debian/Ubuntu brew install ffmpeg         # macOS with Homebrew`
        
2.  **Install dependencies**  
    Run this command in your terminal:
    
    bash
    
    CopyEdit
    
    `pip install requests`
    
3.  **Set your AssemblyAI API key**
    
    *   Create a file called `api_secrets.py` in the root folder.
        
    *   Paste your key like this:
        
        python
        
        CopyEdit
        
        `API_KEY = "your_assembly_ai_api_key"`

* * *

How to Run
-------------

From the terminal run:

bash

CopyEdit

`python main.py yourfile.mp4`

Or for audio:

bash

CopyEdit

`python main.py yourfile.mp3`

* * *

Output
---------

*   A file named like `yourfile_with_speakers.txt` will be generated.
    
*   If multiple speakers: the text includes labels like `Speaker A`, `Speaker B` etc.
    
*   If one speaker: plain transcript without labels.

* * *
