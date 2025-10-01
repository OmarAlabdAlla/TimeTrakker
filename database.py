"""
Database module for Time Tracking Application
Handles SQLite database operations for storing and retrieving time entries
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Tuple


class TimeTrackingDatabase:
    """Manages SQLite database operations for time tracking entries"""
    
    def __init__(self, db_name: str = "time_tracker.db"):
        """Initialize database connection and create table if it doesn't exist"""
        self.db_name = db_name
        self.create_table()
    
    def create_table(self):
        """Create the time_entries table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                total_hours REAL NOT NULL,
                task_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_entry(self, date: str, start_time: str, end_time: str, 
                  total_hours: float, task_notes: str) -> bool:
        """Add a new time entry to the database"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO time_entries (date, start_time, end_time, total_hours, task_notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, start_time, end_time, total_hours, task_notes))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding entry: {e}")
            return False
    
    def get_all_entries(self) -> List[Tuple]:
        """Retrieve all time entries from the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, date, start_time, end_time, total_hours, task_notes
            FROM time_entries
            ORDER BY date DESC, start_time DESC
        ''')
        entries = cursor.fetchall()
        conn.close()
        return entries
    
    def get_weekly_hours(self) -> float:
        """Calculate total hours for the current week"""
        today = datetime.now()
        # Get the start of the week (Monday)
        start_of_week = today - timedelta(days=today.weekday())
        start_date = start_of_week.strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(total_hours)
            FROM time_entries
            WHERE date >= ?
        ''', (start_date,))
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0
    
    def get_monthly_hours(self) -> float:
        """Calculate total hours for the current month"""
        today = datetime.now()
        start_of_month = today.replace(day=1).strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM(total_hours)
            FROM time_entries
            WHERE date >= ?
        ''', (start_of_month,))
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0.0
    
    def export_to_csv(self, filename: str = "time_entries.csv") -> bool:
        """Export all entries to a CSV file"""
        import csv
        try:
            entries = self.get_all_entries()
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Date', 'Start Time', 'End Time', 'Total Hours', 'Task/Notes'])
                writer.writerows(entries)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def export_to_excel(self, filename: str = "time_entries.xlsx") -> bool:
        """Export all entries to an Excel file"""
        from openpyxl import Workbook
        try:
            entries = self.get_all_entries()
            wb = Workbook()
            ws = wb.active
            ws.title = "Time Entries"
            
            # Add headers
            headers = ['ID', 'Date', 'Start Time', 'End Time', 'Total Hours', 'Task/Notes']
            ws.append(headers)
            
            # Add data
            for entry in entries:
                ws.append(entry)
            
            # Auto-adjust column widths
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            wb.save(filename)
            return True
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
            return False
