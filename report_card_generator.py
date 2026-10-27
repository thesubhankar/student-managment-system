"""
Student Management System - Report Card & Marksheet Generator #humanrised
Generates high-resolution, certificate-style academic marksheets and grade cards
using Pillow (PIL) for viewing, saving as PNG, and printing.
"""
import io
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import database


def get_truetype_font(size, bold=False):
    """Safely loads Arial or falls back to system truetype/default font."""
    font_names = ["arialbd.ttf", "segoeuib.ttf", "calibrib.ttf"] if bold else ["arial.ttf", "segoeui.ttf", "calibri.ttf"]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    try:
        return ImageFont.load_default()
    except Exception:
        return None


def generate_report_card_image(student_id, exam_record):
    """
    Constructs a professional, high-resolution A4-proportioned marksheet (800x1050 px).
    exam_record format: (id, exam_name, s1, m1, s2, m2, s3, m3, s4, m4, s5, m5, total, percentage, grade, exam_date)
    """
    student = database.get_student_by_id(student_id)
    if not student:
        raise ValueError(f"Student with ID {student_id} not found in database.")

    student_name = student[2]
    student_class = student[6]
    exam_name = exam_record[1]
    s1, m1 = exam_record[2], float(exam_record[3])
    s2, m2 = exam_record[4], float(exam_record[5])
    s3, m3 = exam_record[6], float(exam_record[7])
    s4, m4 = exam_record[8], float(exam_record[9])
    s5, m5 = exam_record[10], float(exam_record[11])
    total = float(exam_record[12])
    percentage = float(exam_record[13])
    grade = exam_record[14]
    exam_date = exam_record[15] or datetime.now().strftime("%d-%b-%Y")

    # Canvas dimensions
    width, height = 800, 1050
    card = Image.new("RGB", (width, height), color="white")
    draw = ImageDraw.Draw(card)

    # Fonts
    font_header = get_truetype_font(26, bold=True)
    font_sub = get_truetype_font(14, bold=False)
    font_section = get_truetype_font(16, bold=True)
    font_body = get_truetype_font(13, bold=False)
    font_body_bold = get_truetype_font(13, bold=True)
    font_grade_big = get_truetype_font(28, bold=True)

    # Outer decorative borders
    draw.rectangle([15, 15, width - 15, height - 15], outline="#1A365D", width=4)
    draw.rectangle([22, 22, width - 22, height - 22], outline="#2B6CB0", width=1)

    # 1. Header Banner
    draw.rectangle([25, 25, width - 25, 130], fill="#1A365D")
    draw.text((width // 2, 45), "ACADEMIC EXCELLENCE INSTITUTE", fill="white", font=font_header, anchor="mt")
    draw.text((width // 2, 80), "OFFICIAL STATEMENT OF MARKS & GRADE REPORT", fill="#E2E8F0", font=font_sub, anchor="mt")
    draw.text((width // 2, 105), f"Examination: {exam_name.upper()} | Academic Year: 2026", fill="#CBD5E0", font=font_body, anchor="mt")

    # 2. Student Info Card
    draw.rectangle([40, 150, width - 40, 260], fill="#F7FAFC", outline="#E2E8F0", width=2)

    # Student Avatar
    avatar_loaded = False
    if student[8]:
        try:
            raw_img = Image.open(io.BytesIO(student[8])).convert("RGBA")
            raw_img = raw_img.resize((85, 85), Image.Resampling.LANCZOS)
            
            # Mask to circle
            mask = Image.new("L", (85, 85), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, 85, 85), fill=255)
            
            card.paste(raw_img, (60, 162), mask)
            draw.ellipse([58, 160, 147, 249], outline="#2B6CB0", width=2)
            avatar_loaded = True
        except Exception:
            avatar_loaded = False

    if not avatar_loaded:
        draw.rectangle([60, 162, 145, 247], fill="#EDF2F7", outline="#CBD5E0", width=2)
        draw.text((102, 205), student_name[0].upper(), fill="#4A5568", font=font_grade_big, anchor="mm")

    # Details text
    col1_x = 175
    col2_x = 480
    y_start = 168
    line_h = 24

    draw.text((col1_x, y_start), "Student Name:", fill="#718096", font=font_body)
    draw.text((col1_x + 105, y_start), str(student_name), fill="#1A202C", font=font_body_bold)

    draw.text((col1_x, y_start + line_h), "Student ID:", fill="#718096", font=font_body)
    draw.text((col1_x + 105, y_start + line_h), str(student_id), fill="#1A202C", font=font_body_bold)

    draw.text((col1_x, y_start + line_h * 2), "Class / Year:", fill="#718096", font=font_body)
    draw.text((col1_x + 105, y_start + line_h * 2), str(student_class).title(), fill="#1A202C", font=font_body_bold)

    draw.text((col2_x, y_start), "Exam Name:", fill="#718096", font=font_body)
    draw.text((col2_x + 95, y_start), str(exam_name), fill="#1A202C", font=font_body_bold)

    draw.text((col2_x, y_start + line_h), "Date of Issue:", fill="#718096", font=font_body)
    draw.text((col2_x + 95, y_start + line_h), str(exam_date), fill="#1A202C", font=font_body_bold)

    draw.text((col2_x, y_start + line_h * 2), "Status:", fill="#718096", font=font_body)
    res_status = "PASSED" if percentage >= 40 else "FAILED"
    res_color = "#22543D" if percentage >= 40 else "#742A2A"
    draw.text((col2_x + 95, y_start + line_h * 2), res_status, fill=res_color, font=font_body_bold)

    # 3. Marks Table
    table_top = 285
    row_height = 42
    cols = [
        ("SL", 40, 90),
        ("COURSE / SUBJECT NAME", 90, 420),
        ("MAX", 420, 510),
        ("PASS", 510, 600),
        ("OBTAINED", 600, 700),
        ("GRADE", 700, 760)
    ]

    # Table Header Row
    draw.rectangle([40, table_top, width - 40, table_top + 38], fill="#2B6CB0")
    for title, x1, x2 in cols:
        draw.text(((x1 + x2) // 2, table_top + 19), title, fill="white", font=font_body_bold, anchor="mm")

    subjects = [
        (1, s1, m1),
        (2, s2, m2),
        (3, s3, m3),
        (4, s4, m4),
        (5, s5, m5),
    ]

    curr_y = table_top + 38
    for idx, sname, mark in subjects:
        # Alternating background
        bg_col = "#F8FAFC" if idx % 2 == 1 else "white"
        draw.rectangle([40, curr_y, width - 40, curr_y + row_height], fill=bg_col, outline="#E2E8F0")

        # Sub grade
        sub_pct = mark
        sub_grade, _ = database.calculate_grade(sub_pct)
        status_col = "#2B6CB0" if mark >= 40 else "#E53E3E"

        draw.text(((cols[0][1] + cols[0][2]) // 2, curr_y + 21), str(idx), fill="#2D3748", font=font_body, anchor="mm")
        draw.text((cols[1][1] + 15, curr_y + 21), str(sname), fill="#1A202C", font=font_body_bold, anchor="lm")
        draw.text(((cols[2][1] + cols[2][2]) // 2, curr_y + 21), "100", fill="#718096", font=font_body, anchor="mm")
        draw.text(((cols[3][1] + cols[3][2]) // 2, curr_y + 21), "40", fill="#718096", font=font_body, anchor="mm")
        draw.text(((cols[4][1] + cols[4][2]) // 2, curr_y + 21), f"{mark:.1f}", fill=status_col, font=font_body_bold, anchor="mm")
        draw.text(((cols[5][1] + cols[5][2]) // 2, curr_y + 21), sub_grade, fill="#2D3748", font=font_body_bold, anchor="mm")

        curr_y += row_height

    # Total Marks Summary Row
    draw.rectangle([40, curr_y, width - 40, curr_y + 44], fill="#EDF2F7", outline="#CBD5E0", width=2)
    draw.text((cols[1][1] + 15, curr_y + 22), "TOTAL MARKS (AGGREGATE)", fill="#1A202C", font=font_section, anchor="lm")
    draw.text(((cols[2][1] + cols[2][2]) // 2, curr_y + 22), "500", fill="#1A202C", font=font_body_bold, anchor="mm")
    draw.text(((cols[3][1] + cols[3][2]) // 2, curr_y + 22), "200", fill="#1A202C", font=font_body_bold, anchor="mm")
    draw.text(((cols[4][1] + cols[4][2]) // 2, curr_y + 22), f"{total:.1f}", fill="#1A365D", font=font_section, anchor="mm")
    draw.text(((cols[5][1] + cols[5][2]) // 2, curr_y + 22), grade, fill="#1A365D", font=font_section, anchor="mm")

    # 4. Result Analytics Card
    card_y = curr_y + 65
    draw.rectangle([40, card_y, width - 40, card_y + 130], fill="#F7FAFC", outline="#CBD5E0", width=2)

    # 3 Summary Boxes inside Card
    box_w = (width - 120) // 3
    b1_x = 55
    b2_x = b1_x + box_w + 10
    b3_x = b2_x + box_w + 10

    # Box 1: Percentage
    draw.rectangle([b1_x, card_y + 15, b1_x + box_w, card_y + 115], fill="white", outline="#E2E8F0")
    draw.text((b1_x + box_w // 2, card_y + 35), "PERCENTAGE", fill="#718096", font=font_body_bold, anchor="mm")
    draw.text((b1_x + box_w // 2, card_y + 75), f"{percentage:.1f}%", fill="#2B6CB0", font=font_grade_big, anchor="mm")

    # Box 2: Overall Grade
    draw.rectangle([b2_x, card_y + 15, b2_x + box_w, card_y + 115], fill="white", outline="#E2E8F0")
    draw.text((b2_x + box_w // 2, card_y + 35), "FINAL GRADE", fill="#718096", font=font_body_bold, anchor="mm")
    draw.text((b2_x + box_w // 2, card_y + 75), grade, fill="#2B6CB0", font=font_grade_big, anchor="mm")

    # Box 3: Classification
    draw.rectangle([b3_x, card_y + 15, b3_x + box_w, card_y + 115], fill="white", outline="#E2E8F0")
    draw.text((b3_x + box_w // 2, card_y + 35), "RESULT STATUS", fill="#718096", font=font_body_bold, anchor="mm")
    status_text = "PASS" if percentage >= 40 else "FAIL"
    status_badge_color = "#38A169" if percentage >= 40 else "#E53E3E"
    draw.text((b3_x + box_w // 2, card_y + 75), status_text, fill=status_badge_color, font=font_grade_big, anchor="mm")

    # 5. Signatures & Official Stamp Footer
    sig_y = height - 160
    draw.line([70, sig_y, 250, sig_y], fill="#4A5568", width=1)
    draw.text((160, sig_y + 15), "Controller of Examinations", fill="#4A5568", font=font_body, anchor="mt")

    # College Seal Placeholder in Center
    draw.ellipse([345, sig_y - 45, 455, sig_y + 45], outline="#CBD5E0", width=2)
    draw.text((400, sig_y), "OFFICIAL\nSEAL", fill="#A0AEC0", font=font_body_bold, anchor="mm", align="center")

    draw.line([width - 250, sig_y, width - 70, sig_y], fill="#4A5568", width=1)
    draw.text((width - 160, sig_y + 15), "Principal / Dean Academic", fill="#4A5568", font=font_body, anchor="mt")

    # Bottom watermark/verification note
    draw.text((width // 2, height - 35), 
              "This is a computer-generated academic grade card. Generated by Student Management System.",
              fill="#A0AEC0", font=font_body, anchor="mm")

    return card


def preview_report_card_window(parent, student_id, exam_record):
    """
    Opens an interactive modal window displaying the rendered Report Card
    with a 'Download PNG' button.
    """
    try:
        report_img = generate_report_card_image(student_id, exam_record)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate report card:\n{str(e)}", parent=parent)
        return

    win = tk.Toplevel(parent)
    win.title(f"Report Card - {exam_record[1]}")
    win.geometry("560x780")
    win.resizable(False, False)
    win.configure(bg="#F1F5F9")
    win.grab_set()

    # Header Controls
    top_bar = tk.Frame(win, bg="#1E293B", height=50)
    top_bar.pack(fill=tk.X)

    title_lbl = tk.Label(top_bar, text="Academic Grade Card Preview", font=("Segoe UI", 13, "bold"), fg="white", bg="#1E293B")
    title_lbl.pack(side=tk.LEFT, padx=15, pady=10)

    def save_png():
        file_path = filedialog.asksaveasfilename(
            parent=win,
            title="Save Report Card as PNG",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("All Files", "*.*")],
            initialfile=f"ReportCard_{student_id}_{exam_record[1].replace(' ', '_')}.png"
        )
        if file_path:
            try:
                report_img.save(file_path, "PNG")
                messagebox.showinfo("Saved", f"Report card saved successfully to:\n{file_path}", parent=win)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}", parent=win)

    save_btn = tk.Button(top_bar, text="💾 Save as PNG", font=("Segoe UI", 10, "bold"), 
                         bg="#10B981", fg="white", activebackground="#059669", 
                         relief="flat", cursor="hand2", command=save_png)
    save_btn.pack(side=tk.RIGHT, padx=15, pady=8)

    # Scaled preview canvas
    # Original is 800x1050 -> scale to 520x682
    preview_w, preview_h = 520, 682
    scaled_img = report_img.resize((preview_w, preview_h), Image.Resampling.LANCZOS)
    photo_tk = ImageTk.PhotoImage(scaled_img)

    canvas_frame = tk.Frame(win, bg="#E2E8F0", bd=1, relief="solid")
    canvas_frame.pack(padx=20, pady=15)

    img_label = tk.Label(canvas_frame, image=photo_tk, bg="white")
    img_label.image = photo_tk  # Keep reference
    img_label.pack()
