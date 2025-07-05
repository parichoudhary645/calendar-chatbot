"""
Streamlit Frontend for Calendar Booking Chatbot
A beautiful and user-friendly chat interface
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="Cal - Your Calendar Assistant",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 5px solid #9c27b0;
    }
    .message-time {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        height: 3rem;
        font-size: 1rem;
    }
    .stTextInput > div > div > input {
        border-radius: 0.5rem;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Configuration
import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # Use environment variable or default to localhost

class ChatInterface:
    """Manages the chat interface and communication with the backend"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "is_connected" not in st.session_state:
            st.session_state.is_connected = False
        if "backend_url" not in st.session_state:
            st.session_state.backend_url = BACKEND_URL
    
    def check_backend_connection(self) -> bool:
        """Check if the backend is accessible"""
        try:
            response = requests.get(f"{st.session_state.backend_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def send_message(self, message: str) -> str:
        """Send a message to the backend and get response"""
        try:
            response = requests.post(
                f"{st.session_state.backend_url}/chat",
                json={"message": message, "user_id": "streamlit_user"},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"❌ Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.RequestException as e:
            return f"❌ Connection error: {str(e)}"
    
    def reset_conversation(self):
        """Reset the conversation history"""
        try:
            response = requests.post(f"{st.session_state.backend_url}/reset-conversation")
            if response.status_code == 200:
                st.session_state.messages = []
                st.success("✅ Conversation reset successfully!")
            else:
                st.error("❌ Failed to reset conversation")
        except:
            st.error("❌ Could not connect to backend to reset conversation")
    
    def display_header(self):
        """Display the main header"""
        st.markdown('<h1 class="main-header">📅 Cal - Your Calendar Assistant</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">Hi! I\'m Cal, your friendly AI assistant for booking appointments! 😊</p>', unsafe_allow_html=True)
    
    def display_sidebar(self):
        """Display the sidebar with controls and information"""
        with st.sidebar:
            st.header("⚙️ Settings & Info")
            
            # Backend URL configuration
            st.subheader("🔗 Backend Connection")
            backend_url = st.text_input(
                "Backend URL",
                value=st.session_state.backend_url,
                help="URL of your FastAPI backend"
            )
            
            if backend_url != st.session_state.backend_url:
                st.session_state.backend_url = backend_url
                st.rerun()
            
            # Connection status
            is_connected = self.check_backend_connection()
            if is_connected:
                st.success("✅ Connected to backend")
            else:
                st.error("❌ Backend not accessible")
            
            st.session_state.is_connected = is_connected
            
            # Controls
            st.subheader("🎛️ Controls")
            if st.button("🔄 Reset Conversation", use_container_width=True):
                self.reset_conversation()
            
            if st.button("📋 Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()
            
            # Information
            st.subheader("ℹ️ How to use")
            st.markdown("""
            **Try these examples:**
            - "Book a meeting tomorrow at 3pm"
            - "What's my schedule today?"
            - "Find available slots for next Monday"
            - "Check if 2pm tomorrow is free"
            """)
            
            st.subheader("💡 Tips")
            st.markdown("""
            - Be specific about dates and times
            - I can understand natural language
            - I'll suggest alternatives if your time is busy
            - All bookings are made in your connected Google Calendar
            """)
    
    def display_messages(self):
        """Display the chat messages"""
        # Create containers for messages
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    st.caption(message["timestamp"])
    
    def display_chat_input(self):
        """Display the chat input area"""
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "timestamp": datetime.now().strftime("%H:%M")
            })
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
                st.caption(datetime.now().strftime("%H:%M"))
            
            # Check if backend is connected
            if not st.session_state.is_connected:
                st.error("❌ Cannot connect to backend. Please check your connection settings.")
                return
            
            # Show assistant is typing
            with st.chat_message("assistant"):
                with st.spinner("🤔 Thinking..."):
                    # Get response from backend
                    response = self.send_message(prompt)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response,
                        "timestamp": datetime.now().strftime("%H:%M")
                    })
                    
                    # Display response
                    st.markdown(response)
                    st.caption(datetime.now().strftime("%H:%M"))
    
    def display_welcome_message(self):
        """Display welcome message if no conversation exists"""
        if not st.session_state.messages:
            st.info("👋 Welcome! I'm here to help you manage your calendar. Try asking me to book an appointment or check your schedule!")
    
    def run(self):
        """Main method to run the chat interface"""
        # Display header
        self.display_header()
        
        # Display sidebar
        self.display_sidebar()
        
        # Main chat area
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Display messages
            self.display_messages()
            
            # Display welcome message if no conversation
            self.display_welcome_message()

def main():
    """Main function to run the Streamlit app"""
    # Initialize chat interface
    chat_interface = ChatInterface()
    
    # Run the interface
    chat_interface.run()
    
    # Display chat input at the main level (outside any containers)
    chat_interface.display_chat_input()

if __name__ == "__main__":
    main() 