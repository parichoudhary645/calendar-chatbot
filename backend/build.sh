#!/bin/bash

# Render build script for Calendar AI Assistant
echo "🚀 Starting build process..."

# Install system dependencies if needed
echo "📦 Installing Python dependencies..."

# Install requirements with pip
pip install --no-cache-dir -r requirements.txt

# If the above fails, try installing without problematic packages
if [ $? -ne 0 ]; then
    echo "⚠️  Some packages failed to install, trying minimal installation..."
    pip install --no-cache-dir fastapi uvicorn google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv pydantic python-multipart pytz python-dateutil openai groq anthropic google-generativeai
fi

echo "✅ Build completed successfully!" 