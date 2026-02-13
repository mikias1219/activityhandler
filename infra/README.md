# LifeOS — Azure Infrastructure (Bicep)

## Prerequisites

- Azure CLI logged in: `az login`
- Resource group created: `az group create -n lifeos-rg -l eastus`

## Deploy

1. Create a **PostgreSQL** admin password and store in Key Vault or use a secure parameter file.
2. Create **Azure Container Registry** and push your image:
   ```bash
   az acr create -g lifeos-rg -n lifeosacr --sku Basic
   az acr login -n lifeosacr
   docker tag lifeos:latest lifeosacr.azurecr.io/lifeos:latest
   docker push lifeosacr.azurecr.io/lifeos:latest
   ```
3. Edit `main.parameters.json`: set `dockerImage`, `acrLoginServer`, `postgresAdminPassword`.
4. Deploy (from repo root or infra):
   ```bash
   az deployment sub create --location eastus --template-file infra/main.bicep --parameters infra/main.parameters.json
   ```
   Or deploy at resource group scope if you use a RG-scoped template.

## Post-deploy

- **App Service**: Configure App Settings for `DATABASE_URL`, `CACHE_URL`, `SECRET_KEY`, `AZURE_OPENAI_*` etc. from Key Vault or variables.
- **PostgreSQL**: Allow Azure services / your App outbound IP; create database `lifeos` and user.
- **Redis**: Copy connection string to App Settings as `CACHE_URL` and `CELERY_BROKER_URL`.

## GitHub Actions

Use the deploy workflow (`.github/workflows/deploy.yml`) to push image to ACR and deploy to App Service after CI passes.
