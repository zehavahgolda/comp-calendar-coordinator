from dataclasses import dataclass
from datetime import time

@dataclass(frozen=True)
class Event:
    """
    Enhanced Data Model representing a calendar event.
    Now includes date and priority features for smarter scheduling.
    """
    person_name: str
    event_date: str    # Format: YYYY-MM-DD
    start_time: time
    end_time: time
    priority: str      # 'High' or 'Low' (Low priority events are 'flexible')

    def overlaps_with(self, other_start: time, other_end: time) -> bool:
        """Checks if this event conflicts with a given time range."""
        return not (self.end_time <= other_start or self.start_time >= other_end)

    @property
    def is_flexible(self) -> bool:
        """Returns True if the meeting can potentially be moved."""
        return self.priority.lower() == 'low'