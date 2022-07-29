from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, abort, request
import secrets
from db import db as default_db

class User:
    def __init__(self, db=default_db):
        self._db = db

    def login(self, username, password):
        sql = """SELECT id, username, password
                    FROM Users
                    WHERE username=:username"""
        user = self._db.session.execute(sql,
                                {"username":username}).fetchone()
        if not user:
            return False
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        return False

    def register_user(self, username, password, email):
        hash_value = generate_password_hash(password)
        values_to_db = {"username":username,
                        "password":hash_value,
                        "email": email}

        if not self.check_if_username_exists(username):
            sql = """INSERT INTO Users (username,
                                        password,
                                        email)
                        VALUES (:username,
                                :password,
                                :email)"""
            self._db.session.execute(sql, values_to_db)
            self._db.session.commit()
            self.login.user(username, password)
            return True
        return False

    def check_if_username_exists(self, username):
        sql = """SELECT username
                FROM Users
                WHERE username=:username"""
        return bool(self._db.session.execute(sql,
                        {"username":username}).fetchall())

    def modify_user_email(self, sql):
        try:
            self._db.session.execute(sql)
            self._db.session.commit()
            return True
        except:
            return False

    def logout(self):
        del session["user_id"]
        del session["username"]
        del session['csrf_token']

    def check_csrf(self):
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

    def get_user_id(self):
        return session.get("user_id", 0)


user_repository = User()