from database import DB


class Comment:
    def __init__(self, comment_id, message, film):
        self.comment_id = comment_id
        self.message = message
        self.film = film

    def create(self):
        with DB() as db:
            values = (self.message, self.film.film_id)
            db.execute('INSERT INTO COMMENTS (message, film_id) VALUES (?, ?)', values)
            return self

    @staticmethod
    def find_by_film(film):
        with DB() as db:
            rows = db.execute('SELECT * FROM COMMENTS WHERE film_id = ?', (film.film_id,)).fetchall()
            return [Comment(*row) for row in rows]
