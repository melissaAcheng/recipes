from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_name = 'recipes'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.time = data['time']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # class methods
    # CREATE
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, time, date, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(time)s, %(date)s, %(user_id)s);"
        
        return connectToMySQL(cls.db_name).query_db(query, data)

    # READ
    @classmethod
    def get_all_recipes(cls, data):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db_name).query_db(query, data)

        all_recipes = []
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes
        


    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

    # UPDATE
    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, time = %(time)s, date = %(date)s WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)


    # DELETE
    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    #static methods
    # Validate recipe form
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True

        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters long", "recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters long", "recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters long", "recipe")
        if recipe['date'] == "":
            is_valid = False
            flash("Please enter a date", "recipe")

        return is_valid