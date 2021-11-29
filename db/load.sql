\COPY Users FROM 'data/Users_stress_test_database.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/products_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY product_review FROM 'data/review_sample_DB_-_Sheet1.csv' WITH DELIMITER ',' NULL '' CSV

