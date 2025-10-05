import sqlite3

connection = sqlite3.connect("customer_info.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    birthday TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    preferred_contact TEXT
)
""")

connection.commit()
connection.close()

print("Database and table created successfully!")
