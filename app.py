import sqlite3
import tkinter as tk
from tkinter import ttk

connection = sqlite3.connect("customer_info.db")
cursor = connection.cursor()

root = tk.Tk()
root.title("Customer Information Form")

ttk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
name_entry = ttk.Entry(root, width=40)
name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Birthday (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
bday_entry = ttk.Entry(root, width=40)
bday_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
email_entry = ttk.Entry(root, width=40)
email_entry.grid(row=2, column=1, padx=5, pady=5)

ttk.Label(root, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
phone_entry = ttk.Entry(root, width=40)
phone_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(root, text="Address:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
address_entry = ttk.Entry(root, width=40)
address_entry.grid(row=4, column=1, padx=5, pady=5)

ttk.Label(root, text="Preferred Contact:").grid(row=5, column=0, padx=5, pady=5, sticky="e")
contact_method = ttk.Combobox(root, values=["Email", "Phone", "Mail"], state="readonly", width=37)
contact_method.grid(row=5, column=1, padx=5, pady=5)
contact_method.set("Email")  # default choice

def submit():
    name = name_entry.get()
    birthday = bday_entry.get()
    email = email_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()
    preferred = contact_method.get()

    cursor.execute(
        "INSERT INTO customers (name, birthday, email, phone, address, preferred_contact) VALUES (?, ?, ?, ?, ?, ?)",
        (name, birthday, email, phone, address, preferred)
    )
    connection.commit()

    name_entry.delete(0, tk.END)
    bday_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    contact_method.set("Email")

ttk.Button(root, text="Submit", command=submit).grid(row=6, column=0, columnspan=2, pady=10)

root.mainloop()

connection.close()
