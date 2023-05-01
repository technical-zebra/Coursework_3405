from flask import session, Blueprint
from flask_socketio import emit, join_room, leave_room
import socketio

# Created a Flask blueprint named `socket_features`. A blueprint is a way to
# organize related routes and functions in a Flask application.
socket_features = Blueprint('socket_features', __name__)


@socketio.on('begin quiz')
def test_message(message):
    """
    This function listens for a 'begin quiz' event and prints the message received, then emits a
    'redirect' event with the same message data to all connected clients.
    
    :param message: The parameter `message` is the data received from the client-side when the `begin
    quiz` event is triggered.
    """
    print(message)
    emit('redirect', {'data': message['data']}, broadcast=True)

@socketio.on('next quiz')
def test_message(message):
    """
    This function listens for a 'next quiz' event and upon receiving it, prints the message and emits a
    'redirect quiz' event with the same data to all connected clients.
    
    :param message: The parameter `message` is the data received from the client-side when the `next
    quiz` event is triggered.
    """
    print(message)
    emit('redirect quiz', {'data': message['data']}, broadcast=True)


@socketio.on('join hall')
def test_message(message):
    """
    This function listens for a 'join hall' event, prints the message received, and emits a 'new
    student' event with the same message data to all connected clients.
    
    :param message: The message parameter is the data that is sent from the client-side to the
    server-side when the 'join hall' event is triggered.
    """
    print(message)
    emit('new student', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect():
    """
    This function prints a message when a client connects and emits a response to the client.
    """
    print('Client connected')
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    """
    This function prints a message when a client disconnects from a socket.
    """
    print('Client disconnected')

@socketio.on('my_event')
def test_message(message):
    """
    This is a Python function that listens for a socket event called "my_event" and prints the message
    received from the event.
    
    :param message: The parameter "message" is the data that is being sent from the client-side to the
    server-side through a Socket.IO connection.\
    """
    print(message)


@socketio.on('my broadcast event')
def test_message(message):
    """
    This is a Python function that listens for a 'my broadcast event' socket event, and when triggered,
    emits a 'my response' event with the same data to all connected clients.
    
    :param message: The message parameter is the data that is received from the client-side when the 'my
    broadcast event' event is triggered.
    """
    emit('my response', {'data': message['data']}, broadcast=True)



