"""
Simple LLM Calendar Agent
A simplified agent that uses LLMs for natural language understanding without complex Langchain dependencies
"""

import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from calendar_utils import CalendarManager

class SimpleLLMAgent:
    """Simple calendar agent using LLMs for natural language understanding"""
    
    def __init__(self, service_account_file: str = "service_account.json"):
        """Initialize the simple LLM agent"""
        # Load environment variables
        load_dotenv()
        
        self.calendar_manager = CalendarManager(service_account_file)
        self.conversation_history = []
        self.llm = self._initialize_llm()
        
        print("🤖 Simple LLM Calendar Agent initialized successfully!")
        print(f"✅ Using LLM: {self.llm.__class__.__name__}")
    
    def _initialize_llm(self):
        """Initialize LLM with preferred order: Groq, Gemini, OpenAI, Anthropic, fallback"""
        print("🔍 Initializing LLM...")
        
        # Try Groq first (since Gemini is out of quota)
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key:
            print(f"🔑 Found Groq API key: {groq_api_key[:20]}...")
            try:
                from langchain_groq import ChatGroq
                llm = ChatGroq(
                    model="llama3-8b-8192",
                    temperature=0.1,
                    groq_api_key=groq_api_key
                )
                print("✅ Groq LLM initialized successfully!")
                return llm
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
        else:
            print("❌ No Groq API key found")
        
        # Try Gemini (Google) second
        gemini_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            print(f"🔑 Found Gemini API key: {gemini_api_key[:20]}...")
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    google_api_key=gemini_api_key
                )
                print("✅ Gemini LLM initialized successfully!")
                return llm
            except Exception as e:
                print(f"⚠️ Gemini initialization failed: {e}")
        else:
            print("❌ No Gemini API key found")
        
        # Try OpenAI
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            print(f"🔑 Found OpenAI API key: {openai_api_key[:20]}...")
            try:
                from langchain_openai import ChatOpenAI
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.1,
                    openai_api_key=openai_api_key
                )
                print("✅ OpenAI LLM initialized successfully!")
                return llm
            except Exception as e:
                print(f"⚠️ OpenAI initialization failed: {e}")
        else:
            print("❌ No OpenAI API key found")
        
        # Try Anthropic
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_api_key:
            print(f"🔑 Found Anthropic API key: {anthropic_api_key[:20]}...")
            try:
                from langchain_community.llms import Anthropic
                llm = Anthropic(
                    model="claude-3-sonnet-20240229",
                    temperature=0.1,
                    anthropic_api_key=anthropic_api_key
                )
                print("✅ Anthropic LLM initialized successfully!")
                return llm
            except Exception as e:
                print(f"⚠️ Anthropic initialization failed: {e}")
        else:
            print("❌ No Anthropic API key found")
        
        # Fallback to a simple mock LLM
        print("⚠️ No LLM API keys found. Using fallback mode.")
        return self._create_fallback_llm()
    
    def _create_fallback_llm(self):
        """Create a fallback LLM when no API keys are available"""
        class FallbackLLM:
            def __call__(self, prompt: str) -> str:
                # Simple rule-based responses
                prompt_lower = prompt.lower()
                if "book" in prompt_lower or "schedule" in prompt_lower:
                    return "I can help you book a meeting. Please provide the date, time, and title."
                elif "schedule" in prompt_lower or "events" in prompt_lower:
                    return "I can show you your schedule. Please specify which date."
                elif "available" in prompt_lower:
                    return "I can check availability. Please specify the date and time."
                else:
                    return "I'm here to help with your calendar. You can ask me to book meetings, check schedules, or find available times."
        
        return FallbackLLM()
    
    def _extract_booking_info(self, user_message: str) -> Dict[str, str]:
        """Extract booking information from user message using LLM"""
        try:
            # Create a prompt for the LLM to extract information
            prompt = f"""
            Extract booking information from this user message: "{user_message}"
            
            Return only the extracted information in this format:
            - date: (extracted date like "tomorrow", "today", "2024-01-15")
            - time: (extracted time like "3pm", "15:00")
            - title: (extracted meeting title)
            
            If any information is missing, use "None". Only return the extracted info, no other text.
            """
            
            # Get LLM response
            response = self.llm.invoke(prompt)
            
            # Handle different response types
            if hasattr(response, 'content'):
                response_text = response.content
            elif isinstance(response, str):
                response_text = response
            else:
                response_text = str(response)
            
            # Parse the response
            info = {"date": None, "time": None, "title": None}
            
            # Simple parsing - you could make this more sophisticated
            lines = response_text.strip().split('\n')
            for line in lines:
                if 'date:' in line.lower():
                    info['date'] = line.split(':', 1)[1].strip()
                elif 'time:' in line.lower():
                    info['time'] = line.split(':', 1)[1].strip()
                elif 'title:' in line.lower():
                    info['title'] = line.split(':', 1)[1].strip()
            
            return info
            
        except Exception as e:
            print(f"Error extracting booking info: {e}")
            return {"date": None, "time": None, "title": None}
    
    def _understand_intent(self, user_message: str) -> str:
        """Understand user intent using LLM"""
        try:
            prompt = f"""
            What is the user's intent in this message: "{user_message}"
            
            Choose one of:
            - book_meeting: User wants to book/schedule a NEW meeting (e.g., "book a meeting", "schedule a call")
            - check_availability: User wants to check if a time is available (e.g., "is 3pm free", "check availability")
            - get_schedule: User wants to see their EXISTING schedule/events (e.g., "what's my schedule", "show my events")
            - general_chat: General conversation
            
            Return only the intent, nothing else.
            """
            
            response = self.llm.invoke(prompt)
            
            # Handle different response types
            if hasattr(response, 'content'):
                response_text = response.content
            elif isinstance(response, str):
                response_text = response
            else:
                response_text = str(response)
            
            intent = response_text.strip().lower()
            print(f"🔍 LLM returned intent: '{intent}'")
            
            # Map to our intents - be more specific about schedule queries
            if "book" in intent or ("schedule" in intent and "meeting" in intent):
                return "book_meeting"
            elif "available" in intent or "free" in intent:
                return "check_availability"
            elif "what's" in intent or "show" in intent or ("schedule" in intent and "my" in intent):
                return "get_schedule"
            else:
                # Fallback: check the original user message for keywords
                user_lower = user_message.lower()
                if "schedule" in user_lower and ("what" in user_lower or "show" in user_lower or "my" in user_lower):
                    return "get_schedule"
                elif "book" in user_lower or "schedule" in user_lower:
                    return "book_meeting"
                else:
                    return "general_chat"
                
        except Exception as e:
            print(f"Error understanding intent: {e}")
            return "general_chat"
    
    def chat(self, user_message: str) -> str:
        """Process a user message through the simple LLM agent"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Understand intent
            intent = self._understand_intent(user_message)
            print(f"🔍 Detected intent: {intent} for message: '{user_message}'")
            
            # Handle based on intent
            if intent == "book_meeting":
                response = self._handle_booking(user_message)
            elif intent == "check_availability":
                response = self._handle_availability(user_message)
            elif intent == "get_schedule":
                response = self._handle_schedule(user_message)
            else:
                response = self._handle_general_chat(user_message)
            
            # Add response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_message = f"❌ Sorry, I encountered an error: {str(e)}"
            print(f"Agent error: {e}")
            return error_message
    
    def _handle_booking(self, user_message: str) -> str:
        """Handle booking requests"""
        try:
            # Extract booking info
            info = self._extract_booking_info(user_message)
            
            # Check if we have enough information
            if not info['date'] or not info['time'] or not info['title']:
                return "I'd be happy to help you book a meeting! Please provide the date, time, and title of the meeting."
            
            # Parse date and time
            if info['date'].lower() == "tomorrow":
                target_date = datetime.now() + timedelta(days=1)
            elif info['date'].lower() == "today":
                target_date = datetime.now()
            else:
                target_date = self.calendar_manager.parse_date_time(info['date'])
            
            time_obj = self.calendar_manager.parse_date_time("today", info['time'])
            start_time = target_date.replace(hour=time_obj.hour, minute=time_obj.minute)
            end_time = start_time + timedelta(hours=1)
            
            # Check availability
            if not self.calendar_manager.check_availability(start_time, end_time):
                return f"Sorry, {info['time']} on {info['date']} is not available. Please choose another time."
            
            # Create the event
            created_event = self.calendar_manager.create_event(
                summary=info['title'],
                start_time=start_time,
                end_time=end_time,
                description=f"Meeting booked via AI assistant"
            )
            
            return f"✅ Successfully booked '{info['title']}' for {info['date']} at {info['time']}. The meeting has been added to your Google Calendar."
            
        except Exception as e:
            return f"Error booking meeting: {str(e)}"
    
    def _handle_availability(self, user_message: str) -> str:
        """Handle availability check requests"""
        try:
            info = self._extract_booking_info(user_message)
            
            if not info['date']:
                return "I can check availability for you. Please specify which date you'd like to check."
            
            # Parse date
            if info['date'].lower() == "tomorrow":
                target_date = datetime.now() + timedelta(days=1)
            elif info['date'].lower() == "today":
                target_date = datetime.now()
            else:
                target_date = self.calendar_manager.parse_date_time(info['date'])
            
            if info['time']:
                # Check specific time
                time_obj = self.calendar_manager.parse_date_time("today", info['time'])
                start_time = target_date.replace(hour=time_obj.hour, minute=time_obj.minute)
                end_time = start_time + timedelta(hours=1)
                
                is_available = self.calendar_manager.check_availability(start_time, end_time)
                return f"{info['time']} on {info['date']} is {'available' if is_available else 'not available'}"
            else:
                # Get available slots for the day
                available_slots = self.calendar_manager.get_available_slots(target_date)
                if not available_slots:
                    return f"No available slots found for {info['date']}"
                
                slot_list = []
                for start, end in available_slots[:6]:
                    slot_list.append(f"• {self.calendar_manager.format_time_slot(start, end)}")
                
                return f"Available slots for {info['date']}:\n" + "\n".join(slot_list)
                
        except Exception as e:
            return f"Error checking availability: {str(e)}"
    
    def _extract_date_from_message(self, user_message: str) -> str:
        """Extract date information from user message for schedule queries"""
        try:
            user_lower = user_message.lower()
            
            if "today" in user_lower:
                return "today"
            elif "tomorrow" in user_lower:
                return "tomorrow"
            elif "yesterday" in user_lower:
                return "yesterday"
            else:
                # Try to extract other date formats
                prompt = f"""
                Extract the date from this message: "{user_message}"
                
                Return only the date in one of these formats:
                - today
                - tomorrow
                - yesterday
                - a specific date like "2024-01-15" or "next Monday"
                
                If no date is found, return "today" as default.
                """
                
                response = self.llm.invoke(prompt)
                
                # Handle different response types
                if hasattr(response, 'content'):
                    response_text = response.content
                elif isinstance(response, str):
                    response_text = response
                else:
                    response_text = str(response)
                
                return response_text.strip().lower()
                
        except Exception as e:
            print(f"Error extracting date: {e}")
            return "today"  # Default to today
    
    def _handle_schedule(self, user_message: str) -> str:
        """Handle schedule requests"""
        try:
            # Extract date from message
            date_str = self._extract_date_from_message(user_message)
            
            if not date_str:
                return "I can show you your schedule. Please specify which date you'd like to see."
            
            # Parse date
            if date_str.lower() == "tomorrow":
                target_date = datetime.now() + timedelta(days=1)
                day_name = "tomorrow"
            elif date_str.lower() == "today":
                target_date = datetime.now()
                day_name = "today"
            elif date_str.lower() == "yesterday":
                target_date = datetime.now() - timedelta(days=1)
                day_name = "yesterday"
            else:
                target_date = self.calendar_manager.parse_date_time(date_str)
                day_name = date_str
            
            # Get events
            events = self.calendar_manager.get_events_for_date(target_date)
            
            if not events:
                return f"📅 {day_name.title()} is wide open! No events scheduled."
            
            event_list = []
            for event in events[:5]:  # Show first 5 events
                start = event['start'].get('dateTime', event['start'].get('date'))
                if 'dateTime' in event['start']:
                    start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    time_str = start_time.strftime("%I:%M %p")
                    event_list.append(f"• {time_str}: {event['summary']}")
                else:
                    event_list.append(f"• All day: {event['summary']}")
            
            events_text = "\n".join(event_list)
            return f"📅 Here's what's on your schedule {day_name}:\n{events_text}"
            
        except Exception as e:
            return f"Error getting schedule: {str(e)}"
    
    def _handle_general_chat(self, user_message: str) -> str:
        """Handle general conversation"""
        try:
            prompt = f"""
            You are a helpful calendar assistant. The user said: "{user_message}"
            
            Provide a friendly, helpful response about calendar management. You can help with:
            - Booking meetings
            - Checking availability
            - Showing schedules
            - General calendar questions
            
            Keep your response concise and helpful.
            """
            
            response = self.llm.invoke(prompt)
            
            # Handle different response types
            if hasattr(response, 'content'):
                response_text = response.content
            elif isinstance(response, str):
                response_text = response
            else:
                response_text = str(response)
            
            return response_text.strip()
            
        except Exception as e:
            return "I'm here to help with your calendar! You can ask me to book meetings, check schedules, or find available times."
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        return "✅ Conversation history cleared!" 