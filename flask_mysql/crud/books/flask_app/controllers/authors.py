from flask_app import app 
from flask import render_template, request, redirect, url_for
from flask_app.models import book, author

@app.route('/')
def index():
    return redirect ('/authors')

# GET displays all authors and form to add new author
@app.route('/authors')
def authors():
    authors = author.Author.get_all_authors()
    return render_template("authors.html", all_authors = authors)

# POST creates the new author and then redirects to display all authors
@app.route('/authors/create', methods=["POST"])
def create_author():
    author.Author.new_author(request.form)
    return redirect('/')

# GET displays Author Show page
@app.route('/authors/<int:id>')
def show_author(id):
    all_books = book.Book.get_all_books()
    data = {
        "id": id
    }
    author_fav = author.Author.get_favorite_books(data)

    return render_template("show_author.html", author_fav = author_fav, all_books = all_books)


# POST creates a new favorite book by author and refreshes these Author Show page with new favorite
@app.route('/authors/new_fav', methods=["POST"])
def create_fav():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author.Author.add_favorite(data)
    # call the query that adds new author favorite book and displays all favorites
    return redirect (url_for('show_author', id = data['author_id']))