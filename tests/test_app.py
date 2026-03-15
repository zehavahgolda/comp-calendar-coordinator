import pytest
from datetime import time, timedelta
from io_comp.service import CalendarService
from io_comp.models import Event

# 1. MOCK REPOSITORY
class MockCalendarRepository:
    def get_all_events(self):
        return [
            Event(person_name="Alice", event_date="2024-05-20", start_time=time(9, 0), end_time=time(10, 0), priority="High"),
            Event(person_name="Bob", event_date="2024-05-20", start_time=time(10, 0), end_time=time(11, 0), priority="High")
        ]

# 2. FIXTURES
@pytest.fixture
def service():
    mock_repo = MockCalendarRepository()
    return CalendarService(mock_repo)

# 3. UNIT TESTS
def test_find_slots_success(service):
    slots = service.find_slots_by_date(["Alice", "Bob"], "2024-05-20", timedelta(minutes=60))
    assert len(slots) > 0
    assert time(11, 15) in slots

def test_no_slots_when_busy(service):
    slots = service.find_slots_by_date(["Alice", "Bob"], "2024-05-20", timedelta(hours=12))
    assert len(slots) == 0

def test_buffer_time_logic(service):
    slots = service.find_slots_by_date(["Alice"], "2024-05-20", timedelta(minutes=30))
    assert time(10, 0) not in slots

def test_work_day_boundaries(service):
    slots = service.find_slots_by_date(["Alice"], "2024-05-20", timedelta(minutes=30))
    for slot in slots:
        assert slot >= time(8, 0)
        assert slot <= time(18, 0)