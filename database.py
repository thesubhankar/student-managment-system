import sqlite3
import os

def init_database():
    if os.path.exists('student_account.db'):
        pass
    else:
        connection = sqlite3.connect('student_account.db')
        
        cursor = connection.cursor()
        
        cursor.execute("""
            create table data (
                id_number text,
                password text,
                name text,
                age text,
                gender text,
                phone_number text,
                class text,
                email text,
                image blob
            )
                     
            """)
        
        
        
        connection.commit()
        connection.close
init_database()