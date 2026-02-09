from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.movie_service import get_all_movies, get_movie_by_id, create_new_movie, update_existing_movie, delete_movie_by_id, add_rating_to_movie
from app.schemas.schemas import PaginatedMovies, Movie, MovieCreate, MovieUpdate, RatingCreate, Rating
from app.exceptions.custom_exceptions import NotFoundException, ValidationException, InternalServerException
from typing import Optional
from app.models.models import MovieRating

router = APIRouter()

@router.get("/", response_model=None)
def list_movies(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, alias="page_size", ge=1, le=100),
    title: Optional[str] = Query(None),
    release_year: Optional[int] = Query(None),
    genre: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        movies, total = get_all_movies(db, page, page_size, title, release_year, genre)
        paginated = PaginatedMovies(page=page, page_size=page_size, total_items=total, items=[Movie.model_validate(m) for m in movies])
        return {"status": "success", "data": paginated.model_dump()}
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"status": "failure", "error": {"code": 422, "message": str(e)}})
    except Exception:
        raise InternalServerException()

@router.get("/{movie_id}", response_model=None)
def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    try:
        movie = get_movie_by_id(db, movie_id)
        return {"status": "success", "data": Movie.model_validate(movie).model_dump()}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail={"status": "failure", "error": {"code": 404, "message": e.detail}})
    except Exception:
        raise InternalServerException()

@router.post("/", response_model=None, status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    try:
        new_movie = create_new_movie(db, movie)
        return {"status": "success", "data": Movie.model_validate(new_movie).model_dump()}
    except ValidationException as e:
        raise HTTPException(status_code=422, detail={"status": "failure", "error": {"code": 422, "message": e.detail}})
    except Exception:
        raise InternalServerException()

@router.put("/{movie_id}", response_model=None)
def update_movie(movie_id: int, movie: MovieUpdate, db: Session = Depends(get_db)):
    try:
        updated_movie = update_existing_movie(db, movie_id, movie)
        return {"status": "success", "data": Movie.model_validate(updated_movie).model_dump()}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail={"status": "failure", "error": {"code": 404, "message": e.detail}})
    except ValidationException as e:
        raise HTTPException(status_code=422, detail={"status": "failure", "error": {"code": 422, "message": e.detail}})
    except Exception:
        raise InternalServerException()

@router.delete("/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    try:
        delete_movie_by_id(db, movie_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail={"status": "failure", "error": {"code": 404, "message": e.detail}})
    except Exception:
        raise InternalServerException()

@router.post("/{movie_id}/ratings", response_model=None, status_code=201)
def create_rating(movie_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    try:
        new_rating = add_rating_to_movie(db, movie_id, rating)
        return {"status": "success", "data": {"id": new_rating.id, "movie_id": new_rating.movie_id, "score": new_rating.score}}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail={"status": "failure", "error": {"code": 404, "message": e.detail}})
    except ValidationException as e:
        raise HTTPException(status_code=422, detail={"status": "failure", "error": {"code": 422, "message": e.detail}})
    except Exception:
        raise InternalServerException()