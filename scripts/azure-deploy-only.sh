#!/usr/bin/env bash
# LifeOS — Build, push image, update settings, restart (resources must already exist)
set -e

RESOURCE_GROUP="${LIFEOS_RG:-lifeos-rg}"
APP_NAME="${LIFEOS_APP:-lifeos-app}"
ACR_NAME="${LIFEOS_ACR:-lifeosacr}"
IMAGE_NAME="lifeos"

# Use subscription that contains lifeos-rg and set default RG (avoids ACR "not found" under AI-102)
SUB_ID=$(az group show --name "$RESOURCE_GROUP" --query id -o tsv 2>/dev/null | cut -d'/' -f3)
if [ -n "$SUB_ID" ]; then
  az account set --subscription "$SUB_ID"
fi
az configure --defaults group="$RESOURCE_GROUP" -o none 2>/dev/null || true

echo "=== Build image ==="
docker build -t "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:latest" .

echo "=== Push to ACR ==="
az acr login --name "$ACR_NAME"
docker push "${ACR_NAME}.azurecr.io/${IMAGE_NAME}:latest"

echo "=== App settings (SQLite in /app, no Redis) ==="
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))" 2>/dev/null || openssl rand -base64 40)
az webapp config appsettings set --resource-group "$RESOURCE_GROUP" --name "$APP_NAME" \
  --settings \
    WEBSITES_PORT=8000 \
    LIFEOS_ENV=docker \
    SECRET_KEY="$SECRET_KEY" \
    DEBUG=false \
    ALLOWED_HOSTS=".azurewebsites.net" \
  --output none

echo "=== Restart ==="
az webapp restart --resource-group "$RESOURCE_GROUP" --name "$APP_NAME" --output none

echo ""
echo "Done. App URL: https://${APP_NAME}.azurewebsites.net"
echo "Wait 1–2 minutes then open the URL."
