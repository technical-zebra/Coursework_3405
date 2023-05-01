from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO

from .Controller import views
from .AuthController import auth
from .Model import User, Quiz
from .SocketController import socket_features

# - `socketio` is an instance of the `SocketIO` class, which is used for handling real-time
# communication between the server and clients.
socketio = SocketIO()

# - `db` is an instance of the `SQLAlchemy` class, which is used for database management.
db = SQLAlchemy()

# - `DB_NAME` is a string variable that holds the name of the database file.
DB_NAME = "database.db"

# - `current_students` is an empty dictionary that will be used to store information about currently
# connected students.
current_students = {}

# - `current_sessions` is an empty list that will be used to store information about currently active
# quiz sessions.
current_sessions = []


def create_app(debug=False):
    """
    This function creates a Flask application with various configurations and blueprints for views,
    authentication, and sockets.
    
    :param debug: A boolean value that determines whether the application is in debug mode or not.
    """
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = '1MAN3PyxZVi8kSWoz0Iv'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))
    
    app.register_blueprint(socket_features)

    socketio.init_app(app)
    return app


def create_database(app):
    """
    This function creates a database if it does not already exist.
    
    :param app: The app parameter is an instance of a Flask application. It is used to create the
    database tables using the SQLAlchemy ORM.
    """
    if not path.exists('QuizPod/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')
