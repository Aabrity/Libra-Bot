import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import subprocess
import add
import main
import threading
import new_member
import sys

def new_member_scan():
    try:
        new_member.new_member_gui()
    except Exception as e:
        print(f"Error in new_member(): {e}")

def add_books():
    try:
        add.add_books()
    except Exception as e:
        print(f"Error in add_books(): {e}")

def log_out():
    try:
        # Start a new process to run the camera function
        subprocess.Popen([sys.executable, "-c", "import main; main.run_camera()"])

        # Destroy the Tkinter window and terminate the current script
        root.destroy()
        sys.exit()
    except Exception as e:
        print(f"Error in log_out(): {e}")

# Function to load and blur the background image
def load_background_image(image_path):
    original_image = Image.open(image_path)
    return original_image, ImageTk.PhotoImage(original_image)

# Function to handle window resizing and update background image
def resize_bg_image(event=None):
    new_width = root.winfo_width()
    new_height = root.winfo_height()

    # Resize the background image to fit the window
    resized_bg_image = original_bg_image.resize((new_width, new_height), Image.LANCZOS)
    resized_bg_image = resized_bg_image.filter(ImageFilter.GaussianBlur(radius=5))
    bg_image_tk = ImageTk.PhotoImage(resized_bg_image)
    
    canvas_bg.itemconfig(background_image_item, image=bg_image_tk)
    canvas_bg.image = bg_image_tk

# Create the main window
root = tk.Tk()
root.title("LIBBOT")
root.state('zoomed')

# Set window size and background color
root.geometry("1200x800")  # Adjust the size as needed

# Create a canvas for the background image
canvas_bg = tk.Canvas(root)
canvas_bg.pack(fill=tk.BOTH, expand=True)

# Load and process the background image
original_bg_image, bg_image_tk = load_background_image("images/libbb.jpeg")
background_image_item = canvas_bg.create_image(0, 0, anchor=tk.NW, image=bg_image_tk)

# Function to call initial resize after window is created
def on_window_creation():
    resize_bg_image()
    root.update_idletasks()  # Force the window to update

# Bind the resize function to the root window
root.bind('<Configure>', resize_bg_image)

# Load and process the robo image
robo_image = Image.open("images/robo1.png").convert("RGBA")
robo_image_size = (575, 300)  # Set the size of the robo image
robo_image_resized = robo_image.resize(robo_image_size, Image.LANCZOS)
robo_image_tk = ImageTk.PhotoImage(robo_image_resized)

# Create and process the robo image item on the canvas
robo_image_item = canvas_bg.create_image(390, 40, anchor=tk.NW, image=robo_image_tk)

# Create a frame to hold widgets on top of the canvas
frame = tk.Frame(canvas_bg, bg="#316457", highlightbackground="black", highlightcolor="black", highlightthickness=3)
canvas_bg.create_window(480, 250, anchor=tk.NW, window=frame)

# Add a title label
title_label = tk.Label(frame, text="Face Scan System", font=("Comic Sans MS", 22, "bold"), bg="#316457")
title_label.pack(pady=10)

# Create a frame for buttons
button_frame = tk.Frame(frame, bg="#316457", width=300, height=250)
button_frame.pack(pady=30, padx=30)
button_frame.pack_propagate(False)

# Create the "New Member", "Existing Member", and "Admin" buttons with uniform size
button_width = 20  # Width in characters
button_height = 2  # Height in lines

# Button commands with lambda to pass the root
new_member_button = tk.Button(button_frame, text="New Member", font=("Comic Sans MS", 14), bg="#2196F3", fg="black", bd=2, relief="solid", command=lambda: new_member_scan(), width=button_width, height=button_height)
add_books_button = tk.Button(button_frame, text="Add Books", font=("Comic Sans MS", 14), bg="#2196F3", fg="black", bd=2, relief="solid", command=lambda: add_books(), width=button_width, height=button_height)
logout_button = tk.Button(button_frame, text="LogOut", font=("Comic Sans MS", 14), bg="#FF5722", fg="black", bd=2, relief="solid", command=lambda: log_out(), width=button_width, height=button_height)

# Pack buttons
new_member_button.pack(pady=10)
add_books_button.pack(pady=10)
logout_button.pack(pady=10)

# Keep a reference to the background image to prevent garbage collection
canvas_bg.image = bg_image_tk

# Schedule the initial resize after the main loop starts
root.after(10, on_window_creation)

root.mainloop()
