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
    image_url VARCHAR(255) NOT NULL,
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
    PRIMARY KEY(cat_name, pid),
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
    rid VARCHAR(100) NOT NULL, --GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    uid INT NOT NULL, --REFERENCES Users(id),
    sid INT NOT NULL, --REFERENCES --Products(seller_id),
    email VARCHAR(256) UNIQUE NOT NULL, --REFERENCES Users(email),
    rev_timestamp TIMESTAMP, --DEFAULT current_timestamp,
    rating INT NOT NULL,
    review VARCHAR(100) NOT NULL
    --UNIQUE(uid, sid)
);

CREATE TABLE Orders(
    prod_id INT NOT NULL REFERENCES Products(product_id),
    uid INT NOT NULL REFERENCES Users(id),
    order_quantity INT NOT NULL,
    date timestamp without time zone NOT NULL DEFAULT  (current_timestamp AT TIME ZONE 'UTC'),
    ordered VARCHAR(256) UNIQUE NOT NULL,
    PRIMARY KEY(uid, prod_id)
);

CREATE VIEW Prod_Sell_Rev AS(
    SELECT PU.product_name, PU.product_id, PU.product_description, PU.image_url, PU.price, PU.quantity,
    PU.firstname, PU.lastname, PU.available, ROUND(R.avg_rating, 1) AS avg_rating
    FROM (SELECT P.product_name, P.product_id, P.product_description, P.image_url, P.price, P.quantity, P.available,
        U.firstname, U.lastname
        FROM Products AS P, Users AS U
        WHERE P.seller_id = U.id) AS PU, 
        (SELECT product_id, avg_rating
        FROM Products AS Prod
        LEFT JOIN (SELECT AVG(rating) AS avg_rating, pid
                FROM product_review
                GROUP BY pid)
                AS Rev
        ON Prod.product_id = Rev.pid) AS R
        WHERE PU.product_id = R.product_id
);