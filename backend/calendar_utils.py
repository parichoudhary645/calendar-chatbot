"""
Google Calendar Integration Utilities
This module handles all interactions with Google Calendar API
"""

import os
from datetime import datetime, timedelta, time
from typing import List, Dict, Optional, Tuple
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz

class CalendarManager:
    """Manages Google Calendar operations with a friendly, human-like approach"""
    
    def __init__(self, service_account_file: str = "service_account.json"):
        """Initialize the calendar manager with service account credentials"""
        self.service_account_file = service_account_file
        self.calendar_service = None
        self.calendar_id = "primary"  # Use primary calendar by default
        self.timezone = pytz.timezone('UTC')  # Default timezone
        
        # Initialize the calendar service
        self._initialize_service()
    
    def _initialize_service(self):
        """Set up the Google Calendar API service"""
        try:
            # Load service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file,
                scopes=['https://www.googleapis.com/auth/calendar']
            )
            
            # Build the calendar service
            self.calendar_service = build('calendar', 'v3', credentials=credentials)
            print("✅ Calendar service initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing calendar service: {e}")
            raise
    
    def check_availability(self, start_time: datetime, end_time: datetime) -> bool:
        """
        Check if a time slot is available
        Returns True if available, False if busy
        """
        try:
            # Format times for API
            start_str = start_time.isoformat() + 'Z'
            end_str = end_time.isoformat() + 'Z'
            
            # Query for events in the time range
            events_result = self.calendar_service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_str,
                timeMax=end_str,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # If no events found, the slot is available
            return len(events) == 0
            
        except HttpError as error:
            print(f"❌ Error checking availability: {error}")
            return False
    
    def get_available_slots(self, date: datetime, duration_minutes: int = 60) -> List[Tuple[datetime, datetime]]:
        """
        Find available time slots for a given date
        Returns list of (start_time, end_time) tuples
        """
        available_slots = []
        
        # Define business hours (9 AM to 6 PM)
        business_start = date.replace(hour=9, minute=0, second=0, microsecond=0)
        business_end = date.replace(hour=18, minute=0, second=0, microsecond=0)
        
        # Check every 30-minute slot
        current_time = business_start
        while current_time + timedelta(minutes=duration_minutes) <= business_end:
            end_time = current_time + timedelta(minutes=duration_minutes)
            
            if self.check_availability(current_time, end_time):
                available_slots.append((current_time, end_time))
            
            current_time += timedelta(minutes=30)
        
        return available_slots
    
    def create_event(self, summary: str, start_time: datetime, end_time: datetime, 
                    description: str = "", attendee_email: str = None) -> Dict:
        """
        Create a new calendar event
        Returns the created event details
        """
        try:
            # Prepare event details
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            # Add attendee if provided
            if attendee_email:
                event['attendees'] = [{'email': attendee_email}]
            
            # Create the event
            created_event = self.calendar_service.events().insert(
                calendarId=self.calendar_id,
                body=event,
                sendUpdates='all'  # Send email notifications
            ).execute()
            
            print(f"✅ Event created successfully: {summary}")
            return created_event
            
        except HttpError as error:
            print(f"❌ Error creating event: {error}")
            raise
    
    def get_events_for_date(self, date: datetime) -> List[Dict]:
        """
        Get all events for a specific date
        Returns list of event dictionaries
        """
        try:
            # Set time range for the entire day
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            events_result = self.calendar_service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_of_day.isoformat() + 'Z',
                timeMax=end_of_day.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            return events_result.get('items', [])
            
        except HttpError as error:
            print(f"❌ Error getting events: {error}")
            return []
    
    def format_time_slot(self, start_time: datetime, end_time: datetime) -> str:
        """Format a time slot in a human-friendly way"""
        start_str = start_time.strftime("%I:%M %p")
        end_str = end_time.strftime("%I:%M %p")
        return f"{start_str} - {end_str}"
    
    def parse_date_time(self, date_str: str, time_str: str = None) -> datetime:
        """Parse date and time strings into a datetime object"""
        try:
            # Handle None values
            if not date_str:
                raise ValueError("Date string is None or empty")
            
            date_str = date_str.strip().lower()
            
            # Get current date
            now = datetime.now()
            
            # Parse date
            if date_str == "today":
                target_date = now.date()
            elif date_str == "tomorrow":
                target_date = now.date() + timedelta(days=1)
            elif date_str == "next week":
                target_date = now.date() + timedelta(days=7)
            elif date_str.startswith("next "):
                # Handle "next monday", "next tuesday", etc.
                day_name = date_str[5:]  # Remove "next "
                day_map = {
                    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                    "friday": 4, "saturday": 5, "sunday": 6
                }
                if day_name in day_map:
                    target_day = day_map[day_name]
                    current_day = now.weekday()
                    days_ahead = target_day - current_day
                    if days_ahead <= 0:  # Target day already happened this week
                        days_ahead += 7
                    target_date = now.date() + timedelta(days=days_ahead)
                else:
                    raise ValueError(f"Unknown day: {day_name}")
            else:
                # Try to parse as a specific date
                try:
                    # Try different date formats
                    for fmt in ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%B %d", "%b %d"]:
                        try:
                            if fmt in ["%B %d", "%b %d"]:
                                # Add current year for month/day formats
                                date_with_year = f"{date_str} {now.year}"
                                target_date = datetime.strptime(date_with_year, f"{fmt} %Y").date()
                                # If the date has passed, use next year
                                if target_date < now.date():
                                    target_date = datetime.strptime(f"{date_str} {now.year + 1}", f"{fmt} %Y").date()
                                break
                            else:
                                target_date = datetime.strptime(date_str, fmt).date()
                                break
                        except ValueError:
                            continue
                    else:
                        raise ValueError(f"Could not parse date: {date_str}")
                except Exception as e:
                    print(f"Date parsing error: {e}")
                    # Default to today if parsing fails
                    target_date = now.date()
            
            # Parse time
            if time_str:
                time_str = time_str.strip().lower()
                try:
                    # Try different time formats
                    for fmt in ["%I:%M %p", "%I %p", "%H:%M", "%H"]:
                        try:
                            if fmt in ["%I %p", "%H"]:
                                # Add minutes for hour-only formats
                                time_with_minutes = f"{time_str}:00"
                                if fmt == "%I %p":
                                    time_with_minutes = f"{time_str}:00"
                                else:
                                    time_with_minutes = f"{time_str}:00"
                                target_time = datetime.strptime(time_with_minutes, "%H:%M").time()
                                break
                            else:
                                target_time = datetime.strptime(time_str, fmt).time()
                                break
                        except ValueError:
                            continue
                    else:
                        # Try simple hour extraction
                        import re
                        hour_match = re.search(r'(\d{1,2})', time_str)
                        if hour_match:
                            hour = int(hour_match.group(1))
                            if "pm" in time_str and hour != 12:
                                hour += 12
                            elif "am" in time_str and hour == 12:
                                hour = 0
                            target_time = time(hour=hour, minute=0)
                        else:
                            # Default to current time
                            target_time = now.time()
                except Exception as e:
                    print(f"Time parsing error: {e}")
                    # Default to current time if parsing fails
                    target_time = now.time()
            else:
                # Default to current time if no time provided
                target_time = now.time()
            
            # Combine date and time
            return datetime.combine(target_date, target_time)
            
        except Exception as e:
            print(f"Date/time parsing error: {e}")
            # Return current time as fallback
            return datetime.now()
    
    def parse_combined_datetime(self, datetime_str: str) -> datetime:
        """
        Parse combined date-time strings like "tomorrow 3pm", "today 2:30pm", etc.
        """
        from dateutil import parser
        import re
        
        today = datetime.now()
        datetime_str = datetime_str.lower().strip()
        
        # Handle common patterns
        if "tomorrow" in datetime_str:
            # Extract time from "tomorrow 3pm" or "tomorrow at 3pm"
            time_match = re.search(r'tomorrow\s+(?:at\s+)?(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', datetime_str)
            if time_match:
                time_str = time_match.group(1)
                date_obj = today + timedelta(days=1)
                return self._combine_date_and_time(date_obj, time_str)
        
        elif "today" in datetime_str:
            # Extract time from "today 3pm" or "today at 3pm"
            time_match = re.search(r'today\s+(?:at\s+)?(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', datetime_str)
            if time_match:
                time_str = time_match.group(1)
                return self._combine_date_and_time(today, time_str)
        
        # Try to parse as regular datetime
        try:
            return parser.parse(datetime_str)
        except:
            raise ValueError(f"Could not parse datetime: {datetime_str}")
    
    def _combine_date_and_time(self, date_obj: datetime, time_str: str) -> datetime:
        """
        Combine a date object with a time string
        """
        from dateutil import parser
        
        # Parse the time string
        time_obj = parser.parse(time_str)
        
        # Combine date and time
        combined = date_obj.replace(
            hour=time_obj.hour,
            minute=time_obj.minute,
            second=0,
            microsecond=0
        )
        
        return combined 