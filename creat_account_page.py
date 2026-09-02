from email.mime import message
import os
import tkinter as tk
import random
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk



BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def start_creat_account_page(root):
    
    add_student_pic_icon=tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'add_image.png'))
    root.add_student_pic_icon=add_student_pic_icon
    
    
    
    pic_path= tk.StringVar()
    pic_path.set('')
    def open_pic():
        path = askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        
        if path:
            img= ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
            pic_path.set(path)
            
            
            add_pic_btn.config(image=img)
            add_pic_btn.image=img
    
    
    
    
    
    def forward_to_welcome_page():
        add_account_page_fm.destroy()
        root.update()
        # welcome_page()
        from welcome_page import start_welcome_page
        start_welcome_page(root)
    
    
    
    
    add_account_page_fm = tk.Frame(
        root,
        bg="#B7C3B7",
        highlightbackground="#048D9C",
        highlightthickness=3,
    )
    
    
    
    add_pic_section_fm=tk.Frame(
        add_account_page_fm,
        bg="#B7C3B7",
        highlightbackground="#0A0869",
        highlightthickness=2,
    )
    add_pic_section_fm.place(x=5,y=5,width=105,height=105)
    
    add_pic_btn=tk.Button(
        add_pic_section_fm,
        image= add_student_pic_icon,
        bg="#B7C3B7",
        activebackground="#B7C3B7",
        bd=0,
        highlightthickness=0,
        relief='flat',
        command=open_pic,
    )
    add_pic_btn.place(x=3.5,y=4)
    



    student_name_lb=tk.Label(
        add_account_page_fm,
        text='Enter Student Full Name:',
        font=('Arial',12,'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_name_lb.place(x=5,y=130)

    student_name_ent=tk.Entry(
        add_account_page_fm,
        font=('Arial',15,'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_name_ent.place(x=5,y=160,width=200)
    student_name_ent.bind("<KeyRelease>", 
                          lambda e: remove_highlight_warning(entry=student_name_ent))
    
    
    
    student_gender=tk.StringVar()
    
    student_gender_lb=tk.Label(
        add_account_page_fm,
        text='Select Student Gender:',
        font=('Arial',12,'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_gender_lb.place(x=5,y=200)
    
    male_gender_btn=tk.Radiobutton(
        add_account_page_fm,
        text='Male',
        font=('arial',12,'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
        relief='flat',
        variable=student_gender,
        value='Male',

    )
    male_gender_btn.place(x=5,y=225)
    student_gender.set('Male')
    
    femal_gender_btn=tk.Radiobutton(
        add_account_page_fm,
        text='Female',
        font=('arial',12,'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
        relief='flat',
        variable=student_gender,
        value='Female'

    )
    femal_gender_btn.place(x=100,y=225)
    
    
    
    
    student_age_lb=tk.Label(
        add_account_page_fm,
        text='Enter Student Age:',
        font=('Arial',12,'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_age_lb.place(x=5,y=260)

    student_age_ent=tk.Entry(
        add_account_page_fm,
        font=('Arial',15,'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_age_ent.place(x=5,y=290,width=200)
    student_age_ent.bind("<KeyRelease>", 
                            lambda e: remove_highlight_warning(entry=student_age_ent))
    
    
    
    student_contact_lb=tk.Label(
        add_account_page_fm,
        text='Enter Student contact no:',
        font=('Arial',12,'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_contact_lb.place(x=5,y=330)

    student_contact_ent=tk.Entry(
        add_account_page_fm,
        font=('Arial',15,'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    student_contact_ent.place(x=5,y=360,width=200)
    student_contact_ent.bind("<KeyRelease>", 
                                lambda e: remove_highlight_warning(entry=student_contact_ent))
    
    
    year_list=['1st year','2nd year','3rd year','4th year']
    select_student_class_lb=tk.Label(
        add_account_page_fm,
        text='Select Student year:',
        font=('Arial',12,'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
    )
    select_student_class_lb.place(x=5,y=405)

    select_student_class_btn=Combobox(
        add_account_page_fm,
        font=('Arial',15,'bold'),
        state='readonly',
        values=year_list
    )
    select_student_class_btn.place(x=5,y=430,width=180,height=30)
    select_student_class_btn.bind("<KeyRelease>", 
                                     lambda e: remove_highlight_warning(entry=select_student_class_btn))


    # Student ID Generate
    def generate_id():
        student_id = random.randint(1000000000, 9999999999)

        student_id_ent.config(state="normal")
        student_id_ent.delete(0, tk.END)
        student_id_ent.insert(0, str(student_id))
        student_id_ent.config(state="readonly")
        generate_id_btn.config(state="disabled")
        
        
        
        
    student_id_lb=tk.Label(
        add_account_page_fm,
        text="Student ID number:",
        font=('Arial',12,'bold'),
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1
    ) 
    student_id_lb.place(x=250,y=25)
    
    student_id_ent=tk.Entry(
        add_account_page_fm,
        font=('Arial',15,'bold'),
        bg="#FFFFFF",
        fg="#1F3789",
        bd=0,
        highlightcolor="#831689",
        highlightbackground="#2B7B96",
        highlightthickness=1,
        state="readonly",
    )
    student_id_ent.place(x=250,y=55,width=200)
    student_id_ent.bind("<KeyRelease>", 
                              lambda e: remove_highlight_warning(entry=student_id_ent))
    
    
    generate_id_btn = tk.Button(
        add_account_page_fm,
        text="Generate ID",
        font=('Arial',12,'bold'),
        bg="#C4BF9C",
        fg="#081579",
        bd=0,
        highlightcolor="#5E0663",
        highlightbackground="#2B7B96",
        highlightthickness=2,
        command=generate_id
    )
    generate_id_btn.place(x=300,y=85)
    
    id_info_lb=tk.Label(
        add_account_page_fm,
        text="  click on Generate ID button\n"
        "⚠️ Remember Using This ID Number\n"
        " Use this ID number to login",
        justify=tk.LEFT,
        anchor="w",
        padx=10,
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        # highlightcolor="#831689",
        # highlightbackground="#2B7B96",
        # highlightthickness=1,
    )
    id_info_lb.place(x=245,y=115)
    
    
    
    
    student_gmail_lb=tk.Label(
            add_account_page_fm,
            text="Enter Student Gmail ID:",
            font=('Arial',12,'bold'),
            bg='#B7C3B7',
            fg="#081579",
            bd=0,
            highlightcolor="#831689",
            highlightbackground="#2B7B96",
            highlightthickness=1
        ) 
    student_gmail_lb.place(x=250,y=175)
        
    student_gmail_ent=tk.Entry(
            add_account_page_fm,
            font=('Arial',15,'bold'),
            bg="#FFFFFF",
            fg="#1F3789",
            bd=0,
            highlightcolor="#831689",
            highlightbackground="#2B7B96",
            highlightthickness=1,
        )
    student_gmail_ent.place(x=250,y=205,width=200)
    student_gmail_ent.bind("<KeyRelease>", 
                              lambda e: remove_highlight_warning(entry=student_gmail_ent))
    
    
    gmail_info_lb=tk.Label(
        add_account_page_fm,
        text="  Via Email Adress student Can recover\n"
        "⚠️ in Case Forgating Password And\n"
        " Student will Get Future Notification",
        justify=tk.LEFT,
        anchor="w",
        padx=10,
        bg='#B7C3B7',
        fg="#081579",
        bd=0,
        # highlightcolor="#831689",
        # highlightbackground="#2B7B96",
        # highlightthickness=1,
    )
    gmail_info_lb.place(x=240,y=240)
    
    
    
    
    
    account_password_lb=tk.Label(
            add_account_page_fm,
            text="Creat Account PassWord:",
            font=('Arial',12,'bold'),
            bg='#B7C3B7',
            fg="#081579",
            bd=0,
            highlightcolor="#831689",
            highlightbackground="#2B7B96",
            highlightthickness=1
        ) 
    account_password_lb.place(x=250,y=295)
        
    account_password_ent=tk.Entry(
            add_account_page_fm,
            font=('Arial',15,'bold'),
            bg="#FFFFFF",
            fg="#1F3789",
            bd=0,
            highlightcolor="#831689",
            highlightbackground="#2B7B96",
            highlightthickness=1,
        )
    account_password_ent.place(x=250,y=325,width=200)
    account_password_ent.bind("<KeyRelease>", 
                              lambda e: remove_highlight_warning(entry=account_password_ent))
    
    password_info_lb=tk.Label(
            add_account_page_fm,
            text="Via Student Creat Password\n"
            "And Provide Student ID Number\n"
            "Student Can Login Account",
            justify=tk.LEFT,
            anchor="w",
            padx=10,
            bg='#B7C3B7',
            fg="#081579",
            bd=0,
            # highlightcolor="#831689",
            # highlightbackground="#2B7B96",
            # highlightthickness=1,
        )
    password_info_lb.place(x=250,y=360)
    
    
    
    
    def confirmation_box(meesage):
        answer = tk.BooleanVar(value=False)

        confirmation_box_fm = tk.Frame(
            root,
            # text="Do you want To Leave\nRegistration Form?",
            bg="#B7C3B7",
            highlightbackground="#048D9C",
            highlightthickness=3,
        )
        confirmation_box_fm.place(x=100, y=120, width=320, height=220)

        def action(ans):
            answer.set(ans)
            confirmation_box_fm.destroy()

        meesage_lb = tk.Label(
            confirmation_box_fm,
            text=meesage,
            font=('Arial', 12, 'bold'),
            bg='#B7C3B7',
            fg="#081579",
            bd=0,
            highlightcolor="#831689",
            highlightbackground="#2B7B96",
            highlightthickness=1
        )
        meesage_lb.place(x=70, y=30)

        cancel_btn = tk.Button(
            confirmation_box_fm,
            text='Cancel',
            font=('Arial', 15, 'bold'),
            bg="#217A5A",
            fg="#f7f1f1",
            bd=0,
            highlightcolor="#0E2879",
            highlightbackground="#0A4457",
            highlightthickness=2,
            command=lambda: action(False),
        )
        cancel_btn.place(x=50, y=160)

        yes_btn = tk.Button(
            confirmation_box_fm,
            text='Yes',
            font=('Arial', 15, 'bold'),
            bg="#223CBD",
            fg="#f7f1f1",
            bd=0,
            highlightcolor="#0E2879",
            highlightbackground="#0A4457",
            highlightthickness=2,
            command=lambda: action(True),
        )
        yes_btn.place(x=200, y=160, width=80)

        root.wait_window(confirmation_box_fm)
        return answer.get()

    def home_confirmation():
        result = confirmation_box(
            meesage="Do you want To Leave\nRegistration Form?"
        )

        if result:
            forward_to_welcome_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] == "red":
            if entry.get() != "":
                entry.config(highlightbackground="#2B7B96", highlightcolor="#831689")
    
    def check_input_validation():
            if student_name_ent.get() == "":
                student_name_ent.config(highlightbackground="red",
                                        highlightcolor="red")
                student_name_ent.focus()
                message_box(message="Please Enter Student Name")
                return False
            
            elif student_age_ent.get() == "":
                student_age_ent.config(highlightbackground="red",
                                       highlightcolor="red")
                student_age_ent.focus()
                message_box(message="Please Enter Student Age")
                return False
            
            elif student_contact_ent.get() == "":
                student_contact_ent.config(highlightbackground="red",
                                           highlightcolor="red")
                student_contact_ent.focus()
                message_box(message="Please Enter Student Contact")
                return False
            
            elif select_student_class_btn.get() == "":
                # select_student_class_btn.config(highlightbackground="red",
                #                                 highlightcolor="red")
                select_student_class_btn.focus()
                message_box(message="Please Select Student Year")
                return False
            elif student_id_ent.get() == "":
                student_id_ent.config(highlightbackground="red",
                                      highlightcolor="red")
                student_id_ent.focus()
                message_box(message="Please Generate Student ID")
                return False
            
            elif student_gmail_ent.get() == "":
                student_gmail_ent.config(highlightbackground="red",
                                         highlightcolor="red")
                student_gmail_ent.focus()
                message_box(message="Please Enter Student Gmail ID")
                return False
            
            elif account_password_ent.get() == "":
                account_password_ent.config(highlightbackground="red",
                                            highlightcolor="red")
                account_password_ent.focus()
                message_box(message="Please Enter Student Password")
                return False
            
            
    home_btn = tk.Button(
        add_account_page_fm,
        text='Home',
        font=('Arial', 18, 'bold'),
        bg="#880B14",
        fg="#f7f1f1",
        bd=0,
        highlightcolor="#0E2879",
        highlightbackground="#0A4457",
        highlightthickness=2,
        command=home_confirmation,
    )
    home_btn.place(x=240, y=420)
    
    submit_btn = tk.Button(
        add_account_page_fm,
        text='Submit',
        font=('Arial', 18, 'bold'),
        bg="#361D70",
        fg="#95a329",
        bd=0,
        highlightcolor="#6A1A6E",
        highlightbackground="#1D6177",
        highlightthickness=2,
        command=check_input_validation,
    )
    submit_btn.place(x=350, y=420)
    
    
    def message_box(message):
        message_box_fm = tk.Frame(
            root,
            bg="#B7C3B7",
            highlightbackground="#048D9C",
            highlightthickness=3,
        )
        message_box_fm.place(x=100, y=120, width=320, height=220)
        close_btn = tk.Button(
            message_box_fm,
            text='Close',
            font=('Arial', 15, 'bold'),
            bg="#217A5A",
            fg="#f7f1f1",
            bd=0,
            highlightcolor="#0E2879",
            highlightbackground="#0A4457",
            highlightthickness=2,
            command=lambda: message_box_fm.destroy(),
        )
        close_btn.place(x=120, y=160, width=80)

        message_lb=tk.Label(
            message_box_fm,
            text=message,
            font=('Arial', 12, 'bold'),
            bg="#B7C3B7",
            fg="#081579",
            bd=0,
            highlightcolor="#831689",
            highlightbackground="#2B7B96",
            highlightthickness=1
        )
        message_lb.place(x=50,y=30)


    add_account_page_fm.pack(pady=30)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width=470, height=580)

