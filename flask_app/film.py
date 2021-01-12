from database import DB
from comment import Comment


class Film:
    def __init__(self, film_id, name, author, content):
        self.film_id = film_id
        self.name = name
        self.author = author
        self.content = content

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM FILMS').fetchall()
            return [Film(*row) for row in rows]

    @staticmethod
    def find(film_id):
        with DB() as db:
            row = db.execute('SELECT * FROM FILMS WHERE film_id = ?', (film_id,)).fetchone()
            if row is None:
                return
            return Film(*row)

    def create(self):
        with DB() as db:
            values = (self.name, self.author, self.content)
            db.execute('INSERT INTO FILMS (name, author, content) VALUES (?, ?, ?)', values)
            return self

    def save(self):
        with DB() as db:
            values = (self.name, self.author, self.content, self.film_id)
            db.execute('UPDATE FILMS SET name = ?, author = ?, content = ? WHERE film_id = ?', values)
            return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM FILMS WHERE film_id = ?', (self.film_id,))

    def comments(self):
        return Comment.find_by_film(self)
