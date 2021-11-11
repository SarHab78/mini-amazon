from flask import current_app as app


class Product_review:
    def __init__(self, review_id, product_id, uid, rating, review):
        self.review_id = review_id
        self.product_id = product_id
        self.uid = uid
        self.rating = rating
        self.review = review

    @staticmethod
    def get_prod(product_id):
        rows = app.db.execute('''
SELECT review_id, product_id, uid, rating, review
FROM product_review
WHERE product_id = :product_id
''',
                              review_id=review_id)
        return product_review(*(rows[0])) if rows is not None else None
