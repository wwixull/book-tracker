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
                   image_path TEXT DEFAULT 'static/img/nobook.png',
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

def add_book(title, author, user_id, image_path=None):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    if not image_path:
        image_path = "nobook.png"

    cursor.execute(
        """
        INSERT INTO book (title, author, status, user_id, mark, image_path)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (title, author, 0, user_id, 0, image_path)
    )

    book_id = cursor.lastrowid

    cursor.execute(
        """
        INSERT INTO user_book (status, mark, user_id, book_id)
        VALUES (?, ?, ?, ?)
        """, (0, 0, user_id, book_id)
    )

    conn.commit()

def get_books(user_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, author, status, mark, image_path FROM book WHERE user_id=?", (user_id,))
    books = cursor.fetchall()
    conn.close()
    return books

def delete_book(book_id, user_id):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT image_path FROM book WHERE id = ? AND user_id = ?",
        (book_id, user_id)
    )
    result = cursor.fetchone()

    if not result:
        conn.close()
        return False, "Книга не найдена"
    
    image_path = result[0]

    if image_path and image_path != "static/img/nobook.png" and os.path.exists(image_path):
        os.remove(image_path)

    cursor.execute(
            """
            SELECT id FROM book 
            WHERE id = ? AND user_id = ?
            """,
            (book_id, user_id)
        )
        
    if not cursor.fetchone():
        return False, "Книга не найдена"
        
    cursor.execute(
            "DELETE FROM user_book WHERE book_id = ? AND user_id = ?",
            (book_id, user_id)
        )
        
    cursor.execute(
            "DELETE FROM book WHERE id = ? AND user_id = ?",
            (book_id, user_id)
        )
        
    conn.commit()

def change_book_status(book_id, user_id, new_status):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    cursor.execute(
            """
            UPDATE book 
            SET status = ? 
            WHERE id = ? AND user_id = ?
            """,
            (new_status, book_id, user_id)
        )
        
    cursor.execute(
            """
            UPDATE user_book 
            SET status = ? 
            WHERE book_id = ? AND user_id = ?
            """,
            (new_status, book_id, user_id)
        )
         
    conn.commit()

def change_book_mark(book_id, user_id, new_mark):
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    # Обновляем в таблице book
    cursor.execute(
        """
        UPDATE book
        SET mark = ?
        WHERE id = ? AND user_id = ?
        """, (new_mark, book_id, user_id)
    )

    # Обновляем в таблице user_book
    cursor.execute(
        """
        UPDATE user_book
        SET mark = ?
        WHERE book_id = ? AND user_id = ?
        """, (new_mark, book_id, user_id)
    )

    conn.commit()


if __name__ == "__main__":
    create_db()