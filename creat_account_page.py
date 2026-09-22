"""
Student Management System - Create Account Page
Allows new students to register with their personal details, photo, and account password.
"""
import os
import re
import io
import random
import base64
import subprocess
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

from database import add_data, check_id_already_exist

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


# ==========================================
# Native File Dialog for Selecting Photo
# ==========================================
def pick_image_file(root):
    """
    Opens the modern Windows File Dialog for thumbnail previews.
    Falls back to Tkinter dialog if PowerShell is not accessible.
    """
    try:
        script = """
        Add-Type -AssemblyName System.Windows.Forms
        $dlg = New-Object System.Windows.Forms.OpenFileDialog
        $dlg.Title = "Select Student Profile Photo"
        $dlg.Filter = "Image Files (*.png;*.jpg;*.jpeg;*.bmp;*.webp;*.gif)|*.png;*.jpg;*.jpeg;*.bmp;*.webp;*.gif|All Files (*.*)|*.*"
        $dlg.RestoreDirectory = $true
        if ($dlg.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            [Console]::WriteLine($dlg.FileName)
        }
        """
        enc = base64.b64encode(script.encode('utf-16le')).decode('ascii')
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0
        res = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", enc],
            capture_output=True,
            text=True,
            startupinfo=startupinfo,
            creationflags=0x08000000
        )
        selected_path = res.stdout.strip()
        if selected_path and os.path.exists(selected_path):
            return selected_path
    except Exception:
        pass

    # Fallback to standard Tkinter file picker
    return askopenfilename(
        parent=root,
        title="Select Student Profile Photo",
        filetypes=[
            ("All Images", ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp", "*.gif")),
            ("All Files", "*.*")
        ]
    )


# ==========================================
# Create Account Screen
# ==========================================
def start_creat_account_page(root):
    # Load profile placeholder icon
    add_student_pic_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'add_image.png'))
    root.add_student_pic_icon = add_student_pic_icon

    pic_path = tk.StringVar(value='')

    # Photo selector handler
    def open_pic():
        path = pick_image_file(root)
        if path:
            try:
                with Image.open(path) as raw_img:
                    resized = raw_img.convert("RGBA").resize((100, 100), Image.Resampling.LANCZOS)
                    img = ImageTk.PhotoImage(resized)
                    pic_path.set(path)
                    add_pic_btn.config(image=img)
                    add_pic_btn.image = img
            except Exception as e:
                message_box(f"Could not load image: {str(e)}")

    def forward_to_welcome_page():
        add_account_page_fm.destroy()
        root.update()
        from welcome_page import start_welcome_page
        start_welcome_page(root)

    # Main Card Frame
    add_account_page_fm = tk.Frame(
        root,
        bg="#B7C3B7",
        highlightbackground="#048D9C",
        highlightthickness=3,
    )

    # 1. Profile Picture Frame
    add_pic_section_fm = tk.Frame(
        add_account_page_fm,
        bg="#B7C3B7",
        highlightbackground="#0A0869",
        highlightthickness=2,
    )
    add_pic_section_fm.place(x=5, y=5, width=105, height=105)

    add_pic_btn = tk.Button(
        add_pic_section_fm,
        image=add_student_pic_icon,
        bg="#B7C3B7",
        activebackground="#B7C3B7",
        bd=0,
        highlightthickness=0,
        relief='flat',
        command=open_pic,
    )
    add_pic_btn.place(x=3.5, y=4)

    # 2. Student Full Name
    student_name_lb = tk.Label(
        add_account_page_fm,
        text='Enter Student Full Name:',
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    student_name_lb.place(x=5, y=130)

    student_name_ent = tk.Entry(
        add_account_page_fm,
        font=('Arial', 15, 'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_name_ent.place(x=5, y=160, width=200)
    student_name_ent.bind("<KeyRelease>", lambda e: remove_highlight_warning(entry=student_name_ent))

    # 3. Student Gender
    student_gender = tk.StringVar(value='Male')

    student_gender_lb = tk.Label(
        add_account_page_fm,
        text='Select Student Gender:',
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    student_gender_lb.place(x=5, y=200)

    male_gender_btn = tk.Radiobutton(
        add_account_page_fm,
        text='Male',
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        variable=student_gender,
        value='Male',
    )
    male_gender_btn.place(x=5, y=225)

    female_gender_btn = tk.Radiobutton(
        add_account_page_fm,
        text='Female',
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        variable=student_gender,
        value='Female'
    )
    female_gender_btn.place(x=100, y=225)

    # 4. Student Age
    student_age_lb = tk.Label(
        add_account_page_fm,
        text='Enter Student Age:',
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    student_age_lb.place(x=5, y=260)

    student_age_ent = tk.Entry(
        add_account_page_fm,
        font=('Arial', 15, 'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_age_ent.place(x=5, y=290, width=200)
    student_age_ent.bind("<KeyRelease>", lambda e: remove_highlight_warning(entry=student_age_ent))

    # 5. Student Contact Number
    student_contact_lb = tk.Label(
        add_account_page_fm,
        text='Enter Student Contact No:',
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    student_contact_lb.place(x=5, y=330)

    student_contact_ent = tk.Entry(
        add_account_page_fm,
        font=('Arial', 15, 'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_contact_ent.place(x=5, y=360, width=200)
    student_contact_ent.bind("<KeyRelease>", lambda e: remove_highlight_warning(entry=student_contact_ent))

    # 6. Student Year / Class
    year_list = ['1st year', '2nd year', '3rd year', '4th year']
    select_student_class_lb = tk.Label(
        add_account_page_fm,
        text='Select Student Year:',
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    select_student_class_lb.place(x=5, y=405)

    select_student_class_btn = Combobox(
        add_account_page_fm,
        font=('Arial', 13, 'bold'),
        state='readonly',
        values=year_list
    )
    select_student_class_btn.place(x=5, y=430, width=180, height=30)

    # 7. Student ID Generator
    def generate_id():
        while True:
            student_id = random.randint(1000000000, 9999999999)
            if not check_id_already_exist(id_number=student_id):
                student_id_ent.config(state="normal")
                student_id_ent.delete(0, tk.END)
                student_id_ent.insert(0, str(student_id))
                student_id_ent.config(state="readonly")
                generate_id_btn.config(state="disabled")
                break

    student_id_lb = tk.Label(
        add_account_page_fm,
        text="Student ID Number:",
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    student_id_lb.place(x=250, y=25)

    student_id_ent = tk.Entry(
        add_account_page_fm,
        font=('Arial', 15, 'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
        state="readonly",
    )
    student_id_ent.place(x=250, y=55, width=200)

    generate_id_btn = tk.Button(
        add_account_page_fm,
        text="Generate ID",
        font=('Arial', 12, 'bold'),
        bg="#C4BF9C",
        fg="#081579",
        bd=0,
        command=generate_id
    )
    generate_id_btn.place(x=300, y=85)

    id_info_lb = tk.Label(
        add_account_page_fm,
        text="  Click on Generate ID\n⚠️ Remember this ID number\n  Use this ID to login",
        justify=tk.LEFT,
        anchor="w",
        padx=10,
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    id_info_lb.place(x=245, y=115)

    # 8. Student Email Address
    student_gmail_lb = tk.Label(
        add_account_page_fm,
        text="Enter Student Gmail ID:",
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    student_gmail_lb.place(x=250, y=175)

    student_gmail_ent = tk.Entry(
        add_account_page_fm,
        font=('Arial', 15, 'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_gmail_ent.place(x=250, y=205, width=200)
    student_gmail_ent.bind("<KeyRelease>", lambda e: remove_highlight_warning(entry=student_gmail_ent))

    gmail_info_lb = tk.Label(
        add_account_page_fm,
        text="  Email is used for alerts &\n  Password recovery notifications",
        justify=tk.LEFT,
        anchor="w",
        padx=10,
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    gmail_info_lb.place(x=240, y=240)

    # 9. Account Password
    account_password_lb = tk.Label(
        add_account_page_fm,
        text="Create Account Password:",
        font=('Arial', 12, 'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    account_password_lb.place(x=250, y=295)

    account_password_ent = tk.Entry(
        add_account_page_fm,
        font=('Arial', 15, 'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
        show='*'
    )
    account_password_ent.place(x=250, y=325, width=200)
    account_password_ent.bind("<KeyRelease>", lambda e: remove_highlight_warning(entry=account_password_ent))

    password_info_lb = tk.Label(
        add_account_page_fm,
        text="  Student ID & Password\n  will be needed to login",
        justify=tk.LEFT,
        anchor="w",
        padx=10,
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
    )
    password_info_lb.place(x=250, y=360)

    # --- Helper Dialogs ---
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
            fg="#f7f1f1",
            bd=0,
            command=message_box_fm.destroy,
        )
        close_btn.place(x=120, y=120, width=80, height=32)

    def confirmation_box(message_text):
        answer = tk.BooleanVar(value=False)

        confirmation_box_fm = tk.Frame(
            root,
            bg="#B7C3B7",
            highlightbackground="#048D9C",
            highlightthickness=3,
        )
        confirmation_box_fm.place(x=90, y=180, width=320, height=180)

        def action(ans):
            answer.set(ans)
            confirmation_box_fm.destroy()

        meesage_lb = tk.Label(
            confirmation_box_fm,
            text=message_text,
            font=('Arial', 12, 'bold'),
            bg='#B7C3B7',
            fg="#081579",
            wraplength=280,
        )
        meesage_lb.place(x=20, y=30, width=280)

        cancel_btn = tk.Button(
            confirmation_box_fm,
            text='Cancel',
            font=('Arial', 12, 'bold'),
            bg="#217A5A",
            fg="#FFFFFF",
            bd=0,
            command=lambda: action(False),
        )
        cancel_btn.place(x=60, y=120, width=80, height=32)

        yes_btn = tk.Button(
            confirmation_box_fm,
            text='Yes',
            font=('Arial', 12, 'bold'),
            bg="#880B14",
            fg="#FFFFFF",
            bd=0,
            command=lambda: action(True),
        )
        yes_btn.place(x=180, y=120, width=80, height=32)

        root.wait_window(confirmation_box_fm)
        return answer.get()

    def home_confirmation():
        if confirmation_box("Do you want to leave the registration form?"):
            forward_to_welcome_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] == "red" and entry.get() != "":
            entry.config(highlightbackground="#2B7B96", highlightcolor="#831689")

    def check_invalid_email(email):
        pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        return not bool(re.match(pattern, email))

    # --- Validation & Submit Logic ---
    def check_input_validation():
        name_val = student_name_ent.get().strip()
        age_val = student_age_ent.get().strip()
        contact_val = student_contact_ent.get().strip()
        class_val = select_student_class_btn.get().strip()
        id_val = student_id_ent.get().strip()
        email_val = student_gmail_ent.get().strip()
        pwd_val = account_password_ent.get().strip()

        if not name_val:
            student_name_ent.config(highlightbackground="red", highlightcolor="red")
            student_name_ent.focus()
            message_box("Please Enter Student Name")
            return

        if not age_val:
            student_age_ent.config(highlightbackground="red", highlightcolor="red")
            student_age_ent.focus()
            message_box("Please Enter Student Age")
            return

        if not contact_val:
            student_contact_ent.config(highlightbackground="red", highlightcolor="red")
            student_contact_ent.focus()
            message_box("Please Enter Student Contact")
            return

        if not class_val:
            select_student_class_btn.focus()
            message_box("Please Select Student Year")
            return

        if not id_val:
            student_id_ent.config(highlightbackground="red", highlightcolor="red")
            student_id_ent.focus()
            message_box("Please Click 'Generate ID'")
            return

        if not email_val:
            student_gmail_ent.config(highlightbackground="red", highlightcolor="red")
            student_gmail_ent.focus()
            message_box("Please Enter Student Gmail ID")
            return

        if check_invalid_email(email_val.lower()):
            student_gmail_ent.config(highlightbackground="red", highlightcolor="red")
            student_gmail_ent.focus()
            message_box("Please Enter a Valid Gmail ID")
            return

        if not pwd_val:
            account_password_ent.config(highlightbackground="red", highlightcolor="red")
            account_password_ent.focus()
            message_box("Please Enter Student Password")
            return

        # Prepare Student Photo BLOB
        pic_data = b''
        if pic_path.get():
            try:
                with Image.open(pic_path.get()) as raw_img:
                    resized = raw_img.convert("RGBA").resize((100, 100), Image.Resampling.LANCZOS)
                    buffer = io.BytesIO()
                    resized.save(buffer, format="PNG")
                    pic_data = buffer.getvalue()
            except Exception:
                pic_data = b''
        else:
            default_img_path = os.path.join(IMAGES_DIR, 'add_student_img.png')
            if os.path.exists(default_img_path):
                with open(default_img_path, 'rb') as f:
                    pic_data = f.read()

        # Save to Database
        try:
            add_data(
                id_number=id_val,
                password=pwd_val,
                name=name_val,
                age=age_val,
                gender=student_gender.get(),
                phone_number=contact_val,
                student_class=class_val,
                email=email_val,
                pic_data=pic_data
            )
            message_box("Account Created Successfully!")

            # Clear Form
            student_name_ent.delete(0, tk.END)
            student_age_ent.delete(0, tk.END)
            student_contact_ent.delete(0, tk.END)
            select_student_class_btn.set('')
            student_gmail_ent.delete(0, tk.END)
            account_password_ent.delete(0, tk.END)
            student_id_ent.config(state="normal")
            student_id_ent.delete(0, tk.END)
            student_id_ent.config(state="readonly")
            generate_id_btn.config(state="normal")
            pic_path.set('')
            add_pic_btn.config(image=add_student_pic_icon)
        except Exception as e:
            message_box(f"Database Error: {str(e)}")

    # Action Buttons
    home_btn = tk.Button(
        add_account_page_fm,
        text='Home',
        font=('Arial', 16, 'bold'),
        bg="#880B14",
        fg="#FFFFFF",
        activebackground="#66080E",
        activeforeground="#FFFFFF",
        bd=0,
        command=home_confirmation,
    )
    home_btn.place(x=240, y=420, width=90, height=42)

    submit_btn = tk.Button(
        add_account_page_fm,
        text='Submit',
        font=('Arial', 16, 'bold'),
        bg="#361D70",
        fg="#FFFFFF",
        activebackground="#271552",
        activeforeground="#FFFFFF",
        bd=0,
        command=check_input_validation,
    )
    submit_btn.place(x=345, y=420, width=95, height=42)

    # Frame Placement
    add_account_page_fm.pack(pady=30)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width=470, height=580)
