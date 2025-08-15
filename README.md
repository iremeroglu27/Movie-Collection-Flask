# Movie Collection Flask App

A Flask web application to manage your movie collection using **TMDb API**. Users can add movies, update ratings and reviews, and delete movies from their collection.

---

## Features

- Add movies by searching via TMDb API  
- View all movies in your collection  
- Update movie ratings and reviews  
- Delete movies from the collection  
- Automatic ranking of movies based on ratings  

---

## Tech Stack

- **Python 3**  
- **Flask**  
- **Flask-Bootstrap5** for UI  
- **SQLAlchemy** for database management  
- **WTForms** for forms  
- **Requests** for TMDb API integration  

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/movie-collection-flask.git
cd movie-collection-flask
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```
3.Install dependencies:

```bash
pip install -r requirements.txt
```
4.Create a .env file with the following variables:

```ini
SECRET_KEY=your_flask_secret_key
TMDB_API_KEY=your_tmdb_api_key
```
5.Run the application:

```bash
python main.py
```
6.Open http://127.0.0.1:5000/ in your browser.

## Usage
- Add a Movie: Enter the movie title and select the correct result from TMDb.

- Update a Movie: Click "Update" to modify rating and review.

- Delete a Movie: Click "Delete" to remove it from your collection.

## Notes
- .env file contains your secret keys and should never be shared publicly.

- The app uses TMDb API; you need to create an account to get an API key.
