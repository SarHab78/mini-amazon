\COPY Users FROM 'data/users_stress_test_db.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Users FROM 'data/temp_users_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/products_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Products FROM 'data/temp_products_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Category FROM 'data/category_stress_test_db.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Category FROM 'data/temp_category_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY product_review FROM 'data/review_sample_DB_-_Sheet1.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY product_review FROM 'data/temp_reviews_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
