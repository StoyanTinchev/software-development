from database import DB


class Comment:
    def __init__(self, comment_id, post, message):
        self.comment_id = comment_id
        self.post = post
        self.message = message

    def create(self):
        with DB() as db:
            values = (self.post.film_id, self.message)
            db.execute('INSERT INTO COMMENTS (film_id, message) VALUES (?, ?)', values)
            return self

    @staticmethod
    def find_by_film(post):
        with DB() as db:
            rows = db.execute('SELECT * FROM comments WHERE film_id = ?', (post.film_id,)).fetchall()
            return [Comment(*row) for row in rows]
