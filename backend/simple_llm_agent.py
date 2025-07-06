"""
Simple LLM Calendar Agent
A simplified agent that uses direct LLM API calls without Langchain dependencies
"""

import os
import re
import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from calendar_utils import CalendarManager

class SimpleLLMAgent:
    """Simple calendar agent using direct LLM API calls for natural language understanding"""
    
    def __init__(self, service_account_file: str = "service_account.json"):
        """Initialize the simple LLM agent"""
        # Load environment variables
        load_dotenv()
        
        # Check if service account JSON is provided via environment variable (for Render)
        service_account_json = os.getenv("SERVICE_ACCOUNT_JSON")
        if service_account_json:
            # Create temporary file from environment variable
            import tempfile
            
            try:
                # Validate JSON
                json.loads(service_account_json)
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                    f.write(service_account_json)
                    temp_file = f.name
                
                self.calendar_manager = CalendarManager(temp_file)
                print("✅ Calendar service initialized with environment variable JSON")
            except Exception as e:
                print(f"❌ Error with SERVICE_ACCOUNT_JSON: {e}")
                self.calendar_manager = CalendarManager(service_account_file)
        else:
            # Use file-based service account
            self.calendar_manager = CalendarManager(service_account_file)
        
        self.conversation_history = []
        self.llm_client = self._initialize_llm()
        
        print("🤖 Simple LLM Calendar Agent initialized successfully!")
        print(f"✅ Using LLM: {self.llm_client.__class__.__name__}")
    
    def _initialize_llm(self):
        """Initialize LLM client with preferred order: Groq, OpenAI, Anthropic, fallback"""
        print("🔍 Initializing LLM...")
        
        # Try Groq first
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key:
            print(f"🔑 Found Groq API key: {groq_api_key[:20]}...")
            try:
                return GroqClient(groq_api_key)
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
        
        # Try OpenAI
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            print(f"🔑 Found OpenAI API key: {openai_api_key[:20]}...")
            try:
                return OpenAIClient(openai_api_key)
            except Exception as e:
                print(f"⚠️ OpenAI initialization failed: {e}")
        
        # Try Anthropic
        anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        if anthropic_api_key:
            print(f"🔑 Found Anthropic API key: {anthropic_api_key[:20]}...")
            try:
                return AnthropicClient(anthropic_api_key)
            except Exception as e:
                print(f"⚠️ Anthropic initialization failed: {e}")
        
        # Fallback to a simple mock LLM
        print("⚠️ No LLM API keys found. Using fallback mode.")
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
            - title: (extracted meeting title or "Meeting" if none found)
            
            If any information is missing, use "None". Only return the extracted info, no other text.
            """
            
            # Get LLM response
            response = self.llm_client.generate(prompt)
            
            # Parse the response
            info = {"date": None, "time": None, "title": None}
            
            # Simple parsing
            lines = response.strip().split('\n')
            for line in lines:
                if 'date:' in line.lower():
                    date_val = line.split(':', 1)[1].strip()
                    info['date'] = date_val if date_val.lower() != "none" else None
                elif 'time:' in line.lower():
                    time_val = line.split(':', 1)[1].strip()
                    info['time'] = time_val if time_val.lower() != "none" else None
                elif 'title:' in line.lower():
                    title = line.split(':', 1)[1].strip()
                    info['title'] = title if title.lower() != "none" else "Meeting"
            
            # Fallback extraction if LLM didn't find date/time
            if not info['date'] or not info['time']:
                # Extract from the original message
                user_lower = user_message.lower()
                
                # Extract date
                if not info['date']:
                    if "tomorrow" in user_lower:
                        info['date'] = "tomorrow"
                    elif "today" in user_lower:
                        info['date'] = "today"
                
                # Extract time
                if not info['time']:
                    import re
                    time_match = re.search(r'(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', user_lower)
                    if time_match:
                        info['time'] = time_match.group(1)
            
            # Fallback title extraction if LLM didn't find one
            if not info['title'] or info['title'].lower() == "none":
                # Try to extract title from the message
                user_lower = user_message.lower()
                if "called" in user_lower:
                    # Extract title after "called"
                    called_index = user_lower.find("called")
                    title_part = user_message[called_index + 6:].strip()
                    if title_part:
                        info['title'] = title_part.split()[0]  # Take first word as title
                elif "dinner" in user_lower:
                    info['title'] = "Dinner"
                elif "lunch" in user_lower:
                    info['title'] = "Lunch"
                elif "meeting" in user_lower:
                    info['title'] = "Meeting"
                else:
                    info['title'] = "Meeting"  # Default title
            
            return info
            
        except Exception as e:
            print(f"Error extracting booking info: {e}")
            # Fallback extraction
            info = {"date": None, "time": None, "title": "Meeting"}
            
            # Simple keyword extraction
            user_lower = user_message.lower()
            if "tomorrow" in user_lower:
                info['date'] = "tomorrow"
            elif "today" in user_lower:
                info['date'] = "today"
            
            # Extract time
            import re
            time_match = re.search(r'(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', user_lower)
            if time_match:
                info['time'] = time_match.group(1)
            
            # Extract title
            if "dinner" in user_lower:
                info['title'] = "Dinner"
            elif "lunch" in user_lower:
                info['title'] = "Lunch"
            elif "called" in user_lower:
                called_index = user_lower.find("called")
                title_part = user_message[called_index + 6:].strip()
                if title_part:
                    info['title'] = title_part.split()[0]
            
            return info
    
    def _understand_intent(self, user_message: str) -> str:
        """Understand user intent using LLM"""
        try:
            prompt = f"""
            Analyze this user message and determine their intent: "{user_message}"
            
            Choose the most appropriate intent:
            
            1. book_meeting - User wants to SCHEDULE/CREATE a NEW meeting (e.g., "book a meeting", "schedule a call", "set up a meeting", "create an event")
            2. check_schedule - User wants to SEE their EXISTING schedule/events (e.g., "what's my schedule", "show my events", "what do I have today", "my schedule today")
            3. check_availability - User wants to CHECK if a specific time is FREE (e.g., "is 3pm available", "check if 2pm is free", "is tomorrow at 3pm free")
            4. general_chat - General conversation or questions
            
            Key differences:
            - book_meeting: User wants to CREATE a new meeting/event
            - check_schedule: User wants to SEE existing events/schedule
            - check_availability: User wants to CHECK if a time slot is free
            
            Examples:
            - "Book a meeting tomorrow at 3pm" → book_meeting
            - "Schedule a call today" → book_meeting
            - "What's my schedule today?" → check_schedule  
            - "Show my events tomorrow" → check_schedule
            - "My schedule today" → check_schedule
            - "Is 2pm tomorrow free?" → check_availability
            - "Check if 3pm is available" → check_availability
            - "Hello" → general_chat
            
            Return ONLY the intent category (book_meeting, check_schedule, check_availability, or general_chat).
            """
            
            response = self.llm_client.generate(prompt)
            intent = response.strip().lower()
            
            # Map to our intent categories
            if "book_meeting" in intent:
                return "book_meeting"
            elif "check_schedule" in intent:
                return "check_schedule"
            elif "check_availability" in intent:
                return "check_availability"
            else:
                return "general_chat"
                
        except Exception as e:
            print(f"Error understanding intent: {e}")
            # Fallback to simple keyword matching
            user_lower = user_message.lower()
            
            # Check for schedule queries first (more specific)
            if any(word in user_lower for word in ["what's my schedule", "show my schedule", "my schedule", "what do i have", "show my events", "my events"]):
                return "check_schedule"
            # Check for booking requests
            elif any(word in user_lower for word in ["book", "schedule a", "set up", "create meeting", "add meeting"]):
                return "book_meeting"
            # Check for availability queries
            elif any(word in user_lower for word in ["available", "free", "check if"]):
                return "check_availability"
            else:
                return "general_chat"

    def chat(self, user_message: str) -> str:
        """Main chat method that handles user messages"""
        try:
            # Add to conversation history
            self.conversation_history.append({"user": user_message, "timestamp": datetime.now()})
            
            # Understand user intent
            intent = self._understand_intent(user_message)
            print(f"🎯 Detected intent: {intent}")
            
            # Route to appropriate handler
            if intent == "book_meeting":
                return self._handle_booking(user_message)
            elif intent == "check_schedule":
                return self._handle_schedule(user_message)
            elif intent == "check_availability":
                return self._handle_availability(user_message)
            else:
                # Check for "find available slots" queries
                if any(phrase in user_message.lower() for phrase in ["find available", "available slots", "free slots", "open slots"]):
                    return self._handle_available_slots(user_message)
                else:
                    return self._handle_general_chat(user_message)
                
        except Exception as e:
            print(f"Error in chat: {e}")
            return "I'm sorry, I encountered an error. Please try again."

    def _handle_booking(self, user_message: str) -> str:
        """Handle meeting booking requests"""
        try:
            # Extract booking information
            booking_info = self._extract_booking_info(user_message)
            
            # Parse date and time
            date_str = booking_info.get('date')
            time_str = booking_info.get('time')
            title = booking_info.get('title') or "Meeting"
            
            if not date_str or not time_str:
                return "I need more information to book your meeting. Please provide a date and time."
            
            # Try to parse the combined date-time string
            try:
                # First try combined parsing
                combined_str = f"{date_str} {time_str}"
                parsed_date = self.calendar_manager.parse_combined_datetime(combined_str)
            except:
                # Fallback to separate parsing
                try:
                    parsed_date = self.calendar_manager.parse_date_time(date_str, time_str)
                except Exception as e:
                    print(f"Date parsing error: {e}")
                    return "I couldn't understand the date or time. Please try again with a clearer format like 'tomorrow at 3pm' or 'today 2:30pm'."
            
            # Check availability
            if not self.calendar_manager.check_availability(parsed_date, parsed_date + timedelta(hours=1)):
                return f"{time_str} on {date_str} is not available. Please choose another time."
            
            # Create the event
            event = self.calendar_manager.create_event(
                summary=title,
                start_time=parsed_date,
                end_time=parsed_date + timedelta(hours=1)
            )
            
            if event:
                return f"✅ Successfully booked '{title}' for {date_str} at {time_str}. The meeting has been added to your Google Calendar."
            else:
                return "❌ Failed to create the meeting. Please try again."
                
        except Exception as e:
            print(f"Error in booking: {e}")
            return "I encountered an error while booking your meeting. Please try again."

    def _handle_availability(self, user_message: str) -> str:
        """Handle availability checking requests"""
        try:
            # Extract date and time from message
            date_str = self._extract_date_from_message(user_message)
            time_str = self._extract_time_from_message(user_message)
            
            if not date_str or not time_str:
                return "Please specify a date and time to check availability."
            
            # Try to parse the combined date-time string
            try:
                combined_str = f"{date_str} {time_str}"
                parsed_date = self.calendar_manager.parse_combined_datetime(combined_str)
            except:
                # Fallback to separate parsing
                try:
                    parsed_date = self.calendar_manager.parse_date_time(date_str, time_str)
                except Exception as e:
                    print(f"Date parsing error: {e}")
                    return "I couldn't understand the date or time format. Please try again."
            
            # Check availability
            is_available = self.calendar_manager.check_availability(parsed_date, parsed_date + timedelta(hours=1))
            
            if is_available:
                return f"✅ {time_str} on {date_str} is available!"
            else:
                return f"❌ {time_str} on {date_str} is not available. Please choose another time."
                
        except Exception as e:
            print(f"Error checking availability: {e}")
            return "I encountered an error while checking availability. Please try again."

    def _extract_date_from_message(self, user_message: str) -> str:
        """Extract date from user message"""
        user_lower = user_message.lower()
        
        # Simple date extraction with more patterns
        if "today" in user_lower:
            return "today"
        elif "tomorrow" in user_lower:
            return "tomorrow"
        elif "next week" in user_lower:
            return "next week"
        elif "next monday" in user_lower:
            return "next monday"
        elif "next tuesday" in user_lower:
            return "next tuesday"
        elif "next wednesday" in user_lower:
            return "next wednesday"
        elif "next thursday" in user_lower:
            return "next thursday"
        elif "next friday" in user_lower:
            return "next friday"
        elif "next saturday" in user_lower:
            return "next saturday"
        elif "next sunday" in user_lower:
            return "next sunday"
        else:
            # Try to extract date using LLM with better prompt
            prompt = f"""
            Extract ONLY the date from this message: "{user_message}"
            
            Return ONLY the date in one of these formats:
            - today
            - tomorrow  
            - next monday
            - next tuesday
            - next wednesday
            - next thursday
            - next friday
            - next saturday
            - next sunday
            - next week
            
            Examples:
            - "Find available slots for next Monday" → next monday
            - "What's my schedule tomorrow" → tomorrow
            - "Show me today's events" → today
            
            If no date is found, return "today" as default.
            Return ONLY the date, nothing else.
            """
            try:
                response = self.llm_client.generate(prompt)
                date = response.strip().lower()
                # Validate the response
                valid_dates = ["today", "tomorrow", "next monday", "next tuesday", "next wednesday", 
                              "next thursday", "next friday", "next saturday", "next sunday", "next week"]
                if date in valid_dates:
                    return date
                else:
                    return "today"  # Default fallback
            except:
                return "today"  # Default fallback

    def _extract_time_from_message(self, user_message: str) -> str:
        """Extract time from user message"""
        # Simple time extraction
        import re
        time_pattern = r'\b(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)\b'
        matches = re.findall(time_pattern, user_message.lower())
        if matches:
            return matches[0]
        
        # Try LLM extraction
        prompt = f"Extract only the time from this message: '{user_message}'. Return only the time, nothing else."
        try:
            response = self.llm_client.generate(prompt)
            return response.strip()
        except:
            return None

    def _handle_schedule(self, user_message: str) -> str:
        """Handle schedule checking requests"""
        try:
            # Extract date from message
            date_str = self._extract_date_from_message(user_message)
            
            if not date_str:
                return "Please specify which date you'd like to see your schedule for."
            
            print(f"🔍 Extracted date: {date_str}")
            
            # Parse the date
            try:
                # For simple dates like "today", "tomorrow", we need to create a proper datetime
                if date_str == "today":
                    parsed_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                elif date_str == "tomorrow":
                    parsed_date = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                else:
                    # Try combined parsing for other formats
                    parsed_date = self.calendar_manager.parse_combined_datetime(date_str)
            except Exception as e:
                print(f"Date parsing error: {e}")
                # Fallback to simple date parsing
                try:
                    parsed_date = self.calendar_manager.parse_date_time(date_str)
                except Exception as e2:
                    print(f"Fallback date parsing error: {e2}")
                    return f"I couldn't understand the date '{date_str}'. Please try 'today', 'tomorrow', or 'next monday'."
            
            print(f"📅 Parsed date: {parsed_date}")
            
            # Get events for the date
            events = self.calendar_manager.get_events_for_date(parsed_date)
            
            if not events:
                return f"📅 You have no events scheduled for {date_str}."
            
            # Format the response
            response = f"📅 Here's what's on your schedule for {date_str}:\n"
            for event in events:
                start_time = event['start'].get('dateTime', event['start'].get('date'))
                if 'T' in start_time:
                    time = datetime.fromisoformat(start_time.replace('Z', '+00:00')).strftime('%I:%M %p')
                else:
                    time = "All day"
                response += f"• {time}: {event['summary']}\n"
            
            return response
            
        except Exception as e:
            print(f"Error checking schedule: {e}")
            return "I encountered an error while checking your schedule. Please try again."

    def _handle_available_slots(self, user_message: str) -> str:
        """Handle requests to find available time slots"""
        try:
            # Extract date from message
            date_str = self._extract_date_from_message(user_message)
            
            if not date_str:
                return "Please specify which date you'd like to find available slots for (e.g., 'tomorrow', 'next monday')."
            
            print(f"🔍 Looking for available slots on: {date_str}")
            
            # Parse the date
            try:
                if date_str == "today":
                    parsed_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                elif date_str == "tomorrow":
                    parsed_date = (datetime.now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                else:
                    # Try combined parsing for other formats
                    parsed_date = self.calendar_manager.parse_combined_datetime(date_str)
            except Exception as e:
                print(f"Date parsing error: {e}")
                # Fallback to simple date parsing
                try:
                    parsed_date = self.calendar_manager.parse_date_time(date_str)
                except Exception as e2:
                    print(f"Fallback date parsing error: {e2}")
                    return f"I couldn't understand the date '{date_str}'. Please try 'today', 'tomorrow', or 'next monday'."
            
            print(f"📅 Parsed date for available slots: {parsed_date}")
            
            # Get available slots (business hours: 9 AM to 6 PM, 1-hour slots)
            available_slots = self.calendar_manager.get_available_slots(parsed_date, duration_minutes=60)
            
            if not available_slots:
                return f"❌ No available 1-hour slots found for {date_str} during business hours (9 AM - 6 PM)."
            
            # Format the response
            response = f"📅 Available 1-hour slots for {date_str}:\n"
            for start_time, end_time in available_slots:
                time_slot = self.calendar_manager.format_time_slot(start_time, end_time)
                response += f"• {time_slot}\n"
            
            return response
            
        except Exception as e:
            print(f"Error finding available slots: {e}")
            return "I encountered an error while finding available slots. Please try again."

    def _handle_general_chat(self, user_message: str) -> str:
        """Handle general chat and questions"""
        try:
            prompt = f"""
            You are a helpful calendar assistant. The user said: "{user_message}"
            
            Provide a helpful response about calendar management, scheduling, or general assistance.
            Keep it concise and friendly.
            """
            
            response = self.llm_client.generate(prompt)
            return response
            
        except Exception as e:
            print(f"Error in general chat: {e}")
            return "I'm here to help with your calendar! You can ask me to book meetings, check your schedule, or find available times."

    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []

# LLM Client Classes
class GroqClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate(self, prompt: str) -> str:
        try:
            data = {
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Groq API error: {e}")
            return "I'm having trouble processing your request right now."

class OpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate(self, prompt: str) -> str:
        try:
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 500
            }
            
            response = requests.post(self.base_url, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "I'm having trouble processing your request right now."

class AnthropicClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
    
    def generate(self, prompt: str) -> str:
        try:
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(self.base_url, headers=self.headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return result["content"][0]["text"]
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return "I'm having trouble processing your request right now."

class FallbackLLM:
    def generate(self, prompt: str) -> str:
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