from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO

socketio = SocketIO()

db = SQLAlchemy()
DB_NAME = "database.db"
current_students={}
current_sessions=[]

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = '1MAN3PyxZVi8kSWoz0Iv'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .model import User, Quiz

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .socket_features import socket_features
    app.register_blueprint(socket_features)

    socketio.init_app(app)
    return app


def create_database(app):
    if not path.exists('QuizPod/' + DB_NAME):
        db.create_all(app=app)
        print('Created database!')