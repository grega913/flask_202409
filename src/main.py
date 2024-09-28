from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_socketio import SocketIO
import time
import threading
from icecream import ic
import os
from markupsafe import escape
from flask_bcrypt import Bcrypt
from groq import Groq
import pyaudio
import json
from helperz import add, subtract, process_text, append_record
from AudioRecorder import AudioRecorder

import random
from datetime import datetime






from playground.recordin import save_audio, transcribe_audio
from login import valid_login, log_the_user_in

from ai.lesson7 import get_chain_with_message_history

from data.various import mock_json


app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

ar = AudioRecorder(socketio=socketio)
chain_with_message_history = get_chain_with_message_history()

@app.route('/')
def index():
    return render_template('/index.html')


@app.route('/chat')
def chat():
    return render_template('/chat.html') 


@app.route('/chat', methods=['POST', 'GET'])
def handle_button_click():

    if request.method == 'POST':
        ic("post method in handle_button_click")
        
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



@app.route('/read_input', methods=['POST', 'GET'])
def read_input():
    if request.method=="POST":
        return str(add(5,6))
    
@app.route('/send_text', methods=['POST'])
def send_text():
    text = request.form['text']
    # Call your Python function here
    process_text(text)
    return str(text)


@app.route('/mock')
def mock():
  return render_template('mock.html', data=mock_json)


@app.route('/user_message', methods=['POST'])
def user_message():
    if request.method == "POST":
        user_input = request.form['user_input']





        # Call your AI function here to generate a response based on the user's input
        ic(user_input)
        mock_json_new = append_record(mock_json)
        time.sleep(0.2)
        ic(mock_json_new)
        return render_template('mock.html', data=mock_json_new)
    
    else:
        return "Kr neki"



@app.route('/ai')
def ai():
  return render_template('ai.html')


@app.route('/api/datapoint2', methods= ['POST'])
def api_datapoint2():
    ic("api_datapoint2")

    user_input = request.get_json()['user_input']
    ic(user_input)

    
    response = chain_with_message_history.invoke(
         {"input": user_input},
         {"configurable": {"session_id": "abc123"}},
    )

    ic(response)
    content = response.content
    return content





@app.route('/ena')
def ena():
  return render_template('temp1.html')

@app.route('/api/datapoint')
def api_datapoint():

    ic(api_datapoint)

    random_number = random.randint(1, 100)
    double_random_number = random_number * 2
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    dictionary_to_return = {
        'random_number': random_number,
        'double_random_number': double_random_number,
        'timestamp': timestamp
    }

    return jsonify(dictionary_to_return)


        




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