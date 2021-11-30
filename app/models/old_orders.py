from flask import current_app as app


class Orders:
    def __init__(self, prod_id, UID, order_quantity, date, ordered):
        self.prod_id = prod_id
        self.UID = UID
        self.order_quantity = order_quantity
        self.date = date
        self.ordered = ordered


    @staticmethod
    def get(UID):
        rows = app.db.execute('''
SELECT product, UID, order_quantity, date, ordered
FROM Orders
WHERE UID = :UID
''',
                              id=id)
        return Orders(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_cart(ordered="N"):
        rows = app.db.execute('''
SELECT product, UID, order_quantity, date, ordered
FROM Orders
WHERE ordered = :ordered
''',
                            #  available=available
                            )
        return [Orders(*row) for row in rows]
