"""
Student Management System - Database Operations
Handles SQLite database connection, table initialization, and queries.
"""
import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'student_account.db')


def init_database():
    """Initializes the SQLite database and creates the data table if needed."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
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
    cursor.execute("SELECT * FROM data WHERE id_number = ? AND password = ?", (id_number, password))
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
