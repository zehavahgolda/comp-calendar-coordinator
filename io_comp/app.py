import csv
import os
from datetime import datetime, time, timedelta
from typing import List, Dict

# הגדרות מערכת - שעות פעילות המשרד
WORK_START = time(9, 0)  
WORK_END = time(17, 0)   

def find_available_slots(person_list: List[str], event_duration: timedelta, schedules: Dict) -> List[time]:
    """
    מוצא את כל חלונות הזמן הפנויים שבהם כל האנשים ברשימה פנויים בו-זמנית.
    """
    # איסוף כל הפגישות התפוסות של כל המשתתפים
    all_busy_slots = []
    for person in person_list:
        if person in schedules:
            all_busy_slots.extend(schedules[person])
        else:
            print(f"אזהרה: המשתמש {person} לא נמצא במערכת.")
   
    # מיון חשוב לצורך ייעול החיפוש
    all_busy_slots.sort()

    available_starts = []
    
    # אתחול זמן ההתחלה לתחילת יום העבודה
    current_dt = datetime.combine(datetime.today(), WORK_START)
    end_limit = datetime.combine(datetime.today(), WORK_END)

    while current_dt + event_duration <= end_limit:
        slot_start = current_dt.time()
        slot_end = (current_dt + event_duration).time()
       
        is_free = True
        for busy_start, busy_end in all_busy_slots:
            # בדיקת חפיפה בין חלון הזמן המבוקש לפגישה קיימת
            if not (slot_end <= busy_start or slot_start >= busy_end):
                is_free = False
                # שדרוג: קפיצה לסוף הפגישה התפוסה כדי לחסוך בדיקות מיותרות
                current_dt = datetime.combine(datetime.today(), busy_end)
                break
        
        if is_free:
            available_starts.append(slot_start)
            # קפיצה של 15 דקות לחיפוש החלון הבא
            current_dt += timedelta(minutes=15)
            
    return available_starts

def load_calendar_data():
    """טוען נתוני פגישות מקובץ CSV וממיר אותם למילון של אובייקטי זמן"""
    schedules = {}
    file_path = os.path.join('resources', 'calendar.csv')
    
    if not os.path.exists(file_path):
        print(f"שגיאה: הקובץ {file_path} לא נמצא.")
        return {}

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 4: continue
            name, _, start_str, end_str = row
            try:
                start = datetime.strptime(start_str.strip(), "%H:%M").time()
                end = datetime.strptime(end_str.strip(), "%H:%M").time()
                if name not in schedules: schedules[name] = []
                schedules[name].append((start, end))
            except ValueError:
                continue
    return schedules

def main():
    """נקודת הכניסה הראשית להרצת התוכנית"""
    data = load_calendar_data()
    
    # הגדרות ברירת מחדל לבדיקה
    people = ["Alice", "Jack"]
    duration = timedelta(minutes=30)
    
    slots = find_available_slots(people, duration, data)
    
    print(f"\n--- חלונות פנויים עבור {', '.join(people)} (משך: {duration}) ---")
    if not slots:
        print("לא נמצאו חלונות זמן פנויים בשעות העבודה.")
    else:
        for s in slots:
            # חישוב זמן הסיום עבור ההדפסה
            end_time = (datetime.combine(datetime.today(), s) + duration).time()
            print(f"- {s.strftime('%H:%M')} עד {end_time.strftime('%H:%M')}")

if __name__ == "__main__":
    main()