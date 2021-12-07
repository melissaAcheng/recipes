from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import emails
from flask import flash
import re

# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Email:

    db_name = 'emails'

    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_email(cls, data):
        query = "INSERT INTO emails (email) VALUES (%(email)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM emails;"
        results = connectToMySQL(cls.db_name).query_db(query) # list of dict

        all_emails = []
        for row in results:
            one_email = cls(row)
            all_emails.append(one_email)
        return all_emails

    @classmethod
    def delete_email(cls, data):
        query = "DELETE FROM emails WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    @staticmethod
    def validate_email(email):
        is_valid = True
        query = "SELECT * FROM emails where email = %(email)s;"
        results = connectToMySQL(Email.db_name).query_db(query, email)
        #test whether a field matches the pattern
        if len(results) >= 1:
            flash("Email already taken.")
            is_valid = False
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid email address")
            is_valid = False
        return is_valid