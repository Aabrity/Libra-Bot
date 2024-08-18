# import os
# os.environ['TK_SILENCE_DEPRECATION'] = '1'

# import sqlite3
# import time
# import time as time_lib
# import tkinter as tk
# from datetime import datetime
# from tkinter import ttk
# import cv2
# import numpy as np
# import pandas as pd
# import pyttsx3
# import requests
# import speech_recognition as sr
# from PIL import Image, ImageDraw, ImageFilter, ImageTk
# from pyzbar.pyzbar import decode
# import main
# import atexit

# def run_camera_on_exit():
#     main.run_camera()

# # Register the run_camera_on_exit function to be called upon script exit
# atexit.register(run_camera_on_exit)

# # Initialize the text-to-speech engine
# engine = pyttsx3.init()

# # Variable to control if the bot should speak or not
# should_speak = False

# import os
# import threading
# import sqlite3
# import time
# import tkinter as tk
# from datetime import datetime
# from tkinter import ttk
# import cv2
# import numpy as np
# import pandas as pd
# import pyttsx3
# import requests
# import speech_recognition as sr
# from PIL import Image, ImageDraw, ImageFilter, ImageTk
# from pyzbar.pyzbar import decode
# import main
# import atexit

# def run_camera_on_exit():
#     main.run_camera()

# atexit.register(run_camera_on_exit)

# engine = pyttsx3.init()
# should_speak = False

# # Function to get the bot's response from the Rasa server
# def get_bot_response(user_input):
#     global should_speak
#     url = "http://localhost:5005/webhooks/rest/webhook"
#     payload = {
#         "sender": "user",
#         "message": user_input
#     }
#     headers = {'Content-Type': 'application/json'}
    
#     try:
#         response = requests.post(url, json=payload, headers=headers)
#         response.raise_for_status()
#         for res in response.json():
#             bot_message = res.get("text", "")
#             simulate_typing(bot_message)
#             if should_speak:
#                 engine.say(bot_message)
#                 engine.runAndWait()
#     except requests.RequestException as e:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, f"Request error: {e}\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#     except Exception as e:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, f"An unexpected error occurred: {e}\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)

# def handle_user_input(event=None):
#     user_input = chat_entry.get()
#     if user_input.strip() == "" or user_input == "Start conversation":
#         return
#     chat_display.config(state=tk.NORMAL)
#     chat_display.insert(tk.END, f"You: {user_input}\n", 'user')
#     chat_display.config(state=tk.DISABLED)
#     chat_entry.delete(0, tk.END)
    
#     # Start a new thread to handle the bot response
#     threading.Thread(target=get_bot_response, args=(user_input,), daemon=True).start()

# def handle_mic_input(event=None):
#     global should_speak
#     should_speak = True
    
#     chat_display.config(state=tk.NORMAL)
#     chat_display.insert(tk.END, "Speak now...\n", 'bot')
#     chat_display.config(state=tk.DISABLED)
#     chat_display.see(tk.END)
#     chat_display.update_idletasks()
    
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as mic:
#         recognizer.adjust_for_ambient_noise(mic, duration=0.2)
#         audio = recognizer.listen(mic)
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "Processing audio...\n", 'bot')
#         chat_display.config(state=tk.DISABLED)
#         try:
#             text = recognizer.recognize_google(audio)
#             text = text.lower()
#             chat_display.config(state=tk.NORMAL)
#             chat_display.insert(tk.END, f"Recognized: {text}\n", 'user')
#             chat_display.config(state=tk.DISABLED)
            
#             # Start a new thread to handle the bot response
#             threading.Thread(target=get_bot_response, args=(text,), daemon=True).start()
#         except sr.UnknownValueError:
#             chat_display.config(state=tk.NORMAL)
#             chat_display.insert(tk.END, "Could not understand audio. Please try again.\n", 'bot_error')
#             chat_display.config(state=tk.DISABLED)
#         except Exception as e:
#             chat_display.config(state=tk.NORMAL)
#             chat_display.insert(tk.END, f"An error occurred: {e}\n", 'bot_error')
#             chat_display.config(state=tk.DISABLED)
#     should_speak = False


# # Function to simulate typing effect
# def simulate_typing(message):
#     typing_speed = 0.03  # Adjust the typing speed as needed
#     chat_display.config(state=tk.NORMAL)
#     chat_display.insert(tk.END, "Bot: ", 'bot')
#     for char in message:
#         chat_display.insert(tk.END, char, 'bot')
#         chat_display.see(tk.END)  # Scroll to the end of the text widget
#         chat_display.update_idletasks()  # Update the display
#         time.sleep(typing_speed)  # End with a newline for the next input prompt
#     chat_display.insert(tk.END, "\n\n")
#     chat_display.config(state=tk.DISABLED)


# # Function to capture ISBN from camera using OpenCV and pyzbar
# def capture_isbn_from_camera():
#     cap = cv2.VideoCapture(0)  # 0 is the default camera
#     isbn = None

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         barcodes = decode(frame)
#         for barcode in barcodes:
#             barcode_data = barcode.data.decode("utf-8")
#             print(f"Detected barcode data: {barcode_data}")

#             if len(barcode_data) == 13 and barcode_data.isdigit():
#                 isbn = barcode_data
#                 break

#         if isbn:
#             break

#         cv2.imshow('Barcode Scanner', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return isbn

# # Function to get student profile from SQLite database
# def get_student_profile(id):
#     """Retrieve student profile from the SQLite database."""
#     try:
#         conn = sqlite3.connect("students/sqlite.db")
#         cursor = conn.execute("SELECT * FROM STUDENTS WHERE ID=?", (id,))
#         profile = cursor.fetchone()
#     except sqlite3.Error as e:
#         print(f"An error occurred: {e}")
#         profile = None
#     finally:
#         conn.close()
#     return profile

# # Function to get book title from Excel file
# def get_book_title(isbn, excel_path='rasa_bot/actions/Books.xlsx'):
#     """Retrieve book title from the Excel file using ISBN."""
#     try:
#         df = pd.read_excel(excel_path, dtype={'ISBN': str})
#         book_info = df[df['ISBN'] == isbn]
#         if not book_info.empty:
#             title = book_info.iloc[0]['Title']
#         else:
#             title = None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         title = None
#     return title

# # Function to log check-in or check-out in Excel file
# def log_checkin_checkout(student_id, student_name, isbn, title, action, excel_path):
#     try:
#         # Read the existing Excel file
#         df = pd.read_excel(excel_path, dtype={'ISBN': str})

#         # Create a new DataFrame for the new log entry
#         new_entry = pd.DataFrame([{
#             'Student ID': student_id,
#             'Student Name': student_name,
#             'ISBN': str(isbn),  # Ensure ISBN is stored as a string
#             'Title': title,
#             'Action': action,
#             'Date': datetime.now().strftime("%Y-%m-%d")  # Date only, no time
#         }])

#         # Concatenate the existing DataFrame with the new entry
#         df = pd.concat([df, new_entry], ignore_index=True)

#         # Write the updated DataFrame back to the Excel file
#         df.to_excel(excel_path, index=False)
#         print("Data added successfully.")
#     except Exception as e:
#         print(f"An error occurred while logging check-in/check-out: {e}")

# # Function to check if a book is checked out and by whom
# def get_checkout_details(isbn, excel_path='students/students_data.xlsx'):
#     try:
#         df = pd.read_excel(excel_path, dtype={'ISBN': str})
#         checkout_info = df[(df['ISBN'] == isbn) & (df['Action'] == 'Check-Out')]
#         if not checkout_info.empty:
#             last_checkout = checkout_info.iloc[-1]
#             return last_checkout['Student ID'], last_checkout['Student Name']
#         else:
#             return None, None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None, None

# # Function to update book quantity and availability
# def update_book_quantity_and_availability(isbn, change):
#     try:
#         df = pd.read_excel('rasa_bot/actions/Books.xlsx', dtype={'ISBN': str})

#         # Find the book in the DataFrame
#         book_info = df[df['ISBN'] == isbn]

#         if not book_info.empty:
#             # Update the Quantity
#             df.loc[df['ISBN'] == isbn, 'Quantity'] += change

#             # Update the Availability
#             if df.loc[df['ISBN'] == isbn, 'Quantity'].values[0] <= 0:
#                 df.loc[df['ISBN'] == isbn, 'Availability'] = 'Unavailable'
#             else:
#                 df.loc[df['ISBN'] == isbn, 'Availability'] = 'Available'

#             # Write the updated DataFrame back to the Excel file
#             df.to_excel('rasa_bot/actions/Books.xlsx', index=False)
#             print("Book quantity and availability updated successfully.")
#         else:
#             print("Book not found in the database.")
#     except Exception as e:
#         print(f"An error occurred while updating book quantity and availability: {e}")

# # Function to capture face and get student ID
# def capture_face_and_get_student():
#     face_detect = cv2.CascadeClassifier('students/haarcascade_frontalface_default.xml')
#     recognizer = cv2.face.LBPHFaceRecognizer_create()
#     recognizer.read('students/student_recognizer/trainingdata.yml')
#     cam = cv2.VideoCapture(0)
#     student_id = None
#     student_name = None
#     face_detected_time = None  # Variable to store the time when the face is first detected
#     run_duration = 5  # Number of seconds to run the loop after face detection

#     while True:
#         ret, img = cam.read()
#         if not ret:
#             break
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         faces = face_detect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

#         for (x, y, w, h) in faces:
#             id, conf = recognizer.predict(gray[y:y+h, x:x+w])
#             if conf < 70:
#                 profile = get_student_profile(id)
#                 if profile:
#                     student_id = profile[0]
#                     student_name = profile[1]
#                     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#                     cv2.putText(img, student_name, (x, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

#                     if face_detected_time is None:
#                         face_detected_time = time_lib.time()  # Record the time when face was first detected

#         cv2.imshow("Face", img)

#         if face_detected_time is not None and (time_lib.time() - face_detected_time) >= run_duration:
#             # If the specified duration has passed since face detection, break the loop
#             break

#         if cv2.waitKey(1) == 13:  # 13 is the Enter key
#             break

#     cam.release()
#     cv2.destroyAllWindows()
#     return student_id, student_name

# # Function to check-in a book
# def check_in():
#     # Capture face and get student details
#     student_id, student_name = capture_face_and_get_student()
#     if not student_id or not student_name:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "Student not recognized.\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#         return

#     # Capture ISBN from camera
#     isbn = capture_isbn_from_camera()
#     if not isbn:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "ISBN not captured.\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#         return

#     # Get the title of the book from the database
#     title = get_book_title(isbn)
#     if not title:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "Book title not found.\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#         return

#     # Verify if the book was checked out by the same student
#     checkout_student_id, checkout_student_name = get_checkout_details(isbn)
#     if checkout_student_id != student_id:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "This book was not checked out by you.\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#         return

#     # Log the check-in
#     log_checkin_checkout(student_id, student_name, isbn, title, "Check-In", "students/students_data.xlsx")
#     # Update book quantity and availability
#     update_book_quantity_and_availability(isbn, 1)

#     # Display the result in the chat_display
#     message = f"Check-in completed for {student_name} (ID: {student_id}) with Book Title: {title}.\n"
#     chat_display.config(state=tk.NORMAL)
#     chat_display.insert(tk.END, message, 'bot')
#     chat_display.config(state=tk.DISABLED)
#     chat_display.see(tk.END)  # Scroll to the end of the text widget

# # Function to check-out a book
# def check_out():
#     # Capture face and get student details
#     student_id, student_name = capture_face_and_get_student()
#     if not student_id or not student_name:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "Student not recognized.\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#         return

#     # Capture ISBN from camera
#     isbn = capture_isbn_from_camera()
#     if not isbn:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "ISBN not captured.\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#         return

#     # Get the title of the book from the database
#     title = get_book_title(isbn)
#     if not title:
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "Book title not found.\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#         return

#     # Check book availability
#     df = pd.read_excel('rasa_bot/actions/Books.xlsx', dtype={'ISBN': str})
#     book_info = df[df['ISBN'] == isbn]
#     if book_info.empty or book_info.iloc[0]['Availability'] == 'Unavailable':
#         chat_display.config(state=tk.NORMAL)
#         chat_display.insert(tk.END, "The book is currently unavailable.\n", 'bot_error')
#         chat_display.config(state=tk.DISABLED)
#         return

#     # Log the check-out
#     log_checkin_checkout(student_id, student_name, isbn, title, "Check-Out", "students/students_data.xlsx")
#     # Update book quantity and availability
#     update_book_quantity_and_availability(isbn, -1)

#     # Display the result in the chat_display
#     message = f"Check-out completed for {student_name} (ID: {student_id}) with Book Title: {title}.\n"
#     chat_display.config(state=tk.NORMAL)
#     chat_display.insert(tk.END, message, 'bot')
#     chat_display.config(state=tk.DISABLED)
#     chat_display.see(tk.END)  # Scroll to the end of the text widget


# # Function to handle placeholder text in chat entry
# def add_placeholder(event):
#     if chat_entry.get() == "":
#         chat_entry.insert(0, "Start conversation")
#         chat_entry.config(foreground='grey')

# def remove_placeholder(event):
#     if chat_entry.get() == "Start conversation":
#         chat_entry.delete(0, tk.END)
#         chat_entry.config(foreground='black')

# # Create the main window
# root = tk.Tk()
# root.title("LIBBOT")
# root.geometry("1500x700")
# root.state('zoomed')

# # Create a canvas for the background image and overlay image
# canvas_bg = tk.Canvas(root)
# canvas_bg.pack(fill=tk.BOTH, expand=True)  # Ensure canvas fills the window

# # Load and process the background image
# original_bg_image = Image.open("images/libbb.jpeg")

# # Function to resize background image and update other image positions
# def resize_bg_image(event=None):
#     new_width = root.winfo_width()
#     new_height = root.winfo_height()
    
#     resized_bg_image = original_bg_image.resize((new_width, new_height), Image.LANCZOS)
#     resized_bg_image = resized_bg_image.filter(ImageFilter.GaussianBlur(radius=5))
#     bg_image_tk = ImageTk.PhotoImage(resized_bg_image)
#     canvas_bg.itemconfig(background_image_item, image=bg_image_tk)
#     canvas_bg.image = bg_image_tk

#     # Reposition book image
#     book_image_x = new_width - book_image_size - 70  # Position it 20 pixels from the right edge
#     book_image_y = new_height - book_image_size - 290  # Position it 20 pixels from the bottom edge
#     canvas_bg.coords(book_image_item, book_image_x, book_image_y)

#     # Update position of robo image
#     chat_frame_x = chat_frame.winfo_x()
#     chat_frame_y = chat_frame.winfo_y()
#     robo_image_x_shift = -200  # Shift the image further to the left
#     robo_image_y_shift = 100   # Shift the image downwards
#     canvas_bg.coords(robo_image_item, chat_frame_x + robo_image_x_shift, chat_frame_y - robo_image_size[1] + robo_image_y_shift)  # Shifted x and y coordinates

# # Load and display the background image initially
# bg_image_tk = ImageTk.PhotoImage(original_bg_image)
# background_image_item = canvas_bg.create_image(0, 0, anchor=tk.NW, image=bg_image_tk)

# # Create and process the book image
# book_image_original = Image.open("images/book.png").convert("RGBA")
# book_image_size = 100  # Fixed size
# book_image_resized = book_image_original.resize((book_image_size, book_image_size), Image.LANCZOS)
# book_image_tk = ImageTk.PhotoImage(book_image_resized)

# # Create and process the book image item on the canvas
# book_image_item = canvas_bg.create_image(0, 0, anchor=tk.CENTER, image=book_image_tk)
# canvas_bg.image = book_image_tk

# # Load and process the robo image
# robo_image = Image.open("images/robo.png").convert("RGBA")
# robo_image_size = (575, 300)  # Set the size of the robo image
# robo_image_resized = robo_image.resize(robo_image_size, Image.LANCZOS)
# robo_image_tk = ImageTk.PhotoImage(robo_image_resized)

# # Create and process the robo image item on the canvas
# robo_image_item = canvas_bg.create_image(0, 0, anchor=tk.NW, image=robo_image_tk)

# # Create a frame for the chatbot interface with a semi-transparent background
# chat_frame = tk.Frame(root, bg='black', bd=5)
# chat_frame.place(relx=0.4, rely=0.54, anchor=tk.CENTER, relwidth=0.75, relheight=0.70)  # Use relative positioning

# # Create a grid configuration for chat display and input area
# chat_display = tk.Text(chat_frame, wrap=tk.WORD, bg='white', fg='#000000', font=('Comic Sans MS', 19), padx=10, pady=10)
# chat_display.grid(row=0, column=0, columnspan=3, sticky='nsew')
# chat_display.config(state=tk.DISABLED)

# chat_display.tag_config('user', foreground='black', font=('Comic Sans MS', 20, 'bold'))
# chat_display.tag_config('bot', foreground='green', font=('Courier', 20, 'normal'))
# chat_display.tag_config('bot_error', foreground='red', font=('Comic Sans MS', 20, 'bold'))

# chat_entry = ttk.Entry(chat_frame, font=('Comic Sans MS', 20), foreground='grey')
# chat_entry.insert(0, "Start conversation")
# chat_entry.bind("<FocusIn>", remove_placeholder)
# chat_entry.bind("<FocusOut>", add_placeholder)
# chat_entry.grid(row=1, column=0, sticky='ew')
# chat_entry.bind("<Return>", handle_user_input)

# # Load and resize the send icon
# send_image = Image.open("images/sub.webp").convert("RGBA")
# send_image = send_image.resize((50, 50), Image.LANCZOS)
# send_icon = ImageTk.PhotoImage(send_image)

# send_button = tk.Label(chat_frame, image=send_icon, bd=0, bg='black')
# send_button.bind("<Button-1>", handle_user_input)
# send_button.grid(row=1, column=1, padx=5)

# # Load and resize the microphone icon
# mic_image = Image.open("images/micc.png").convert("RGBA")
# size = (50, 50)  # Adjust the size of the circular image
# mic_image = mic_image.resize((size[0] - 10, size[1] - 10), Image.LANCZOS)

# # Create a circular image with microphone icon
# circle_image = Image.new("RGBA", size, (255, 255, 255, 0))
# mask = Image.new("L", size, 0)
# draw = ImageDraw.Draw(mask)
# draw.ellipse((0, 0, size[0], size[1]), fill="black")

# # Paste the microphone icon onto the circular image
# mic_icon = mic_image.resize((size[0] - 10, size[1] - 10), Image.LANCZOS)
# circle_image.paste(mic_icon, (5, 5), mic_icon)

# # Convert to Tkinter-compatible image
# mic_icon_tk = ImageTk.PhotoImage(circle_image)

# # Create the microphone button with the circular icon
# mic_button = tk.Label(chat_frame, image=mic_icon_tk, bd=0, bg='black')
# mic_button.bind("<Button-1>", handle_mic_input)
# mic_button.grid(row=1, column=2, padx=5)

# # Bind hover events to change the cursor
# def change_cursor(event):
#     root.config(cursor='hand2')

# def reset_cursor(event):
#     root.config(cursor='')

# send_button.bind("<Enter>", change_cursor)
# send_button.bind("<Leave>", reset_cursor)
# mic_button.bind("<Enter>", change_cursor)
# mic_button.bind("<Leave>", reset_cursor)

# # Configure grid weights to make the UI responsive
# chat_frame.grid_rowconfigure(0, weight=1)
# chat_frame.grid_rowconfigure(1, weight=0)
# chat_frame.grid_columnconfigure(0, weight=1)
# chat_frame.grid_columnconfigure(1, weight=0)
# chat_frame.grid_columnconfigure(2, weight=0)

# # Create and style the "Check IN" and "Check OUT" buttons
# style = ttk.Style()
# style.configure('Blue.TButton',
#                 background='#008b8b',  # Button background color
#                 foreground='black',     # Button text color
#                 font=('Comic Sans MS', 19),  # Font size
#                 borderwidth=0)  # Remove border
# style.map('Blue.TButton',
#           background=[('active', '#008b8b')],  # Button color on hover
#           foreground=[('active', 'black')])    # Text color on hover

# button_frame = tk.Frame(root, bg='#000000')  # Added padding around buttons
# button_frame.place(relx=0.88, rely=0.6, anchor=tk.CENTER, relwidth=0.138, relheight=0.16)  # Adjusted button frame position and size

# check_in_button = ttk.Button(button_frame, text="Check IN", style='Blue.TButton', command=check_in)
# check_in_button.grid(row=0, column=0, padx=7, pady=6)  # Adjusted padding between buttons

# check_out_button = ttk.Button(button_frame, text="Check OUT", style='Blue.TButton', command=check_out)
# check_out_button.grid(row=1, column=0, padx=7, pady=4)  # Adjusted padding between buttons

# # Trigger the resize function initially to set the correct background image size
# root.update_idletasks()  # Ensure all geometry calculations are done
# resize_bg_image()  # Call resize function to adjust image sizes

# # Bind the resize function to the root window
# root.bind('<Configure>', resize_bg_image)

# # Set up the window close protocol to exit gracefully
# root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy()))

# # Start the Tkinter main loop
# root.mainloop()



import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import sqlite3
import time
import time as time_lib
import tkinter as tk
from datetime import datetime
from tkinter import ttk
import cv2
import numpy as np
import pandas as pd
import pyttsx3
import requests
import speech_recognition as sr
from PIL import Image, ImageDraw, ImageFilter, ImageTk
from pyzbar.pyzbar import decode
import main
import atexit
import threading

def run_camera_on_exit():
    main.run_camera()

# Register the run_camera_on_exit function to be called upon script exit
atexit.register(run_camera_on_exit)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Variable to control if the bot should speak or not
should_speak = False

# Function to handle user input and bot responses
def handle_user_input(event=None):
    user_input = chat_entry.get()
    if user_input.strip() == "" or user_input == "Start conversation":
        return
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {user_input}\n", 'user')
    chat_display.config(state=tk.DISABLED)
    chat_entry.delete(0, tk.END)
    
    # Start a new thread for getting the bot response
    threading.Thread(target=get_bot_response, args=(user_input,), daemon=True).start()


# Function to get the bot's response from the Rasa server
def get_bot_response(user_input):
    global should_speak
    def run_response():
        url = "http://localhost:5005/webhooks/rest/webhook"
        payload = {
            "sender": "user",
            "message": user_input
        }
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
            for res in response.json():
                bot_message = res.get("text", "")
                simulate_typing(bot_message)
                if should_speak:
                    engine.say(bot_message)
                    engine.runAndWait()
        except requests.RequestException as e:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"Request error: {e}\n", 'bot_error')
            chat_display.config(state=tk.DISABLED)
        except Exception as e:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"An unexpected error occurred: {e}\n", 'bot_error')
            chat_display.config(state=tk.DISABLED)

    # Run the response function in a separate thread
    threading.Thread(target=run_response, daemon=True).start()


# Function to simulate typing effect
def simulate_typing(message):
    typing_speed = 0.03  # Adjust the typing speed as needed
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "Bot: ", 'bot')
    for char in message:
        chat_display.insert(tk.END, char, 'bot')
        chat_display.see(tk.END)  # Scroll to the end of the text widget
        chat_display.update_idletasks()  # Update the display
        time.sleep(typing_speed)  # End with a newline for the next input prompt
    chat_display.insert(tk.END, "\n\n")
    chat_display.config(state=tk.DISABLED)

# Function to handle microphone input
def handle_mic_input(event=None):
    global should_speak
    should_speak = True  # Set should_speak to True when using microphone
    
    # Display "Speak now..." immediately
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "Speak now...\n", 'bot')
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)
    chat_display.update_idletasks()  # Update the display immediately

    def process_audio():
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, "Processing audio...\n", 'bot')
            chat_display.config(state=tk.DISABLED)
            try:
                text = recognizer.recognize_google(audio)
                text = text.lower()
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"Recognized: {text}\n", 'user')
                chat_display.config(state=tk.DISABLED)
                # Start a new thread for getting the bot response
                threading.Thread(target=get_bot_response, args=(text,), daemon=True).start()
            except sr.UnknownValueError:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, "Could not understand audio. Please try again.\n", 'bot_error')
                chat_display.config(state=tk.DISABLED)
            except Exception as e:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, f"An error occurred: {e}\n", 'bot_error')
                chat_display.config(state=tk.DISABLED)
        should_speak = False  # Reset should_speak to False after processing microphone input

    # Run audio processing in a separate thread
    threading.Thread(target=process_audio, daemon=True).start()



# Function to capture ISBN from camera using OpenCV and pyzbar
def capture_isbn_from_camera():
    cap = cv2.VideoCapture(0)  # 0 is the default camera
    isbn = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            print(f"Detected barcode data: {barcode_data}")

            if len(barcode_data) == 13 and barcode_data.isdigit():
                isbn = barcode_data
                break

        if isbn:
            break

        cv2.imshow('Barcode Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return isbn

# Function to get student profile from SQLite database
def get_student_profile(id):
    """Retrieve student profile from the SQLite database."""
    try:
        conn = sqlite3.connect("students/sqlite.db")
        cursor = conn.execute("SELECT * FROM STUDENTS WHERE ID=?", (id,))
        profile = cursor.fetchone()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        profile = None
    finally:
        conn.close()
    return profile

# Function to get book title from Excel file
def get_book_title(isbn, excel_path='rasa_bot/actions/Books.xlsx'):
    """Retrieve book title from the Excel file using ISBN."""
    try:
        df = pd.read_excel(excel_path, dtype={'ISBN': str})
        book_info = df[df['ISBN'] == isbn]
        if not book_info.empty:
            title = book_info.iloc[0]['Title']
        else:
            title = None
    except Exception as e:
        print(f"An error occurred: {e}")
        title = None
    return title

# Function to log check-in or check-out in Excel file
def log_checkin_checkout(student_id, student_name, isbn, title, action, excel_path):
    try:
        # Read the existing Excel file
        df = pd.read_excel(excel_path, dtype={'ISBN': str})

        # Create a new DataFrame for the new log entry
        new_entry = pd.DataFrame([{
            'Student ID': student_id,
            'Student Name': student_name,
            'ISBN': str(isbn),  # Ensure ISBN is stored as a string
            'Title': title,
            'Action': action,
            'Date': datetime.now().strftime("%Y-%m-%d")  # Date only, no time
        }])

        # Concatenate the existing DataFrame with the new entry
        df = pd.concat([df, new_entry], ignore_index=True)

        # Write the updated DataFrame back to the Excel file
        df.to_excel(excel_path, index=False)
        print("Data added successfully.")
    except Exception as e:
        print(f"An error occurred while logging check-in/check-out: {e}")

# Function to check if a book is checked out and by whom
def get_checkout_details(isbn, excel_path='students/students_data.xlsx'):
    try:
        df = pd.read_excel(excel_path, dtype={'ISBN': str})
        checkout_info = df[(df['ISBN'] == isbn) & (df['Action'] == 'Check-Out')]
        if not checkout_info.empty:
            last_checkout = checkout_info.iloc[-1]
            return last_checkout['Student ID'], last_checkout['Student Name']
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Function to update book quantity and availability
def update_book_quantity_and_availability(isbn, change):
    try:
        df = pd.read_excel('rasa_bot/actions/Books.xlsx', dtype={'ISBN': str})

        # Find the book in the DataFrame
        book_info = df[df['ISBN'] == isbn]

        if not book_info.empty:
            # Update the Quantity
            df.loc[df['ISBN'] == isbn, 'Quantity'] += change

            # Update the Availability
            if df.loc[df['ISBN'] == isbn, 'Quantity'].values[0] <= 0:
                df.loc[df['ISBN'] == isbn, 'Availability'] = 'Unavailable'
            else:
                df.loc[df['ISBN'] == isbn, 'Availability'] = 'Available'

            # Write the updated DataFrame back to the Excel file
            df.to_excel('rasa_bot/actions/Books.xlsx', index=False)
            print("Book quantity and availability updated successfully.")
        else:
            print("Book not found in the database.")
    except Exception as e:
        print(f"An error occurred while updating book quantity and availability: {e}")

# Function to capture face and get student ID
def capture_face_and_get_student():
    face_detect = cv2.CascadeClassifier('students/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('students/student_recognizer/trainingdata.yml')
    cam = cv2.VideoCapture(0)
    student_id = None
    student_name = None
    face_detected_time = None  # Variable to store the time when the face is first detected
    run_duration = 5  # Number of seconds to run the loop after face detection

    while True:
        ret, img = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 70:
                profile = get_student_profile(id)
                if profile:
                    student_id = profile[0]
                    student_name = profile[1]
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, student_name, (x, y+h+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                    if face_detected_time is None:
                        face_detected_time = time_lib.time()  # Record the time when face was first detected

        cv2.imshow("Face", img)

        if face_detected_time is not None and (time_lib.time() - face_detected_time) >= run_duration:
            # If the specified duration has passed since face detection, break the loop
            break

        if cv2.waitKey(1) == 13:  # 13 is the Enter key
            break

    cam.release()
    cv2.destroyAllWindows()
    return student_id, student_name

# Function to check-in a book
def check_in():
    # Capture face and get student details
    student_id, student_name = capture_face_and_get_student()
    if not student_id or not student_name:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Student not recognized.\n", 'bot_error')
        chat_display.config(state=tk.DISABLED)
        return

    # Capture ISBN from camera
    isbn = capture_isbn_from_camera()
    if not isbn:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "ISBN not captured.\n", 'bot_error')
        chat_display.config(state=tk.DISABLED)
        return

    # Get the title of the book from the database
    title = get_book_title(isbn)
    if not title:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Book title not found.\n", 'bot_error')
        chat_display.config(state=tk.DISABLED)
        return

    # Verify if the book was checked out by the same student
    checkout_student_id, checkout_student_name = get_checkout_details(isbn)
    if checkout_student_id != student_id:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "This book was not checked out by you.\n", 'bot_error')
        chat_display.config(state=tk.DISABLED)
        return

    # Log the check-in
    log_checkin_checkout(student_id, student_name, isbn, title, "Check-In", "students/students_data.xlsx")
    # Update book quantity and availability
    update_book_quantity_and_availability(isbn, 1)

    # Display the result in the chat_display
    message = f"Check-in completed for {student_name} (ID: {student_id}) with Book Title: {title}.\n"
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, message, 'bot')
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)  # Scroll to the end of the text widget

# Function to check-out a book
def check_out():
    # Capture face and get student details
    student_id, student_name = capture_face_and_get_student()
    if not student_id or not student_name:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Student not recognized.\n", 'bot_error')
        chat_display.config(state=tk.DISABLED)
        return

    # Capture ISBN from camera
    isbn = capture_isbn_from_camera()
    if not isbn:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "ISBN not captured.\n", 'bot_error')
        chat_display.config(state=tk.DISABLED)
        return

    # Get the title of the book from the database
    title = get_book_title(isbn)
    if not title:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Book title not found.\n", 'bot_error')
        chat_display.config(state=tk.DISABLED)
        return

    # Check book availability
    df = pd.read_excel('rasa_bot/actions/Books.xlsx', dtype={'ISBN': str})
    book_info = df[df['ISBN'] == isbn]
    if book_info.empty or book_info.iloc[0]['Availability'] == 'Unavailable':
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "The book is currently unavailable.\n", 'bot_error')
        chat_display.config(state=tk.DISABLED)
        return

    # Log the check-out
    log_checkin_checkout(student_id, student_name, isbn, title, "Check-Out", "students/students_data.xlsx")
    # Update book quantity and availability
    update_book_quantity_and_availability(isbn, -1)

    # Display the result in the chat_display
    message = f"Check-out completed for {student_name} (ID: {student_id}) with Book Title: {title}.\n"
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, message, 'bot')
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)  # Scroll to the end of the text widget


# Function to handle placeholder text in chat entry
def add_placeholder(event):
    if chat_entry.get() == "":
        chat_entry.insert(0, "Start conversation")
        chat_entry.config(foreground='grey')

def remove_placeholder(event):
    if chat_entry.get() == "Start conversation":
        chat_entry.delete(0, tk.END)
        chat_entry.config(foreground='black')

# Create the main window
root = tk.Tk()
root.title("LIBBOT")
root.geometry("1500x700")
root.state('zoomed')

# Create a canvas for the background image and overlay image
canvas_bg = tk.Canvas(root)
canvas_bg.pack(fill=tk.BOTH, expand=True)  # Ensure canvas fills the window

# Load and process the background image
original_bg_image = Image.open("images/libbb.jpeg")

# Function to resize background image and update other image positions
def resize_bg_image(event=None):
    new_width = root.winfo_width()
    new_height = root.winfo_height()
    
    resized_bg_image = original_bg_image.resize((new_width, new_height), Image.LANCZOS)
    resized_bg_image = resized_bg_image.filter(ImageFilter.GaussianBlur(radius=5))
    bg_image_tk = ImageTk.PhotoImage(resized_bg_image)
    canvas_bg.itemconfig(background_image_item, image=bg_image_tk)
    canvas_bg.image = bg_image_tk

    # Reposition book image
    book_image_x = new_width - book_image_size - 74 # Position it 20 pixels from the right edge
    book_image_y = new_height - book_image_size - 308  # Position it 20 pixels from the bottom edge
    canvas_bg.coords(book_image_item, book_image_x, book_image_y)

    # Update position of robo image
    chat_frame_x = chat_frame.winfo_x()
    chat_frame_y = chat_frame.winfo_y()
    robo_image_x_shift = -200  # Shift the image further to the left
    robo_image_y_shift = 100   # Shift the image downwards
    canvas_bg.coords(robo_image_item, chat_frame_x + robo_image_x_shift, chat_frame_y - robo_image_size[1] + robo_image_y_shift)  # Shifted x and y coordinates

# Load and display the background image initially
bg_image_tk = ImageTk.PhotoImage(original_bg_image)
background_image_item = canvas_bg.create_image(0, 0, anchor=tk.NW, image=bg_image_tk)

# Create and process the book image
book_image_original = Image.open("images/book.png").convert("RGBA")
book_image_size = 100  # Fixed size
book_image_resized = book_image_original.resize((book_image_size, book_image_size), Image.LANCZOS)
book_image_tk = ImageTk.PhotoImage(book_image_resized)

# Create and process the book image item on the canvas
book_image_item = canvas_bg.create_image(0, 0, anchor=tk.CENTER, image=book_image_tk)
canvas_bg.image = book_image_tk

# Load and process the robo image
robo_image = Image.open("images/robo.png").convert("RGBA")
robo_image_size = (575, 300)  # Set the size of the robo image
robo_image_resized = robo_image.resize(robo_image_size, Image.LANCZOS)
robo_image_tk = ImageTk.PhotoImage(robo_image_resized)

# Create and process the robo image item on the canvas
robo_image_item = canvas_bg.create_image(0, 0, anchor=tk.NW, image=robo_image_tk)

# Create a frame for the chatbot interface with a semi-transparent background
chat_frame = tk.Frame(root, bg='black', bd=5)
chat_frame.place(relx=0.4, rely=0.58, anchor=tk.CENTER, relwidth=0.75, relheight=0.70)  # Use relative positioning

# Create a grid configuration for chat display and input area
chat_display = tk.Text(chat_frame, wrap=tk.WORD, bg='white', fg='#000000', font=('Comic Sans MS', 20), padx=10, pady=10)
chat_display.grid(row=0, column=0, columnspan=3, sticky='nsew')
chat_display.config(state=tk.DISABLED)

chat_display.tag_config('user', foreground='black', font=('Comic Sans MS', 19, 'bold'))
chat_display.tag_config('bot', foreground='green', font=('Comic Sans MS', 19, 'normal'))
chat_display.tag_config('bot_error', foreground='red', font=('Comic Sans MS', 19, 'bold'))

chat_entry = ttk.Entry(chat_frame, font=('Comic Sans MS', 20), foreground='grey')
chat_entry.insert(0, "Start conversation")
chat_entry.bind("<FocusIn>", remove_placeholder)
chat_entry.bind("<FocusOut>", add_placeholder)
chat_entry.grid(row=1, column=0, sticky='ew')
chat_entry.bind("<Return>", handle_user_input)

# Load and resize the send icon
send_image = Image.open("images/sub.webp").convert("RGBA")
send_image = send_image.resize((50, 50), Image.LANCZOS)
send_icon = ImageTk.PhotoImage(send_image)

send_button = tk.Label(chat_frame, image=send_icon, bd=0, bg='black')
send_button.bind("<Button-1>", handle_user_input)
send_button.grid(row=1, column=1, padx=5)

# Load and resize the microphone icon
mic_image = Image.open("images/micc.png").convert("RGBA")
size = (50, 50)  # Adjust the size of the circular image
mic_image = mic_image.resize((size[0] - 10, size[1] - 10), Image.LANCZOS)

# Create a circular image with microphone icon
circle_image = Image.new("RGBA", size, (255, 255, 255, 0))
mask = Image.new("L", size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, size[0], size[1]), fill="black")

# Paste the microphone icon onto the circular image
mic_icon = mic_image.resize((size[0] - 10, size[1] - 10), Image.LANCZOS)
circle_image.paste(mic_icon, (5, 5), mic_icon)

# Convert to Tkinter-compatible image
mic_icon_tk = ImageTk.PhotoImage(circle_image)

# Create the microphone button with the circular icon
mic_button = tk.Label(chat_frame, image=mic_icon_tk, bd=0, bg='black')
mic_button.bind("<Button-1>", handle_mic_input)
mic_button.grid(row=1, column=2, padx=5)

# Bind hover events to change the cursor
def change_cursor(event):
    root.config(cursor='hand2')

def reset_cursor(event):
    root.config(cursor='')

send_button.bind("<Enter>", change_cursor)
send_button.bind("<Leave>", reset_cursor)
mic_button.bind("<Enter>", change_cursor)
mic_button.bind("<Leave>", reset_cursor)

# Configure grid weights to make the UI responsive
chat_frame.grid_rowconfigure(0, weight=1)
chat_frame.grid_rowconfigure(1, weight=0)
chat_frame.grid_columnconfigure(0, weight=1)
chat_frame.grid_columnconfigure(1, weight=0)
chat_frame.grid_columnconfigure(2, weight=0)

# Create and style the "Check IN" and "Check OUT" buttons
style = ttk.Style()
style.configure('Blue.TButton',
                background='#008b8b',  # Button background color
                foreground='black',     # Button text color
                font=('Comic Sans MS', 19),  # Font size
                borderwidth=0)  # Remove border
style.map('Blue.TButton',
          background=[('active', '#008b8b')],  # Button color on hover
          foreground=[('active', 'black')])    # Text color on hover

button_frame = tk.Frame(root, bg='#000000')  # Added padding around buttons
button_frame.place(relx=0.88, rely=0.6, anchor=tk.CENTER, relwidth=0.14, relheight=0.16)  # Adjusted button frame position and size

check_out_button = ttk.Button(button_frame, text="Check OUT", style='Blue.TButton', command=check_out)
check_out_button.grid(row=0, column=0, padx=7, pady=6)  # Adjusted padding between buttons

check_in_button = ttk.Button(button_frame, text="Check IN", style='Blue.TButton', command=check_in)
check_in_button.grid(row=1, column=0, padx=7, pady=4)  # Adjusted padding between buttons

# Trigger the resize function initially to set the correct background image size
root.update_idletasks()  # Ensure all geometry calculations are done
resize_bg_image()  # Call resize function to adjust image sizes

# Bind the resize function to the root window
root.bind('<Configure>', resize_bg_image)

# Set up the window close protocol to exit gracefully
root.protocol("WM_DELETE_WINDOW", lambda: (root.destroy()))

# Start the Tkinter main loop
root.mainloop()

