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

CREATE TABLE cart_total(
    uid REFERENCES Users PRIMARY KEY,
    totalitems INTEGER NOT NULL,
    totalcost INTEGER NOT NULL,
    orderID INTEGER NOT NULL REFERENCES total,
    inprogress BOOLEAN default TRUE
);

CREATE TABLE total (
    pid INTEGER NOT NULL REFERENCES products,
    uid INTEGER NOT NULL REFERENCES Users,
    orderID INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (pid)
);

CREATE TABLE ordertotal(
    orderID REFERENCES total NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    fulfilled BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (orderID)
);

CREATE TABLE balance(
    uid REFERENCES Users NOT NULL,
    credit INTEGER NOT NULL,
    PRIMARY KEY (uid)
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


CREATE FUNCTION TF_balance() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT * FROM  Users
  WHERE balance < 0 
  THEN 
  RAISE EXCEPTION 'Balance has fallen below 0';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_balance
  BEFORE INSERT OR UPDATE ON Users
  FOR EACH ROW
  EXECUTE PROCEDURE TF_balance();

CREATE FUNCTION CheckBalance() RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (SELECT * FROM balance, total
  WHERE balance.card<total.totalcost
  THEN 
  RAISE EXCEPTION 'Insufficient funds';
 IF EXISTS (SELECT * FROM balance, total
  WHERE balance.card>total.totalcost
  THEN 
EXECUTE PROCEDURE UpdateBalance();

  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER InsufFunds()
  BEFORE INSERT OR UPDATE ON total
  FOR EACH ROW
  EXECUTE PROCEDURE CheckBalance();

CREATE PROCEDURE UpdateBalance() 
AS
BEGIN //how to access seller’s balance from here?
  SET balance.card = balance.card - total.totalcost AND seller.balance = seller.balance + total.totalcost
UPDATE balance.card, seller.balance
END