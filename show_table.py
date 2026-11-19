"""Print the columns and rows of the travelbuddy_trip table.

It reads db.sqlite3 directly, not through the Django model, so it still works
after a rollback, when models.py and the database don't match any more.

Run it from the project folder: python show_table.py
"""
import sqlite3

connection = sqlite3.connect("db.sqlite3")
cursor = connection.execute("SELECT * FROM travelbuddy_trip")

columns = [column[0] for column in cursor.description]
print("Columns:", ", ".join(columns))
for row in cursor:
    print(row)

connection.close()
