from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.models import Director
from typing import List, Optional

def create_director(db: Session, director: Director) -> Director:
    db.add(director)
    db.commit()
    db.refresh(director)
    return director

def get_directors(db: Session, skip: int = 0, limit: int = 10) -> List[Director]:
    return db.scalars(select(Director).offset(skip).limit(limit)).all()

def get_director(db: Session, director_id: int) -> Optional[Director]:
    return db.scalar(select(Director).filter(Director.id == director_id))