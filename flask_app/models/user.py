from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
# from flask_app.models import show
from flask import flash, session
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_0]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    db = "tv_shows"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

# CREATE 

    @classmethod
    def create_user(cls,data):
        query = """
        INSERT INTO users (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        results= connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def login_user(cls, data):
        this_user = cls.read_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['first_name'] = this_user.first_name
                session['user_id'] = this_user.id
        return this_user

# READ

    @classmethod
    def read_by_email(cls,data):
        query = """
        SELECT * FROM users WHERE email = %(email)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_username(cls, data):
        query = "SELECT * FROM users WHERE first_name = %(first_name)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        else: 
            return cls(results[0])

    @classmethod
    def read_by_id(cls,data):
        query = """
        SELECT * FROM users WHERE id = %(id)s
        ;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


# validate user info

    @staticmethod
    def validate_register(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, {"email": user['email']})
        if len(results) > 0:
            flash("Email already taken", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email!")
            is_valid = False
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("Passwords don't match")
            is_valid = False
        return is_valid

