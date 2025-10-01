"""
Time Tracking Desktop Application
A Tkinter-based GUI application for tracking work sessions with SQLite persistence
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from database import TimeTrackingDatabase


class TimeTrackerApp:
    """Main application class for the Time Tracking GUI"""
    
    def __init__(self, root):
        """Initialize the Time Tracker application"""
        self.root = root
        self.root.title("Time Tracking Application")
        self.root.geometry("900x700")
        
        # Initialize database
        self.db = TimeTrackingDatabase()
        
        # Create GUI components
        self.create_input_section()
        self.create_buttons_section()
        self.create_table_section()
        self.create_summary_section()
        
        # Load existing entries
        self.refresh_table()
        self.update_summary()
    
    def create_input_section(self):
        """Create the input fields section at the top"""
        input_frame = ttk.LabelFrame(self.root, text="Add New Entry", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Date field
        ttk.Label(input_frame, text="Date:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=15)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Start Time field
        ttk.Label(input_frame, text="Start Time:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.start_time_entry = ttk.Entry(input_frame, width=10)
        self.start_time_entry.grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(input_frame, text="(HH:MM)", font=('Arial', 8)).grid(row=0, column=4, sticky="w")
        
        # End Time field
        ttk.Label(input_frame, text="End Time:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.end_time_entry = ttk.Entry(input_frame, width=10)
        self.end_time_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(input_frame, text="(HH:MM)", font=('Arial', 8)).grid(row=1, column=2, sticky="w")
        
        # Task/Notes field
        ttk.Label(input_frame, text="Task/Notes:").grid(row=1, column=3, sticky="w", padx=5, pady=5)
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Configure column weights for responsiveness
        input_frame.columnconfigure(4, weight=1)
    
    def create_buttons_section(self):
        """Create the buttons section"""
        button_frame = ttk.Frame(self.root, padding=5)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        # Add Entry button
        self.add_button = ttk.Button(button_frame, text="Add Entry", command=self.add_entry)
        self.add_button.pack(side="left", padx=5)
        
        # Export to CSV button
        self.csv_button = ttk.Button(button_frame, text="Export to CSV", command=self.export_csv)
        self.csv_button.pack(side="left", padx=5)
        
        # Export to Excel button
        self.excel_button = ttk.Button(button_frame, text="Export to Excel", command=self.export_excel)
        self.excel_button.pack(side="left", padx=5)
        
        # Refresh button
        self.refresh_button = ttk.Button(button_frame, text="Refresh", command=self.refresh_all)
        self.refresh_button.pack(side="left", padx=5)
    
    def create_table_section(self):
        """Create the table/grid view section"""
        table_frame = ttk.LabelFrame(self.root, text="Time Entries", padding=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Create Treeview with scrollbars
        tree_scroll_y = ttk.Scrollbar(table_frame, orient="vertical")
        tree_scroll_y.pack(side="right", fill="y")
        
        tree_scroll_x = ttk.Scrollbar(table_frame, orient="horizontal")
        tree_scroll_x.pack(side="bottom", fill="x")
        
        # Define columns
        columns = ('ID', 'Date', 'Start Time', 'End Time', 'Total Hours', 'Task/Notes')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings',
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Define headings
        self.tree.heading('ID', text='ID')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Start Time', text='Start Time')
        self.tree.heading('End Time', text='End Time')
        self.tree.heading('Total Hours', text='Total Hours')
        self.tree.heading('Task/Notes', text='Task/Notes')
        
        # Define column widths
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Date', width=100, anchor='center')
        self.tree.column('Start Time', width=100, anchor='center')
        self.tree.column('End Time', width=100, anchor='center')
        self.tree.column('Total Hours', width=100, anchor='center')
        self.tree.column('Task/Notes', width=400, anchor='w')
        
        self.tree.pack(fill="both", expand=True)
    
    def create_summary_section(self):
        """Create the summary section at the bottom"""
        summary_frame = ttk.LabelFrame(self.root, text="Summary", padding=10)
        summary_frame.pack(fill="x", padx=10, pady=5)
        
        # Weekly hours
        ttk.Label(summary_frame, text="Total Hours This Week:", font=('Arial', 10, 'bold')).grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        self.weekly_hours_label = ttk.Label(summary_frame, text="0.00", font=('Arial', 10))
        self.weekly_hours_label.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Monthly hours
        ttk.Label(summary_frame, text="Total Hours This Month:", font=('Arial', 10, 'bold')).grid(
            row=0, column=2, sticky="w", padx=20, pady=5)
        self.monthly_hours_label = ttk.Label(summary_frame, text="0.00", font=('Arial', 10))
        self.monthly_hours_label.grid(row=0, column=3, sticky="w", padx=5, pady=5)
    
    def validate_time(self, time_str: str) -> bool:
        """Validate time format (HH:MM)"""
        try:
            datetime.strptime(time_str, '%H:%M')
            return True
        except ValueError:
            return False
    
    def calculate_hours(self, start_time: str, end_time: str) -> float:
        """Calculate total hours between start and end time"""
        try:
            start = datetime.strptime(start_time, '%H:%M')
            end = datetime.strptime(end_time, '%H:%M')
            
            # If end time is before start time, assume it's the next day
            if end < start:
                end += timedelta(days=1)
            
            duration = end - start
            hours = duration.total_seconds() / 3600
            return round(hours, 2)
        except Exception as e:
            print(f"Error calculating hours: {e}")
            return 0.0
    
    def add_entry(self):
        """Add a new time entry"""
        # Get input values
        date = self.date_entry.get().strip()
        start_time = self.start_time_entry.get().strip()
        end_time = self.end_time_entry.get().strip()
        task_notes = self.task_entry.get().strip()
        
        # Validate inputs
        if not date or not start_time or not end_time:
            messagebox.showerror("Error", "Please fill in Date, Start Time, and End Time!")
            return
        
        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD")
            return
        
        # Validate time formats
        if not self.validate_time(start_time):
            messagebox.showerror("Error", "Invalid start time format! Use HH:MM (e.g., 09:00)")
            return
        
        if not self.validate_time(end_time):
            messagebox.showerror("Error", "Invalid end time format! Use HH:MM (e.g., 17:00)")
            return
        
        # Calculate total hours
        total_hours = self.calculate_hours(start_time, end_time)
        
        if total_hours <= 0:
            messagebox.showerror("Error", "End time must be after start time!")
            return
        
        # Add to database
        if self.db.add_entry(date, start_time, end_time, total_hours, task_notes):
            messagebox.showinfo("Success", f"Entry added successfully! Total hours: {total_hours}")
            
            # Clear input fields (except date)
            self.start_time_entry.delete(0, tk.END)
            self.end_time_entry.delete(0, tk.END)
            self.task_entry.delete(0, tk.END)
            
            # Refresh table and summary
            self.refresh_table()
            self.update_summary()
        else:
            messagebox.showerror("Error", "Failed to add entry to database!")
    
    def refresh_table(self):
        """Refresh the table with all entries from database"""
        # Clear existing entries
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load entries from database
        entries = self.db.get_all_entries()
        for entry in entries:
            self.tree.insert('', 'end', values=entry)
    
    def update_summary(self):
        """Update the summary section with weekly and monthly totals"""
        weekly_hours = self.db.get_weekly_hours()
        monthly_hours = self.db.get_monthly_hours()
        
        self.weekly_hours_label.config(text=f"{weekly_hours:.2f} hours")
        self.monthly_hours_label.config(text=f"{monthly_hours:.2f} hours")
    
    def refresh_all(self):
        """Refresh both table and summary"""
        self.refresh_table()
        self.update_summary()
        messagebox.showinfo("Refreshed", "Data refreshed successfully!")
    
    def export_csv(self):
        """Export entries to CSV file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="time_entries.csv"
        )
        
        if filename:
            if self.db.export_to_csv(filename):
                messagebox.showinfo("Success", f"Data exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export to CSV!")
    
    def export_excel(self):
        """Export entries to Excel file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile="time_entries.xlsx"
        )
        
        if filename:
            if self.db.export_to_excel(filename):
                messagebox.showinfo("Success", f"Data exported to {filename}")
            else:
                messagebox.showerror("Error", "Failed to export to Excel!")


def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
