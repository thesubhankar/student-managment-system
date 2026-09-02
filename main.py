import tkinter as tk
from welcome_page import start_welcome_page


root = tk.Tk()
root.geometry('500x600')
root.title('student managment system')
root.resizable(False, False)
root.configure(bg="#F8FAFC")

start_welcome_page(root)
root.mainloop()