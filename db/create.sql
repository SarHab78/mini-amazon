-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

Create Table Users(
	id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
	email VARCHAR(256) UNIQUE NOT NULL,
	pwd VARCHAR(256) NOT NULL,
	address VARCHAR (256)NOT NULL,
	firstname VARCHAR(256) NOT NULL,
	lastname VARCHAR(256) NOT NULL,
	balance INTEGER NOT NULL,
	is_seller VARCHAR(2) NOT NULL
);


CREATE TABLE Category (
    cat_name VARCHAR(255) UNIQUE NOT NULL
);

--need to update with sophie's changes--
CREATE TABLE Products (
    name VARCHAR(255) UNIQUE NOT NULL,
    id INT NOT NULL PRIMARY KEY, --GENERATED BY DEFAULT AS IDENTITY,
    describe VARCHAR(255) NOT NULL,
    image_url VARCHAR(255) NOT NULL, 
    price DECIMAL(12,2) NOT NULL,
    seller_id INT NOT NULL REFERENCES Users(id),
    quantity INT NOT NULL,
    available VARCHAR(1)
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE product_review(
    id INT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    email VARCHAR(255) UNIQUE NOT NULL REFERENCES Users(email),
    rev_timestamp TIMESTAMP NOT NULL,
    rating INT NOT NULL,
    review VARCHAR(100) NOT NULL,
    UNIQUE(uid, pid)
);

CREATE TABLE Orders(
   user_id INT REFERENCES Users(id),
   prod_id INT REFERENCES Products(id),
   order_quantity INT NOT NULL,
   date_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

