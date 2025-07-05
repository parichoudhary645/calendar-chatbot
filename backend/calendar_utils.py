"""
Google Calendar Integration Utilities
This module handles all interactions with Google Calendar API
"""

import os
from datetime import datetime, timedelta
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
        """
        Parse date and time strings into datetime objects
        Handles various formats like "tomorrow", "next Monday", etc.
        """
        from dateutil import parser
        from dateutil.relativedelta import relativedelta
        
        today = datetime.now()
        
        # Handle relative dates
        if date_str.lower() == "today":
            date_obj = today
        elif date_str.lower() == "tomorrow":
            date_obj = today + timedelta(days=1)
        elif date_str.lower().startswith("next "):
            # Handle "next Monday", "next Tuesday", etc.
            day_name = date_str.lower().replace("next ", "")
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            if day_name in days:
                target_day = days.index(day_name)
                current_day = today.weekday()
                days_ahead = target_day - current_day
                if days_ahead <= 0:  # Target day already passed this week
                    days_ahead += 7
                date_obj = today + timedelta(days=days_ahead)
            else:
                date_obj = parser.parse(date_str)
        else:
            # Try to parse as regular date
            date_obj = parser.parse(date_str)
        
        # If time is provided, combine with date
        if time_str:
            time_obj = parser.parse(time_str)
            date_obj = date_obj.replace(hour=time_obj.hour, minute=time_obj.minute)
        
        return date_obj 