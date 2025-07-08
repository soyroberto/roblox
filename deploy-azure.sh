#!/bin/bash

# Azure Deployment Script for Roblox Architecture Explained
# This script deploys the application to Azure Static Web Apps

set -e

echo "🚀 Starting Azure deployment..."

# Configuration
RESOURCE_GROUP="roblox-architecture-rg"
STATIC_APP_NAME="roblox-architecture-app"
LOCATION="East US"
STORAGE_ACCOUNT="robloxarchstorage$(date +%s)"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first:"
    echo "   brew install azure-cli"
    exit 1
fi

# Login to Azure
echo "🔐 Logging into Azure..."
az login

# Create resource group
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location "$LOCATION"

# Option 1: Deploy as Static Web App (Recommended)
deploy_static_web_app() {
    echo "🌐 Deploying to Azure Static Web Apps..."
    
    # Build frontend
    echo "🏗️ Building frontend..."
    cd frontend
    yarn build
    cd ..
    
    # Create static web app
    az staticwebapp create \
        --name $STATIC_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --location "$LOCATION" \
        --source "https://github.com/your-username/your-repo" \
        --branch main \
        --app-location "/frontend" \
        --api-location "/backend" \
        --build-location "build"
    
    echo "✅ Static Web App deployed!"
    echo "🔗 URL: https://$STATIC_APP_NAME.azurestaticapps.net"
}

# Option 2: Deploy to Storage Account
deploy_storage_account() {
    echo "💾 Deploying to Azure Storage Account..."
    
    # Build frontend
    echo "🏗️ Building frontend..."
    cd frontend
    yarn build
    cd ..
    
    # Create storage account
    az storage account create \
        --name $STORAGE_ACCOUNT \
        --resource-group $RESOURCE_GROUP \
        --location "$LOCATION" \
        --sku Standard_LRS
    
    # Enable static website hosting
    az storage blob service-properties update \
        --account-name $STORAGE_ACCOUNT \
        --static-website \
        --index-document index.html \
        --404-document index.html
    
    # Upload build files
    az storage blob upload-batch \
        --account-name $STORAGE_ACCOUNT \
        --source frontend/build \
        --destination '$web'
    
    # Get website URL
    WEBSITE_URL=$(az storage account show -n $STORAGE_ACCOUNT -g $RESOURCE_GROUP --query "primaryEndpoints.web" --output tsv)
    
    echo "✅ Storage Account deployment complete!"
    echo "🔗 URL: $WEBSITE_URL"
}

# Option 3: Deploy backend to Azure Functions
deploy_backend_functions() {
    echo "⚡ Deploying backend to Azure Functions..."
    
    FUNCTION_APP_NAME="roblox-arch-functions-$(date +%s)"
    
    # Create Function App
    az functionapp create \
        --resource-group $RESOURCE_GROUP \
        --consumption-plan-location "$LOCATION" \
        --runtime python \
        --runtime-version 3.9 \
        --functions-version 4 \
        --name $FUNCTION_APP_NAME \
        --storage-account $STORAGE_ACCOUNT
    
    # Deploy function code
    cd backend
    func azure functionapp publish $FUNCTION_APP_NAME
    cd ..
    
    echo "✅ Function App deployed!"
    echo "🔗 API URL: https://$FUNCTION_APP_NAME.azurewebsites.net"
}

# Main deployment menu
echo "Choose deployment option:"
echo "1) Static Web App (Full stack - Recommended)"
echo "2) Storage Account (Frontend only)"
echo "3) Functions + Storage (Full stack)"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        deploy_static_web_app
        ;;
    2)
        deploy_storage_account
        ;;
    3)
        deploy_storage_account
        deploy_backend_functions
        echo "🔄 Update frontend .env with function app URL and redeploy"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo "🎉 Deployment complete!"
echo "📋 Next steps:"
echo "   1. Update DNS records if using custom domain"
echo "   2. Configure environment variables in Azure portal"
echo "   3. Set up monitoring and alerts"
echo "   4. Configure CI/CD pipeline if needed"