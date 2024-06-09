import sqlite3
import os

# deleting the database if it exists
try:
  os.remove(f'blog.db')
except Exception:
  pass

# Database connection
conn = sqlite3.connect('blog.db')

# Create Login Creds table
conn.execute("""
    CREATE TABLE Login_Creds (
        Owner_UID INTEGER PRIMARY KEY AUTOINCREMENT,
        User_ID TEXT,
        Name TEXT,
        Phone_Number TEXT,
        Email_ID TEXT,
        Password TEXT
    );
""")

# Create Blog table
conn.execute("""
    CREATE TABLE Blog (
        Blog_UID INTEGER PRIMARY KEY AUTOINCREMENT,
        Owner_UID INTEGER,
        Blog_Title TEXT,
        Blog_contents TEXT
    );
""")

# Create Comments table
conn.execute("""
    CREATE TABLE Comments (
        Comment_UID INTEGER PRIMARY KEY AUTOINCREMENT,
        Owner_UID INTEGER,
        Blog_UID INTEGER,
        Comment_contents TEXT
    );
""")

# Close the connection
conn.close()

print("Database tables created successfully!")