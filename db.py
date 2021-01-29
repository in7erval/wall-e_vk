import sqlite3
from sqlite3 import Error


def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return conn


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def write_row(event):
    peer_id = event.object.object.message.peer_id
    text = event.object.object.message.text
    from_id = event.object.object.message.from_id
    execute_query(connection,
                     f"INSERT INTO messages (peer_id, text, from_id) VALUES ({peer_id}, '{text}', {from_id})")


connection = create_connection("db.sqlite")

