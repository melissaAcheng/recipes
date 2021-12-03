# import author.py to access the class
from flask_app.models import author
from flask_app.config.mysqlconnection import connectToMySQL

class Book:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.num_of_pages = db_data['num_of_pages']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

        # list of authors related to the book
        self.authors = []

    # class method to get all books
    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"       
        results = connectToMySQL('books_schema').query_db(query)

        all_books = []
        for book in results:
            all_books.append(cls(book))
        
        return all_books

    # class method to create a new book
    @classmethod
    def new_book(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        return connectToMySQL('books_schema').query_db(query, data)

    # class method to retrieve the authors who favorited the book
    @classmethod
    def get_authors_with_book(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON favorites.book_id = books.id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;"
        results = connectToMySQL("books_schema").query_db(query, data)
 
        # print(results)
        # returns of list of dict contianing all authors who favorited the selected book
        book = cls(results[0])
        # parse the data to make instances and add to list (self.authors)
        for row_from_db in results:
            author_data = {
                "id": row_from_db["authors.id"],
                "name": row_from_db["name"],
                "created_at": row_from_db["authors.created_at"],
                "updated_at": row_from_db["authors.updated_at"]
            }
            book.authors.append(author.Author(author_data))
        return book
   