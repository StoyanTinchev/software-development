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