# GCP Deployment Commands
# Copy and paste these commands one by one in your terminal

# Your Project ID
export PROJECT_ID="psyched-silicon-470414-a1"

# 1. Enable required APIs (if not already done)
echo "Enabling APIs..."
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

# 2. Build and push container (this takes 5-10 minutes)
echo "Building container image..."
gcloud builds submit \
  --tag gcr.io/${PROJECT_ID}/talking-drum-api \
  --timeout=20m

# 3. Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy talking-drum-api \
  --image gcr.io/${PROJECT_ID}/talking-drum-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --port 8080 \
  --timeout 300

# 4. Get the service URL
echo "Getting service URL..."
gcloud run services describe talking-drum-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
