from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app import app
from flask_app.models.user import User
from flask import flash

class Show:
    db = "tv_shows"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user']

# CREATE

    @classmethod
    def create_show(cls, data):
        query = """INSERT INTO shows (title, network, release_date, description, user_id) 
        VALUES (%(title)s, %(network)s, %(release_date)s, %(description)s, %(user_id)s)
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

# READ

    @classmethod
    def read_all_shows(cls):
        query = """ 
        SELECT * 
        FROM shows JOIN users ON shows.user_id = users.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_shows = []
        for row in results:
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            this_user = User(user_data)
            row["user"] = this_user
            all_shows.append(cls(row))
        return all_shows

    @classmethod
    def read_by_id(cls, data):
        query = """
        SELECT * FROM shows JOIN users on shows.user_id = users.id WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        row = results[0]
        user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
        this_user = User(user_data)
        row['user'] = this_user
        return cls(row)

# UPDATE

    @classmethod
    def update_show(cls, data):
        query = """
        UPDATE shows
        SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, user_id = %(user_id)s, updated_at = NOW()
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

# DELETE

    @classmethod
    def delete_show(cls, data):
        query = """
        DELETE FROM shows
        WHERE id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)
        
# Validation

    @staticmethod
    def validate_show(show):
        is_valid = True
        if len(show['title']) < 3:
            flash("Title must be at least 3 character")
            is_valid = False
        if len(show['network']) < 3:
            flash("Network must be at least 3 characters")
            is_valid = False
        if len(show['description']) < 3:
            flash("Description must be at least 3 characters")
            is_valid = False
        if show['release_date'] == "":
            flash("Please enter a date")
            is_valid = False
        return is_valid
