from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from .model import Quiz, User, Answer
from . import db, current_students, current_sessions
from flask_login import login_user, login_required, logout_user, current_user
import json
import time
import random

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("index.html", user=current_user)


@views.route('/go')
@login_required
def go():
    return render_template("index.html")


@views.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    if request.method == 'POST':

        question = request.form.get('question')
        quiz_mode = request.form.get('QuizMode')
        if quiz_mode == "MutiChoices":
            choice1 = request.form.get('choice1')
            choice2 = request.form.get('choice2')
            choice3 = request.form.get('choice3')
            choice4 = request.form.get('choice4')
        else:
            choice1 = request.form.get('choice1')
            choice2 = request.form.get('choice2')
            choice3 = ""
            choice4 = ""

        answer = request.form.get('answer')

        if len(question) < 3:
            flash('Question should be at least 3 characters', category='error')

        elif answer != "1" and answer != "2" and answer != "3" and answer != "4":
            flash('Answer should be "1" or "2" or "3" or "4"', category='error')

        elif quiz_mode != "MutiChoices" and quiz_mode != "TrueOrFalse":
            flash('Please give a valid quiz mode', category='error')

        else:
            new_quiz = Quiz(user_id=current_user.id, content=question, type=quiz_mode, answer_id=answer,
                            choice_1_content=choice1,
                            choice_2_content=choice2, choice_3_content=choice3, choice_4_content=choice4)
            db.session.add(new_quiz)
            db.session.commit()

            flash('Quiz created!', category='pass')
            print("Quiz created!")

        # print(f"{question} \n{quiz_mode} \n{choice1} \n{choice2} \n{choice3} \n{choice4} \n{answer}")

    return render_template("create_quiz.html", user=current_user)


@views.route('/display_quiz', methods=['GET', 'POST'])
@login_required
def display_quiz():
    # if request.method == 'GET':

    quizs = Quiz.query.all()
    return render_template("display_quiz.html", quizs=quizs, user=current_user)


@views.route('/run_quiz', methods=['GET', 'POST'])
def run_quiz():
    session_id = random.randint(20001, 40000)
    current_sessions.append(session_id)
    current_students = []
    ## return redirect(url_for('views.run_test', qid=0))
    return redirect(url_for('views.start_session', session_id=session_id))

@views.route('/start_session/<session_id>', methods=['GET', 'POST'])
def start_session(session_id):
    return render_template('waiting_hall.html', user=current_user, session_id=session_id)

@views.route('/run_test/<qid>', methods=['GET', 'POST'])
def run_test(qid):
    qid = int(qid)
    quizs = Quiz.query.all()
    if len(quizs) == 0:
        flash('No questions in database', category='error')
        return redirect(url_for('views.home'))
    return render_template('run_quiz.html', quiz=quizs[qid], length=len(quizs), user=current_user)



@views.route('/leaderboard')
def get_leaderboard():
    dict(sorted(current_students.items(), key=lambda item: item[1], reverse=True))
    print(current_students)
    logout_user()
    return render_template("leaderboard.html", current_students=current_students, user=current_user)



@views.route('/send-answer', methods=['POST'])
def send_answer():
    content = json.loads(request.data)
    ans = content['ans']
    quiz_id = content['quizId']
    nickname = content['nickname']
    quiz = Quiz.query.filter_by(id=quiz_id).first()
    print(quiz)
    print(ans)
    if ans == 0:
        correctness = False;
        print(f"ans:{ans} correctness:{correctness}")
    else:
        example_ans = quiz.answer_id
        correctness = False;
        if ans == example_ans:
            correctness = True
            current_students[nickname] += 1
        print(f"ans:{ans}  ex_ans:{example_ans} correctness:{correctness}")

    #new_answer = Answer(quiz_id=quiz_id, user_choice_id=ans, correctness=correctness)
    #db.session.add(new_answer)
    #db.session.commit()
    #print(new_answer)

    return jsonify({})


@views.route('/delete-quiz', methods=['POST'])
def delete_quiz():
    quiz = json.loads(request.data)
    quiz_id = quiz['quizId']
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        if quiz.user_id == current_user.id:
            db.session.delete(quiz)
            db.session.commit()

    return jsonify({})


def countdown(t):
    while t:
        mins = t // 60
        secs = t % 60
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print('Blast off!!!')
    t = input("Enter the time in seconds: ")
    countdown(int(t))

