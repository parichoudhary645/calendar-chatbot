#!/usr/bin/env python3
"""
Test script to verify deployment setup
"""

import os
import requests
import json
from dotenv import load_dotenv

def test_backend_health(backend_url):
    """Test backend health endpoint"""
    try:
        response = requests.get(f"{backend_url}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Health: {data}")
            return True
        else:
            print(f"❌ Backend Health Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Connection Error: {e}")
        return False

def test_backend_chat(backend_url):
    """Test backend chat endpoint"""
    try:
        response = requests.post(
            f"{backend_url}/chat",
            json={"message": "Hello, can you help me with my calendar?"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Backend Chat: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Backend Chat Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend Chat Error: {e}")
        return False

def test_environment_variables():
    """Test if required environment variables are set"""
    required_vars = ['GROQ_API_KEY', 'GOOGLE_API_KEY']
    optional_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
    
    print("🔍 Checking Environment Variables:")
    
    all_good = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:20]}...")
        else:
            print(f"❌ {var}: Not set")
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {value[:20]}...")
        else:
            print(f"⚠️ {var}: Not set (optional)")
    
    return all_good

def main():
    """Main test function"""
    print("🧪 Calendar AI Assistant - Deployment Test")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    # Get backend URL from environment or use default
    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    print(f"\n🔗 Testing Backend URL: {backend_url}")
    
    # Test backend
    health_ok = test_backend_health(backend_url)
    chat_ok = test_backend_chat(backend_url)
    
    # Summary
    print("\n📊 Test Summary:")
    print("=" * 30)
    print(f"Environment Variables: {'✅' if env_ok else '❌'}")
    print(f"Backend Health: {'✅' if health_ok else '❌'}")
    print(f"Backend Chat: {'✅' if chat_ok else '❌'}")
    
    if env_ok and health_ok and chat_ok:
        print("\n🎉 All tests passed! Your deployment is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Please check your configuration.")
        
        if not env_ok:
            print("- Set required environment variables")
        if not health_ok:
            print("- Check if backend is running")
        if not chat_ok:
            print("- Check backend logs for errors")

if __name__ == "__main__":
    main() 