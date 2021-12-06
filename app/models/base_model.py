from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, firstname, lastname, email, address, balance, is_seller):
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
    def register(email, password, firstname, lastname, address, balance, is_seller):
        try:
            rows = app.db.execute("""
INSERT INTO Users(firstname, lastname, email, pwd, address, balance, is_seller)
VALUES(:firstname, :lastname, :email, :password, :address, :balance, :is_seller)
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
class Add_Product:
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
    def add_product(product_name, product_description, image_url, price, seller_id, quantity, available):
        try:
            rows = app.db.execute("""
INSERT INTO Products(product_name, product_description, image_url, price, seller_id, quantity, available)
VALUES(:product_name, :product_description, :image_url, :price, :seller_id, :quantity, :available)
RETURNING user
""",
#changed line 146 from RETURNING nameS to RETURNING id
                                  product_name = product_name,  
                                  product_description= product_description,
                                  image_url=image_url,
                                  price=price,
                                  seller_id = seller_id,
                                  quantity = quantity,
                                  available = available
                                  
            )
            
        except Exception:
            return None

#Product table information
class Product:
    def __init__(self, product_name, product_id, product_description, image_url, price, seller_id, quantity, available, avg_rating):
        self.product_name = product_name
        self.product_id = product_id
        self.product_description = product_description
        self.image_url = image_url
        self.price = price
        self.seller_id = seller_id
        self.quantity = quantity
        self.available = available
        self.avg_rating = avg_rating
        
    

    @staticmethod
    def get_seller_products(id):
        
        rows = app.db.execute('''
SELECT Prod.product_name, Prod.product_id, Prod.product_description, Prod.image_url, Prod.price, Prod.seller_id, Prod.quantity, Prod.available, ROUND(Rev.avg_rating,1) AS avg_rating
FROM (Products AS Prod
LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
        FROM product_review
        GROUP BY pid)
        AS Rev
ON Prod.product_id = Rev.pid), Users AS U
WHERE Prod.seller_id = :id
AND U.id = :id
AND U.is_seller = 'Y'
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
SELECT Prod.product_name, Prod.product_id, Prod.product_description, Prod.image_url, Prod.price, Prod.seller_id, Prod.quantity, Prod.available, ROUND(Rev.avg_rating,1) AS avg_rating
FROM Products AS Prod
LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
    FROM product_review
    GROUP BY pid)
    AS Rev
ON Prod.product_id = Rev.pid
WHERE Prod.available = :available
        ''',
                                available = available)
        return [Product(*row) for row in rows] if rows else []


    @staticmethod
    def product_exists(product_name, seller_id ):
        rows = app.db.execute("""
SELECT Products.product_id, Products.product_name, Products.product_description, Products.image_url, Products.price, Products.seller_id, Products.quantity, Products.available
FROM Products, Users
WHERE Products.product_name = :product_name
AND Users.id = :seller_id
AND Products.seller_id = :seller_id
""",
                              product_name=product_name,
                              seller_id = seller_id
                               
                              )
        return len(rows)>0

    @staticmethod
    def get_search_result_2(search_str='', available='Y', order_by = 'price'):
        if order_by == 'name':
            rows = app.db.execute('''
SELECT Prod.product_name, Prod.product_id, Prod.product_description, Prod.image_url, Prod.price, Prod.seller_id, Prod.quantity, Prod.available, Rev.avg_rating
FROM Products AS Prod
LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
    FROM product_review
    GROUP BY pid)
    AS Rev
ON Prod.product_id = Rev.pid
WHERE Prod.available = :available
AND LOWER(Prod.product_name) LIKE :search_str OR LOWER(Prod.product_description) LIKE :search_str
ORDER BY Prod.product_name
    ''',
                                search_str = '%' + search_str.lower() + '%', available=available, order_by = order_by)
        elif order_by == 'rating':
            rows = app.db.execute('''
    SELECT Prod.product_name, Prod.product_id, Prod.product_description, Prod.image_url, Prod.price, Prod.seller_id, Prod.quantity, Prod.available, Rev.avg_rating
    FROM Products AS Prod
    LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
        FROM product_review
        GROUP BY pid)
        AS Rev
    ON Prod.product_id = Rev.pid
    WHERE Prod.available = :available
    AND LOWER(Prod.product_name) LIKE :search_str OR LOWER(Prod.product_description) LIKE :search_str
    ORDER BY Rev.avg_rating DESC NULLS LAST
    ''',
                                search_str = '%' + search_str.lower() + '%', available=available, order_by = order_by)
        else:
            rows = app.db.execute('''
    SELECT Prod.product_name, Prod.product_id, Prod.product_description, Prod.image_url, Prod.price, Prod.seller_id, Prod.quantity, Prod.available, Rev.avg_rating
    FROM Products AS Prod
    LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
        FROM product_review
        GROUP BY pid)
        AS Rev
    ON Prod.product_id = Rev.pid
    WHERE Prod.available = :available
    AND LOWER(Prod.product_name) LIKE :search_str OR LOWER(Prod.product_description) LIKE :search_str
    ORDER BY Prod.price DESC
    ''',
                                search_str = '%' + search_str.lower() + '%', available=available, order_by = order_by)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_product_for_page(product_id='', available='Y'):
        rows = app.db.execute('''
SELECT Prod.product_name, Prod.product_id, Prod.product_description, Prod.image_url, Prod.price, Prod.seller_id, Prod.quantity, Prod.available, Rev.avg_rating
FROM Products AS Prod
LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
    FROM product_review
    GROUP BY pid)
    AS Rev
ON Prod.product_id = Rev.pid
WHERE Prod.available = :available
AND Prod.product_id = :product_id
''',
                              product_id = product_id, available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_products_by_other_sellers(product_id='', available='Y'):
        target_name = app.db.execute('''
SELECT product_name
FROM Products
WHERE available = :available 
AND product_id = :product_id
''',
                              product_id = product_id, available=available)
        target_name = ("").join([r for (r,) in target_name])
        rows = app.db.execute('''
SELECT product_name, product_id, product_description, image_url, price, seller_id, quantity, available, avg_rating
FROM Products AS Prod
LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
        FROM product_review
        GROUP BY pid)
        AS Rev
ON Prod.product_id = Rev.pid
WHERE available = :available 
AND product_name = :target_name
AND product_id <> :product_id
ORDER BY price, quantity
''',
                              product_id = product_id, available=available, target_name = target_name)
        return [Product(*row) for row in rows]


    @staticmethod
    def get_products_by_other_sellers(product_id='', available='Y'):
        target_name = app.db.execute('''
SELECT product_name
FROM Products
WHERE available = :available 
AND product_id = :product_id
''',
                              product_id = product_id, available=available)
        target_name = ("").join([r for (r,) in target_name])
        rows = app.db.execute('''
SELECT product_name, product_id, product_description, image_url, price, seller_id, quantity, available, avg_rating
FROM Products AS Prod
LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
        FROM product_review
        GROUP BY pid)
        AS Rev
ON Prod.product_id = Rev.pid
WHERE available = :available 
AND product_name = :target_name
AND product_id <> :product_id
ORDER BY price, quantity
''',
                              product_id = product_id, available=available, target_name = target_name)
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
        try:
            avg = ("").join(['{:.1f}'.format(a) for (a,) in avg])
        except:
            avg = 'N/A (no reviews yet)'
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
        try:
            count = ("").join([str(c) for (c,) in count])
        except:
            count = 'N/A (no reviews yet)'
        
        if count == '0':
            count = 'N/A (no reviews yet)'
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


    @staticmethod
    def get_cart(uid):
        rows = app.db.execute('''
SELECT Orders.prod_id, Orders.uid, Orders.order_quantity, Orders.date, Orders.ordered
FROM Orders, Products
WHERE Orders.prod_id = Products.product_id AND Orders.ordered = 'N' AND Orders.uid = :uid
        ''',uid= uid)
        return [Products(*row) for row in rows] 


    # @staticmethod
    # def add_to_cart(product_id, quantity, uid):
    #         if ordered = 'Y' and quantity > 0:
    #             rows = app.db.execute("""
    # SELECT CAST( GETDATE() AS Date )
    # INSERT INTO Orders(prod_id, uid, order_quantity, date, ordered)
    # VALUES(:product_id, :uid, 1, Date, 'N')
    # RETURNING prod_id
    # """, 
    #                             product_id= product_id,
    #                               uid = uid
    #         )
        #     return Orders.get_cart(prod_id, uid)
        # else:
        #     # add error message that is not available or quanitiy < 1
        #     return None

class Prod_Sell_Rev_Cat:
    def __init__(self, product_name, product_id, product_description, image_url, price, quantity, firstname, lastname, available, avg_rating, cat_name):
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.image_url = image_url
        self.quantity = quantity
        self.price = price
        self.firstname = firstname
        self.lastname = lastname
        self.avg_rating = avg_rating
        self.available = available
        self.cat_name = cat_name
    
    all_categories = tuple(['Automotive & Powersports','Baby Products','Beauty','Books','Camera & Photo','Cell Phones & Accessories','Collectible Coins','Consumer Electronics',
    'Entertainment Collectibles','Fine Art','Grocery & Gourmet Foods','Health & Personal Care','Home & Garden','Independent Design','Industrial & Scientific','Major Appliances','Misc','Music and DVD','Musical Instruments',
    'Office Products','Outdoors','Personal Computers','Pet Supplies','Software','Sports','Sports Collectibles','Tools & Home Improvement','Toys & Games',
    'Video, DVD & Blu-ray','Video Games','Watches'])

    @staticmethod
    def get_sell_rev_info(product_id):
        rows = app.db.execute('''
SELECT *
FROM Prod_Sell_Rev_cat
WHERE Prod_Sell_Rev_Cat.product_id = :product_id
        ''',product_id= product_id)
        return [Prod_Sell_Rev_Cat(*row) for row in rows]

    def get_quant_list(product_id):
        quant = app.db.execute('''
SELECT quantity
FROM Prod_Sell_Rev_Cat
WHERE Prod_Sell_Rev_Cat.product_id = :product_id
        ''',product_id= product_id)

        quant = int(('').join([str(q) for (q,) in quant]))
        quant_list = [0]*quant
        for i in range(0,quant):
            quant_list[i] = i+1

        return quant_list

    @staticmethod
    def get_products_by_other_sellers(product_id='', available='Y'):
        target_name = app.db.execute('''
SELECT product_name
FROM Prod_Sell_Rev_Cat
WHERE available = :available 
AND product_id = :product_id
''',
                              product_id = product_id, available=available)
        target_name = ("").join([r for (r,) in target_name])
        rows = app.db.execute('''
SELECT *
FROM Prod_Sell_Rev_Cat
WHERE available = :available 
AND product_name = :target_name
AND product_id <> :product_id
        ''',target_name=target_name, available=available, product_id=product_id)
        return [Prod_Sell_Rev_Cat(*row) for row in rows]

    @staticmethod
    def get_search_result(search_str='', available='Y', order_by = 'price', direc='high-to-low', filt_list=all_categories):
        base_query = '''
        SELECT * 
        FROM Prod_Sell_Rev_Cat 
        WHERE available = :available 
        AND (LOWER(product_name) LIKE :search_str OR LOWER(product_description) LIKE :search_str) 
        AND cat_name IN :filt_list
            '''
        ending = ''
        if direc == 'high-to-low':
            if order_by == 'name':
                ending = ' ORDER BY product_name DESC'
            elif order_by == 'rating':
                ending = ' ORDER BY avg_rating DESC NULLS LAST'
            else:
                ending = ' ORDER BY price DESC'
        else:
            if order_by == 'name':
                ending = ' ORDER BY product_name ASC'
            elif order_by == 'rating':
                ending = ' ORDER BY avg_rating ASC NULLS LAST'
            else:
                 ending = ' ORDER BY price ASC'
        full_query = base_query + ending

        rows = app.db.execute(full_query,
                            search_str = '%' + search_str.lower() + '%', available=available, order_by = order_by, direc=direc, filt_list=filt_list)

        return [Prod_Sell_Rev_Cat(*row) for row in rows]
    
    @staticmethod
    def get_top_rated(available = 'Y'):
        rows = app.db.execute('''
SELECT *
FROM Prod_Sell_Rev_Cat
ORDER BY avg_rating DESC NULLS LAST, price DESC
        ''',
                                available = available)
        return [Prod_Sell_Rev_Cat(*row) for row in rows][0:10] if rows else []

    def get_all(available = 'Y'):
        rows = app.db.execute('''
SELECT *
FROM Prod_Sell_Rev_Cat
ORDER BY avg_rating DESC NULLS LAST, price DESC
        ''',
                                available = available)
        return [Prod_Sell_Rev_Cat(*row) for row in rows] if rows else []