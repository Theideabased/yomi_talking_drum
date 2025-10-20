# 🚀 Deploy Backend to GCP Cloud Run

## Quick Start (3 Steps)

### 1. Get Your GCP Project ID
- Go to https://console.cloud.google.com
- Create a new project or use existing one
- Note your **Project ID** (not project name)

### 2. Run the Deployment Script
```bash
./deploy-to-gcp.sh
```

Enter your Project ID when prompted. The script will:
- ✅ Login to GCP (if needed)
- ✅ Enable required APIs
- ✅ Build Docker container
- ✅ Deploy to Cloud Run
- ✅ Give you the live URL

### 3. Test Your API
Once deployed, you'll get a URL like:
```
https://talking-drum-api-xxxxx-uc.a.run.app
```

Test it:
```bash
curl https://YOUR-URL/health
```

## What You Need

1. **Google Cloud Account** (free tier available)
2. **Billing Enabled** on your project (required for Cloud Run)
3. **gcloud CLI** (already installed ✅)
4. **Trained Model** (your model files in `/model` directory)

## Cost

- **Free Tier**: 2 million requests/month
- **Typical Cost**: $5-15/month for moderate usage
- Cloud Run only charges for actual usage (not idle time)

## After Deployment

1. Copy your API URL
2. Update frontend:
   ```bash
   # In Vercel or .env.production
   REACT_APP_API_URL=https://your-api-url.run.app
   ```
3. Deploy frontend to Vercel

## Troubleshooting

**"Project ID not found"**
- Make sure you're using Project ID, not Project Name
- Find it in GCP Console dashboard

**"Build failed"**
- Check if model files exist: `ls model/`
- Try again: `./deploy-to-gcp.sh`

**"Need to enable billing"**
- Go to GCP Console → Billing
- Link a billing account (free trial available)

## Manual Deployment

If you prefer manual control:

```bash
# 1. Set project
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# 2. Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# 3. Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/talking-drum-api

# 4. Deploy
gcloud run deploy talking-drum-api \
  --image gcr.io/$PROJECT_ID/talking-drum-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2
```

## Next Steps

✅ Backend deployed to GCP  
⬜ Update frontend with API URL  
⬜ Deploy frontend to Vercel  
⬜ Test full application  

---

**Ready?** Just run:
```bash
./deploy-to-gcp.sh
```
