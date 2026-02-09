from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import func, select
from app.models.models import Movie, Genre, Director, MovieRating, movie_genres
from typing import List, Optional, Tuple

def get_movies(db: Session, skip: int = 0, limit: int = 10, title: Optional[str] = None, release_year: Optional[int] = None, genre: Optional[str] = None) -> Tuple[List[Movie], int]:
    query = select(Movie).options(
        joinedload(Movie.director),
        joinedload(Movie.genres)
    )
    
    if title:
        query = query.filter(Movie.title.ilike(f"%{title}%"))
    if release_year:
        query = query.filter(Movie.release_year == release_year)
    if genre:
        g = aliased(Genre)
        query = query.join(Movie.genres.of_type(g)).filter(g.name.ilike(f"%{genre}%"))
    
    total = db.scalar(select(func.count()).select_from(query.subquery()))
    movies = db.scalars(query.offset(skip).limit(limit)).all()
    
    for movie in movies:
        avg_rating = db.scalar(select(func.avg(MovieRating.score)).filter(MovieRating.movie_id == movie.id))
        count_ratings = db.scalar(select(func.count(MovieRating.id)).filter(MovieRating.movie_id == movie.id))
        movie.average_rating = float(avg_rating) if avg_rating else None
        movie.ratings_count = count_ratings or 0
    
    return movies, total

def get_movie(db: Session, movie_id: int) -> Optional[Movie]:
    movie = db.scalar(select(Movie).options(joinedload(Movie.director), joinedload(Movie.genres)).filter(Movie.id == movie_id))
    if movie:
        avg_rating = db.scalar(select(func.avg(MovieRating.score)).filter(MovieRating.movie_id == movie.id))
        count_ratings = db.scalar(select(func.count(MovieRating.id)).filter(MovieRating.movie_id == movie.id))
        movie.average_rating = float(avg_rating) if avg_rating else None
        movie.ratings_count = count_ratings or 0
    return movie

def create_movie(db: Session, movie: Movie, genres: List[Genre]) -> Movie:
    db.add(movie)
    db.flush()
    for genre in genres:
        db.execute(movie_genres.insert().values(movie_id=movie.id, genre_id=genre.id))
    db.commit()
    db.refresh(movie)
    return movie

def update_movie(db: Session, movie: Movie, genres: Optional[List[Genre]] = None) -> Movie:
    if genres is not None:
        db.execute(movie_genres.delete().where(movie_genres.c.movie_id == movie.id))
        for genre in genres:
            db.execute(movie_genres.insert().values(movie_id=movie.id, genre_id=genre.id))
    db.commit()
    db.refresh(movie)
    return movie

def delete_movie(db: Session, movie_id: int) -> bool:
    movie = get_movie(db, movie_id)
    if movie:
        db.delete(movie)
        db.commit()
        return True
    return False

def create_rating(db: Session, rating: MovieRating) -> MovieRating:
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating

def get_genres_by_ids(db: Session, genre_ids: List[int]) -> List[Genre]:
    return db.scalars(select(Genre).filter(Genre.id.in_(genre_ids))).all()

def get_director_by_id(db: Session, director_id: int) -> Optional[Director]:
    return db.scalar(select(Director).filter(Director.id == director_id))