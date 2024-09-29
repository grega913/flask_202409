from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_socketio import SocketIO
import time
import threading
from icecream import ic


from AudioRecorder import AudioRecorder


from playground.recordin import save_audio, transcribe_audio
from login import valid_login, log_the_user_in
from ai.lesson7 import get_chain_with_message_history
from ai.test_persistence import get_chain_with_message_history_2, invoke_and_save


from routes import routes_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.register_blueprint(routes_blueprint)

socketio = SocketIO(app)


ar = AudioRecorder(socketio=socketio)








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