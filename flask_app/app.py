from flask import Flask, session, flash
from flask import render_template, redirect, url_for, request
import hashlib
from datetime import timedelta

# from film import Film
# from comment import Comment
from users import User

app = Flask(__name__)
app.secret_key = hashlib.sha256("project".encode('utf-8')).hexdigest()


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/')
def go_to():
    if "user" in session:
        return redirect(url_for("home"))
    else:
        return redirect(url_for('log_home'))


@app.route('/log_home')
def log_home():
    return render_template("Before_log.html")


@app.route('/home')
def home():
    return render_template("user.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = User.hash_password(request.form["password"])
        pass_rep = User.hash_password(request.form["psw-repeat"])
        if password == pass_rep:
            User(username, password).create()
            return redirect(url_for("log_home"))
        else:
            flash("The passwords do not match", "info")
            return render_template("register.html")

    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = User.find_by_username(request.form['username'])
        password = request.form['password']
        if user and user.verify_password(password):
            checkbox = request.form["remember"]
            if checkbox:
                session["user"] = checkbox
            return redirect(url_for("home"))
        else:
            flash("Wrong password!", "info")
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/<user>")
def usr(user):
    return User.find_by_username(user)


if __name__ == '__main__':
    app.run()
