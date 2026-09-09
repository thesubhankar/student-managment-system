import sqlite3
import os

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, 'student_account.db')


def init_database():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id_number TEXT PRIMARY KEY,
            password TEXT,
            name TEXT,
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


def add_data(id_number, password, name, age, gender, 
             phone_number, student_class, email, pic_data):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO data (id_number, password, name, age, gender, phone_number, class, email, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_number, password, name, age, gender, phone_number, student_class, email, pic_data))
    connection.commit()
    connection.close()


def check_student_login(id_number, password):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM data WHERE id_number = ? AND password = ?", (id_number, password))
    user = cursor.fetchone()
    connection.close()
    return user
