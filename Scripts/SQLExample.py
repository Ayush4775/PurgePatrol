import sqlite3

# Connect to a SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("demo.db")
cursor = connection.cursor()

# Step 1: Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT
)
''')


connection.commit()

# Step 2: Insert data into the table
users = [
    ('Alice', 25, 'alice@example.com'),
    ('Bob', 30, 'bob@example.com'),
    ('Charlie', 35, 'charlie@example.com')
]

cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", users)
connection.commit()

# Step 3: Query the data
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Step 4: Update a record
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (28, 'Alice'))
connection.commit()

# Step 5: Delete a record
cursor.execute("DELETE FROM users WHERE name = ?", ('Charlie',))
connection.commit()

# Step 6: Verify the update
cursor.execute("SELECT * FROM users")
updated_results = cursor.fetchall()
print("Updated records:")
for row in updated_results:
    print(row)

# Close the connection
connection.close()
