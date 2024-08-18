import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import sqlite3
import os
import subprocess

# Load the face detection model
import cv2
from PIL import Image

def insert_or_update_admin(ID, Username):
    conn = sqlite3.connect("admin/database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ADMINS WHERE ID=?", (ID,))
    is_record_exist = cursor.fetchone() is not None
    
    if is_record_exist:
        cursor.execute("UPDATE ADMINS SET Username=? WHERE ID=?", (Username, ID))
    else:
        cursor.execute("INSERT INTO ADMINS (ID, Username) VALUES (?, ?)", (ID, Username))
    
    conn.commit()
    conn.close()

def start_face_detection():
    admin_id = entry_id.get()
    admin_name = entry_name.get()

    # Insert or update the admin's details in the database
    insert_or_update_admin(admin_id, admin_name)

    sample_num = 0
    cv2.namedWindow("Face Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Face Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            sample_num += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(f"admin/dataset/admin.{admin_id}.{sample_num}.jpg", face_img)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.waitKey(100)
        
        cv2.imshow("Face Detection", img)
        cv2.waitKey(1)
        
        if sample_num > 20:
            break

    cam.release()
    cv2.destroyAllWindows()

    # Call the training script after the data collection is complete
    subprocess.run(["python", "admin/trainer.py"])

    # Reset fields and show confirmation message
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    messagebox.showinfo("Info", f"Admin {admin_name} is created")

# Create the main window
root = tk.Tk()
root.title("Admin Panel")
root.geometry("300x200")

# Create and place labels and entries for Admin ID and Name
tk.Label(root, text="Admin ID:").pack(pady=5)
entry_id = tk.Entry(root)
entry_id.pack(pady=5)

tk.Label(root, text="Admin Name:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

# Create and place the button to start face detection
start_button = tk.Button(root, text="Start Face Detection", command=start_face_detection)
start_button.pack(pady=20)

# Load the face detection model
faceDetect = cv2.CascadeClassifier('admin/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)

# Run the application
root.mainloop()
