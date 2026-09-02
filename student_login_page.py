import os
import tkinter as tk

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def start_student_login_page(root):
    login_student_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'login_student_img.png'))
    locked_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'locked.png'))
    unlocked_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'unlocked.png'))

    root.student_login_icon = login_student_icon
    root.locked_icon = locked_icon
    root.unlocked_icon = unlocked_icon

    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hiden_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show='*')
            show_hiden_btn.config(image=locked_icon)
            
    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        root.update()
        from welcome_page import start_welcome_page
        start_welcome_page(root)

    student_login_page_fm = tk.Frame(
        root,
        bg="#B7C3B7",
        highlightbackground="#4A5461",
        highlightthickness=3,
    )

    heading_lb = tk.Label(
        student_login_page_fm,
        text='student login page',
        bg="#0C3C85",
        fg="#B7C3B7",
        font=('Arial', 18, 'bold'),
    )
    heading_lb.place(x=1, y=1, width=432)
    
    back_btn=tk.Button(
        student_login_page_fm,
        text='←',
        font=('Bold',20),
        fg="#0c1491",
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0, 
        relief='flat',
        command=forward_to_welcome_page,
    )
    back_btn.place(x=5,y=40)

    student_icon_lb = tk.Label(
        student_login_page_fm,
        image=login_student_icon,
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        highlightthickness=0,
        relief='flat',
    )
    student_icon_lb.place(x=150, y=50)

    id_number_lb = tk.Label(
        student_login_page_fm,
        text=' Enter Student Id Number: ',
        font=('Arial', 18, 'bold'),
        bg="#B7C3B7",
        fg="#2c2977",
    )
    id_number_lb.place(x=70, y=140)

    id_number_ent = tk.Entry(
        student_login_page_fm,
        font=('Arial', 18, 'bold'),
        justify=tk.CENTER,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1.5,
    )
    id_number_ent.place(x=80, y=190)

    password_lb = tk.Label(
        student_login_page_fm,
        text=' Enter Student Password:',
        font=('Arial', 18, 'bold'),
        bg="#B7C3B7",
        fg="#2c2977",
    )
    password_lb.place(x=70, y=260)

    password_ent = tk.Entry(
        student_login_page_fm,
        font=('Arial', 18, 'bold'),
        justify=tk.CENTER,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1.5,
        show='*',
    )
    password_ent.place(x=80, y=310)

    show_hiden_btn = tk.Button(
        student_login_page_fm,
        image=locked_icon,
        bg='#B7C3B7',
        activebackground='#B7C3B7',
        bd=0,
        highlightthickness=0,
        relief='flat',
        command=show_hide_password,
    )
    show_hiden_btn.place(x=350, y=306)

    login_btn = tk.Button(
        student_login_page_fm,
        text='Login',
        font=('Arial', 18, 'bold'),
        bg="#B7C3B7",
        fg="#7e6f6f",
    )
    login_btn.place(x=110, y=390, width=200, height=40)

    forget_password_btn = tk.Button(
        student_login_page_fm,
        text='💀\nForget Password',
        bg='#B7C3B7',
        fg="#892525",
    )
    forget_password_btn.place(x=150, y=450)

    student_login_page_fm.pack(pady=30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=440, height=530)

