import csv
import logging
from typing import List, Protocol
from datetime import datetime
from .models import Event, DataFileError

# Define the Interface (Teacher's requirement)
class ICalendarRepository(Protocol):
    def get_all_events(self) -> List[Event]:
        ...

class CalendarRepository: # Implements ICalendarRepository
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.logger = logging.getLogger(__name__)

    def get_all_events(self) -> List[Event]:
        events = []
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        start_t = datetime.strptime(row['start_time'].strip(), "%H:%M").time()
                        end_t = datetime.strptime(row['end_time'].strip(), "%H:%M").time()
                        
                        events.append(Event(
                            person_name=row['name'].strip(),
                            event_date=row['date'].strip(),
                            start_time=start_t,
                            end_time=end_t,
                            priority=row.get('priority', 'High').strip()
                        ))
                    except (ValueError, KeyError) as e:
                        self.logger.warning(f"Skipping malformed row: {row} - Error: {e}")
                        continue
        except FileNotFoundError:
            self.logger.error(f"File not found: {self.file_path}")
            raise DataFileError(f"Could not find calendar file at {self.file_path}")
        return events