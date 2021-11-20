from flask import current_app as app


class Sellers:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased
        
    @staticmethod
    def get_all_sellers():
        rows = app.db.execute('''
SELECT id
FROM Users
WHERE is_seller = 'Y'
''')
        return Sellers(*(rows[0])) if rows else None
