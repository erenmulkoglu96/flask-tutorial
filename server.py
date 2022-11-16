import os
from db_init import initialize

from flask import Flask, redirect, url_for, render_template, request, Blueprint
from psycopg2 import extensions
from queries import *

extensions.register_type(extensions.UNICODE)
extensions.register_type(extensions.UNICODEARRAY)

app = Flask(__name__)

HEROKU = True

if(not HEROKU): 
    os.environ['DATABASE_URL'] = "dbname='postgres' user='postgres' host='localhost' password='eren157123'"
    initialize(os.environ.get('DATABASE_URL'))

@app.route("/")
def home_page():
    return render_template("home_page.html")

@app.route("/movies", methods=['GET','POST'])
def movies_page():
    if request.method == "GET":
        movies = select("id,name,likes,dislikes,image","movie",asDict=True)
        return render_template("movies.html", movies = movies)
    elif request.method == "POST":
        if "like" in request.form:
            update("movie","likes=likes+1","id={}".format(request.form.get('like')))
        elif "dislike" in request.form:
            update("movie","dislikes=dislikes+1","id={}".format(request.form.get('dislike')))
        return redirect(url_for('movies_page'))         


@app.route("/movies/<id>")
def movie_detail_page(id):
    movie = select("name,image","movie","id={}".format(id),asDict=True)
    actors = select("actor.name,actor.likes,actor.dislikes,actor.image",
    "actor join index on actor.id=index.actor_id","index.movie_id={}".format(id),asDict=True)
    return render_template("movie_detail_page.html", movie=movie, actors=actors)



@app.route("/actors", methods=['GET','POST'])
def actors_page():
    if request.method == "GET":
        actors = select("id,name,likes,dislikes,image","actor",asDict=True)
        return render_template("actors.html", actors = actors)
    elif request.method == "POST":
        if "like" in request.form:
            update("actor","likes=likes+1","id={}".format(request.form.get('like')))
        elif "dislike" in request.form:
            update("actor","dislikes=dislikes+1","id={}".format(request.form.get('dislike')))
        return redirect(url_for('actors_page'))         


@app.route("/actors/<id>")
def actor_detail_page(id):
    actor = select("name,image","movie","id={}".format(id),asDict=True)
    movies = select("movie.name,movie.likes,movie.dislikes,movie.image",
    "movie join index on movie.id=index.movie_id","index.actor_id={}".format(id),asDict=True)
    return render_template("actor_detail_page.html", movies=movies, actor=actor)




if  __name__ == "__main__":
    if(not HEROKU):
        app.run(debug = True)
    else:
        app.run()

