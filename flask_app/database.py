import sqlite3


conn = sqlite3.connect("films.db")

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
        added_by TEXT,
        film_id INTEGER,
        FOREIGN KEY(film_id) REFERENCES FILMS(film_id)
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

conn.cursor().execute('''
CREATE TABLE IF NOT EXISTS RATINGS
    (
        rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rating INTEGER NOT NULL,
        film_id INTEGER,
        FOREIGN KEY(film_id) REFERENCES FILMS(film_id)
    )
''')

conn.commit()


class DB:
    def __enter__(self):
        self.conn = sqlite3.connect("films.db")
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
