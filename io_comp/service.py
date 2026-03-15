import logging
from datetime import time, timedelta, datetime
from typing import List, Tuple
from .models import Event
from .repository import ICalendarRepository 

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class CalendarService:
    def __init__(self, repository: ICalendarRepository): 
        self.repository = repository
        self.logger = logging.getLogger(__name__)
        
        # Configuration - Centralized values to avoid Hardcoding
        self.work_start = time(8, 0)
        self.work_end = time(18, 0)
        self.buffer = timedelta(minutes=10)

    def find_slots_by_date(self, participants: List[str], target_date: str, duration: timedelta, max_slots: int = 3) -> List[time]:
        """
        Finds available meeting slots for multiple participants.
        Includes Early Exit optimization and O(n log n) efficiency.
        """
        self.logger.info(f"Searching slots for {participants} on {target_date}")
        
        all_events = self.repository.get_all_events()
        # Filtering for relevant participants and date
        relevant = [e for e in all_events if e.person_name in participants and e.event_date == target_date]
        
        # Optimization: Merge overlapping events to reduce checks in the loop
        merged_busy_periods = self._merge_events(relevant)
        
        available = []
        current = self.work_start
        
        # Main Loop: Iterates through the day to find gaps
        while self._add_minutes(current, duration) <= self.work_end:
            # OPTIMIZATION: Early Exit (Question 14)
            if len(available) >= max_slots:
                self.logger.info(f"Early exit: found requested {max_slots} slots.")
                break
                
            potential_end = self._add_minutes(current, duration)
            is_busy = False
            
            # Check if current time slot overlaps with any merged busy period
            for busy_start, busy_end in merged_busy_periods:
                # Adding buffer to the end of existing events
                busy_end_with_buffer = self._add_minutes(busy_end, self.buffer)
                
                # Overlap logic
                if not (current >= busy_end_with_buffer or potential_end <= busy_start):
                    is_busy = True
                    break
            
            if not is_busy:
                available.append(current)
                # Slot found, skip ahead (Optimization)
                current = self._add_minutes(current, timedelta(minutes=30))
            else:
                # Current time is busy, move forward to check next possibility
                current = self._add_minutes(current, timedelta(minutes=15))
        
        return available

    def _merge_events(self, events: List[Event]) -> List[Tuple[time, time]]:
        """
        Merges overlapping events into single ranges.
        Complexity: O(n log n) due to sorting.
        """
        if not events:
            return []
            
        # Sort events by start time - Essential for merging and efficiency
        sorted_events = sorted(events, key=lambda e: e.start_time)
        merged = []
        
        curr_start = sorted_events[0].start_time
        curr_end = sorted_events[0].end_time
        
        for next_event in sorted_events[1:]:
            if next_event.start_time <= curr_end:
                # Overlap detected - extend the current busy range
                curr_end = max(curr_end, next_event.end_time)
            else:
                # No overlap - save previous range and start new one
                merged.append((curr_start, curr_end))
                curr_start = next_event.start_time
                curr_end = next_event.end_time
                
        merged.append((curr_start, curr_end))
        return merged

    def _add_minutes(self, t: time, delta: timedelta) -> time:
        """Helper to safely add time and return a time object."""
        return (datetime.combine(datetime.today(), t) + delta).time()