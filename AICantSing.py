import openai
import pyaudio
import wave
import numpy as np
import time
import keyboard
import threading
from pynput import keyboard as pynput_keyboard
#import multiprocessing

import sys
import os

from dotenv import load_dotenv
load_dotenv()

USE_LOCAL_MODEL = False

artist_song_info = input('Enter the artist and song or relevant details (leave blank to skip). then press Enter: ').strip()

ABS_PATH = os.getenv("MY_ABS_PATH")
sys.path.append(os.path.dirname(os.path.abspath("ABS_PATH")))
from utils import generate_image  # Importing the function from a separate file

API_KEY = os.getenv("MY_API_KEY")

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
DEVICE_INDEX = 2  # Change this to the desired input device index. You can find it using the resepctive cell in the ipnyb.

AUDIO_FILE = os.path.expanduser("~/Desktop/output.wav")  # Temporary file for transcription. Save to Desktop
#AUDIO_FILE = "temp_audio.wav"  # Temporary file for transcription

# Global pause flag
pause_flag = threading.Event()
pause_flag.clear()

def on_press(key):
    try:
        if key == pynput_keyboard.Key.f8:
            pause_flag.set()
            print("\n--- PAUSED --- (Press F9 to resume)")
        elif key == pynput_keyboard.Key.f9:
            if pause_flag.is_set():
                pause_flag.clear()
                print("Resumed.")
    except Exception:
        pass

# Start listener in background
listener = pynput_keyboard.Listener(on_press=on_press)
listener.daemon = True
listener.start()

# Function to capture audio from the microphone
def record_audio(duration=3):
    """Records audio for a specified duration and saves it to a file."""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=DEVICE_INDEX)

    print("Recording...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(AUDIO_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

# Function to transcribe recorded audio
def transcribe_audio():
    """Uses OpenAI Whisper API to transcribe recorded audio."""
    client = openai.OpenAI(api_key=API_KEY)  # Add your API key here

    with open(AUDIO_FILE, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    return transcript.text  # Access the text field properly

# Function to check for meaningful content and spawn a process
def check_and_spawn_process(transcript, function_to_run):
    import string
    
    # Remove spaces and punctuation, convert to lowercase
    cleaned_text = transcript.lower().translate(str.maketrans('', '', string.punctuation + ' '))
    
    # Check if there are at least 4 meaningful characters
    if len(cleaned_text) >= 4:
        print(f"Meaningful content detected! Generating image...")
        # Use the full transcript as the sentence
        sentence = transcript.strip()
        # Prepend artist/song info if provided
        if artist_song_info:
            prompt = f"{artist_song_info}: {sentence}"
        else:
            prompt = sentence
        function_to_run(prompt, API_KEY, use_local_model=USE_LOCAL_MODEL)
        return True
    return False


# Main function to handle live transcription
needs_prompt = False

def main():
    global artist_song_info, needs_prompt
    while True:
        if pause_flag.is_set():
            # Wait until unpaused
            while pause_flag.is_set():
                time.sleep(0.1)
            # Set flag to prompt after current operation
            needs_prompt = True

        record_audio(duration=3)
        transcript = transcribe_audio()
        print(f"Transcription: {transcript}")
        check_and_spawn_process(transcript, generate_image)
        import cv2
        cv2.waitKey(1)
        time.sleep(0.3)

        # Prompt for new info if needed
        if needs_prompt:
            new_info = input("Enter new artist and song info (leave blank to keep current): ").strip()
            if new_info:
                artist_song_info = new_info
            needs_prompt = False

if __name__ == "__main__":
    main()
