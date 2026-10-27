"""
Student Management System - Password Recovery Page
Allows students to recover and reset their account password by verifying their Student ID and Email.
"""
import os
import random
import tkinter as tk
from database import verify_student_recovery, update_student_password

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def start_forgot_password_page(root):
    # Load Icons
    locked_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'locked.png'))
    unlocked_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'unlocked.png'))
    root._fp_locked = locked_icon
    root._fp_unlocked = unlocked_icon

    def forward_to_login_page():
        recovery_fm.destroy()
        root.update()
        from student_login_page import start_student_login_page
        start_student_login_page(root)

    # Main Container Frame
    recovery_fm = tk.Frame(
        root,
        bg="#B7C3B7",
        highlightbackground="#4A5461",
        highlightthickness=3,
    )

    # Header Bar
    heading_lb = tk.Label(
        recovery_fm,
        text='Password Recovery',
        bg="#0C3C85",
        fg="#FFFFFF",
        font=('Arial', 18, 'bold'),
    )
    heading_lb.place(x=1, y=1, width=432)

    # Back Button
    back_btn = tk.Button(
        recovery_fm,
        text='←',
        font=('Bold', 20),
        fg="#0c1491",
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        relief='flat',
        command=forward_to_login_page,
    )
    back_btn.place(x=5, y=40)

    # Subtitle Label
    sub_lb = tk.Label(
        recovery_fm,
        text='Verify your identity to reset password',
        font=('Arial', 12, 'bold'),
        bg="#B7C3B7",
        fg="#1E3A8A",
    )
    sub_lb.place(x=65, y=55)

    # 1. Student ID Input
    id_lb = tk.Label(
        recovery_fm,
        text='Student ID Number:',
        font=('Arial', 13, 'bold'),
        bg="#B7C3B7",
        fg="#2c2977",
    )
    id_lb.place(x=50, y=95)

    id_ent = tk.Entry(
        recovery_fm,
        font=('Arial', 14, 'bold'),
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1.5,
    )
    id_ent.place(x=50, y=125, width=340, height=35)

    # 2. Registered Email Input
    email_lb = tk.Label(
        recovery_fm,
        text='Registered Email Address:',
        font=('Arial', 13, 'bold'),
        bg="#B7C3B7",
        fg="#2c2977",
    )
    email_lb.place(x=50, y=170)

    email_ent = tk.Entry(
        recovery_fm,
        font=('Arial', 14, 'bold'),
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1.5,
    )
    email_ent.place(x=50, y=200, width=340, height=35)

    # State variables
    generated_otp = tk.StringVar(value="")
    verified_id = tk.StringVar(value="")

    # Message Box Helper
    def show_msg(message, is_success=False):
        box_fm = tk.Frame(
            root,
            bg="#B7C3B7",
            highlightbackground="#048D9C",
            highlightthickness=3,
        )
        box_fm.place(x=90, y=180, width=320, height=180)

        msg_lb = tk.Label(
            box_fm,
            text=message,
            font=('Arial', 11, 'bold'),
            bg="#B7C3B7",
            fg="#081579" if not is_success else "#065F46",
            wraplength=280,
        )
        msg_lb.place(x=20, y=25, width=280)

        btn_ok = tk.Button(
            box_fm,
            text='OK',
            font=('Arial', 12, 'bold'),
            bg="#217A5A",
            fg="#FFFFFF",
            bd=0,
            command=box_fm.destroy,
        )
        btn_ok.place(x=120, y=125, width=80, height=32)

    # OTP and Reset Form Widgets (Shown in Step 2)
    otp_lb = tk.Label(recovery_fm, text='Enter 6-Digit OTP / Code:', font=('Arial', 12, 'bold'), bg="#B7C3B7", fg="#2c2977")
    otp_ent = tk.Entry(recovery_fm, font=('Arial', 13, 'bold'), highlightcolor="#831689", highlightbackground="#2B7B96", highlightthickness=1.5)

    new_pwd_lb = tk.Label(recovery_fm, text='New Password:', font=('Arial', 12, 'bold'), bg="#B7C3B7", fg="#2c2977")
    new_pwd_ent = tk.Entry(recovery_fm, font=('Arial', 13, 'bold'), show='*', highlightcolor="#831689", highlightbackground="#2B7B96", highlightthickness=1.5)

    show_btn = tk.Button(
        recovery_fm,
        image=locked_icon,
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        highlightthickness=0,
        relief='flat',
        command=lambda: toggle_pwd(),
    )

    def toggle_pwd():
        if new_pwd_ent['show'] == '*':
            new_pwd_ent.config(show='')
            show_btn.config(image=unlocked_icon)
        else:
            new_pwd_ent.config(show='*')
            show_btn.config(image=locked_icon)

    confirm_btn = tk.Button(recovery_fm, text='Reset Password', font=('Arial', 14, 'bold'), bg="#217A5A", fg="#FFFFFF", bd=0)

    # Step 1: Send OTP / Verify
    def handle_send_otp():
        id_val = id_ent.get().strip()
        email_val = email_ent.get().strip()

        if not id_val:
            show_msg("Please enter your Student ID Number")
            id_ent.focus()
            return
        if not email_val:
            show_msg("Please enter your registered Email ID")
            email_ent.focus()
            return

        student = verify_student_recovery(id_val, email_val)
        if not student:
            show_msg("Verification Failed!\nNo matching record found for this ID & Email.")
            return

        # Generate 6-digit verification code
        otp = str(random.randint(100000, 999999))
        generated_otp.set(otp)
        verified_id.set(id_val)

        # Lock ID & Email
        id_ent.config(state="readonly")
        email_ent.config(state="readonly")
        verify_btn.place_forget()

        # Display Step 2 Fields
        otp_lb.place(x=50, y=250)
        otp_ent.place(x=50, y=278, width=180, height=32)

        new_pwd_lb.place(x=50, y=320)
        new_pwd_ent.place(x=50, y=348, width=290, height=32)
        show_btn.place(x=350, y=350)

        confirm_btn.config(command=handle_confirm_reset)
        confirm_btn.place(x=120, y=410, width=200, height=42)

        show_msg(f"Verification Code Sent!\nYour OTP Code is: {otp}\n\n(Enter this code to set a new password)", is_success=True)

    def handle_confirm_reset():
        user_otp = otp_ent.get().strip()
        new_pwd = new_pwd_ent.get().strip()

        if not user_otp:
            show_msg("Please enter the 6-Digit OTP code")
            otp_ent.focus()
            return

        if user_otp != generated_otp.get():
            show_msg("Invalid OTP code! Please check and try again.")
            return

        if len(new_pwd) < 4:
            show_msg("Password must be at least 4 characters long")
            new_pwd_ent.focus()
            return

        # Update in database
        try:
            update_student_password(verified_id.get(), new_pwd)
            # Success popup with automatic redirection
            def on_success_close():
                box_fm.destroy()
                forward_to_login_page()

            box_fm = tk.Frame(root, bg="#B7C3B7", highlightbackground="#048D9C", highlightthickness=3)
            box_fm.place(x=90, y=180, width=320, height=180)
            msg_lb = tk.Label(
                box_fm,
                text="Password Reset Successful!\nYou can now log in with your new password.",
                font=('Arial', 11, 'bold'),
                bg="#B7C3B7",
                fg="#065F46",
                wraplength=280,
            )
            msg_lb.place(x=20, y=30, width=280)
            btn_ok = tk.Button(box_fm, text='Login Now', font=('Arial', 12, 'bold'), bg="#217A5A", fg="#FFFFFF", bd=0, command=on_success_close)
            btn_ok.place(x=110, y=120, width=100, height=34)

        except Exception as e:
            show_msg(f"Error resetting password: {str(e)}")

    verify_btn = tk.Button(
        recovery_fm,
        text='Verify & Get OTP',
        font=('Arial', 14, 'bold'),
        bg="#159BD7",
        fg="#FFFFFF",
        activebackground="#0D7AA8",
        activeforeground="#FFFFFF",
        bd=0,
        command=handle_send_otp,
    )
    verify_btn.place(x=120, y=260, width=200, height=42)

    # Frame Placement
    recovery_fm.pack(pady=30)
    recovery_fm.pack_propagate(False)
    recovery_fm.configure(width=440, height=530)
