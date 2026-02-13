# GitHub Actions — CI and Deploy

LifeOS uses two workflows so that **everything runs automatically** from GitHub: lint, test, build, push to ACR, and deploy to Azure.

## Workflows

### 1. CI (`.github/workflows/ci.yml`)

Runs on every **push** and **pull request** to `main` or `develop`.

- **Lint**: Ruff check and format on `lifeos`, `core`, `users`, `productivity`, `habits`, `finance`, `automation`, `ai_coach`, `web`.
- **Test**: Pytest with PostgreSQL and Redis services; coverage for core, users, productivity, habits, finance, automation, ai_coach.
- **Build**: Docker build (no push) when the push is to `main` or `develop`.

### 2. Deploy (`.github/workflows/deploy.yml`)

Runs **after CI completes successfully** on `main`, or manually via **workflow_dispatch**.

- Logs in to Azure, sets default resource group (`lifeos-rg`).
- Logs in to ACR, builds the image, pushes `latest` and `<sha>`.
- Deploys the image to the Azure Web App.
- Sets app settings: `WEBSITES_PORT=8000`, `LIFEOS_ENV=docker`, `DEBUG=false`, `ALLOWED_HOSTS=.azurewebsites.net`. Optionally `SECRET_KEY` from secret `APP_SECRET_KEY`.
- Restarts the Web App.

So: **push to `main` → CI runs → if green, Deploy runs → app is updated.**

## GitHub setup

### 1. Push the repo to GitHub

```bash
cd lifeos
git init   # if not already
git add .
git commit -m "LifeOS: Django app with CI/CD"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

Or push to the existing activityhandler repo:

```bash
git remote add activityhandler https://github.com/mikias1219/activityhandler.git
git push activityhandler main
```

### 2. Secrets (Settings → Secrets and variables → Actions)

| Secret | Description |
|--------|-------------|
| `AZURE_CREDENTIALS` | JSON from `az ad sp create-for-rbac --scopes /subscriptions/<sub-id>/resourceGroups/lifeos-rg --role Contributor --sdk-auth` |
| `ACR_USERNAME` | ACR admin username (e.g. `lifeosacr`) |
| `ACR_PASSWORD` | ACR admin password (from Azure portal or `az acr credential show`) |
| `APP_SECRET_KEY` | (Optional) Django `SECRET_KEY` for the Web App |

### 3. Variables (optional)

| Variable | Default | Description |
|----------|---------|-------------|
| `AZURE_WEBAPP_NAME` | `lifeos-app` | Web App name (e.g. `lifeos-app-900038`) |
| `AZURE_RESOURCE_GROUP` | `lifeos-rg` | Resource group containing ACR and Web App |

### 4. Environment (optional)

Create an environment named `production` in the repo to use it in the deploy job (e.g. for approval gates).

## Managing the app easily

- **Tasks**: Create, edit, delete, mark done; Today view.  
- **Habits**: Create, edit, delete habits; check in; see streaks.  
- **Finance**: Categories (add/delete), expenses (add/delete), budgets (add/delete), monthly report.  
- **Automation**: Reminders (add/delete), rules (add/delete).  

All from the Web UI at `/app/` after login. API docs at `/api/docs/`.
