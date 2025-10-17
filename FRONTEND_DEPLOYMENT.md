# 🚀 Frontend Deployment Guide

## Deploy to GitHub + Vercel (5 minutes)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
cd /home/user/Documents/yomi_talking_drum
git init
git add .
git commit -m "🎵 Initial commit: Yoruba Talking Drum AI App"

# Create GitHub repository (replace with your username)
gh repo create yomi_talking_drum --public --push
# OR manually create on GitHub.com and push:
git remote add origin https://github.com/Theideabased/yomi_talking_drum.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from frontend directory
cd frontend
vercel --prod

# Follow the prompts:
# ? Set up and deploy "~/yomi_talking_drum/frontend"? Y
# ? Which scope should contain your project? [Your Account]
# ? What's your project's name? yoruba-talking-drum
# ? In which directory is your code located? ./
```

#### Option B: Using Vercel Website
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your `yomi_talking_drum` repository
5. Set these settings:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
6. Click "Deploy"

### Step 3: Configure Environment Variables

In Vercel dashboard:
1. Go to your project settings
2. Add environment variables:
   - `REACT_APP_API_URL`: `https://your-backend-url` (when backend is deployed)

### Step 4: Custom Domain (Optional)

```bash
# Add custom domain
vercel domains add your-domain.com
vercel alias your-deployment-url your-domain.com
```

---

## 🔧 Environment Variables

### Development (`.env.local`)
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
```

### Production (Vercel)
```bash
REACT_APP_API_URL=https://your-backend-url
REACT_APP_ENV=production
```

---

## 🌐 Expected URLs

After deployment:
- **Frontend**: `https://yoruba-talking-drum.vercel.app`
- **GitHub**: `https://github.com/Theideabased/yomi_talking_drum`

---

## 🛠️ Troubleshooting

### Build Failures
```bash
# Clear cache and rebuild
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Routing Issues
- ✅ Already configured in `vercel.json`
- All routes redirect to `index.html` for SPA

### API Connection
- Update `REACT_APP_API_URL` in Vercel dashboard
- Check CORS settings in backend

---

## 📊 Performance Optimization

### Already Implemented:
- ✅ Production build with minification
- ✅ Static asset caching
- ✅ Code splitting
- ✅ Gzip compression
- ✅ Security headers

### Lighthouse Score (Expected):
- 🟢 Performance: 90+
- 🟢 Accessibility: 95+
- 🟢 Best Practices: 100
- 🟢 SEO: 90+

---

## 🔄 Automatic Deployments

Every push to `main` branch will automatically deploy to Vercel!

```bash
git add .
git commit -m "✨ Add new feature"
git push origin main
# 🚀 Automatically deploys to Vercel
```
