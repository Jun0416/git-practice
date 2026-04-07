from flask import Flask, request
import sqlite3
app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/books')
def get_books():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    return str([dict(book) for book in books])

@app.route('/books/add', methods=['POST'])
def add_book():
    title = request.json['title']
    author = request.json['author']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    return '추가 성공!'

@app.route('/books/delete/<id>', methods=['DELETE'])
def delete_book(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    conn.commit()
    return '삭제 성공!'

@app.route('/books/update/<id>', methods=['PUT'])
def update_book(id):
    title = request.json['title']
    author = request.json['author']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=? WHERE id=?", (title, author, id))
    conn.commit()
    return '수정 성공!'

@app.route('/books/search')
def search_book():
    title = request.args.get('title')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f'%{title}%',))
    books = cursor.fetchall()
    conn.commit()
    return str([dict(book) for book in books])
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
