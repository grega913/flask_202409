
import time
from icecream import ic
import threading
import tempfile
import wave
import pyaudio
import keyboard                         
import pyautogui
import pyperclip
from groq import Groq
import pyaudio
import os
from icecream import ic


from recordin import save_audio, transcribe_audio

from main import  socketio

# Set up Groq client
client = Groq()

'''
class AudioRecorder():

    def __init__(self):
        print("init")
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.transcription = None
        self.running = None
        self.chunk=1024
        self.sample_rate = 16000

    def start_recording(self):
        self.running = True
        self.transcription = None
        self.frames=[]

        stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk,
        )


        while self.running:
            data = stream.read(self.chunk)
            self.frames.append(data)
        
        ic("Recording finished.")
        stream.stop_stream()
        stream.close()
        self.p.terminate()

       
        return self.frames, self.sample_rate


    def stop_recording(self):
        ic("def stop recording")

        self.running = False
        temp_audio_file = save_audio(self.frames, self.sample_rate)
        transcription = transcribe_audio(temp_audio_file)

        # Copy transcription to clipboard
        if transcription:
            ic("\nTranscription:")
            ic(transcription)
            ic("Copying transcription to clipboard...")
            # copy_transcription_to_clipboard(transcription)
            ic("Transcription copied to clipboard and pasted into the application.")


            # Emit the transcription to the client
            socketio.emit('transcription_ready', {'transcription': transcription})

        else:
            print("Transcription failed.")

        # Clean up temporary file
        os.unlink(temp_audio_file)

'''





if __name__=="__main__":
    print("starting in playSignals")


    


