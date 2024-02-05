import tkinter as tk
from tkinter import messagebox
import threading
import time
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller

# Initialize the keyboard controller
keyboard = Controller()

# Global variable to keep track of whether the script is running
is_running = False

def send_whatsapp_message(msg: str, phone_numbers: list):
    try:
        for phone_no in phone_numbers:
            if not is_running:
                break  # Exit the loop if the script is stopped
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone_no,
                message=msg,
                tab_close=True
            )
            pyautogui.click()
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            print(f"Message sent to {phone_no}!")
        if is_running:
            messagebox.showinfo("Success", "Messages sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def run_script(phone_numbers, message):
    global is_running
    is_running = True
    threading.Thread(target=send_whatsapp_message, args=(message, phone_numbers)).start()

def stop_script():
    global is_running
    is_running = False
    messagebox.showinfo("Info", "Script stopped.")

def on_send_click(phone_numbers, message):
    if not is_running:
        run_script(phone_numbers, message)
    else:
        messagebox.showwarning("Warning", "Script is already running.")

def on_stop_click():
    stop_script()

def add_number():
    number = number_entry.get()
    if number:
        number_with_code = "+91" + number  # Prepend "+91" to the number
        phone_listbox.insert(tk.END, number_with_code)
        number_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a phone number.")

def delete_number():
    selected_indices = phone_listbox.curselection()
    if selected_indices:
        for index in selected_indices[::-1]:  # Reverse order to avoid index shifting
            phone_listbox.delete(index)
    else:
        messagebox.showwarning("Warning", "Please select a phone number to delete.")

def select_all_numbers():
    phone_listbox.select_set(0, tk.END)

# Create the main window
window = tk.Tk()
window.title("WhatsApp Message Sender")

# Create a label for phone numbers
phone_label = tk.Label(window, text="Select phone numbers:")
phone_label.pack(pady=5)

# Create a listbox for phone numbers
phone_listbox = tk.Listbox(window, selectmode=tk.MULTIPLE)
phone_listbox.pack()

# Populate the listbox with sample phone numbers
friend_numbers = []
for number in friend_numbers:
    phone_listbox.insert(tk.END, number)

# Create a label and entry for adding a new phone number
number_label = tk.Label(window, text="Enter new number:")
number_label.pack(pady=5)

number_entry = tk.Entry(window)
number_entry.pack()

# Create a button to add a new number to the list
add_button = tk.Button(window, text="Add Number", command=add_number)
add_button.pack(pady=5)

# Create a button to delete selected numbers from the list
delete_button = tk.Button(window, text="Delete Selected", command=delete_number)
delete_button.pack(pady=5)

# Create a button to select all numbers
select_all_button = tk.Button(window, text="Select All", command=select_all_numbers)
select_all_button.pack(pady=5)

# Create a label for the message
message_label = tk.Label(window, text="Enter message:")
message_label.pack(pady=5)

# Create an entry for the message
message_entry = tk.Entry(window)
message_entry.pack()

# Set a default message
message_entry.insert(tk.END, "Hey bro, have you completed your Python task?")

# Create a button to send messages
send_button = tk.Button(window, text="Send Messages", command=lambda: on_send_click(get_selected_numbers(), get_message()))
send_button.pack(pady=10)

# Create a button to stop the script
stop_button = tk.Button(window, text="Stop Script", command=on_stop_click)
stop_button.pack(pady=5)

# Function to get the selected phone numbers
def get_selected_numbers():
    selected_indices = phone_listbox.curselection()
    return [phone_listbox.get(index) for index in selected_indices]

# Function to get the message from the entry
def get_message():
    return message_entry.get()

# Start the main event loop
window.mainloop()
