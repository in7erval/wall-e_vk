from db import connection
import db

text = db.execute_read_query(db.connection, "SELECT text FROM messages WHERE peer_id=406612510")
for a in text:
    print(a[0])