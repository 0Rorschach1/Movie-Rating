from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import Genre
from typing import List, Optional

def create_genre(db: Session, genre: Genre) -> Genre:
    db.add(genre)
    db.commit()
    db.refresh(genre)
    return genre

def get_genres(db: Session, skip: int = 0, limit: int = 10) -> List[Genre]:
    return db.scalars(select(Genre).offset(skip).limit(limit)).all()

def get_genre(db: Session, genre_id: int) -> Optional[Genre]:
    return db.scalar(select(Genre).filter(Genre.id == genre_id))