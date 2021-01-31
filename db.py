import sqlite3
from sqlite3 import Error
import logging

logging.basicConfig(level=logging.INFO)


def create_connection(path):
    conn = None
    try:
        conn = sqlite3.connect(path)
        logging.info("Connection to SQLite DB successful")
    except Error as e:
        logging.error(f"The error '{e}' occurred")
    return conn


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        logging.info("Query executed successfully")
    except Error as e:
        logging.error(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        logging.error(f"The error '{e}' occurred")


def write_row(event, name, date):
    peer_id = event.object.object.message.peer_id
    text = event.object.object.message.text
    from_id = event.object.object.message.from_id
    execute_query(connection,
                  f"INSERT INTO messages (peer_id, text, from_id, name, date) VALUES ({peer_id}, '{text}', {from_id},"
                  f" '{name}', '{date}')")


def get_messages(peer_id, with_time=False):
    query = f"SELECT date, name, text FROM messages WHERE peer_id={peer_id}"
    messages = execute_read_query(connection, query)
    print(messages)
    messages.reverse()
    result = ""
    count = 0
    for x in messages:
        row = x[1] + ': ' + x[2] + '\n'
        if with_time:
            row = x[0] + ' | ' + row
        result += row
        if len(result) > 900:
            break
        count += 1
    return f'Последние {count} сообщений:\n' + result


def save_sticker(peer_id, sticker_id, sticker_name="unknown"):
    execute_query(connection,
                  f"INSERT INTO stickers (sticker_id, sticker_name, peer_id) VALUES "
                  f"({sticker_id}, '{sticker_name}', {peer_id})")


connection = create_connection("db.sqlite")
