# LifeOS — Personal Life Operating System

A modular system to **monitor, control, optimize, and improve** every area of your life. Built with Django, Docker, and Azure.

## 📁 Project structure

```
lifeos/
├── docs/                 # Architecture, MVP scope, database schema
├── lifeos/               # Django project config
│   ├── settings/         # base, development, docker, production
│   ├── urls.py
│   └── wsgi.py
├── core/                 # Audit, health, feature flags
├── users/                # Custom user, JWT auth
├── productivity/         # Tasks, daily planner, Eisenhower priority
├── habits/               # Habit tracker, check-ins, streaks
├── finance/              # Expenses, categories, budgets, reports
├── ai_coach/             # AI: "what should I do now?", optional OpenAI
├── automation/           # Phase 2: IFTTT rules, reminders
├── infra/                # Azure Bicep (App Service, PostgreSQL, Redis, Key Vault)
├── requirements/
├── docker-compose.yml
├── Dockerfile
├── .github/workflows/ci.yml
└── .github/workflows/deploy.yml   # ACR push + App Service deploy
```

## 🚀 Quick start (local)

1. **Clone and enter project**
   ```bash
   cd lifeos
   ```

2. **Create virtualenv and install deps**
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # or .venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Environment**
   ```bash
   cp .env.example .env
   # Edit .env if needed (DB, Redis)
   ```

4. **Database**
   - Option A — PostgreSQL + Redis via Docker:
     ```bash
     docker-compose up -d db redis
     cp .env.example .env   # DATABASE_URL=postgresql://lifeos:lifeos@localhost:5432/lifeos
     python manage.py migrate
     python manage.py createsuperuser
     ```
   - Option B — SQLite (no Docker) for quick local try:
     ```bash
     # Use absolute path for SQLite
     export DATABASE_URL=sqlite:////tmp/lifeos.db
     python manage.py migrate
     python manage.py createsuperuser
     ```
   - Cache: set `CACHE_URL=redis://localhost:6379/0` or leave default (Redis required for full stack).

5. **Run server**
   ```bash
   python manage.py runserver
   ```
   - API: http://127.0.0.1:8000/api/v1/
   - Swagger: http://127.0.0.1:8000/api/docs/
   - Health: http://127.0.0.1:8000/api/health/

## 🌐 Web UI — manage everything easily

A **full UI** with **full CRUD** for every area: login, register, password reset, dashboard (AI “what to do now”), **tasks** (create, edit, delete, mark done, today view), **habits** (create, edit, delete, check-in, streaks), **finance** (categories, expenses, budgets: add/delete; monthly report), **automation** (reminders and rules: add/delete). Open the app root (e.g. http://127.0.0.1:8000/) and sign in. See [docs/UI_AND_DEPLOY.md](docs/UI_AND_DEPLOY.md) and [docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md).

## 🐳 Run with Docker Compose

```bash
docker-compose up -d db redis
docker-compose run --rm web python manage.py migrate
docker-compose up web
```

## 📌 Features

- **Auth**: Register, login (JWT), refresh, **password reset (email)**, me
- **Productivity**: Tasks (CRUD, today view, Eisenhower priority)
- **Habits**: Habits, check-ins, streaks
- **Finance**: Expense categories, expenses, budgets, report by month
- **AI Coach**: `GET /api/v1/ai/what-to-do-now/` — suggestions from tasks + habits (optional Azure/OpenAI)
- **Phase 2 — Automation**: IFTTT-style rules, reminders (`/api/v1/automation/rules/`, `/api/v1/automation/reminders/`)
- **Calendar alignment**: See [docs/CALENDAR_ALIGNMENT.md](docs/CALENDAR_ALIGNMENT.md) (Africa/Addis_Ababa, your weekly routine)
- **API**: REST, OpenAPI at `/api/docs/`
- **DevOps**: CI (lint, test, build), **Deploy** (ACR + Azure App Service), **Azure Bicep** in `infra/`

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/MVP_SCOPE.md](docs/MVP_SCOPE.md).

## ☁️ Azure deploy (live URL)

Default Web App name: **`lifeos-app`** → **https://lifeos-app.azurewebsites.net** (must be globally unique).

```bash
# One-time: create resources
bash scripts/azure-create-resources.sh

# Or just redeploy (resources exist)
LIFEOS_APP=lifeos-app bash scripts/azure-deploy-only.sh
```

If you see **"Application Error"**, see **docs/WHY_IT_FAILED.md** and run `scripts/azure-deploy-only.sh` after rebuilding the image.

## 📦 Add everything to GitHub + Actions

1. **Push to GitHub** (new repo or activityhandler):
   ```bash
   git init && git add . && git commit -m "LifeOS with CI/CD and full CRUD"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git branch -M main && git push -u origin main
   ```
   Or: `git remote add activityhandler https://github.com/mikias1219/activityhandler.git` then `git push activityhandler main`.

2. **Configure GitHub Actions** (Settings → Secrets and variables → Actions):
   - **Secrets**: `AZURE_CREDENTIALS`, `ACR_USERNAME`, `ACR_PASSWORD`; optional `APP_SECRET_KEY` for Django.
   - **Variables** (optional): `AZURE_WEBAPP_NAME` (e.g. `lifeos-app-900038`), `AZURE_RESOURCE_GROUP` (default `lifeos-rg`).

3. **What Actions do**: On every push to `main`, **CI** runs (lint, test, Docker build). If CI succeeds, **Deploy** runs: build image, push to ACR, deploy to Azure Web App, set app settings, restart. So one push updates the live app. See [docs/GITHUB_ACTIONS.md](docs/GITHUB_ACTIONS.md).

## 🧪 Tests

```bash
# Requires: PostgreSQL and Redis (e.g. docker-compose up -d db redis)
export DATABASE_URL=postgresql://lifeos:lifeos@localhost:5432/lifeos_test
pytest
```

## 📜 License

Private / your choice.
