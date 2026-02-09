from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DirectorBase(BaseModel):
    name: str
    birth_year: int
    description: Optional[str] = None

class DirectorCreate(DirectorBase):
    pass

class Director(DirectorBase):
    id: int

    class Config:
        from_attributes = True

class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int

    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    title: str
    director_id: int
    release_year: int
    cast: Optional[str] = None
    genres: List[int] = []

class MovieCreate(MovieBase):
    pass

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    release_year: Optional[int] = None
    cast: Optional[str] = None
    genres: Optional[List[int]] = None

class Movie(MovieBase):
    id: int
    director: Director
    genres: List[Genre]
    average_rating: Optional[float] = None
    ratings_count: int = 0

    class Config:
        from_attributes = True

class RatingBase(BaseModel):
    score: int = Field(..., ge=1, le=10)

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    movie_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaginatedMovies(BaseModel):
    page: int
    page_size: int
    total_items: int
    items: List[Movie]

class ResponseSuccess(BaseModel):
    status: str = "success"
    data: dict

class ResponseFailure(BaseModel):
    status: str = "failure"
    error: dict