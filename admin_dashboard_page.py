"""
Student Management System - Admin Dashboard
Comprehensive administrative control panel matching Tkinter Hub Parts 12, 13A, and 13B:
- Dashboard Metrics (Total Students & Counts by Year)
- Find & Manage Students (Search, Live Treeview table, Photo Preview)
- Edit & Delete Student records
- View / Generate & Print Student ID Cards from Admin Panel
- Broadcast Announcements to All Students or Specific Classes
- Logout
"""
import os
import io
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk

from database import (
    get_all_students,
    search_students,
    get_student_by_id,
    get_student_counts,
    update_student,
    delete_student,
    add_announcement,
    get_announcements
)

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def start_admin_dashboard_page(root):
    """
    Renders the Administrator Dashboard.
    """
    # Expand window for table and sidebar
    root.geometry("1020x660")
    root.title("Student Management System - Administrator Dashboard")

    # Load UI Icons
    admin_icon = tk.PhotoImage(file=os.path.join(IMAGES_DIR, 'admin_img.png'))
    root._admin_icon = admin_icon

    # Top Header Bar
    header_fm = tk.Frame(root, bg="#070B6F", height=55)
    header_fm.pack(fill="x", side="top")
    header_fm.pack_propagate(False)

    tk.Label(
        header_fm,
        text="🛡️ Administrator Dashboard - Student Management System",
        font=('Arial', 15, 'bold'),
        bg="#070B6F",
        fg="#FFFFFF",
    ).pack(side="left", padx=20, pady=12)

    tk.Label(
        header_fm,
        text="Role: System Admin  |  Status: Online 🟢",
        font=('Arial', 11, 'bold'),
        bg="#070B6F",
        fg="#93C5FD",
    ).pack(side="right", padx=20, pady=12)

    # Main Workspace Container
    body_fm = tk.Frame(root, bg="#F1F5F9")
    body_fm.pack(fill="both", expand=True)

    # Left Navigation Sidebar
    sidebar_fm = tk.Frame(body_fm, bg="#0F172A", width=220)
    sidebar_fm.pack(side="left", fill="y")
    sidebar_fm.pack_propagate(False)

    # Admin Badge
    tk.Label(
        sidebar_fm,
        image=admin_icon,
        bg="#0F172A",
        bd=0,
    ).pack(pady=(20, 5))

    tk.Label(
        sidebar_fm,
        text="Administrator",
        font=('Arial', 13, 'bold'),
        bg="#0F172A",
        fg="#FFFFFF",
    ).pack()

    tk.Label(
        sidebar_fm,
        text="Control Panel",
        font=('Arial', 9),
        bg="#0F172A",
        fg="#94A3B8",
    ).pack(pady=(0, 15))

    tk.Frame(sidebar_fm, bg="#334155", height=1).pack(fill="x", padx=15, pady=(0, 15))

    # Content Area (Right Side)
    content_fm = tk.Frame(body_fm, bg="#F8FAFC")
    content_fm.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    nav_buttons = {}

    def set_active_btn(key):
        for k, btn in nav_buttons.items():
            if k == key:
                btn.config(bg="#1E293B", fg="#38BDF8")
            else:
                btn.config(bg="#0F172A", fg="#E2E8F0")

    def clear_content():
        for widget in content_fm.winfo_children():
            widget.destroy()

    # ==========================================
    # TAB 1: DASHBOARD HOME & METRICS (Part 12)
    # ==========================================
    def show_metrics_view():
        clear_content()
        set_active_btn("home")

        counts = get_student_counts()
        total_count = counts["total"]
        class_counts = counts["classes"]

        title_row = tk.Frame(content_fm, bg="#F8FAFC")
        title_row.pack(fill="x", pady=(0, 15))
        tk.Label(title_row, text="System Overview & Enrollment Metrics", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(side="left")

        # Metric Cards Row
        cards_fm = tk.Frame(content_fm, bg="#F8FAFC")
        cards_fm.pack(fill="x", pady=10)

        # Card Template Helper
        def create_metric_card(parent, title_text, count_val, bg_color, fg_accent):
            card = tk.Frame(parent, bg="#FFFFFF", bd=1, relief="solid", highlightthickness=0, width=140, height=110)
            card.pack_propagate(False)

            strip = tk.Frame(card, bg=fg_accent, height=4)
            strip.pack(fill="x", side="top")

            tk.Label(card, text=title_text, font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#64748B").pack(pady=(12, 4))
            tk.Label(card, text=str(count_val), font=('Arial', 24, 'bold'), bg="#FFFFFF", fg=fg_accent).pack()
            return card

        # Total Students Metric Card (Bigger)
        total_card = tk.Frame(cards_fm, bg="#FFFFFF", bd=1, relief="solid", width=180, height=110)
        total_card.pack_propagate(False)
        total_card.pack(side="left", padx=8)
        tk.Frame(total_card, bg="#2563EB", height=4).pack(fill="x", side="top")
        tk.Label(total_card, text="TOTAL STUDENTS", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#64748B").pack(pady=(12, 4))
        tk.Label(total_card, text=str(total_count), font=('Arial', 26, 'bold'), bg="#FFFFFF", fg="#2563EB").pack()

        # Breakdown by Class Year Cards
        colors = [
            ("1st Year", class_counts.get("1st year", 0), "#16A34A"),
            ("2nd Year", class_counts.get("2nd year", 0), "#9333EA"),
            ("3rd Year", class_counts.get("3rd year", 0), "#EA580C"),
            ("4th Year", class_counts.get("4th year", 0), "#0891B2"),
        ]

        for year_name, count_v, accent in colors:
            c = create_metric_card(cards_fm, f"{year_name}", count_v, "#FFFFFF", accent)
            c.pack(side="left", padx=8)

        # Quick Actions & Summary Box
        info_card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        info_card.pack(fill="both", expand=True, pady=15)

        tk.Label(info_card, text="Quick Management Tools", font=('Arial', 13, 'bold'), bg="#FFFFFF", fg="#0F172A").pack(anchor="w", padx=20, pady=(15, 10))
        tk.Frame(info_card, bg="#E2E8F0", height=1).pack(fill="x", padx=20, pady=(0, 15))

        btn_grid = tk.Frame(info_card, bg="#FFFFFF")
        btn_grid.pack(anchor="w", padx=20, pady=5)

        tk.Button(
            btn_grid,
            text="📋 Find & Manage Students",
            font=('Arial', 11, 'bold'),
            bg="#1E3A5F",
            fg="#FFFFFF",
            bd=0,
            command=show_students_table_view,
        ).grid(row=0, column=0, padx=8, pady=8, ipady=8, ipadx=14)

        tk.Button(
            btn_grid,
            text="📢 Publish College Notice",
            font=('Arial', 11, 'bold'),
            bg="#2563EB",
            fg="#FFFFFF",
            bd=0,
            command=show_announcements_view,
        ).grid(row=0, column=1, padx=8, pady=8, ipady=8, ipadx=14)

        def handle_admin_add_student():
            header_fm.destroy()
            body_fm.destroy()
            root.geometry("500x600")
            root.update()
            from creat_account_page import start_creat_account_page
            start_creat_account_page(root)

        tk.Button(
            btn_grid,
            text="➕ Register New Student",
            font=('Arial', 11, 'bold'),
            bg="#16A34A",
            fg="#FFFFFF",
            bd=0,
            command=handle_admin_add_student,
        ).grid(row=0, column=2, padx=8, pady=8, ipady=8, ipadx=14)

        # Status text
        tk.Label(
            info_card,
            text="Database Status: SQLite3 (student_account.db) Active & Synchronized\nID Card Generation System: Operational",
            font=('Arial', 10),
            bg="#FFFFFF",
            fg="#64748B",
            justify="left",
        ).pack(anchor="w", padx=25, pady=25)

    # ==========================================
    # TAB 2: FIND & MANAGE STUDENTS (Part 13A)
    # ==========================================
    def show_students_table_view():
        clear_content()
        set_active_btn("students")

        top_search = tk.Frame(content_fm, bg="#F8FAFC")
        top_search.pack(fill="x", pady=(0, 10))

        tk.Label(top_search, text="Manage Students", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(side="left")

        # Search Controls
        search_box = tk.Frame(top_search, bg="#F8FAFC")
        search_box.pack(side="right")

        search_ent = tk.Entry(search_box, font=('Arial', 11), width=26)
        search_ent.pack(side="left", padx=6, ipady=4)

        def do_search():
            kw = search_ent.get().strip()
            if kw:
                results = search_students(kw)
            else:
                results = get_all_students()
            load_tree_data(results)

        search_btn = tk.Button(search_box, text="🔍 Search", font=('Arial', 10, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0, command=do_search)
        search_btn.pack(side="left", padx=4, ipady=3, ipadx=8)

        reset_btn = tk.Button(search_box, text="🔄 Reset", font=('Arial', 10), bg="#E2E8F0", fg="#0F172A", bd=0, command=lambda: [search_ent.delete(0, tk.END), load_tree_data(get_all_students())])
        reset_btn.pack(side="left", padx=4, ipady=3, ipadx=6)

        # Main Table + Preview Split Layout
        split_fm = tk.Frame(content_fm, bg="#F8FAFC")
        split_fm.pack(fill="both", expand=True)

        # Treeview Container
        tree_fm = tk.Frame(split_fm, bg="#FFFFFF", bd=1, relief="solid")
        tree_fm.pack(side="left", fill="both", expand=True)

        cols = ("id", "name", "class", "gender", "age", "phone", "email")
        tree = ttk.Treeview(tree_fm, columns=cols, show="headings", selectmode="browse")

        tree.heading("id", text="Student ID")
        tree.heading("name", text="Full Name")
        tree.heading("class", text="Class / Year")
        tree.heading("gender", text="Gender")
        tree.heading("age", text="Age")
        tree.heading("phone", text="Contact No")
        tree.heading("email", text="Email ID")

        tree.column("id", width=105, anchor="center")
        tree.column("name", width=130, anchor="w")
        tree.column("class", width=85, anchor="center")
        tree.column("gender", width=65, anchor="center")
        tree.column("age", width=45, anchor="center")
        tree.column("phone", width=100, anchor="center")
        tree.column("email", width=150, anchor="w")

        scroll_y = ttk.Scrollbar(tree_fm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        scroll_y.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

        # Side Preview Card (Selected Student Details & Photo)
        preview_fm = tk.Frame(split_fm, bg="#FFFFFF", bd=1, relief="solid", width=190)
        preview_fm.pack(side="right", fill="y", padx=(10, 0))
        preview_fm.pack_propagate(False)

        tk.Label(preview_fm, text="Student Preview", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#0F172A").pack(pady=(10, 5))

        preview_canvas = tk.Canvas(preview_fm, width=80, height=80, bg="#FFFFFF", bd=0, highlightthickness=0)
        preview_canvas.pack(pady=5)

        prev_name_lb = tk.Label(preview_fm, text="Select a student", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#1E3A5F", wraplength=170)
        prev_name_lb.pack()

        prev_id_lb = tk.Label(preview_fm, text="", font=('Arial', 9), bg="#FFFFFF", fg="#64748B")
        prev_id_lb.pack(pady=(0, 10))

        prev_details_lb = tk.Label(preview_fm, text="", font=('Arial', 9), bg="#FFFFFF", fg="#334155", justify="left", wraplength=170)
        prev_details_lb.pack(padx=8)

        # Store full records mapping by ID
        records_map = {}

        def load_tree_data(rows):
            tree.delete(*tree.get_children())
            records_map.clear()
            for r in rows:
                # r: id_number, name, age, gender, phone_number, class, email, image
                tree.insert("", "end", values=(r[0], r[1], r[5], r[3], r[2], r[4], r[6]))
                records_map[str(r[0])] = r

            if rows:
                tree.selection_set(tree.get_children()[0])
                on_select_row(None)

        def on_select_row(event):
            selected = tree.selection()
            if not selected:
                return
            vals = tree.item(selected[0], "values")
            s_id = str(vals[0])
            rec = records_map.get(s_id)
            if rec:
                prev_name_lb.config(text=rec[1])
                prev_id_lb.config(text=f"ID: {rec[0]}")
                prev_details_lb.config(text=f"Class: {rec[5]}\nAge: {rec[2]} | {rec[3]}\nPhone: {rec[4]}\nEmail: {rec[6]}")

                # Display student photo
                img_data = rec[7]
                pil_img = None
                if img_data:
                    try:
                        pil_img = Image.open(io.BytesIO(img_data)).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
                    except Exception:
                        pass
                if not pil_img:
                    d_path = os.path.join(IMAGES_DIR, 'add_student_img.png')
                    if os.path.exists(d_path):
                        pil_img = Image.open(d_path).convert("RGBA").resize((76, 76), Image.Resampling.LANCZOS)
                    else:
                        pil_img = Image.new("RGBA", (76, 76), color="#E2E8F0")

                tk_img = ImageTk.PhotoImage(pil_img)
                preview_fm._prev_img = tk_img
                preview_canvas.delete("all")
                preview_canvas.create_image(40, 40, image=tk_img)

        tree.bind("<<TreeviewSelect>>", on_select_row)

        # Action Buttons Row
        actions_bar = tk.Frame(content_fm, bg="#F8FAFC")
        actions_bar.pack(fill="x", pady=10)

        # Action 1: View / Generate Student Card
        def handle_view_card():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Notice", "Please select a student from the table first")
                return
            s_id = tree.item(sel[0], "values")[0]
            # Fetch complete tuple: (id, pwd, name, age, gender, phone, class, email, image)
            full_data = get_student_by_id(s_id)
            if full_data:
                # Open Student Card Page Window
                card_win = tk.Toplevel(root)
                card_win.title(f"Student Card - {full_data[2]}")
                card_win.geometry("500x600")
                card_win.resizable(False, False)
                card_win.configure(bg="#F8FAFC")
                from student_card_page import start_student_card_page
                start_student_card_page(card_win, full_data, prev_page='admin')

        # Action 2: Edit Student Details
        def handle_edit_student():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Notice", "Please select a student from the table first")
                return
            s_id = tree.item(sel[0], "values")[0]
            rec = records_map.get(s_id)
            if not rec:
                return

            edit_win = tk.Toplevel(root)
            edit_win.title(f"Edit Student - {rec[1]}")
            edit_win.geometry("420x450")
            edit_win.configure(bg="#F1F5F9")
            edit_win.transient(root)
            edit_win.grab_set()

            tk.Label(edit_win, text=f"Edit Student Details (ID: {rec[0]})", font=('Arial', 12, 'bold'), bg="#F1F5F9", fg="#0F172A").pack(pady=15)

            form = tk.Frame(edit_win, bg="#F1F5F9")
            form.pack(padx=20)

            tk.Label(form, text="Full Name:", font=('Arial', 10, 'bold'), bg="#F1F5F9").grid(row=0, column=0, sticky="w", pady=6)
            name_e = tk.Entry(form, font=('Arial', 10), width=28)
            name_e.insert(0, rec[1])
            name_e.grid(row=0, column=1, pady=6)

            tk.Label(form, text="Age:", font=('Arial', 10, 'bold'), bg="#F1F5F9").grid(row=1, column=0, sticky="w", pady=6)
            age_e = tk.Entry(form, font=('Arial', 10), width=28)
            age_e.insert(0, rec[2])
            age_e.grid(row=1, column=1, pady=6)

            tk.Label(form, text="Gender:", font=('Arial', 10, 'bold'), bg="#F1F5F9").grid(row=2, column=0, sticky="w", pady=6)
            gen_var = tk.StringVar(value=rec[3])
            gen_cb = ttk.Combobox(form, textvariable=gen_var, values=["Male", "Female", "Other"], state="readonly", width=26)
            gen_cb.grid(row=2, column=1, pady=6)

            tk.Label(form, text="Phone:", font=('Arial', 10, 'bold'), bg="#F1F5F9").grid(row=3, column=0, sticky="w", pady=6)
            phone_e = tk.Entry(form, font=('Arial', 10), width=28)
            phone_e.insert(0, rec[4])
            phone_e.grid(row=3, column=1, pady=6)

            tk.Label(form, text="Class / Year:", font=('Arial', 10, 'bold'), bg="#F1F5F9").grid(row=4, column=0, sticky="w", pady=6)
            cls_var = tk.StringVar(value=rec[5])
            cls_cb = ttk.Combobox(form, textvariable=cls_var, values=["1st year", "2nd year", "3rd year", "4th year"], state="readonly", width=26)
            cls_cb.grid(row=4, column=1, pady=6)

            tk.Label(form, text="Email:", font=('Arial', 10, 'bold'), bg="#F1F5F9").grid(row=5, column=0, sticky="w", pady=6)
            email_e = tk.Entry(form, font=('Arial', 10), width=28)
            email_e.insert(0, rec[6])
            email_e.grid(row=5, column=1, pady=6)

            def save_admin_edit():
                n_v = name_e.get().strip()
                a_v = age_e.get().strip()
                g_v = gen_var.get().strip()
                p_v = phone_e.get().strip()
                c_v = cls_var.get().strip()
                e_v = email_e.get().strip()

                if not n_v or not a_v or not p_v or not c_v or not e_v:
                    messagebox.showwarning("Notice", "Please fill in all fields")
                    return

                try:
                    update_student(
                        id_number=rec[0],
                        name=n_v,
                        age=a_v,
                        gender=g_v,
                        phone_number=p_v,
                        student_class=c_v,
                        email=e_v
                    )
                    messagebox.showinfo("Success", "Student details updated successfully!")
                    edit_win.destroy()
                    load_tree_data(get_all_students())
                except Exception as err:
                    messagebox.showerror("Error", f"Could not update student: {err}")

            tk.Button(edit_win, text="Save Updates", font=('Arial', 11, 'bold'), bg="#16A34A", fg="#FFFFFF", bd=0, command=save_admin_edit).pack(pady=20, ipadx=10, ipady=4)

        # Action 3: Delete Student
        def handle_delete_student():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Notice", "Please select a student from the table to delete")
                return
            s_id = tree.item(sel[0], "values")[0]
            s_name = tree.item(sel[0], "values")[1]

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete student:\n\n{s_name} (ID: {s_id})?\n\nThis action cannot be undone."
            )
            if confirm:
                try:
                    delete_student(s_id)
                    messagebox.showinfo("Success", "Student deleted successfully.")
                    load_tree_data(get_all_students())
                except Exception as err:
                    messagebox.showerror("Error", f"Failed to delete student: {err}")

        # Buttons Placement
        btn_view_card = tk.Button(actions_bar, text="🪪 View / Print ID Card", font=('Arial', 11, 'bold'), bg="#159BD7", fg="#FFFFFF", bd=0, command=handle_view_card)
        btn_view_card.pack(side="left", padx=6, ipady=6, ipadx=10)

        btn_edit = tk.Button(actions_bar, text="✏️ Edit Student", font=('Arial', 11, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0, command=handle_edit_student)
        btn_edit.pack(side="left", padx=6, ipady=6, ipadx=10)

        btn_delete = tk.Button(actions_bar, text="❌ Delete Student", font=('Arial', 11, 'bold'), bg="#DC2626", fg="#FFFFFF", bd=0, command=handle_delete_student)
        btn_delete.pack(side="left", padx=6, ipady=6, ipadx=10)

        btn_refresh = tk.Button(actions_bar, text="🔄 Refresh Table", font=('Arial', 11), bg="#E2E8F0", fg="#0F172A", bd=0, command=lambda: load_tree_data(get_all_students()))
        btn_refresh.pack(side="left", padx=6, ipady=6, ipadx=10)

        # Initial Load
        load_tree_data(get_all_students())

    # ==========================================
    # TAB 3: ANNOUNCEMENTS (Part 13B)
    # ==========================================
    def show_announcements_view():
        clear_content()
        set_active_btn("announcements")

        title = tk.Label(content_fm, text="College Announcements & Notifications", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A")
        title.pack(anchor="w", pady=(0, 10))

        # Compose Announcement Form Card
        compose_card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        compose_card.pack(fill="x", pady=(0, 15))

        tk.Label(compose_card, text="Compose New Notice / Announcement", font=('Arial', 12, 'bold'), bg="#FFFFFF", fg="#1E3A5F").pack(anchor="w", padx=15, pady=(12, 8))

        row1 = tk.Frame(compose_card, bg="#FFFFFF")
        row1.pack(fill="x", padx=15, pady=4)

        tk.Label(row1, text="Target Audience:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").pack(side="left", padx=(0, 10))
        target_var = tk.StringVar(value="All Students")
        target_cb = ttk.Combobox(row1, textvariable=target_var, values=["All Students", "1st year", "2nd year", "3rd year", "4th year"], state="readonly", width=18)
        target_cb.pack(side="left")

        row2 = tk.Frame(compose_card, bg="#FFFFFF")
        row2.pack(fill="x", padx=15, pady=6)

        tk.Label(row2, text="Notice Title:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").pack(side="left", padx=(0, 36))
        title_ent = tk.Entry(row2, font=('Arial', 10), width=45)
        title_ent.pack(side="left")

        row3 = tk.Frame(compose_card, bg="#FFFFFF")
        row3.pack(fill="x", padx=15, pady=6)

        tk.Label(row3, text="Message Body:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").pack(anchor="nw", pady=(0, 4))
        msg_text = tk.Text(row3, font=('Arial', 10), height=4, width=70)
        msg_text.pack(fill="x")

        def handle_post_notice():
            t_aud = target_var.get().strip()
            t_title = title_ent.get().strip()
            t_msg = msg_text.get("1.0", tk.END).strip()

            if not t_title or not t_msg:
                messagebox.showwarning("Notice", "Please enter both notice title and message body")
                return

            date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            try:
                add_announcement(t_title, t_aud, t_msg, date_str)
                messagebox.showinfo("Published", f"Announcement published successfully for '{t_aud}'!")
                title_ent.delete(0, tk.END)
                msg_text.delete("1.0", tk.END)
                show_announcements_view()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to publish announcement: {e}")

        tk.Button(compose_card, text="📢 Publish Notice", font=('Arial', 11, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0, command=handle_post_notice).pack(anchor="e", padx=15, pady=(4, 12), ipady=4, ipadx=12)

        # Published Notices Feed
        tk.Label(content_fm, text="Recent Published Notices", font=('Arial', 12, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(anchor="w", pady=(5, 5))

        feed_wrap = tk.Frame(content_fm, bg="#F8FAFC")
        feed_wrap.pack(fill="both", expand=True)

        notices = get_announcements(target_class='All Students')
        if not notices:
            tk.Label(feed_wrap, text="No announcements published yet.", font=('Arial', 10, 'italic'), bg="#F8FAFC", fg="#64748B").pack(pady=10)
        else:
            for n_t, n_aud, n_msg, n_d in notices[:5]:
                box = tk.Frame(feed_wrap, bg="#FFFFFF", bd=1, relief="solid")
                box.pack(fill="x", pady=4)

                top_l = tk.Frame(box, bg="#FFFFFF")
                top_l.pack(fill="x", padx=10, pady=(6, 2))
                tk.Label(top_l, text=f"📢 {n_t}", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#1E3A5F").pack(side="left")
                tk.Label(top_l, text=f"Target: {n_aud}  |  {n_d}", font=('Arial', 8), bg="#FFFFFF", fg="#64748B").pack(side="right")

                tk.Label(box, text=n_msg, font=('Arial', 9), bg="#FFFFFF", fg="#334155", wraplength=700, justify="left").pack(anchor="w", padx=10, pady=(0, 6))

    # ==========================================
    # LOGOUT (Returns to Welcome Page)
    # ==========================================
    def handle_admin_logout():
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to log out of the Admin Panel?")
        if confirm:
            header_fm.destroy()
            body_fm.destroy()
            root.geometry("500x600")
            root.update()
            from welcome_page import start_welcome_page
            start_welcome_page(root)

    # Sidebar Navigation Buttons
    nav_items = [
        ("home", "📊  Dashboard Home", show_metrics_view),
        ("students", "📋  Manage Students", show_students_table_view),
        ("announcements", "📢  Announcements", show_announcements_view),
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
        btn.pack(fill="x", pady=2, ipady=8)
        nav_buttons[key] = btn

    # Logout Button at bottom
    logout_btn = tk.Button(
        sidebar_fm,
        text="🚪  Admin Logout",
        font=('Arial', 11, 'bold'),
        bg="#880B14",
        fg="#FFFFFF",
        activebackground="#66080E",
        activeforeground="#FFFFFF",
        bd=0,
        anchor="w",
        padx=20,
        command=handle_admin_logout,
    )
    logout_btn.pack(side="bottom", fill="x", pady=20, ipady=8)

    # Launch initial view
    show_metrics_view()
