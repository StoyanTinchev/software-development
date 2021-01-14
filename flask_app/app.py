from flask import Flask, flash, session
from flask import render_template, redirect, url_for, request
import os

from film import Film
from comment import Comment
from users import User

app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.route('/')
def go_to():
    if "usr" in session:
        user = session["usr"]
        if User.validate_username(user):
            return redirect(url_for("home"))
    session['log'] = False
    return redirect(url_for("log_home"))


@app.route('/log_home')
def log_home():
    if session["log"]:
        return redirect(url_for("home"))
    session['log'] = False  # because log_out redirect us here and session 'log' popped
    return render_template("films.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if session["log"]:
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form["username"]
        password = User.hash_password(request.form["password"])
        pass_rep = User.hash_password(request.form["psw-repeat"])
        if password == pass_rep:
            if User.find_by_username(username):
                flash("There is already a person with such a name, please choose another")
                return render_template("register.html")
            else:
                User(None, username, password).create()
            return redirect(url_for("log_home"))
        else:
            flash("The passwords do not match", "info")
            return render_template("register.html")

    else:
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if session["log"]:
        return redirect(url_for("home"))

    if request.method == "POST":
        user = User.find_by_username(request.form['username'])
        password = User.hash_password(request.form["password"])
        if user and user.verify_password(password):
            checkbox = request.form.get("remember")
            session['log'] = True
            if checkbox is not None:
                session['usr'] = request.form['username']
            return redirect(url_for("home"))
        else:
            flash("Wrong username or password!", "info")
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/log_out")
def log_out():
    if 'usr' in session:
        session.pop('log', None)
        session.pop('usr', None)
    return redirect(url_for("log_home"))


@app.route('/home')
def home():
    return render_template("films.html", films=Film.all())


if __name__ == '__main__':
    app.run()
