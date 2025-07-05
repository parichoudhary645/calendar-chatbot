#!/bin/bash

# Calendar Booking Chatbot Startup Script
# This script starts both the backend and frontend services

echo "🚀 Starting Calendar Booking Chatbot..."
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if required files exist
if [ ! -f "backend/service_account.json" ]; then
    echo "❌ service_account.json not found in backend/ directory"
    echo "Please copy your Google Service Account JSON file to backend/service_account.json"
    exit 1
fi

if [ ! -f "backend/.env" ]; then
    echo "❌ .env file not found in backend/ directory"
    echo "Please create backend/.env file with your OPENAI_API_KEY"
    echo "Example:"
    echo "OPENAI_API_KEY=your_openai_api_key_here"
    echo "SERVICE_ACCOUNT_FILE=service_account.json"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check if ports are available
echo "🔍 Checking ports..."
if ! check_port 8000; then
    echo "Please stop the service using port 8000 or change the backend port"
    exit 1
fi

if ! check_port 8501; then
    echo "Please stop the service using port 8501 or change the frontend port"
    exit 1
fi

echo "✅ Ports are available"

# Install dependencies if needed
echo "📦 Installing dependencies..."

echo "Installing backend dependencies..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
cd ..

echo "Installing frontend dependencies..."
cd frontend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt
cd ..

echo "✅ Dependencies installed"

# Start backend
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Check if backend started successfully
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Backend started successfully (PID: $BACKEND_PID)"

# Start frontend
echo "🎨 Starting frontend server..."
cd frontend
source venv/bin/activate
streamlit run app.py &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 3

# Check if frontend started successfully
if ! curl -s http://localhost:8501 > /dev/null; then
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 1
fi

echo "✅ Frontend started successfully (PID: $FRONTEND_PID)"

echo ""
echo "🎉 Calendar Booking Chatbot is now running!"
echo "=========================================="
echo "Frontend: http://localhost:8501"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep script running
wait 