import os
import tkinter as tk
from student_login_page import start_student_login_page
from admin_login_page import start_admin_login_page
from creat_account_page import start_creat_account_page


BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images') 


def start_welcome_page(root):
    login_student_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'login_student_img.png'))
    login_admin_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'admin_img.png'))
    newstudent_login_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'add_student_img.png'))

    root.login_student_icon = login_student_icon
    root.login_admin_icon = login_admin_icon
    root.newstudent_login_icon = newstudent_login_icon

    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        start_student_login_page(root)
        
    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        start_admin_login_page(root)
        
    def forward_to_creat_account_page():
        welcome_page_fm.destroy()
        start_creat_account_page(root)
        

    welcome_page_fm = tk.Frame(
        root,
        bg="#B7C3B7",
        highlightbackground="#4A5461",
        highlightthickness=3,
    )

    heading_lb = tk.Label(
        welcome_page_fm,
        text='Student Registration \n&& Managment',
        bg="#1e3a5f",
        fg="#ffffff",
        font=('Arial', 18, 'bold'),
    )
    heading_lb.place(x=1, y=1, width=432)

    student_login_btn = tk.Button(
        welcome_page_fm,
        text='login student',
        bg="#159BD7",
        fg="#FFFFFF",
        font=('Arial', 18, 'bold'),
        bd=0,
        command=forward_to_student_login_page,
    )
    student_login_btn.place(x=140, y=160, width=200)

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

    admin_login_btn = tk.Button(
        welcome_page_fm,
        text='login Admin',
        bg="#159BD7",
        fg="#FFFFFF",
        font=('Arial', 18, 'bold'),
        bd=0,
        command=forward_to_admin_login_page,
    )
    admin_login_btn.place(x=140, y=260, width=200)

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
    admin_login_img.place(x=60, y=240)

    register_btn = tk.Button(
        welcome_page_fm,
        text='Creat Account ',
        bg="#159BD7",
        fg="#FFFFFF",
        font=('Arial', 18, 'bold'),
        bd=0,
        command=forward_to_creat_account_page,
    )
    register_btn.place(x=140, y=400, width=200)

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
    register_img.place(x=60, y=380)

    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=440, height=530)
