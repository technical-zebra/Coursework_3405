from flask import Blueprint, render_template, request, flash, redirect, url_for
from Model import User
from werkzeug.security import generate_password_hash, check_password_hash
from Facade import db, current_students, current_sessions
from flask_login import login_user, login_required, logout_user, current_user

# Creates a Blueprint object named "auth" that is used to define
# a set of related routes and views for user authentication.
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the login process by checking the user's email and password, and if they
    match, logs the user in and redirects them to the home page.
    :return: a rendered template of "login.html" with the current user object passed as an argument.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Login successfully!', category='pass')
                login_user(user, remember=True)
                print("Login successfully!")
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('User does not exist!', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
    This function logs out the user and redirects them to the login page.
    :return: a redirect to the login page of the authentication blueprint.
    """
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    This function handles the registration process for a user, checking for valid email and password
    requirements before creating a new user account.
    :return: the rendered template "register.html" with the current user object passed as an argument.
    If all correct, a new user is created and the user is redirected to the home page.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        ## requirement for email ##
        elif email.find('@') == -1:
            flash('Email must contain @', category='error')
        elif len(email) < 5:
            flash('Email must at least 5 characters', category='error')

        # ## requirement for firstname ##
        # elif len(first_name) < 2:
        #     flash('Username must at least 2 characters', category='error')
        #
        # ## requirement for lastname ##
        # elif len(last_name) < 2:
        #     flash('Username must at least 2 characters', category='error')

        ## requirement for password ##
        elif len(password) < 8:
            flash('password should be at least 8 characters', category='error')
        elif len(password) > 20:
            flash('password should be no more than 20 characters', category='error')
        elif not any(char.isdigit() for char in password):
            flash('password should have at least one numeral', category='error')
        elif not any(char.isupper() for char in password):
            flash('Password should have at least one uppercase letter', category='error')
        elif not any(char.islower() for char in password):
            flash('Password should have at least one lowercase letter', category='error')

        # ## requirement for confirm password ##
        # elif password1 != password2:
        #     flash('Confirm password should be same with password', category='error')

        ## success message ##
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'), type="teacher")
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='pass')
            return redirect(url_for('views.home'))

    return render_template("register.html", user=current_user)

@auth.route('/join_quiz/', methods=['GET', 'POST'])
def join_quiz():
    """
    This function allows a student to join a quiz session by providing a session ID and a nickname, and
    performs some validation checks before adding the student to the current session and creating a new
    user in the database.
    :return: a messsage if fail, redirect to quiz if success.
    """
    if request.method == 'POST':
        session_id = int(request.form.get('session_id'))
        nickname = request.form.get('nickname')

        if session_id not in current_sessions:
            print(current_sessions)
            print(type(session_id))
            flash('Session not exists!', category='error')
        elif nickname in current_students.keys():
            flash('Student already exists!', category='error')
        elif len(nickname) < 3:
            flash('nickname should be at least 3 characters', category='error')
        else:
            current_students[nickname] = 0
            new_student = User(email=f"{nickname}@student", password=None, type="student")
            db.session.add(new_student)
            db.session.commit()
            login_user(new_student, remember=False)
            return redirect(url_for('views.start_session', session_id=session_id))

    return render_template("join_quiz.html", user=current_user)