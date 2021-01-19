from flask import Flask, flash, session
from flask import render_template, redirect, url_for, request
import os
import logging

from film import Film
from comment import Comment
from users import User
from ratings import Rating

app = Flask(__name__)
app.secret_key = os.urandom(12)

logFormatStr = "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
logging.basicConfig(format=logFormatStr, filename="global.log", level=logging.DEBUG)
formatter = logging.Formatter(logFormatStr, "%m-%d %H:%M:%S")
fileHandler = logging.FileHandler("flask-app.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)
app.logger.addHandler(streamHandler)
app.logger.info("Logging is set up.")


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
                app.logger.info("'%s' wants to register again!", username)
                flash("There is already a person with such a name, please choose another")
                return render_template("register.html")
            else:
                User(None, username, password).create()
                app.logger.info("'%s' registered successfully!", username)
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
            app.logger.info("'%s' logged in successfully", user.username)
            return redirect(url_for("home"))
        else:
            app.logger.warn("'%s' is NOT logged!", user.username)
            flash("Wrong username or password!", "info")
            return render_template("login.html")
    elif request.method == "GET":
        return render_template("login.html")


@app.route("/log_out")
def log_out():
    if "usr" in session:
        app.logger.info("'%s' logged out", session["usr"])
        session.pop("usr", None)
        if "log" in session:
            session.pop("log")
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("films.html", films=Film.all(),
                           usr=None)


@app.route("/profile")
def profile():
    if "usr" not in session:
        return redirect(url_for("go_to"))
    return render_template("films.html", films=Film.films_by_author(session["usr"]),
                           usr=session["usr"])


@app.route("/profile/add_film", methods=["GET", "POST"])
def add_film():
    if "usr" not in session:
        return redirect(url_for("go_to"))
    if request.method == "GET":
        return render_template("add_film.html")
    elif request.method == "POST":
        film_name = request.form["film_name"]
        film_content = request.form["film_content"]
        film = Film(*(None, film_name, session["usr"], film_content)).create()
        app.logger.debug("Film with id '%s' is created", film.film_id)
        return redirect(url_for("home"))


@app.route("/home/<int:film_id>")
def show_film(film_id):
    if "usr" not in session:
        flash("To see film content - please login!")
        return redirect(url_for("go_to"))
    film = Film.find(film_id)
    return render_template("film.html", film=film, edit=session["usr"])


@app.route("/home/<int:film_id>/delete", methods=["POST"])
def delete_film(film_id):
    film = Film.find(film_id)
    app.logger.debug("Film with id '%s' is deleted", film_id)
    film.delete()
    return redirect(url_for("home"))


@app.route("/new_comment", methods=["POST"])
def new_comment():
    film = Film.find(request.form["film_id"])
    user = session["usr"]
    Comment(*(None, request.form["message"], user, film)).create()
    app.logger.info("'%s' add a comment to the film '%s'", session["usr"], film.name)
    return redirect(url_for("show_film", film_id=film.film_id))


@app.route("/home/<int:film_id>/edit", methods=["GET", "POST"])
def edit_film(film_id):
    film = Film.find(film_id)
    if request.method == "GET":
        return render_template("add_film.html", film=film)
    elif request.method == "POST":
        film.name = request.form["film_name"]
        film.content = request.form["film_content"]
        film.save()
        app.logger.debug("Film with id '%s' edited", film.film_id)
        return redirect(url_for("show_film", film_id=film.film_id))


@app.route("/ratings/")
def ratings():
    if "usr" not in session:
        return redirect(url_for("go_to"))
    films = Film.film_ratings()
    return render_template("ratings.html", film=films)


@app.route("/ratings/<int:film_id>", methods=["GET", "POST"])
def rate_film(film_id):
    current_film = Film.find(film_id)
    if request.method == "GET":
        return render_template("rate.html", film=current_film)
    elif request.method == "POST":
        rate = request.form["rate"]
        try:
            if int(rate) > 5 or int(rate) < 0:
                flash("Please insert rating between 0 and 5!")
                return render_template("rate.html", film=current_film)
        except Exception:
            flash("Please insert rating between 0 and 5!")
            return render_template("rate.html", film=current_film)
        Rating.create(rate, film_id)
        app.logger.info("'%s' add a rating to the film '%s'", session["usr"], current_film.name)
    return redirect(url_for("ratings"))


if __name__ == "__main__":
    app.run()
