#!/bin/bash
# Full-Stack Development Startup Script

echo "🚀 Starting Yoruba Talking Drum Translator"
echo "============================================"

# Check if model files exist
echo "📁 Checking model files..."
if [ ! -f "model/best_model.pth" ]; then
    echo "❌ Model file missing: model/best_model.pth"
    echo "💡 Please export your trained model from the notebook first"
    exit 1
fi

if [ ! -f "model/scaler.pkl" ]; then
    echo "❌ Scaler file missing: model/scaler.pkl"
    echo "💡 Please export the scaler from your notebook first"
    exit 1
fi

if [ ! -f "model/label_encoder.pkl" ]; then
    echo "❌ Label encoder file missing: model/label_encoder.pkl"
    echo "💡 Please export the label encoder from your notebook first"
    exit 1
fi

echo "✅ All model files found!"

# Start backend in background
echo "🔧 Starting FastAPI backend..."
cd backend
source ../.venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running on http://localhost:8000"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "🎨 Starting React frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 Application started successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"  
echo "📚 API Docs: http://localhost:8000/docs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop both servers"

# Handle shutdown
cleanup() {
    echo ""
    echo "🛑 Shutting down..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait
