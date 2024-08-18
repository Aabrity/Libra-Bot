import cv2
import numpy as np
import sqlite3
import subprocess
import time
import tkinter as tk
from tkinter import messagebox
import mediapipe as mp
import serial

# Load face recognition models
admin_recognizer = cv2.face.LBPHFaceRecognizer_create()
student_recognizer = cv2.face.LBPHFaceRecognizer_create()

admin_recognizer.read("admin/recognizer/trainingdata.yml")
student_recognizer.read("students/student_recognizer/trainingdata.yml")

# Load face detection model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the serial connection (adjust 'COM4' to your Arduino's port)
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
    IS_ARDUINO = True
except serial.SerialException:
    print("Could not open serial port. Arduino not connected.")
    IS_ARDUINO = False

def get_profile_from_db(user_id, table):
    conn = sqlite3.connect("students/sqlite.db" if table == "STUDENTS" else "admin/database.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE ID=?", (user_id,))
    profile = cursor.fetchone()
    conn.close()
    return profile

def show_message(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showwarning("Alert", message)
    root.destroy()

def display_text(frame, text):
    cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

def trigger_buzzer(duration=3):
    """Trigger the buzzer for a specified duration using Arduino."""
    if IS_ARDUINO:
        arduino.write(b'B')  # Send the 'B' command to Arduino to trigger the buzzer
        time.sleep(duration)  # Wait for the specified duration
    else:
        print("Buzzer triggered (mock)")

def run_camera():
    cam = cv2.VideoCapture(0)
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

    recognized_start_time = None
    recognized_profile = None
    recognized_table = None
    unknown_start_time = None
    thumbs_up_detected = False
    gesture_detection_start_time = time.time()

    # Create a fullscreen window
    window_name = "Face and Gesture Recognition"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            continue

        if not thumbs_up_detected:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks and connections
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                    if (thumb_tip.y < index_tip.y) and (thumb_tip.y < pinky_tip.y):
                        thumbs_up_detected = True
                        gesture_detection_start_time = time.time()
                        break

            display_text(frame, "Show thumbs up to scan face")

            if time.time() - gesture_detection_start_time > 3:
                gesture_detection_start_time = time.time()  # Restart the gesture detection window
        else:
            display_text(frame, "Scanning")
            cv2.imshow(window_name, frame)
            cv2.waitKey(1500)  # Display "Scanning" for 2 seconds before starting face detection
            break  # Exit the loop to start face detection

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        unknown_detected = False
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            user_id, confidence = admin_recognizer.predict(roi_gray)
            if confidence < 50:
                profile = get_profile_from_db(user_id, "ADMINS")
                if profile:
                    recognized_profile = profile
                    recognized_table = "ADMINS"
                    name = profile[1]
                    color = (0, 255, 0)  # Green for recognized
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                    if recognized_start_time is None:
                        recognized_start_time = time.time()
                    break
            else:
                user_id, confidence = student_recognizer.predict(roi_gray)
                if confidence < 50:
                    profile = get_profile_from_db(user_id, "STUDENTS")
                    if profile:
                        recognized_profile = profile
                        recognized_table = "STUDENTS"
                        name = profile[1]
                        color = (0, 255, 0)  # Green for recognized
                        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                        cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                        if recognized_start_time is None:
                            recognized_start_time = time.time()
                        break
                else:
                    color = (0, 0, 255)  # Red for unrecognized
                    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
                    cv2.putText(frame, "Unknown", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                    unknown_detected = True
                    if unknown_start_time is None:
                        unknown_start_time = time.time()
                    elif time.time() - unknown_start_time >= 3:
                        trigger_buzzer()  # Trigger the buzzer when unknown face is detected for 4 seconds
                        cam.release()
                        cv2.destroyAllWindows()
                        show_message("Consult with admin")
                        run_camera()

        if not unknown_detected:
            unknown_start_time = None  # Reset the unknown start time if no unknown face is detected

        if recognized_profile:
            if time.time() - recognized_start_time >= 3:
                cam.release()
                cv2.destroyAllWindows()
                if recognized_table == "ADMINS":
                    subprocess.run(["python", "admin.py"])
                elif recognized_table == "STUDENTS":
                    subprocess.run(["python", "chat_ui.py"])
                return  # Exit the function after handling

        cv2.imshow(window_name, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    run_camera()
