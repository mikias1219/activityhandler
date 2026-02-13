# Why You Saw "Application Error" and How It Was Fixed

## What you saw

Opening your Azure app (e.g. `https://lifeos-app-900038.azurewebsites.net`) showed:

**"Application Error – If you are the application administrator, you can access the diagnostic resources."**

That means the container **exited or never started correctly**, so Azure has nothing to serve.

---

## Why it wasn’t working

### 1. **Wrong database path (main cause)**

- App settings had: `DATABASE_URL=sqlite:////home/site/wwwroot/db.sqlite3`
- `/home/site/wwwroot` is used for **code deployment** (zip deploy), not for **custom Docker** apps.
- In a custom container, that path often **doesn’t exist** or isn’t writable.
- Django tried to run `migrate` and create the DB file there → **failed** → process exited → **Application Error**.

**Fix:** In Docker we now use **`/app/db.sqlite3`** (inside the image, writable). No `DATABASE_URL` is set in Azure so the app uses this path automatically.

### 2. **Redis required**

- Default settings used Redis for cache.
- The container had **no Redis**.
- First request (or startup) that touched the cache could **hang or fail** and contribute to the error.

**Fix:** When `LIFEOS_ENV=docker` and `CACHE_URL` is not set, we use **DummyCache** so the app runs without Redis.

### 3. **Startup stopped on first failure**

- The run command was: `migrate && collectstatic && gunicorn ...`
- If `migrate` failed, the rest **never ran**, so Gunicorn never started and the app never listened on port 8000.

**Fix:** Switched to `migrate; collectstatic; gunicorn ...` so Gunicorn **always starts**. If migrate fails, you still get a running process and can see errors in logs.

### 4. **Settings not loaded as “docker”**

- Docker settings (SQLite in `/app`, DummyCache) only load when `LIFEOS_ENV=docker`.
- If that env var wasn’t set in the container, the app used **development-style** settings (e.g. DB path from base settings) and could fail.

**Fix:** The Dockerfile now sets **`LIFEOS_ENV=docker`** (and `DJANGO_SETTINGS_MODULE=lifeos.settings`) so the container always uses the Docker settings even if Azure doesn’t pass the variable.

---

## Domain / app name (rename)

- Your live URL is: **`https://<APP_NAME>.azurewebsites.net`**
- Script default is **`lifeos-app`** → **`https://lifeos-app.azurewebsites.net`**
- To use another name (e.g. `mylifeos` → `https://mylifeos.azurewebsites.net`), create the Web App with that name or set **`LIFEOS_APP=mylifeos`** when running the script. Names must be **globally unique** in Azure.

If you already have `lifeos-app-900038`, you can keep using it or create a **new** Web App with a cleaner name (e.g. `lifeos-app`) and point it at the same image; Azure doesn’t let you rename an existing Web App.

---

## What to do now

1. **Rebuild and push the image** (from project root):
   ```bash
   docker build -t lifeosacr.azurecr.io/lifeos:latest .
   az acr login --name lifeosacr
   docker push lifeosacr.azurecr.io/lifeos:latest
   ```

2. **Set app settings and restart** (replace `YOUR_APP_NAME` with your Web App name, e.g. `lifeos-app` or `lifeos-app-900038`):
   ```bash
   export LIFEOS_APP=YOUR_APP_NAME
   bash scripts/azure-deploy-only.sh
   ```
   Or manually:
   ```bash
   az webapp config appsettings set --resource-group lifeos-rg --name YOUR_APP_NAME \
     --settings WEBSITES_PORT=8000 LIFEOS_ENV=docker SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(50))')" DEBUG=false ALLOWED_HOSTS=".azurewebsites.net" \
     --output none
   az webapp restart --resource-group lifeos-rg --name YOUR_APP_NAME
   ```

3. Wait 1–2 minutes and open: **https://YOUR_APP_NAME.azurewebsites.net**

If **ACR login** fails with "Resource ... under resource group 'AI-102' was not found", the CLI default resource group is wrong. The deploy script now sets the default to `lifeos-rg` so ACR is found. To fix it manually and rerun:
```bash
az configure --defaults group=lifeos-rg
# and/or if needed:
az account set --subscription "Microsoft Azure Sponsorship"
LIFEOS_APP=lifeos-app-900038 bash scripts/azure-deploy-only.sh
```

If the app still shows "Application Error", check logs:
```bash
az webapp log tail --resource-group lifeos-rg --name YOUR_APP_NAME
```
