#!/usr/bin/env bash
# LifeOS — Create Azure resources and make the app live
# Prerequisites: az login, Docker
set -e

RESOURCE_GROUP="${LIFEOS_RG:-lifeos-rg}"
LOCATION="${LIFEOS_LOCATION:-eastus}"
ACR_NAME="${LIFEOS_ACR:-lifeosacr}"
APP_NAME="${LIFEOS_APP:-lifeos-app}"
PLAN_NAME="${LIFEOS_PLAN:-lifeos-plan}"
IMAGE_NAME="lifeos"
IMAGE_TAG="${IMAGE_TAG:-latest}"

echo "=== Creating resource group: $RESOURCE_GROUP ==="
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output none

echo "=== Creating Container Registry: $ACR_NAME ==="
az acr create --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" --sku Basic --admin-enabled true --output none

echo "=== Creating App Service plan: $PLAN_NAME (Linux B1) ==="
az appservice plan create --resource-group "$RESOURCE_GROUP" --name "$PLAN_NAME" --is-linux --sku B1 --output none

echo "=== Creating Web App (container): $APP_NAME ==="
az webapp create --resource-group "$RESOURCE_GROUP" --plan "$PLAN_NAME" --name "$APP_NAME" --deployment-container-image-name "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}" --output none

echo "=== Enabling admin credentials and getting ACR login ==="
ACR_USER=$(az acr credential show --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" --query username -o tsv)
ACR_PASS=$(az acr credential show --resource-group "$RESOURCE_GROUP" --name "$ACR_NAME" --query "passwords[0].value" -o tsv)

echo "=== Configuring Web App to use ACR ==="
az webapp config container set --resource-group "$RESOURCE_GROUP" --name "$APP_NAME" \
  --docker-custom-image-name "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}" \
  --docker-registry-server-url "https://${ACR_NAME}.azurecr.io" \
  --docker-registry-server-user "$ACR_USER" \
  --docker-registry-server-password "$ACR_PASS" \
  --output none

echo "=== Setting app settings (SQLite in /app; no Redis required) ==="
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))" 2>/dev/null || openssl rand -base64 40)
az webapp config appsettings set --resource-group "$RESOURCE_GROUP" --name "$APP_NAME" \
  --settings \
    WEBSITES_PORT=8000 \
    LIFEOS_ENV=docker \
    SECRET_KEY="$SECRET_KEY" \
    DEBUG=false \
    ALLOWED_HOSTS=".azurewebsites.net" \
  --output none

echo "=== Build and push Docker image (run from project root) ==="
echo "Logging into ACR..."
az acr login --name "$ACR_NAME"
echo "Building image..."
docker build -t "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}" -t "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:latest" .
echo "Pushing image..."
docker push "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${IMAGE_TAG}"
docker push "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:latest"

echo "=== Restarting Web App ==="
az webapp restart --resource-group "$RESOURCE_GROUP" --name "$APP_NAME" --output none

APP_URL="https://${APP_NAME}.azurewebsites.net"
echo ""
echo "=== Done ==="
echo "App URL: $APP_URL"
echo "Give it 1-2 minutes to start, then open: $APP_URL"
echo "To use PostgreSQL/Redis later, create them and set DATABASE_URL and CACHE_URL in App Settings."
