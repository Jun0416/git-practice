from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sqlite3
import bcrypt

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)

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
    return jsonify([dict(book) for book in books]), 200

@app.route('/books/add', methods=['POST'])
@jwt_required()
def add_book():
    title = request.json['title']
    author = request.json['author']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    return '추가 성공!', 201

@app.route('/books/delete/<id>', methods=['DELETE'])
def delete_book(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM books WHERE id = ?", (id,))
    book = cursor.fetchone()
    if book is None:
        return "없는책", 404
    else:
        cursor.execute("DELETE FROM books WHERE id = ?", (id,))
        conn.commit()
        return '삭제 성공!', 200

@app.route('/books/update/<id>', methods=['PUT'])
def update_book(id):
    title = request.json['title']
    author = request.json['author']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=?, author=? WHERE id=?", (title, author, id))
    conn.commit()
    return '수정 성공!', 200

@app.route('/books/search')
def search_book():
    title = request.args.get('title')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", (f'%{title}%',))
    books = cursor.fetchall()
    conn.commit()
    return jsonify([dict(book) for book in books]), 200


@app.route('/books/search-author')
def search_author():
    author = request.args.get('author')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE author Like ?", (f'%{author}%',))
    books = cursor.fetchall()
    conn.commit()
    return jsonify([dict(book) for book in books]), 200


@app.route('/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
    conn.commit()
    return '가입 성공', 201


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username =?", (username,))
    user = cursor.fetchone()
    if user is None:
        return "없는 사용자입니다", 401
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        token = create_access_token(identity=username)
        return jsonify({'token': token}), 200
    else:
        return "비밀번호 틀림", 401
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
