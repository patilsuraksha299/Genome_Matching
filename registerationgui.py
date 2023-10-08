import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import hashlib

win = tk.Tk()
win.title("Registration Form")
win.geometry('800x500')
win.configure(background='grey')

l1 = tk.Label(win, text='Registration Form', bg='black', fg='yellow', font=("bold", 30))
l1.pack(fill=tk.X)

fm1 = tk.Frame(win, bg='grey')
fm1.pack(pady=10)
fm2 = tk.Frame(win, bg='grey')
fm2.pack(pady=10)
fm3 = tk.Frame(win, bg='grey')
fm3.pack(pady=10)
fm4 = tk.Frame(win, bg='grey')
fm4.pack(pady=10)
fm5 = tk.Frame(win, bg='grey')
fm5.pack(pady=10)
fm6 = tk.Frame(win, bg='grey')
fm6.pack(pady=10)

l3 = tk.Label(fm2, text='Select Text File:', bg='grey', fg='black', font=("bold", 15))
l3.grid(row=0, column=0, padx=20, pady=5, sticky='w')

l10 = tk.Label(fm2, text="Patient's Name:", bg='grey', fg='black', font=("bold", 15))
l10.grid(row=1, column=0, padx=20, pady=5, sticky='w')  
patient_name_entry = tk.Entry(fm2)
patient_name_entry.grid(row=1, column=1, padx=20, pady=5, sticky='w') 

l4 = tk.Label(fm3, text='Relative 1 Name:', bg='grey', fg='black', font=("bold", 15))
l4.grid(row=0, column=0, padx=20, pady=5, sticky='w')
rel1_name_entry = tk.Entry(fm3)
rel1_name_entry.grid(row=0, column=1, padx=20, pady=5)

l5 = tk.Label(fm3, text='Relative 1 Contact:', bg='grey', fg='black', font=("bold", 15))
l5.grid(row=0, column=2, padx=20, pady=5, sticky='w')
rel1_contact_entry = tk.Entry(fm3)
rel1_contact_entry.grid(row=0, column=3, padx=20, pady=5)

l6 = tk.Label(fm4, text='Relative 2 Name:', bg='grey', fg='black', font=("bold", 15))
l6.grid(row=0, column=0, padx=20, pady=5, sticky='w')
rel2_name_entry = tk.Entry(fm4)
rel2_name_entry.grid(row=0, column=1, padx=20, pady=5)

l7 = tk.Label(fm4, text='Relative 2 Contact:', bg='grey', fg='black', font=("bold", 15))
l7.grid(row=0, column=2, padx=20, pady=5, sticky='w')
rel2_contact_entry = tk.Entry(fm4)
rel2_contact_entry.grid(row=0, column=3, padx=20, pady=5)

l8 = tk.Label(fm5, text='Relative 3 Name:', bg='grey', fg='black', font=("bold", 15))
l8.grid(row=0, column=0, padx=20, pady=5, sticky='w')
rel3_name_entry = tk.Entry(fm5)
rel3_name_entry.grid(row=0, column=1, padx=20, pady=5)

l9 = tk.Label(fm5, text='Relative 3 Contact:', bg='grey', fg='black', font=("bold", 15))
l9.grid(row=0, column=2, padx=20, pady=5, sticky='w')
rel3_contact_entry = tk.Entry(fm5)
rel3_contact_entry.grid(row=0, column=3, padx=20, pady=5)


file_entry = tk.Entry(fm2, state='readonly', width=40)
file_entry.grid(row=0, column=1, padx=20, pady=5)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        file_entry.config(state='normal')
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)
        file_entry.config(state='readonly')

def create_table():
    connection = sqlite3.connect("registration.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY,
        txtfile_path TEXT,
        txtfile_hash TEXT,
        patient_name TEXT, 
        rel1_name TEXT,
        rel1_contact TEXT,
        rel2_name TEXT,
        rel2_contact TEXT,
        rel3_name TEXT,
        rel3_contact TEXT
    )
    """)

    connection.commit()
    connection.close()

create_table()

def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def submit_form():
    file_path = file_entry.get()
    txtfile_name = file_path.split('/')[-1] 
    txtfile_hash = calculate_file_hash(file_path)

    patient_name = patient_name_entry.get()
    rel1_name = rel1_name_entry.get()
    rel1_contact = rel1_contact_entry.get()
    rel2_name = rel2_name_entry.get()
    rel2_contact = rel2_contact_entry.get()
    rel3_name = rel3_name_entry.get()
    rel3_contact = rel3_contact_entry.get()

    connection = sqlite3.connect("registration.db")
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO registrations (txtfile_path, txtfile_hash, patient_name, rel1_name, rel1_contact, rel2_name, rel2_contact, rel3_name, rel3_contact)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (file_path, txtfile_hash, patient_name, rel1_name, rel1_contact, rel2_name, rel2_contact, rel3_name, rel3_contact))

    connection.commit()
    connection.close()

    messagebox.showinfo('Message', 'Registration Successful!')

browse_button = tk.Button(fm2, text='Browse', width=10, bg='brown', fg='white', command=browse_file, font=("bold", 12))
browse_button.grid(row=0, column=2, padx=10, pady=5)

submit_button = tk.Button(win, text='Submit', width=10, bg='brown', fg='white', command=submit_form, font=("bold", 15))
submit_button.pack()

win.mainloop()
