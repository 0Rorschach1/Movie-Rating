from sqlalchemy.orm import Session
from app.models.models import Movie, MovieRating
from app.schemas.schemas import MovieCreate, MovieUpdate, RatingCreate
from app.repositories.movie_repository import get_movies, get_movie, create_movie, update_movie, delete_movie, create_rating, get_genres_by_ids, get_director_by_id
from app.exceptions.custom_exceptions import NotFoundException, ValidationException
from typing import Tuple, List, Optional

def get_all_movies(db: Session, page: int = 1, page_size: int = 10, title: Optional[str] = None, release_year: Optional[int] = None, genre: Optional[str] = None) -> Tuple[List[Movie], int]:
    skip = (page - 1) * page_size
    return get_movies(db, skip=skip, limit=page_size, title=title, release_year=release_year, genre=genre)

def get_movie_by_id(db: Session, movie_id: int) -> Movie:
    movie = get_movie(db, movie_id)
    if not movie:
        raise NotFoundException("Movie not found")
    return movie

def create_new_movie(db: Session, movie_data: MovieCreate) -> Movie:
    director = get_director_by_id(db, movie_data.director_id)
    if not director:
        raise ValidationException("Invalid director_id")
    
    genres = get_genres_by_ids(db, movie_data.genres)
    if len(genres) != len(movie_data.genres):
        raise ValidationException("Invalid genres")
    
    movie = Movie(
        title=movie_data.title,
        director_id=movie_data.director_id,
        release_year=movie_data.release_year,
        cast=movie_data.cast
    )
    return create_movie(db, movie, genres)

def update_existing_movie(db: Session, movie_id: int, movie_data: MovieUpdate) -> Movie:
    movie = get_movie(db, movie_id)
    if not movie:
        raise NotFoundException("Movie not found")
    
    if movie_data.title is not None:
        movie.title = movie_data.title
    if movie_data.release_year is not None:
        movie.release_year = movie_data.release_year
    if movie_data.cast is not None:
        movie.cast = movie_data.cast
    
    genres = None
    if movie_data.genres is not None:
        genres = get_genres_by_ids(db, movie_data.genres)
        if len(genres) != len(movie_data.genres):
            raise ValidationException("Invalid genres")
    
    return update_movie(db, movie, genres)

def delete_movie_by_id(db: Session, movie_id: int):
    deleted = delete_movie(db, movie_id)
    if not deleted:
        raise NotFoundException("Movie not found")

def add_rating_to_movie(db: Session, movie_id: int, rating_data: RatingCreate) -> MovieRating:
    if get_movie(db, movie_id) is None:
        raise NotFoundException("Movie not found")
    rating = MovieRating(movie_id=movie_id, score=rating_data.score)
    return create_rating(db, rating)