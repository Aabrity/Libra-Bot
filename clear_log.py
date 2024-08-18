import sqlite3

def clear_access_log():
    """Clear all data from the ACCESS_LOG table."""
    try:
        conn = sqlite3.connect("database.db")
        conn.execute("DELETE FROM ACCESS_LOG")
        conn.commit()
        print("Access log cleared successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while clearing the access log: {e}")
    finally:
        conn.close()

clear_access_log()