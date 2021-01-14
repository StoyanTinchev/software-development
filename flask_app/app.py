from flask import Flask, flash, session
from flask import render_template, redirect, url_for, request
import os

from film import Film
from comment import Comment
from users import User

app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.route("/")
def go_to():
    if "usr" in session:
        if "log" in session:
            return redirect(url_for("home"))
        else:
            session.pop("usr", None)
    return redirect(url_for("home"))


@app.route("/register", methods=["POST", "GET"])
def register():
    if "usr" in session:
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
            return redirect(url_for("home"))
        else:
            flash("The passwords do not match", "info")
            return render_template("register.html")

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if "usr" in session:
        return redirect(url_for("home"))

    if request.method == "POST":
        user = User.find_by_username(request.form["username"])
        password = User.hash_password(request.form["password"])
        if user and user.verify_password(password):
            checkbox = request.form.get("remember")
            session["usr"] = request.form["username"]
            if checkbox is not None:
                session["log"] = True
            return redirect(url_for("home"))
        else:
            flash("Wrong username or password!", "info")
            return render_template("login.html")
    elif request.method == "GET":
        return render_template("login.html")


@app.route("/log_out")
def log_out():
    if "usr" in session:
        session.pop("usr", None)
        if "log" in session:
            session.pop("log")
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("films.html", films=Film.all(), usr=None)


@app.route("/profile")
def profile():
    if "usr" not in session:
        return redirect(url_for(go_to))
    return render_template("films.html", films=Film.films_by_author(session["usr"]), usr=session["usr"])


@app.route("/profile/add_film", methods=["GET", "POST"])
def add_film():
    if "usr" not in session:
        return redirect(url_for(go_to))
    if request.method == "GET":
        return render_template("add_film.html")
    elif request.method == "POST":
        film_name = request.form["film_name"]
        film_content = request.form["film_content"]
        Film(*(None, film_name, session['usr'], film_content)).create()
        return redirect(url_for("home"))


@app.route("/home/<int:film_id>")
def show_film(film_id):
    if "usr" not in session:
        return redirect(url_for("go_to"))
    film = Film.find(film_id)

    return render_template("film.html", film=film)


if __name__ == "__main__":
    app.run()
