import sqlite3
# TODO: also think to delete some special info like Social number in case employee leaves + ofc anonymies it
from typing import List, Tuple, Dict, Any

#TODO: probably just hard code the connections here instead of always giving connection

def connect_db(db_name: str):
    return sqlite3.connect(db_name)


def create_table(connection, table_name: str, columns: Dict[str, str]):
    cursor = connection.cursor()
    columns_str = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")
    connection.commit()


def insert_record(connection, table_name: str, data: Dict[str, Any]):
    cursor = connection.cursor()
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])
    values = tuple(data.values())
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
    connection.commit()


def update_record(connection, table_name: str, updates: Dict[str, Any], condition: str, condition_params: Tuple):
    cursor = connection.cursor()
    updates_str = ', '.join([f"{col} = ?" for col in updates.keys()])
    values = tuple(updates.values()) + condition_params
    cursor.execute(f"UPDATE {table_name} SET {updates_str} WHERE {condition}", values)
    connection.commit()



def delete_record(connection, table_name: str, condition: str, condition_params: Tuple):
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}", condition_params)
    connection.commit()


# this is where the magic happens lol
def remove_employee(connection, employee_id):
    #TODO: make this function require a password
    db_name = 'employee_worktimes.db'
    conn = connect_db(db_name)

    #TODO: Get the keys to replace it with
    







def fetch_records(connection, table_name: str, columns: List[str] = None, condition: str = None, condition_params: Tuple = ()):
    cursor = connection.cursor()
    columns_str = ', '.join(columns) if columns else '*'
    query = f"SELECT {columns_str} FROM {table_name}"
    if condition:
        query += f" WHERE {condition}"
    cursor.execute(query, condition_params)
    return cursor.fetchall()





# Example usage
if __name__ == "__main__":
    # Database setup
    db_name = 'example.db'
    conn = connect_db(db_name)
    
    # Create table example
    create_table(conn, 'users', {
        'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
        'name': 'TEXT',
        'age': 'INTEGER',
        'email': 'TEXT'
    })
    
    # Insert a record
    insert_record(conn, 'users', {
        'name': 'Alice',
        'age': 25,
        'email': 'alice@example.com'
    })

    # Update a record
    update_record(conn, 'users', {
        'age': 26
    }, 'name = ?', ('Alice',))

    # Fetch and print records
    users = fetch_records(conn, 'users')
    print("Users:", users)

    # Delete a record
    delete_record(conn, 'users', 'name = ?', ('Alice',))

    # Close the connection
    conn.close()
