import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
SALT = "kdfjkjwekjq002302mdmclcs[ck,]"

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
    CREATE TABLE IF NOT EXISTS book (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title VARCHAR(256) NOT NULL,
                   author VARCHAR(256),
                   status INTEGER DEFAULT 0,
                   user_id INTEGER,
                   mark INTEGER DEFAULT 0,
                   FOREIGN KEY (user_id) REFERENCES user (id)
                   )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_book (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   status INTEGER DEFAULT 0,
                   mark INTEGER DEFAULT 0,
                   user_id INTEGER,
                   book_id INTEGER,
                   FOREIGN KEY (user_id) REFERENCES user (id)
                   )
    ''')
            # 0 - план
            # 1 - в процессе
            # 2 - прочитано

def add_user(login, password):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password + SALT)

    cursor.execute("INSERT INTO user (login, password) VALUES (?,?)", (login, hashed_password))

    conn.commit()

def get_users():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    return users

def check_user_exists(login):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user WHERE login=?", (login,))

    user = cursor.fetchone()
    return True if user else False

def auth_user(login, password):

    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE login = ?", (login,))
    user = cursor.fetchone()
    if not user:
        return -1
    
    if check_password_hash(user[2], password+SALT):
        return user[0]
    return -1

if __name__ == "__main__":
    create_db()