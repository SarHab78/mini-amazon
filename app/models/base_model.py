from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address, balance, is_seller):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.balance = balance
        self.is_seller = is_seller



    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT pwd, id, email, firstname, lastname, address, balance, is_seller
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
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
    def register(email, password, firstname, lastname, address, balance, is_seller):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, pwd, firstname, lastname, address, balance, is_seller)
VALUES(:email, :password, :firstname, :lastname, :address, :balance, :is_seller)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname,
                                  address= address,
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
SELECT id, email, firstname, lastname, address, balance, is_seller
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
    def __init__(self, id, name, describe, image_url, price, seller_id, quantity, available):
        self.id = id
        self.describe = describe
        self.name = name
        self.image_url = image_url
        self.price = price
        self.seller_id = seller_id
        self.quantity = quantity
        self.available = available


    @staticmethod
    def get_seller_products(id):
        
        rows = app.db.execute('''
SELECT Products.id, Products.describe, Products.name, Products.image_url, Products.price, Products.seller_id, Products.quantity, Products.available
FROM Products, Users
WHERE Products.seller_id = :id
AND Users.id = :id
AND Users.is_seller = 'Y'

''',
id = id)
       
        return [Product(*row) for row in rows] if rows else []

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, price, available
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available= 'Y'):
        rows = app.db.execute('''
SELECT *
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]


        
   