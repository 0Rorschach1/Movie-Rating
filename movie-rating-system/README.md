# Movie Rating System

## Setup Instructions

1. Install Poetry: `pip install poetry`
2. `poetry install`
3. Start Postgres: `docker-compose up -d`
4. Init Alembic: `alembic init alembic` (if not pre-set)
5. Create migration: `alembic revision --autogenerate -m "initial"`
6. Run migration: `alembic upgrade head`
7. Run server: `uvicorn app.main:app --reload`

## API Endpoints

- `GET /api/v1/movies/` - List movies (paginated, filtered)
- `GET /api/v1/movies/{movie_id}` - Get movie details
- `POST /api/v1/movies/` - Create movie
- `PUT /api/v1/movies/{movie_id}` - Update movie
- `DELETE /api/v1/movies/{movie_id}` - Delete movie
- `POST /api/v1/movies/{movie_id}/ratings` - Add rating
- `POST /api/v1/directors/` - Create director
- `GET /api/v1/directors/` - List directors
- `GET /api/v1/directors/{director_id}` - Get director
- `POST /api/v1/genres/` - Create genre
- `GET /api/v1/genres/` - List genres
- `GET /api/v1/genres/{genre_id}` - Get genre