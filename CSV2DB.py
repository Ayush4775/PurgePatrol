import sqlite3
import pandas as pd
import os

# Step 1: Load the CSV file
csv_file = 'project_data.csv' # Replace with your CSV file path
data = pd.read_csv(csv_file)

# Automatically generate the .db file name based on the CSV file name
db_file = os.path.splitext(csv_file)[0] + '.db'
connection = sqlite3.connect(db_file)
cursor = connection.cursor()

# Step 3: Create a table in the database based on CSV headers
table_name = 'data_table'  # You can name the table as needed
columns = ', '.join([f"{col} TEXT" for col in data.columns])  # Assuming all columns are TEXT
cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

# Step 4: Insert CSV data into the database
# Convert DataFrame rows to list of tuples for insertion
data_tuples = [tuple(x) for x in data.values]

# Prepare a SQL insert statement based on the number of columns
placeholders = ', '.join(['?'] * len(data.columns))
insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

# Execute many inserts at once
cursor.executemany(insert_query, data_tuples)
connection.commit()

# Step 5: Verify the data insertion (optional)
for row in cursor.execute(f"SELECT * FROM {table_name}").fetchall():
    print(row)

# Step 6: Close the connection
connection.close()
