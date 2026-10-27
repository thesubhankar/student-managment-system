"""
Student Management System - Database Operations
Handles SQLite database connection, table initialization, and queries.
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
    """, (id_number, password, name, age, gender, phone_number, student_class, email, pic_data))
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
    """Retrieves all students from database ordered by ID."""
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
        """, (name, age, gender, phone_number, student_class, email, pic_data, str(id_number)))
    else:
        cursor.execute("""
            UPDATE data 
            SET name = ?, age = ?, gender = ?, phone_number = ?, class = ?, email = ?
            WHERE id_number = ?
        """, (name, age, gender, phone_number, student_class, email, str(id_number)))
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
    """Deletes a student record permanently."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM data WHERE id_number = ?", (str(id_number),))
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
    cursor.execute("SELECT id_number, name FROM data WHERE id_number = ? AND LOWER(email) = ?", (str(id_number).strip(), email.strip().lower()))
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
