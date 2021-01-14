from database import DB


class Comment:
    def __init__(self, comment_id, message, film):
        self.comment_id = comment_id
        self.message = message
        self.film = film

    def create(self):
        with DB() as db:
            values = (self.film.film_id, self.message)
            db.execute('INSERT INTO COMMENTS (film_id, message) VALUES (?, ?)', values)
            return self

    @staticmethod
    def find_by_film(film):
        with DB() as db:
            rows = db.execute('SELECT * FROM COMMENTS WHERE film_id = ?', (film.film_id,)).fetchall()
            return [Comment(*row) for row in rows]
