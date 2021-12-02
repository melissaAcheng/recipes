from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import ninja

class Dojo:
    db_name = "dojos_and_ninjas"

    # constructor
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # list to store all ninjas associated with the dojo
        self.ninjas = []
    
    # class methods
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query)

        # turn list of dict into obj
        # create empty list to store obj
        all_dojos = []
        for row in results:
            one_dojo = cls(row)
            all_dojos.append(one_dojo)
        
        return all_dojos

    @classmethod
    def create_dojo(cls, data):
        query = "INSERT INTO dojos (name) VALUES (%(name)s);"
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)

        return results

    @classmethod
    def get_dojo_with_ninjas(cls, data):
        query = "SELECT * FROM dojos LEFT JOIN ninjas on dojos.id = ninjas.dojo_id WHERE dojos.id = %(id)s;"
        results = connectToMySQL("dojos_and_ninjas_schema").query_db(query, data)
        # print(results)

        one_dojo = cls(results[0])

        for row_from_db in results:
            ninja_data = {
                "id": row_from_db["ninjas.id"],
                "first_name": row_from_db["first_name"],
                "last_name": row_from_db["last_name"],
                "age": row_from_db["age"],
                "created_at": row_from_db["ninjas.created_at"],
                "updated_at": row_from_db["ninjas.updated_at"]
            }
            one_dojo.ninjas.append(ninja.Ninja(ninja_data))
        return one_dojo