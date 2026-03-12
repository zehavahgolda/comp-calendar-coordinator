from datetime import timedelta, time
from io_comp.repository import CalendarRepository
from io_comp.service import CalendarService

def main():
    repo = CalendarRepository('resources/calendar.csv')
    service = CalendarService(repo)

    # Configuration
    users = ["Alice", "Bob"]
    target_date = "2024-05-20"  # Example date
    meeting_len = timedelta(minutes=60)

    print("\n" + "🌟" * 20)
    print("  ENTERPRISE SCHEDULER PRO")
    print("🌟" * 20)
    print(f"📅 Date: {target_date} | 👥 Team: {', '.join(users)}")
    print("-" * 40)

    try:
        slots = service.find_slots_by_date(users, target_date, meeting_len)

        if slots:
            print(f"🎯 Found {len(slots)} optimized slots:\n")
            for s in slots:
                # UX Logic: Different icons for different times
                if s < time(12, 0):
                    status = "⭐ [GOLDEN MORNING]"
                elif time(12, 0) <= s < time(13, 30):
                    status = "🍕 [LUNCH TIME WINDOW]"
                else:
                    status = "🔹 [AFTERNOON SLOT]"
                
                print(f" {s.strftime('%H:%M')} {status}")
        else:
            print("❌ No slots found. Try changing the date or priority.")
            
    except Exception as e:
        print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()