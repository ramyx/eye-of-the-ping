import os
from tkinter import messagebox


def send_notification(title, message):
    # Simple notification for now
    messagebox.showinfo(title, message)


def play_sound(file_path):
    if os.path.exists(file_path):
        os.system(f"aplay {file_path}")  # Replace with appropriate player
