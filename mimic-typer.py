import tkinter as tk
from tkinter import scrolledtext, ttk
import pyautogui
import keyboard
import threading
import time
import random

# Define a dictionary mapping each key to its neighboring keys
keyboard_neighbors = {
    'a': 'qwsxz',
    'b': 'vghn',
    'c': 'xdfv',
    'd': 'serfcx',
    'e': 'wsdfr',
    'f': 'drtgvc',
    'g': 'ftyhbv',
    'h': 'gyujnb',
    'i': 'uojkl',
    'j': 'huiknm',
    'k': 'jilm,',
    'l': 'kop;.',
    'm': 'njk,',
    'n': 'bhjm',
    'o': 'iklp',
    'p': 'ol;[',
    'q': 'wa',
    'r': 'edft',
    's': 'qazxdcw',
    't': 'rfgy',
    'u': 'yhjik',
    'v': 'cfgb',
    'w': 'qsaed',
    'x': 'zasdc',
    'y': 'tghu',
    'z': 'asx',
    ',': 'mkl',
    '.': 'l;,',
    ';': 'lkp',
    ':': 'l;\'',
    "'": 'l;[',
    '"': 'l;[',
    '[': 'p;\'',
    ']': '[;\'',
    '{': 'p;"',
    '}': '}":',
}

typing_active = False

root = tk.Tk()
root.title("Mimic Typer")
root.geometry("900x500")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.Y)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=5, pady=15, fill=tk.BOTH, expand=True)

text_area = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=50, height=25)
text_area.pack(expand=True, fill=tk.BOTH)

delay_label = tk.Label(left_frame, text="Delay (seconds):")
delay_label.pack(anchor='w')

delay_entry = tk.Entry(left_frame)
delay_entry.pack(anchor='w')
delay_entry.insert(0, "0.03")  # Default delay value

random_mistakes_var = tk.BooleanVar(value=False)
typing_speed_variation_var = tk.BooleanVar(value=False)
pauses_var = tk.BooleanVar(value=False)

random_mistakes_checkbox = tk.Checkbutton(left_frame, text="Random Mistakes", variable=random_mistakes_var)
random_mistakes_checkbox.pack(anchor='w')

typing_speed_variation_checkbox = tk.Checkbutton(left_frame, text="Typing Speed Variation", variable=typing_speed_variation_var)
typing_speed_variation_checkbox.pack(anchor='w')

pauses_checkbox = tk.Checkbutton(left_frame, text="Pauses", variable=pauses_var)
pauses_checkbox.pack(anchor='w')

separator = ttk.Separator(left_frame, orient='horizontal')
separator.pack(fill='x', pady=10)

status_label = tk.Label(left_frame, text="Status: Idle")
status_label.pack(anchor='w')
progress_label = tk.Label(left_frame, text="Progress: 0%")
progress_label.pack(anchor='w')

word_count_label = tk.Label(left_frame, text="Words: 0")
word_count_label.pack(anchor='w')
char_count_label = tk.Label(left_frame, text="Characters: 0")
char_count_label.pack(anchor='w')

def update_count(*args):
    text = text_area.get("1.0", tk.END)
    words = len(text.split())
    characters = len(text) - 1  # Subtract 1 to ignore the last newline character
    word_count_label.config(text=f"Words: {words}")
    char_count_label.config(text=f"Characters: {characters}")

text_area.bind("<KeyRelease>", update_count) # Bind the update_count function to text changes in text_area

def update_status(status, progress=0):
    status_label.config(text=f"Status: {status}")
    progress_label.config(text=f"Progress: {progress}%")

def type_text():
    global typing_active
    base_delay = float(delay_entry.get())
    time.sleep(0.5)
    text = text_area.get("1.0", tk.END)
    total_length = len(text)
    typed_length = 0

    if text.endswith("\n"):
        text = text[:-1]

    for char in text:
        if not typing_active:
            break

        original_char = char

        # Avoid mistakes on whitespace
        if char.isspace():
            pyautogui.write(char)
            time.sleep(0.1)  # Adjust the delay for whitespace typing
            continue

        # Toggle for random mistakes
        if random_mistakes_var.get() and random.random() < 0.05:
            char = generate_realistic_mistake(char)

        # Toggle for typing speed variation
        speed_factor = random.uniform(0.1, 3)
        if typing_speed_variation_var.get():
            interval = base_delay * speed_factor
        else:
            interval = base_delay

        # Toggle for pauses
        if char in ".!?" and pauses_var.get():
            interval *= random.uniform(10, 30)  # Add even longer pause for end of sentences

        typed_length += 1
        progress = int((typed_length / total_length) * 100)
        update_status("Typing", progress)

        pyautogui.write(char, interval=interval)
        time.sleep(interval)

        # If a mistake was made, correct it
        if original_char != char:
            pyautogui.press('backspace')
            time.sleep(0.1)  # Delay before correcting
            pyautogui.write(original_char)
            time.sleep(interval)

    typing_active = False
    update_status("Idle")

def generate_realistic_mistake(char):
    # If the character has neighboring keys, choose one of them
    if char.lower() in keyboard_neighbors:
        neighbors = keyboard_neighbors[char.lower()]
        return random.choice(neighbors)

    # If not, return a random mistake
    return random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()-=_+[]{}|;':\",.<>/? ")

def on_macro_triggered():
    global typing_active
    typing_active = not typing_active
    if typing_active:
        update_status("Starting")
        threading.Thread(target=type_text).start()
    else:
        update_status("Stopped")

def listen_for_macro():
    keyboard.add_hotkey('ctrl+shift+/', on_macro_triggered)

def start_listening():
    listener_thread = threading.Thread(target=listen_for_macro)
    listener_thread.daemon = True
    listener_thread.start()

start_listening()
root.mainloop()
