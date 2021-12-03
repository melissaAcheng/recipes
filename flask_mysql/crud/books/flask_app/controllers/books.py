from flask_app import app 
from flask import render_template, request, redirect, url_for
from flask_app.models import book, author 

# GET displays all books in database
@app.route('/books')
def books():
    books = book.Book.get_all_books()
    return render_template("books.html", all_books = books)

# POST creates a new book, adds to the database, and then redirects to show all books
@app.route('/books/create', methods=["POST"])
def create_book():
    book.Book.new_book(request.form)
    return redirect("/books")

# GET displays Book Show page
@app.route('/books/<int:id>')
def show_book(id):
    data = {
        "id": id
    }
    authors = author.Author.get_all_authors()
    fav_books = book.Book.get_authors_with_book(data)
    return render_template("show_book.html", books = fav_books, all_authors = authors)


# POST shows another author favorited the book
@app.route('/books/new_fav', methods=["POST"])
def create_new_fav():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author.Author.add_favorite(data)

    return redirect (url_for('show_book', id=data['book_id']))
