"""
Student Management System - Database Operations #humanrised
Handles SQLite database connection, table initialization, attendance tracking,
examination marks, announcement records, and student profile CRUD queries.
"""
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'student_account.db')


def init_database():
    """Initializes the SQLite database and creates all tables if needed."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # 1. Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id_number TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            age TEXT,
            gender TEXT,
            phone_number TEXT,
            class TEXT,
            email TEXT,
            image BLOB
        )
    """)
    
    # 2. Announcements Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS announcements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            target_class TEXT NOT NULL,
            message TEXT NOT NULL,
            date_posted TEXT NOT NULL
        )
    """)
    
    # 3. Attendance Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            class_year TEXT NOT NULL,
            UNIQUE(student_id, date)
        )
    """)
    
    # 4. Exam Marks Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            exam_name TEXT NOT NULL,
            subject_1 TEXT,
            marks_1 REAL,
            subject_2 TEXT,
            marks_2 REAL,
            subject_3 TEXT,
            marks_3 REAL,
            subject_4 TEXT,
            marks_4 REAL,
            subject_5 TEXT,
            marks_5 REAL,
            total REAL,
            percentage REAL,
            grade TEXT,
            exam_date TEXT,
            UNIQUE(student_id, exam_name)
        )
    """)
    
    connection.commit()
    connection.close()


def check_id_already_exist(id_number):
    """Checks whether the given student ID already exists in the database."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT id_number FROM data WHERE id_number = ?", (str(id_number),))
    result = cursor.fetchone()
    connection.close()
    return result is not None


# Alias for backward compatibility
check_id_alredy_exist = check_id_already_exist


def add_data(id_number, password, name, age, gender, phone_number, student_class, email, pic_data):
    """Adds a new student record to the database."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO data (id_number, password, name, age, gender, phone_number, class, email, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (str(id_number), str(password), name, str(age), gender, str(phone_number), student_class, email, pic_data))
    connection.commit()
    connection.close()


def check_student_login(id_number, password):
    """Authenticates student credentials and returns student details if matched."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM data WHERE id_number = ? AND password = ?", (str(id_number), str(password)))
    user = cursor.fetchone()
    connection.close()
    return user


def get_student_by_id(id_number):
    """Fetches a student record using their unique ID number."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM data WHERE id_number = ?", (str(id_number),))
    user = cursor.fetchone()
    connection.close()
    return user


def get_all_students():
    """Retrieves all students from database ordered by Name."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT id_number, name, age, gender, phone_number, class, email, image FROM data ORDER BY name ASC")
    students = cursor.fetchall()
    connection.close()
    return students


def search_students(keyword):
    """Searches students by ID number, Name, Class, or Email."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    pattern = f"%{keyword.strip()}%"
    cursor.execute("""
        SELECT id_number, name, age, gender, phone_number, class, email, image 
        FROM data 
        WHERE id_number LIKE ? OR name LIKE ? OR class LIKE ? OR email LIKE ?
        ORDER BY name ASC
    """, (pattern, pattern, pattern, pattern))
    students = cursor.fetchall()
    connection.close()
    return students


def update_student(id_number, name, age, gender, phone_number, student_class, email, pic_data=None):
    """Updates an existing student's personal details and optionally their photo."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    if pic_data:
        cursor.execute("""
            UPDATE data 
            SET name = ?, age = ?, gender = ?, phone_number = ?, class = ?, email = ?, image = ?
            WHERE id_number = ?
        """, (name, str(age), gender, str(phone_number), student_class, email, pic_data, str(id_number)))
    else:
        cursor.execute("""
            UPDATE data 
            SET name = ?, age = ?, gender = ?, phone_number = ?, class = ?, email = ?
            WHERE id_number = ?
        """, (name, str(age), gender, str(phone_number), student_class, email, str(id_number)))
    connection.commit()
    connection.close()


def update_student_password(id_number, new_password):
    """Updates student login password."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("UPDATE data SET password = ? WHERE id_number = ?", (str(new_password), str(id_number)))
    connection.commit()
    connection.close()


def delete_student(id_number):
    """Deletes a student record permanently along with their attendance and marks."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM data WHERE id_number = ?", (str(id_number),))
    cursor.execute("DELETE FROM attendance WHERE student_id = ?", (str(id_number),))
    cursor.execute("DELETE FROM marks WHERE student_id = ?", (str(id_number),))
    connection.commit()
    connection.close()


def get_student_counts():
    """Returns total student count and breakdown by year/class."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM data")
    total = cursor.fetchone()[0]

    classes = ['1st year', '2nd year', '3rd year', '4th year']
    class_counts = {}
    for c in classes:
        cursor.execute("SELECT COUNT(*) FROM data WHERE LOWER(class) = ?", (c.lower(),))
        class_counts[c] = cursor.fetchone()[0]

    connection.close()
    return {"total": total, "classes": class_counts}


def verify_student_recovery(id_number, email):
    """Verifies if student ID and Email match for password recovery."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT id_number, name FROM data WHERE id_number = ? AND LOWER(email) = ?", 
                   (str(id_number).strip(), email.strip().lower()))
    match = cursor.fetchone()
    connection.close()
    return match


def add_announcement(title, target_class, message, date_posted):
    """Adds a new announcement from admin."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO announcements (title, target_class, message, date_posted)
        VALUES (?, ?, ?, ?)
    """, (title, target_class, message, date_posted))
    connection.commit()
    connection.close()


def get_announcements(target_class='All Students'):
    """Fetches announcements targeted to All Students or student's specific class."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    if target_class == 'All Students':
        cursor.execute("SELECT title, target_class, message, date_posted FROM announcements ORDER BY id DESC")
    else:
        cursor.execute("""
            SELECT title, target_class, message, date_posted 
            FROM announcements 
            WHERE target_class = 'All Students' OR LOWER(target_class) = ? 
            ORDER BY id DESC
        """, (target_class.strip().lower(),))
    announcements = cursor.fetchall()
    connection.close()
    return announcements


# ==============================================================================
# ATTENDANCE MANAGEMENT OPERATIONS #humanrised
# ==============================================================================

def mark_attendance(student_id, date_str, status, class_year):
    """
    Records or updates attendance for a student on a specific date.
    Status can be 'Present', 'Absent', or 'Leave'.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO attendance (student_id, date, status, class_year)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(student_id, date) DO UPDATE SET
            status = excluded.status,
            class_year = excluded.class_year
    """, (str(student_id), date_str, status, class_year))
    connection.commit()
    connection.close()


def get_attendance_for_date_and_class(date_str, class_year='All Classes'):
    """
    Returns list of students with their attendance status for a given date and class.
    Each item: (id_number, name, class, status)
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    if class_year == 'All Classes':
        cursor.execute("""
            SELECT d.id_number, d.name, d.class, COALESCE(a.status, 'Not Marked')
            FROM data d
            LEFT JOIN attendance a ON d.id_number = a.student_id AND a.date = ?
            ORDER BY d.class, d.name
        """, (date_str,))
    else:
        cursor.execute("""
            SELECT d.id_number, d.name, d.class, COALESCE(a.status, 'Not Marked')
            FROM data d
            LEFT JOIN attendance a ON d.id_number = a.student_id AND a.date = ?
            WHERE LOWER(d.class) = ?
            ORDER BY d.name
        """, (date_str, class_year.strip().lower()))
        
    records = cursor.fetchall()
    connection.close()
    return records


def get_student_attendance_summary(student_id):
    """
    Calculates total days, present days, absent days, leave days,
    and attendance percentage for a student.
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    cursor.execute("SELECT status FROM attendance WHERE student_id = ?", (str(student_id),))
    rows = cursor.fetchall()
    connection.close()
    
    total = len(rows)
    present = sum(1 for (s,) in rows if s == 'Present')
    absent = sum(1 for (s,) in rows if s == 'Absent')
    leave = sum(1 for (s,) in rows if s == 'Leave')
    
    percentage = round((present / total * 100), 1) if total > 0 else 100.0
    
    return {
        "total_days": total,
        "present_days": present,
        "absent_days": absent,
        "leave_days": leave,
        "percentage": percentage
    }


def get_student_attendance_history(student_id, limit=30):
    """Returns recent attendance records for a specific student."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT date, status, class_year
        FROM attendance
        WHERE student_id = ?
        ORDER BY date DESC
        LIMIT ?
    """, (str(student_id), limit))
    records = cursor.fetchall()
    connection.close()
    return records


# ==============================================================================
# EXAMINATION MARKS & GRADES OPERATIONS #humanrised
# ==============================================================================

def calculate_grade(percentage):
    """Calculates letter grade and performance description from percentage."""
    if percentage >= 90:
        return 'A+', 'Outstanding'
    elif percentage >= 80:
        return 'A', 'Excellent'
    elif percentage >= 70:
        return 'B+', 'Very Good'
    elif percentage >= 60:
        return 'B', 'Good'
    elif percentage >= 50:
        return 'C', 'Average'
    elif percentage >= 40:
        return 'D', 'Pass'
    else:
        return 'F', 'Fail'


def save_or_update_marks(student_id, exam_name, s1, m1, s2, m2, s3, m3, s4, m4, s5, m5, exam_date):
    """
    Saves or updates exam marks for a student and calculates total, percentage, and grade.
    """
    total = float(m1) + float(m2) + float(m3) + float(m4) + float(m5)
    percentage = round(total / 5.0, 2)
    grade, _ = calculate_grade(percentage)
    
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO marks (
            student_id, exam_name, subject_1, marks_1, subject_2, marks_2,
            subject_3, marks_3, subject_4, marks_4, subject_5, marks_5,
            total, percentage, grade, exam_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(student_id, exam_name) DO UPDATE SET
            subject_1 = excluded.subject_1, marks_1 = excluded.marks_1,
            subject_2 = excluded.subject_2, marks_2 = excluded.marks_2,
            subject_3 = excluded.subject_3, marks_3 = excluded.marks_3,
            subject_4 = excluded.subject_4, marks_4 = excluded.marks_4,
            subject_5 = excluded.subject_5, marks_5 = excluded.marks_5,
            total = excluded.total, percentage = excluded.percentage,
            grade = excluded.grade, exam_date = excluded.exam_date
    """, (
        str(student_id), exam_name, s1, float(m1), s2, float(m2),
        s3, float(m3), s4, float(m4), s5, float(m5),
        total, percentage, grade, exam_date
    ))
    connection.commit()
    connection.close()
    return total, percentage, grade


def get_student_marks(student_id):
    """Returns all exam records for a specific student."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, exam_name, subject_1, marks_1, subject_2, marks_2,
               subject_3, marks_3, subject_4, marks_4, subject_5, marks_5,
               total, percentage, grade, exam_date
        FROM marks
        WHERE student_id = ?
        ORDER BY id DESC
    """, (str(student_id),))
    records = cursor.fetchall()
    connection.close()
    return records


def get_marks_by_exam_and_class(exam_name='All Exams', class_year='All Classes'):
    """
    Fetches student marks filtered by exam name and/or class year.
    Returns: (marks_id, student_id, student_name, class, exam_name, total, percentage, grade, exam_date)
    """
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    query = """
        SELECT m.id, d.id_number, d.name, d.class, m.exam_name, m.total, m.percentage, m.grade, m.exam_date
        FROM marks m
        JOIN data d ON m.student_id = d.id_number
        WHERE 1=1
    """
    params = []
    
    if exam_name != 'All Exams':
        query += " AND m.exam_name = ?"
        params.append(exam_name)
    if class_year != 'All Classes':
        query += " AND LOWER(d.class) = ?"
        params.append(class_year.strip().lower())
        
    query += " ORDER BY d.class, d.name"
    cursor.execute(query, params)
    records = cursor.fetchall()
    connection.close()
    return records


def delete_marks_record(marks_id):
    """Deletes an exam marks record by ID."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM marks WHERE id = ?", (marks_id,))
    connection.commit()
    connection.close()


# Initialize all tables on startup
init_database()
