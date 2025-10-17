# 🚀 Deploy Talking Drum API to Google Cloud Platform

## Prerequisites

1. **Google Cloud Account**: [Create one here](https://cloud.google.com/)
2. **GCP Project**: Create a new project in the [GCP Console](https://console.cloud.google.com/)
3. **gcloud CLI**: [Install gcloud](https://cloud.google.com/sdk/docs/install)

---

## 🔧 Quick Setup (5 minutes)

### Step 1: Install and Setup gcloud CLI

```bash
# Install gcloud (if not already installed)
# For Ubuntu/Debian:
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# For macOS:
brew install --cask google-cloud-sdk

# For Windows:
# Download and run the installer from https://cloud.google.com/sdk/docs/install
```

### Step 2: Authenticate and Setup Project

```bash
# Login to your Google account
gcloud auth login

# Set your project ID (replace with your actual project ID)
export PROJECT_ID="your-talking-drum-project"
gcloud config set project $PROJECT_ID

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
```

### Step 3: Deploy Your API

```bash
# Navigate to backend directory
cd /home/user/Documents/yomi_talking_drum/backend

# Set your project ID in the script
export PROJECT_ID="your-talking-drum-project"

# Run the deployment script
./deploy.sh
```

---

## 🌍 Alternative Deployment Methods

### Method 1: One-Command Deploy (Recommended)

```bash
cd backend
export PROJECT_ID="your-project-id"
./deploy.sh
```

### Method 2: Manual Deploy

```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Build image
gcloud builds submit --tag gcr.io/$PROJECT_ID/talking-drum-api

# Deploy to Cloud Run
gcloud run deploy talking-drum-api \
  --image gcr.io/$PROJECT_ID/talking-drum-api \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --allow-unauthenticated
```

### Method 3: Deploy with Custom Domain

```bash
# Deploy with custom domain
gcloud run deploy talking-drum-api \
  --image gcr.io/$PROJECT_ID/talking-drum-api \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --allow-unauthenticated

# Map custom domain (optional)
gcloud run domain-mappings create \
  --service talking-drum-api \
  --domain your-custom-domain.com \
  --region us-central1
```

---

## 💰 Cost Estimation

**Cloud Run Pricing** (Pay-per-use):
- **Free Tier**: 2 million requests/month, 400,000 GB-seconds/month
- **After Free Tier**: ~$0.40 per million requests
- **Memory**: ~$0.0000025 per GB-second
- **CPU**: ~$0.0000100 per vCPU-second

**Your API Cost Estimate**:
- Light usage (1000 requests/day): **FREE**
- Medium usage (10,000 requests/day): **~$5/month**
- Heavy usage (100,000 requests/day): **~$50/month**

---

## 🔧 Configuration Options

### Environment Variables

```bash
# Set environment variables during deployment
gcloud run deploy talking-drum-api \
  --set-env-vars="MODEL_PATH=/app/model,DEBUG=false"
```

### Resource Limits

```bash
# Configure resources
gcloud run deploy talking-drum-api \
  --memory=4Gi \
  --cpu=4 \
  --timeout=600 \
  --max-instances=20 \
  --min-instances=1
```

### Security & Authentication

```bash
# Deploy with authentication required
gcloud run deploy talking-drum-api \
  --no-allow-unauthenticated

# Create service account for API access
gcloud iam service-accounts create talking-drum-api-sa

# Grant access to specific users
gcloud run services add-iam-policy-binding talking-drum-api \
  --member="user:your-email@domain.com" \
  --role="roles/run.invoker"
```

---

## 🧪 Testing Your Deployed API

After deployment, you'll get a URL like: `https://talking-drum-api-xyz-uc.a.run.app`

```bash
# Get your service URL
SERVICE_URL=$(gcloud run services describe talking-drum-api --region=us-central1 --format="value(status.url)")

# Test health endpoint
curl $SERVICE_URL/health

# Test prediction endpoint
curl -X POST "$SERVICE_URL/predict" \
  -F "file=@/path/to/audio/sample.wav"

# Visit API documentation
open $SERVICE_URL/docs
```

---

## 🔍 Monitoring & Logs

### View Logs
```bash
# Real-time logs
gcloud run logs tail talking-drum-api --region=us-central1

# Recent logs
gcloud run logs read talking-drum-api --region=us-central1 --limit=50
```

### Monitoring Dashboard
- Visit: [Cloud Run Console](https://console.cloud.google.com/run)
- Click on your service
- View metrics: requests, latency, errors, CPU, memory

---

## 🔄 Updates & Rollbacks

### Update Your API
```bash
# Build new version
gcloud builds submit --tag gcr.io/$PROJECT_ID/talking-drum-api:v2

# Deploy new version
gcloud run deploy talking-drum-api \
  --image gcr.io/$PROJECT_ID/talking-drum-api:v2
```

### Rollback
```bash
# List revisions
gcloud run revisions list --service=talking-drum-api

# Rollback to previous version
gcloud run services update-traffic talking-drum-api \
  --to-revisions=talking-drum-api-00001-abc=100
```

---

## 🛡️ Security Best Practices

1. **Use Secret Manager for sensitive data**:
```bash
# Store model files in Secret Manager
gcloud secrets create model-files --data-file=model.zip
```

2. **Enable VPC Access** (if needed):
```bash
gcloud run deploy talking-drum-api \
  --vpc-connector=your-connector
```

3. **Set up Cloud Armor** (DDoS protection):
```bash
gcloud compute security-policies create talking-drum-policy
```

---

## 🚀 Frontend Deployment

Deploy your React frontend to **Firebase Hosting**:

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login and init
firebase login
firebase init hosting

# Update API URL in frontend
# Edit src/App.js: const API_URL = "https://your-api-url"

# Build and deploy
npm run build
firebase deploy
```

---

## 📞 Support & Troubleshooting

### Common Issues:

1. **"Service not found"**: Check project ID and region
2. **"Permission denied"**: Run `gcloud auth login`
3. **"Build failed"**: Check Dockerfile and dependencies
4. **"Cold starts"**: Set min-instances > 0
5. **"Timeout"**: Increase timeout in deploy command

### Get Help:
```bash
# Check service status
gcloud run services describe talking-drum-api --region=us-central1

# Debug logs
gcloud run logs read talking-drum-api --region=us-central1

# List all services
gcloud run services list
```

---

## 🎉 Success Checklist

After successful deployment:

- [ ] ✅ API responds to health checks
- [ ] ✅ Prediction endpoint works with test audio
- [ ] ✅ API documentation accessible
- [ ] ✅ Frontend deployed and connected
- [ ] ✅ Custom domain configured (optional)
- [ ] ✅ Monitoring setup
- [ ] ✅ Costs within budget

---

**Your Talking Drum API is now live on Google Cloud! 🥁✨**

Share your API URL with your supervisor to showcase your full-stack AI application running in production!
