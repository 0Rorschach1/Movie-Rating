from sqlalchemy import Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship
from app.db.session import Base

movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)

class Director(Base):
    __tablename__ = "directors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    birth_year = Column(Integer)
    description = Column(Text)
    
    movies = relationship("Movie", back_populates="director")

class Genre(Base):
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    
    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    director_id = Column(Integer, ForeignKey("directors.id"))
    release_year = Column(Integer)
    cast = Column(Text)
    
    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    ratings = relationship("MovieRating", back_populates="movie", cascade="all, delete-orphan")

class MovieRating(Base):
    __tablename__ = "movie_ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    score = Column(Integer)
    
    movie = relationship("Movie", back_populates="ratings")