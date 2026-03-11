from datetime import time, timedelta
from io_comp.app import find_available_slots

def test_find_slots_simple():
    # בדיקה 1: אדם אחד, לו"ז ריק
    schedules = {"Alice": []}
    duration = timedelta(hours=1)
    results = find_available_slots(["Alice"], duration, schedules)
    assert len(results) > 0
    assert results[0] == time(9, 0)

def test_find_slots_busy():
    # בדיקה 2: אדם אחד, תפוס בבוקר
    schedules = {"Alice": [(time(9, 0), time(10, 0))]}
    duration = timedelta(hours=1)
    results = find_available_slots(["Alice"], duration, schedules)
    assert time(9, 0) not in results
    assert time(10, 0) in results

def test_two_people_coordination():
    # בדיקה 3: שני אנשים עם פגישות שונות
    schedules = {
        "Alice": [(time(9, 0), time(10, 0))],
        "Bob": [(time(10, 0), time(11, 0))]
    }
    duration = timedelta(hours=1)
    results = find_available_slots(["Alice", "Bob"], duration, schedules)
    
    # אליס חוסמת את 9, בוב חוסם את 10. הזמן הראשון הפנוי לשניהם הוא 11
    assert time(9, 0) not in results
    assert time(10, 0) not in results
    assert time(11, 0) in results