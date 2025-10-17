# Yoruba Talking Drum Translator - Full Stack Setup Guide

## 🏗️ Architecture

**Backend**: FastAPI (Python) - RESTful API
**Frontend**: React.js - Modern SPA
**AI Model**: PyTorch CNN (100% accuracy)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Export Your Model

First, open your Jupyter notebook and add this cell at the END:

```python
import torch, pickle, os
os.makedirs('../model', exist_ok=True)

# Save model
torch.save(models['CNN'].state_dict(), '../model/best_model.pth')

# Save scaler
with open('../model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

# Save label encoder
with open('../model/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("✅ Model exported!")
```

### Step 2: Start the Backend

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the API server
python main.py
```

The API will run at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Step 3: Start the Frontend

Open a **NEW terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm start
```

The app will open at: `http://localhost:3000`

---

## 📁 Project Structure

```
yomi_talking_drum/
├── backend/
│   ├── main.py                 # FastAPI application
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js       # Drag & drop component
│   │   │   ├── FileUpload.css
│   │   │   ├── PredictionResult.js # Results display
│   │   │   ├── PredictionResult.css
│   │   │   ├── ModelInfo.js        # Model information
│   │   │   └── ModelInfo.css
│   │   ├── App.js              # Main application
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json            # Node dependencies
│
└── model/
    ├── best_model.pth         # Trained CNN model
    ├── scaler.pkl             # Feature scaler
    └── label_encoder.pkl      # Label encoder
```

---

## 🎯 Features

### Backend (FastAPI)
- ✅ RESTful API with automatic OpenAPI docs
- ✅ CORS enabled for frontend access
- ✅ Audio file upload handling
- ✅ 47 audio features extraction
- ✅ Real-time prediction
- ✅ Cultural information endpoint
- ✅ Model health check
- ✅ Error handling

### Frontend (React.js)
- ✅ Modern, responsive UI
- ✅ Drag & drop file upload
- ✅ Real-time prediction results
- ✅ Interactive confidence charts
- ✅ Cultural context display
- ✅ Model information dashboard
- ✅ Beautiful animations
- ✅ Mobile-friendly

---

## 🔌 API Endpoints

### GET `/`
Health check - Returns API status

### GET `/health`
Model health check

### GET `/model-info`
Get model architecture information

### POST `/predict`
Upload audio file for prediction

**Request:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/audio.wav"
```

**Response:**
```json
{
  "success": true,
  "predicted_note": "Do",
  "confidence": 99.82,
  "all_confidences": {
    "Do": 99.82,
    "Re": 0.10,
    ...
  },
  "cultural_info": {
    "pitch": "Low tone (Yoruba low pitch)",
    "usage": "Used for deep, resonant messages",
    "cultural": "Represents stability...",
    "frequency": "85-120 Hz"
  },
  "audio_duration": 0.35,
  "sample_rate": 22050
}
```

### GET `/cultural-info/{note}`
Get cultural information for a specific note

### GET `/notes`
Get information about all tonic solfa notes

---

## 🧪 Testing the Application

### 1. Test Backend Directly

```bash
# Check health
curl http://localhost:8000/health

# Get model info
curl http://localhost:8000/model-info

# Test prediction
curl -X POST "http://localhost:8000/predict" \
  -F "file=@augmented_talking_drum_dataset/Do/Do_amp_aug_00_001.wav"
```

### 2. Test Frontend

1. Open `http://localhost:3000` in browser
2. Drag and drop a WAV file
3. Click "Predict Note"
4. View results with confidence scores
5. Check "Model Info" tab

### 3. Test Files

Use samples from your dataset:
```
augmented_talking_drum_dataset/Do/Do_amp_aug_00_001.wav
augmented_talking_drum_dataset/Mi/Mi_aug_00_015.wav
augmented_talking_drum_dataset/So/So_aug_00_020.wav
```

---

## 🎓 For Your Supervisor Presentation

### Demo Script (5 minutes)

#### 1. Show Architecture (30 seconds)
"I've built a full-stack application with FastAPI backend and React frontend, demonstrating production-ready deployment skills."

#### 2. Show Backend API (1 minute)
Open `http://localhost:8000/docs`
- "This is the auto-generated API documentation"
- "We have endpoints for prediction, health checks, and cultural information"
- Show `/predict` endpoint and test it

#### 3. Show Frontend (2 minutes)
Open `http://localhost:3000`
- "Modern, responsive UI built with React"
- Drag and drop an audio file
- "Real-time prediction with confidence visualization"
- Show the confidence chart
- Show cultural context

#### 4. Show Model Info Tab (1 minute)
- "47 engineered features"
- "100% accuracy across all models"
- "1,050 perfectly balanced samples"
- Show tonic solfa notes with cultural information

#### 5. Highlight Technical Skills (30 seconds)
- RESTful API design
- Modern frontend development
- Real-time data visualization
- Full-stack integration
- Production-ready code

---

## 💡 Key Advantages Over Streamlit

1. **Professional Architecture**
   - Separated backend and frontend
   - Scalable and maintainable
   - Industry-standard tech stack

2. **Better Performance**
   - Faster load times
   - Optimized API calls
   - Efficient state management

3. **Enhanced UX**
   - Modern, responsive design
   - Smooth animations
   - Interactive visualizations
   - Mobile-friendly

4. **Portfolio-Ready**
   - Shows full-stack skills
   - Demonstrates API design
   - Modern JavaScript/React knowledge
   - Production deployment capability

---

## 🚢 Deployment Options

### Backend Deployment

**Option 1: Heroku**
```bash
# Create Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
heroku create talking-drum-api
git push heroku main
```

**Option 2: AWS Lambda**
- Use Mangum for serverless deployment
- Package with dependencies
- Deploy via AWS SAM or Serverless Framework

### Frontend Deployment

**Option 1: Vercel** (Recommended)
```bash
npm install -g vercel
vercel --prod
```

**Option 2: Netlify**
```bash
npm run build
netlify deploy --prod --dir=build
```

**Option 3: GitHub Pages**
```bash
npm install gh-pages
npm run build
npm run deploy
```

---

## 🛠️ Troubleshooting

### Backend Issues

**Problem: ModuleNotFoundError**
```bash
Solution: pip install -r requirements.txt
```

**Problem: Model not found**
```bash
Solution: Make sure model/ directory exists with:
- best_model.pth
- scaler.pkl
- label_encoder.pkl
```

**Problem: CORS errors**
```bash
Solution: Already configured in main.py
Check that frontend is at http://localhost:3000
```

### Frontend Issues

**Problem: npm command not found**
```bash
Solution: Install Node.js from https://nodejs.org/
```

**Problem: Port 3000 already in use**
```bash
Solution: Kill process on port 3000
- Linux/Mac: lsof -ti:3000 | xargs kill -9
- Windows: netstat -ano | findstr :3000, then taskkill /PID <pid> /F
```

**Problem: Cannot connect to backend**
```bash
Solution: 
1. Make sure backend is running on port 8000
2. Check proxy in package.json: "proxy": "http://localhost:8000"
```

---

## 📈 Future Enhancements

1. **Real-Time Recording**
   - Add WebRTC for live microphone input
   - Real-time audio streaming

2. **Batch Processing**
   - Upload multiple files
   - Export results as CSV/JSON

3. **User Authentication**
   - User accounts
   - Save prediction history

4. **Advanced Analytics**
   - Prediction statistics
   - Model performance tracking
   - Usage analytics

5. **Mobile App**
   - React Native version
   - iOS/Android support

---

## 🎉 What You've Built

You now have:
- ✅ Professional full-stack web application
- ✅ RESTful API with FastAPI
- ✅ Modern React frontend
- ✅ Real-time audio classification
- ✅ Interactive data visualization
- ✅ Production-ready code
- ✅ API documentation
- ✅ Responsive design
- ✅ Cultural preservation features

**This demonstrates:**
- Backend development (Python/FastAPI)
- Frontend development (JavaScript/React)
- API design
- Machine learning deployment
- Full-stack integration
- Professional software engineering

---

## 📞 Support

If you encounter any issues:
1. Check this guide carefully
2. Verify all dependencies are installed
3. Ensure model files are exported
4. Check terminal for error messages
5. Test backend API first, then frontend

---

**Your supervisor will be VERY impressed! 🎓✨**
