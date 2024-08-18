import os
import sqlite3

dataset_path = "students/student_dataset"

def clear_dataset(path):
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

def clear_database():
    try:
        conn = sqlite3.connect("students/sqlite.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM STUDENTS")
        conn.commit()
        print("Deleted all records from students table")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Clear the dataset and the database
clear_dataset(dataset_path)
clear_database()
