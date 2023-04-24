from flask import Blueprint, render_template, url_for, request, session, redirect, flash
from flask_login import login_required, current_user
import requests
from . import db

views = Blueprint('views', __name__)


@views.route('/')
def home():
    data = requests.get("https://www.omdbapi.com/?i=tt3896198&apikey=11fcd31b&s=creed")
    movies = data.json()
    return render_template("home.html", user=current_user, movies=movies)


@views.route('/shelf')
@login_required
def shelf():
    data = requests.get("https://www.omdbapi.com/?i=tt3896198&apikey=11fcd31b&s=avengers")
    movies = data.json()
    return render_template("shelf.html", user=current_user, movies=movies)


@views.route('/genres')
def geners():
    return render_template("genres.html", user=current_user)


@views.route('/movieDescription/<title>')
@login_required
def movieDescription(title):
    data = requests.get("https://www.omdbapi.com/?i=tt3896198&apikey=11fcd31b&t=" + title)
    movie = data.json()
    return render_template("movieDescription.html",user=current_user, movie=movie)


@views.route('/results', methods=["POST"])
def search_by_title():
    title = request.form["title"]
    data = requests.get("https://www.omdbapi.com/?i=tt3896198&apikey=11fcd31b&s=" + title)
    movies = data.json()
    return render_template("results.html",user=current_user, movies=movies)


@views.route('/favourite_list')
@login_required
def favourite_list():
    favourite_list = session.get("favourite")

    if favourite_list == None:
        flash("The favourite list is empty !")
        return redirect(url_for("views.shelf"))
    else:
        return render_template("favourites.html", user=current_user, favourite_list=favourite_list)


def search_by_title_two(title):
    data = requests.get("https://www.omdbapi.com/?i=tt3896198&apikey=11fcd31b&s=" + title)
    movies = data.json()
    return render_template("favourites.html", user=current_user, movies=movies)


@views.route('add_to_favourite/<title>')
def add_to_favourite(title):
    favourite_list = {}
    if "favourite" in session:
        favourite_list = session.get("favourite") 
    else:
        session["favourite"] = {}
    favourite_list[title] = title
    session["favourite"] = favourite_list
    flash("Added to favourites list !")
    favourite_list = []
    return redirect(url_for("views.shelf"))


@views.route('/delete_from_list/<title>')
def delete_from_list(title):
    favourite_list = session.get("favourite")
    favourite_list.pop(title, None)
    session["favourite"] = favourite_list
    return redirect(url_for("views.favourite_list"))