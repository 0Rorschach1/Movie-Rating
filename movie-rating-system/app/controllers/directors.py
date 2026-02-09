from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.director_repository import create_director, get_directors, get_director
from app.schemas.schemas import DirectorCreate, Director
from app.exceptions.custom_exceptions import NotFoundException, InternalServerException
from typing import List

router = APIRouter()

@router.post("/", response_model=None, status_code=201)
def create_new_director(director: DirectorCreate, db: Session = Depends(get_db)):
    try:
        new_director = create_director(db, Director(**director.model_dump()))
        return {"status": "success", "data": Director.model_validate(new_director).model_dump()}
    except Exception:
        raise InternalServerException()

@router.get("/", response_model=None)
def list_directors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        directors = get_directors(db, skip, limit)
        return {"status": "success", "data": [Director.model_validate(d).model_dump() for d in directors]}
    except Exception:
        raise InternalServerException()

@router.get("/{director_id}", response_model=None)
def get_director_detail(director_id: int, db: Session = Depends(get_db)):
    try:
        director = get_director(db, director_id)
        if not director:
            raise NotFoundException("Director not found")
        return {"status": "success", "data": Director.model_validate(director).model_dump()}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail={"status": "failure", "error": {"code": 404, "message": e.detail}})
    except Exception:
        raise InternalServerException()