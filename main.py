"""
Student Management System - Main Entry Point
Launches the Tkinter application and initializes the database.
"""
import tkinter as tk
from welcome_page import start_welcome_page
from database import init_database

# 1. Initialize SQLite database tables
init_database()

# 2. Setup main application window
root = tk.Tk()
root.geometry('500x600')
root.title('Student Management System')
root.resizable(False, False)
root.configure(bg="#F8FAFC")

# 3. Open the Welcome Screen
start_welcome_page(root)

# 4. Run the Tkinter main event loop
root.mainloop()