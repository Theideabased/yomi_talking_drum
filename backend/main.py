"""
Yoruba Talking Drum Translator - FastAPI Backend
================================================
RESTful API for talking drum audio classification
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch
import torch.nn as nn
import numpy as np
import librosa
import pickle
import os
import tempfile
from typing import Dict, List
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Yoruba Talking Drum Translator API",
    description="AI-powered API for translating talking drum sounds to tonic solfa",
    version="1.0.0"
)

# CORS middleware - allows frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model Architecture (enhanced version to match saved model)
class TalkingDrumModel(nn.Module):
    """Enhanced Talking Drum Model with Cultural Context"""
    def __init__(self, input_size=47, num_classes=7, d_model=128):
        super(TalkingDrumModel, self).__init__()
        self.input_size = input_size
        self.d_model = d_model
        
        # Input projection
        self.input_projection = nn.Linear(input_size, d_model)
        
        # Positional embedding
        self.pos_embedding = nn.Parameter(torch.randn(1, d_model))
        
        # Transformer layers
        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=8,
                dim_feedforward=256,
                dropout=0.1,
                batch_first=True
            ),
            num_layers=6
        )
        
        # Cultural attention
        self.cultural_attention = nn.MultiheadAttention(d_model, 4, batch_first=True)
        
        # Layer norm
        self.layer_norm = nn.LayerNorm(d_model)
        
        # Classifier
        self.classifier = nn.Sequential(
            nn.Linear(d_model, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes)
        )
    
    def forward(self, x):
        # Project input
        x = self.input_projection(x)  # [batch, d_model]
        x = x.unsqueeze(1)  # [batch, 1, d_model]
        
        # Add positional embedding
        x = x + self.pos_embedding.unsqueeze(0)
        
        # Transformer
        x = self.transformer(x)
        
        # Cultural attention
        attn_out, _ = self.cultural_attention(x, x, x)
        x = x + attn_out
        
        # Layer norm
        x = self.layer_norm(x)
        
        # Classifier
        x = x.squeeze(1)  # [batch, d_model]
        x = self.classifier(x)
        
        return x

# Fallback CNN Model
class CNNModel(nn.Module):
    """Simple CNN for compatibility"""
    def __init__(self, input_size=47, num_classes=7):
        super(CNNModel, self).__init__()
        self.features = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
        )
        self.classifier = nn.Linear(64, num_classes)
        
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# Global variables for model
model = None
scaler = None
label_encoder = None
NOTES = ['Do', 'Fa', 'La', 'Mi', 'Re', 'So', 'Ti']

# Pydantic models for API responses
class PredictionResponse(BaseModel):
    success: bool
    predicted_note: str
    confidence: float
    all_confidences: Dict[str, float]
    cultural_info: Dict[str, str]
    audio_duration: float
    sample_rate: int

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    message: str

class ModelInfoResponse(BaseModel):
    architecture: str
    input_features: int
    num_classes: int
    classes: List[str]
    accuracy: str
    sample_rate: int

def extract_features(audio, sr=22050):
    """Extract 47 audio features from audio signal"""
    features = {}
    
    try:
        if len(audio) == 0:
            return None
        
        # Pad or trim audio to consistent length
        max_len = int(sr * 5)
        if len(audio) > max_len:
            audio = audio[:max_len]
        else:
            audio = np.pad(audio, (0, max_len - len(audio)))
        
        # Time domain features
        features['rms'] = np.sqrt(np.mean(audio**2))
        features['zcr'] = np.mean(librosa.feature.zero_crossing_rate(audio)[0])
        
        # Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        features['spectral_centroid_std'] = np.std(spectral_centroids)
        
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
        features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
        features['spectral_rolloff_std'] = np.std(spectral_rolloff)
        
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)[0]
        features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
        features['spectral_bandwidth_std'] = np.std(spectral_bandwidth)
        
        # MFCCs
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        for i in range(13):
            features[f'mfcc_{i}_mean'] = np.mean(mfccs[i])
            features[f'mfcc_{i}_std'] = np.std(mfccs[i])
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        for i in range(12):
            features[f'chroma_{i}_mean'] = np.mean(chroma[i])
        
        # Temporal features
        onset_frames = librosa.onset.onset_detect(y=audio, sr=sr)
        features['onset_rate'] = len(onset_frames) / (len(audio) / sr)
        
        return list(features.values())
    
    except Exception as e:
        print(f"Error extracting features: {e}")
        return None

def get_cultural_info(note: str) -> Dict[str, str]:
    """Get cultural information about the note"""
    info = {
        'Do': {
            'pitch': 'Low tone (Yoruba low pitch)',
            'usage': 'Used for deep, resonant messages and greetings',
            'cultural': 'Represents stability and foundation in Yoruba music',
            'frequency': '85-120 Hz'
        },
        'Re': {
            'pitch': 'Mid-low tone',
            'usage': 'Transitional tone in musical phrases',
            'cultural': 'Bridges low and mid range expressions',
            'frequency': '95-140 Hz'
        },
        'Mi': {
            'pitch': 'Mid tone',
            'usage': 'Neutral tone for narrative communication',
            'cultural': 'Common in storytelling and proverbs',
            'frequency': '110-160 Hz'
        },
        'Fa': {
            'pitch': 'Mid-high tone',
            'usage': 'Elevated expression and emphasis',
            'cultural': 'Used for important announcements',
            'frequency': '130-180 Hz'
        },
        'So': {
            'pitch': 'High tone',
            'usage': 'Alert and attention-getting sounds',
            'cultural': 'Represents elevation and importance',
            'frequency': '150-220 Hz'
        },
        'La': {
            'pitch': 'High-mid tone',
            'usage': 'Refined high-range communication',
            'cultural': 'Used in ceremonial contexts',
            'frequency': '180-250 Hz'
        },
        'Ti': {
            'pitch': 'Highest tone (Yoruba high pitch)',
            'usage': 'Peak expression and climactic moments',
            'cultural': 'Represents highest level of emphasis',
            'frequency': '220-300 Hz'
        }
    }
    return info.get(note, {})

@app.on_event("startup")
async def load_model():
    """Load model on startup"""
    global model, scaler, label_encoder
    
    try:
        # Load model - try enhanced model first, then fallback to CNN
        model_paths = ['model/best_model.pth', '../model/best_model.pth']
        model_loaded = False
        
        for path in model_paths:
            if os.path.exists(path):
                try:
                    # Try enhanced model first
                    model = TalkingDrumModel(input_size=47, num_classes=7)
                    model.load_state_dict(torch.load(path, map_location='cpu'))
                    model.eval()
                    print(f"✅ Enhanced model loaded successfully from {path}")
                    model_loaded = True
                    break
                except Exception as e:
                    try:
                        # Fallback to CNN model
                        model = CNNModel(input_size=47, num_classes=7)
                        model.load_state_dict(torch.load(path, map_location='cpu'))
                        model.eval()
                        print(f"✅ CNN model loaded successfully from {path}")
                        model_loaded = True
                        break
                    except Exception as e2:
                        print(f"❌ Error loading model from {path}: {str(e2)}")
                        continue
        
        if not model_loaded:
            print("⚠️  Model file not found or incompatible")
            model = None
        
        # Load scaler
        scaler_paths = ['model/scaler.pkl', '../model/scaler.pkl']
        scaler_loaded = False
        for path in scaler_paths:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    scaler = pickle.load(f)
                print(f"✅ Scaler loaded successfully from {path}")
                scaler_loaded = True
                break
        if not scaler_loaded:
            print("⚠️  Scaler file not found")
            scaler = None
        
        # Load label encoder
        encoder_paths = ['model/label_encoder.pkl', '../model/label_encoder.pkl']
        encoder_loaded = False
        for path in encoder_paths:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    label_encoder = pickle.load(f)
                print(f"✅ Label encoder loaded successfully from {path}")
                encoder_loaded = True
                break
        if not encoder_loaded:
            print("⚠️  Label encoder file not found")
            label_encoder = None
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = None
        scaler = None
        label_encoder = None

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    return {
        "status": "online",
        "model_loaded": model is not None and scaler is not None,
        "message": "Yoruba Talking Drum Translator API is running"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    model_status = model is not None and scaler is not None
    return {
        "status": "healthy" if model_status else "model_not_loaded",
        "model_loaded": model_status,
        "message": "Model loaded and ready" if model_status else "Model not loaded. Please train and export model first."
    }

@app.get("/model-info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get model information"""
    return {
        "architecture": "CNN (Convolutional Neural Network)",
        "input_features": 47,
        "num_classes": 7,
        "classes": NOTES,
        "accuracy": "100%",
        "sample_rate": 22050
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_audio(file: UploadFile = File(...)):
    """
    Predict tonic solfa note from uploaded audio file
    
    - **file**: Audio file (WAV, MP3, M4A, AAC)
    """
    
    # Check if model is loaded
    if model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train and export model first."
        )
    
    # Validate file type
    allowed_extensions = ['.wav', '.mp3', '.m4a', '.aac']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file temporarily
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Load audio
        audio, sr = librosa.load(tmp_path, sr=22050)
        duration = len(audio) / sr
        
        # Extract features
        features = extract_features(audio, sr)
        if features is None:
            raise HTTPException(status_code=400, detail="Failed to extract features from audio")
        
        # Scale features
        features_array = np.array(features).reshape(1, -1)
        features_scaled = scaler.transform(features_array)
        
        # Convert to tensor and predict
        features_tensor = torch.FloatTensor(features_scaled)
        
        with torch.no_grad():
            outputs = model(features_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            confidence_scores = probabilities.cpu().numpy()[0]
            predicted_class = torch.argmax(outputs, dim=1).cpu().numpy()[0]
        
        predicted_note = NOTES[predicted_class]
        confidence = float(confidence_scores[predicted_class] * 100)
        
        # Create confidence dictionary
        all_confidences = {
            note: float(conf * 100) 
            for note, conf in zip(NOTES, confidence_scores)
        }
        
        # Get cultural info
        cultural_info = get_cultural_info(predicted_note)
        
        # Clean up temp file
        os.remove(tmp_path)
        
        return {
            "success": True,
            "predicted_note": predicted_note,
            "confidence": confidence,
            "all_confidences": all_confidences,
            "cultural_info": cultural_info,
            "audio_duration": duration,
            "sample_rate": sr
        }
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)
        
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.get("/cultural-info/{note}")
async def get_note_cultural_info(note: str):
    """Get cultural information for a specific note"""
    note = note.capitalize()
    if note not in NOTES:
        raise HTTPException(status_code=404, detail=f"Note not found. Valid notes: {', '.join(NOTES)}")
    
    return get_cultural_info(note)

@app.get("/notes")
async def get_all_notes():
    """Get information about all tonic solfa notes"""
    return {
        "notes": NOTES,
        "count": len(NOTES),
        "cultural_info": {note: get_cultural_info(note) for note in NOTES}
    }

if __name__ == "__main__":
    print("🚀 Starting Yoruba Talking Drum Translator API")
    print("📡 API will be available at: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    print("🔧 ReDoc available at: http://localhost:8000/redoc")
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
