# 📅 Comp Calendar - Smart Meeting Coordinator

A Python-based tool designed to automate and streamline meeting scheduling between multiple participants. This system identifies available time slots by cross-referencing individual schedules while respecting predefined office hours.

## 🚀 Key Features
- **Multi-Participant Sync:** Finds optimal time slots where all required attendees are simultaneously free.
- **Office Hours Management:** Automatically restricts suggestions to standard working hours (09:00 - 17:00).
- **Smart Skip Algorithm:** Optimized search logic that bypasses busy periods to improve performance.
- **CSV Data Integration:** Dynamically loads calendar data from external CSV resources.
- **Automated Testing:** Robust logic verification using `pytest`.

## 📁 Project Structure
- `io_comp/`: Core application logic and main entry point.
- `resources/`: Data storage containing `calendar.csv`.
- `tests/`: Unit tests for ensuring algorithm reliability.
- `setup.py`: Configuration for installing the project as a Python package.

## 🛠 Installation & Usage

1. **Install the package locally:**
   Run the following command in the root directory:
   ```bash
   pip install -e .
2.Run the application:
    Comp-calendar
🧪 Running Tests
To verify the system's logic, execute the automated test suite:
    python -m pytest
