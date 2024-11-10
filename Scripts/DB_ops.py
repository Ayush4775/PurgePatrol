import sqlite3
import hashlib
import random
import string


# Function to connect to the database
def connect_db(db_name: str = "employee_worktimes.db"):
    return sqlite3.connect(db_name)


# Function to generate a random secret word
def generate_secret_word(length: int = 12) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


# Function to hash the employee ID with a given secret word
def generate_hash(employee_id: int, secret_word: str) -> str:
    data = f"{employee_id}{secret_word}"
    return hashlib.sha256(data.encode()).hexdigest()


# Function to remove the employee and anonymize the employee ID occurrences
def remove_employee(employee_id: int):
    # Connect to the specified database
    connection = connect_db()
    cursor = connection.cursor()

    # Step 1: Find all occurrences of the employee ID in the 'Employee_id' column
    cursor.execute(
        "SELECT COUNT(*) FROM employee_worktimes WHERE Employee_id = ?", (employee_id,)
    )
    count = cursor.fetchone()[0]

    # If the employee ID does not exist, exit the function
    if count == 0:
        print(f"Employee ID {employee_id} not found in the database.")
        connection.close()
        return

    # Step 2: Generate a list of random secret words, one for each occurrence
    secret_words = [generate_secret_word() for _ in range(count)]

    # Step 3: Generate distinct hashes using the random secret words
    hashes = [generate_hash(employee_id, secret_word) for secret_word in secret_words]

    # Step 4: Update the 'Employee_id' column with the generated hashes
    cursor.execute(
        "SELECT rowid FROM employee_worktimes WHERE Employee_id = ?", (employee_id,)
    )
    rows = cursor.fetchall()

    for i, (row_id,) in enumerate(rows):
        cursor.execute(
            "UPDATE employee_worktimes SET Employee_id = ? WHERE rowid = ?",
            (hashes[i], row_id),
        )

    # Commit the changes and close the connection
    connection.commit()
    connection.close()
    print(
        f"Successfully anonymized {count} occurrences of employee ID {employee_id} using unique random secret words."
    )

    # Step 5: Retrieve and delete employee data from 'employee_data.db'
    connection_data = connect_db("employee_data.db")
    cursor_data = connection_data.cursor()

    # Retrieve the row for the employee_id
    cursor_data.execute("SELECT * FROM employee_data WHERE `EmpID` = ?", (employee_id,))
    employee_row = cursor_data.fetchone()

    if not employee_row:
        print(f"Employee ID {employee_id} not found in 'employee_data.db'.")
        connection_data.close()
        return

    # Get the column names from 'employee_data.db'
    column_names = [description[0] for description in cursor_data.description]

    # Delete the row from 'employee_data.db'
    cursor_data.execute("DELETE FROM employee_data WHERE `EmpID` = ?", (employee_id,))
    connection_data.commit()
    connection_data.close()
    print(
        f"Copied and deleted employee data for ID {employee_id} from 'employee_data.db'."
    )

    # Step 6: Insert the copied data into 'secret_data.db'
    connection_secret = connect_db("secret_data.db")
    cursor_secret = connection_secret.cursor()

    # Create the 'secret_data' table if it doesn't exist
    columns_with_types = ", ".join(
        [f"{col} TEXT" for col in column_names] + ["secret_words TEXT"]
    )
    cursor_secret.execute(
        f"CREATE TABLE IF NOT EXISTS secret_data ({columns_with_types})"
    )

    # Prepare the data to insert, including the list of secret words
    secret_words_str = ",".join(secret_words)
    employee_data_with_secret = list(employee_row) + [secret_words_str]
    placeholders = ", ".join(["?" for _ in employee_data_with_secret])

    # Insert the data into 'secret_data.db'
    cursor_secret.execute(
        f"INSERT INTO secret_data VALUES ({placeholders})",
        tuple(employee_data_with_secret),
    )
    connection_secret.commit()
    connection_secret.close()
    print("Stored employee data and secret words in 'secret_data.db'.")


# Example usage:
remove_employee(employee_id=2002)
