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
    def can_sell(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address, balance, is_seller
FROM Users
WHERE id = :id
AND is_seller = 'Y'
""",
                              id=id)
        return ['Y'] if rows else []


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
    def __init__(self, product_name, product_id, product_description, image_url, price, seller_id, quantity, available):
        self.product_name = product_name
        self.product_id = product_id
        self.product_description = product_description
        self.image_url = image_url
        self.price = price
        self.seller_id = seller_id
        self.quantity = quantity
        self.available = available
        
    @staticmethod
    def add_product(product_name, product_id, product_description, image_url, price, seller_id, quantity, available):
        try:
            rows = app.db.execute("""
INSERT INTO Products(product_name, product_id, product_description, image_url, price, seller_id, quantity, available)
VALUES(:product_name, :id, :product_description, :image_url, :price, :seller_id, :quantity, :available)
RETURNING id 
""",
#changed line 146 from RETURNING nameS to RETURNING id
                                  product_id=product_id,
                                  describe= product_description,
                                  image_url=image_url,
                                  price=price,
                                  seller_id= seller_id,
                                  quantity = quantity,
                                  available = available,
                                  product_name = product_name
            )
            return User.get(id)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None

    @staticmethod
    def get_seller_products(id):
        
        rows = app.db.execute('''
SELECT Products.product_id, Products.product_name, Products.product_description, Products.image_url, Products.price, Products.seller_id, Products.quantity, Products.available
FROM Products, Users
WHERE Products.seller_id = :id
AND Users.id = :id
AND Users.is_seller = 'Y'
''',
                                id = id)

  
  
        return [Product(*row) for row in rows] if rows else []

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
SELECT product_name, product_id, product_description, image_url, price, seller_id, quantity, available
FROM Products
WHERE product_id = :product_id
''',
                                product_id = product_id)

  
  
        return [Product(*row) for row in rows] if rows else []


    @staticmethod
    def get_all(available = 'Y'):
        rows = app.db.execute('''
SELECT product_name, product_id, product_description, image_url, price, seller_id, quantity, available
FROM Products
WHERE available = :available
        ''',
                                available = available)
        return [Product(*row) for row in rows] if rows else []


    @staticmethod
    def product_exists(product_name, product_id):
        rows = app.db.execute("""
SELECT Products.product_id, Products.product_name, Products.product_description, Products.image_url, Products.price, Products.seller_id, Products.quantity, Products.available
FROM Products, Users
WHERE Products.product_name = :product_name
AND Users.id = :id
""",
                              product_name=product_name
                              )
        return len(rows) > 0

    @staticmethod
    def get_search_result(search_str='', available='Y'):
        rows = app.db.execute('''
SELECT product_name, product_id, product_description, image_url, price, seller_id, quantity, available
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
SELECT product_name, product_id, product_description, image_url, price, seller_id, quantity, available
FROM Products
WHERE available = :available 
AND LOWER(product_name) LIKE :search_str OR LOWER(product_description) LIKE :search_str
ORDER BY product_name
    ''',
                                search_str = '%' + search_str.lower() + '%', available=available, order_by = order_by)
        else:
            rows = app.db.execute('''
    SELECT product_name, product_id, product_description, image_url, price, seller_id, quantity, available
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
SELECT product_name, product_id, product_description, image_url, price, seller_id, quantity, available
FROM Products
WHERE available = :available 
AND product_id = :product_id
''',
                              product_id = product_id, available=available)
        return [Product(*row) for row in rows]



##add to git - all functions for reviews

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


#to get reviews for a specific product id
    @staticmethod
    def get_prod_reviews(pid):
        rows = app.db.execute('''
SELECT rid, pid, uid, email, rev_timestamp, rating, review
FROM product_review
WHERE pid = :pid
ORDER BY rev_timestamp
''',
                              pid=pid)
        return [Product_review(*row) for row in rows] 


#to get reviews written by a specific user
    @staticmethod
    def get_users_reviews(uid):
        rows = app.db.execute('''
SELECT rid, pid, uid, email, rev_timestamp, rating, review
FROM product_review
WHERE uid = :uid
ORDER BY rev_timestamp
''',
                              uid=uid)
        return [Product_review(*row) for row in rows] 


#average rating for a product
    @staticmethod
    def avg_product_rating(pid):
        avg = app.db.execute('''
SELECT AVG(rating)
FROM product_review
WHERE pid = :pid
''',
                            pid=pid)
        return avg #change

#number of reviews for a product
    @staticmethod
    def count_prod_reviews(pid):
        count = app.db.execute('''
SELECT COUNT(rating)
FROM product_review
WHERE pid = :pid
''',
                            pid=pid)
        return count


#add a review 
    @staticmethod
    def add_review(rid, pid, uid, email, timestamp, rating, review):
        try:
            rows = app.db.execute("""
INSERT INTO Reviews(rid, pid, uid, email, timestamp, rating, review)
VALUES(:rid, :pid, :uid, :email, :timestamp, :rating, :review)
RETURNING nameS
""", ##what is nameS?
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

class Orders:
    def __init__(self, prod_id, uid, order_quantity, date, ordered):
        self.prod_id = prod_id
        self.uid = uid
        self.order_quantity = order_quantity
        self.date = date
        self.ordered = ordered
   
