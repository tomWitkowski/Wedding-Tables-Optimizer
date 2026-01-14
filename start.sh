#!/bin/bash

echo "🎊 Wedding Tables Optimizer - Startup Script 🎊"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command_exists node; then
    echo "⚠️  Node.js is not installed. Frontend will not be available."
    SKIP_FRONTEND=true
else
    echo "✓ Node.js found"
fi

echo "✓ Python 3 found"
echo ""

# Start Backend
echo "Starting backend..."
cd api

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "Backend starting on http://localhost:8000"
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

cd ..

# Start Frontend
if [ "$SKIP_FRONTEND" != "true" ]; then
    echo ""
    echo "Starting frontend..."
    cd frontend

    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        npm install
    fi

    echo "Frontend starting on http://localhost:3000"
    npm run dev &
    FRONTEND_PID=$!

    cd ..
fi

echo ""
echo "✅ Application is running!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
if [ "$SKIP_FRONTEND" != "true" ]; then
    echo "📍 Frontend: http://localhost:3000"
fi
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
