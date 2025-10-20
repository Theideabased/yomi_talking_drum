# ✅ FIXED - GCP Deployment Commands

## The Issue
The Dockerfile was trying to copy files from `../model/` but Cloud Build needs relative paths from the project root.

## The Solution
Build from the **project root** (where you are now), not from the backend directory.

## Correct Commands

### 1. Build (Using cloudbuild.yaml) - RUNNING NOW
```bash
gcloud builds submit --config=cloudbuild.yaml
```

### OR Build (Direct command)
```bash
gcloud builds submit \
  --tag gcr.io/psyched-silicon-470414-a1/talking-drum-api \
  -f backend/Dockerfile \
  .
```
Note: The `.` at the end means "use current directory as build context"

### 2. After Build Completes, Deploy
```bash
gcloud run deploy talking-drum-api \
  --image gcr.io/psyched-silicon-470414-a1/talking-drum-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --port 8080 \
  --timeout 300
```

### 3. Get Your URL
```bash
gcloud run services describe talking-drum-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

## What Changed in Dockerfile
- Changed: `COPY ../model/` ❌
- To: `COPY model/` ✅
- Changed: `COPY main.py` ❌  
- To: `COPY backend/main.py` ✅

## Build Status
Your build is now running! You can monitor it with:
```bash
gcloud builds list --limit=1
```

Or view live logs:
```bash
# Get the build ID from the output, then:
gcloud builds log <BUILD_ID> --stream
```

## Next Steps
1. ⏳ Wait for build to complete (5-10 minutes)
2. ✅ Run deploy command
3. 🎉 Get your API URL
4. 🧪 Test: `curl YOUR_URL/health`
