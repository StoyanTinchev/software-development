from database import DB


class Rating:
    def __init__(self, rating_id, rating, film_id):
        self.rating_id = rating_id
        self.rating = rating
        self.film_id = film_id

    @staticmethod
    def create(rating, film_id):
        with DB() as db:
            values = (rating, film_id)
            db.execute('INSERT INTO RATINGS (rating,film_id) VALUES (?, ?)', values)
        return 'Ready'

    # @staticmethod
    # def find_by_film(film_id):
    #     with DB() as db:
    #         rows = db.execute('SELECT * FROM comments WHERE film_id = ?', film_id).fetchall()
    #         return [Rating(*row) for row in rows]
