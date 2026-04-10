import sqlite3
import os

def create_db():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   login VARCHAR(1000) NOT NULL,
                   password VARCHAR(256) NOT NULL
                   )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title VARCHAR(256) NOT NULL,
                   author VARCHAR(256),
                   status INTEGER DEFAULT 0,
                   user_id INTEGER,
                   mark INTEGER DELAULT 1,
                   FOREIGN KEY (user_id) REFERENCES user (id)
                   )
    ''')
            # 0 - план
            # 1 - в процессе
            # 2 - прочитано