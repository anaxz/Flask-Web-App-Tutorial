from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # you can get input like this instead of event listener js
        email = request.form.get('email')
        password = request.form.get('password')

        # filter_by -> filter all users that have that email and return the frist result
        user = User.query.filter_by(email=email).first()
        if user:
            # hash pass and check the from pass
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                # param(user, remebers user has been logged in)
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    #user=current_user -> ref user and check if authenticated
    #this is used to display logout btn or not etc
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #check email doesn't already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #sha256 -> hashing algorithm type
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            # add new user to db
            db.session.add(new_user)
            # update changes to db
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            #'views.home' -> views file, home func
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

## can flash a message on screen with flask
# category can be nameed whatever you want

#a@gmail.com
#tester123