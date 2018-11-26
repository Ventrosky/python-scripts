import os
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = b'>\xb7\xaff\xef\xa8\xd3\xce|A\xd29\xfe\xe92\xf3\xfc\xd4\x93\xbc\xb8|\x19\x0e'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('received message')

@socketio.on('send message')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received sent: ' + str(json))
    socketio.emit('message text', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)