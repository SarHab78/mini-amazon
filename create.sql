-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    uid INT GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    address VARCHAR(256) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    balance INTEGER NOT NULL,
    PRIMARY KEY (system_id, email),
    UNIQUE email

);

CREATE TABLE Seller (
    uid INTEGER NOT NULL REFERENCES Users 
)

CREATE TABLE Category (
    cat_name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE Purchase_History(
    uid INTEGER NOT NULL REFERENCES Users, 
    purchase_name INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    number_of_items INTEGER NOT NULL,
    status VARCHAR(256) NOT NULL,
    time TIMESTAMP NOT NULL,
    (uid, purchase_name) PRIMARY KEY;
);


CREATE TABLE Products (
    cat_name references Category,
    pid INT NOT NULL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price FLOAT NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Purchases (
    uid INT NOT NULL references Users,
    pid INT NOT NULL PRIMARY KEY,
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Product_Review (
    uid VARCHAR(256) REFERENCES Users NOT NULL,
    product_name VARCHAR(256) REFERENCES products NOT NULL,
    review_time TIMESTAMP(256) NOT NULL,
    rating INTEGER NOT NULL,
    review VARCHAR(256) NOT NULL,
    PRIMARY KEY(uid, product_name)
);

CREATE TABLE Seller_review (
    uid VARCHAR(256) REFERENCES Users NOT NULL,
    seller_name VARCHAR(256) REFERENCES Users NOT NULL,
    review_time TIMESTAMP(256) NOT NULL,
    rating INTEGER NOT NULL,
    review VARCHAR(256) NOT NULL,
    PRIMARY KEY(uid, seller_name)
);
CREATE TABLE orders_fulfilled(
   user REFERENCES UID PRIMARY KEY,
   prod REFERENCES product_id PRIMARY KEY,
   order _quantity INTEGER NOT NULL,
   Date INTEGER default NULL
);

CREATE FUNCTION TF_email() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT * FROM  Users
  WHERE email = NEW.email AND system_id <> NEW.system_id 
  THEN 
  RAISE EXCEPTION 'Email already exists';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_email
  BEFORE INSERT OR UPDATE ON Users
  FOR EACH ROW
  EXECUTE PROCEDURE TF_email();



