# After Build SUCCESS - Run These Commands

## 1. Deploy to Cloud Run
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

## 2. Get Your URL
```bash
gcloud run services describe talking-drum-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

## 3. Test It
```bash
curl $(gcloud run services describe talking-drum-api --platform managed --region us-central1 --format 'value(status.url)')/health
```

## Or Run the Script
```bash
chmod +x deploy-after-build.sh
./deploy-after-build.sh
```
