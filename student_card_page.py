import os
import io
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(BASE_DIR, 'Images')


def start_student_card_page(root, student_data, prev_page='welcome'):
    """
    Renders the Student ID Card Page.
    student_data: (id_number, password, name, age, gender, phone_number, student_class, email, image_blob)
    """
    id_number = str(student_data[0]) if student_data else "N/A"
    name = str(student_data[2]) if student_data else "N/A"
    age = str(student_data[3]) if student_data else "N/A"
    gender = str(student_data[4]) if student_data else "N/A"
    phone_number = str(student_data[5]) if student_data else "N/A"
    student_class = str(student_data[6]) if student_data else "N/A"
    email = str(student_data[7]) if student_data else "N/A"
    image_blob = student_data[8] if student_data and len(student_data) > 8 else None

    # Load and process student profile image
    profile_photo_pil = None
    if image_blob:
        try:
            profile_photo_pil = Image.open(io.BytesIO(image_blob)).convert("RGBA")
        except Exception:
            profile_photo_pil = None

    if not profile_photo_pil:
        default_img_path = os.path.join(IMAGES_DIR, 'add_student_img.png')
        if os.path.exists(default_img_path):
            profile_photo_pil = Image.open(default_img_path).convert("RGBA")
        else:
            profile_photo_pil = Image.new("RGBA", (100, 100), color="#E2E8F0")

    profile_photo_resized = profile_photo_pil.resize((70, 70), Image.Resampling.LANCZOS)
    profile_photo_tk = ImageTk.PhotoImage(profile_photo_resized)

    # Load Card Frame
    frame_path = os.path.join(IMAGES_DIR, 'student_card_frame.png')
    card_width, card_height = 360, 360
    if os.path.exists(frame_path):
        frame_pil = Image.open(frame_path).convert("RGBA").resize((card_width, card_height), Image.Resampling.LANCZOS)
    else:
        frame_pil = Image.new("RGBA", (card_width, card_height), color="#FFFFFF")

    card_frame_tk = ImageTk.PhotoImage(frame_pil)

    # Retain references so garbage collector does not remove them
    root._card_frame_tk = card_frame_tk
    root._profile_photo_tk = profile_photo_tk

    def forward_to_previous_page():
        student_card_page_fm.destroy()
        root.update()
        if prev_page == 'student_login':
            from student_login_page import start_student_login_page
            start_student_login_page(root)
        else:
            from welcome_page import start_welcome_page
            start_welcome_page(root)

    # Main page container
    student_card_page_fm = tk.Frame(
        root,
        bg="#B7C3B7",
        highlightbackground="#048D9C",
        highlightthickness=3,
    )
    student_card_page_fm.place(x=25, y=20, width=450, height=560)

    # Header
    heading_lb = tk.Label(
        student_card_page_fm,
        text="Student Identity Card",
        bg="#1e3a5f",
        fg="#ffffff",
        font=('Arial', 16, 'bold'),
    )
    heading_lb.place(x=0, y=0, width=444, height=38)

    # Back / Logout Button
    back_btn = tk.Button(
        student_card_page_fm,
        text='← Back',
        bg="#1e3a5f",
        activebackground="#1e3a5f",
        fg="#FFFFFF",
        activeforeground="#CBD5E1",
        font=('Arial', 11, 'bold'),
        bd=0,
        relief='flat',
        command=forward_to_previous_page,
    )
    back_btn.place(x=6, y=5, height=28)

    # Card Canvas
    card_canvas = tk.Canvas(
        student_card_page_fm,
        width=card_width,
        height=card_height,
        bg="#B7C3B7",
        bd=0,
        highlightthickness=0,
    )
    card_canvas.place(x=42, y=48)

    # Draw Card Background Frame
    card_canvas.create_image(0, 0, anchor="nw", image=card_frame_tk)

    # Card Header / Title inside frame
    card_canvas.create_text(
        card_width // 2, 35,
        text="STUDENT MANAGEMENT SYSTEM",
        font=('Arial', 10, 'bold'),
        fill="#1e3a5f"
    )
    card_canvas.create_text(
        card_width // 2, 52,
        text="STUDENT IDENTITY CARD",
        font=('Arial', 12, 'bold'),
        fill="#081579"
    )
    card_canvas.create_line(30, 65, card_width - 30, 65, fill="#048D9C", width=2)

    # Student Photo with Border
    photo_x, photo_y = 35, 78
    card_canvas.create_rectangle(
        photo_x - 2, photo_y - 2, photo_x + 72, photo_y + 72,
        outline="#1e3a5f", width=2, fill="#FFFFFF"
    )
    card_canvas.create_image(photo_x, photo_y, anchor="nw", image=profile_photo_tk)

    # Student Name & ID in Top Section
    card_canvas.create_text(
        120, 85,
        anchor="nw",
        text=name,
        font=('Arial', 12, 'bold'),
        fill="#1e3a5f"
    )
    card_canvas.create_text(
        120, 110,
        anchor="nw",
        text=f"ID: {id_number}",
        font=('Arial', 11, 'bold'),
        fill="#081579"
    )
    card_canvas.create_text(
        120, 132,
        anchor="nw",
        text=f"Year: {student_class}",
        font=('Arial', 10, 'bold'),
        fill="#334155"
    )

    card_canvas.create_line(30, 160, card_width - 30, 160, fill="#CBD5E1", width=1.5)

    # Details rows
    details = [
        ("Gender / Age:", f"{gender} / {age} yrs"),
        ("Contact No:", phone_number),
        ("Email ID:", email),
    ]

    start_y = 175
    line_spacing = 30
    for i, (label, val) in enumerate(details):
        curr_y = start_y + (i * line_spacing)
        card_canvas.create_text(
            35, curr_y,
            anchor="nw",
            text=label,
            font=('Arial', 10, 'bold'),
            fill="#475569"
        )
        card_canvas.create_text(
            140, curr_y,
            anchor="nw",
            text=val,
            font=('Arial', 10, 'bold'),
            fill="#0F172A"
        )

    # Card Footer inside frame
    card_canvas.create_line(30, 310, card_width - 30, 310, fill="#048D9C", width=1.5)
    card_canvas.create_text(
        card_width // 2, 330,
        text="Authorized Student Identity",
        font=('Arial', 9, 'italic'),
        fill="#64748B"
    )

    # Save Student Card Function
    def save_student_card_image():
        file_path = filedialog.asksaveasfilename(
            parent=root,
            title="Save Student Card As",
            defaultextension=".png",
            initialfile=f"student_card_{id_number}.png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        try:
            # Generate high-resolution PIL Card Image
            card_img = frame_pil.copy()
            draw = ImageDraw.Draw(card_img)

            # Paste profile photo onto card
            card_img.paste(profile_photo_resized, (photo_x, photo_y), profile_photo_resized)

            # Draw photo border
            draw.rectangle(
                [photo_x - 2, photo_y - 2, photo_x + 72, photo_y + 72],
                outline="#1e3a5f", width=2
            )

            # Load default/truetype fonts if available
            try:
                font_title = ImageFont.truetype("arialbd.ttf", 13)
                font_subtitle = ImageFont.truetype("arialbd.ttf", 15)
                font_name = ImageFont.truetype("arialbd.ttf", 15)
                font_bold = ImageFont.truetype("arialbd.ttf", 13)
                font_regular = ImageFont.truetype("arial.ttf", 12)
                font_small = ImageFont.truetype("ariali.ttf", 11)
            except Exception:
                font_title = font_subtitle = font_name = font_bold = font_regular = font_small = ImageFont.load_default()

            # Draw Headers
            draw.text((card_width // 2, 28), "STUDENT MANAGEMENT SYSTEM", fill="#1e3a5f", anchor="mm", font=font_title)
            draw.text((card_width // 2, 48), "STUDENT IDENTITY CARD", fill="#081579", anchor="mm", font=font_subtitle)
            draw.line([(30, 62), (card_width - 30, 62)], fill="#048D9C", width=2)

            # Student Info Top
            draw.text((120, 80), name, fill="#1e3a5f", font=font_name)
            draw.text((120, 105), f"ID: {id_number}", fill="#081579", font=font_bold)
            draw.text((120, 128), f"Year: {student_class}", fill="#334155", font=font_regular)

            draw.line([(30, 158), (card_width - 30, 158)], fill="#CBD5E1", width=1)

            # Details
            for i, (label, val) in enumerate(details):
                curr_y = start_y + (i * line_spacing) - 5
                draw.text((35, curr_y), label, fill="#475569", font=font_bold)
                draw.text((140, curr_y), val, fill="#0F172A", font=font_regular)

            # Footer
            draw.line([(30, 305), (card_width - 30, 305)], fill="#048D9C", width=1)
            draw.text((card_width // 2, 325), "Authorized Student Identity", fill="#64748B", anchor="mm", font=font_small)

            # Save file
            card_img.convert("RGB").save(file_path)
            show_popup_message("Student Card saved successfully!")
        except Exception as e:
            show_popup_message(f"Error saving card: {str(e)}")

    def print_card():
        show_popup_message("Please save the card as PNG to print!")

    def show_popup_message(msg):
        popup_fm = tk.Frame(
            root,
            bg="#B7C3B7",
            highlightbackground="#048D9C",
            highlightthickness=3,
        )
        popup_fm.place(x=100, y=180, width=300, height=180)

        lbl = tk.Label(
            popup_fm,
            text=msg,
            font=('Arial', 11, 'bold'),
            bg="#B7C3B7",
            fg="#081579",
            wraplength=260,
        )
        lbl.place(x=20, y=30, width=260)

        ok_btn = tk.Button(
            popup_fm,
            text="OK",
            font=('Arial', 12, 'bold'),
            bg="#217A5A",
            fg="#FFFFFF",
            bd=0,
            command=popup_fm.destroy,
        )
        ok_btn.place(x=110, y=120, width=80, height=32)

    # Action Buttons
    save_student_card_btn = tk.Button(
        student_card_page_fm,
        text='💾 Save Card',
        bg="#159BD7",
        fg="#FFFFFF",
        activebackground="#0D7AA8",
        activeforeground="#FFFFFF",
        font=('Arial', 13, 'bold'),
        bd=0,
        command=save_student_card_image,
    )
    save_student_card_btn.place(x=45, y=430, width=160, height=40)

    print_student_card_btn = tk.Button(
        student_card_page_fm,
        text="🖨️ Print",
        bg="#159BD7",
        fg="#FFFFFF",
        activebackground="#0D7AA8",
        activeforeground="#FFFFFF",
        font=('Arial', 13, 'bold'),
        bd=0,
        command=print_card,
    )
    print_student_card_btn.place(x=225, y=430, width=80, height=40)

    logout_btn = tk.Button(
        student_card_page_fm,
        text="🚪 Logout",
        bg="#880B14",
        fg="#FFFFFF",
        activebackground="#66080E",
        activeforeground="#FFFFFF",
        font=('Arial', 13, 'bold'),
        bd=0,
        command=forward_to_previous_page,
    )
    logout_btn.place(x=320, y=430, width=90, height=40)