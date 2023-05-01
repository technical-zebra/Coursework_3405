from QuizPod.Facade import create_app, socketio

# Creating a Flask application instance with debugging enabled.
app = create_app(debug=True)

if __name__ == '__main__':
   # running the Flask application with Socket.IO support.
    socketio.run(app)
