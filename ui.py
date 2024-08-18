import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import sqlite3
import pandas as pd
import os
import subprocess

# Function to prompt for the main admin code
def prompt_admin_code():
    admin_code = simpledialog.askstring("Admin Code", "Enter main admin code:", show='*')
    return admin_code

# Function to verify the admin code
def verify_admin_code(admin_code):
    main_admin_code = "12345"  # Replace with your actual main admin code
    return admin_code == main_admin_code

# Function to add a book
def add_book():
    messagebox.showinfo("Be ready!", "Ready to detect admins face!")
    subprocess.run(["python", "detect1.py"])

# Function to create a new admin
def create_admin():
    admin_code = prompt_admin_code()
    if verify_admin_code(admin_code):
        messagebox.showinfo("Info", "Admin code verified. Create Admin button clicked")
        subprocess.run(["python", "dataset_creater2.py"])
    else:
        messagebox.showerror("Error", "Invalid admin code")

# Function to manage existing admins
def manage_admin():
    admin_code = prompt_admin_code()
    if verify_admin_code(admin_code):
        open_manage_admin_ui()
    else:
        messagebox.showerror("Error", "Invalid admin code")

# Function to open the manage admin UI
def open_manage_admin_ui():
    manage_admin_window = tk.Toplevel()
    manage_admin_window.title("Manage Admins")
    manage_admin_window.geometry("800x600")
    manage_admin_window.grab_set()  # Make the new window modal

    # Label for existing admins
    label = tk.Label(manage_admin_window, text="EXISTING ADMINS", font=("Arial", 16))
    label.pack(pady=10)

    # Load data from database and create a DataFrame
    conn = sqlite3.connect('database.db')
    query = 'SELECT ID, Username FROM ADMINS'  # Excluding the email and password columns
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Display DataFrame in the UI
    table_frame = tk.Frame(manage_admin_window)
    table_frame.pack(fill=tk.BOTH, expand=True)

    def refresh_table():
        for widget in table_frame.winfo_children():
            widget.destroy()

        conn = sqlite3.connect('database.db')
        query = 'SELECT ID, Username FROM ADMINS'  # Excluding the email and password columns
        df = pd.read_sql_query(query, conn)
        conn.close()

        if not df.empty:
            tree = ttk.Treeview(table_frame, columns=df.columns.tolist(), show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            # Define column headings and add to treeview
            for column in df.columns:
                tree.heading(column, text=column)
                tree.column(column, width=100, anchor=tk.CENTER)

            # Add data to treeview
            for _, row in df.iterrows():
                tree.insert("", tk.END, values=row.tolist())

            # Add delete button
            def delete_row():
                selected_item = tree.selection()[0]
                row_id = tree.item(selected_item)['values'][0]
                conn = sqlite3.connect('database.db')
                conn.execute('DELETE FROM ADMINS WHERE ID=?', (row_id,))
                conn.commit()
                conn.close()

                # Delete associated image files
                for file in os.listdir('dataset'):
                    if file.startswith(f"admin.{row_id}."):
                        os.remove(os.path.join('dataset', file))

                tree.delete(selected_item)
                messagebox.showinfo("Info", f"Admin with ID {row_id} has been deleted")

            delete_button = tk.Button(manage_admin_window, text="Delete", command=delete_row)
            delete_button.pack(pady=10)

            # Style the treeview for borders
            style = ttk.Style()
            style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
            style.configure("Treeview", rowheight=25, bordercolor='black', borderwidth=1)
            style.map("Treeview", background=[('selected', 'blue')])

    refresh_table()

# Create the main window
root = tk.Tk()
root.title("Admin Panel")
root.geometry("300x200")

# Create and place buttons
add_book_button = tk.Button(root, text="Add Book", command=add_book)
add_book_button.pack(pady=10)

create_admin_button = tk.Button(root, text="Create Admin", command=create_admin)
create_admin_button.pack(pady=10)

manage_admin_button = tk.Button(root, text="Manage Admin", command=manage_admin)
manage_admin_button.pack(pady=10)

# Run the application
root.mainloop()
