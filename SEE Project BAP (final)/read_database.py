import sqlite3

# Database connection
conn = sqlite3.connect('blog.db')

# Get a cursor object to execute queries
cursor = conn.cursor()

# Fetch table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Print table names
print("Tables in the database:")
for table_name in tables:
    print(table_name[0])

# Fetch data from each table
for table_name in tables:
    print(f"\nContents of table '{table_name[0]}':")
    cursor.execute(f"SELECT * FROM {table_name[0]};")
    data = cursor.fetchall()

    # Print column names (optional)
    column_names = [desc[0] for desc in cursor.description]
    print(column_names)  # Uncomment to print column names

    # Print table data
    for row in data:
        print(row)

# Close the connection
conn.close()
