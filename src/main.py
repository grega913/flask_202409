from flask import Flask, redirect, url_for, request, render_template
from flask_socketio import SocketIO
import time
import threading
from icecream import ic
import os
from markupsafe import escape
from flask_bcrypt import Bcrypt
from groq import Groq
import pyaudio

from recordin import save_audio, transcribe_audio

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)



from login import valid_login, log_the_user_in

client = Groq()


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
            #socketio.emit('transcription_ready', {'transcription': transcription})
           
            socketio.emit('readTrans', {'transcription': transcription})
        else:
            print("Transcription failed.")

        # Clean up temporary file
        os.unlink(temp_audio_file)



ar = AudioRecorder()


@app.route('/index')
def index():
    return render_template('/index.html')



@app.route('/chat')
def chat():
    return render_template('/chat.html') 



@app.route('/chat', methods=['POST', 'GET'])
def handle_button_click():

    if request.method == 'POST':

        button_name = request.form['button']

        if button_name == 'button1':
            # Function for Button 1
            print("Button 1 clicked!")
            # Perform actions specific to Button 1
        elif button_name == 'button2':
            # Function for Button 2
            print("Button 2 clicked!")
            # Perform actions specific to Button 2
        elif button_name == 'button3':
            # Function for Button 3
            print("Button 3 clicked!")
            # Perform actions specific to Button 3
        else:
            print("Invalid button pressed.")

    # Return the template to keep the page visible
    return render_template('chat.html')

# variable routes
@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route('/hello')
def hello(name=None):
    return render_template('hello.html', name=name)



def show_the_login_form(name=None):
    return render_template("/hello.html", name = name)


def do_the_login():
    return render_template("/chat.html")

@app.route('/button_clicked', methods=['POST'])
def button_clicked():

    if request.method=="POST":
        print("button_clicked")
        return "This was Post"

    print("this is get")
    return 'Button clicked!'














# end route



# SOCKET IO #

@socketio.on('my_event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


def print_time():

    while True:
        print(time.strftime("%H:%M:%S"))
        socketio.emit('emitFromPy', {'time in python': time.strftime("%H:%M:%S")})
        time.sleep(1)

# Start the function in a separate thread



@socketio.on('pDown')
def record(event):
    ic("pDown: " + str(event))
    ar.start_recording()

@socketio.on("pUp")
def stopRec(event):
    ar.stop_recording()









if __name__ == '__main__':
    ''' 
    thread2 = threading.Thread(target=print_time)
    thread2.daemon = True  # So the thread dies when the main program terminates
    thread2.start()
    '''
    '''
    record_thread = threading.Thread(target=record_main)
    record_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits
    record_thread.start()
    '''

    socketio.run(app, debug=True, use_reloader=True)