from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    __tablename__ = "user_account"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(250))
    type = db.Column(db.String(10))


    quizs = db.relationship('Quiz')


class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user_account.id"), nullable=False)
    content = db.Column(db.String(50))
    type = db.Column(db.String(50))
    answer_id = db.Column(db.Integer)
    choice_1_content = db.Column(db.String(50))
    choice_2_content = db.Column(db.String(50))
    choice_3_content = db.Column(db.String(50))
    choice_4_content = db.Column(db.String(50))


class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, ForeignKey("quiz.id"), nullable=False)
    student_id = db.Column(db.Integer, ForeignKey("student.id"), nullable=False)
    user_choice_id = db.Column(db.Integer)
    correctness = db.Column(db.Boolean)


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, ForeignKey("quiz.id"), nullable=False)
    student_name = db.Column(db.String(20))
    session_id = db.Column(db.String(6))
    answers = db.relationship('Answer')









