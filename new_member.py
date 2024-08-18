# import tkinter as tk
# from PIL import Image, ImageTk, ImageFilter, ImageEnhance
# import sqlite3
# import numpy as np
# from tkinter import messagebox
# import cv2
# import os
# import threading

# # Global variables to keep image references
# background_images = {}

# # Function to load and blur the background image
# def load_background_image(image_path, width, height):
#     original_image = Image.open(image_path).resize((width, height), Image.LANCZOS)
#     blurred_image = original_image.filter(ImageFilter.GaussianBlur(radius=5))
#     return original_image, ImageTk.PhotoImage(blurred_image)

# # Function to handle new member process
# def new_member_process(Id, Name, age):
#     insert_or_update(Id, Name, age)
#     create_dataset(Id)

# def insert_or_update(Id, Name, age):
#     conn = sqlite3.connect("students/sqlite.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM STUDENTS WHERE ID=?", (Id,))
#     is_record_exist = cursor.fetchone()
#     if is_record_exist:
#         cursor.execute("UPDATE STUDENTS SET Name=?, age=? WHERE ID=?", (Name, age, Id))
#     else:
#         cursor.execute("INSERT INTO STUDENTS (ID, Name, age) VALUES (?, ?, ?)", (Id, Name, age))
#     conn.commit()
#     conn.close()

# def augment_image(image):
#     enhancers = [
#         ImageEnhance.Color(image),
#         ImageEnhance.Contrast(image),
#         ImageEnhance.Brightness(image),
#         ImageEnhance.Sharpness(image)
#     ]
#     augmented_images = []
#     for enhancer in enhancers:
#         for factor in [0.8, 1.0, 1.2]:
#             augmented_images.append(enhancer.enhance(factor))
#     return augmented_images

# def get_images_with_id(path):
#     image_paths = [os.path.join(path, f) for f in os.listdir(path)]
#     faces = []
#     ids = []
#     for image_path in image_paths:
#         try:
#             face_img = Image.open(image_path).convert("L")
#             id = int(os.path.split(image_path)[-1].split(".")[1])
#             print(f"ID: {id}")
#             augmented_images = augment_image(face_img)
#             for img in augmented_images:
#                 face_np = np.array(img, np.uint8)
#                 faces.append(face_np)
#                 ids.append(id)
#         except Exception as e:
#             print(f"Error processing {image_path}: {e}")
#     return np.array(ids), faces

# def train_recognizer():
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     dataset_path = "students/student_dataset"
#     ids, faces = get_images_with_id(dataset_path)
#     recognizer.train(faces, ids)
#     recognizer.save("students/student_recognizer/trainingdata.yml")
#     messagebox.showinfo("Success", "New member added successfully.")

# def create_dataset(Id):
#     face_detect = cv2.CascadeClassifier('students/haarcascade_frontalface_default.xml')
    
#     def capture_faces():
#         cam = cv2.VideoCapture(0)
#         sample_num = 0

#         while True:
#             ret, img = cam.read()
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             faces = face_detect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

#             for (x, y, w, h) in faces:
#                 sample_num += 1
#                 cv2.imwrite(f"students/student_dataset/user.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
#                 cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#                 cv2.waitKey(100)

#             cv2.imshow("Face", img)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#             if sample_num >= 20:
#                 break
        
#         train_recognizer()

#         cam.release()
#         cv2.destroyAllWindows()

#     # Run the capture_faces function in a separate thread
#     threading.Thread(target=capture_faces).start()

# def new_member_gui(root):
#     details_dialog = tk.Toplevel(root)
#     details_dialog.title("New Member Details")
#     details_dialog.geometry("800x600")
#     details_dialog.configure(bg="#316457")

#     details_canvas = tk.Canvas(details_dialog)
#     details_canvas.pack(fill=tk.BOTH, expand=True)

#     width, height = 800, 600
#     original_details_bg_image, details_bg_image_tk = load_background_image("images/libbb.jpeg", width, height)
#     background_images["details"] = details_bg_image_tk  # Keep a reference to avoid garbage collection
#     details_bg_image_item = details_canvas.create_image(0, 0, anchor=tk.NW, image=details_bg_image_tk)

#     def resize_details_bg_image(event=None):
#         new_width = details_dialog.winfo_width()
#         new_height = details_dialog.winfo_height()
#         resized_bg_image = original_details_bg_image.resize((new_width, new_height), Image.LANCZOS)
#         resized_bg_image = resized_bg_image.filter(ImageFilter.GaussianBlur(radius=5))
#         bg_image_tk = ImageTk.PhotoImage(resized_bg_image)
#         background_images["details"] = bg_image_tk  # Keep a reference to avoid garbage collection
#         details_canvas.itemconfig(details_bg_image_item, image=bg_image_tk)
#         details_canvas.config(width=new_width, height=new_height)
#         details_canvas.coords(details_bg_image_item, 0, 0)

#     details_dialog.bind('<Configure>', resize_details_bg_image)

#     details_frame = tk.Frame(details_canvas, bg="#316457", highlightthickness=2)
#     details_canvas.create_window(400, 300, window=details_frame, anchor=tk.CENTER)

#     tk.Label(details_frame, text="User ID:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=0, column=0, padx=10, pady=13, sticky=tk.W)
#     tk.Label(details_frame, text="Name:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
#     tk.Label(details_frame, text="Age:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

#     id_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")
#     name_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")
#     age_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")

#     id_entry.grid(row=0, column=1, padx=10, pady=10)
#     name_entry.grid(row=1, column=1, padx=10, pady=10)
#     age_entry.grid(row=2, column=1, padx=10, pady=10)

#     def on_submit():
#         Id = id_entry.get()
#         Name = name_entry.get()
#         age = age_entry.get()
#         if Id and Name and age:
#             details_dialog.destroy()
#             new_member_process(Id, Name, age)
#         else:
#             messagebox.showerror("Error", "All fields are required.")

#     tk.Button(details_frame, text="Submit", font=("Comic Sans MS", 20), command=on_submit, bg="#4CAF50", fg="black", bd=2, relief="solid", width=10).grid(row=3, column=0, columnspan=2, padx=20, pady=20)

#     # Manually call resize function to adjust the background image initially
#     resize_details_bg_image()

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()
#     new_member_gui(root)
#     root.mainloop()




# import tkinter as tk
# from PIL import Image, ImageTk, ImageFilter, ImageEnhance
# import sqlite3
# import numpy as np
# from tkinter import messagebox
# import cv2
# import os
# import threading

# # Global variables to keep image references
# background_images = {}

# # Function to load and blur the background image
# def load_background_image(image_path, width, height):
#     original_image = Image.open(image_path).resize((width, height), Image.LANCZOS)
#     blurred_image = original_image.filter(ImageFilter.GaussianBlur(radius=5))
#     return original_image, ImageTk.PhotoImage(blurred_image)

# # Function to handle new member process
# def new_member_process(Id, Name, age):
#     insert_or_update(Id, Name, age)
#     create_dataset(Id)

# def insert_or_update(Id, Name, age):
#     conn = sqlite3.connect("students/sqlite.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM STUDENTS WHERE ID=?", (Id,))
#     is_record_exist = cursor.fetchone()
#     if is_record_exist:
#         cursor.execute("UPDATE STUDENTS SET Name=?, age=? WHERE ID=?", (Name, age, Id))
#     else:
#         cursor.execute("INSERT INTO STUDENTS (ID, Name, age) VALUES (?, ?, ?)", (Id, Name, age))
#     conn.commit()
#     conn.close()

# def augment_image(image):
#     enhancers = [
#         ImageEnhance.Color(image),
#         ImageEnhance.Contrast(image),
#         ImageEnhance.Brightness(image),
#         ImageEnhance.Sharpness(image)
#     ]
#     augmented_images = []
#     for enhancer in enhancers:
#         for factor in [0.8, 1.0, 1.2]:
#             augmented_images.append(enhancer.enhance(factor))
#     return augmented_images

# def get_images_with_id(path):
#     image_paths = [os.path.join(path, f) for f in os.listdir(path)]
#     faces = []
#     ids = []
#     for image_path in image_paths:
#         try:
#             face_img = Image.open(image_path).convert("L")
#             id = int(os.path.split(image_path)[-1].split(".")[1])
#             print(f"ID: {id}")
#             augmented_images = augment_image(face_img)
#             for img in augmented_images:
#                 face_np = np.array(img, np.uint8)
#                 faces.append(face_np)
#                 ids.append(id)
#         except Exception as e:
#             print(f"Error processing {image_path}: {e}")
#     return np.array(ids), faces

# def train_recognizer():
#     try:
#         recognizer = cv2.face.LBPHFaceRecognizer_create()
#         dataset_path = "students/student_dataset"
#         ids, faces = get_images_with_id(dataset_path)
#         recognizer.train(faces, ids)
#         recognizer.save("students/student_recognizer/trainingdata.yml")
#         messagebox.showinfo("Success", "New member added successfully.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to train recognizer: {e}")

# def create_dataset(Id):
#     face_detect = cv2.CascadeClassifier('students/haarcascade_frontalface_default.xml')

#     def capture_faces():
#         cam = cv2.VideoCapture(0)
#         sample_num = 0

#         while True:
#             ret, img = cam.read()
#             if not ret:
#                 break
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             faces = face_detect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

#             for (x, y, w, h) in faces:
#                 sample_num += 1
#                 cv2.imwrite(f"students/student_dataset/user.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
#                 cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#                 cv2.waitKey(100)

#             cv2.imshow("Face", img)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#             if sample_num >= 20:
#                 break
        
#         cam.release()
#         cv2.destroyAllWindows()

#         # Call the train_recognizer function in a separate thread
#         threading.Thread(target=train_recognizer).start()

#     # Run the capture_faces function in a separate thread
#     threading.Thread(target=capture_faces).start()

# def new_member_gui(root):
#     details_dialog = tk.Toplevel(root)
#     details_dialog.title("New Member Details")
#     details_dialog.geometry("800x600")
#     details_dialog.configure(bg="#316457")

#     details_canvas = tk.Canvas(details_dialog)
#     details_canvas.pack(fill=tk.BOTH, expand=True)

#     width, height = 800, 600
#     original_details_bg_image, details_bg_image_tk = load_background_image("images/libbb.jpeg", width, height)
#     background_images["details"] = details_bg_image_tk  # Keep a reference to avoid garbage collection
#     details_bg_image_item = details_canvas.create_image(0, 0, anchor=tk.NW, image=details_bg_image_tk)

#     def resize_details_bg_image(event=None):
#         new_width = details_dialog.winfo_width()
#         new_height = details_dialog.winfo_height()
#         resized_bg_image = original_details_bg_image.resize((new_width, new_height), Image.LANCZOS)
#         resized_bg_image = resized_bg_image.filter(ImageFilter.GaussianBlur(radius=5))
#         bg_image_tk = ImageTk.PhotoImage(resized_bg_image)
#         background_images["details"] = bg_image_tk  # Keep a reference to avoid garbage collection
#         details_canvas.itemconfig(details_bg_image_item, image=bg_image_tk)
#         details_canvas.config(width=new_width, height=new_height)
#         details_canvas.coords(details_bg_image_item, 0, 0)

#     details_dialog.bind('<Configure>', resize_details_bg_image)

#     details_frame = tk.Frame(details_canvas, bg="#316457", highlightthickness=2)
#     details_canvas.create_window(400, 300, window=details_frame, anchor=tk.CENTER)

#     tk.Label(details_frame, text="User ID:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=0, column=0, padx=10, pady=13, sticky=tk.W)
#     tk.Label(details_frame, text="Name:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
#     tk.Label(details_frame, text="Age:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

#     id_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")
#     name_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")
#     age_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")

#     id_entry.grid(row=0, column=1, padx=10, pady=10)
#     name_entry.grid(row=1, column=1, padx=10, pady=10)
#     age_entry.grid(row=2, column=1, padx=10, pady=10)

#     def on_submit():
#         Id = id_entry.get()
#         Name = name_entry.get()
#         age = age_entry.get()
#         if Id and Name and age:
#             details_dialog.destroy()
#             new_member_process(Id, Name, age)
#         else:
#             messagebox.showerror("Error", "All fields are required.")

#     tk.Button(details_frame, text="Submit", font=("Comic Sans MS", 20), command=on_submit, bg="#4CAF50", fg="black", bd=2, relief="solid", width=10).grid(row=3, column=0, columnspan=2, padx=20, pady=20)

#     # Manually call resize function to adjust the background image initially
#     resize_details_bg_image()

# if __name__ == "__main__":
#     root = tk.Tk()
#     root.withdraw()
#     new_member_gui(root)
#     root.mainloop()











import tkinter as tk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
import sqlite3
import numpy as np
from tkinter import messagebox
import cv2
import os
import threading

# Global variables to keep image references
background_images = {}

# Function to load and blur the background image
def load_background_image(image_path, width, height):
    original_image = Image.open(image_path).resize((width, height), Image.LANCZOS)
    blurred_image = original_image.filter(ImageFilter.GaussianBlur(radius=5))
    return original_image, ImageTk.PhotoImage(blurred_image)

# Function to handle new member process
def new_member_process(Id, Name, age):
    insert_or_update(Id, Name, age)
    create_dataset(Id)

def insert_or_update(Id, Name, age):
    conn = sqlite3.connect("students/sqlite.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM STUDENTS WHERE ID=?", (Id,))
    is_record_exist = cursor.fetchone()
    if is_record_exist:
        cursor.execute("UPDATE STUDENTS SET Name=?, age=? WHERE ID=?", (Name, age, Id))
    else:
        cursor.execute("INSERT INTO STUDENTS (ID, Name, age) VALUES (?, ?, ?)", (Id, Name, age))
    conn.commit()
    conn.close()

def augment_image(image):
    enhancers = [
        ImageEnhance.Color(image),
        ImageEnhance.Contrast(image),
        ImageEnhance.Brightness(image),
        ImageEnhance.Sharpness(image)
    ]
    augmented_images = []
    for enhancer in enhancers:
        for factor in [0.8, 1.0, 1.2]:
            augmented_images.append(enhancer.enhance(factor))
    return augmented_images

def get_images_with_id(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    ids = []
    for image_path in image_paths:
        try:
            face_img = Image.open(image_path).convert("L")
            id = int(os.path.split(image_path)[-1].split(".")[1])
            print(f"ID: {id}")
            augmented_images = augment_image(face_img)
            for img in augmented_images:
                face_np = np.array(img, np.uint8)
                faces.append(face_np)
                ids.append(id)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
    return np.array(ids), faces

def train_recognizer():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        dataset_path = "students/student_dataset"
        ids, faces = get_images_with_id(dataset_path)

        # Log the data types and shapes
        print(f"IDs type: {type(ids)}, IDs shape: {ids.shape}")
        print(f"Faces type: {type(faces)}, number of faces: {len(faces)}")
        
        # Ensure faces and ids are in the correct format
        if len(faces) == 0 or len(ids) == 0:
            raise ValueError("No faces or IDs found for training.")
        
        # Convert faces to the correct format for training
        faces_np = [np.array(face, np.uint8) for face in faces]
        ids_np = np.array(ids, np.int32)

        # Log after conversion
        print(f"Converted Faces type: {type(faces_np)}, number of converted faces: {len(faces_np)}")
        print(f"Converted IDs type: {type(ids_np)}, IDs shape: {ids_np.shape}")

        recognizer.train(faces_np, ids_np)
        recognizer.save("students/student_recognizer/trainingdata.yml")
        messagebox.showinfo("Success", "New member added successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to train recognizer: {e}")
        # Additional print statement for debugging
        print(f"Exception: {e}")


def create_dataset(Id):
    face_detect = cv2.CascadeClassifier('students/haarcascade_frontalface_default.xml')

    def capture_faces():
        cam = cv2.VideoCapture(0)
        sample_num = 0

        while True:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                sample_num += 1
                cv2.imwrite(f"students/student_dataset/user.{Id}.{sample_num}.jpg", gray[y:y+h, x:x+w])
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.waitKey(100)

            cv2.imshow("Face", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if sample_num >= 20:
                break
        
        cam.release()
        cv2.destroyAllWindows()

        # Call the train_recognizer function in a separate thread
        threading.Thread(target=train_recognizer).start()

    # Run the capture_faces function in a separate thread
    threading.Thread(target=capture_faces).start()

def new_member_gui():
    details_dialog = tk.Toplevel()
    details_dialog.title("New Member Details")
    details_dialog.geometry("800x600")
    details_dialog.configure(bg="#316457")

    details_canvas = tk.Canvas(details_dialog)
    details_canvas.pack(fill=tk.BOTH, expand=True)

    width, height = 800, 600
    original_details_bg_image, details_bg_image_tk = load_background_image("images/libbb.jpeg", width, height)
    background_images["details"] = details_bg_image_tk  # Keep a reference to avoid garbage collection
    details_bg_image_item = details_canvas.create_image(0, 0, anchor=tk.NW, image=details_bg_image_tk)

    def resize_details_bg_image(event=None):
        new_width = details_dialog.winfo_width()
        new_height = details_dialog.winfo_height()
        resized_bg_image = original_details_bg_image.resize((new_width, new_height), Image.LANCZOS)
        resized_bg_image = resized_bg_image.filter(ImageFilter.GaussianBlur(radius=5))
        bg_image_tk = ImageTk.PhotoImage(resized_bg_image)
        background_images["details"] = bg_image_tk  # Keep a reference to avoid garbage collection
        details_canvas.itemconfig(details_bg_image_item, image=bg_image_tk)
        details_canvas.config(width=new_width, height=new_height)
        details_canvas.coords(details_bg_image_item, 0, 0)

    details_dialog.bind('<Configure>', resize_details_bg_image)

    details_frame = tk.Frame(details_canvas, bg="#316457", highlightthickness=2)
    details_canvas.create_window(400, 300, window=details_frame, anchor=tk.CENTER)

    tk.Label(details_frame, text="User ID:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=0, column=0, padx=10, pady=13, sticky=tk.W)
    tk.Label(details_frame, text="Name:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Label(details_frame, text="Age:", bg="#316457", font=("Comic Sans MS", 20)).grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

    id_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")
    name_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")
    age_entry = tk.Entry(details_frame, font=("Comic Sans MS", 20), width=20, fg="black", bg="white")

    id_entry.grid(row=0, column=1, padx=10, pady=10)
    name_entry.grid(row=1, column=1, padx=10, pady=10)
    age_entry.grid(row=2, column=1, padx=10, pady=10)

    def on_submit():
        Id = id_entry.get()
        Name = name_entry.get()
        age = age_entry.get()
        if Id and Name and age:
            details_dialog.destroy()
            new_member_process(Id, Name, age)
        else:
            messagebox.showerror("Error", "All fields are required.")

    tk.Button(details_frame, text="Submit", font=("Comic Sans MS", 20), command=on_submit, bg="#4CAF50", fg="black", bd=2, relief="solid", width=10).grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    # Manually call resize function to adjust the background image initially
    resize_details_bg_image()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    new_member_gui()
    root.mainloop()
