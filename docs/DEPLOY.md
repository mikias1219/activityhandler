# LifeOS — Deploy to Azure (activityhandler repo)

## 1. Push code to activityhandler

```bash
cd /path/to/lifeos
git remote add activityhandler https://github.com/mikias1219/activityhandler.git
git push activityhandler main
```

## 2. GitHub Secrets (Settings → Secrets and variables → Actions)

| Secret | Description |
|--------|-------------|
| `AZURE_CREDENTIALS` | JSON from `az ad sp create-for-rbac --name lifeos-github --role contributor --scopes /subscriptions/<sub-id>/resourceGroups/lifeos-rg --sdk-auth` |
| `ACR_USERNAME` | Azure Container Registry username (Admin enabled, or AAD) |
| `ACR_PASSWORD` | ACR admin password or service principal secret |

## 3. Azure setup (one-time)

1. **Resource group**
   ```bash
   az group create -n lifeos-rg -l eastus
   ```

2. **Container Registry**
   ```bash
   az acr create -g lifeos-rg -n lifeosacr --sku Basic
   az acr update -n lifeosacr --admin-enabled true
   az acr credential show -n lifeosacr  # use for ACR_USERNAME / ACR_PASSWORD
   ```

3. **Bicep (optional)** — deploy App Service, PostgreSQL, Redis, Key Vault:
   ```bash
   az deployment group create -g lifeos-rg -f infra/main.bicep -p infra/main.parameters.json
   ```
   Then set App Service app settings: `DATABASE_URL`, `CACHE_URL`, `SECRET_KEY`, etc.

## 4. Deploy workflow

- **CI** runs on push/PR to `main` or `develop`: lint, test, build image.
- **Deploy** runs after CI succeeds on `main` (or via "Run workflow"): pushes image to ACR, deploys to Azure Web App `lifeos-app`.

Update `.github/workflows/deploy.yml` env `AZURE_WEBAPP_NAME` and `REGISTRY` to match your names.
