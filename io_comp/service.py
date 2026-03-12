from datetime import time, timedelta, datetime
from typing import List, Dict
from .models import Event
from .repository import CalendarRepository

class CalendarService:
    """
    Advanced Service Layer.
    Supports multi-day filtering and professional scheduling constraints.
    """

    def __init__(self, repository: CalendarRepository):
        self.repository = repository
        self.work_start = time(8, 0)
        self.work_end = time(18, 0)
        self.buffer = timedelta(minutes=10)

    def find_slots_by_date(self, participants: List[str], target_date: str, duration: timedelta) -> List[time]:
        """Finds available slots for a specific date among chosen participants."""
        all_events = self.repository.get_all_events()
        
        # Filter: Only events for these people on this specific date
        relevant = [e for e in all_events if e.person_name in participants and e.event_date == target_date]
        
        available = []
        current = self.work_start
        
        while self._add_minutes(current, duration + self.buffer) <= self.work_end:
            potential_end = self._add_minutes(current, duration)
            
            # Smart Check: Is anyone busy?
            is_busy = any(event.overlaps_with(current, potential_end) for event in relevant)
            
            if not is_busy:
                available.append(current)
                current = self._add_minutes(current, timedelta(minutes=30))
            else:
                current = self._add_minutes(current, timedelta(minutes=15))
        
        return available

    def _add_minutes(self, t: time, delta: timedelta) -> time:
        return (datetime.combine(datetime.today(), t) + delta).time()