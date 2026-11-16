# CLAUDE.md — Stateside

Stateside is a job platform for international students in the USA: legal job aggregation, H-1B / E-Verify / cap-exempt filters, honest ATS-tailored resumes, alerts, visa News, and visa Guidance.
**Full spec:** `docs/PROJECT_SPEC.md` — read the relevant section before starting any task.

## Ground rules (never break these)
1. **Legal data only.** Use official public APIs and government datasets. Never write scrapers for LinkedIn, Indeed, Handshake, Glassdoor, or any site whose terms forbid it. LinkedIn/Indeed/Handshake = pre-filled deep links only.
2. **Never fabricate resume content.** Resume agents may only use facts from the user's `profile_items`. Every claim in an output must map to a source item.
3. **Sponsorship data is history, not a promise.** UI text: "Filed 120 H-1B LCAs in FY2025", never "Will sponsor you".
4. **No hard-coded immigration rules.** Fees, limits, windows, and dates come from the `visa_rules` table with `source_url` + `verified_at`.
5. **Guidance & News:** every item links an official source and shows a verified date; Guidance is published only after human review.
6. **Privacy:** never log resume text or personal data; encrypt files at rest; support full account deletion.
7. **Secrets** live in `.env` (never committed). Use `.env.example` for placeholders.

## Stack
- Backend: Python 3.12, FastAPI, SQLAlchemy 2.x, Pydantic v2, Alembic, APScheduler
- DB: PostgreSQL 16 + pgvector + pg_trgm
- LLM: Claude API via the `anthropic` SDK; structured JSON outputs validated with Pydantic
- Frontend: Next.js (App Router) + TypeScript + Tailwind
- Resume export: WeasyPrint (PDF), python-docx (DOCX)
- Tests: pytest (backend), Vitest + Playwright (frontend)
- Infra: Docker Compose locally

## Repo layout
```
backend/
  app/
    api/            # FastAPI routers (jobs, employers, resumes, searches, news, guidance)
    core/           # config, db session, security
    models/         # SQLAlchemy models
    schemas/        # Pydantic schemas
    ingest/
      jobs/         # one fetcher per source: greenhouse.py, lever.py, ashby.py, adzuna.py ...
      gov/          # lca.py, uscis.py, everify.py, irs.py
      news/         # federal_register.py, uscis_news.py ...
    agents/         # jd_analyzer, recruiter, level_strategist, writer, ats_checker, critic
    services/       # matching, scoring, dedupe, alerts, deeplinks
  alembic/
  tests/
    fixtures/       # saved sample API responses — tests never hit the network
frontend/
docs/
  PROJECT_SPEC.md
  decisions/        # short ADRs: 0001-why-no-scraping.md, ...
docker-compose.yml
```

## Commands
- Start everything: `docker compose up -d`
- Backend tests: `cd backend && pytest -q`
- Lint/format: `cd backend && ruff check . && ruff format .`
- Migrations: `cd backend && alembic revision --autogenerate -m "msg" && alembic upgrade head`
- Frontend: `cd frontend && npm run dev` / `npm test`

## Conventions
- Every job fetcher implements `fetch(board_token) -> list[NormalizedJob]` and has a test using a saved fixture in `tests/fixtures/`.
- Respect rate limits; exponential backoff; generic User-Agent `Stateside/0.1`. Never put the user's email in requests.
- LLM calls: go through `app/agents/llm.py` (one place for model name, retries, JSON validation, caching by input hash).
- Type hints everywhere; small functions; no silent `except:`.
- Small, focused commits with clear messages (`feat(ingest): add Lever fetcher`).

## How to work with me (Claude)
- For any task bigger than one file: **propose a plan first**, wait for approval, then implement.
- Write or update tests with every change and run them before saying a task is done.
- If something in the spec is unclear or conflicts with these rules, ask instead of guessing.
- After finishing a task, summarize what changed and what to verify manually.
