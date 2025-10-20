#!/bin/bash
# Quick GCP Deployment - Interactive Setup

echo "🥁 Yoruba Talking Drum - GCP Deployment Setup"
echo "=============================================="
echo ""

# Prompt for project ID
read -p "Enter your GCP Project ID: " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Project ID is required"
    exit 1
fi

echo ""
echo "📋 Configuration:"
echo "   Project ID: $PROJECT_ID"
echo "   Service: talking-drum-api"
echo "   Region: us-central1"
echo ""

# Login check
echo "1️⃣ Checking authentication..."
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | grep -q "@"; then
    echo "Please login to gcloud:"
    gcloud auth login
fi

# Set project
echo ""
echo "2️⃣ Setting project..."
gcloud config set project $PROJECT_ID

# Enable APIs
echo ""
echo "3️⃣ Enabling APIs (this may take a moment)..."
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable run.googleapis.com --quiet
gcloud services enable containerregistry.googleapis.com --quiet

echo "✅ APIs enabled"

# Check model files
echo ""
echo "4️⃣ Verifying model files..."
cd /home/user/Documents/yomi_talking_drum

if [ ! -f "model/best_model.pth" ]; then
    echo "❌ Model not found! Please train your model first."
    exit 1
fi

echo "✅ Model files verified"

# Build and deploy
echo ""
echo "5️⃣ Building and deploying (this will take 5-10 minutes)..."
echo ""

gcloud builds submit \
    --tag gcr.io/$PROJECT_ID/talking-drum-api \
    --timeout=20m

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo ""
echo "6️⃣ Deploying to Cloud Run..."

gcloud run deploy talking-drum-api \
    --image gcr.io/$PROJECT_ID/talking-drum-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --port 8080 \
    --quiet

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed"
    exit 1
fi

# Get URL
URL=$(gcloud run services describe talking-drum-api \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)')

echo ""
echo "=========================================="
echo "🎉 DEPLOYMENT SUCCESSFUL!"
echo "=========================================="
echo ""
echo "🔗 Your API URL:"
echo "   $URL"
echo ""
echo "📝 Next steps:"
echo "   1. Test: curl $URL/health"
echo "   2. Update frontend REACT_APP_API_URL=$URL"
echo "   3. Deploy frontend to Vercel"
echo ""

# Save URL to file
echo $URL > backend/deployed_url.txt
echo "💾 URL saved to backend/deployed_url.txt"
