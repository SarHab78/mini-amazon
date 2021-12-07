--DO NOT CHANGE NAMES OF THINGS!!!!!!!
Create Table Users(
	id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
	firstname VARCHAR(256) NOT NULL,
	lastname VARCHAR(256) NOT NULL,
    email VARCHAR(256) UNIQUE NOT NULL,
	pwd VARCHAR(256) NOT NULL,
	address VARCHAR (256)NOT NULL,
	balance INTEGER NOT NULL,
	is_seller VARCHAR(2) NOT NULL
);

CREATE TABLE Products (
    product_name VARCHAR(255) NOT NULL,
    product_id INT UNIQUE NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    product_description VARCHAR(255) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    --link VARCHAR(255) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    seller_id INT NOT NULL REFERENCES Users(id),
    quantity INT NOT NULL,
    available VARCHAR(10) NOT NULL
);
-- might need a trigger so that seller_id always corresponds to a seller

CREATE TABLE Category(
    cat_name VARCHAR(255) NOT NULL,
    pid INT UNIQUE NOT NULL,
    PRIMARY KEY(pid),
    FOREIGN KEY (pid) REFERENCES Products(product_id)
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(product_id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Product_review(
    rid VARCHAR(500) NOT NULL PRIMARY KEY, --GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    pid INT NOT NULL, --REFERENCES Products(product_id),
    uid INT NOT NULL, --REFERENCES Users(id),
    email VARCHAR(256) NOT NULL, --REFERENCES Users(email),
    rev_timestamp TIMESTAMP DEFAULT current_timestamp,
    rating INT NOT NULL,
    review VARCHAR(500) NOT NULL
    --UNIQUE(uid, pid)
);

CREATE TABLE seller_review(
    rid VARCHAR(500) NOT NULL PRIMARY KEY, --GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    uid INT NOT NULL, --REFERENCES Users(id),
    sid INT NOT NULL, --REFERENCES --Products(seller_id),
    email VARCHAR(256) NOT NULL, --REFERENCES Users(email),
    rev_timestamp TIMESTAMP DEFAULT current_timestamp,
    rating INT NOT NULL,
    review VARCHAR(100) NOT NULL
    --UNIQUE(uid, sid)
);

CREATE TABLE Orders(
    prod_id INT NOT NULL REFERENCES Products(product_id),
    uid INT NOT NULL REFERENCES Users(id),
    order_quantity INT NOT NULL,
    add_date TIMESTAMP, --DEFAULT current_timestamp,    
    ordered VARCHAR(256) NOT NULL
    -- PRIMARY KEY(uid, prod_id, ordered)
);

CREATE VIEW Prod_Sell_Rev_Cat AS(
    SELECT PUR.product_name, PUR.product_id, PUR.product_description, PUR.image_url, PUR.price, PUR.quantity,
    PUR.firstname, PUR.lastname, PUR.email, PUR.address, PUR.id, PUR.available, PUR.avg_rating, C.cat_name
    FROM(
        SELECT PU.product_name, PU.product_id, PU.product_description, PU.image_url, PU.price, PU.quantity,
        PU.firstname, PU.lastname, PU.email, PU.address, PU.id, PU.available, ROUND(R.avg_rating, 1) AS avg_rating
        FROM (SELECT P.product_name, P.product_id, P.product_description, P.image_url, P.price, P.quantity, P.available,
            U.firstname, U.lastname, U.email, U.address, U.id
            FROM Products AS P, Users AS U
            WHERE P.seller_id = U.id) AS PU, 
            (SELECT product_id, avg_rating
            FROM Products AS Prod
            LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
                    FROM product_review
                    GROUP BY pid)
                    AS Rev
            ON Prod.product_id = Rev.pid) AS R
            WHERE PU.product_id = R.product_id) AS PUR, Category AS C
            WHERE PUR.product_id = C.pid
);

CREATE VIEW Prod_Sell_Rev_Cat_Ord AS(
	SELECT PORC.product_name, PORC.product_id, PORC.product_description, PORC.image_url, PORC.price, PORC.seller_id, PORC.quantity,
    PORC.available, PORC.uid, PORC.order_quantity, PORC.add_date, PORC.ordered, PORC.avg_rating, PORC.cat_name,
		U.id, U.firstname, U.lastname, U.address, U.email
		FROM
    (SELECT POR.product_name, POR.product_id, POR.product_description, POR.image_url, POR.price, POR.seller_id, POR.quantity,
    POR.available, POR.uid, POR.order_quantity, POR.add_date, POR.ordered, POR.avg_rating, C.cat_name
    FROM(
        SELECT PO.product_name, PO.product_id, PO.product_description, PO.image_url, PO.price, PO.seller_id, PO.quantity,
        PO.available, PO.uid, PO.order_quantity, PO.add_date, PO.ordered, ROUND(R.avg_rating, 1) AS avg_rating
        FROM (SELECT P.product_name, P.product_id, P.product_description, P.image_url, P.price, P.seller_id, P.quantity, P.available,
            O.uid, O.order_quantity, O.add_date, O.ordered
            FROM Products AS P, Orders AS O
            WHERE P.product_id = O.prod_id) AS PO, 
            (SELECT product_id, avg_rating
            FROM Products AS Prod
            LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
                    FROM product_review
                    GROUP BY pid)
                    AS Rev
            ON Prod.product_id = Rev.pid) AS R
            WHERE PO.product_id = R.product_id) AS POR, Category AS C
            WHERE POR.product_id = C.pid) AS PORC, Users as U
						WHERE PORC.uid = U.id
);
CREATE VIEW Product_Review_User_Information AS(
    SELECT pr.rid, pr.pid, pr.email, u.id, u.firstname, u.lastname
    FROM Product_review as pr, Users as u
    Where pr.uid = u.id);

CREATE VIEW Seller_Review_User_Information AS(
    SELECT sr.rid, sr.sid, sr.email, u.id, u.firstname, u.lastname
    FROM Seller_review as sr, Users as u
    Where sr.sid = u.id);


CREATE FUNCTION TF_insertProduct() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT * 
    FROM Products
    WHERE seller_id = NEW.seller_id
    AND product_name = NEW.product_name
    AND product_id <> NEW.product_id) 
    THEN
    RAISE EXCEPTION 'You already have a product with this name, %. Please update that product instead.', NEW.product_name;
    END IF;
  -- YOUR IMPLEMENTATION GOES HERE
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TF_insertProduct
  BEFORE INSERT ON Products
  FOR EACH ROW
  EXECUTE PROCEDURE TF_insertProduct();
