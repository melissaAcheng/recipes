from flask_app.config.mysqlconnection import connectToMySQL

class User:

    db_name = "friendships_schema"

    #constructor

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        # instance method
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # class methods
    # CREATE - add new user
    @classmethod
    def create_user(cls, data):
        query = "INSERT INTO users (first_name, last_name) VALUES (%(first_name)s, %(last_name)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # CREATE new friendship
    @classmethod
    def create_friendship(cls, data):
        query = "INSERT INTO friendships (user_id, friend_id) VALUES (%(user_id)s, %(friend_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)


    # READ - GET all users
    @classmethod                      
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db_name).query_db(query)   # list of dict

        all_users = []  
        for user in results:
            all_users.append(cls(user))
        
        return all_users # list of objects

    # READ - GET all friendships
    @classmethod
    def get_friendships(cls):
        query = "SELECT * FROM friendships JOIN users on user_id = users.id JOIN users as friends ON friend_id = friends.id;"

        results = connectToMySQL(cls.db_name).query_db(query) # returns a list of dictionary
        

        friends = []

        for row in results:

            friendship_data = {
                "id": row["id"],
                "user_id": row["user_id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "friend_id": row["friends.id"],
                "friend_first_name": row["friends.first_name"],
                "friend_last_name": row["friends.last_name"],
            }
            
            # append data 
            friends.append(friendship_data)

        # print("FRIENDS", friends)
        return friends
    
    @classmethod
    def get_one_friendship(cls, data):
        query = "SELECT * FROM friendships WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s OR user_id = %(friend_id)s AND friend_id = %(user_id)s;"
        
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_friendship(cls, data):
        query = "DELETE FROM friendships WHERE id = %(id)s;"

        print("QUERY", query)

        return connectToMySQL(cls.db_name).query_db(query, data)

