"""
FastAPI Backend for Calendar Booking Chatbot
This is the main API server that handles chat requests
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import uvicorn
from dotenv import load_dotenv

from simple_llm_agent import SimpleLLMAgent

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Calendar Booking Chatbot API",
    description="A friendly AI assistant for booking Google Calendar appointments",
    version="1.0.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None

def initialize_agent():
    """Initialize the calendar booking agent"""
    global agent
    
    # Check if service account JSON is provided via environment variable (for Render)
    service_account_json = os.getenv("SERVICE_ACCOUNT_JSON")
    
    if service_account_json:
        # Use environment variable (Render deployment)
        print("✅ Using SERVICE_ACCOUNT_JSON from environment variable")
        agent = SimpleLLMAgent()
    else:
        # Use file-based service account (local development)
        service_account_file = os.getenv("SERVICE_ACCOUNT_FILE", "service_account.json")
        
        if not os.path.exists(service_account_file):
            print(f"⚠️ Service account file not found: {service_account_file}")
            print("⚠️ Please set SERVICE_ACCOUNT_JSON environment variable or provide service_account.json file")
            raise FileNotFoundError(f"Service account file not found: {service_account_file}")
        
        print(f"✅ Using service account file: {service_account_file}")
        agent = SimpleLLMAgent(service_account_file)
    
    print("🚀 Simple LLM Calendar Agent initialized and ready!")

@app.on_event("startup")
async def startup_event():
    """Initialize the agent when the server starts"""
    try:
        initialize_agent()
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        raise

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "🎉 Welcome to the Calendar Booking Chatbot API!",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/chat - Send a message to the chatbot",
            "health": "/health - Check API health",
            "docs": "/docs - API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if agent is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    return {
        "status": "healthy",
        "agent_ready": agent is not None,
        "message": "🤖 Calendar agent is ready to help!"
    }

@app.post("/chat")
async def chat_endpoint(request: Dict[str, Any]):
    """Main chat endpoint - handles user messages"""
    try:
        if agent is None:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        # Extract message from request
        message = request.get("message", "")
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Process the message through the agent
        response = agent.chat(message)
        
        return {
            "response": response,
            "success": True
        }
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        return {
            "response": "Sorry, I'm having trouble right now. Please try again!",
            "success": False,
            "error": str(e)
        }

@app.get("/conversation-history")
async def get_conversation_history():
    """Get the current conversation history"""
    try:
        if agent is None:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        history = agent.get_conversation_history()
        
        return {"messages": history}
        
    except Exception as e:
        print(f"❌ Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset-conversation")
async def reset_conversation():
    """Reset the conversation history"""
    try:
        if agent is None:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        # Reset conversation history
        agent.conversation_history = []
        
        return {
            "message": "✅ Conversation history cleared!",
            "success": True
        }
        
    except Exception as e:
        print(f"❌ Error resetting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpoint not found",
        "message": "The requested endpoint doesn't exist. Check /docs for available endpoints.",
        "status_code": 404
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal server error",
        "message": "Something went wrong on our end. Please try again later.",
        "status_code": 500
    }

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 