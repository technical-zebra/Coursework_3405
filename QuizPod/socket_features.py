from flask import session, Blueprint
from flask_socketio import emit, join_room, leave_room
from . import socketio

socket_features = Blueprint('socket_features', __name__)


@socketio.on('begin quiz')
def test_message(message):
    print(message)
    emit('redirect', {'data': message['data']}, broadcast=True)

@socketio.on('next quiz')
def test_message(message):
    print(message)
    emit('redirect quiz', {'data': message['data']}, broadcast=True)


@socketio.on('join hall')
def test_message(message):
    print(message)
    emit('new student', {'data': message['data']}, broadcast=True)

@socketio.on('my_event')
def test_message(message):
    print(message)


@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect')
def test_connect():
    print('Client connected')
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
