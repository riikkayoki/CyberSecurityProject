
from db import db as default_db

class Messages:
    def __init__(self, db=default_db):
        self._db = db

    def create_message(self, message):
        sql = '''INSERT INTO Messages (message)
                    VALUES (:message)'''
        self._db.session.execute(sql, {"message":message})
        self._db.session.commit()
           

    def get_all_messages(self):
        sql = '''SELECT * FROM Messages'''
        return self._db.session.execute(sql).fetchall()

message_service = Messages()