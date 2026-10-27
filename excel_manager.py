"""
Student Management System - Excel & CSV Manager #humanrised
Provides robust export, import, and template generation for Student records,
Attendance sheets, and Examination Marks using pandas and openpyxl.
"""
import os
import io
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import database


def create_default_avatar_bytes(name="Student"):
    """
    Creates a clean default PNG avatar in-memory for bulk-imported students.
    """
    initial = (name.strip()[0] if name and name.strip() else "S").upper()
    img = Image.new("RGBA", (100, 100), color=(52, 152, 219, 255)) # Soft blue background
    draw = ImageDraw.Draw(img)
    
    # Draw simple centered initial
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except Exception:
        font = ImageFont.load_default()
        
    draw.text((36, 26), initial, fill="white", font=font)
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()


def export_students_to_excel(file_path):
    """
    Exports all registered students to an Excel (.xlsx) or CSV file.
    """
    students = database.get_all_students()
    data = []
    for s in students:
        # id_number, name, age, gender, phone_number, class, email, image
        data.append({
            "Student ID": s[0],
            "Full Name": s[1],
            "Class / Year": s[5],
            "Age": s[2],
            "Gender": s[3],
            "Phone Number": s[4],
            "Email Address": s[6]
        })
        
    df = pd.DataFrame(data)
    if not df.empty:
        df.sort_values(by="Full Name", inplace=True)
        
    if file_path.lower().endswith(".csv"):
        df.to_csv(file_path, index=False)
    else:
        df.to_excel(file_path, index=False, sheet_name="Students_List")
    return len(data)


def export_attendance_to_excel(date_str, class_year, file_path):
    """
    Exports attendance sheet for a given date and class to Excel or CSV.
    """
    records = database.get_attendance_for_date_and_class(date_str, class_year)
    data = []
    for r in records:
        # id_number, name, class, status
        data.append({
            "Student ID": r[0],
            "Student Name": r[1],
            "Class / Year": r[2],
            "Date": date_str,
            "Attendance Status": r[3]
        })
        
    df = pd.DataFrame(data)
    if file_path.lower().endswith(".csv"):
        df.to_csv(file_path, index=False)
    else:
        sheet_name = f"Attendance_{date_str.replace('-', '')}"[:30]
        df.to_excel(file_path, index=False, sheet_name=sheet_name)
    return len(data)


def export_marks_to_excel(exam_name, class_year, file_path):
    """
    Exports examination results and grades to Excel or CSV.
    """
    records = database.get_marks_by_exam_and_class(exam_name, class_year)
    data = []
    for r in records:
        # marks_id, student_id, student_name, class, exam_name, total, percentage, grade, exam_date
        data.append({
            "Student ID": r[1],
            "Student Name": r[2],
            "Class / Year": r[3],
            "Exam Name": r[4],
            "Total Marks (500)": r[5],
            "Percentage (%)": r[6],
            "Grade": r[7],
            "Exam Date": r[8]
        })
        
    df = pd.DataFrame(data)
    if file_path.lower().endswith(".csv"):
        df.to_csv(file_path, index=False)
    else:
        df.to_excel(file_path, index=False, sheet_name="Exam_Results")
    return len(data)


def generate_student_sample_template(file_path):
    """
    Generates a pre-formatted Excel template with sample student records
    to guide administrators during bulk import.
    """
    sample_data = [
        {
            "id_number": "1001",
            "password": "pass1001",
            "name": "Rahul Sharma",
            "age": "20",
            "gender": "Male",
            "phone_number": "9876543210",
            "class": "1st year",
            "email": "rahul@example.com"
        },
        {
            "id_number": "1002",
            "password": "pass1002",
            "name": "Priyanka Jena",
            "age": "21",
            "gender": "Female",
            "phone_number": "9876543211",
            "class": "2nd year",
            "email": "priyanka@example.com"
        },
        {
            "id_number": "1003",
            "password": "pass1003",
            "name": "Amit Kumar Nayak",
            "age": "22",
            "gender": "Male",
            "phone_number": "9876543212",
            "class": "3rd year",
            "email": "amit@example.com"
        }
    ]
    df = pd.DataFrame(sample_data)
    if file_path.lower().endswith(".csv"):
        df.to_csv(file_path, index=False)
    else:
        df.to_excel(file_path, index=False, sheet_name="Student_Template")
    return file_path


def import_students_from_excel(file_path):
    """
    Imports student records in bulk from an Excel (.xlsx/.xls) or CSV file.
    Validates required fields and saves to SQLite database.
    Returns: {"success": int, "skipped": int, "errors": list}
    """
    if file_path.lower().endswith(".csv"):
        df = pd.read_csv(file_path, dtype=str)
    else:
        df = pd.read_excel(file_path, dtype=str)
        
    # Standardize column headers to lowercase and trimmed
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]
    
    # Required field mapping
    # id_number, password, name, age, gender, phone_number, class, email
    success_count = 0
    skipped_count = 0
    errors = []
    
    for index, row in df.iterrows():
        row_num = index + 2  # Excel 1-based header offset
        
        # Extract student ID
        id_val = row.get("id_number") or row.get("id") or row.get("student_id") or row.get("roll_no")
        if not id_val or pd.isna(id_val) or not str(id_val).strip():
            errors.append(f"Row {row_num}: Missing Student ID.")
            skipped_count += 1
            continue
        id_str = str(id_val).strip()
        
        # Extract student name
        name_val = row.get("name") or row.get("full_name") or row.get("student_name")
        if not name_val or pd.isna(name_val) or not str(name_val).strip():
            errors.append(f"Row {row_num} (ID {id_str}): Missing Student Name.")
            skipped_count += 1
            continue
        name_str = str(name_val).strip()
        
        # Check if already exists in DB
        if database.check_id_already_exist(id_str):
            errors.append(f"Row {row_num}: Student ID '{id_str}' already exists in database.")
            skipped_count += 1
            continue
            
        # Optional fields with clean fallbacks
        password_str = str(row.get("password") or f"pass{id_str}").strip()
        age_str = str(row.get("age") or "19").strip()
        gender_str = str(row.get("gender") or "Other").strip().capitalize()
        phone_str = str(row.get("phone_number") or row.get("phone") or "N/A").strip()
        class_str = str(row.get("class") or row.get("student_class") or row.get("year") or "1st year").strip()
        email_str = str(row.get("email") or row.get("email_address") or f"{id_str}@college.edu").strip()
        
        # Default placeholder avatar
        avatar_bytes = create_default_avatar_bytes(name_str)
        
        try:
            database.add_data(
                id_number=id_str,
                password=password_str,
                name=name_str,
                age=age_str,
                gender=gender_str,
                phone_number=phone_str,
                student_class=class_str,
                email=email_str,
                pic_data=avatar_bytes
            )
            success_count += 1
        except Exception as e:
            errors.append(f"Row {row_num} (ID {id_str}): Database error: {str(e)}")
            skipped_count += 1
            
    return {
        "success": success_count,
        "skipped": skipped_count,
        "errors": errors
    }
