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
	is_seller VARCHAR(1) NOT NULL
);

CREATE TABLE Category (
    cat_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE product_review(
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    uid INTEGER NOT NULL REFERENCES Users(id),
    pid INTEGER NOT NULL REFERENCES Products(id),
    email VARCHAR(256) UNIQUE NOT NULL REFERENCES Users(email),
    rev_timestamp TIMESTAMP NOT NULL,
    rating INTEGER NOT NULL,
    review VARCHAR(100) NOT NULL,
    UNIQUE(uid, pid)
);

CREATE TABLE Orders(
   user REFERENCES User(UID) PRIMARY KEY,
   prod REFERENCES Products(product_id) PRIMARY KEY,
   order _quantity INTEGER NOT NULL,
   Date INTEGER default NULL
);

