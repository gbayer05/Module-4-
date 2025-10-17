from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Use SQLite for simplicity; the DB file will be `books.db`
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    publisher = db.Column(db.String(120), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_name': self.book_name,
            'author': self.author,
            'publisher': self.publisher
        }

# Initialize the database (create tables)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return {"message": "Welcome to the Book API"}

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

# Get one book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404, description="Book not found")
    return jsonify(book.to_dict()), 200

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    # Data validation: ensure required fields
    if not data or 'book_name' not in data or 'author' not in data or 'publisher' not in data:
        abort(400, description="Missing fields in request body")
    
    new_book = Book(
        book_name = data['book_name'],
        author = data['author'],
        publisher = data['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

# Update an existing book (PUT)
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404, description="Book not found")
    data = request.get_json()
    # For full replace, you might require all fields. Or allow partial.
    if not data:
        abort(400, description="Missing JSON body")

    # Update fields if present
    if 'book_name' in data:
        book.book_name = data['book_name']
    if 'author' in data:
        book.author = data['author']
    if 'publisher' in data:
        book.publisher = data['publisher']
    
    db.session.commit()
    return jsonify(book.to_dict()), 200

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        abort(404, description="Book not found")
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Book {book_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
