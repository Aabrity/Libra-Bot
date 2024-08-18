import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import requests
import time
import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Variable to control if the bot should speak or not
should_speak = False

# Function to handle user input and bot responses
def handle_user_input(event=None):
    user_input = chat_entry.get()
    if user_input.strip() == "":
        return
    chat_display.insert(tk.END, f"You: {user_input}\n", 'user')
    chat_entry.delete(0, tk.END)
    get_bot_response(user_input)

# Function to get the bot's response from the Rasa server
def get_bot_response(user_input):
    global should_speak
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": "user",
        "message": user_input
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        for res in response.json():
            bot_message = res.get("text", "")
            simulate_typing(bot_message)
            # Speak the response only if should_speak is True
            if should_speak:
                engine.say(bot_message)
                engine.runAndWait()
    else:
        chat_display.insert(tk.END, f"Bot: Error {response.status_code}\n", 'bot_error')

# Function to simulate typing effect
def simulate_typing(message):
    typing_speed = 0.03  # Adjust the typing speed as needed
    chat_display.insert(tk.END, "Bot: ", 'bot')
    for char in message:
        chat_display.insert(tk.END, char, 'bot')
        chat_display.see(tk.END)  # Scroll to the end of the text widget
        chat_display.update_idletasks()  # Update the display
        time.sleep(typing_speed)  # End with a newline for the next input prompt
    chat_display.insert(tk.END, "\n\n")

# Function to handle microphone input
def handle_mic_input(event=None):
    global should_speak
    should_speak = True  # Set should_speak to True when using microphone
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        chat_display.insert(tk.END, "Listening...\n", 'bot')
        audio = recognizer.listen(mic)
        chat_display.insert(tk.END, "Processing audio...\n", 'bot')
        try:
            text = recognizer.recognize_google(audio)
            text = text.lower()
            chat_display.insert(tk.END, f"Recognized: {text}\n", 'user')
            get_bot_response(text)
        except sr.UnknownValueError:
            chat_display.insert(tk.END, "Could not understand audio. Please try again.\n", 'bot_error')
        except Exception as e:
            chat_display.insert(tk.END, f"An error occurred: {e}\n", 'bot_error')
    should_speak = False  # Reset should_speak to False after processing microphone input

# Function to resize background image and update other image positions
def resize_bg_image(event):
    new_width = event.width
    new_height = event.height
    resized_bg_image = original_bg_image.resize((new_width, new_height), Image.LANCZOS)
    resized_bg_image = resized_bg_image.filter(ImageFilter.GaussianBlur(radius=5))
    bg_image_tk = ImageTk.PhotoImage(resized_bg_image)
    canvas_bg.itemconfig(background_image_item, image=bg_image_tk)
    canvas_bg.image = bg_image_tk

    # Update position of book image
    button_x = button_frame.winfo_rootx() + check_in_button.winfo_x() + check_in_button.winfo_width() // 2
    button_y = button_frame.winfo_rooty() + check_in_button.winfo_y()
    canvas_bg.coords(book_image_item, button_x, button_y - book_image_size - 10)  # Adjust y-coordinate

    # Update position of robo image (shifted further to the left and downwards)
    chat_frame_x = chat_frame.winfo_x()
    chat_frame_y = chat_frame.winfo_y()
    robo_image_x_shift = -200  # Increased this value to shift the image further to the left
    robo_image_y_shift = 100   # Shifted 100 pixels downwards
    canvas_bg.coords(robo_image_item, chat_frame_x + robo_image_x_shift, chat_frame_y - robo_image_size[1] + robo_image_y_shift)  # Shifted x and y coordinates

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
root.geometry("800x600")

# Create a canvas for the background image and overlay image
canvas_bg = tk.Canvas(root)
canvas_bg.pack(fill=tk.BOTH, expand=True)  # Use pack to fill the window

# Load and process the background image
original_bg_image = Image.open("libbb.jpeg")
bg_image_tk = ImageTk.PhotoImage(original_bg_image)
background_image_item = canvas_bg.create_image(0, 0, anchor=tk.NW, image=bg_image_tk)

# Load and process the book image
book_image_original = Image.open("book.png").convert("RGBA")
book_image_size = 100  # Fixed size
book_image_resized = book_image_original.resize((book_image_size, book_image_size), Image.LANCZOS)
book_image_tk = ImageTk.PhotoImage(book_image_resized)

# Create and process the book image item on the canvas
book_image_item = canvas_bg.create_image(0, 0, anchor=tk.CENTER, image=book_image_tk)
canvas_bg.image = book_image_tk

# Load and process the robo image
robo_image = Image.open("robo.png").convert("RGBA")
robo_image_size = (575, 300)  # Set the size of the robo image
robo_image_resized = robo_image.resize(robo_image_size, Image.LANCZOS)
robo_image_tk = ImageTk.PhotoImage(robo_image_resized)

# Create and process the robo image item on the canvas
robo_image_item = canvas_bg.create_image(0, 0, anchor=tk.NW, image=robo_image_tk)

# Bind the resize function to the root window
root.bind('<Configure>', resize_bg_image)

# Create a frame for the chatbot interface with a semi-transparent background
chat_frame = tk.Frame(root, bg='black', bd=5)
chat_frame.place(relx=0.4, rely=0.54, anchor=tk.CENTER, relwidth=0.75, relheight=0.70)  # Use relative positioning

# Create a grid configuration for chat display and input area
chat_display = tk.Text(chat_frame, wrap=tk.WORD, bg='white', fg='#000000', font=('Comic Sans MS', 20), padx=10, pady=10)
chat_display.grid(row=0, column=0, columnspan=3, sticky='nsew')

chat_display.tag_config('user', foreground='black', font=('Comic Sans MS', 20, 'bold'))
chat_display.tag_config('bot', foreground='green', font=('Comic Sans MS', 20, 'italic'))
chat_display.tag_config('bot_error', foreground='red', font=('Comic Sans MS', 20, 'bold'))

chat_entry = ttk.Entry(chat_frame, font=('Comic Sans MS', 20), foreground='grey')
chat_entry.insert(0, "Start conversation")
chat_entry.bind("<FocusIn>", remove_placeholder)
chat_entry.bind("<FocusOut>", add_placeholder)
chat_entry.grid(row=1, column=0, sticky='ew')
chat_entry.bind("<Return>", handle_user_input)

# Load and resize the send icon
send_image = Image.open("sub.webp").convert("RGBA")
send_image = send_image.resize((40, 40), Image.LANCZOS)  # Resize to desired size
send_icon_tk = ImageTk.PhotoImage(send_image)

# Create the send button with the circular icon
send_button = tk.Label(chat_frame, image=send_icon_tk, bd=0)
send_button.bind("<Button-1>", handle_user_input)
send_button.grid(row=1, column=1, padx=5)

# Load and resize the microphone icon
mic_image = Image.open("micc.png").convert("RGBA")
mic_image = mic_image.resize((20, 20), Image.LANCZOS)  # Resize to desired size

# Create a circular image with transparent background
size = (40, 40)
circle_image = Image.new("RGBA", size)
draw = ImageDraw.Draw(circle_image)
draw.ellipse((0, 0, size[0], size[1]), fill="black")

# Paste the microphone icon onto the circular image
mic_icon = mic_image.resize((size[0] - 10, size[1] - 10), Image.LANCZOS)
circle_image.paste(mic_icon, (5, 5), mic_icon)

# Convert to Tkinter-compatible image
mic_icon_tk = ImageTk.PhotoImage(circle_image)

# Create the microphone button with the circular icon
mic_button = tk.Label(chat_frame, image=mic_icon_tk, bd=0)
mic_button.bind("<Button-1>", handle_mic_input)
mic_button.grid(row=1, column=2, padx=5)

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
button_frame.place(relx=0.88, rely=0.6, anchor=tk.CENTER, relwidth=0.125, relheight=0.14)  # Adjusted button frame position and size

check_in_button = ttk.Button(button_frame, text="Check IN", style='Blue.TButton')
check_in_button.grid(row=0, column=0, padx=7, pady=6)  # Adjusted padding between buttons

check_out_button = ttk.Button(button_frame, text="Check OUT", style='Blue.TButton')
check_out_button.grid(row=1, column=0, padx=7, pady=6)  # Adjusted padding between buttons

# Start the Tkinter main loop
root.mainloop()
