from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import time
from wtforms.fields import DateTimeField


from .. import login

#user class (elements from Users table in create.sql)
class User(UserMixin):
    def __init__(self, id, firstname, lastname, email, address, balance, is_seller):
        self.id = id
        self.email = firstname
        self.firstname = lastname
        self.lastname = email
        self.address = address
        self.balance = balance
        self.is_seller = is_seller

#method to decrease balance after a user purchases something
    @staticmethod
    def decrement_balance(id, balance, total):
        bal = app.db.execute("""
    Update User
    SET balance = balance - total
    WHERE id = :id """,
                    balance = balance, 
                    total = total
                    
)
        return bal

#authorizes user based on email and password
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

#checks to see if a user is a seller (is_seller='Y')
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

#registration method--inserts values into Users table in database
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

#gets all information about a user based on their User ID
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

#method to edit a profile--updates elements in Users table in the database by using User ID as a key
    @staticmethod
    def edit(id, email, password, firstname, lastname, address, balance, is_seller):
        #try:
            rows = app.db.execute("""
UPDATE Users
SET email = :email, pwd = :password, firstname = :firstname, lastname = :lastname, address = :address, balance  = :balance, is_seller = :is_seller
WHERE id = :id
RETURNING id, email, pwd, firstname, lastname, address, balance, is_seller
""",
                                  id=id,
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname,
                                  lastname=lastname,
                                  address= address,
                                  balance = balance,
                                  is_seller = is_seller)
            id = rows[0][0]
            print(rows)
            return User.get(id)
        #except Exception:
            # likely email already in use; better error checking and
            # reporting needed
          #  return 'test'

#below are a series of methods that can be used to edit individual profile elements by updating just that element in the Users table
    @staticmethod
    def edit_firstname(id, firstname):
        #try:
            rows = app.db.execute("""
UPDATE Users
SET(Users.firstname = :firstname)
WHERE id = :id
RETURNING id, firstname
""",
                                  id=id,
                                  firstname=firstname
                                  )
            id = rows[0][0]
            print(rows)
            return User.get(id)
        #except Exception:
            # likely email already in use; better error checking and
            # reporting needed
          #  return 'test'
 
    @staticmethod
    def edit_lastname(id, lastname):
        #try:
            rows = app.db.execute("""
UPDATE Users
SET(lastname = :lastname)
WHERE id = :id
RETURNING id, lastname
""",
                                  id=id,
                                  lastname=lastname
                                  )
            id = rows[0][0]
            print(rows)
            return User.get(id)

    @staticmethod
    def edit_email(id, email):
        #try:
            rows = app.db.execute("""
UPDATE Users
SET(email = :email)
WHERE id = :id
RETURNING id, email
""",
                                  id=id,
                                  email=email
                                  )
            id = rows[0][0]
            print(rows)
            return User.get(id)

    @staticmethod
    def edit_address(id, address):
        #try:
            rows = app.db.execute("""
UPDATE Users
SET(address = :address)
WHERE id = :id
RETURNING id, address
""",
                                  id=id,
                                  address=address
                                  )
            id = rows[0][0]
            print(rows)
            return User.get(id)

    @staticmethod
    def edit_balance(id, balance):
        #try:
            rows = app.db.execute("""
UPDATE Users
SET balance = :balance
WHERE id = :id
RETURNING id, balance
""",
                                  id=id,
                                  balance=balance
                                  )
            id = rows[0][0]
            print(rows)
            return User.get(id)

    @staticmethod
    def edit_is_seller(id, is_seller):
        #try:
            rows = app.db.execute("""
UPDATE Users
SET(is_seller = :is_seller)
WHERE id = :id
RETURNING id, is_seller
""",
                                  id=id,
                                  is_seller=is_seller
                                  )
            id = rows[0][0]
            print(rows)
            return User.get(id)

    @staticmethod
    def edit_password(id, password):
        #try:
            rows = app.db.execute("""
UPDATE Users
SET(password = :password)
WHERE id = :id
RETURNING id, password
""",
                                  id=id,
                                  password=password
                                  )
            id = rows[0][0]
            print(rows)
            return User.get(id)
#end update methods
    


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
        
        #how to add to a table with an new product, a trigger is reference on update of this so that conditions are met
    @staticmethod
    def add_product(product_name, product_description, image_url, price, seller_id, quantity, available):
        try:
            rows = app.db.execute("""
INSERT INTO Products(product_name, product_description, image_url, price, seller_id, quantity, available)
VALUES(:product_name, :product_description, :image_url, :price, :seller_id, :quantity, :available)
RETURNING seller_id
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
#this makes sure to add to the category table by first getting the newly generated product id and then adding that and the category selected on the form to the correct table. 
    @staticmethod
    def add_category(category, product_name):
        add_to_category = app.db.execute("""
SELECT product_id
FROM Products
WHERE product_name = :product_name
""",
        product_name = product_name)
        
        
        
        add_to_category = ("").join([str(r) for (r,) in add_to_category])
        print(type(add_to_category))
        try:
            rows = app.db.execute('''
        INSERT INTO Category(cat_name, pid)
        VALUES(:category, :add_to_category)
        RETURNING pid
        ''',
                                    category = category, add_to_category = add_to_category)

        except Exception:
            return None


          
        

    @staticmethod
    def update_product(product_id, seller_id, quantity, available):
        try:
            rows = app.db.execute("""
UPDATE Products
SET quantity = :quantity, available = :available
WHERE product_id = :product_id
AND seller_id = :seller_id
RETURNING seller_id
""",
#changed line 146 from RETURNING nameS to RETURNING id
                                  product_id = product_id, 
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
        
    
#this makes sure to get all the necessary information for a product, including the rating and the product information so that users can get enough detail about a product. 
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
AND available = 'Y'
''',
                                product_id = product_id)

  
  
        return [Product(*row) for row in rows] if rows else []

   
#this only gets products that have the correct available designation of Y
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
    def product_can_be_updated(product_id):
        rows = app.db.execute("""
SELECT Products.product_id, Products.product_name, Products.product_description, Products.image_url, Products.price, Products.seller_id, Products.quantity, Products.available
FROM Products, Users
WHERE Products.product_id = :product_id
""",
                              product_id=product_id
                             
                               
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


        
class Product_review:
    def __init__(self, rid, pid, uid, email, rev_timestamp, rating, review):
        self.rid = rid
        self.pid = pid
        self.uid = uid
        self.email = email
        self.rev_timestamp = rev_timestamp
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
ORDER BY rev_timestamp DESC
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
ORDER BY rev_timestamp DESC
''',
                              uid=uid)
        return [Product_review(*row) for row in rows] 

    
    @staticmethod
    def user_has_reviewed(uid, pid):
        rows = app.db.execute('''
SELECT rid, pid, uid, email, rev_timestamp, rating, review
FROM product_review
WHERE uid = :uid
AND pid = :pid
''',
                              uid=uid,
                              pid=pid)
        return len(rows)>0 


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

#get by review id
    @staticmethod
    def get(rid):
        rows = app.db.execute('''
SELECT rid, pid, uid, email, rev_timestamp, rating, review
FROM product_review
WHERE rid = :rid
''',
                              rid=rid)
        return [Product_review(*row) for row in rows]

    
    @staticmethod
    def delete(rid):
        rows = app.db.execute("""
DELETE FROM Product_review 
WHERE rid = :rid
RETURNING *
""",
                                    rid=rid)
        return [Product_review(*row) for row in rows]

        


#edit a review
    @staticmethod
    def edit(rid, pid, uid, email, rating, review):
        #try:
            rows = app.db.execute("""
UPDATE Product_review
SET rid = :rid, pid = :pid, uid = :uid, email = :email, rev_timestamp = NOW()::TIMESTAMP, rating  = :rating, review = :review
WHERE rid = :rid
RETURNING rid, pid, uid, email, rev_timestamp, rating, review
""",
                                    rid=rid,
                                    pid=pid,
                                    uid=uid,
                                    email=email,
                                    rating=rating,
                                    review= review)
            id = rows[0][0]
            print(rows)
            return Product_review.get(id)




class Add_review:
    def __init__(self, rid, pid, uid, email, rev_timestamp, rating, review):
        self.rid = rid
        self.pid = pid
        self.uid = uid
        self.email = email
        self.rev_timestamp = rev_timestamp
        self.rating = rating
        self.review = review

    @staticmethod
    def add_review(rid, pid, uid, email, rating, review):
        try:
            print("are you even trying")
            rows = app.db.execute("""
INSERT INTO Product_review(rid, pid, uid, email, rev_timestamp, rating, review) 
VALUES(:rid, :pid, :uid, :email, NOW()::TIMESTAMP, :rating, :review)
RETURNING rid
""", 
                                  rid=str(rid),
                                  pid= int(pid),
                                  uid=int(uid),
                                  email=str(email),
                                  #rev_timestamp= rev_timestamp,
                                  rating = int(rating),
                                  review = str(review)
            )
           # return Product_review.get(rid)
        except Exception:
            print('exception. not added to db :( ')
            # likely email already in use; better error checking and
            # reporting needed
            return None


class Seller_review:
    def __init__(self, rid, uid, sid, email, rev_timestamp, rating, review):
        self.rid = rid
        self.uid = uid
        self.sid = sid
        self.email = email
        self.rev_timestamp = rev_timestamp
        self.rating = rating
        self.review = review

    @staticmethod
    def get_seller_reviews(sid):
        rows = app.db.execute('''
SELECT rid, uid, sid, email, rev_timestamp, rating, review
FROM seller_review
WHERE sid = :sid
ORDER BY rev_timestamp
''',
                              sid=sid)
        return [Seller_review(*row) for row in rows] 


    @staticmethod
    def get_users_reviews(uid):
        rows = app.db.execute('''
SELECT rid, uid, sid, email, rev_timestamp, rating, review
FROM Seller_review
WHERE uid = :uid
ORDER BY rev_timestamp DESC
''',
                              uid=uid)
        return [Seller_review(*row) for row in rows] 


    @staticmethod
    def count_seller_reviews(sid):
        count = app.db.execute('''
SELECT COUNT(rating)
FROM seller_review
WHERE sid = :sid
''',
                            sid=sid)
        try:
            count = ("").join([str(c) for (c,) in count])
        except:
            count = 'N/A (no reviews yet)'
        
        if count == '0':
            count = 'N/A (no reviews yet)'
        return count

    #get by review id
    @staticmethod
    def get(rid):
        rows = app.db.execute('''
SELECT rid, uid, sid, email, rev_timestamp, rating, review
FROM seller_review
WHERE rid = :rid
''',
                              rid=rid)
        return [Seller_review(*row) for row in rows]


    @staticmethod
    def delete(rid):
        rows = app.db.execute("""
DELETE FROM Seller_review 
WHERE rid = :rid
RETURNING *
""",
                                    rid=rid)
        return [Seller_review(*row) for row in rows]


#average rating for a product
    @staticmethod
    def avg_seller_rating(sid):
        avg = app.db.execute('''
SELECT AVG(rating)
FROM seller_review
WHERE sid = :sid
''',
                            sid=sid)
        try:
            avg = ("").join(['{:.1f}'.format(a) for (a,) in avg])
        except:
            avg = 'N/A (no reviews yet)'
        return avg #change

    @staticmethod
    def edit(rid, uid, sid, email, rating, review):
        #try:
            rows = app.db.execute("""
UPDATE Seller_review
SET rid = :rid, uid = :uid, sid = :sid, email = :email, rev_timestamp = NOW()::TIMESTAMP, rating  = :rating, review = :review
WHERE rid = :rid
RETURNING rid, uid, sid, email, rev_timestamp, rating, review
""",
                                    rid=rid,
                                    uid=uid,
                                    sid=sid,
                                    email=email,
                                    rating=rating,
                                    review= review)
            id = rows[0][0]
            print(rows)
            return Seller_review.get(id)
    
#check if user has an existing seller review
    @staticmethod
    def user_has_reviewed(uid, sid):
        rows = app.db.execute('''
SELECT rid, uid, sid, email, rev_timestamp, rating, review
FROM Seller_review
WHERE uid = :uid
AND sid = :sid
''',
                              uid=uid,
                              sid=sid)
        return len(rows)>0 


    @staticmethod
    def stest():
        print('this is a method')
        return None
    
    @staticmethod
    def add_seller_review(rid, uid, sid, email, rating, review):
        try:
            print("are you even trying")
            rows = app.db.execute("""
INSERT INTO Seller_review(rid, uid, sid, email, rev_timestamp, rating, review) 
VALUES(:rid, :uid, :sid, :email, NOW()::TIMESTAMP, :rating, :review)
RETURNING rid
""", 
                                  rid=str(rid),
                                  uid= int(uid),
                                  sid=int(sid),
                                  email=str(email),
                                  #rev_timestamp= rev_timestamp,
                                  rating = int(rating),
                                  review = str(review)
            )
           # return Product_review.get(rid)
        except Exception:
            print('exception. not added to db :( ')
            # likely email already in use; better error checking and
            # reporting needed
            return None

    
# class takes care of all things in orders table
class Orders:
    def __init__(self, prod_id, uid, order_quantity, add_date, ordered):
        self.prod_id = prod_id
        self.uid = uid
        self.order_quantity = order_quantity
        self.add_date = add_date
        self.ordered = ordered
    # allows items to be deleted, buggy right now
    @staticmethod
    def delete_item(uid, prod_id, add_date):
        delete = app.db.execute('''
DELETE FROM Orders
WHERE uid = :uid AND prod_id = :prod_id AND add_date = :add_date
RETURNING *
        ''',
                uid= uid,
                prod_id = prod_id,
                add_date = add_date)
        return Orders.get_cart(uid)

# changes values in carts to indicate the item haas been purchased and is no longer in the cart
    @staticmethod
    def checkout_cart(uid):
        rows = app.db.execute('''
UPDATE Orders
SET ordered = 'Y' 
WHERE ordered = 'N' AND uid = :uid
RETURNING uid
        ''',
                uid= uid)
        return Orders.get_cart(uid)
# accessing past orders using ordered = 'y' that is changed from n to y when person checks out
    @staticmethod
    def past_orders(uid):
        rows = app.db.execute('''
SELECT *
FROM Orders
WHERE Orders.ordered = 'Y' AND Orders.uid = :uid
        ''',
        
                        uid = uid)
        return [Orders(*row) for row in rows] 

# grabs all data inside the cart table when they have not yet checked out
    @staticmethod
    def get_cart(uid):
        rows = app.db.execute('''
SELECT Orders.prod_id, Orders.uid, Orders.order_quantity, Orders.add_date, Orders.ordered
FROM Orders, Products
WHERE Orders.prod_id = Products.product_id AND Orders.ordered = 'N' AND Orders.uid = :uid
        ''',uid= uid)
        return [Orders(*row) for row in rows] 
    
    @staticmethod
    def add_to_cart(prod_id, quantity, uid, add_date):
        rows = app.db.execute("""
    INSERT INTO Orders
    VALUES (:prod_id, :uid, :quantity, :add_date, 'N')
    RETURNING uid
    """, 
                                uid = uid,
                                prod_id = prod_id,
                                quantity = quantity,
                                add_date = add_date
            )
        return Orders.get_cart(uid)


    @staticmethod
    def user_has_bought(prod_id, uid):
        rows = app.db.execute('''
SELECT *
FROM Orders
WHERE prod_id = :prod_id
AND ordered = 'Y'
AND uid = :uid
ORDER BY add_date DESC
        ''',uid= uid,
            prod_id = prod_id)
        return len(rows) > 0

#add seller reviews
class Add_seller_review:
    def __init__(self, uid, sid, email, rev_timestamp, rating, review):
        self.rid = rid
        self.uid = uid
        self.sid = sid
        self.email = email
        self.rev_timestamp = rev_timestamp
        self.rating = rating
        self.review = review

    @staticmethod
    def add_review(rid, uid, sid, email, rating, review):
        try:
            rows = app.db.execute("""
INSERT INTO Reviews(rid, uid, sid, email, rating, review)
VALUES(:rid, :uid, :sid, :email, :rating, :review)
RETURNING rid
""", 
                                  rid= rid,
                                  uid= int(uid),
                                  sid=sid,
                                  email=email,
                                 # rev_timestamp= rev_timestamp,
                                  rating = rating,
                                  review = review,
            )
            #return Product_review.get(rid)
        except Exception:
            # likely email already in use; better error checking and
            # reporting needed
            return None

#this references a view that was created in create.sql to join the product, user/seller, review, and category tables to get all the necessary information for the following functions
class Prod_Sell_Rev_Cat:
    def __init__(self, product_name, product_id, product_description, image_url, price, quantity, firstname, lastname, email, address, id, available, avg_rating, cat_name):
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.image_url = image_url
        self.quantity = quantity
        self.price = price
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.address = address
        self.id = id
        self.avg_rating = avg_rating
        self.available = available
        self.cat_name = cat_name
       
    
        
        
    #predefined list of categories
    all_categories = tuple(['Automotive & Powersports','Baby Products','Beauty','Books','Camera & Photo','Cell Phones & Accessories','Collectible Coins','Clothing','Consumer Electronics',
    'Entertainment Collectibles','Fine Art','Grocery & Gourmet Foods','Health & Personal Care','Home & Garden','Independent Design','Industrial & Scientific','Major Appliances','Misc','Music and DVD','Musical Instruments',
    'Office Products','Outdoors','Personal Computers','Pet Supplies','Software','Sports','Sports Collectibles','Tools & Home Improvement','Toys & Games',
    'Video DVD & Blu-ray','Video Games','Watches'])

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
        if filt_list == 'all':
            filt_list = Prod_Sell_Rev_Cat.all_categories
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
            elif order_by == 'category':
                ending = ' ORDER BY cat_name DESC'
            else:
                ending = ' ORDER BY price DESC'
        else:
            if order_by == 'name':
                ending = ' ORDER BY product_name ASC'
            elif order_by == 'rating':
                ending = ' ORDER BY avg_rating ASC NULLS LAST'
            elif order_by == 'category':
                ending = ' ORDER BY cat_name ASC'
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

#this references a view that is created from the products, users, reviews, categories, and orders table to get all the necessary information for the following functions
class Prod_Sell_Rev_Cat_Ord:
    def __init__(self, product_name, product_id, product_description, image_url, price, seller_id, quantity, available, uid, order_quantity, add_date, ordered, avg_rating, cat_name, id, firstname, lastname, address, email):
        self.product_name = product_name
        self.product_id = product_id
        self.product_description = product_description
        self.image_url = image_url
        self.price = price
        self.seller_id = seller_id
        self.quantity = quantity
        self.available = available
        self.uid = uid
        self.order_quantity = order_quantity
        self.add_date = add_date
        self.ordered = ordered
        self.avg_rating = avg_rating
        self.cat_name = cat_name
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.email = email

       #predefined categories list
    all_categories = tuple(['Automotive & Powersports','Baby Products','Beauty','Books','Camera & Photo','Cell Phones & Accessories','Collectible Coins','Clothing','Consumer Electronics',
    'Entertainment Collectibles','Fine Art','Grocery & Gourmet Foods','Health & Personal Care','Home & Garden','Independent Design','Industrial & Scientific','Major Appliances','Misc','Music and DVD','Musical Instruments',
    'Office Products','Outdoors','Personal Computers','Pet Supplies','Software','Sports','Sports Collectibles','Tools & Home Improvement','Toys & Games',
    'Video DVD & Blu-ray','Video Games','Watches'])  
    

    def get_sellers_and_incs(self):
        l = [''] * len(self)
        l2 = [''] * len(self)
        for i in range(0, len(l)):
            l[i] = self[i].seller_id
            l2[i] = float(self[i].price * self[i].order_quantity)

        d = dict(zip(l, l2))
        return(d)
    
    def get_buyers_and_decs(self):
        if len(self) > 0:
            l = [self[0].uid]
            l2 = [0]
            for i in range(0, len(self)):
                l2[0] = l2[0] + float(self[i].price * self[i].order_quantity)

            d = dict(zip(l, l2))
            return(d)
        else:
            return {}
    
    def get_products_and_decs(self):
        l = [''] * len(self)
        l2 = [''] * len(self)
        for i in range(0, len(l)):
            l[i] = self[i].product_id
            l2[i] = int(self[i].order_quantity)

        d = dict(zip(l, l2))
        return(d)
    
    @staticmethod
    def get_cart(uid):
        rows = app.db.execute('''
SELECT *
FROM Prod_Sell_Rev_Cat_Ord
WHERE ordered = 'N' AND uid = :uid
        ''',uid= uid)
        return [Prod_Sell_Rev_Cat_Ord(*row) for row in rows] 

        
    @staticmethod
    def checkout_cart(uid, sellers_amounts_dict, buyers_amounts_dict, products_amounts_dict):
        skeys = sellers_amounts_dict.keys()
        pkeys = products_amounts_dict.keys()

        ###### update orders - set Ordered to Y where appropriate
        rows = app.db.execute('''
    UPDATE Orders
    SET ordered = 'Y' 
    WHERE ordered = 'N' AND uid = :uid
    RETURNING uid
            ''',
                    # add_date = add_date,
                    uid= uid)

    @staticmethod
    def get_cart_all_info(id):
        rows = app.db.execute('''
SELECT *
FROM Prod_Sell_Rev_Cat_Ord
WHERE ordered = 'N' AND uid = :uid
        ''',uid= uid)
        return [Prod_Sell_Rev_Cat_Ord(*row) for row in rows] 

    @staticmethod
    def make_sure_user_can_purchase(id, amount):
    # get the buyer's current balance
            buy_current_balance = app.db.execute('''
    SELECT balance
    FROM Users
    WHERE id = :id
            ''',
                    id = id)

            # format the buyer's current balance
            buy_current_balance = float(("").join([str(float(r)) for (r,) in buy_current_balance]))

            # if you're trying to purchase more than your balance
            if amount > buy_current_balance:
                return 0
            return 1
        
    @staticmethod
    def checkout_cart(uid, sellers_amounts_dict, buyers_amounts_dict, products_amounts_dict):
        skeys = sellers_amounts_dict.keys()
        pkeys = products_amounts_dict.keys()

        ###### update orders - set Ordered to Y where appropriate
        rows = app.db.execute('''
    UPDATE Orders
    SET ordered = 'Y' 
    WHERE ordered = 'N' AND uid = :uid
    RETURNING uid
            ''',
                    # add_date = add_date,
                    uid= uid)
        
        ####### Loop through sellers and make corresponding changes
        for k in skeys:
            seller_id = k
            amount = sellers_amounts_dict[k]

            # get the seller's current balance
            sell_current_balance = app.db.execute('''
    SELECT balance
    FROM Users
    WHERE id = :seller_id
            ''',
                    seller_id = seller_id)

            # format the seller's current balance
            sell_current_balance = float(("").join([str(float(r)) for (r,) in sell_current_balance]))
            
            # increment the seller's balance
            rows = app.db.execute('''
    UPDATE Users
    SET balance = :new_amount
    WHERE id = :seller_id
    RETURNING id
            ''',
                    seller_id = seller_id,
                    new_amount = sell_current_balance + amount)

        ##### Make changes to buyres
        buyer_id = uid
        buy_amount = buyers_amounts_dict[buyer_id]

        # get the buyer's current balance
        buy_current_balance = app.db.execute('''
SELECT balance
FROM Users
WHERE id = :buyer_id
        ''',
                buyer_id = buyer_id)

        # format the buyer's current balance
        buy_current_balance = float(("").join([str(float(r)) for (r,) in buy_current_balance]))
        
        # decrement the buyer's balance
        rows = app.db.execute('''
UPDATE Users
SET balance = :new_amount
WHERE id = :buyer_id
RETURNING id
        ''',
                buyer_id = buyer_id,
                new_amount = buy_current_balance - buy_amount)

        ###### Loop through products and make the changes
        for k in pkeys:
            product_id = k
            quant = products_amounts_dict[k]

            # get the product's current quantity
            prod_current_quant = app.db.execute('''
    SELECT quantity
    FROM Products
    WHERE product_id = :product_id
            ''',
                    product_id = product_id)

            # format the product's current quantity
            prod_current_quant = int(("").join([str(r) for (r,) in prod_current_quant]))
            
            # decrement the product's quantity
            rows = app.db.execute('''
    UPDATE Products
    SET quantity = :new_amount
    WHERE product_id = :product_id
    RETURNING product_id
            ''',
                    product_id = product_id,
                    new_amount = prod_current_quant - quant)
        
        return Prod_Sell_Rev_Cat_Ord.get_cart(uid)


    @staticmethod
    def get_all(seller_id):
        rows = app.db.execute('''
SELECT *
FROM Prod_Sell_Rev_Cat_Ord
WHERE Prod_Sell_Rev_Cat_Ord.seller_id= :seller_id
ORDER BY Prod_Sell_Rev_Cat_Ord.add_date DESC

        ''', seller_id = seller_id)

       # get_prod_id = ("").join([str(r) for (r,) in get_prod_id])
        print(rows)
        return [Prod_Sell_Rev_Cat_Ord(*row) for row in rows] if rows else []
        

    @staticmethod
    def get_search_result(seller_id, search_str='', order_by = 'price', direc='high-to-low', filt_list=all_categories):
        all_categories = tuple(['Automotive & Powersports','Baby Products','Beauty','Books','Camera & Photo','Cell Phones & Accessories','Collectible Coins','Clothing','Consumer Electronics',
    'Entertainment Collectibles','Fine Art','Grocery & Gourmet Foods','Health & Personal Care','Home & Garden','Independent Design','Industrial & Scientific','Major Appliances','Misc','Music and DVD','Musical Instruments',
    'Office Products','Outdoors','Personal Computers','Pet Supplies','Software','Sports','Sports Collectibles','Tools & Home Improvement','Toys & Games',
    'Video DVD & Blu-ray','Video Games','Watches'])  
    
        if filt_list == 'all':
           filt_list = all_categories
        
        base_query = '''
        SELECT * 
        FROM Prod_Sell_Rev_Cat_Ord 
        WHERE Prod_Sell_Rev_Cat_Ord.seller_id = :seller_id
        AND (LOWER(product_name) LIKE :search_str OR LOWER(product_description) LIKE :search_str) 
        AND cat_name IN :filt_list
            '''
        ending = ''
        if direc == 'high-to-low':
            if order_by == 'name':
                ending = ' ORDER BY Prod_Sell_Rev_Cat_Ord.product_name DESC'
            elif order_by == 'rating':
                ending = ' ORDER BY avg_rating DESC NULLS LAST'
            elif order_by == 'category':
                ending = ' ORDER BY Prod_Sell_Rev_Cat_Ord.cat_name DESC'
            else:
                ending = ' ORDER BY Prod_Sell_Rev_Cat_Ord.price DESC'
        else:
            if order_by == 'name':
                ending = ' ORDER BY Prod_Sell_Rev_Cat_Ord.product_name ASC'
            elif order_by == 'rating':
                ending = ' ORDER BY Prod_Sell_Rev_Cat_Ord.avg_rating ASC NULLS LAST'
            elif order_by == 'category':
                ending = ' ORDER BY Prod_Sell_Rev_Cat_Ord.cat_name ASC'
            else:
                 ending = ' ORDER BY Prod_Sell_Rev_Cat_Ord.price ASC'
        full_query = base_query + ending

        rows = app.db.execute(full_query,
                            search_str = '%' + search_str.lower() + '%',  order_by = order_by, direc=direc, filt_list=filt_list, seller_id = seller_id)

        return [Prod_Sell_Rev_Cat_Ord(*row) for row in rows]


class Seller_Information:
    def __init__(self, product_name, product_id, firstname, lastname, email, address, id):
        self.product_name = product_name
        self.product_id = product_id
        self.firstname=firstname
        self.lastname=lastname
        self.email=email
        self.address=address
        self.id = id

    @staticmethod
    def get_information(product_id):
        rows = app.db.execute('''
SELECT p.product_name, p.product_id, u.firstname, u.lastname, u.email, u.address, u.id
FROM Products as p
FULL OUTER JOIN Users as u
ON p.seller_id = u.id
WHERE p.product_id = :product_id
        ''',
                                product_id = product_id)
        return [Seller_Information(*row) for row in rows] 
#corresponds to a view used to get information about people who have written product reviews so their info can be displayed

class Prod_user_rev:
    def __init__(self, rid, pid, email, id, firstname, lastname):
        self.rid=rid
        self.pid=pid
        self.email=email
        self.id=id
        self.firstname=firstname
        self.lastname=lastname

#gets information about a user based on their review that corresponds to a product_review
    @staticmethod
    def get_user_info(pid):
        rows = app.db.execute('''
SELECT *
FROM Product_Review_User_Information
WHERE Product_Review_User_Information.pid = :pid
        ''',pid= pid)
        return [Prod_user_rev(*row) for row in rows]

class Sell_user_rev:
    def __init__(self, rid, sid, email, id, firstname, lastname):
        self.rid=rid
        self.sid=sid
        self.email=email
        self.id=id
        self.firstname=firstname
        self.lastname=lastname

#gets information about a user based on their review that corresponds to a product_review
    @staticmethod
    def get_user_info(sid):
        rows = app.db.execute('''
SELECT *
FROM Seller_Review_User_Information
WHERE Seller_Review_User_Information.sid = :sid
        ''',sid= sid)
        return [Sell_user_rev(*row) for row in rows]


#corresponds to a view in create.sql to get information from products, users, and orders for the order history element on the profile page
class Past_Order_Info:
    def __init__(self, prod_id, uid, order_quantity, add_date, ordered, product_name, price, seller_id, cat_name, total_spent):
        self.prod_id=prod_id
        self.uid=uid
        self.order_quantity=order_quantity
        self.add_date=add_date
        self.ordered=ordered
        self.product_name = product_name
        self.price = price
        self.seller_id = seller_id
        self.cat_name = cat_name
        self.total_spent=total_spent

    @staticmethod
    def get_user_orders(uid):
        rows = app.db.execute('''
SELECT *
FROM Past_Order_Info
WHERE Past_Order_Info.uid = :uid
AND ordered = 'Y'
ORDER BY add_date DESC
        ''',uid= uid)
        return [Past_Order_Info(*row) for row in rows]

    
    
    
          
