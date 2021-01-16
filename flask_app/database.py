import sqlite3

DB_NAME = 'films.db'

conn = sqlite3.connect(DB_NAME)

conn.cursor().execute('''
    CREATE TABLE IF NOT EXISTS FILMS 
    (
        film_id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT, 
        author TEXT, 
        content TEXT
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS COMMENTS
    (
        comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        film_id INTEGER,
        FOREIGN KEY(film_id) REFERENCES FILMS(id)
    )
''')

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS USERS
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect(DB_NAME)
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
