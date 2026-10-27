"""
Student Management System - Student Dashboard
Provides a complete student portal with Sidebar navigation:
- Profile View (with circular/framed student photo)
- ID Card Generator & PNG Export
- Edit/Update Profile & Change Photo
- Security / Change Password
- Announcements & Notices
- Logout
"""
import os
import io
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont

from database import (
    get_student_by_id,
    update_student,
    update_student_password,
    get_announcements
)

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
    # Resize window for dashboard experience
    root.geometry("860x620")
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

    # Sidebar Student Avatar & Name
    avatar_canvas = tk.Canvas(sidebar_fm, width=90, height=90, bg="#0F172A", bd=0, highlightthickness=0)
    avatar_canvas.pack(pady=(20, 5))

    sidebar_name_lb = tk.Label(
        sidebar_fm,
        text=current_student[2],
        font=('Arial', 11, 'bold'),
        bg="#0F172A",
        fg="#FFFFFF",
        wraplength=190,
    )
    sidebar_name_lb.pack()

    sidebar_id_lb = tk.Label(
        sidebar_fm,
        text=f"ID: {current_student[0]}",
        font=('Arial', 9),
        bg="#0F172A",
        fg="#94A3B8",
    )
    sidebar_id_lb.pack(pady=(0, 15))

    tk.Frame(sidebar_fm, bg="#334155", height=1).pack(fill="x", padx=15, pady=(0, 15))

    # Content Area (Right Side)
    content_fm = tk.Frame(body_fm, bg="#F8FAFC")
    content_fm.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    def refresh_sidebar_avatar():
        pil_img = get_profile_pil()
        circ = make_circular_image(pil_img, size=(80, 80))
        tk_circ = ImageTk.PhotoImage(circ)
        sidebar_fm._avatar = tk_circ
        avatar_canvas.delete("all")
        avatar_canvas.create_image(45, 45, image=tk_circ)
        sidebar_name_lb.config(text=current_student[2])
        welcome_user_lb.config(text=f"Welcome, {current_student[2]}!")

    refresh_sidebar_avatar()

    # Active Tab Buttons Management
    nav_buttons = {}

    def set_active_button(tab_key):
        for k, btn in nav_buttons.items():
            if k == tab_key:
                btn.config(bg="#1E293B", fg="#38BDF8")
            else:
                btn.config(bg="#0F172A", fg="#E2E8F0")

    def clear_content():
        for widget in content_fm.winfo_children():
            widget.destroy()

    # Generic Message Popup
    def show_popup(msg, is_error=False):
        pop = tk.Toplevel(root)
        pop.title("Notification")
        pop.geometry("320x160")
        pop.configure(bg="#F1F5F9")
        pop.resizable(False, False)
        pop.transient(root)
        pop.grab_set()

        lbl = tk.Label(
            pop,
            text=msg,
            font=('Arial', 11, 'bold'),
            bg="#F1F5F9",
            fg="#DC2626" if is_error else "#0F766E",
            wraplength=280,
            justify="center",
        )
        lbl.pack(expand=True, padx=15, pady=15)

        ok_b = tk.Button(
            pop,
            text="OK",
            font=('Arial', 11, 'bold'),
            bg="#1E3A5F",
            fg="#FFFFFF",
            bd=0,
            command=pop.destroy,
        )
        ok_b.pack(pady=(0, 15), ipadx=15, ipady=3)

    # ==========================================
    # TAB 1: PROFILE VIEW (Part 10)
    # ==========================================
    def show_profile_view():
        clear_content()
        set_active_button("profile")

        title = tk.Label(content_fm, text="Student Profile", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid", highlightthickness=0)
        card.pack(fill="both", expand=True, padx=5, pady=5)

        # Photo & Quick Info Header
        top_row = tk.Frame(card, bg="#FFFFFF")
        top_row.pack(fill="x", padx=25, pady=20)

        photo_canvas = tk.Canvas(top_row, width=100, height=100, bg="#FFFFFF", bd=0, highlightthickness=0)
        photo_canvas.pack(side="left", padx=(0, 20))
        circ_photo = make_circular_image(get_profile_pil(), size=(96, 96))
        card._photo_tk = ImageTk.PhotoImage(circ_photo)
        photo_canvas.create_image(50, 50, image=card._photo_tk)

        info_header = tk.Frame(top_row, bg="#FFFFFF")
        info_header.pack(side="left", fill="both", expand=True)

        tk.Label(info_header, text=current_student[2], font=('Arial', 16, 'bold'), bg="#FFFFFF", fg="#0F172A").pack(anchor="w")
        tk.Label(info_header, text=f"Roll / Student ID: {current_student[0]}", font=('Arial', 12, 'bold'), bg="#FFFFFF", fg="#2563EB").pack(anchor="w", pady=2)
        tk.Label(info_header, text=f"Class / Year: {current_student[6]}", font=('Arial', 11), bg="#FFFFFF", fg="#475569").pack(anchor="w")

        tk.Frame(card, bg="#E2E8F0", height=1).pack(fill="x", padx=25, pady=10)

        # Detailed Grid
        grid_fm = tk.Frame(card, bg="#FFFFFF")
        grid_fm.pack(fill="both", expand=True, padx=30, pady=10)

        fields = [
            ("Full Name:", current_student[2]),
            ("Student ID Number:", current_student[0]),
            ("Academic Year / Class:", current_student[6]),
            ("Gender / Age:", f"{current_student[4]} / {current_student[3]} years"),
            ("Contact Phone Number:", current_student[5]),
            ("Email Address:", current_student[7]),
            ("Account Status:", "Active / Enrolled ✅"),
        ]

        for i, (label_txt, val_txt) in enumerate(fields):
            tk.Label(grid_fm, text=label_txt, font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=i, column=0, sticky="w", pady=6)
            tk.Label(grid_fm, text=val_txt, font=('Arial', 11), bg="#FFFFFF", fg="#0F172A").grid(row=i, column=1, sticky="w", padx=20, pady=6)

    # ==========================================
    # TAB 2: STUDENT ID CARD VIEW
    # ==========================================
    def show_id_card_view():
        clear_content()
        set_active_button("card")

        top_bar = tk.Frame(content_fm, bg="#F8FAFC")
        top_bar.pack(fill="x", pady=(0, 10))

        tk.Label(top_bar, text="Student Identity Card", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(side="left")

        # Frame Container for the ID card canvas
        card_wrap = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        card_wrap.pack(pady=10)

        frame_path = os.path.join(IMAGES_DIR, 'student_card_frame.png')
        card_w, card_h = 340, 340
        if os.path.exists(frame_path):
            frame_pil = Image.open(frame_path).convert("RGBA").resize((card_w, card_h), Image.Resampling.LANCZOS)
        else:
            frame_pil = Image.new("RGBA", (card_w, card_h), color="#FFFFFF")
        card_bg_tk = ImageTk.PhotoImage(frame_pil)
        content_fm._card_bg = card_bg_tk

        canvas = tk.Canvas(card_wrap, width=card_w, height=card_h, bg="#FFFFFF", bd=0, highlightthickness=0)
        canvas.pack()

        # Draw frame background
        canvas.create_image(0, 0, anchor="nw", image=card_bg_tk)

        # Header Titles
        canvas.create_text(card_w // 2, 32, text="STUDENT MANAGEMENT SYSTEM", font=('Arial', 9, 'bold'), fill="#1e3a5f")
        canvas.create_text(card_w // 2, 48, text="STUDENT IDENTITY CARD", font=('Arial', 11, 'bold'), fill="#081579")
        canvas.create_line(25, 60, card_w - 25, 60, fill="#048D9C", width=2)

        # Photo
        prof_pil = get_profile_pil().resize((65, 65), Image.Resampling.LANCZOS)
        prof_tk = ImageTk.PhotoImage(prof_pil)
        content_fm._prof_tk = prof_tk

        canvas.create_rectangle(30, 72, 98, 140, outline="#1e3a5f", width=2, fill="#FFFFFF")
        canvas.create_image(32, 74, anchor="nw", image=prof_tk)

        # Name & ID beside photo
        canvas.create_text(110, 78, anchor="nw", text=current_student[2], font=('Arial', 11, 'bold'), fill="#1e3a5f")
        canvas.create_text(110, 100, anchor="nw", text=f"ID: {current_student[0]}", font=('Arial', 10, 'bold'), fill="#081579")
        canvas.create_text(110, 120, anchor="nw", text=f"Year: {current_student[6]}", font=('Arial', 10), fill="#334155")

        canvas.create_line(25, 150, card_w - 25, 150, fill="#CBD5E1", width=1)

        # Details list
        details_list = [
            ("Gender / Age:", f"{current_student[4]} / {current_student[3]} yrs"),
            ("Contact No:", current_student[5]),
            ("Email ID:", current_student[7]),
        ]
        curr_y = 165
        for lbl_t, val_t in details_list:
            canvas.create_text(30, curr_y, anchor="nw", text=lbl_t, font=('Arial', 9, 'bold'), fill="#475569")
            canvas.create_text(125, curr_y, anchor="nw", text=val_t, font=('Arial', 9), fill="#0F172A")
            curr_y += 28

        canvas.create_line(25, 290, card_w - 25, 290, fill="#048D9C", width=1.5)
        canvas.create_text(card_w // 2, 310, text="Authorized Student Identity", font=('Arial', 8, 'italic'), fill="#64748B")

        # Save Card Image Handler
        def handle_save_card():
            path = filedialog.asksaveasfilename(
                title="Save Student Card Image",
                defaultextension=".png",
                initialfile=f"student_card_{current_student[0]}.png",
                filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
            )
            if not path:
                return

            try:
                card_img = frame_pil.copy()
                draw = ImageDraw.Draw(card_img)

                # Paste photo
                card_img.paste(prof_pil, (32, 74), prof_pil)
                draw.rectangle([30, 72, 98, 140], outline="#1e3a5f", width=2)

                draw.text((card_w // 2, 28), "STUDENT MANAGEMENT SYSTEM", fill="#1e3a5f", anchor="mm")
                draw.text((card_w // 2, 46), "STUDENT IDENTITY CARD", fill="#081579", anchor="mm")
                draw.line([(25, 58), (card_w - 25, 58)], fill="#048D9C", width=2)

                draw.text((110, 75), current_student[2], fill="#1e3a5f")
                draw.text((110, 96), f"ID: {current_student[0]}", fill="#081579")
                draw.text((110, 116), f"Year: {current_student[6]}", fill="#334155")

                draw.line([(25, 145), (card_w - 25, 145)], fill="#CBD5E1", width=1)

                cy = 160
                for lt, vt in details_list:
                    draw.text((30, cy), f"{lt}  {vt}", fill="#0F172A")
                    cy += 28

                draw.line([(25, 285), (card_w - 25, 285)], fill="#048D9C", width=1)
                draw.text((card_w // 2, 305), "Authorized Student Identity", fill="#64748B", anchor="mm")

                card_img.convert("RGB").save(path)
                show_popup("Student Card downloaded successfully!")
            except Exception as e:
                show_popup(f"Error saving card: {str(e)}", is_error=True)

        btn_bar = tk.Frame(content_fm, bg="#F8FAFC")
        btn_bar.pack(pady=10)

        save_btn = tk.Button(btn_bar, text="💾 Save Card as PNG", font=('Arial', 12, 'bold'), bg="#159BD7", fg="#FFFFFF", bd=0, command=handle_save_card)
        save_btn.pack(side="left", padx=10, ipady=6, ipadx=12)

        print_btn = tk.Button(btn_bar, text="🖨️ Print Card", font=('Arial', 12, 'bold'), bg="#217A5A", fg="#FFFFFF", bd=0, command=lambda: show_popup("Card ready! Please save as PNG to print."))
        print_btn.pack(side="left", padx=10, ipady=6, ipadx=12)

    # ==========================================
    # TAB 3: EDIT PROFILE (Part 11)
    # ==========================================
    def show_edit_profile_view():
        clear_content()
        set_active_button("edit")

        title = tk.Label(content_fm, text="Edit Profile Information", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=5, pady=5)

        # Selected Image state for editing
        edit_pic_data = [None]  # holds new binary pic if changed

        top_edit_bar = tk.Frame(card, bg="#FFFFFF")
        top_edit_bar.pack(fill="x", padx=25, pady=15)

        edit_avatar_canvas = tk.Canvas(top_edit_bar, width=80, height=80, bg="#FFFFFF", bd=0, highlightthickness=0)
        edit_avatar_canvas.pack(side="left", padx=(0, 15))

        def update_edit_avatar_preview(p_img):
            c_img = make_circular_image(p_img, size=(75, 75))
            tk_c = ImageTk.PhotoImage(c_img)
            card._preview_tk = tk_c
            edit_avatar_canvas.delete("all")
            edit_avatar_canvas.create_image(40, 40, image=tk_c)

        update_edit_avatar_preview(get_profile_pil())

        def handle_change_photo():
            from creat_account_page import pick_image_file
            path = pick_image_file(root)
            if path:
                try:
                    with Image.open(path) as raw_img:
                        resized = raw_img.convert("RGBA").resize((100, 100), Image.Resampling.LANCZOS)
                        buffer = io.BytesIO()
                        resized.save(buffer, format="PNG")
                        edit_pic_data[0] = buffer.getvalue()
                        update_edit_avatar_preview(resized)
                except Exception as e:
                    show_popup(f"Error loading image: {str(e)}", is_error=True)

        change_photo_btn = tk.Button(
            top_edit_bar,
            text="📷 Change Profile Photo",
            font=('Arial', 10, 'bold'),
            bg="#2563EB",
            fg="#FFFFFF",
            bd=0,
            command=handle_change_photo,
        )
        change_photo_btn.pack(side="left", padx=10, ipady=4, ipadx=8)

        # Inputs Form
        form_fm = tk.Frame(card, bg="#FFFFFF")
        form_fm.pack(fill="both", expand=True, padx=25, pady=5)

        # Full Name
        tk.Label(form_fm, text="Full Name:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=0, column=0, sticky="w", pady=6)
        name_ent = tk.Entry(form_fm, font=('Arial', 11), width=35)
        name_ent.insert(0, current_student[2])
        name_ent.grid(row=0, column=1, sticky="w", padx=10, pady=6)

        # Age
        tk.Label(form_fm, text="Age:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=1, column=0, sticky="w", pady=6)
        age_ent = tk.Entry(form_fm, font=('Arial', 11), width=35)
        age_ent.insert(0, current_student[3])
        age_ent.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        # Gender
        tk.Label(form_fm, text="Gender:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=2, column=0, sticky="w", pady=6)
        gender_var = tk.StringVar(value=current_student[4])
        gender_combo = ttk.Combobox(form_fm, textvariable=gender_var, values=["Male", "Female", "Other"], state="readonly", font=('Arial', 10), width=33)
        gender_combo.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        # Phone
        tk.Label(form_fm, text="Contact No:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=3, column=0, sticky="w", pady=6)
        phone_ent = tk.Entry(form_fm, font=('Arial', 11), width=35)
        phone_ent.insert(0, current_student[5])
        phone_ent.grid(row=3, column=1, sticky="w", padx=10, pady=6)

        # Class Year
        tk.Label(form_fm, text="Year / Class:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=4, column=0, sticky="w", pady=6)
        class_var = tk.StringVar(value=current_student[6])
        class_combo = ttk.Combobox(form_fm, textvariable=class_var, values=["1st year", "2nd year", "3rd year", "4th year"], state="readonly", font=('Arial', 10), width=33)
        class_combo.grid(row=4, column=1, sticky="w", padx=10, pady=6)

        # Email
        tk.Label(form_fm, text="Email Address:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=5, column=0, sticky="w", pady=6)
        email_ent = tk.Entry(form_fm, font=('Arial', 11), width=35)
        email_ent.insert(0, current_student[7])
        email_ent.grid(row=5, column=1, sticky="w", padx=10, pady=6)

        def handle_save_profile():
            n = name_ent.get().strip()
            a = age_ent.get().strip()
            g = gender_var.get().strip()
            p = phone_ent.get().strip()
            c = class_var.get().strip()
            e = email_ent.get().strip()

            if not n or not a or not p or not c or not e:
                show_popup("Please fill in all profile fields", is_error=True)
                return

            try:
                update_student(
                    id_number=current_student[0],
                    name=n,
                    age=a,
                    gender=g,
                    phone_number=p,
                    student_class=c,
                    email=e,
                    pic_data=edit_pic_data[0]
                )
                # Refresh local state
                current_student[2] = n
                current_student[3] = a
                current_student[4] = g
                current_student[5] = p
                current_student[6] = c
                current_student[7] = e
                if edit_pic_data[0]:
                    current_student[8] = edit_pic_data[0]

                refresh_sidebar_avatar()
                show_popup("Profile updated successfully!")
            except Exception as err:
                show_popup(f"Failed to update profile: {str(err)}", is_error=True)

        save_btn = tk.Button(
            card,
            text="💾 Save Changes",
            font=('Arial', 12, 'bold'),
            bg="#16A34A",
            fg="#FFFFFF",
            bd=0,
            command=handle_save_profile,
        )
        save_btn.pack(pady=15, ipady=5, ipadx=15)

    # ==========================================
    # TAB 4: CHANGE PASSWORD (Part 11)
    # ==========================================
    def show_change_password_view():
        clear_content()
        set_active_button("password")

        title = tk.Label(content_fm, text="Security & Password Management", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 15))

        card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        card.pack(fill="both", expand=True, padx=5, pady=5)

        form = tk.Frame(card, bg="#FFFFFF")
        form.pack(padx=30, pady=30)

        # Current Password
        tk.Label(form, text="Current Password:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=0, column=0, sticky="w", pady=10)
        curr_pwd_ent = tk.Entry(form, font=('Arial', 12), show='*', width=25)
        curr_pwd_ent.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # New Password
        tk.Label(form, text="New Password:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=1, column=0, sticky="w", pady=10)
        new_pwd_ent = tk.Entry(form, font=('Arial', 12), show='*', width=25)
        new_pwd_ent.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        # Confirm Password
        tk.Label(form, text="Confirm New Password:", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#334155").grid(row=2, column=0, sticky="w", pady=10)
        conf_pwd_ent = tk.Entry(form, font=('Arial', 12), show='*', width=25)
        conf_pwd_ent.grid(row=2, column=1, sticky="w", padx=10, pady=10)

        # Show/Hide Toggle
        def toggle_pwds():
            s = '' if curr_pwd_ent['show'] == '*' else '*'
            curr_pwd_ent.config(show=s)
            new_pwd_ent.config(show=s)
            conf_pwd_ent.config(show=s)

        eye_btn = tk.Button(form, text="👁️ Toggle Password Visibility", font=('Arial', 10), bg="#E2E8F0", bd=0, command=toggle_pwds)
        eye_btn.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        def handle_pwd_update():
            c_p = curr_pwd_ent.get().strip()
            n_p = new_pwd_ent.get().strip()
            cf_p = conf_pwd_ent.get().strip()

            if not c_p or not n_p or not cf_p:
                show_popup("Please fill out all password fields", is_error=True)
                return

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
            font=('Arial', 12, 'bold'),
            bg="#2563EB",
            fg="#FFFFFF",
            bd=0,
            command=handle_pwd_update,
        )
        up_btn.pack(pady=10, ipady=5, ipadx=15)

    # ==========================================
    # TAB 5: ANNOUNCEMENTS VIEW (Part 13B)
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
            padx=20,
            command=cmd,
        )
        btn.pack(fill="x", pady=2, ipady=6)
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
        padx=20,
        command=handle_logout,
    )
    logout_btn.pack(side="bottom", fill="x", pady=20, ipady=6)

    # Initial View
    show_profile_view()
