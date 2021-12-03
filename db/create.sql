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
    product_id INT UNIQUE NOT NULL PRIMARY KEY, --GENERATED BY DEFAULT AS IDENTITY
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

CREATE TABLE product_review(
    rid VARCHAR(100) NOT NULL, --GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    uid INT NOT NULL, --REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(product_id),
    email VARCHAR(256) UNIQUE NOT NULL, --REFERENCES Users(email),
    rev_timestamp TIMESTAMP, --DEFAULT current_timestamp,
    rating INT NOT NULL,
    review VARCHAR(100) NOT NULL,
    UNIQUE(uid, pid)
);

CREATE TABLE Orders(
    prod_id INT NOT NULL REFERENCES Products(product_id),
    uid INT NOT NULL REFERENCES Users(id),
    order_quantity INT NOT NULL,
    date timestamp without time zone NOT NULL DEFAULT  (current_timestamp AT TIME ZONE 'UTC'),
    ordered VARCHAR(256) UNIQUE NOT NULL,
    PRIMARY KEY(uid, prod_id)
);
