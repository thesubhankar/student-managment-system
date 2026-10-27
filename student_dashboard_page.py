"""
Student Management System - Student Dashboard #humanrised
Provides a complete student portal with Sidebar navigation:
- Profile View (with circular/framed student photo)
- ID Card Generator & PNG Export
- My Attendance (Percentage %, Alert Badge, and History log)
- Exam Results (Marks breakdown, Grade, and Downloadable Official Report Card)
- Edit/Update Profile & Change Photo
- Security / Change Password
- Announcements & Notices
- Logout
"""
import os
import io
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

from database import (
    get_student_by_id,
    update_student,
    update_student_password,
    get_announcements,
    get_student_attendance_summary,
    get_student_attendance_history,
    get_student_marks
)
from report_card_generator import preview_report_card_window

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def make_circular_image(pil_img, size=(100, 100)):
    """Creates a clean circular cropped image using Pillow mask."""
    resized = pil_img.convert("RGBA").resize(size, Image.Resampling.LANCZOS)
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((1, 1, size[0] - 1, size[1] - 1), fill=255)
    circle_img = Image.new("RGBA", size, (0, 0, 0, 0))
    circle_img.paste(resized, (0, 0), mask=mask)
    return circle_img


def start_student_dashboard_page(root, student_data):
    """
    Renders the modern Student Dashboard.
    student_data: (id_number, password, name, age, gender, phone_number, student_class, email, image_blob)
    """
    # Resize window for comfortable dashboard experience
    root.geometry("940x650")
    root.title("Student Management System - Student Portal")

    # Load Icons
    locked_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'locked.png'))
    unlocked_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'unlocked.png'))
    root._dash_locked = locked_icon
    root._dash_unlocked = unlocked_icon

    # Maintain current student state
    current_student = list(student_data)
    # [0: id, 1: pwd, 2: name, 3: age, 4: gender, 5: phone, 6: class, 7: email, 8: image_blob]

    def get_profile_pil():
        image_blob = current_student[8] if len(current_student) > 8 else None
        if image_blob:
            try:
                return Image.open(io.BytesIO(image_blob)).convert("RGBA")
            except Exception:
                pass
        default_path = os.path.join(IMAGES_DIR, 'add_student_img.png')
        if os.path.exists(default_path):
            return Image.open(default_path).convert("RGBA")
        return Image.new("RGBA", (100, 100), color="#CBD5E1")

    # Top Header Bar
    header_fm = tk.Frame(root, bg="#1e3a5f", height=55)
    header_fm.pack(fill="x", side="top")
    header_fm.pack_propagate(False)

    app_title_lb = tk.Label(
        header_fm,
        text="🎓 Student Management System",
        font=('Arial', 16, 'bold'),
        bg="#1e3a5f",
        fg="#FFFFFF",
    )
    app_title_lb.pack(side="left", padx=20, pady=12)

    welcome_user_lb = tk.Label(
        header_fm,
        text=f"Welcome, {current_student[2]}!",
        font=('Arial', 12, 'bold'),
        bg="#1e3a5f",
        fg="#93C5FD",
    )
    welcome_user_lb.pack(side="right", padx=20, pady=12)

    # Main Workspace Container
    body_fm = tk.Frame(root, bg="#F1F5F9")
    body_fm.pack(fill="both", expand=True)

    # Left Navigation Sidebar
    sidebar_fm = tk.Frame(body_fm, bg="#0F172A", width=220)
    sidebar_fm.pack(side="left", fill="y")
    sidebar_fm.pack_propagate(False)

    # Profile Avatar in Sidebar
    avatar_canvas = tk.Label(sidebar_fm, bg="#0F172A", bd=0)
    avatar_canvas.pack(pady=(15, 6))

    def update_sidebar_avatar():
        pil_pic = get_profile_pil()
        circ_pic = make_circular_image(pil_pic, (85, 85))
        tk_pic = ImageTk.PhotoImage(circ_pic)
        avatar_canvas.config(image=tk_pic)
        avatar_canvas.image = tk_pic

    update_sidebar_avatar()

    sidebar_name_lb = tk.Label(
        sidebar_fm,
        text=current_student[2],
        font=('Arial', 11, 'bold'),
        bg="#0F172A",
        fg="#FFFFFF",
    )
    sidebar_name_lb.pack()

    sidebar_class_lb = tk.Label(
        sidebar_fm,
        text=f"Class: {current_student[6]}",
        font=('Arial', 9),
        bg="#0F172A",
        fg="#94A3B8",
    )
    sidebar_class_lb.pack(pady=(0, 10))

    tk.Frame(sidebar_fm, bg="#334155", height=1).pack(fill="x", padx=15, pady=(0, 10))

    # Content Area (Right Side)
    content_fm = tk.Frame(body_fm, bg="#F8FAFC")
    content_fm.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    nav_buttons = {}

    def set_active_button(active_key):
        for key, btn in nav_buttons.items():
            if key == active_key:
                btn.config(bg="#1E293B", fg="#38BDF8")
            else:
                btn.config(bg="#0F172A", fg="#E2E8F0")

    def clear_content():
        for widget in content_fm.winfo_children():
            widget.destroy()

    def show_popup(msg, is_error=False):
        pop = tk.Toplevel(root)
        pop.title("Alert" if is_error else "Success")
        pop.geometry("320x130")
        pop.configure(bg="#F8FAFC")
        pop.resizable(False, False)
        pop.transient(root)
        pop.grab_set()

        col = "#DC2626" if is_error else "#16A34A"
        tk.Label(pop, text=msg, font=('Arial', 10, 'bold'), bg="#F8FAFC", fg=col, wraplength=280).pack(pady=(20, 15))
        tk.Button(pop, text="OK", font=('Arial', 10, 'bold'), bg="#1E3A5F", fg="#FFFFFF", bd=0, command=pop.destroy).pack(ipadx=15, ipady=3)

    # ==========================================
    # TAB 1: PROFILE VIEW (Part 10)
    # ==========================================
    def show_profile_view():
        clear_content()
        set_active_button("profile")

        title = tk.Label(content_fm, text="My Student Profile", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=5, pady=5)

        # Profile Image
        top_box = tk.Frame(card, bg="#FFFFFF")
        top_box.pack(fill="x", padx=25, pady=(20, 10))

        raw_pic = get_profile_pil()
        circ_pic = make_circular_image(raw_pic, (110, 110))
        photo_tk = ImageTk.PhotoImage(circ_pic)

        img_lbl = tk.Label(top_box, image=photo_tk, bg="#FFFFFF", bd=0)
        img_lbl.image = photo_tk
        img_lbl.pack(side="left", padx=(0, 20))

        info_header = tk.Frame(top_box, bg="#FFFFFF")
        info_header.pack(side="left", fill="both")

        tk.Label(info_header, text=current_student[2], font=('Arial', 18, 'bold'), bg="#FFFFFF", fg="#1E293B").pack(anchor="w")
        tk.Label(info_header, text=f"Student ID: {current_student[0]}", font=('Arial', 12, 'bold'), bg="#FFFFFF", fg="#2563EB").pack(anchor="w", pady=(2, 0))
        tk.Label(info_header, text=f"Academic Year: {current_student[6]}", font=('Arial', 11), bg="#FFFFFF", fg="#64748B").pack(anchor="w", pady=(2, 0))

        tk.Frame(card, bg="#E2E8F0", height=1).pack(fill="x", padx=25, pady=10)

        # Details Grid
        details_fm = tk.Frame(card, bg="#FFFFFF")
        details_fm.pack(fill="both", expand=True, padx=30, pady=10)

        fields = [
            ("Full Name:", current_student[2]),
            ("Student ID Number:", current_student[0]),
            ("Class / Year:", current_student[6]),
            ("Age:", current_student[3]),
            ("Gender:", current_student[4]),
            ("Contact Phone:", current_student[5]),
            ("Registered Email:", current_student[7]),
        ]

        for i, (label_txt, val_txt) in enumerate(fields):
            row = i // 2
            col = (i % 2) * 2

            tk.Label(details_fm, text=label_txt, font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#64748B").grid(row=row, column=col, sticky="w", padx=(10, 5), pady=8)
            tk.Label(details_fm, text=str(val_txt), font=('Arial', 11), bg="#FFFFFF", fg="#0F172A").grid(row=row, column=col + 1, sticky="w", padx=(0, 30), pady=8)

    # ==========================================
    # TAB 2: ID CARD VIEW (Part 7)
    # ==========================================
    def show_id_card_view():
        clear_content()
        set_active_button("card")

        title = tk.Label(content_fm, text="Official Student ID Card", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 10))

        from student_card_page import draw_student_card

        card_pil = draw_student_card(
            student_name=current_student[2],
            student_class=current_student[6],
            student_age=current_student[3],
            student_id=current_student[0],
            student_image=get_profile_pil()
        )

        preview_pil = card_pil.resize((480, 300), Image.Resampling.LANCZOS)
        card_tk = ImageTk.PhotoImage(preview_pil)

        card_display = tk.Label(content_fm, image=card_tk, bg="#F8FAFC", bd=1, relief="solid")
        card_display.image = card_tk
        card_display.pack(pady=10)

        btn_row = tk.Frame(content_fm, bg="#F8FAFC")
        btn_row.pack(pady=10)

        def save_card():
            fpath = filedialog.asksaveasfilename(
                title="Save Student ID Card",
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png")],
                initialfile=f"ID_Card_{current_student[0]}.png"
            )
            if fpath:
                try:
                    card_pil.save(fpath, format="PNG")
                    show_popup("ID Card saved successfully!")
                except Exception as e:
                    show_popup(f"Failed to save card: {str(e)}", is_error=True)

        tk.Button(
            btn_row,
            text="💾 Save ID Card as PNG",
            font=('Arial', 11, 'bold'),
            bg="#2563EB",
            fg="#FFFFFF",
            bd=0,
            command=save_card,
        ).pack(side="left", padx=10, ipady=6, ipadx=15)

    # ==========================================
    # TAB 3: MY ATTENDANCE VIEW (NEW! #humanrised)
    # ==========================================
    def show_attendance_view():
        clear_content()
        set_active_button("attendance")

        title = tk.Label(content_fm, text="My Attendance & Performance Record", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 12))

        # Fetch attendance stats from database
        summary = get_student_attendance_summary(current_student[0])
        total_days = summary["total_days"]
        present_days = summary["present_days"]
        absent_days = summary["absent_days"]
        leave_days = summary["leave_days"]
        pct = summary["percentage"]

        # Metric Cards Container
        metrics_fm = tk.Frame(content_fm, bg="#F8FAFC")
        metrics_fm.pack(fill="x", pady=(0, 15))

        # Color based on 75% requirement
        pct_color = "#16A34A" if pct >= 75.0 else "#DC2626"
        alert_msg = "🟢 Status: Good Standing" if pct >= 75.0 else "⚠️ Warning: Below 75% Requirement"

        # Big Percentage Box
        pct_card = tk.Frame(metrics_fm, bg="#FFFFFF", bd=1, relief="solid", width=190, height=95)
        pct_card.pack_propagate(False)
        pct_card.pack(side="left", padx=(0, 10))

        tk.Frame(pct_card, bg=pct_color, height=4).pack(fill="x", side="top")
        tk.Label(pct_card, text="ATTENDANCE RATE", font=('Arial', 9, 'bold'), bg="#FFFFFF", fg="#64748B").pack(pady=(8, 2))
        tk.Label(pct_card, text=f"{pct:.1f}%", font=('Arial', 22, 'bold'), bg="#FFFFFF", fg=pct_color).pack()
        tk.Label(pct_card, text=alert_msg, font=('Arial', 8, 'bold'), bg="#FFFFFF", fg=pct_color).pack()

        # Breakdown Cards
        def create_att_card(parent, label_text, count_val, fg_col):
            c = tk.Frame(parent, bg="#FFFFFF", bd=1, relief="solid", width=125, height=95)
            c.pack_propagate(False)
            tk.Frame(c, bg=fg_col, height=4).pack(fill="x", side="top")
            tk.Label(c, text=label_text, font=('Arial', 9, 'bold'), bg="#FFFFFF", fg="#64748B").pack(pady=(12, 4))
            tk.Label(c, text=str(count_val), font=('Arial', 20, 'bold'), bg="#FFFFFF", fg=fg_col).pack()
            return c

        create_att_card(metrics_fm, "Total Days", total_days, "#2563EB").pack(side="left", padx=5)
        create_att_card(metrics_fm, "Present", present_days, "#16A34A").pack(side="left", padx=5)
        create_att_card(metrics_fm, "Absent", absent_days, "#DC2626").pack(side="left", padx=5)
        create_att_card(metrics_fm, "On Leave", leave_days, "#D97706").pack(side="left", padx=5)

        # Recent Logs Table
        tk.Label(content_fm, text="Recent Attendance Log", font=('Arial', 12, 'bold'), bg="#F8FAFC", fg="#1E293B").pack(anchor="w", pady=(5, 5))

        tree_frame = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True)

        history = get_student_attendance_history(current_student[0], limit=40)

        tree = ttk.Treeview(tree_frame, columns=("date", "status", "class"), show="headings", height=8)
        tree.heading("date", text="Date (YYYY-MM-DD)")
        tree.heading("status", text="Attendance Status")
        tree.heading("class", text="Academic Class")

        tree.column("date", width=180, anchor="center")
        tree.column("status", width=200, anchor="center")
        tree.column("class", width=180, anchor="center")

        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        if not history:
            tree.insert("", "end", values=("No records yet", "Attendance not yet marked by admin", current_student[6]))
        else:
            for d_val, s_val, c_val in history:
                tag = "p" if s_val == "Present" else ("a" if s_val == "Absent" else "l")
                tree.insert("", "end", values=(d_val, s_val, c_val), tags=(tag,))

        tree.tag_configure("p", foreground="#16A34A")
        tree.tag_configure("a", foreground="#DC2626")
        tree.tag_configure("l", foreground="#D97706")

    # ==========================================
    # TAB 4: EXAM RESULTS & REPORT CARD (NEW! #humanrised)
    # ==========================================
    def show_results_view():
        clear_content()
        set_active_button("results")

        title = tk.Label(content_fm, text="Academic Examinations & Grade Cards", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 10))

        records = get_student_marks(current_student[0])

        if not records:
            card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
            card.pack(fill="both", expand=True, pady=10)
            tk.Label(card, text="📝 No examination results published yet.", font=('Arial', 13, 'bold'), bg="#FFFFFF", fg="#64748B").pack(pady=40)
            tk.Label(card, text="Your examination marks and official grade cards will appear here once entered by the faculty.", font=('Arial', 10), bg="#FFFFFF", fg="#94A3B8").pack()
            return

        # Scrollable container for exams
        outer_fm = tk.Frame(content_fm, bg="#F8FAFC")
        outer_fm.pack(fill="both", expand=True)

        for exam in records:
            # exam: (id, exam_name, s1, m1, s2, m2, s3, m3, s4, m4, s5, m5, total, percentage, grade, exam_date)
            exam_name = exam[1]
            total = exam[12]
            pct = exam[13]
            grade = exam[14]
            edate = exam[15]

            exam_card = tk.Frame(outer_fm, bg="#FFFFFF", bd=1, relief="solid")
            exam_card.pack(fill="x", pady=8, padx=2)

            top_row = tk.Frame(exam_card, bg="#F8FAFC")
            top_row.pack(fill="x", padx=15, pady=(10, 6))

            tk.Label(top_row, text=f"🎓 {exam_name}", font=('Arial', 13, 'bold'), bg="#F8FAFC", fg="#1E3A5F").pack(side="left")
            tk.Label(top_row, text=f"Date: {edate}", font=('Arial', 10), bg="#F8FAFC", fg="#64748B").pack(side="right")

            # Metrics row
            metrics_row = tk.Frame(exam_card, bg="#FFFFFF")
            metrics_row.pack(fill="x", padx=15, pady=6)

            tk.Label(metrics_row, text=f"Total: {total:.1f}/500", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#1E293B").pack(side="left", padx=(0, 20))
            tk.Label(metrics_row, text=f"Percentage: {pct:.1f}%", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#2563EB").pack(side="left", padx=(0, 20))
            tk.Label(metrics_row, text=f"Grade: {grade}", font=('Arial', 12, 'bold'), bg="#FFFFFF", fg="#16A34A").pack(side="left")

            # Action button
            def download_report(rec=exam):
                preview_report_card_window(root, current_student[0], rec)

            tk.Button(
                metrics_row,
                text="📄 View & Download Official Marksheet",
                font=('Arial', 10, 'bold'),
                bg="#10B981",
                fg="#FFFFFF",
                bd=0,
                command=download_report,
            ).pack(side="right", ipady=4, ipadx=10)

    # ==========================================
    # TAB 5: EDIT PROFILE (Part 11)
    # ==========================================
    def show_edit_profile_view():
        clear_content()
        set_active_button("edit")

        title = tk.Label(content_fm, text="Edit Personal Details", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 10))

        card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=5, pady=5)

        form_fm = tk.Frame(card, bg="#FFFFFF")
        form_fm.pack(fill="both", expand=True, padx=30, pady=20)

        # Name
        tk.Label(form_fm, text="Full Name:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=0, column=0, sticky="w", pady=8)
        name_ent = tk.Entry(form_fm, font=('Arial', 10), width=35)
        name_ent.grid(row=0, column=1, sticky="w", padx=10, pady=8)
        name_ent.insert(0, current_student[2])

        # Age
        tk.Label(form_fm, text="Age:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=1, column=0, sticky="w", pady=8)
        age_ent = tk.Entry(form_fm, font=('Arial', 10), width=35)
        age_ent.grid(row=1, column=1, sticky="w", padx=10, pady=8)
        age_ent.insert(0, current_student[3])

        # Phone Number
        tk.Label(form_fm, text="Phone Number:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=2, column=0, sticky="w", pady=8)
        phone_ent = tk.Entry(form_fm, font=('Arial', 10), width=35)
        phone_ent.grid(row=2, column=1, sticky="w", padx=10, pady=8)
        phone_ent.insert(0, current_student[5])

        # Class / Year
        tk.Label(form_fm, text="Class / Year:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=3, column=0, sticky="w", pady=8)
        class_var = tk.StringVar(value=current_student[6])
        class_cb = ttk.Combobox(form_fm, textvariable=class_var, values=["1st year", "2nd year", "3rd year", "4th year"], state="readonly", width=33)
        class_cb.grid(row=3, column=1, sticky="w", padx=10, pady=8)

        # Change Photo Box
        new_photo_data = [None]
        photo_status_lbl = tk.Label(form_fm, text="No new photo chosen", font=('Arial', 9, 'italic'), bg="#FFFFFF", fg="#64748B")

        def handle_pick_photo():
            path = filedialog.askopenfilename(
                title="Select Student Photo",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
            )
            if path:
                try:
                    with open(path, "rb") as f:
                        new_photo_data[0] = f.read()
                    photo_status_lbl.config(text=f"Selected: {os.path.basename(path)}", fg="#16A34A")
                except Exception as e:
                    show_popup(f"Failed to load image: {str(e)}", is_error=True)

        tk.Label(form_fm, text="Profile Photo:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=4, column=0, sticky="w", pady=8)
        photo_btn_row = tk.Frame(form_fm, bg="#FFFFFF")
        photo_btn_row.grid(row=4, column=1, sticky="w", padx=10, pady=8)

        tk.Button(
            photo_btn_row,
            text="📁 Change Photo...",
            font=('Arial', 9, 'bold'),
            bg="#0284C7",
            fg="#FFFFFF",
            bd=0,
            command=handle_pick_photo,
        ).pack(side="left")
        photo_status_lbl.pack(side="left", padx=10)

        def handle_save_profile():
            n = name_ent.get().strip()
            a = age_ent.get().strip()
            p = phone_ent.get().strip()
            c = class_var.get().strip()

            if not n or not a or not p or not c:
                show_popup("All fields are required!", is_error=True)
                return

            try:
                pic_to_save = new_photo_data[0] if new_photo_data[0] else current_student[8]
                update_student(
                    id_number=current_student[0],
                    name=n,
                    age=a,
                    gender=current_student[4],
                    phone_number=p,
                    student_class=c,
                    email=current_student[7],
                    pic_data=pic_to_save
                )
                current_student[2] = n
                current_student[3] = a
                current_student[5] = p
                current_student[6] = c
                if new_photo_data[0]:
                    current_student[8] = new_photo_data[0]

                welcome_user_lb.config(text=f"Welcome, {n}!")
                sidebar_name_lb.config(text=n)
                sidebar_class_lb.config(text=f"Class: {c}")
                update_sidebar_avatar()
                show_popup("Profile updated successfully!")
            except Exception as e:
                show_popup(f"Failed to update profile: {str(e)}", is_error=True)

        save_btn = tk.Button(
            card,
            text="💾 Save Changes",
            font=('Arial', 11, 'bold'),
            bg="#16A34A",
            fg="#FFFFFF",
            bd=0,
            command=handle_save_profile,
        )
        save_btn.pack(pady=10, ipady=5, ipadx=15)

    # ==========================================
    # TAB 6: SECURITY / CHANGE PASSWORD (Part 11)
    # ==========================================
    def show_change_password_view():
        clear_content()
        set_active_button("password")

        title = tk.Label(content_fm, text="Security & Password Settings", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 10))

        card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=5, pady=5)

        form_fm = tk.Frame(card, bg="#FFFFFF")
        form_fm.pack(padx=30, pady=20)

        # Current Password
        tk.Label(form_fm, text="Current Password:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=0, column=0, sticky="w", pady=10)
        curr_pwd_ent = tk.Entry(form_fm, font=('Arial', 11), show="•", width=25)
        curr_pwd_ent.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # New Password
        tk.Label(form_fm, text="New Password:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=1, column=0, sticky="w", pady=10)
        new_pwd_ent = tk.Entry(form_fm, font=('Arial', 11), show="•", width=25)
        new_pwd_ent.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Confirm Password
        tk.Label(form_fm, text="Confirm Password:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=2, column=0, sticky="w", pady=10)
        conf_pwd_ent = tk.Entry(form_fm, font=('Arial', 11), show="•", width=25)
        conf_pwd_ent.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        def handle_pwd_update():
            c_p = curr_pwd_ent.get()
            n_p = new_pwd_ent.get()
            cf_p = conf_pwd_ent.get()

            if c_p != current_student[1]:
                show_popup("Incorrect Current Password!", is_error=True)
                curr_pwd_ent.focus()
                return

            if len(n_p) < 4:
                show_popup("New password must be at least 4 characters long", is_error=True)
                new_pwd_ent.focus()
                return

            if n_p != cf_p:
                show_popup("New password and confirm password do not match!", is_error=True)
                conf_pwd_ent.focus()
                return

            try:
                update_student_password(current_student[0], n_p)
                current_student[1] = n_p
                curr_pwd_ent.delete(0, tk.END)
                new_pwd_ent.delete(0, tk.END)
                conf_pwd_ent.delete(0, tk.END)
                show_popup("Password updated successfully!")
            except Exception as e:
                show_popup(f"Failed to update password: {str(e)}", is_error=True)

        up_btn = tk.Button(
            card,
            text="🔒 Update Password",
            font=('Arial', 11, 'bold'),
            bg="#2563EB",
            fg="#FFFFFF",
            bd=0,
            command=handle_pwd_update,
        )
        up_btn.pack(pady=10, ipady=5, ipadx=15)

    # ==========================================
    # TAB 7: ANNOUNCEMENTS VIEW (Part 13B)
    # ==========================================
    def show_announcements_view():
        clear_content()
        set_active_button("announcements")

        title = tk.Label(content_fm, text="College Announcements & Notices", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 15))

        announcements = get_announcements(target_class=current_student[6])

        scroll_fm = tk.Frame(content_fm, bg="#F8FAFC")
        scroll_fm.pack(fill="both", expand=True)

        if not announcements:
            empty_lb = tk.Label(
                scroll_fm,
                text="📢 No announcements posted at this time.",
                font=('Arial', 12),
                bg="#F8FAFC",
                fg="#64748B",
            )
            empty_lb.pack(pady=40)
            return

        for title_t, target_t, msg_t, date_t in announcements:
            box = tk.Frame(scroll_fm, bg="#FFFFFF", bd=1, relief="solid")
            box.pack(fill="x", pady=6, padx=5)

            top = tk.Frame(box, bg="#FFFFFF")
            top.pack(fill="x", padx=12, pady=(10, 4))

            tk.Label(top, text=f"📢 {title_t}", font=('Arial', 12, 'bold'), bg="#FFFFFF", fg="#1E3A5F").pack(side="left")
            tk.Label(top, text=f"{date_t} | Target: {target_t}", font=('Arial', 9), bg="#FFFFFF", fg="#64748B").pack(side="right")

            tk.Label(box, text=msg_t, font=('Arial', 10), bg="#FFFFFF", fg="#334155", justify="left", wraplength=550).pack(anchor="w", padx=12, pady=(0, 10))

    # ==========================================
    # LOGOUT (Returns to Welcome Page)
    # ==========================================
    def handle_logout():
        def on_confirm_logout():
            pop.destroy()
            header_fm.destroy()
            body_fm.destroy()
            root.geometry("500x600")
            root.update()
            from welcome_page import start_welcome_page
            start_welcome_page(root)

        pop = tk.Toplevel(root)
        pop.title("Confirm Logout")
        pop.geometry("300x150")
        pop.configure(bg="#F1F5F9")
        pop.resizable(False, False)
        pop.transient(root)
        pop.grab_set()

        tk.Label(pop, text="Are you sure you want to log out?", font=('Arial', 11, 'bold'), bg="#F1F5F9", fg="#0F172A").pack(pady=(25, 20))
        btn_box = tk.Frame(pop, bg="#F1F5F9")
        btn_box.pack()

        tk.Button(btn_box, text="Cancel", font=('Arial', 10), bg="#94A3B8", fg="#FFFFFF", bd=0, command=pop.destroy).pack(side="left", padx=10, ipadx=10)
        tk.Button(btn_box, text="Logout", font=('Arial', 10, 'bold'), bg="#DC2626", fg="#FFFFFF", bd=0, command=on_confirm_logout).pack(side="left", padx=10, ipadx=10)

    # Sidebar Navigation Buttons
    nav_items = [
        ("profile", "👤  My Profile", show_profile_view),
        ("card", "🪪  My ID Card", show_id_card_view),
        ("attendance", "📅  My Attendance", show_attendance_view),
        ("results", "📝  Exam Results", show_results_view),
        ("edit", "✏️  Edit Profile", show_edit_profile_view),
        ("password", "🔒  Security", show_change_password_view),
        ("announcements", "📢  Notices", show_announcements_view),
    ]

    for key, text, cmd in nav_items:
        btn = tk.Button(
            sidebar_fm,
            text=text,
            font=('Arial', 11, 'bold'),
            bg="#0F172A",
            fg="#E2E8F0",
            activebackground="#1E293B",
            activeforeground="#38BDF8",
            bd=0,
            relief='flat',
            anchor="w",
            padx=18,
            command=cmd,
        )
        btn.pack(fill="x", pady=2, ipady=5)
        nav_buttons[key] = btn

    # Logout Button at bottom of sidebar
    logout_btn = tk.Button(
        sidebar_fm,
        text="🚪  Logout",
        font=('Arial', 11, 'bold'),
        bg="#880B14",
        fg="#FFFFFF",
        activebackground="#66080E",
        activeforeground="#FFFFFF",
        bd=0,
        anchor="w",
        padx=18,
        command=handle_logout,
    )
    logout_btn.pack(side="bottom", fill="x", pady=15, ipady=6)

    # Initial View
    show_profile_view()
