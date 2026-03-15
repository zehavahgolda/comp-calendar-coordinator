import logging
from datetime import time, timedelta, datetime
from typing import List
from .models import Event
from .repository import ICalendarRepository 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class CalendarService:
    def __init__(self, repository: ICalendarRepository): 
        self.repository = repository
        self.logger = logging.getLogger(__name__)
        
        self.work_start = time(8, 0)
        self.work_end = time(18, 0)
        self.buffer = timedelta(minutes=10)

    def find_slots_by_date(self, participants: List[str], target_date: str, duration: timedelta) -> List[time]:
        self.logger.info(f"Searching slots for {participants} on {target_date}")
        
        all_events = self.repository.get_all_events()
        relevant = [e for e in all_events if e.person_name in participants and e.event_date == target_date]
        
        available = []
        current = self.work_start
        
        while self._add_minutes(current, duration) <= self.work_end:
            potential_end = self._add_minutes(current, duration)
            
            is_busy = False
            for event in relevant:
                event_end_with_buffer = self._add_minutes(event.end_time, self.buffer)
                if not (current >= event_end_with_buffer or potential_end <= event.start_time):
                    is_busy = True
                    break
            
            if not is_busy:
                available.append(current)
                current = self._add_minutes(current, timedelta(minutes=30))
            else:
                current = self._add_minutes(current, timedelta(minutes=15))
        
        return available

    def _add_minutes(self, t: time, delta: timedelta) -> time:
        return (datetime.combine(datetime.today(), t) + delta).time()