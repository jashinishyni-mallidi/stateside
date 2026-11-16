# Stateside — Project Spec & Database Schema

> One platform where international students in the USA can find jobs they are actually eligible for, see each employer's real sponsorship history, generate an honest, ATS-optimized resume tailored to each job, get alerts for new jobs, follow visa news for every visa type, and get step-by-step **Guidance** (steps, documents, deadlines) for every visa path — from CPT to OPT to H-1B and beyond.

**Use this file as the knowledge file in your Claude Project.** It is the single source of truth for scope, data sources, architecture, schema, and rules.

---

## 1. Ground rules (non-negotiable)

1. **Legal data only.** Use only official public APIs, public government datasets, and openly licensed lists. **No scraping** of LinkedIn, Indeed, Handshake, Glassdoor, or any site whose terms forbid it.
2. **LinkedIn / Indeed / Handshake = deep links only.** We build pre-filled search URLs that open those sites in the user's browser. We never fetch or store their data.
3. **Never fabricate experience.** The resume agents may reword, reorder, emphasize, and add keywords the user *actually has*. They may never invent jobs, titles, dates, degrees, skills, or metrics.
4. **Sponsorship data = past behavior, not a promise.** Always label it ("Filed 120 H-1B LCAs in FY2025"), never "Will sponsor you."
5. **Not legal advice.** Work authorization (CPT/OPT/STEM OPT/H-1B) is decided by the student's DSO, USCIS, and the employer. Show a disclaimer on every visa-related screen and link to official sources.
6. **Immigration rules change often.** Keep rule text (fees, lottery rules, dates) in a config table / news feed — never hard-code it in logic.
8. **Guidance & News are official-source-first.** Every step and news summary links the official page, shows a "last verified" date, and is human-reviewed before publishing. AI drafts; a person approves.
7. **Privacy.** Resumes contain personal data: encrypt at rest, let users delete everything, never sell or share data.

---

## 2. The problem

International students (F-1 / J-1) face problems that general job boards ignore:

- Most listings don't say whether the employer sponsors visas — students waste weeks applying to jobs that auto-reject them ("must be authorized to work without sponsorship", "US citizens only", "clearance required").
- Students don't know which companies have a **track record** of sponsoring H-1Bs, or which employers are **E-Verify** enrolled (required for STEM OPT).
- Almost nobody knows about **cap-exempt employers** (universities, affiliated nonprofits, nonprofit/government research orgs) that can sponsor H-1B **without the lottery**.
- Strict timelines: limited unemployment days on OPT, lottery dates, OPT end dates.
- Resumes get filtered by ATS keyword matching, and students don't know how to frame their level (intern vs junior vs senior) honestly and effectively.

---

## 3. How it helps every kind of international student

> ⚠️ Rules below are summaries for product design. Always confirm with your school's DSO and official USCIS pages; show this disclaimer in-app.

| Student situation | What they struggle with | What Stateside gives them |
|---|---|---|
| **Undergrad, first/second year (F-1)** | Most internships need CPT; often need ≥1 academic year enrolled first; don't know where to start | Filter: *Internship + CPT-friendly + accepts F-1*; "Eligible soon" tags; beginner-level resume (projects/coursework first); on-campus job listings (no CPT needed for on-campus work, within hour limits) |
| **Co-op program students** | Co-op roles are scattered; need CPT paperwork timing | Filter: *Co-op*, by term (Spring/Summer/Fall) and duration; reminder to start CPT paperwork with DSO before start date |
| **Grad students (MS)** | Short program = little time; need internship fast; some programs allow Day-1 CPT | Filters: *Internship + Summer + sponsors F-1 interns*; "Hired F-1 interns before" signal; fast one-click tailored resumes |
| **PhD students / researchers** | Want research roles, labs, postdocs; need H-1B without lottery risk | **Cap-exempt filter** (universities, affiliated nonprofits, research orgs); research-focused resume/CV mode |
| **New grads on OPT** | Limited unemployment days on OPT — every day counts; need jobs related to their degree | Filter: *New grad + Sponsors H-1B + Related to my major*; **OPT clock tracker** (days used/left); daily alerts so they apply first |
| **STEM OPT extension seekers** | Employer **must be enrolled in E-Verify**; must have a training plan (I-983) | **E-Verify badge + filter**; "STEM OPT-ready employer" tag; tips checklist for I-983 conversation |
| **Lost the H-1B lottery / want to avoid it** | Need a backup path | **Cap-exempt employers filter**; explains concurrent cap-exempt employment options (link to official info) |
| **Lottery-season applicants** | New wage-weighted selection — salary level affects odds | Shows the **prevailing-wage level** a job's posted salary falls into (DOL OFLC wage data) so students understand where they stand |
| **Non-STEM students (business, arts, social sciences)** | Fewer sponsors, shorter OPT, less guidance | Sponsor history broken down by job title/role family (e.g., "Marketing Analyst LCAs"), not just tech; nonprofit & NGO filter |
| **Students interested in NGOs / nonprofits / public interest** | Hard to find which orgs hire internationals | **Nonprofit filter** (IRS tax-exempt data) + cap-exempt flag; Idealist-style roles where legally available |
| **Students who want remote roles** | Remote + visa rules are confusing | Remote filter + "US-based remote" vs "anywhere"; work-location field from LCA data |
| **Students in small cities / not near tech hubs** | Few local sponsors | Map/location filter using LCA worksite data — "companies near you that sponsor" |
| **Anyone** | Wasting time on jobs that auto-reject internationals | **Auto-flag** "No sponsorship / US citizens only / clearance required" from JD text; **Eligibility score** on every job card |

### Core value in one sentence
**Stop applying blind:** every job shows *can I apply, has this employer sponsored people like me before, and here is my honest, keyword-matched resume for it.*

---

## 4. Features

### MVP (v1)
1. **Account + master profile** — upload resume (PDF/DOCX) → parsed into structured profile (education, experience, projects, skills). User sets visa status, degree, major, graduation date, OPT dates.
2. **Job feed** — aggregated from legal sources (§5), refreshed every 3–6 hours, deduplicated.
3. **Filters**
   - Role / role family, keyword, location, remote/hybrid/onsite
   - Date posted (24h / 3d / 7d / 30d)
   - Level: Intern, Co-op, New grad, Junior, Mid, Senior, Lead/Manager
   - Employment type: full-time, part-time, contract, internship, co-op
   - **International filters:** sponsors H-1B (history), E-Verify enrolled, cap-exempt, nonprofit/NGO, CPT/F-1-intern friendly, hides "no sponsorship"/"citizens only"/"clearance" jobs
   - Salary range + wage level
4. **Company page** — H-1B LCA history (counts by year, top job titles, median wages, worksites), E-Verify status, cap-exempt/nonprofit status, open jobs.
5. **Eligibility badge on each job** — 🟢 Likely eligible / 🟡 Unclear / 🔴 Not eligible (with reasons).
6. **One-click tailored resume** (§7) — tailored to JD + level, ATS match score, missing keywords, PDF + DOCX export.
7. **Deep links** — "Search on LinkedIn / Indeed / Handshake" with pre-filled role, location, and type.
8. **Paste any JD** — tailor a resume for a job found anywhere (user brings the data).

### v2
9. **Saved searches + alerts** — email / web push when new jobs match (instant or daily digest).
10. **Application tracker** — Saved → Applied → Interview → Offer → Rejected.
11. **Visa timeline** — OPT start/end, unemployment-days counter, STEM OPT window, lottery dates (from config table).
12. **Cover letter generator** (same honesty rules).
13. **Visa News** — all visa types, from official sources (§16).
14. **Guidance** — step-by-step visa pathways, document checklists, deadlines, and a personal roadmap (§17).

### App navigation
`Jobs` · `Companies` · `My Resumes` · `Tracker` · **`Guidance`** · **`News`** · `Profile`

---

## 5. Data sources (legal only)

### 5.1 Job listings
| Source | Type | Notes |
|---|---|---|
| **Greenhouse Job Board API** | Public, no auth | `GET https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true` |
| **Lever Postings API** | Public, no auth | `GET https://api.lever.co/v0/postings/{company}?mode=json` |
| **Ashby Job Board API** | Public, no auth | `GET https://api.ashbyhq.com/posting-api/job-board/{board_name}?includeCompensation=true` |
| **SmartRecruiters Posting API** | Public | `GET https://api.smartrecruiters.com/v1/companies/{company_id}/postings` |
| **Workable / Recruitee** | Public widget/careers endpoints | Check each one's terms |
| **Adzuna API** | Free key | Broad US coverage, salary, date posted |
| **Jooble / Careerjet / The Muse** | Free keys | Supplementary coverage |
| **Remotive / RemoteOK / Arbeitnow** | Public APIs | Remote jobs; follow attribution rules |
| **USAJobs API** | Official, free key | Most need citizenship → auto-flag 🔴 for F-1 |
| **GitHub intern/new-grad lists** (e.g., SimplifyJobs repos) | Open repos | Check license; credit source; great for interns |
| **University career sites / HigherEdJobs** | Public pages/feeds where permitted | Cap-exempt jobs; verify terms before ingesting |

> Endpoints above should be verified against each provider's current docs before coding. Respect rate limits and `robots.txt`; identify the app with a generic User-Agent.

**Seeding company lists:** Greenhouse/Lever/Ashby need a company "board token." Build the list from the H-1B employer data (§5.2) + known tech/startup lists, then probe which ATS each company uses. Store in `company_ats_boards`.

### 5.2 Enrichment (visa & employer data)
| Dataset | What it gives | Use |
|---|---|---|
| **DOL OFLC LCA Disclosure Data** (quarterly) | Every H-1B LCA: employer, job title, SOC code, wage, wage level, worksite | Sponsorship history, wages, locations |
| **USCIS H-1B Employer Data Hub** | Approvals/denials by employer & year | Sponsorship track record |
| **DOL OFLC prevailing wage data (OEWS-based)** | Wage levels I–IV by SOC + area | Show wage level of a posted salary |
| **E-Verify employer search** | Whether employer is enrolled | STEM OPT eligibility badge |
| **IRS Exempt Organizations (EO BMF)** | Nonprofit status | Nonprofit/NGO filter |
| **IPEDS (Dept. of Education)** | List of US higher-ed institutions | Cap-exempt detection (universities) |
| **USCIS / DOL news pages** | Official policy updates | Visa news panel, `visa_rules` config |

### 5.3 Deep links (no data fetched)
- LinkedIn: `https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}`
- Indeed: `https://www.indeed.com/jobs?q={q}&l={loc}`
- Handshake: link to the student's school Handshake job search (user logs in themselves)

---

## 6. Architecture

```
                ┌───────────────────────────── Scheduler (APScheduler/Celery beat) ─────────────────┐
                │                                                                                  │
 Job APIs ──► Fetchers (one per source) ──► Normalizer ──► Deduper ──► JD Classifier (LLM) ──► Postgres
                                                                         │  level, type, role family,
 Gov datasets ──► ETL loaders ──► Employer matcher (fuzzy name) ─────────┤  sponsorship phrases,
                                                                         │  skills/keywords
                                                                         ▼
                                                           Alert matcher ──► Email / Web push
                                                                         │
 Next.js frontend ◄──── FastAPI backend ◄────────────────────────────────┘
        │                     │
        └── "Tailor resume" ──► Resume Agent Pipeline (§7) ──► PDF/DOCX
```

**Stack**
- Backend: Python 3.12, FastAPI, SQLAlchemy, Pydantic
- Jobs/scheduling: APScheduler (MVP) → Celery + Redis (scale)
- DB: PostgreSQL 16 + `pgvector` + `pg_trgm` (fuzzy company-name matching)
- LLM: Claude API (tool calling, structured JSON outputs)
- Frontend: Next.js + Tailwind
- Resume output: HTML template → PDF (WeasyPrint), DOCX (python-docx)
- Email: Resend or SendGrid; Web push: VAPID
- Deploy: Docker; Render/Railway/Fly.io; managed Postgres

**Hardest problem:** matching employer names across datasets ("Google LLC" vs "Google" vs "GOOGLE INC."). Approach: normalize (lowercase, strip suffixes like LLC/Inc/Corp), `pg_trgm` similarity, then LLM/manual review for low-confidence matches; store in `employer_aliases`.

---

## 7. Resume agent pipeline

All agents return **structured JSON** and only use facts from the user's `profile`.

1. **JD Analyzer** → `{required_skills, nice_to_have, level, responsibilities, keywords[], sponsorship_flags, years_required}`
2. **Recruiter Agent** ("You are the hiring manager/recruiter at {company}") → what would make them shortlist; top 5 signals to emphasize; red flags.
3. **Level Strategist** → framing rules by level:
   - **Intern / Co-op:** education + projects + coursework first; skills section prominent; 1 page
   - **New grad / Junior:** hands-on contributions, tools, internships; 1 page
   - **Mid:** ownership of features, measurable impact
   - **Senior:** scope, system design, metrics, cross-team impact; 1–2 pages
   - **Lead / Manager:** mentoring, strategy, team outcomes, stakeholder management
   - If the user's real experience is below the JD level → **warn honestly** ("This role asks for 7+ yrs; you have 2") and suggest better-fit jobs. **Never inflate.**
4. **Resume Writer** → rewrites bullets (action verb + what + impact), inserts JD keywords **only where truthful**, orders sections for the level.
5. **ATS Checker** → parses the generated file back to text, checks: standard headings, single column, no tables/images/text boxes, contact info parsed, dates parsed; computes **keyword coverage %** and lists missing keywords.
6. **Critic loop** → if score < threshold or a fabrication check fails, revise (max 3 rounds).
7. **Fabrication guard** → every output claim must map to a `profile` source item; unmapped claims are removed.

**Output:** tailored resume (PDF + DOCX), match score, missing keywords ("add only if true"), recruiter notes, eligibility notes.

> We show a **keyword match score**, not "passes all ATS" — no tool can guarantee that, because each ATS works differently.

---

## 8. Eligibility & sponsorship scoring

**Job eligibility (per user):**
- 🔴 Not eligible if JD contains: citizenship required, security clearance, "will not sponsor" / "no sponsorship now or in the future" (when the user will need sponsorship), or source = USAJobs requiring citizenship.
- 🟡 Unclear if JD says nothing about sponsorship.
- 🟢 Likely eligible if JD says sponsorship available **or** employer has strong LCA history for similar roles **and** no blocking phrases.

**Employer sponsorship score (0–100):** weighted mix of
- LCA count last 3 fiscal years (log-scaled)
- LCAs for the same role family / SOC code
- USCIS approval rate
- E-Verify enrolled (+)
- Cap-exempt (+, shown separately)
- Recency (more weight to recent years)

Always show the raw numbers next to the score.

---

## 9. Database schema (PostgreSQL)

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ========== USERS & PROFILES ==========
CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email           TEXT UNIQUE NOT NULL,
  password_hash   TEXT,                       -- null if OAuth
  created_at      TIMESTAMPTZ DEFAULT now(),
  deleted_at      TIMESTAMPTZ
);

CREATE TABLE student_profiles (
  user_id             UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  full_name           TEXT,
  visa_status         TEXT CHECK (visa_status IN ('F1','J1','F1_OPT','F1_STEM_OPT','H1B','H4_EAD','OTHER')),
  degree_level        TEXT CHECK (degree_level IN ('BACHELORS','MASTERS','PHD','OTHER')),
  major               TEXT,
  is_stem             BOOLEAN,
  school              TEXT,
  graduation_date     DATE,
  opt_start_date      DATE,
  opt_end_date        DATE,
  unemployment_days_used INT DEFAULT 0,
  needs_sponsorship   BOOLEAN DEFAULT TRUE,
  target_roles        TEXT[],
  target_locations    TEXT[],
  open_to_remote      BOOLEAN DEFAULT TRUE,
  years_experience    NUMERIC(4,1),
  updated_at          TIMESTAMPTZ DEFAULT now()
);

-- Master resume, parsed into structured, verifiable items
CREATE TABLE resume_sources (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
  file_path     TEXT,                         -- encrypted storage
  raw_text      TEXT,
  parsed_json   JSONB,                        -- full parsed profile
  uploaded_at   TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE profile_items (                  -- each item = a fact the agents may use
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
  item_type     TEXT CHECK (item_type IN ('EXPERIENCE','PROJECT','EDUCATION','SKILL','CERT','AWARD','PUBLICATION','VOLUNTEER')),
  title         TEXT,
  organization  TEXT,
  start_date    DATE,
  end_date      DATE,
  bullets       TEXT[],
  skills        TEXT[],
  embedding     VECTOR(1024)
);

-- ========== EMPLOYERS & VISA DATA ==========
CREATE TABLE employers (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  canonical_name    TEXT NOT NULL,
  normalized_name   TEXT NOT NULL,            -- lowercased, suffixes stripped
  website           TEXT,
  fein              TEXT,                     -- when available from gov data
  hq_city           TEXT,
  hq_state          TEXT,
  is_e_verify       BOOLEAN,
  e_verify_checked_at TIMESTAMPTZ,
  is_nonprofit      BOOLEAN,
  is_cap_exempt     BOOLEAN,
  cap_exempt_reason TEXT,                     -- 'UNIVERSITY','AFFILIATED_NONPROFIT','NONPROFIT_RESEARCH','GOV_RESEARCH'
  sponsorship_score INT,
  updated_at        TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX employers_name_trgm ON employers USING gin (normalized_name gin_trgm_ops);

CREATE TABLE employer_aliases (
  alias_normalized TEXT PRIMARY KEY,
  employer_id      UUID REFERENCES employers(id) ON DELETE CASCADE,
  source           TEXT,                      -- 'LCA','USCIS','IRS','ATS','MANUAL'
  confidence       NUMERIC(3,2)
);

CREATE TABLE lca_filings (                    -- DOL OFLC disclosure data
  case_number       TEXT PRIMARY KEY,
  employer_id       UUID REFERENCES employers(id),
  fiscal_year       INT,
  case_status       TEXT,
  visa_class        TEXT,                     -- H-1B, H-1B1, E-3
  job_title         TEXT,
  soc_code          TEXT,
  soc_title         TEXT,
  wage_from         NUMERIC,
  wage_to           NUMERIC,
  wage_unit         TEXT,
  pw_wage_level     TEXT,                     -- I, II, III, IV
  worksite_city     TEXT,
  worksite_state    TEXT,
  decision_date     DATE
);
CREATE INDEX lca_emp_year ON lca_filings (employer_id, fiscal_year);

CREATE TABLE uscis_h1b_stats (                -- USCIS Employer Data Hub
  employer_id        UUID REFERENCES employers(id),
  fiscal_year        INT,
  initial_approvals  INT,
  initial_denials    INT,
  continuing_approvals INT,
  continuing_denials INT,
  PRIMARY KEY (employer_id, fiscal_year)
);

CREATE TABLE prevailing_wages (               -- for wage-level estimate
  soc_code    TEXT,
  area_code   TEXT,
  level       TEXT,                           -- I..IV
  hourly_wage NUMERIC,
  annual_wage NUMERIC,
  valid_from  DATE,
  valid_to    DATE,
  PRIMARY KEY (soc_code, area_code, level, valid_from)
);

-- ========== JOBS ==========
CREATE TABLE job_sources (
  id          SERIAL PRIMARY KEY,
  name        TEXT UNIQUE,                    -- 'greenhouse','lever','ashby','adzuna','usajobs',...
  terms_url   TEXT,
  attribution TEXT,
  enabled     BOOLEAN DEFAULT TRUE
);

CREATE TABLE company_ats_boards (
  employer_id  UUID REFERENCES employers(id),
  source_id    INT REFERENCES job_sources(id),
  board_token  TEXT,
  last_fetched_at TIMESTAMPTZ,
  PRIMARY KEY (source_id, board_token)
);

CREATE TABLE jobs (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id        INT REFERENCES job_sources(id),
  external_id      TEXT,
  employer_id      UUID REFERENCES employers(id),
  title            TEXT NOT NULL,
  description_html TEXT,
  description_text TEXT,
  apply_url        TEXT NOT NULL,
  location_city    TEXT,
  location_state   TEXT,
  workplace_type   TEXT CHECK (workplace_type IN ('ONSITE','HYBRID','REMOTE','UNKNOWN')),
  employment_type  TEXT CHECK (employment_type IN ('FULL_TIME','PART_TIME','CONTRACT','INTERNSHIP','COOP','TEMP','UNKNOWN')),
  level            TEXT CHECK (level IN ('INTERN','COOP','NEW_GRAD','JUNIOR','MID','SENIOR','LEAD','MANAGER','UNKNOWN')),
  role_family      TEXT,                      -- 'SWE','DATA','PM','DESIGN','MARKETING','FINANCE','RESEARCH',...
  soc_code_guess   TEXT,
  salary_min       NUMERIC,
  salary_max       NUMERIC,
  salary_period    TEXT,
  est_wage_level   TEXT,                      -- I..IV computed from prevailing_wages
  years_required   NUMERIC(4,1),
  -- sponsorship signals extracted from JD text
  jd_sponsorship   TEXT CHECK (jd_sponsorship IN ('OFFERS','NO_SPONSORSHIP','NOT_MENTIONED')),
  requires_citizenship BOOLEAN DEFAULT FALSE,
  requires_clearance   BOOLEAN DEFAULT FALSE,
  accepts_cpt_opt      TEXT CHECK (accepts_cpt_opt IN ('YES','NO','UNKNOWN')),
  skills           TEXT[],
  keywords         TEXT[],
  embedding        VECTOR(1024),
  dedupe_hash      TEXT,                      -- hash(employer + normalized title + location)
  posted_at        TIMESTAMPTZ,
  first_seen_at    TIMESTAMPTZ DEFAULT now(),
  last_seen_at     TIMESTAMPTZ DEFAULT now(),
  is_active        BOOLEAN DEFAULT TRUE,
  UNIQUE (source_id, external_id)
);
CREATE INDEX jobs_filters ON jobs (is_active, level, employment_type, role_family, posted_at DESC);
CREATE INDEX jobs_dedupe ON jobs (dedupe_hash);
CREATE INDEX jobs_embedding ON jobs USING hnsw (embedding vector_cosine_ops);

-- ========== TAILORED RESUMES ==========
CREATE TABLE tailored_resumes (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id          UUID REFERENCES users(id) ON DELETE CASCADE,
  job_id           UUID REFERENCES jobs(id),
  pasted_jd_text   TEXT,                      -- when job came from "paste any JD"
  target_level     TEXT,
  content_json     JSONB,                     -- structured resume
  pdf_path         TEXT,
  docx_path        TEXT,
  keyword_score    INT,                       -- 0-100
  missing_keywords TEXT[],
  recruiter_notes  TEXT,
  level_warning    TEXT,
  agent_trace      JSONB,                     -- prompts/outputs per step (for eval & debugging)
  created_at       TIMESTAMPTZ DEFAULT now()
);

-- ========== SAVED SEARCHES, ALERTS, TRACKER ==========
CREATE TABLE saved_searches (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID REFERENCES users(id) ON DELETE CASCADE,
  name         TEXT,
  filters_json JSONB NOT NULL,                -- same shape as job feed filters
  frequency    TEXT CHECK (frequency IN ('INSTANT','DAILY','WEEKLY')) DEFAULT 'DAILY',
  channels     TEXT[] DEFAULT ARRAY['EMAIL'],
  last_run_at  TIMESTAMPTZ,
  created_at   TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE notifications (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID REFERENCES users(id) ON DELETE CASCADE,
  search_id    UUID REFERENCES saved_searches(id) ON DELETE CASCADE,
  job_id       UUID REFERENCES jobs(id),
  channel      TEXT,
  sent_at      TIMESTAMPTZ DEFAULT now(),
  UNIQUE (search_id, job_id)                  -- never notify twice for the same job
);

CREATE TABLE push_subscriptions (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID REFERENCES users(id) ON DELETE CASCADE,
  endpoint   TEXT UNIQUE,
  keys_json  JSONB
);

CREATE TABLE applications (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID REFERENCES users(id) ON DELETE CASCADE,
  job_id       UUID REFERENCES jobs(id),
  resume_id    UUID REFERENCES tailored_resumes(id),
  status       TEXT CHECK (status IN ('SAVED','APPLIED','OA','INTERVIEW','OFFER','REJECTED','WITHDRAWN')) DEFAULT 'SAVED',
  applied_at   DATE,
  notes        TEXT,
  updated_at   TIMESTAMPTZ DEFAULT now()
);

-- ========== RULES & NEWS (never hard-code visa rules) ==========
CREATE TABLE visa_rules (
  key          TEXT PRIMARY KEY,              -- e.g. 'opt_unemployment_days_limit'
  value_json   JSONB,
  description  TEXT,
  source_url   TEXT,                          -- official USCIS/DOL page
  verified_at  DATE
);

CREATE TABLE visa_news (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title        TEXT,
  summary      TEXT,
  source_url   TEXT,
  published_at TIMESTAMPTZ
);

-- ========== NEWS (all visa types, §16) ==========
CREATE TABLE news_sources (
  id          SERIAL PRIMARY KEY,
  name        TEXT UNIQUE,                    -- 'uscis_newsroom','federal_register','state_dept','ice_sevp','dol_oflc','cbp'
  feed_url    TEXT,
  is_official BOOLEAN DEFAULT TRUE,
  enabled     BOOLEAN DEFAULT TRUE
);

CREATE TABLE news_items (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source_id     INT REFERENCES news_sources(id),
  external_id   TEXT,
  title         TEXT NOT NULL,
  original_url  TEXT NOT NULL,                -- always link the official original
  published_at  TIMESTAMPTZ,
  summary_plain TEXT,                         -- LLM plain-English summary, reviewed
  who_is_affected TEXT,
  what_to_do    TEXT,                         -- "talk to your DSO", "no action needed", etc.
  impact_level  TEXT CHECK (impact_level IN ('HIGH','MEDIUM','LOW','INFO')),
  effective_date DATE,
  status        TEXT CHECK (status IN ('PROPOSED','FINAL','IN_EFFECT','BLOCKED_BY_COURT','WITHDRAWN','UNKNOWN')),
  review_state  TEXT CHECK (review_state IN ('AUTO','REVIEWED','NEEDS_REVIEW')) DEFAULT 'NEEDS_REVIEW',
  UNIQUE (source_id, external_id)
);

CREATE TABLE news_visa_tags (                 -- many-to-many: one item can affect several visa types
  news_id    UUID REFERENCES news_items(id) ON DELETE CASCADE,
  visa_type  TEXT,                            -- 'F1','CPT','OPT','STEM_OPT','J1','H1B','H4','L1','O1','TN','E3','H1B1','GREEN_CARD','TRAVEL'
  PRIMARY KEY (news_id, visa_type)
);

-- ========== GUIDANCE (§17) ==========
CREATE TABLE visa_types (
  code          TEXT PRIMARY KEY,             -- 'F1','CPT','DAY1_CPT','OPT','STEM_OPT','CAP_GAP','H1B_CAP','H1B_CAP_EXEMPT','J1','J1_AT','H4_EAD','O1','L1','TN','E3','H1B1','EB2_NIW', ...
  name          TEXT,
  category      TEXT,                         -- 'STUDENT','WORK_AUTH','WORK_VISA','DEPENDENT','GREEN_CARD'
  summary       TEXT,
  official_url  TEXT
);

CREATE TABLE guidance_paths (                 -- e.g. "F-1 → OPT → STEM OPT → H-1B"
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug          TEXT UNIQUE,
  title         TEXT,
  from_visa     TEXT REFERENCES visa_types(code),
  to_visa       TEXT REFERENCES visa_types(code),
  audience      TEXT,                         -- who this path is for
  summary       TEXT,
  last_verified DATE NOT NULL,
  verified_by   TEXT,                         -- reviewer (you / a DSO / an attorney)
  is_published  BOOLEAN DEFAULT FALSE
);

CREATE TABLE guidance_steps (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  path_id         UUID REFERENCES guidance_paths(id) ON DELETE CASCADE,
  step_order      INT,
  title           TEXT,
  body_md         TEXT,                       -- plain-English explanation
  who_does_it     TEXT CHECK (who_does_it IN ('STUDENT','DSO','EMPLOYER','USCIS','DOS','ATTORNEY')),
  timing_rule     JSONB,                      -- e.g. {"anchor":"program_end_date","from_days":-90,"to_days":60}
  official_url    TEXT NOT NULL,
  warning_md      TEXT                        -- common mistakes
);

CREATE TABLE guidance_documents (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  code        TEXT UNIQUE,                    -- 'I20','I765','I983','I129','LCA','I797','EAD','DS2019','I94','PASSPORT', ...
  name        TEXT,
  description TEXT,
  who_provides TEXT,
  official_url TEXT
);

CREATE TABLE step_documents (
  step_id     UUID REFERENCES guidance_steps(id) ON DELETE CASCADE,
  document_id UUID REFERENCES guidance_documents(id),
  required    BOOLEAN DEFAULT TRUE,
  PRIMARY KEY (step_id, document_id)
);

CREATE TABLE guidance_faq (
  id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  path_id   UUID REFERENCES guidance_paths(id) ON DELETE CASCADE,
  question  TEXT,
  answer_md TEXT,
  official_url TEXT
);

-- Personal roadmap: user's own checklist + computed deadlines
CREATE TABLE user_roadmaps (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id    UUID REFERENCES users(id) ON DELETE CASCADE,
  path_id    UUID REFERENCES guidance_paths(id),
  started_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE user_step_progress (
  roadmap_id   UUID REFERENCES user_roadmaps(id) ON DELETE CASCADE,
  step_id      UUID REFERENCES guidance_steps(id),
  status       TEXT CHECK (status IN ('NOT_STARTED','IN_PROGRESS','DONE','NOT_APPLICABLE')) DEFAULT 'NOT_STARTED',
  window_start DATE,                          -- computed from timing_rule + user dates
  window_end   DATE,
  reminder_sent BOOLEAN DEFAULT FALSE,
  notes        TEXT,
  PRIMARY KEY (roadmap_id, step_id)
);

CREATE TABLE ingestion_runs (                 -- observability
  id          BIGSERIAL PRIMARY KEY,
  source_id   INT REFERENCES job_sources(id),
  started_at  TIMESTAMPTZ,
  finished_at TIMESTAMPTZ,
  jobs_new    INT,
  jobs_updated INT,
  jobs_closed INT,
  errors      JSONB
);
```

---

## 10. API endpoints (FastAPI)

| Method | Path | Purpose |
|---|---|---|
| POST | `/auth/signup`, `/auth/login` | Auth |
| GET/PUT | `/me/profile` | Student profile (visa status, dates, targets) |
| POST | `/me/resume` | Upload master resume → parse → `profile_items` |
| GET | `/jobs` | Feed with filters: `q, role_family, level, type, location, remote, posted_within, sponsors_h1b, e_verify, cap_exempt, nonprofit, hide_no_sponsorship, salary_min` |
| GET | `/jobs/{id}` | Job detail + eligibility badge + employer visa stats |
| GET | `/employers/{id}` | Company page: LCA history, USCIS stats, E-Verify, cap-exempt |
| POST | `/resumes/tailor` | `{job_id}` or `{pasted_jd}` → runs agent pipeline |
| GET | `/resumes/{id}/pdf`, `/docx` | Downloads |
| CRUD | `/searches` | Saved searches + alert settings |
| CRUD | `/applications` | Tracker |
| GET | `/deeplinks?q=&loc=&type=` | LinkedIn/Indeed/Handshake URLs |
| GET | `/news?visa_type=&impact=&since=` | Visa news feed, filterable by visa type |
| GET | `/news/{id}` | Plain-English summary + official link |
| GET | `/guidance/visa-types` | All visa types |
| GET | `/guidance/paths?from=F1` | Pathways from a visa status |
| GET | `/guidance/paths/{slug}` | Steps, documents, timing, FAQs |
| POST | `/guidance/roadmap` | Start a personal roadmap → computes deadline windows from profile dates |
| PATCH | `/guidance/roadmap/{id}/steps/{step_id}` | Mark step done / add notes |
| POST | `/guidance/ask` | "Ask Guidance" chat — answers only from published guidance + official pages, with citations |
| GET | `/visa/rules` | Config values (fees, limits) with source + verified date |
| DELETE | `/me` | Delete all user data |

---

## 11. Ingestion & alerts flow

1. Scheduler runs each fetcher every 3–6 h (respect rate limits; back off on errors).
2. Normalize into `jobs` shape → compute `dedupe_hash` → upsert; mark jobs not seen in 2 runs as `is_active = false`.
3. New/changed jobs → **JD Classifier** (LLM, JSON output): level, type, role family, SOC guess, sponsorship phrases, citizenship/clearance, skills, keywords, years required. Cache by description hash to save cost.
4. Employer matching → link `employer_id` (aliases + trigram) → join visa data.
5. Compute embeddings + `est_wage_level`.
6. **Alert matcher:** for each saved search, find jobs with `first_seen_at > last_run_at` that match filters → insert into `notifications` (unique constraint prevents duplicates) → send email/push → update `last_run_at`.
7. Gov datasets: LCA quarterly, USCIS yearly, E-Verify on-demand (cached 30 days), IRS monthly.

---

## 12. Evaluation (makes the project stand out)

- **JD classifier accuracy:** hand-label 200 JDs (level, sponsorship phrases, citizenship) → report precision/recall.
- **Employer matching accuracy:** hand-check 200 matches → report % correct.
- **Resume quality:** for 50 JD/profile pairs, measure keyword coverage before vs after; fabrication rate (target 0%); ATS re-parse success rate.
- **User study:** 10–30 international students; track time-to-apply and "jobs I was actually eligible for" vs a normal job board.
- Put results in the README with charts.

---

## 13. Roadmap (≈10 weeks)

| Week | Deliverable |
|---|---|
| 1 | Spec (this file), repo setup, Docker, Postgres schema, CLAUDE.md |
| 2 | Fetchers: Greenhouse, Lever, Ashby + normalizer + dedupe |
| 3 | Gov ETL: LCA, USCIS, E-Verify cache, IRS; employer matching |
| 4 | JD classifier + eligibility/sponsorship scoring; `/jobs` API with filters |
| 5 | Next.js feed, filters, job detail, company page, deep links |
| 6 | Resume upload/parse + agent pipeline + PDF/DOCX + ATS checker |
| 7 | Saved searches + alerts, Adzuna/GitHub lists |
| 8 | **News:** Federal Register + USCIS + State Dept + SEVP ingest, LLM summaries + visa tagging, news alerts |
| 9 | **Guidance:** content for the MVP paths (§17.3), personal roadmap + deadline reminders, "Ask Guidance" RAG chat |
| 10 | Deploy, eval, README + demo video |

---

## 14. Working with Claude (how to show AI-assisted development)

- **Claude Project (planning):** keep this spec, the schema, and design decisions as knowledge files. Use it for specs, prompt design, reviewing trade-offs.
- **Claude Code (building):** keep a `CLAUDE.md` in the repo with: stack, folder layout, coding conventions, test command, and the **Ground rules (§1)**.
- **Workflow to show in interviews:** spec → ask Claude for a plan → generate code in small PRs → **you review & write/run tests** → commit. Keep meaningful commit messages.
- **README section "How I built this with AI":** what Claude did, what you decided, bugs you caught in AI output, and what you'd do differently.

---

## 15. Resume bullets (fill in real numbers)

- Built **Stateside**, a job platform for international students aggregating **N+** postings from public ATS APIs (Greenhouse, Lever, Ashby) with H-1B, E-Verify, cap-exempt, and nonprofit filters.
- Engineered an ETL pipeline joining **DOL LCA** and **USCIS** H-1B data to **N** employers with **X%** name-matching accuracy using trigram similarity + LLM review.
- Designed a multi-agent resume tailoring pipeline (JD analyzer, recruiter simulator, writer, ATS checker) raising average keyword coverage from **X% → Y%** with a **0%** fabrication rate on a 50-case eval set.
- Shipped saved-search alerts (email/web push) and deployed with Docker on **Render**; developed using **Claude Code** with an AI-assisted spec → generate → review → test workflow.

- Built a visa **Guidance** module with **N** step-by-step pathways (CPT, OPT, STEM OPT, H-1B, O-1, J-1, …) and personal deadline roadmaps, plus a RAG assistant that answers only from reviewed, officially-cited content.
- Built an official-source **visa news pipeline** (Federal Register API, USCIS, State Dept, SEVP) with LLM summarization and visa-type tagging, alerting users only about changes that affect their status.

---

## 16. News — visa changes for all visa types

**Goal:** one place to see every immigration change that matters to international students and workers, in plain English, filtered to *my* visa type — always linking the official original.

### 16.1 Sources (official first)
| Source | What | How |
|---|---|---|
| **Federal Register API** (federalregister.gov) | Proposed & final rules, notices, proclamations (DHS, USCIS, ICE, State, Labor) | Free official JSON API; filter by agency + keywords |
| **USCIS Newsroom** | Alerts, policy manual updates, fee/form changes, H-1B season announcements | RSS / news pages |
| **U.S. Department of State (travel.state.gov)** | Visa news, consular updates, travel restrictions, **monthly Visa Bulletin** | News pages + monthly bulletin |
| **ICE SEVP — Study in the States** | F-1/M-1 policy, OPT/STEM OPT, SEVIS updates | News/updates pages |
| **DOL OFLC** | LCA, prevailing wage, PERM announcements | Announcements page |
| **CBP** | Entry/travel rules, I-94 | Newsroom |
| **Court rulings** | Injunctions or decisions that block/change a rule | Link the court order or the agency's own update; reputable news only as secondary context |

### 16.2 Pipeline
1. Fetch every 2–6 h → dedupe by URL/ID.
2. **LLM tagger** (JSON output): `visa_tags[]`, `impact_level`, `status` (proposed / final / in effect / blocked by court), `effective_date`.
3. **LLM summarizer:** "What changed", "Who is affected", "What you should do" (usually: *talk to your DSO / employer's attorney*), in ≤120 words — paraphrased, never copying the source text.
4. **Human review gate:** `HIGH` impact items stay `NEEDS_REVIEW` until checked; others publish as `AUTO` with a visible "AI summary — read the official source" label.
5. **Alerts:** users get notified only for tags matching their profile (e.g., an F-1 STEM OPT user gets `STEM_OPT`, `OPT`, `H1B`, `TRAVEL`).
6. **Rule linkage:** when a news item changes a value in `visa_rules` (fee, limit, date), flag that rule + affected Guidance steps for re-verification.

### 16.3 UI
- Feed with tag chips: `F-1` `CPT` `OPT` `STEM OPT` `J-1` `H-1B` `H-4` `L-1` `O-1` `TN` `E-3` `H-1B1` `Green card` `Travel`
- Status badge on each item: 🟡 Proposed · 🟢 Final/In effect · ⛔ Blocked by court · ⚪ Info
- "Timeline" view for big topics (e.g., all H-1B changes this year in order)
- Visa Bulletin tracker (priority dates by category/country) for green-card paths

---

## 17. Guidance — visa pathways, steps & documents

**Goal:** answer "What do I do next, by when, and with which documents?" for every common situation — as a step-by-step checklist that turns into a **personal roadmap with deadlines**.

### 17.1 Content rules (critical)
1. Every step has an **official source link** (USCIS, Study in the States, State Dept, DOL, ECFR) and a **"last verified" date**.
2. Content is **written and reviewed by a human** before publishing (`is_published`). AI may draft; a person approves. Ideally ask your school's international office to review.
3. Fees, numeric limits, and dates live in `visa_rules` — steps reference them, never hard-code them.
4. When a related News item appears (§16.2 step 6), affected paths show a banner: "Rules may have changed — re-verifying."
5. Every page ends with: *"This is general information, not legal advice. Your DSO/RO (for F-1/J-1) or an immigration attorney decides what applies to you."*
6. Guidance explains processes; it never tells a user how to get around a rule, and it routes risky situations (status problems, gaps, denials, arrests, travel while pending) to the DSO/attorney.

### 17.2 Path catalog (organized by "Where are you now?")

**🎓 I'm on F-1 (in school)**
- On-campus employment
- **CPT** (Curricular Practical Training) — part-time vs full-time
- **Day-1 CPT** (graduate programs that require practical training from the start)
- Pre-completion OPT
- Changing schools / SEVIS transfer
- Traveling and re-entering the US as a student

**🎓➡️💼 I'm graduating (F-1 → work)**
- **Post-completion OPT** (12 months)
- **STEM OPT extension** (24 months)
- **Cap-gap** (staying in status while an H-1B change of status is pending)
- Starting a second degree vs. OPT (pros/cons — DSO decision)

**💼 Work visas**
- **H-1B cap (lottery)** — registration → selection → petition → start
- **H-1B cap-exempt** (universities, affiliated nonprofits, nonprofit/government research)
- **O-1A / O-1B** (extraordinary ability)
- **L-1** (intracompany transfer, usually after working abroad for the company)
- **Nationality-specific:** **TN** (Canada/Mexico), **E-3** (Australia), **H-1B1** (Chile/Singapore)
- Changing employers on H-1B (portability), H-1B extensions

**🔬 J-1 exchange visitors**
- **Academic Training** (J-1 work authorization via Responsible Officer)
- Two-year home residency requirement (212(e)) & waivers — overview + "talk to an attorney"

**👨‍👩‍👧 Dependents**
- F-2, J-2 (J-2 work authorization), H-4, **H-4 EAD** eligibility

**🟩 Green card paths (overview level)**
- PERM → I-140 → I-485 / consular processing
- **EB-2 NIW**, **EB-1A** (self-petition overview)
- Understanding the monthly Visa Bulletin & priority dates

### 17.3 MVP paths (build these first, deepest detail)
1. F-1 CPT (incl. Day-1 CPT)
2. Post-completion OPT
3. STEM OPT extension
4. H-1B cap lottery (incl. cap-gap)
5. H-1B cap-exempt
6. J-1 Academic Training

### 17.4 Example path structure (draft content — verify every item against official sources before publishing)

#### Path: F-1 → Post-completion OPT
| # | Step | Who | Timing (from `visa_rules`) | Documents |
|---|---|---|---|---|
| 1 | Check eligibility (full-time F-1 for ≥1 academic year; full-time CPT history doesn't block OPT unless it hit the limit) | Student + DSO | Before applying | I-20, transcript |
| 2 | Request OPT recommendation from DSO → new I-20 with OPT recommendation | DSO | Before filing; filing deadline counts from the DSO's SEVIS entry | I-20 (OPT rec.) |
| 3 | File **Form I-765** with USCIS (online or paper), choose start date | Student | Filing window around program end date (e.g., before/after completion — see `visa_rules.opt_filing_window`) | I-765, I-20, I-94, passport, prior EADs, photos, fee |
| 4 | Receive receipt notice (I-797C); track case | USCIS | — | I-797C |
| 5 | Receive **EAD card** — do not work before the EAD start date | USCIS | — | EAD |
| 6 | Report employer & address in **SEVP Portal** | Student | Within the reporting window (`visa_rules.opt_reporting_days`) | Employer info |
| 7 | Stay within **unemployment-day limit**; job must relate to degree | Student | Ongoing (`visa_rules.opt_unemployment_days_limit`) | Offer letters, job descriptions |
| 8 | Plan next step: STEM OPT / H-1B / other | Student | Months before EAD expires | — |

*Common mistakes shown in-app:* filing outside the window, missing photos/signature, working before EAD start date, not reporting employer, unemployment days running out.

#### Path: F-1 → STEM OPT extension
| # | Step | Who | Documents |
|---|---|---|---|
| 1 | Confirm degree is on the **DHS STEM Designated Degree Program List** | Student + DSO | Degree/CIP code |
| 2 | Confirm employer is enrolled in **E-Verify** (Stateside shows this) and offers a qualifying role | Student + Employer | E-Verify number |
| 3 | Complete **Form I-983** training plan with employer | Student + Employer | I-983 |
| 4 | DSO reviews I-983, issues new I-20 with STEM OPT recommendation | DSO | I-20 |
| 5 | File **I-765** before current OPT EAD expires (window in `visa_rules`) | Student | I-765, I-20, current EAD, degree copy, fee |
| 6 | Validation reports, I-983 self-evaluations, report changes | Student + Employer | I-983 evaluations |
| 7 | Track **total unemployment-day limit** across OPT + STEM OPT | Student | — |

#### Path: H-1B cap lottery (from F-1/OPT)
| # | Step | Who | Documents |
|---|---|---|---|
| 1 | Employer agrees to sponsor; confirm role/wage (Stateside shows estimated **wage level**, which affects selection odds under weighted selection) | Employer | Offer letter |
| 2 | Employer submits **electronic registration** during the March window | Employer/Attorney | Passport info, degree info |
| 3 | Selection results announced; check with employer | USCIS | Selection notice |
| 4 | Employer gets **LCA** certified by DOL | Employer | LCA (ETA-9035) |
| 5 | Employer files **Form I-129** petition in the filing window | Employer/Attorney | I-129, degree evaluations, transcripts, I-20s, EADs, pay stubs |
| 6 | **Cap-gap:** if change of status is timely filed, F-1 status/work authorization may be extended | DSO updates I-20 | Receipt notice, cap-gap I-20 |
| 7 | Approval (I-797A/B); H-1B start date | USCIS | I-797 |
| 8 | If not selected: Plan B — cap-exempt employers, STEM OPT, O-1, next season, further study (DSO) | Student | — |

*Live notes pulled from News:* fees/proclamations and their court status, selection method changes — never hard-coded.

#### Path: F-1 CPT & Day-1 CPT
| # | Step | Who | Documents |
|---|---|---|---|
| 1 | Check your school's CPT rules (credit course, timing, ≥1 academic year unless program requires earlier) | Student | School CPT policy |
| 2 | Get an offer that's integral to your curriculum | Student | Offer letter (dates, hours, location, duties) |
| 3 | Apply via school (course registration, advisor approval) | Student + Advisor | CPT request form |
| 4 | DSO authorizes CPT in SEVIS → new I-20 showing employer & dates; **start work only after this** | DSO | Updated I-20 |
| 5 | Understand: ≥12 months **full-time** CPT removes OPT eligibility | Student | — |
| Day-1 | Only for programs that require practical training from the start; ask DSO about long-term risks (future visa/green-card scrutiny) and school accreditation | Student + DSO | Program requirements |

### 17.5 Personal roadmap
- User picks a path (or Stateside suggests one from profile: visa status, graduation date, STEM degree, OPT dates).
- `timing_rule` + user dates → computed **deadline windows** per step (e.g., "OPT filing window: Feb 15 – Jul 14").
- Reminders by email/push before each window opens and closes.
- Progress checklist with document upload *checklist only* (don't store immigration documents in MVP — privacy risk).
- **OPT clock:** unemployment days used / remaining.

### 17.6 "Ask Guidance" assistant
- RAG over **published** Guidance content + cached official pages only.
- Every answer cites the step/page it used, with links.
- Refuses individualized legal advice ("Can I travel while my H-1B is pending?") → explains general rule if documented + "ask your DSO/attorney."
- Logs unanswered questions → content backlog.

### 17.7 How Guidance connects to Jobs
- Job card shows *your* readiness: "STEM OPT eligible here ✅ (E-Verify)", "Cap-exempt employer — no lottery ✅".
- Path pages link to matching jobs (e.g., H-1B cap-exempt path → cap-exempt jobs filter).
- Tracker: when you accept an offer, Stateside suggests the next roadmap (e.g., "Report employer in SEVP Portal").

---

*Disclaimer for the app: Stateside provides job information and historical public data. It is not legal advice. Confirm work authorization with your school's DSO and official USCIS resources.*
