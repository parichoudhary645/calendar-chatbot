#!/bin/bash

# Calendar AI Assistant - Railway Deployment Script
# This script helps deploy both backend and frontend to Railway

set -e

echo "🚀 Calendar AI Assistant - Railway Deployment"
echo "=============================================="

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    railway login
fi

echo ""
echo "📋 Prerequisites Check:"
echo "1. Make sure you have your API keys ready:"
echo "   - GROQ_API_KEY"
echo "   - GOOGLE_API_KEY (Gemini)"
echo "   - OPENAI_API_KEY (optional)"
echo "   - ANTHROPIC_API_KEY (optional)"
echo "2. Make sure you have your service_account.json file"
echo "3. Make sure your Google Calendar is shared with the service account email"
echo ""

read -p "✅ Are you ready to deploy? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled."
    exit 1
fi

echo ""
echo "🔧 Deploying Backend..."
echo "======================="

# Deploy backend
cd backend
echo "📦 Initializing Railway project for backend..."
railway init --name calendar-ai-backend

echo "🚀 Deploying backend to Railway..."
railway up

# Get the backend URL
BACKEND_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
echo "✅ Backend deployed at: $BACKEND_URL"

echo ""
echo "🔧 Deploying Frontend..."
echo "======================="

# Deploy frontend
cd ../frontend
echo "📦 Initializing Railway project for frontend..."
railway init --name calendar-ai-frontend

echo "🚀 Deploying frontend to Railway..."
railway up

# Get the frontend URL
FRONTEND_URL=$(railway status --json | grep -o '"url":"[^"]*"' | cut -d'"' -f4)
echo "✅ Frontend deployed at: $FRONTEND_URL"

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: $FRONTEND_URL"
echo ""
echo "📝 Next Steps:"
echo "1. Go to Railway Dashboard and set environment variables for both services"
echo "2. Upload your service_account.json file to the backend service"
echo "3. Set BACKEND_URL environment variable in the frontend service to: $BACKEND_URL"
echo "4. Test your application!"
echo ""
echo "🔗 Railway Dashboard: https://railway.app/dashboard" 