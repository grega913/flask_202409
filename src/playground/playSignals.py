
import time
from icecream import ic
import threading
import tempfile
import wave
import pyaudio
import keyboard                         
import pyautogui
import pyperclip

import pyaudio



def save_audio(frames, sample_rate):
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
        print(f"An error occurred: {str(e)}")
        return None


class AudioRecorder():

    def __init__(self, sample_rate = 44100, channels=1, chunk=1024, ):
        print("init")
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk = chunk
        self.transcription = None



    def start_recording(self):

        print("start recording")
        self.stream = self.p.open(format=pyaudio.paInt16,
                                channels=self.channels,
                                rate=self.sample_rate,
                                input=True,
                                frames_per_buffer=self.chunk)
        
        print("Recording started...")

        data = self.stream.read(self.chunk)
        self.frames.append(data)


    def stop_recording(self):
        print("stop recording")

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
            print("Recording stopped...")

            temp_audio_file = save_audio(self.frames, self.sample_rate)
            self.transcription = transcribe_audio(temp_audio_file)

            print(self.transcription)


        else:
            print("No recording is in progress.")

    def __del__(self):
        print("delete recorder")
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
        if self.transcription:
            # Clean up any resources associated with the transcription
            self.transcription = None
            pass



def rec():
    print("rec")
    recorder = AudioRecorder()
    recorder.start_recording()

    time.sleep(3)
    recorder.stop_recording()



if __name__=="__main__":
    print("starting in playSignals")
    rec()

    


