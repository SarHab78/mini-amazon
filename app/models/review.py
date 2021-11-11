from flask import current_app as app


class Product_review:
    def __init__(self, rid, pid, uid, email, timestamp, rating, review):
        self.rid = rid
        self.pid = pid
        self.uid = uid
        self.email = email
        self.timestamp = timestamp
        self.rating = rating
        self.review = review

    @staticmethod
    def get_prod(pid):
        rows = app.db.execute('''
SELECT rid, pid, uid, email, timestamp, rating, review
FROM product_review
WHERE pid = :pid
''',
                              rid=rid)
        return product_review(*(rows[0])) if rows is not None else None
