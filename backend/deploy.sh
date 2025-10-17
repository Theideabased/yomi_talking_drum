#!/bin/bash
# GCP Deployment Script for Talking Drum API

set -e  # Exit on any error

# Configuration
PROJECT_ID="${PROJECT_ID:-your-gcp-project-id}"
SERVICE_NAME="talking-drum-api"
REGION="${REGION:-us-central1}"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 DEPLOYING TALKING DRUM API TO GOOGLE CLOUD RUN"
echo "=================================================="
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"
echo "Region: $REGION"
echo "Image: $IMAGE_NAME"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install it first:"
    echo "   https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if logged in
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not logged into gcloud. Please run:"
    echo "   gcloud auth login"
    exit 1
fi

# Check if project is set
if [ "$PROJECT_ID" = "your-gcp-project-id" ]; then
    echo "❌ Please set your PROJECT_ID:"
    echo "   export PROJECT_ID=your-actual-project-id"
    echo "   Or edit this script to set the PROJECT_ID variable"
    exit 1
fi

echo "🔧 Setting up GCP project..."
gcloud config set project $PROJECT_ID

echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo "🐳 Building Docker image..."
# Copy model files to backend directory first
cp -r ../model ./model/ || echo "⚠️  Model files not found, will create dummy files"

# Build and push image
gcloud builds submit --tag $IMAGE_NAME .

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --allow-unauthenticated \
    --port 8000

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your API is now available at:"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
echo "   $SERVICE_URL"
echo ""
echo "📚 API Documentation:"
echo "   $SERVICE_URL/docs"
echo ""
echo "🔍 Test your API:"
echo "   curl $SERVICE_URL/health"
echo ""
echo "📊 Monitor your service:"
echo "   https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME"
