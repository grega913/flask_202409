from flask import Flask, redirect, url_for, request, render_template, jsonify
from flask_socketio import SocketIO
from icecream import ic

from AudioRecorder import AudioRecorder

from routes import routes_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.register_blueprint(routes_blueprint)




socketio = SocketIO(app)


ar = AudioRecorder(socketio=socketio)

@socketio.on('pDown')
def record(event):
    ic("pDown: " + str(event))
    ar.start_recording()

@socketio.on("pUp")
def stopRec(event):
    ar.stop_recording()


socketio.run(app, debug=True, use_reloader=True)






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