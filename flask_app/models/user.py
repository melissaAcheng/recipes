from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.controllers import users
from flask import flash
import re 
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name = 'recipes'

    # constructor
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # class methods
    # CREATE
    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)


    # READ
    # Get one user by email
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        # if no email found
        if len(result) < 1:
            return False
        return cls(result[0])

    # Get one user by id
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)

        # if no email found
        if len(result) < 1:
            return False
        return cls(result[0])


    # static methods 
    # validate user registration
    @staticmethod
    def validate_registration(user):
        is_valid = True

        # check if email is in database already
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db_name).query_db(query, user)

        # email validations
        if len(results) >= 1:
            is_valid = False
            flash("Email already taken", "reg_error")
        if not EMAIL_REGEX.match(user['email']): 
            is_valid = False
            flash("Please enter valid email address", "reg_error")
        
        # check first name, last name
        if len(user['first_name']) < 2:
            is_valid = False
            flash("First name must be least 2 characters", "reg_error")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Last name must be least 2 characters", "reg_error")

        # check if passwords match
        if user['password'] != user['password_confirm']:
            is_valid = False
            flash("Last name must be least 2 characters", "reg_error")

        return is_valid


    # validate user login
    @staticmethod
    def validate_login(user):
        is_valid = True

        # run a query to get all emails in database
        query = "SELECT * FROM users WHERE email = %(email)s"    
        results = connectToMySQL(User.db_name).query_db(query, user)

        if len(results) < 1: # no users are found
            is_valid = False
            flash("Invalid login credentials.", "login_error")
    

        return is_valid