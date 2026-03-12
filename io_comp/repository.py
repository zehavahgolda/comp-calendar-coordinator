import csv
from typing import List
from datetime import datetime
from .models import Event

class CalendarRepository:
    """Handles advanced CSV parsing for multi-day calendars."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all_events(self) -> List[Event]:
        events = []
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        # Parsing with additional fields: date and priority
                        start_t = datetime.strptime(row['start_time'].strip(), "%H:%M").time()
                        end_t = datetime.strptime(row['end_time'].strip(), "%H:%M").time()
                        
                        events.append(Event(
                            person_name=row['name'].strip(),
                            event_date=row['date'].strip(),
                            start_time=start_t,
                            end_time=end_t,
                            priority=row.get('priority', 'High').strip()
                        ))
                    except (ValueError, KeyError):
                        continue
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
        return events