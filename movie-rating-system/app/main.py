from fastapi import FastAPI
from app.db.session import engine
from app.models.models import Base
from app.controllers import movies, directors, genres

app = FastAPI(title="Movie Rating System", version="1.0")

# For dev: Base.metadata.create_all(bind=engine)

app.include_router(movies.router, prefix="/api/v1/movies", tags=["movies"])
app.include_router(directors.router, prefix="/api/v1/directors", tags=["directors"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Movie Rating System"}