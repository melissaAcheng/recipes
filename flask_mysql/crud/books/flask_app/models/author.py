from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # create a list to add the author's favorites
        self.favorites = []

    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL("books_schema").query_db(query)

        all_authors = []
        for author in results:
            all_authors.append(cls(author))

        return results

    
    @classmethod
    def new_author(cls, data):
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        return connectToMySQL("books_schema").query_db(query, data)


     # class method to retrieve the favorite books per author
    @classmethod
    def get_favorite_books(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON favorites.author_id = authors.id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)

        author = cls(results[0])
        for row_from_db in results:
            book_data = {
                "id": row_from_db["books.id"],
                "title": row_from_db["title"],
                "num_of_pages": row_from_db["num_of_pages"],
                "created_at": row_from_db["books.created_at"],
                "updated_at": row_from_db["books.updated_at"]
            }
            author.favorites.append(book.Book(book_data))
        return author

    # class method to add favorite book
    @classmethod
    def add_favorite(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL('books_schema').query_db(query, data)