from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.genre_repository import create_genre, get_genres, get_genre
from app.schemas.schemas import GenreCreate, Genre
from app.exceptions.custom_exceptions import NotFoundException, InternalServerException
from typing import List

router = APIRouter()

@router.post("/", response_model=None, status_code=201)
def create_new_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    try:
        new_genre = create_genre(db, Genre(**genre.model_dump()))
        return {"status": "success", "data": Genre.model_validate(new_genre).model_dump()}
    except Exception:
        raise InternalServerException()

@router.get("/", response_model=None)
def list_genres(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        genres = get_genres(db, skip, limit)
        return {"status": "success", "data": [Genre.model_validate(g).model_dump() for g in genres]}
    except Exception:
        raise InternalServerException()

@router.get("/{genre_id}", response_model=None)
def get_genre_detail(genre_id: int, db: Session = Depends(get_db)):
    try:
        genre = get_genre(db, genre_id)
        if not genre:
            raise NotFoundException("Genre not found")
        return {"status": "success", "data": Genre.model_validate(genre).model_dump()}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail={"status": "failure", "error": {"code": 404, "message": e.detail}})
    except Exception:
        raise InternalServerException()