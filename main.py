from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:/Users/badge/OneDrive/Desktop/100-days-of-python/day 51 InternetSpeed/.env")

TMDB_API_JETON = os.getenv("TMDB_API_JETON")

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"



app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
Bootstrap5(app)

class Base(DeclarativeBase):
  pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE DB
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=True) 
    ranking: Mapped[int] = mapped_column(Integer, nullable=True)
    review: Mapped[str] = mapped_column(String(250), nullable=True)
    img_url: Mapped[str] = mapped_column(String(1000), nullable=False)

# CREATE TABLE
with app.app_context():
   db.create_all()



class UpdateForm(FlaskForm):
    rating = StringField(label='Your rating out of 10 e. g. 7.5', validators=[DataRequired()])
    review = StringField(label='Your Rewiew', validators=[DataRequired()])
    submit = SubmitField(label='Update')

class AddForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

def search_movie(title):
    header = {
        "Authorization": "Bearer {TMDB_API_JETON}"
    }
    response= requests.get(url=f'https://api.themoviedb.org/3/search/movie?query={title}', headers=header)
    data = response.json()["results"]
    return data


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))     
    all_movies = result.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)

@app.route("/update/<int:id>", methods=["POST","GET"])
def update(id):
    update_form = UpdateForm()
    movie_to_update = db.get_or_404(Movie, id)
    if update_form.validate_on_submit():
        movie_to_update.rating = float(update_form.rating.data)
        movie_to_update.review = update_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie_to_update, form=update_form)

@app.route("/delete")
def delete_movie():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["POST", "GET"])
def add_movie():
    form = AddForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        movies_data = search_movie(movie_title)

        return render_template("select.html", movies=movies_data)
    return render_template("add.html", form=form)

@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        response = requests.get(url=f'https://api.themoviedb.org/3/movie/{movie_api_id}', params={"api_key": TMDB_API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = Movie(
            title=data["title"],
            year=data["release_date"].split("-")[0],
            img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
            description=data["overview"],
            )
        db.session.add(new_movie)
        db.session.commit()
        movie_id = request.args.get("id")
        return redirect(url_for('update', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
