from dataclasses import dataclass
from datetime import time

# Custom Exception for Domain errors (Teacher's requirement)
class CalendarError(Exception):
    """Base class for exceptions in this module."""
    pass

class DataFileError(CalendarError):
    """Raised when the data source is missing or corrupted."""
    pass

@dataclass(frozen=True) # Checked: Already frozen!
class Event:
    person_name: str
    event_date: str
    start_time: time
    end_time: time
    priority: str

    def overlaps_with(self, other_start: time, other_end: time) -> bool:
        return not (self.end_time <= other_start or self.start_time >= other_end)