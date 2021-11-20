from flask import current_app as app
from flask_wtf import FlaskForm
from flask_login import UserMixin
from .. import login


class Product_review(UserMixin):
    def __init__(self, rid, pid, uid, email, timestamp, rating, review):
        self.rid = rid
        self.pid = pid
        self.uid = uid
        self.email = email
        self.timestamp = timestamp
        self.rating = rating
        self.review = review

    @staticmethod
    def get_prod_reviews(pid):
        rows = app.db.execute('''
SELECT rid, pid, uid, email, timestamp, rating, review
FROM product_review
WHERE pid = :pid
''',
                              rid=rid)
        return product_review(*(rows[0])) if rows is not None else None
