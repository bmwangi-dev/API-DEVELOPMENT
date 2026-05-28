# Habit Tracker API

FastAPI backend for the Habit Tracker app, containerized with PostgreSQL and RustFS S3-compatible object storage.

## Run With Docker

1. Create your local environment file:

   ```sh
   cp .env.example .env
   ```

2. Start the stack:

   ```sh
   docker compose up --build
   ```

The API will be available at `http://localhost:8000`.

Useful local URLs:

- API root: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`
- API health: `http://localhost:8000/health`
- RustFS S3 API: `http://localhost:9000`
- RustFS S3 health: `http://localhost:9000/health`
- RustFS console: `http://localhost:9001/rustfs/console/`
- RustFS console health: `http://localhost:9001/rustfs/console/health`

PostgreSQL is published on `localhost:5433` by default to avoid clashing with a local Postgres install. PostgreSQL is not an HTTP service, so `http://localhost:5433/` will not show a web page. Use `make db-shell` or a database client instead.

RustFS exposes its S3 API on `http://localhost:9000` and its console on `http://localhost:9001/rustfs/console/`. Inside Docker, the API still reaches RustFS at `http://rustfs:9000`. The compose file also creates the `RUSTFS_BUCKET` bucket with `minio/mc` so profile image uploads can work immediately.

## Services

- `api`: FastAPI app running with Uvicorn.
- `db`: PostgreSQL database used through `DATABASE_URL`.
- `rustfs`: S3-compatible file storage used by `storage.py`.
- `rustfs-init`: one-shot bucket creation helper.

## Notes

- The app still falls back to local SQLite if `DATABASE_URL` is not set, which keeps non-Docker local development simple.
- For production, replace the default `.env` secrets and consider adding Alembic migrations instead of relying on `models.Base.metadata.create_all`.
