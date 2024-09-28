# https://github.com/KennyVaneetvelde/groq_whisperer/blob/main/main.py

import os
import tempfile
import wave
import pyaudio
import keyboard                         
import pyautogui
import pyperclip
from groq import Groq
from icecream import ic

from dotenv import load_dotenv
load_dotenv()

# Set up Groq client
client = Groq()



def record_audio(sample_rate=16000, channels=1, chunk=1024):

    global running

    ic(record_audio)

    """
    Record audio from the microphone while the PAUSE button is held down.
    """
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk,
    )

    ic("Press and hold the PAUSE button to start recording...")
    frames = []


    keyboard.wait("pause")  # Wait for PAUSE button to be pressed
    ic("Recording... (Release PAUSE to stop)")

    while keyboard.is_pressed("pause"):
        data = stream.read(chunk)
        ic(data)
        frames.append(data)

    ic("Recording finished.")
    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames, sample_rate


def save_audio(frames, sample_rate):
    ic("def save_audio")
    ic(len(frames))
    ic(sample_rate)
    """
    Save recorded audio to a temporary WAV file.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        wf = wave.open(temp_audio.name, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()
        return temp_audio.name


def transcribe_audio(audio_file_path):

    ic("transcribing at: ", audio_file_path)

    """
    Transcribe audio using Groq's Whisper implementation.
    """
    try:
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(audio_file_path), file.read()),
                model="whisper-large-v3",
                prompt="""The audio is by a programmer discussing programming issues, the programmer mostly uses python and might mention python libraries or reference code in his speech.""",
                response_format="text",
                language="en",
            )
        return transcription  # This is now directly the transcription text
    except Exception as e:
        ic(f"An error occurred in transribe_audio: {str(e)}")
        return None


def copy_transcription_to_clipboard(text):
    """
    Copy the transcribed text to clipboard using pyperclip.
    """
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")



def record_main():
    ic(" def record_main")

    while True:
        # Record audio
        frames, sample_rate = record_audio()

        # Save audio to temporary file
        temp_audio_file = save_audio(frames, sample_rate)


        ic(temp_audio_file)

        # Transcribe audio
        print("Transcribing...")
        transcription = transcribe_audio(temp_audio_file)

        # Copy transcription to clipboard
        if transcription:
            print("\nTranscription:")
            ic(transcription)
            print("Copying transcription to clipboard...")
            # copy_transcription_to_clipboard(transcription)
            print("Transcription copied to clipboard and pasted into the application.")
        else:
            print("Transcription failed.")

        # Clean up temporary file
        os.unlink(temp_audio_file)

        print("\nReady for next recording. Press PAUSE to start.")
    



if __name__ == "__main__":
    record_main()