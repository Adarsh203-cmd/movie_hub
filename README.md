
# Movie Management System

## Overview
The Movie Management System is a Django-based application designed for managing movies, genres, and associated personnel (such as actors, directors, and technicians). It provides functionalities to list, create, update, and delete movies, manage genres, and handle people associated with movies.

This system offers RESTful APIs that allow users to interact with the database, including features like searching for movies by their title, genres, and the people associated with them.

## Features
- **Movie Management**: Create, update, delete, and retrieve movie details.
- **Genre Management**: Manage movie genres (action, drama, comedy, etc.).
- **People Management**: Manage roles like Actor, Director, and Technician.
- **Search and Filter**: Search for movies by title, genre, or people (actor, director, technician).
- **Pagination**: Paginate the list of movies to enhance user experience for large datasets.

## Technologies Used
- **Django**: The web framework for building the application.
- **Django REST Framework**: To build the REST APIs for the Movie Management System.
- **PostgreSQL**: Database used for storing movie data, genres, and personnel.
- **Python**: Programming language used for development.

## Setup

### Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- PostgreSQL (for database management)
- Django (>=5.1)
- Django REST Framework (>=3.14)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd movie_management
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Setup PostgreSQL Database:
   - Create a new PostgreSQL database.
   - Update the `DATABASES` settings in `settings.py` with your PostgreSQL configuration.

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at:
   ```bash
   http://127.0.0.1:8000/
   ```

## API Endpoints

## API Testing with Postman

After deploying the app, you can test the API endpoints using **Postman**.

- **Install Postman**: Download it from [Postman Download](https://www.postman.com/downloads/).
- **Test Endpoints**: Use Postman to make requests to your API endpoints.

### Movies
- **GET** `/movies/`: Retrieve a list of all movies (supports pagination and filters).
- **POST** `/movies/`: Create a new movie.
- **GET** `/movies/{id}/`: Retrieve a movie by its ID.
- **PUT** `/movies/{id}/`: Update a movie's details.

### People (Actors, Directors, Technicians)
- **POST** `/actors/{id}/delete/`: Delete an actor (if not associated with any movies).

## Models

### Genre
Represents a genre of a movie (e.g., Action, Comedy, Drama).

```python
class Genre(models.Model):
    genre_name = models.CharField(max_length=100, unique=True)
```

### Person
Represents a person involved in the movie (e.g., Actor, Director, Technician).

```python
class Person(models.Model):
    full_name = models.CharField(max_length=150)
    role_type = models.CharField(choices=[('Actor', 'Actor'), ('Director', 'Director'), ('Technician', 'Technician')])
```

### Movie
Represents a movie, including its title, release year, rating, genres, and associated people.

```python
class Movie(models.Model):
    movie_title = models.CharField(max_length=200)
    release_year = models.PositiveIntegerField()
    average_user_rating = models.FloatField()
    genres = models.ManyToManyField(Genre)
    associated_people = models.ManyToManyField(Person)
```

## Example Requests

### Get Movies
```bash
GET /movies/?search=action
```

### Create Movie
```bash
POST /movies/
{
    "movie_title": "The Matrix",
    "release_year": 1999,
    "average_user_rating": 8.7,
    "genres": [1, 2],
    "associated_people": [1, 2]
}
```

