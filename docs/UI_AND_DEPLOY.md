# LifeOS — Web UI and Azure Deploy

## Web UI (fully functional)

The app includes a **template-based UI** that uses all LifeOS features:

| Page | URL | Features |
|------|-----|----------|
| Login | `/login/` | Email + password, JWT stored in localStorage |
| Register | `/register/` | Create account |
| Password reset | `/password-reset/` | Request link; confirm at `/password-reset/confirm/?uid=...&token=...` |
| Dashboard | `/app/` | AI "What should I do now?", links to Tasks, Habits, Finance |
| Tasks | `/app/tasks/` | List, Today view, create/edit/delete, mark done, Eisenhower priority |
| Habits | `/app/habits/` | Create habits, check in today, streak |
| Finance | `/app/finance/` | Categories, add expense, monthly report, recent expenses |
| Automation | `/app/automation/` | Reminders, rules (IFTTT-style) |

- **Tech**: Django templates, Tailwind CSS (CDN), vanilla JS with `lifeos` API helper (JWT refresh, auth redirect).
- **Static**: `/static/js/app.js`, `tasks.js`, `habits.js`, `finance.js` (and WhiteNoise in production).
- **Root** `/` redirects to `/app/` (dashboard). Unauthenticated users are redirected to `/login/` by the frontend.

### Run UI locally

```bash
cd lifeos
LIFEOS_ENV=development SECRET_KEY=dev DATABASE_URL=sqlite:////tmp/lifeos.db python manage.py migrate
python manage.py runserver
# Open http://127.0.0.1:8000/ → login or register, then use the app.
```

---

## Azure — create resources and go live

You already have:

- **Resource group**: `lifeos-rg` (eastus)
- **ACR**: `lifeosacr` in `lifeos-rg`
- **App Service plan**: `lifeos-plan`
- **Web App**: use **`lifeos-app`** for a clean URL: **https://lifeos-app.azurewebsites.net** (must be globally unique; if taken, use e.g. `LIFEOS_APP=mylifeos` when creating)

### 1. Use the correct subscription and push image

If `az acr login` fails with "Resource ... under resource group 'AI-102' was not found", set the resource group and subscription:

```bash
# List your subscriptions and pick the one that has lifeos-rg
az account list -o table
az account set --subscription "YOUR_SUBSCRIPTION_ID_OR_NAME"

# Login to ACR (ACR is in lifeos-rg)
az acr login --name lifeosacr
```

### 2. Push the image

From the **lifeos** project root (where the Dockerfile is):

```bash
docker tag lifeosacr.azurecr.io/lifeos:latest lifeosacr.azurecr.io/lifeos:latest
docker push lifeosacr.azurecr.io/lifeos:latest
```

If ACR is in a different subscription, ensure `az account set` is that subscription before `az acr login`.

### 3. Configure the Web App

Point the Web App to your ACR and set app settings:

```bash
RESOURCE_GROUP=lifeos-rg
APP_NAME=lifeos-app          # your web app name → https://lifeos-app.azurewebsites.net
ACR_NAME=lifeosacr

# Get ACR credentials (use --resource-group so it finds lifeosacr in lifeos-rg)
ACR_USER=$(az acr credential show --resource-group $RESOURCE_GROUP --name $ACR_NAME --query username -o tsv)
ACR_PASS=$(az acr credential show --resource-group $RESOURCE_GROUP --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Configure container
az webapp config container set --resource-group $RESOURCE_GROUP --name $APP_NAME \
  --docker-custom-image-name "${ACR_NAME}.azurecr.io/lifeos:latest" \
  --docker-registry-server-url "https://${ACR_NAME}.azurecr.io" \
  --docker-registry-server-user "$ACR_USER" \
  --docker-registry-server-password "$ACR_PASS"

# App settings: SQLite in /app (writable in container). Omit DATABASE_URL to use /app/db.sqlite3.
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
az webapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP_NAME \
  --settings WEBSITES_PORT=8000 LIFEOS_ENV=docker SECRET_KEY="$SECRET_KEY" DEBUG=false \
    ALLOWED_HOSTS=".azurewebsites.net" \
  --output none

# Restart
az webapp restart --resource-group $RESOURCE_GROUP --name $APP_NAME
```

### 4. Open the app

**https://lifeos-app.azurewebsites.net** (or your `APP_NAME`)

Give it 1–2 minutes after the first deploy. Register a user and use the full UI.

### 5. If you see "Application Error"

See **docs/WHY_IT_FAILED.md** for causes and fixes. Quick redeploy:

```bash
# From project root; set LIFEOS_APP to your actual Web App name if different
LIFEOS_APP=lifeos-app bash scripts/azure-deploy-only.sh
```

### One-command script (after fixing subscription)

From project root:

```bash
LIFEOS_RG=lifeos-rg LIFEOS_APP=lifeos-app-900038 bash scripts/azure-create-resources.sh
```

The script creates RG/ACR/Plan/App (if missing), configures the app, builds and pushes the image, and restarts the Web App. Ensure your Azure CLI default subscription is the one that contains `lifeos-rg` (or set it with `az account set`).
