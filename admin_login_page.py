"""
Student Management System - Admin Login Page
Authenticates administrator credentials to access the administrative dashboard.
"""
import os
import tkinter as tk

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def start_admin_login_page(root):
    # Load UI Icons
    login_admin_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'admin_img.png'))
    locked_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'locked.png'))
    unlocked_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'unlocked.png'))

    root.login_admin_icon = login_admin_icon
    root.locked_icon = locked_icon
    root.unlocked_icon = unlocked_icon

    # Password Visibility Toggle
    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hiden_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show='*')
            show_hiden_btn.config(image=locked_icon)

    # Navigation back to Welcome Screen
    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        from welcome_page import start_welcome_page
        start_welcome_page(root)

    # Main Card Container
    admin_login_page_fm = tk.Frame(
        root,
        bg="#B7C3B7",
        highlightbackground="#4A5461",
        highlightthickness=3,
    )

    # Header Bar
    heading_lb = tk.Label(
        admin_login_page_fm,
        text='Admin Login',
        bg="#070B6F",
        fg="#F5F0F0",
        font=('Arial', 18, 'bold'),
    )
    heading_lb.place(x=1, y=1, width=432)

    # Back Button
    back_btn = tk.Button(
        admin_login_page_fm,
        text='←',
        font=('Bold', 20),
        fg="#0c1491",
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        relief='flat',
        command=forward_to_welcome_page,
    )
    back_btn.place(x=5, y=40)

    # Admin Icon
    admin_icon_lb = tk.Label(
        admin_login_page_fm,
        image=login_admin_icon,
        bg='#B7C3B7',
        bd=0,
    )
    admin_icon_lb.place(x=150, y=50)

    # Admin ID / Username Entry
    id_number_lb = tk.Label(
        admin_login_page_fm,
        text='Enter Admin Username:',
        font=('Arial', 16, 'bold'),
        bg="#B7C3B7",
        fg="#2c2977",
    )
    id_number_lb.place(x=70, y=140)

    id_number_ent = tk.Entry(
        admin_login_page_fm,
        font=('Arial', 16, 'bold'),
        justify=tk.CENTER,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1.5,
    )
    id_number_ent.place(x=80, y=185, width=280, height=35)

    # Admin Password Entry
    password_lb = tk.Label(
        admin_login_page_fm,
        text='Enter Admin Password:',
        font=('Arial', 16, 'bold'),
        bg="#B7C3B7",
        fg="#2c2977",
    )
    password_lb.place(x=70, y=245)

    password_ent = tk.Entry(
        admin_login_page_fm,
        font=('Arial', 16, 'bold'),
        justify=tk.CENTER,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1.5,
        show='*',
    )
    password_ent.place(x=80, y=290, width=280, height=35)

    # Show/Hide Password Eye Button
    show_hiden_btn = tk.Button(
        admin_login_page_fm,
        image=locked_icon,
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        highlightthickness=0,
        relief='flat',
        command=show_hide_password,
    )
    show_hiden_btn.place(x=365, y=292)

    # Message Popup Dialog
    def message_box(message):
        message_box_fm = tk.Frame(
            root,
            bg="#B7C3B7",
            highlightbackground="#048D9C",
            highlightthickness=3,
        )
        message_box_fm.place(x=90, y=180, width=320, height=180)

        message_lb = tk.Label(
            message_box_fm,
            text=message,
            font=('Arial', 12, 'bold'),
            bg="#B7C3B7",
            fg="#081579",
            wraplength=280,
        )
        message_lb.place(x=20, y=30, width=280)

        close_btn = tk.Button(
            message_box_fm,
            text='Close',
            font=('Arial', 13, 'bold'),
            bg="#217A5A",
            fg="#FFFFFF",
            bd=0,
            command=message_box_fm.destroy,
        )
        close_btn.place(x=120, y=120, width=80, height=32)

    # Admin Login Handler
    def handle_admin_login():
        admin_id = id_number_ent.get().strip()
        admin_pwd = password_ent.get().strip()

        if not admin_id:
            message_box("Please Enter Admin Username")
            id_number_ent.focus()
            return
        if not admin_pwd:
            message_box("Please Enter Admin Password")
            password_ent.focus()
            return

        # Default admin credentials check
        if admin_id == "admin" and admin_pwd == "admin123":
            admin_login_page_fm.destroy()
            root.update()
            from admin_dashboard_page import start_admin_dashboard_page
            start_admin_dashboard_page(root)
        else:
            message_box("Invalid Admin Credentials!\nDefault: admin / admin123")

    # Action Buttons
    login_btn = tk.Button(
        admin_login_page_fm,
        text='Login',
        font=('Arial', 16, 'bold'),
        bg="#159BD7",
        fg="#FFFFFF",
        activebackground="#0D7AA8",
        activeforeground="#FFFFFF",
        bd=0,
        command=handle_admin_login,
    )
    login_btn.place(x=120, y=370, width=200, height=42)

    forget_password_btn = tk.Button(
        admin_login_page_fm,
        text='💀 Forget Password?',
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        fg="#892525",
        font=('Arial', 11, 'bold'),
        bd=0,
        relief='flat',
        command=lambda: message_box("Admin default credentials are: admin / admin123"),
    )
    forget_password_btn.place(x=140, y=435)

    # Frame Placement
    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=440, height=530)
