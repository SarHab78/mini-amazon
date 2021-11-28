from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, addr, pwd, balance, is_seller):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.addr = addr
        self.pwd = pwd
        self.balance = balance
        self.is_seller = is_seller

    @staticmethod
    def get_by_auth(email, pwd):
        rows = app.db.execute("""
SELECT pwd, id, email, firstname, lastname, addr, balance, is_seller
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], pwd):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, pwd, firstname, lastname, addr, balance, is_seller):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, pwd, firstname, lastname, addr, balance, is_seller)
VALUES(:email, :pwd, :firstname, :lastname, :addr, :balance, :is_seller)
RETURNING id
""",
                                  email=email,
                                  pwd=generate_password_hash(pwd),
                                  firstname=firstname,
                                  lastname=lastname,
                                  addr= addr,
                                  balance = balance,
                                  is_seller = is_seller)
            id = rows[0][0]
            return User.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, addr, balance, is_seller
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None



#Purchase table information
        
class Purchase:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]


#Product table information
class Product:
    def __init__(self, product_id, product_name, product_description, image_url, price, available):
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.image_url = image_url
        self.price = price
        self.available = available

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT product_id, product_name, product_description, image_url, price, available
FROM Products
WHERE product_id = :product_id
''',
                              product_id=product_id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available='Y'):
        rows = app.db.execute('''
SELECT product_id, product_name, product_description, image_url, price, available
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_search_result(search_str='', available='Y'):
        rows = app.db.execute('''
SELECT product_id, product_name, product_description, image_url, price, available
FROM Products
WHERE available = :available 
AND LOWER(product_name) LIKE :search_str OR LOWER(product_description) LIKE :search_str
ORDER BY price
''',
                              search_str = '%' + search_str.lower() + '%', available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_search_result_2(search_str='', available='Y', order_by = 'price'):
        if order_by == 'name':
            rows = app.db.execute('''
    SELECT product_id, product_name, product_description, image_url, price, available
    FROM Products
    WHERE available = :available 
    AND LOWER(product_name) LIKE :search_str OR LOWER(product_description) LIKE :search_str
    ORDER BY product_name
    ''',
                                search_str = '%' + search_str.lower() + '%', available=available, order_by = order_by)
        else:
            rows = app.db.execute('''
    SELECT product_id, product_name, product_description, image_url, price, available
    FROM Products
    WHERE available = :available 
    AND LOWER(product_name) LIKE :search_str OR LOWER(product_description) LIKE :search_str
    ORDER BY price DESC
    ''',
                                search_str = '%' + search_str.lower() + '%', available=available, order_by = order_by)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_product_for_page(product_id='', available='Y'):
        rows = app.db.execute('''
SELECT product_id, product_name, product_description, image_url, price, available
FROM Products
WHERE available = :available 
AND product_id = :product_id
''',
                              product_id = product_id, available=available)
        return [Product(*row) for row in rows]



##add to git

class Product_review:
    def __init__(self, rid, pid, uid, email, timestamp, rating, review):
        self.rid = rid
        self.pid = pid
        self.uid = uid
        self.email = email
        self.timestamp = timestamp
        self.rating = rating
        self.review = review
#possibly rename review attr because it could fuck stuff up who knows


    @staticmethod
    def get_prod_reviews(pid):
        rows = app.db.execute('''
SELECT rid, pid, uid, email, timestamp, rating, review
FROM product_review
WHERE pid = :pid
''',
                              rid=rid)
        return product_review(*(rows[0])) if rows is not None else None


    @staticmethod
    def add_review(rid, pid, uid, email, timestamp, rating, review):
        try:
            rows = app.db.execute("""
INSERT INTO Reviews(rid, pid, uid, email, timestamp, rating, review)
VALUES(:rid, :pid, :uid, :email, :timestamp, :rating, :review)
RETURNING nameS
""", ##what is nameS
                                  rid=rid,
                                  pid= pid,
                                  uid=uid,
                                  email=email,
                                  timestamp= timestamp,
                                  rating = rating,
                                  review = review,
            )
            return Review.get_prod_reviews(pid)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None


   