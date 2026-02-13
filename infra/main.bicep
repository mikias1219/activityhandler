// LifeOS — Azure infrastructure (Bicep)
// Usage: az deployment group create -g lifeos-rg -f main.bicep -p main.parameters.json

@description('Base name for resources')
param baseName string = 'lifeos'

@description('Docker image for the app')
param dockerImage string

@description('ACR login server')
param acrLoginServer string

@description('PostgreSQL admin login')
param postgresAdminLogin string = 'lifeosadmin'

@secure()
param postgresAdminPassword string

var location = resourceGroup().location

resource plan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: '${baseName}-plan'
  location: location
  sku: { name: 'B1', tier: 'Basic' }
  kind: 'linux'
  properties: { reserved: true }
}

resource web 'Microsoft.Web/sites@2022-09-01' = {
  name: '${baseName}-app'
  location: location
  kind: 'app,linux,container'
  properties: {
    serverFarmId: plan.id
    siteConfig: {
      linuxFxVersion: 'DOCKER|${dockerImage}'
      alwaysOn: true
      appSettings: [
        { name: 'WEBSITES_PORT', value: '8000' }
        { name: 'DOCKER_REGISTRY_SERVER_URL', value: 'https://${acrLoginServer}' }
      ]
    }
    httpsOnly: true
  }
}

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: '${replace(baseName, '-', '')}kv${uniqueString(resourceGroup().id)}'
  location: location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    enableRbacAuthorization: true
  }
}

resource pg 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: '${baseName}-pg'
  location: location
  sku: { name: 'Standard_B1ms', tier: 'Burstable' }
  properties: {
    version: '15'
    administratorLogin: postgresAdminLogin
    administratorLoginPassword: postgresAdminPassword
    storage: { storageSizeGB: 32 }
    backup: { backupRetentionDays: 7 }
    highAvailability: { mode: 'Disabled' }
  }
}

resource redis 'Microsoft.Cache/redis@2023-08-01' = {
  name: '${baseName}-redis'
  location: location
  properties: {
    sku: { name: 'Basic', family: 'C', capacity: 0 }
    enableNonSslPort: false
    minimumTlsVersion: '1.2'
  }
}

output appName string = web.name
output keyVaultName string = kv.name
output postgresFqdn string = pg.properties.fullyQualifiedDomainName
output redisHost string = redis.properties.hostName
