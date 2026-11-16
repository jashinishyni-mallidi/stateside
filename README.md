# Stateside

A job platform for international students in the USA. It aggregates jobs from legal sources and adds H-1B, E-Verify and cap-exempt filters, honest ATS-tailored resumes, alerts, visa news and visa guidance.

Ground rules: only legal data sources (official APIs and government datasets, no scraping), and resume content always comes from the user's real profile, never made up. See [`docs/PROJECT_SPEC.md`](docs/PROJECT_SPEC.md) and [`CLAUDE.md`](CLAUDE.md).

## Run locally (Windows / PowerShell)

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) with the WSL 2 backend, and Git.
The backend runs on Python 3.12 inside Docker, so you don't need a local Python install.

```powershell
# 1. Create your local env file (then edit values if you like)
Copy-Item .env.example .env

# 2. Build and start Postgres + backend
docker compose up -d --build

# 3. Check the API is up
Invoke-RestMethod http://localhost:8000/health   # -> status: ok
```

API docs: http://localhost:8000/docs

### Everyday commands

```powershell
docker compose exec backend pytest                 # tests
docker compose exec backend ruff check .           # lint
docker compose exec backend ruff format .          # format
docker compose exec backend alembic upgrade head   # apply migrations
docker compose logs -f backend                     # follow API logs (hot reload is on)
docker compose down                                # stop
docker compose down -v                             # stop AND wipe the database
```

### Notes
- If port `5432` is already taken by a local Postgres, set `POSTGRES_PORT=5433` in `.env`.
- `docker/postgres/init/01-extensions.sql` enables `vector` and `pg_trgm`. It runs only when the database volume is first created, so run `docker compose down -v` to re-run it.
- Edits under `backend/` trigger a reload through file polling (`WATCHFILES_FORCE_POLLING`), because file events from Windows don't reach the container under WSL 2.
