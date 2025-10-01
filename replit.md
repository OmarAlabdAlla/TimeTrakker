# Time Tracking Desktop Application

## Overview
A Python desktop application for tracking work sessions with persistent SQLite storage, CSV/Excel export capabilities, and weekly/monthly summaries.

## Project Structure
- `time_tracker.py` - Main Tkinter GUI application
- `database.py` - SQLite database module for data persistence
- `time_tracker.db` - SQLite database (auto-created on first run)

## Features
✅ Tkinter-based cross-platform GUI
✅ Input fields for Date, Start Time, End Time, and Task/Notes
✅ Automatic calculation of total hours
✅ Real-time data table displaying all entries
✅ CSV export functionality
✅ Excel (.xlsx) export functionality
✅ Weekly and monthly hour summaries
✅ Time validation (HH:MM format)
✅ Persistent data storage with SQLite
✅ Security: Formula injection protection in exports
✅ Performance: Indexed date queries

## How to Use
1. The app runs automatically and displays in the VNC pane
2. Enter work session details in the input fields
3. Click "Add Entry" to save and display the entry
4. Use "Export to CSV" or "Export to Excel" to export all data
5. View weekly and monthly totals in the summary section
6. Click "Refresh" to reload data from the database

## Technical Details
- **Database**: SQLite with context managers for safe resource handling
- **Security**: Formula injection protection in CSV/Excel exports
- **Performance**: Date column indexed for faster queries
- **Validation**: Date (YYYY-MM-DD) and time (HH:MM) format validation
- **Hour Calculation**: Handles overnight sessions correctly

## Dependencies
- Python 3.11
- tkinter (built-in)
- sqlite3 (built-in)
- openpyxl (for Excel export)

## Recent Changes (October 1, 2025)
- Initial implementation of time tracking application
- Added security fixes for formula injection in exports
- Implemented context managers for database operations
- Added date index for improved query performance
- Fixed weekly/monthly queries with proper date bounds
