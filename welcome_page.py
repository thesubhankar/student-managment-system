"""
Student Management System - Welcome Page
Provides navigation to Student Login, Admin Login, and Account Registration.
"""
import os
import tkinter as tk
from student_login_page import start_student_login_page
from admin_login_page import start_admin_login_page
from creat_account_page import start_creat_account_page

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def start_welcome_page(root):
    # Load Navigation Icons
    login_student_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'login_student_img.png'))
    login_admin_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'admin_img.png'))
    newstudent_login_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'add_student_img.png'))

    root.login_student_icon = login_student_icon
    root.login_admin_icon = login_admin_icon
    root.newstudent_login_icon = newstudent_login_icon

    # Navigation Handlers
    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        start_student_login_page(root)

    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        start_admin_login_page(root)

    def forward_to_creat_account_page():
        welcome_page_fm.destroy()
        start_creat_account_page(root)

    # Main Card Container
    welcome_page_fm = tk.Frame(
        root,
        bg="#B7C3B7",
        highlightbackground="#4A5461",
        highlightthickness=3,
    )

    # Header Title
    heading_lb = tk.Label(
        welcome_page_fm,
        text='Student Registration\n& Management System',
        bg="#1e3a5f",
        fg="#ffffff",
        font=('Arial', 18, 'bold'),
    )
    heading_lb.place(x=1, y=1, width=432)

    # 1. Student Login Section
    student_login_img = tk.Button(
        welcome_page_fm,
        image=login_student_icon,
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        highlightthickness=0,
        relief='flat',
        command=forward_to_student_login_page,
    )
    student_login_img.place(x=60, y=140)

    student_login_btn = tk.Button(
        welcome_page_fm,
        text='Student Login',
        bg="#159BD7",
        fg="#FFFFFF",
        activebackground="#0D7AA8",
        activeforeground="#FFFFFF",
        font=('Arial', 16, 'bold'),
        bd=0,
        command=forward_to_student_login_page,
    )
    student_login_btn.place(x=140, y=160, width=200, height=45)

    # 2. Admin Login Section
    admin_login_img = tk.Button(
        welcome_page_fm,
        image=login_admin_icon,
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        highlightthickness=0,
        relief='flat',
        command=forward_to_admin_login_page,
    )
    admin_login_img.place(x=60, y=250)

    admin_login_btn = tk.Button(
        welcome_page_fm,
        text='Admin Login',
        bg="#159BD7",
        fg="#FFFFFF",
        activebackground="#0D7AA8",
        activeforeground="#FFFFFF",
        font=('Arial', 16, 'bold'),
        bd=0,
        command=forward_to_admin_login_page,
    )
    admin_login_btn.place(x=140, y=270, width=200, height=45)

    # 3. Create Account Section
    register_img = tk.Button(
        welcome_page_fm,
        image=newstudent_login_icon,
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        highlightthickness=0,
        relief='flat',
        command=forward_to_creat_account_page,
    )
    register_img.place(x=60, y=370)

    register_btn = tk.Button(
        welcome_page_fm,
        text='Create Account',
        bg="#159BD7",
        fg="#FFFFFF",
        activebackground="#0D7AA8",
        activeforeground="#FFFFFF",
        font=('Arial', 16, 'bold'),
        bd=0,
        command=forward_to_creat_account_page,
    )
    register_btn.place(x=140, y=390, width=200, height=45)

    # Layout Placement
    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=440, height=530)
