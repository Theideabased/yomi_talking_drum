# Railway Deployment (Easiest!)

Railway is the fastest way to deploy your ML backend. Here's how:

## Option 1: Deploy from GitHub (Recommended - 2 minutes!)

1. **Push your code to GitHub** (if not already):
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Go to Railway**: https://railway.app
   - Sign up with GitHub (free)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `yomi_talking_drum` repository
   - Select the `main` branch

3. **Railway auto-detects everything!**
   - Finds your Dockerfile
   - Builds and deploys automatically
   - Gives you a live URL in 3-5 minutes!

4. **Get your URL**:
   - Click on your service
   - Go to "Settings" → "Generate Domain"
   - Copy the URL (like `https://your-app.up.railway.app`)

## Option 2: Railway CLI (Alternative)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up

# Get your URL
railway domain
```

## Configuration

Railway will use your existing `Dockerfile` - no changes needed!

Your model files will be included automatically.

## Cost
- **Free Tier**: $5 credit/month (plenty for development)
- **Paid**: ~$5-10/month for moderate usage
- Only pay for what you use

## After Deployment

1. Copy your Railway URL
2. Update frontend:
   ```bash
   # frontend/.env.production
   REACT_APP_API_URL=https://your-app.up.railway.app
   ```

---

## Alternative: Render.com (Also Easy!)

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - Root Directory: Leave empty
   - Build Command: (auto-detected from Dockerfile)
   - Start Command: (auto-detected)
5. Click "Create Web Service"
6. Get your URL: `https://your-app.onrender.com`

## Which to Choose?

- **Railway**: Faster deployment, better free tier
- **Render**: More generous free tier (but slower builds)
- **GCP Cloud Run**: Best for production at scale (but complex)

## My Recommendation

Use **Railway** - it's the sweet spot of:
- ✅ Fast deployment (3-5 minutes)
- ✅ Easy setup (just connect GitHub)
- ✅ Handles ML models well
- ✅ Generous free tier
- ✅ Great developer experience

Would you like me to help you deploy to Railway instead?
