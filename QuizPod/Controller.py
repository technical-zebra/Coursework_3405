import json
import random
import time

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, logout_user, current_user

from Facade import db, current_students, current_sessions
from Model import Quiz

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    """
    This function returns the rendered template "index.html" with the current user's information for the
    home page, but only if the user is logged in.
    :return: The function `home()` is returning the rendered template "index.html" with the current user
    passed as a parameter.
    """
    return render_template("index.html", user=current_user)


@views.route('/go')
@login_required
def go():
    """
    This function is a route decorator that requires login authentication and renders an HTML template
    called "index.html" when the user navigates to the "/go" URL.
    :return: the rendered template "index.html" when the user navigates to the "/go" route, but only if
    the user is logged in (due to the @login_required decorator).
    """
    return render_template("index.html")


@views.route('/create_quiz', methods=['GET', 'POST'])
@login_required
def create_quiz():
    """
    This function creates a quiz by taking input from a form and adding it to a database.
    :return: a rendered HTML template "create_quiz.html" with the current user object passed as a
    parameter.
    """
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
    """
    This function displays a quiz page for a logged-in user, showing all available quizzes.
    :return: a rendered HTML template "display_quiz.html" with a list of all the quizzes in the database
    and the current user object.
    """
    # if request.method == 'GET':

    quizs = Quiz.query.all()
    return render_template("display_quiz.html", quizs=quizs, user=current_user)


@views.route('/run_quiz', methods=['GET', 'POST'])
def run_quiz():
    """
    This function generates a random session ID and redirects the user to the start session page.
    :return: a redirect to the 'start_session' view with the session_id as a parameter.
    """
    session_id = random.randint(20001, 40000)
    current_sessions.append(session_id)
    current_students = []
    ## return redirect(url_for('views.run_test', qid=0))
    return redirect(url_for('views.start_session', session_id=session_id))


@views.route('/start_session/<session_id>', methods=['GET', 'POST'])
def start_session(session_id):
    """
    This function renders a waiting hall template with the current user and session ID as parameters.
    
    :param session_id: The session_id parameter is a variable that is passed to the start_session
    function as an argument. It represents the unique identifier for a particular session.
    :return: a rendered HTML template called "waiting_hall.html" with the current user and session ID as
    parameters.
    """
    return render_template('waiting_hall.html', user=current_user, session_id=session_id)


@views.route('/run_test/<qid>', methods=['GET', 'POST'])
def run_test(qid):
    """
    This function renders a template to run a quiz with a specific ID and displays an error message if
    there are no questions in the database.
    
    :param qid: qid is the ID of the quiz that the user wants to run. It is passed as a parameter in the
    URL when the user clicks on a specific quiz to run.
    :return: a rendered HTML template 'run_quiz.html' with the quiz object and its length passed as
    arguments, and the current user object if available.
    """
    qid = int(qid)
    quizs = Quiz.query.all()
    if len(quizs) == 0:
        flash('No questions in database', category='error')
        return redirect(url_for('views.home'))
    return render_template('run_quiz.html', quiz=quizs[qid], length=len(quizs), user=current_user)


@views.route('/leaderboard')
def get_leaderboard():
    """
    This function retrieves the leaderboard data, sorts it in descending order, prints it, logs out the
    user, and renders the leaderboard template with the sorted data and current user.
    :return: a rendered HTML template called "leaderboard.html" with the variables "current_students"
    and "user" passed to it. The "current_students" variable is a dictionary that has been sorted in
    descending order based on the values of its items. The function also logs out the current user
    before rendering the template.
    """
    dict(sorted(current_students.items(), key=lambda item: item[1], reverse=True))
    print(current_students)
    logout_user()
    return render_template("leaderboard.html", current_students=current_students, user=current_user)


@views.route('/send-answer', methods=['POST'])
def send_answer():
    """
    This function receives a POST request with answer data, checks if the answer is correct, updates a
    dictionary of current students' scores, and returns an empty JSON response.
    :return: A JSON response with an empty object.
    """
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

    # new_answer = Answer(quiz_id=quiz_id, user_choice_id=ans, correctness=correctness)
    # db.session.add(new_answer)
    # db.session.commit()
    # print(new_answer)

    return jsonify({})


@views.route('/delete-quiz', methods=['POST'])
def delete_quiz():
    """
    This function deletes a quiz from the database if the quiz exists and is owned by the current user.
    :return: An empty JSON object.
    """
    quiz = json.loads(request.data)
    quiz_id = quiz['quizId']
    quiz = Quiz.query.get(quiz_id)
    if quiz:
        if quiz.user_id == current_user.id:
            db.session.delete(quiz)
            db.session.commit()

    return jsonify({})

