\COPY Products FROM 'data/products_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Users FROM 'data/test_users_db.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY product_review FROM 'data/review_sample_DB_-_Sheet1.csv' WITH DELIMITER ',' NULL '' CSV

