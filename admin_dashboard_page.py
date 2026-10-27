"""
Student Management System - Admin Dashboard #humanrised
Comprehensive administrative control panel matching Tkinter Hub Parts 12, 13A, 13B,
with extended modules for:
- Dashboard Metrics (Total Students & Counts by Year)
- Student Directory (Search, Live Treeview table, Photo Preview, Edit, Delete, View ID Card)
- Attendance Management (Mark daily attendance, Mark All Present, Save, Export)
- Examination Marks & Results (Input marks, Grade calculation, View & Download Official Report Card)
- Excel Data Hub (Export Students, Attendance, Results to Excel & Bulk Import from Excel/CSV)
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
    get_announcements,
    mark_attendance,
    get_attendance_for_date_and_class,
    save_or_update_marks,
    get_marks_by_exam_and_class,
    delete_marks_record,
    calculate_grade
)
import excel_manager
from report_card_generator import preview_report_card_window

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def start_admin_dashboard_page(root):
    """
    Renders the Administrator Dashboard.
    """
    # Expand window for table, attendance, and sidebar
    root.geometry("1060x680")
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
    sidebar_fm = tk.Frame(body_fm, bg="#0F172A", width=225)
    sidebar_fm.pack(side="left", fill="y")
    sidebar_fm.pack_propagate(False)

    # Admin Badge
    tk.Label(
        sidebar_fm,
        image=admin_icon,
        bg="#0F172A",
        bd=0,
    ).pack(pady=(16, 4))

    tk.Label(
        sidebar_fm,
        text="Administrator",
        font=('Arial', 12, 'bold'),
        bg="#0F172A",
        fg="#FFFFFF",
    ).pack()

    tk.Label(
        sidebar_fm,
        text="Control Panel",
        font=('Arial', 9),
        bg="#0F172A",
        fg="#94A3B8",
    ).pack(pady=(0, 10))

    tk.Frame(sidebar_fm, bg="#334155", height=1).pack(fill="x", padx=15, pady=(0, 8))

    # Content Area (Right Side)
    content_fm = tk.Frame(body_fm, bg="#F8FAFC")
    content_fm.pack(side="right", fill="both", expand=True, padx=12, pady=12)

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

        def create_metric_card(parent, title_text, count_val, fg_accent):
            card = tk.Frame(parent, bg="#FFFFFF", bd=1, relief="solid", highlightthickness=0, width=145, height=105)
            card.pack_propagate(False)
            tk.Frame(card, bg=fg_accent, height=4).pack(fill="x", side="top")
            tk.Label(card, text=title_text, font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#64748B").pack(pady=(10, 4))
            tk.Label(card, text=str(count_val), font=('Arial', 24, 'bold'), bg="#FFFFFF", fg=fg_accent).pack()
            return card

        # Total Students Metric Card
        total_card = tk.Frame(cards_fm, bg="#FFFFFF", bd=1, relief="solid", width=180, height=105)
        total_card.pack_propagate(False)
        total_card.pack(side="left", padx=6)
        tk.Frame(total_card, bg="#2563EB", height=4).pack(fill="x", side="top")
        tk.Label(total_card, text="TOTAL STUDENTS", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#64748B").pack(pady=(10, 4))
        tk.Label(total_card, text=str(total_count), font=('Arial', 26, 'bold'), bg="#FFFFFF", fg="#2563EB").pack()

        colors = [
            ("1st Year", class_counts.get("1st year", 0), "#16A34A"),
            ("2nd Year", class_counts.get("2nd year", 0), "#9333EA"),
            ("3rd Year", class_counts.get("3rd year", 0), "#EA580C"),
            ("4th Year", class_counts.get("4th year", 0), "#0891B2"),
        ]

        for year_name, count_v, accent in colors:
            c = create_metric_card(cards_fm, year_name, count_v, accent)
            c.pack(side="left", padx=6)

        # Quick Actions Box
        info_card = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        info_card.pack(fill="both", expand=True, pady=15)

        tk.Label(info_card, text="Quick Management Tools", font=('Arial', 13, 'bold'), bg="#FFFFFF", fg="#0F172A").pack(anchor="w", padx=20, pady=(15, 10))
        tk.Frame(info_card, bg="#E2E8F0", height=1).pack(fill="x", padx=20, pady=(0, 15))

        btn_grid = tk.Frame(info_card, bg="#FFFFFF")
        btn_grid.pack(anchor="w", padx=20, pady=5)

        tk.Button(btn_grid, text="📋 Manage Students", font=('Arial', 11, 'bold'), bg="#1E3A5F", fg="#FFFFFF", bd=0,
                  command=show_students_table_view).grid(row=0, column=0, padx=8, pady=8, ipady=8, ipadx=14)

        tk.Button(btn_grid, text="📅 Mark Attendance", font=('Arial', 11, 'bold'), bg="#0284C7", fg="#FFFFFF", bd=0,
                  command=show_attendance_view).grid(row=0, column=1, padx=8, pady=8, ipady=8, ipadx=14)

        tk.Button(btn_grid, text="📝 Exams & Marksheets", font=('Arial', 11, 'bold'), bg="#16A34A", fg="#FFFFFF", bd=0,
                  command=show_marks_view).grid(row=0, column=2, padx=8, pady=8, ipady=8, ipadx=14)

        tk.Button(btn_grid, text="📊 Excel Hub & Import", font=('Arial', 11, 'bold'), bg="#D97706", fg="#FFFFFF", bd=0,
                  command=show_excel_center_view).grid(row=0, column=3, padx=8, pady=8, ipady=8, ipadx=14)

    # ==========================================
    # TAB 2: MANAGE STUDENTS TABLE (Part 13A)
    # ==========================================
    def show_students_table_view():
        clear_content()
        set_active_btn("students")

        top_bar = tk.Frame(content_fm, bg="#F8FAFC")
        top_bar.pack(fill="x", pady=(0, 10))

        tk.Label(top_bar, text="Student Directory & Management", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(side="left")

        search_bar = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        search_bar.pack(fill="x", pady=(0, 10), ipady=6, ipadx=10)

        tk.Label(search_bar, text="🔍 Search:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").pack(side="left", padx=(10, 5))
        search_ent = tk.Entry(search_bar, font=('Arial', 10), width=28)
        search_ent.pack(side="left", padx=5)

        def handle_search(*args):
            query = search_ent.get().strip()
            if not query:
                load_tree_data(get_all_students())
            else:
                load_tree_data(search_students(query))

        search_ent.bind("<KeyRelease>", handle_search)

        tk.Button(search_bar, text="Search", font=('Arial', 9, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0,
                  command=handle_search).pack(side="left", padx=5, ipadx=10)

        tk.Button(search_bar, text="Reset", font=('Arial', 9), bg="#94A3B8", fg="#FFFFFF", bd=0,
                  command=lambda: (search_ent.delete(0, tk.END), load_tree_data(get_all_students()))).pack(side="left", padx=5, ipadx=8)

        # Split Container: Treeview (Left) + Selected Preview (Right)
        split_fm = tk.Frame(content_fm, bg="#F8FAFC")
        split_fm.pack(fill="both", expand=True)

        tree_frame = tk.Frame(split_fm, bg="#FFFFFF", bd=1, relief="solid")
        tree_frame.pack(side="left", fill="both", expand=True)

        cols = ("id", "name", "class", "gender", "phone", "email")
        tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")

        tree.heading("id", text="Student ID")
        tree.heading("name", text="Full Name")
        tree.heading("class", text="Class / Year")
        tree.heading("gender", text="Gender")
        tree.heading("phone", text="Phone")
        tree.heading("email", text="Email")

        tree.column("id", width=95, anchor="center")
        tree.column("name", width=130, anchor="w")
        tree.column("class", width=85, anchor="center")
        tree.column("gender", width=70, anchor="center")
        tree.column("phone", width=95, anchor="center")
        tree.column("email", width=140, anchor="w")

        v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=v_scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        v_scroll.pack(side="right", fill="y")

        # Preview Panel on Right
        preview_fm = tk.Frame(split_fm, bg="#FFFFFF", bd=1, relief="solid", width=220)
        preview_fm.pack(side="right", fill="y", padx=(10, 0))
        preview_fm.pack_propagate(False)

        tk.Label(preview_fm, text="Student Details", font=('Arial', 11, 'bold'), bg="#FFFFFF", fg="#1E293B").pack(pady=(12, 6))
        tk.Frame(preview_fm, bg="#E2E8F0", height=1).pack(fill="x", padx=10, pady=(0, 10))

        avatar_lbl = tk.Label(preview_fm, bg="#FFFFFF", bd=0)
        avatar_lbl.pack(pady=5)

        detail_lbl = tk.Label(preview_fm, text="Select a student to\nview full profile", font=('Arial', 9), bg="#FFFFFF", fg="#64748B", justify="center")
        detail_lbl.pack(pady=8, padx=10)

        # Action Buttons under preview
        btn_box = tk.Frame(preview_fm, bg="#FFFFFF")
        btn_box.pack(side="bottom", fill="x", pady=15, padx=10)

        selected_student = [None]

        def on_tree_select(event):
            sel = tree.selection()
            if not sel:
                return
            item = tree.item(sel[0])
            s_id = item["values"][0]
            st = get_student_by_id(s_id)
            if not st:
                return
            selected_student[0] = st

            # Render Photo
            if st[8]:
                try:
                    pil_img = Image.open(io.BytesIO(st[8])).convert("RGBA").resize((75, 75), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(pil_img)
                    avatar_lbl.config(image=tk_img)
                    avatar_lbl.image = tk_img
                except Exception:
                    avatar_lbl.config(image="", text="👤")
            else:
                avatar_lbl.config(image="", text="👤")

            txt = f"Name: {st[2]}\nID: {st[0]}\nClass: {st[6]}\nAge: {st[3]} | Gender: {st[4]}\nPhone: {st[5]}\nEmail: {st[7]}"
            detail_lbl.config(text=txt, justify="left", fg="#1E293B", font=('Arial', 9))

        tree.bind("<<TreeviewSelect>>", on_tree_select)

        def load_tree_data(students):
            for r in tree.get_children():
                tree.delete(r)
            for s in students:
                tree.insert("", "end", values=(s[0], s[1], s[5], s[3], s[4], s[6]))

        # View ID Card Button
        def handle_view_card():
            if not selected_student[0]:
                messagebox.showwarning("Selection Required", "Please select a student from the table.")
                return
            st = selected_student[0]
            from student_card_page import draw_student_card
            img = Image.open(io.BytesIO(st[8])).convert("RGBA") if st[8] else None
            card = draw_student_card(st[2], st[6], st[3], st[0], img)

            w = tk.Toplevel(root)
            w.title(f"Student ID Card - {st[2]}")
            w.geometry("540x360")
            w.resizable(False, False)
            scaled = card.resize((500, 310), Image.Resampling.LANCZOS)
            tk_c = ImageTk.PhotoImage(scaled)
            l = tk.Label(w, image=tk_c)
            l.image = tk_c
            l.pack(pady=20)

        tk.Button(btn_box, text="🪪 View ID Card", font=('Arial', 9, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0,
                  command=handle_view_card).pack(fill="x", pady=2, ipady=4)

        # Delete Student Button
        def handle_delete_student():
            if not selected_student[0]:
                messagebox.showwarning("Selection Required", "Please select a student from the table.")
                return
            st = selected_student[0]
            confirm = messagebox.askyesno("Confirm Delete", f"Permanently delete student '{st[2]}' (ID: {st[0]})?")
            if confirm:
                delete_student(st[0])
                messagebox.showinfo("Deleted", "Student record deleted successfully.")
                selected_student[0] = None
                avatar_lbl.config(image="", text="")
                detail_lbl.config(text="Select a student to view details")
                load_tree_data(get_all_students())

        tk.Button(btn_box, text="🗑️ Delete Student", font=('Arial', 9, 'bold'), bg="#DC2626", fg="#FFFFFF", bd=0,
                  command=handle_delete_student).pack(fill="x", pady=2, ipady=4)

        load_tree_data(get_all_students())

    # ==========================================
    # TAB 3: ATTENDANCE MANAGEMENT (NEW! #humanrised)
    # ==========================================
    def show_attendance_view():
        clear_content()
        set_active_btn("attendance")

        title_row = tk.Frame(content_fm, bg="#F8FAFC")
        title_row.pack(fill="x", pady=(0, 10))
        tk.Label(title_row, text="Attendance Management System", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(side="left")

        # Control & Filter Bar
        ctrl_bar = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        ctrl_bar.pack(fill="x", pady=(0, 10), ipady=6, ipadx=10)

        # Date Selector (defaults to today)
        tk.Label(ctrl_bar, text="Date (YYYY-MM-DD):", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").pack(side="left", padx=(10, 4))
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        date_ent = tk.Entry(ctrl_bar, font=('Arial', 10), width=12)
        date_ent.insert(0, today_str)
        date_ent.pack(side="left", padx=5)

        # Class Selector
        tk.Label(ctrl_bar, text="Class:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").pack(side="left", padx=(15, 4))
        class_var = tk.StringVar(value="All Classes")
        class_cb = ttk.Combobox(ctrl_bar, textvariable=class_var, values=["All Classes", "1st year", "2nd year", "3rd year", "4th year"], state="readonly", width=14)
        class_cb.pack(side="left", padx=5)

        # Table Container
        tbl_fm = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        tbl_fm.pack(fill="both", expand=True)

        cols = ("id", "name", "class", "status")
        tree = ttk.Treeview(tbl_fm, columns=cols, show="headings", height=12)
        tree.heading("id", text="Student ID")
        tree.heading("name", text="Student Name")
        tree.heading("class", text="Class / Year")
        tree.heading("status", text="Current Status")

        tree.column("id", width=120, anchor="center")
        tree.column("name", width=200, anchor="w")
        tree.column("class", width=130, anchor="center")
        tree.column("status", width=150, anchor="center")

        scr = ttk.Scrollbar(tbl_fm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scr.set)
        tree.pack(side="left", fill="both", expand=True)
        scr.pack(side="right", fill="y")

        # Map to hold in-memory status for current date: {student_id: status}
        student_status_map = {}

        def refresh_attendance_table():
            student_status_map.clear()
            for r in tree.get_children():
                tree.delete(r)

            d_str = date_ent.get().strip()
            c_str = class_var.get().strip()
            records = get_attendance_for_date_and_class(d_str, c_str)

            for sid, sname, sclass, stat in records:
                # Default to 'Present' if not yet marked
                actual_stat = stat if stat != 'Not Marked' else 'Present'
                student_status_map[sid] = (sclass, actual_stat)
                tree.insert("", "end", iid=sid, values=(sid, sname, sclass, actual_stat))

        def load_btn_click():
            refresh_attendance_table()

        tk.Button(ctrl_bar, text="🔄 Load / Filter", font=('Arial', 9, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0,
                  command=load_btn_click).pack(side="left", padx=8, ipadx=8)

        # Quick Mark Buttons on ctrl bar
        def mark_all_present():
            for sid in student_status_map:
                sclass, _ = student_status_map[sid]
                student_status_map[sid] = (sclass, "Present")
                item = tree.item(sid)
                tree.item(sid, values=(item["values"][0], item["values"][1], item["values"][2], "Present"))

        tk.Button(ctrl_bar, text="✅ Mark All Present", font=('Arial', 9, 'bold'), bg="#16A34A", fg="#FFFFFF", bd=0,
                  command=mark_all_present).pack(side="left", padx=8, ipadx=8)

        # Toggle individual student attendance status by double clicking row
        def on_row_double_click(event):
            sel = tree.selection()
            if not sel:
                return
            sid = sel[0]
            item = tree.item(sid)
            curr = item["values"][3]
            nxt = "Absent" if curr == "Present" else ("Leave" if curr == "Absent" else "Present")
            sclass, _ = student_status_map[sid]
            student_status_map[sid] = (sclass, nxt)
            tree.item(sid, values=(item["values"][0], item["values"][1], item["values"][2], nxt))

        tree.bind("<Double-1>", on_row_double_click)

        # Bottom Bar: Save & Export
        btm_bar = tk.Frame(content_fm, bg="#F8FAFC")
        btm_bar.pack(fill="x", pady=10)

        tk.Label(btm_bar, text="💡 Tip: Double-click any row to toggle between Present ➔ Absent ➔ Leave",
                 font=('Arial', 9, 'italic'), bg="#F8FAFC", fg="#64748B").pack(side="left")

        def handle_save_attendance():
            d_str = date_ent.get().strip()
            if not d_str:
                messagebox.showerror("Error", "Please specify a valid date.")
                return
            try:
                for sid, (sclass, stat) in student_status_map.items():
                    mark_attendance(sid, d_str, stat, sclass)
                messagebox.showinfo("Saved", f"Attendance for {len(student_status_map)} students saved successfully for {d_str}!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")

        def handle_export_attendance():
            d_str = date_ent.get().strip()
            c_str = class_var.get().strip()
            fpath = filedialog.asksaveasfilename(
                title="Export Attendance to Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel Workbook", "*.xlsx"), ("CSV File", "*.csv")],
                initialfile=f"Attendance_{d_str}_{c_str.replace(' ', '_')}.xlsx"
            )
            if fpath:
                try:
                    count = excel_manager.export_attendance_to_excel(d_str, c_str, fpath)
                    messagebox.showinfo("Export Successful", f"Exported {count} attendance records to:\n{fpath}")
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export attendance:\n{str(e)}")

        tk.Button(btm_bar, text="💾 Save Attendance to DB", font=('Arial', 10, 'bold'), bg="#16A34A", fg="#FFFFFF", bd=0,
                  command=handle_save_attendance).pack(side="right", padx=6, ipady=4, ipadx=12)

        tk.Button(btm_bar, text="📥 Export Attendance to Excel", font=('Arial', 10, 'bold'), bg="#0284C7", fg="#FFFFFF", bd=0,
                  command=handle_export_attendance).pack(side="right", padx=6, ipady=4, ipadx=12)

        refresh_attendance_table()

    # ==========================================
    # TAB 4: EXAM MARKS & RESULTS (NEW! #humanrised)
    # ==========================================
    def show_marks_view():
        clear_content()
        set_active_btn("marks")

        top_row = tk.Frame(content_fm, bg="#F8FAFC")
        top_row.pack(fill="x", pady=(0, 10))
        tk.Label(top_row, text="Examinations, Marks & Report Cards", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(side="left")

        # Action / Filter Bar
        bar = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        bar.pack(fill="x", pady=(0, 10), ipady=6, ipadx=10)

        tk.Label(bar, text="Filter Exam:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").pack(side="left", padx=(10, 4))
        exam_filter_var = tk.StringVar(value="All Exams")
        exam_filter_cb = ttk.Combobox(bar, textvariable=exam_filter_var, values=["All Exams", "Mid-Term Exam 2026", "Final Exam 2026", "Semester 1", "Semester 2"], state="readonly", width=18)
        exam_filter_cb.pack(side="left", padx=5)

        tk.Label(bar, text="Class:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").pack(side="left", padx=(10, 4))
        c_filter_var = tk.StringVar(value="All Classes")
        c_filter_cb = ttk.Combobox(bar, textvariable=c_filter_var, values=["All Classes", "1st year", "2nd year", "3rd year", "4th year"], state="readonly", width=12)
        c_filter_cb.pack(side="left", padx=5)

        # Marks Table
        tbl_fm = tk.Frame(content_fm, bg="#FFFFFF", bd=1, relief="solid")
        tbl_fm.pack(fill="both", expand=True)

        cols = ("mid", "sid", "name", "class", "exam", "total", "pct", "grade", "date")
        tree = ttk.Treeview(tbl_fm, columns=cols, show="headings", height=10)

        tree.heading("mid", text="ID")
        tree.heading("sid", text="Student ID")
        tree.heading("name", text="Full Name")
        tree.heading("class", text="Class / Year")
        tree.heading("exam", text="Exam Name")
        tree.heading("total", text="Total (500)")
        tree.heading("pct", text="Percentage")
        tree.heading("grade", text="Grade")
        tree.heading("date", text="Date")

        tree.column("mid", width=40, anchor="center")
        tree.column("sid", width=95, anchor="center")
        tree.column("name", width=140, anchor="w")
        tree.column("class", width=85, anchor="center")
        tree.column("exam", width=130, anchor="w")
        tree.column("total", width=85, anchor="center")
        tree.column("pct", width=85, anchor="center")
        tree.column("grade", width=65, anchor="center")
        tree.column("date", width=95, anchor="center")

        scr = ttk.Scrollbar(tbl_fm, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scr.set)
        tree.pack(side="left", fill="both", expand=True)
        scr.pack(side="right", fill="y")

        def load_marks_table():
            for r in tree.get_children():
                tree.delete(r)
            ex_val = exam_filter_var.get().strip()
            cl_val = c_filter_var.get().strip()
            records = get_marks_by_exam_and_class(ex_val, cl_val)
            for m_id, s_id, s_name, s_class, e_name, tot, pct, gr, dt in records:
                tree.insert("", "end", iid=m_id, values=(m_id, s_id, s_name, s_class, e_name, f"{tot:.1f}", f"{pct:.1f}%", gr, dt))

        exam_filter_cb.bind("<<ComboboxSelected>>", lambda e: load_marks_table())
        c_filter_cb.bind("<<ComboboxSelected>>", lambda e: load_marks_table())

        # Modal Dialog to Enter / Update Marks
        def open_add_marks_dialog():
            students = get_all_students()
            if not students:
                messagebox.showwarning("No Students", "No students available to assign marks.")
                return

            win = tk.Toplevel(root)
            win.title("Enter / Update Student Exam Marks")
            win.geometry("520x560")
            win.resizable(False, False)
            win.configure(bg="#F8FAFC")
            win.grab_set()

            tk.Label(win, text="Record Student Examination Marks", font=('Arial', 14, 'bold'), bg="#F8FAFC", fg="#1E3A5F").pack(pady=(15, 10))

            card = tk.Frame(win, bg="#FFFFFF", bd=1, relief="solid")
            card.pack(fill="both", expand=True, padx=20, pady=(0, 15))

            f_grid = tk.Frame(card, bg="#FFFFFF")
            f_grid.pack(padx=20, pady=15, fill="both")

            # Student Choice
            tk.Label(f_grid, text="Select Student:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=0, column=0, sticky="w", pady=6)
            s_choices = [f"{s[0]} - {s[1]} ({s[5]})" for s in students]
            s_var = tk.StringVar(value=s_choices[0])
            s_cb = ttk.Combobox(f_grid, textvariable=s_var, values=s_choices, state="readonly", width=30)
            s_cb.grid(row=0, column=1, sticky="w", pady=6)

            # Exam Title
            tk.Label(f_grid, text="Exam Name:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=1, column=0, sticky="w", pady=6)
            exam_name_var = tk.StringVar(value="Mid-Term Exam 2026")
            exam_cb = ttk.Combobox(f_grid, textvariable=exam_name_var, values=["Mid-Term Exam 2026", "Final Exam 2026", "Semester 1", "Semester 2", "Class Assessment"], width=28)
            exam_cb.grid(row=1, column=1, sticky="w", pady=6)

            # Exam Date
            tk.Label(f_grid, text="Exam Date:", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#475569").grid(row=2, column=0, sticky="w", pady=6)
            date_e = tk.Entry(f_grid, font=('Arial', 10), width=20)
            date_e.insert(0, datetime.date.today().strftime("%d-%b-%Y"))
            date_e.grid(row=2, column=1, sticky="w", pady=6)

            tk.Frame(f_grid, bg="#E2E8F0", height=1).grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)

            # 5 Subject Marks
            defaults = [
                ("Mathematics", "85"),
                ("Physics / Computer", "88"),
                ("Chemistry / Electronics", "82"),
                ("Programming Lab", "90"),
                ("English & Communication", "84"),
            ]
            s_entries = []
            m_entries = []

            for i, (def_s, def_m) in enumerate(defaults):
                r_idx = 4 + i
                s_ent = tk.Entry(f_grid, font=('Arial', 9), width=22)
                s_ent.insert(0, def_s)
                s_ent.grid(row=r_idx, column=0, sticky="w", pady=4, padx=(0, 10))

                m_ent = tk.Entry(f_grid, font=('Arial', 9), width=8, justify="center")
                m_ent.insert(0, def_m)
                m_ent.grid(row=r_idx, column=1, sticky="w", pady=4)

                s_entries.append(s_ent)
                m_entries.append(m_ent)

            def save_marks_action():
                chosen_str = s_var.get()
                sid = chosen_str.split(" - ")[0].strip()
                ex_name = exam_cb.get().strip()
                ex_dt = date_e.get().strip()

                if not ex_name:
                    messagebox.showerror("Error", "Please enter an Exam Name.", parent=win)
                    return

                try:
                    s_vals = [e.get().strip() for e in s_entries]
                    m_vals = [float(e.get().strip()) for e in m_entries]
                    for m in m_vals:
                        if m < 0 or m > 100:
                            messagebox.showerror("Invalid Marks", "Marks must be between 0 and 100.", parent=win)
                            return
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numeric marks for all subjects.", parent=win)
                    return

                try:
                    tot, pct, grd = save_or_update_marks(
                        student_id=sid,
                        exam_name=ex_name,
                        s1=s_vals[0], m1=m_vals[0],
                        s2=s_vals[1], m2=m_vals[1],
                        s3=s_vals[2], m3=m_vals[2],
                        s4=s_vals[3], m4=m_vals[3],
                        s5=s_vals[4], m5=m_vals[4],
                        exam_date=ex_dt
                    )
                    messagebox.showinfo("Saved", f"Marks saved successfully!\nTotal: {tot}/500 | {pct:.1f}% | Grade: {grd}", parent=win)
                    win.destroy()
                    load_marks_table()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save marks: {str(e)}", parent=win)

            tk.Button(card, text="💾 Save Marks & Calculate Grade", font=('Arial', 10, 'bold'), bg="#16A34A", fg="#FFFFFF", bd=0,
                      command=save_marks_action).pack(pady=(0, 15), ipady=5, ipadx=15)

        tk.Button(bar, text="➕ Enter / Update Marks", font=('Arial', 9, 'bold'), bg="#16A34A", fg="#FFFFFF", bd=0,
                  command=open_add_marks_dialog).pack(side="right", padx=6, ipadx=10)

        # Bottom Bar: View Report Card, Delete, Export
        btm_bar = tk.Frame(content_fm, bg="#F8FAFC")
        btm_bar.pack(fill="x", pady=10)

        def handle_view_report_card():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Selection Required", "Please select a student's exam record from the table.")
                return
            m_id = sel[0]
            item = tree.item(m_id)
            sid = item["values"][1]
            exam_name = item["values"][4]

            # Fetch full record
            from database import get_student_marks
            records = get_student_marks(sid)
            match_rec = next((r for r in records if r[1] == exam_name), None)
            if not match_rec:
                messagebox.showerror("Error", "Could not load exam details.")
                return

            preview_report_card_window(root, sid, match_rec)

        def handle_delete_marks():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Selection Required", "Please select an exam record to delete.")
                return
            m_id = sel[0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this examination record?"):
                delete_marks_record(m_id)
                load_marks_table()

        def handle_export_marks():
            ex_val = exam_filter_var.get().strip()
            cl_val = c_filter_var.get().strip()
            fpath = filedialog.asksaveasfilename(
                title="Export Results to Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel Workbook", "*.xlsx"), ("CSV File", "*.csv")],
                initialfile=f"Results_{ex_val.replace(' ', '_')}_{cl_val.replace(' ', '_')}.xlsx"
            )
            if fpath:
                try:
                    count = excel_manager.export_marks_to_excel(ex_val, cl_val, fpath)
                    messagebox.showinfo("Export Successful", f"Exported {count} exam results to:\n{fpath}")
                except Exception as e:
                    messagebox.showerror("Export Error", f"Failed to export marks:\n{str(e)}")

        tk.Button(btm_bar, text="📄 View / Print Official Report Card", font=('Arial', 10, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0,
                  command=handle_view_report_card).pack(side="left", padx=5, ipady=4, ipadx=12)

        tk.Button(btm_bar, text="🗑️ Delete Record", font=('Arial', 10, 'bold'), bg="#DC2626", fg="#FFFFFF", bd=0,
                  command=handle_delete_marks).pack(side="left", padx=5, ipady=4, ipadx=10)

        tk.Button(btm_bar, text="📥 Export Results to Excel", font=('Arial', 10, 'bold'), bg="#0284C7", fg="#FFFFFF", bd=0,
                  command=handle_export_marks).pack(side="right", padx=5, ipady=4, ipadx=12)

        load_marks_table()

    # ==========================================
    # TAB 5: EXCEL CENTER & DATA HUB (NEW! #humanrised)
    # ==========================================
    def show_excel_center_view():
        clear_content()
        set_active_btn("excel")

        title_row = tk.Frame(content_fm, bg="#F8FAFC")
        title_row.pack(fill="x", pady=(0, 10))
        tk.Label(title_row, text="Excel & Data Integration Hub", font=('Arial', 16, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(side="left")

        # Two Main Panels: Export (Left) and Bulk Import (Right)
        panels = tk.Frame(content_fm, bg="#F8FAFC")
        panels.pack(fill="both", expand=True)

        # Panel 1: Export Hub
        p1 = tk.Frame(panels, bg="#FFFFFF", bd=1, relief="solid")
        p1.pack(side="left", fill="both", expand=True, padx=(0, 8), pady=5)

        tk.Label(p1, text="📥 Export Data to Excel / CSV", font=('Arial', 13, 'bold'), bg="#FFFFFF", fg="#1E3A5F").pack(anchor="w", padx=20, pady=(15, 6))
        tk.Label(p1, text="Generate formatted spreadsheets for offline reporting & records.", font=('Arial', 9), bg="#FFFFFF", fg="#64748B").pack(anchor="w", padx=20, pady=(0, 10))
        tk.Frame(p1, bg="#E2E8F0", height=1).pack(fill="x", padx=20, pady=(0, 15))

        def export_all_students_action():
            fpath = filedialog.asksaveasfilename(
                title="Export Students to Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel Workbook", "*.xlsx"), ("CSV File", "*.csv")],
                initialfile="All_Registered_Students.xlsx"
            )
            if fpath:
                try:
                    count = excel_manager.export_students_to_excel(fpath)
                    messagebox.showinfo("Export Successful", f"Successfully exported {count} student records to:\n{fpath}")
                except Exception as e:
                    messagebox.showerror("Error", f"Export failed:\n{str(e)}")

        tk.Button(p1, text="📑 Export All Students List (.xlsx)", font=('Arial', 10, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0,
                  command=export_all_students_action).pack(fill="x", padx=25, pady=8, ipady=6)

        def export_attendance_action():
            show_attendance_view()

        tk.Button(p1, text="📅 Export Attendance Sheets (.xlsx)", font=('Arial', 10, 'bold'), bg="#0284C7", fg="#FFFFFF", bd=0,
                  command=export_attendance_action).pack(fill="x", padx=25, pady=8, ipady=6)

        def export_marks_action():
            show_marks_view()

        tk.Button(p1, text="📝 Export Exam Marksheets (.xlsx)", font=('Arial', 10, 'bold'), bg="#16A34A", fg="#FFFFFF", bd=0,
                  command=export_marks_action).pack(fill="x", padx=25, pady=8, ipady=6)

        # Panel 2: Bulk Import Hub
        p2 = tk.Frame(panels, bg="#FFFFFF", bd=1, relief="solid")
        p2.pack(side="right", fill="both", expand=True, padx=(8, 0), pady=5)

        tk.Label(p2, text="📤 Bulk Import Students", font=('Arial', 13, 'bold'), bg="#FFFFFF", fg="#1E3A5F").pack(anchor="w", padx=20, pady=(15, 6))
        tk.Label(p2, text="Register 50-500+ students instantly using an Excel or CSV file.", font=('Arial', 9), bg="#FFFFFF", fg="#64748B").pack(anchor="w", padx=20, pady=(0, 10))
        tk.Frame(p2, bg="#E2E8F0", height=1).pack(fill="x", padx=20, pady=(0, 15))

        def download_template_action():
            fpath = filedialog.asksaveasfilename(
                title="Save Sample Student Template",
                defaultextension=".xlsx",
                filetypes=[("Excel Workbook", "*.xlsx"), ("CSV File", "*.csv")],
                initialfile="Sample_Student_Import_Template.xlsx"
            )
            if fpath:
                try:
                    excel_manager.generate_student_sample_template(fpath)
                    messagebox.showinfo("Template Downloaded", f"Pre-formatted template saved successfully to:\n{fpath}\n\nYou can fill student records into this file and import it!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save template:\n{str(e)}")

        tk.Button(p2, text="📄 Download Sample Excel Template", font=('Arial', 10, 'bold'), bg="#475569", fg="#FFFFFF", bd=0,
                  command=download_template_action).pack(fill="x", padx=25, pady=8, ipady=6)

        status_box = tk.Text(p2, font=('Consolas', 9), height=7, bg="#F8FAFC", bd=1, relief="solid")
        status_box.insert("1.0", "Ready to import. Click 'Choose Excel File to Import...' below.")

        def import_file_action():
            fpath = filedialog.askopenfilename(
                title="Select Student Excel or CSV File to Import",
                filetypes=[("Spreadsheet Files", "*.xlsx;*.xls;*.csv")]
            )
            if not fpath:
                return

            try:
                res = excel_manager.import_students_from_excel(fpath)
                s_cnt = res["success"]
                sk_cnt = res["skipped"]
                errs = res["errors"]

                status_box.delete("1.0", tk.END)
                status_box.insert(tk.END, f"=== IMPORT SUMMARY ===\n")
                status_box.insert(tk.END, f"File: {os.path.basename(fpath)}\n")
                status_box.insert(tk.END, f"✅ Successfully Imported: {s_cnt} students\n")
                status_box.insert(tk.END, f"⚠️ Skipped / Duplicates: {sk_cnt} students\n")
                if errs:
                    status_box.insert(tk.END, f"\nDetails / Warnings:\n" + "\n".join(errs[:8]))

                messagebox.showinfo("Import Complete", f"Successfully imported {s_cnt} students!\nSkipped/Duplicates: {sk_cnt}")
            except Exception as e:
                messagebox.showerror("Import Failed", f"Could not process file:\n{str(e)}")

        tk.Button(p2, text="🚀 Choose Excel File to Import...", font=('Arial', 10, 'bold'), bg="#16A34A", fg="#FFFFFF", bd=0,
                  command=import_file_action).pack(fill="x", padx=25, pady=8, ipady=6)

        status_box.pack(fill="both", expand=True, padx=25, pady=(5, 15))

    # ==========================================
    # TAB 6: ANNOUNCEMENTS (Part 13B)
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
        msg_text = tk.Text(row3, font=('Arial', 10), height=3, width=70)
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

        tk.Button(compose_card, text="📢 Publish Notice", font=('Arial', 10, 'bold'), bg="#2563EB", fg="#FFFFFF", bd=0, command=handle_post_notice).pack(anchor="e", padx=15, pady=(4, 10), ipady=4, ipadx=12)

        # Published Notices Feed
        tk.Label(content_fm, text="Recent Published Notices", font=('Arial', 12, 'bold'), bg="#F8FAFC", fg="#0F172A").pack(anchor="w", pady=(5, 5))

        feed_wrap = tk.Frame(content_fm, bg="#F8FAFC")
        feed_wrap.pack(fill="both", expand=True)

        notices = get_announcements(target_class='All Students')
        if not notices:
            tk.Label(feed_wrap, text="No announcements published yet.", font=('Arial', 10, 'italic'), bg="#F8FAFC", fg="#64748B").pack(pady=10)
        else:
            for n_t, n_aud, n_msg, n_d in notices[:4]:
                box = tk.Frame(feed_wrap, bg="#FFFFFF", bd=1, relief="solid")
                box.pack(fill="x", pady=3)

                top_l = tk.Frame(box, bg="#FFFFFF")
                top_l.pack(fill="x", padx=10, pady=(4, 2))
                tk.Label(top_l, text=f"📢 {n_t}", font=('Arial', 10, 'bold'), bg="#FFFFFF", fg="#1E3A5F").pack(side="left")
                tk.Label(top_l, text=f"Target: {n_aud}  |  {n_d}", font=('Arial', 8), bg="#FFFFFF", fg="#64748B").pack(side="right")

                tk.Label(box, text=n_msg, font=('Arial', 9), bg="#FFFFFF", fg="#334155", wraplength=700, justify="left").pack(anchor="w", padx=10, pady=(0, 4))

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
        ("attendance", "📅  Daily Attendance", show_attendance_view),
        ("marks", "📝  Exams & Marksheets", show_marks_view),
        ("excel", "📊  Excel & Data Hub", show_excel_center_view),
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
            padx=18,
            command=cmd,
        )
        btn.pack(fill="x", pady=2, ipady=6)
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
        padx=18,
        command=handle_admin_logout,
    )
    logout_btn.pack(side="bottom", fill="x", pady=15, ipady=6)

    # Launch initial view
    show_metrics_view()
