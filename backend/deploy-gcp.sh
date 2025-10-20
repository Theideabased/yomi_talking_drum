#!/bin/bash
# GCP Cloud Run Deployment Script for Yoruba Talking Drum Backend

set -e  # Exit on error

echo "🥁 Yoruba Talking Drum Backend - GCP Cloud Run Deployment"
echo "=========================================================="

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-your-gcp-project-id}"
SERVICE_NAME="talking-drum-api"
REGION="${GCP_REGION:-us-central1}"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "📋 Deployment Configuration:"
echo "   Project ID: ${PROJECT_ID}"
echo "   Service Name: ${SERVICE_NAME}"
echo "   Region: ${REGION}"
echo "   Image: ${IMAGE_NAME}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed${NC}"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✅ gcloud CLI found${NC}"

# Check if logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to gcloud${NC}"
    echo "Running: gcloud auth login"
    gcloud auth login
fi

echo -e "${GREEN}✅ Authenticated with gcloud${NC}"

# Set the project
echo ""
echo "Setting GCP project..."
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo ""
echo "🔧 Enabling required GCP APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo -e "${GREEN}✅ APIs enabled${NC}"

# Check if model files exist
echo ""
echo "🔍 Checking model files..."
if [ ! -f "../model/best_model.pth" ]; then
    echo -e "${RED}❌ Model file not found: ../model/best_model.pth${NC}"
    echo "Please train your model first using the Jupyter notebook"
    exit 1
fi

if [ ! -f "../model/scaler.pkl" ]; then
    echo -e "${RED}❌ Scaler file not found: ../model/scaler.pkl${NC}"
    exit 1
fi

if [ ! -f "../model/label_encoder.pkl" ]; then
    echo -e "${RED}❌ Label encoder file not found: ../model/label_encoder.pkl${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All model files found${NC}"

# Build and push the container
echo ""
echo "🏗️  Building and pushing container to Google Container Registry..."
echo "This may take several minutes..."

# Build from the backend directory but include parent context for model files
cd ..
gcloud builds submit \
    --tag ${IMAGE_NAME} \
    --timeout=20m \
    backend/

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Container built and pushed successfully${NC}"

# Deploy to Cloud Run
echo ""
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --port 8080

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Deployment failed${NC}"
    exit 1
fi

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 Deployment Successful!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📡 Your API is now live at:"
echo "   ${SERVICE_URL}"
echo ""
echo "📚 API Documentation:"
echo "   ${SERVICE_URL}/docs"
echo ""
echo "🔧 ReDoc Documentation:"
echo "   ${SERVICE_URL}/redoc"
echo ""
echo "🏥 Health Check:"
echo "   ${SERVICE_URL}/health"
echo ""
echo "🔗 Next Steps:"
echo "   1. Test your API: curl ${SERVICE_URL}/health"
echo "   2. Update your frontend REACT_APP_API_URL to: ${SERVICE_URL}"
echo "   3. Deploy your frontend to Vercel with the new API URL"
echo ""
echo "💡 Useful Commands:"
echo "   View logs: gcloud run services logs read ${SERVICE_NAME} --region ${REGION}"
echo "   Update service: gcloud run services update ${SERVICE_NAME} --region ${REGION}"
echo "   Delete service: gcloud run services delete ${SERVICE_NAME} --region ${REGION}"
echo ""
