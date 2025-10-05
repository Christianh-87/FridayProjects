import sqlite3

conn = sqlite3.connect("customer_info.db")
cur = conn.cursor()

for row in cur.execute("SELECT * FROM customers"):
    print(row)

conn.close()
