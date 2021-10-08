\COPY Users FROM 'data/Users.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/Products.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV

INSERT into Users VALUES
    (1, 'homer@duke.edu', 'homersimpson12', '212 Simspon Way', 'Homer', 'Simpson', 100),
    (2, 'lisa@duke.edu', 'password', '310 Donut Street', 'Lisa', 'Simpson', 50),
    (3, 'rhea@duke.edu', 'pw321', '300 Swift Avenue', 'Rhea', 'Tejwani', 10000),
    (4, 'flannery@duke.edu', 'sejf203', '90 Duke Road', 'Flannery', 'Nania', 38),
    (5, 'sarah@duke.edu', '28457jhfse', '1 Chapel Boulevard', 'Sarah', 'Habib', 0),
    (6, 'jordan@duke.edu', '3456y7uijh', '100 Cameron Road', 'Jordan', 'Smith', 2948),
    (7, 'sophie@duke.edu', 'asdfb', '434 North Road', 'Sophie', 'Vincoff', 23487);


INSERT into Category VALUES
    ('technology'),
    ('kitchen'),
    ('books'),
    ('pets'),
    ('fashion');

INSERT into Purchase_History VALUES
    (1, 'purchase 2', 50, 1, 'shipped', '2021-10-06 10:00:00'),
    (2, 'purchase 22', 21, 1, 'ordered', '2021-10-06 11:00:00'),
    (3, 'purchase 8', 90, 2, 'in transit', '2021-10-06 12:00:00'),
    (4, 'purchase 16', 103, 4, 'shipped', '2021-10-06 13:00:00'),
    (5, 'purchase 1048', 291, 8, 'ordered', '2021-10-06 14:00:00');

INSERT into products VALUES
    ('technology', 302, 'computer', 1000, TRUE),
    ('kitchen', 130, 'mixer', 21, TRUE),
    ('books', 3, 'fundamentals of computer science', 50, TRUE),
    ('pets', 12309, 'dog toy', 5, FALSE),
    ('fashion', 8, 'boots', 831, TRUE);

INSERT into Purchases VALUES
    (1, 302, '2021-10-06 10:00:00'),
    (2, 130, '2021-10-06 11:00:00'),
    (3, 3, '2021-10-06 12:00:00'),
    (4, 12309, '2021-10-06 13:00:00'),
    (4, 8, '2021-10-06 13:00:00');

INSERT into Product_Review VALUES
    (1, 'computer', '2021-10-06 18:00:00', 3, 'I bought a computer on Amazon, so you get what you pay for.'),
    (2, 'computer', '2021-10-06 19:00:00', 5, 'Honestly the best thing I have ever used in my whole life'),
    (3, 'computer', '2021-10-06 20:00:00', 1, 'Worst thing I have ever used in my whole life'),
    (3, 'boots', '2021-10-06 21:00:00', 5, 'These boots are phenomenal. Most complements I have ever recieved'),
    (3, 'mixer', '2021-10-06 22:00:00', 2, 'I have seen worse and better. Very eh');

INSERT into Seller_review VALUES
    (1, 'Marge Simpson', '2021-10-07 18:00:00', 4, 'pretty good'),
    (2, 'Maggie Simpson', '2021-10-07 19:00:00', 1, 'Horrible! Like dealing with a baby'),
    (2, 'Professor Yang', '2021-10-07 20:00:00', 5, 'The best seller I have ever encountered'),
    (3, 'Professor Yang', '2021-10-07 21:00:00', 5, 'His book taught me so much about Database Systems'),
    (4, 'President Price', '2021-10-07 22:00:00', 3, 'He should stop selling on Amazon and go lead a University or something');

INSERT into cart_total VALUES
    (1, 2, 80, 219, TRUE),
    (2, 5, 1244, 259, TRUE),
    (3, 1, 21, 343, FALSE),
    (4, 2, 43, 233, TRUE),
    (5, 1, 4, 341, TRUE);

INSERT into total VALUES
    (302, 1, 219, 1),
    (130, 2, 259, 10),
    (3, 3, 343, 2),
    (12309, 4, 233, 3),
    (8, 5, 341, 5);

INSERT into ordertotal VALUES
    (219, '2021-10-07 08:00:00', FALSE),
    (259, '2021-10-07 09:00:00', TRUE),
    (343, '2021-10-07 10:00:00', TRUE),
    (233, '2021-10-07 11:00:00', FALSE),
    (341, '2021-10-07 12:00:00', FALSE);

INSERT into balance VALUES
    (1, 100),
    (2, 29),
    (3, 13),
    (4, 0),
    (5, 340);
