from datetime import datetime, timedelta
from typing import Optional

class TimerUtils:
    """Timer utility functions"""
    
    @staticmethod
    def get_remaining_time(start_time: datetime, duration_minutes: int) -> timedelta:
        """Calculate remaining time"""
        if start_time is None:
            return timedelta(minutes=duration_minutes)
        
        elapsed = datetime.now() - start_time
        total_duration = timedelta(minutes=duration_minutes)
        remaining = total_duration - elapsed
        return max(remaining, timedelta(0))
    
    @staticmethod
    def format_time(time_delta: timedelta) -> str:
        """Format time delta as MM:SS"""
        total_seconds = int(time_delta.total_seconds())
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def is_time_up(start_time: datetime, duration_minutes: int) -> bool:
        """Check if time is up"""
        if start_time is None:
            return False
        elapsed = datetime.now() - start_time
        return elapsed >= timedelta(minutes=duration_minutes)