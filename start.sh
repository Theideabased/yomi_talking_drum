#!/bin/bash
# Yoruba Talking Drum Full Stack Startup Script

echo "🥁 Starting Yoruba Talking Drum Translator"
echo "=========================================="

# Check if Python virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please create .venv first."
    exit 1
fi

# Check if model files exist
if [ ! -f "model/best_model.pth" ]; then
    echo "❌ Model files not found. Please train the model first."
    echo "💡 Run your Jupyter notebook to train the model"
    exit 1
fi

echo "✅ Model files found"
echo "✅ Virtual environment found"

# Start backend in background
echo "🚀 Starting backend server..."
cd backend
source ../.venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend server started successfully on http://localhost:8000"
else
    echo "❌ Backend server failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# Start frontend
echo "🚀 Starting frontend server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 Full stack application started!"
echo "=================================="
echo "🔗 Frontend: http://localhost:3000"
echo "🔗 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT

# Keep script running
wait
