from flask import Blueprint, redirect, url_for, request, render_template
from flask_login import (
    current_user, login_required,
    login_user, logout_user,
)
from .User import User

views = Blueprint('views', __name__)

@views.get("/")
def index():
    username = "anonymous"
    if current_user.is_authenticated:  # type: ignore
        username = current_user.username  # type: ignore
    return f"""
        <h1>Hi {username}</h1>
        <h3>Welcome to Flask Login without ORM!</h3>
    """

@views.route('/home')
@login_required
def home():
    #user=current_user -> ref user and check if authenticated
    #this is used to display logout btn or not etc
    return render_template("views.home", user=current_user)

# @views.route('/login2', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # you can get input like this instead of event listener js
#         email = request.form.get('email')
#         password = request.form.get('password')

#     #user=current_user -> ref user and check if authenticated
#     #this is used to display logout btn or not etc
#     return render_template("login.html", user=current_user)

@views.get("/login/<id>/<password>")
def login(id, password):
    user = User.get(id)
    print(user)
    if user and user.password == password:
        login_user(user)
        return redirect(url_for("views.home"))
    return "<h1>Invalid user id or password</h1>"


@views.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.login"))

##----
@views.get("users/<id>")
def users(id):
    user = User.get(id)
    return f"{user.id}, {user.email}, {user.password}"