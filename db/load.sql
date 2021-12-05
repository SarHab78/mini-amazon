\COPY Users FROM 'data/Users_stress_test_db.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

--\COPY Users FROM 'data/temp_users_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Products FROM 'data/products_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_product_id_seq',
                         (SELECT MAX(product_id)+1 FROM Products),
                         false);



--\COPY Products FROM 'data/temp_products_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Category FROM 'data/category_stress_test_db.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Category FROM 'data/temp_category_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY Purchases FROM 'data/Purchases.csv' WITH DELIMITER ',' NULL '' CSV
\COPY product_review FROM 'data/review_sample_DB_-_Sheet1.csv' WITH DELIMITER ',' NULL '' CSV
--\COPY product_review FROM 'data/temp_reviews_stress_test.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Seller_review FROM 'data/seller_review_db.csv' WITH DELIMITER ',' NULL '' CSV
