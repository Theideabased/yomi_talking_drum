#!/bin/bash
# Run this AFTER build completes successfully

echo "🚀 Deploying to Cloud Run..."

gcloud run deploy talking-drum-api \
  --image gcr.io/psyched-silicon-470414-a1/talking-drum-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --port 8080 \
  --timeout 300

echo ""
echo "✅ Getting your API URL..."
URL=$(gcloud run services describe talking-drum-api \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')

echo ""
echo "===================================="
echo "🎉 YOUR API IS LIVE!"
echo "===================================="
echo ""
echo "📡 API URL: $URL"
echo ""
echo "🧪 Test it:"
echo "   curl $URL/health"
echo ""
echo "📚 Docs: $URL/docs"
echo ""

# Save URL
echo $URL > backend/DEPLOYED_URL.txt
echo "💾 URL saved to backend/DEPLOYED_URL.txt"
