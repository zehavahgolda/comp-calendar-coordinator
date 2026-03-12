# Comp Calendar System

A professional Python-based calendar management system designed to find available meeting slots for multiple participants.

## Key Features & Architecture

- **Layered Architecture**: Separation of concerns between Data (Repository), Business Logic (Service), and Data Models.
- **Dependency Injection**: The `CalendarService` is decoupled from the data source, allowing for high flexibility and testability.
- **Efficiency**: The search algorithm uses a linear scan with $O(N \log N)$ complexity due to initial event sorting.
- **Robustness**: Comprehensive error handling for CSV parsing, including time format validation and data cleaning.
- **Type Hinting**: Fully utilized Python's `typing` module for better code clarity and maintainability.

## Project Structure

- `io_comp/models.py`: Core data structures (`Event`).
- `io_comp/repository.py`: Data access layer for CSV operations.
- `io_comp/service.py`: Main availability logic.
- `io_comp/app.py`: Application entry point.
- `tests/`: Automated unit tests using `pytest`.


## 🚀 Advanced Features (The "Wow" Factor)

To make this system industry-ready, I implemented several advanced scheduling logics:

1. **Buffer Time Management**: The system automatically adds a 10-minute "recovery" buffer between meetings to prevent back-to-back fatigue.
2. **Golden Slot Heuristics**: Using business logic to prioritize morning slots (8:00 AM - 12:00 PM), marked with a ⭐ in the output.
3. **Lunch Break Protection**: The algorithm recognizes the 12:00-13:00 window as a low-priority zone to ensure employee well-being.
4. **Dependency Injection & Layered Architecture**: Full separation between the CSV storage, the Event model, and the Scheduling Service.
5. **Robust Parsing**: Data cleaning and error handling for malformed CSV rows to ensure the system never crashes on bad input.

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python -m io_comp.app`
3. Run tests: `pytest`