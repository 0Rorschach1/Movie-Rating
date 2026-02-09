# Placeholder for checking seed data
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app.db.session import engine
from app.models.models import Movie

load_dotenv()
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print(f"Number of movies: {db.query(Movie).count()}")
finally:
    db.close()