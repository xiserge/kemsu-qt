import sqlite3
from os import path


def create_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            image_data BLOB)''')
    conn.commit()
    conn.close()


def get_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = c.fetchone()
    conn.close()
    return book


def add_book_with_image(title, author, image_path):
    image_data = None
    if path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_data = f.read()  # Чтение изображения как бинарных данных
            image_data = sqlite3.Binary(image_data)

    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('INSERT INTO books (title, author, image_data) VALUES (?, ?, ?)',
              (title, author, image_data))  # Сохраняем изображение как BLOB
    conn.commit()
    conn.close()


def remove_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()


def update_book(book_id, title, author, image_path):
    image_data = None
    if image_path and path.exists(image_path):
        with open(image_path, 'rb') as f:
            image_data = f.read()
            image_data = sqlite3.Binary(image_data)

    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('UPDATE books SET title = ?, author = ?, image_data = COALESCE(?, image_data) WHERE id = ?',
              (title, author, image_data, book_id))
    conn.commit()
    conn.close()


def get_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM books')
    books = c.fetchall()
    conn.close()
    return books
