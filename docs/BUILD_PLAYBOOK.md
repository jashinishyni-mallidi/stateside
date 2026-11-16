# Stateside — Build Playbook (Claude Project + Claude Code)

## Who does what
| Tool | Use it for |
|---|---|
| **Claude Project** ("Stateside — Planning") | Thinking: specs, design decisions, prompt design for the agents, reviewing trade-offs, writing Guidance content drafts, README, interview prep |
| **Claude Code** (in your repo) | Doing: writing code, running tests, debugging, migrations, refactors, commits |
| **You** | Deciding, reviewing every diff, testing manually, verifying visa content against official sources |

**The loop:** plan in Project → paste the task into Claude Code → ask for a plan → approve → it builds + tests → you review the diff → commit → note decisions back in the Project.

---

## Step 0 — Setup (day 1)

**Claude Project**
1. Create a project: *Stateside — Planning*.
2. Upload `PROJECT_SPEC.md` (and later your ADRs).
3. Project instructions (paste):
   > You are my senior engineer and product partner for Stateside. Always follow the ground rules in PROJECT_SPEC.md §1. When I ask for a task, turn it into a precise Claude Code prompt with: goal, files to touch, acceptance criteria, and tests.

**Claude Code**
1. Install Claude Code (see the official docs at docs.claude.com) and sign in.
2. `mkdir stateside && cd stateside && git init`
3. Put `CLAUDE.md` in the root and `PROJECT_SPEC.md` in `docs/`.
4. Create a GitHub repo and push.

**Useful habits in Claude Code**
- Use **plan mode** for anything bigger than one file.
- One task per session; clear/compact context between big tasks.
- Commit after every working step, so you can always roll back.
- Never paste API keys into chat — put them in `.env`.

---

## Phase 1 — Core job platform (weeks 1–5)

### 1.1 Skeleton
```
Read CLAUDE.md and docs/PROJECT_SPEC.md §6 and §9.
Set up the repo skeleton: backend (FastAPI app factory, config from .env, health endpoint),
docker-compose with Postgres 16 + pgvector + pg_trgm, Alembic, ruff, pytest, .env.example,
and a GitHub Actions workflow that runs lint + tests. Propose a plan first.
Acceptance: `docker compose up -d` works, GET /health returns ok, pytest passes in CI.
```

### 1.2 Database models
```
Implement SQLAlchemy models + an Alembic migration for these tables from §9:
users, student_profiles, employers, employer_aliases, job_sources, company_ats_boards, jobs, ingestion_runs.
Leave the other tables for later. Add a seed script that inserts job_sources rows.
Acceptance: migration runs on a fresh DB; a test creates and reads each model.
```

### 1.3 Job fetchers
```
Implement fetchers for Greenhouse, Lever, and Ashby public job board APIs (§5.1)
in backend/app/ingest/jobs/. First, verify each endpoint's current response format from
the official docs and save one real sample response per source to tests/fixtures/.
Each fetcher returns list[NormalizedJob]. Add retries/backoff and rate limiting.
Tests must use fixtures only (no network).
Acceptance: pytest passes; a CLI command `python -m app.ingest.run --source greenhouse --board <token>` stores jobs.
```

### 1.4 Normalize, dedupe, schedule
```
Add dedupe (dedupe_hash per §11), upsert logic, mark-inactive after 2 missed runs,
ingestion_runs logging, and an APScheduler job that refreshes all boards every 4 hours.
Acceptance: running ingest twice creates no duplicates; tests cover update + close.
```

### 1.5 Government data + employer matching (hardest part)
```
Implement ETL loaders for DOL LCA disclosure data and USCIS H-1B Employer Data Hub (§5.2),
plus employer name normalization and matching with pg_trgm (§6 "Hardest problem").
Store low-confidence matches for manual review. Add lca_filings and uscis_h1b_stats tables.
Acceptance: test set of 30 tricky names (e.g., "Google LLC" vs "GOOGLE INC.") matches correctly;
report match accuracy in the test output.
```

### 1.6 JD classifier + scoring
```
Implement app/agents/llm.py (single Claude API wrapper: retries, JSON validation, cache by input hash)
and a JD classifier that fills: level, employment_type, role_family, jd_sponsorship,
requires_citizenship, requires_clearance, accepts_cpt_opt, skills, keywords, years_required (§11 step 3).
Then implement eligibility badge + employer sponsorship score (§8).
Acceptance: an eval script runs on 50 hand-labeled JDs in tests/fixtures/jd_labels.json and prints accuracy per field.
```

### 1.7 API + frontend
```
Build GET /jobs with all filters in §10, GET /jobs/{id}, GET /employers/{id}, GET /deeplinks.
Then scaffold the Next.js frontend: job feed with filters, job detail with eligibility badge,
company page with LCA history chart. Keep the visa disclaimer on visa-related screens.
```

### 1.8 Saved searches + alerts
```
Implement saved_searches, notifications (unique per search+job), email via Resend,
and the alert matcher from §11 step 6. Add a daily digest option.
Acceptance: test proves a user is never notified twice for the same job.
```

**🚀 Ship Phase 1:** deploy, share with 20+ international students, collect feedback.

---

## Phase 2 — Resume agents (weeks 6–7)
```
Implement resume upload + parsing into profile_items, then the agent pipeline in §7
(JD analyzer → recruiter → level strategist → writer → ATS checker → critic loop → fabrication guard).
PDF + DOCX export with a single-column ATS-friendly template.
Acceptance: eval on 20 profile/JD pairs reports keyword coverage before/after and fabrication rate (must be 0).
```
Tip: design and iterate the agent prompts in your **Claude Project** first, then hand the final prompts to Claude Code.

---

## Phase 3 — News + Guidance (weeks 8–10)
```
News: implement §16 — Federal Register API + USCIS + State Dept + SEVP ingest,
LLM tagging/summaries (paraphrase only), review_state gate, and visa-type alerts.
```
```
Guidance: implement §17 tables, admin page to create/review paths, personal roadmap with
computed deadline windows from timing_rule, reminders, and the "Ask Guidance" RAG endpoint
that answers only from published content with citations.
```
Write Guidance content drafts in your **Claude Project**, verify each step against official sources yourself, then publish.

---

## Things that make this look great to recruiters
- `docs/decisions/` ADRs (e.g., *why official APIs instead of scraping*).
- Eval numbers in the README (classifier accuracy, match accuracy, keyword coverage, 0% fabrication).
- README section **"How I built this with AI"**: your workflow, what you reviewed, bugs you caught in AI-written code.
- Clean commit history, CI badge, live demo link, 2-minute demo video.
- Real user count.
