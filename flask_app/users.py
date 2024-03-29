import hashlib

from database import DB


class User:
    def __init__(self, id, username, password):
        self.username = username
        self.password = password

    def create(self):
        with DB() as db:
            values = (self.username, self.password)
            db.execute('''
                INSERT INTO USERS (username, password)
                VALUES (?, ?)''', values)
            return self

    @staticmethod
    def validate_username(username):
        if not username:
            return False
        with DB() as db:
            row = db.execute(
                'SELECT * FROM USERS WHERE username = ?',
                (username,)
            ).fetchone()
            if row:
                return True
            else:
                return False

    @staticmethod
    def find_by_username(username):
        if not username:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM USERS WHERE username = ?',
                (username,)
            ).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def verify_password(self, password):
        return self.password == password
