#!/bin/bash

# Quick Start Script for Yoruba Talking Drum Translator
# Run this after exporting your model from the notebook

echo "🥁 Yoruba Talking Drum Translator - Quick Start"
echo "================================================"
echo ""

# Check if model directory exists
if [ ! -d "model" ]; then
    echo "❌ Error: 'model' directory not found!"
    echo ""
    echo "Please export your model first:"
    echo "1. Open your Jupyter notebook"
    echo "2. Add a new cell at the end"
    echo "3. Copy code from EXPORT_MODEL_NOTEBOOK_CELL.py"
    echo "4. Run the cell"
    echo "5. Then run this script again"
    exit 1
fi

# Check if model files exist
if [ ! -f "model/best_model.pth" ]; then
    echo "❌ Error: model/best_model.pth not found!"
    echo "Please run the model export cell in your notebook first."
    exit 1
fi

if [ ! -f "model/scaler.pkl" ]; then
    echo "❌ Error: model/scaler.pkl not found!"
    echo "Please run the model export cell in your notebook first."
    exit 1
fi

echo "✅ Model files found!"
echo ""

# Check if requirements are installed
echo "📦 Checking dependencies..."
pip install -q streamlit torch librosa scikit-learn soundfile matplotlib seaborn numpy pandas Pillow 2>&1 | grep -v "already satisfied"

echo ""
echo "✅ All dependencies installed!"
echo ""

# Run the app
echo "🚀 Starting Yoruba Talking Drum Translator..."
echo ""
echo "📱 The app will open in your browser at: http://localhost:8501"
echo ""
echo "💡 Tips:"
echo "   - Use 'Upload Audio' tab for reliable demo"
echo "   - Use 'Real-Time Recording' tab to impress your supervisor"
echo "   - Test with files from augmented_talking_drum_dataset/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run talking_drum_app.py
