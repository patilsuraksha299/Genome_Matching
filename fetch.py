import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import hashlib

def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read the file in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def display_registration_details(result):
    details_window = tk.Toplevel(root)
    details_window.title("Registration Details")
    details_window.geometry('600x400')

    details_label = tk.Label(details_window, text='Registration Details', font=("bold", 20))
    details_label.pack(pady=10)

    tk.Label(details_window, text=f"Patient's Name: {result[3]}", font=("bold", 12)).pack()
    tk.Label(details_window, text=f"Relative 1 Name: {result[4]}", font=("bold", 12)).pack()
    tk.Label(details_window, text=f"Relative 1 Contact: {result[5]}", font=("bold", 12)).pack()
    tk.Label(details_window, text=f"Relative 2 Name: {result[6]}", font=("bold", 12)).pack()
    tk.Label(details_window, text=f"Relative 2 Contact: {result[7]}", font=("bold", 12)).pack()
    tk.Label(details_window, text=f"Relative 3 Name: {result[8]}", font=("bold", 12)).pack()
    tk.Label(details_window, text=f"Relative 3 Contact: {result[9]}", font=("bold", 12)).pack()

def check_registration():
    file_path = file_entry.get()
    if not file_path:
        messagebox.showerror('Error', 'Please select a text file.')
        return

    calculated_hash = calculate_file_hash(file_path)

    connection = sqlite3.connect("registration.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM registrations WHERE txtfile_hash=?", (calculated_hash,))
    result = cursor.fetchone()

    connection.close()

    if result:
        display_registration_details(result)
    else:
        messagebox.showinfo('Message', 'No matching registration found.')

root = tk.Tk()
root.title("Registration Checker")
root.geometry('800x500')
root.configure(background='grey')

l1 = tk.Label(root, text='Registration Checker', bg='black', fg='yellow', font=("bold", 30))
l1.pack(fill=tk.X)

fm1 = tk.Frame(root, bg='grey')
fm1.pack(pady=10)
fm2 = tk.Frame(root, bg='grey')
fm2.pack(pady=10)

l3 = tk.Label(fm2, text='Select Text File:', bg='grey', fg='black', font=("bold", 15))
l3.grid(row=0, column=0, padx=20, pady=5, sticky='w')

file_entry = tk.Entry(fm2, state='readonly', width=40)
file_entry.grid(row=0, column=1, padx=20, pady=5)

browse_button = tk.Button(fm2, text='Browse', width=10, bg='brown', fg='white', command=lambda: file_entry.config(state='normal') or file_entry.delete(0, tk.END) or file_entry.insert(0, filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])) or file_entry.config(state='readonly'), font=("bold", 12))
browse_button.grid(row=0, column=2, padx=10, pady=5)

check_button = tk.Button(root, text='Check Registration', width=15, bg='brown', fg='white', command=check_registration, font=("bold", 15))
check_button.pack(pady=10)

root.mainloop()
