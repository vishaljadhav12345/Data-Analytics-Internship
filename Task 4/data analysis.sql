-- 1. TABLE CREATION

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    city VARCHAR(50)
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- 2. SAMPLE DATA INSERTION

INSERT INTO customers (customer_id, first_name, last_name, city) VALUES
(1, 'Alice', 'Smith', 'New York'),
(2, 'Bob', 'Jones', 'Chicago'),
(3, 'Carol', 'Lee', 'New York');

INSERT INTO products (product_id, product_name, price) VALUES
(1, 'Widget', 10.0),
(2, 'Gadget', 20.0);

INSERT INTO orders (order_id, customer_id, order_date) VALUES
(1, 1, '2025-06-01'),
(2, 2, '2025-06-02'),
(3, 1, '2025-06-03');

INSERT INTO order_items (order_item_id, order_id, product_id, quantity) VALUES
(1, 1, 1, 2),
(2, 1, 2, 1),
(3, 2, 2, 3),
(4, 3, 1, 1);

-- 3. DATA ANALYSIS QUERIES

-- a. SELECT, WHERE, ORDER BY, GROUP BY
SELECT * FROM customers
WHERE city = 'New York'
ORDER BY last_name;

SELECT customer_id, COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC;

-- b. JOINS (INNER, LEFT, RIGHT)
SELECT o.order_id, c.first_name, c.last_name, o.order_date
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

SELECT c.customer_id, c.first_name, o.order_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

-- (Note: SQLite does not support RIGHT JOIN)
SELECT o.order_id, c.first_name, c.last_name
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.customer_id;

-- c. SUBQUERIES
SELECT customer_id, first_name, last_name
FROM customers
WHERE customer_id IN (
    SELECT customer_id
    FROM orders
    GROUP BY customer_id
    HAVING COUNT(*) > 1
);

SELECT * FROM products
WHERE price = (SELECT MAX(price) FROM products);

-- d. AGGREGATE FUNCTIONS (SUM, AVG)
SELECT p.product_id, p.product_name, SUM(oi.quantity * p.price) AS total_sales
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sales DESC;

SELECT AVG(order_total) AS avg_order_value
FROM (
    SELECT o.order_id, SUM(oi.quantity * p.price) AS order_total
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY o.order_id
) AS sub;

-- e. CREATE VIEWS FOR ANALYSIS
CREATE VIEW customer_order_summary AS
SELECT c.customer_id, c.first_name, c.last_name, COUNT(o.order_id) AS num_orders, COALESCE(SUM(oi.quantity * p.price),0) AS total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
GROUP BY c.customer_id, c.first_name, c.last_name;

-- f. OPTIMIZE QUERIES WITH INDEXES
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_products_price ON products(price);

-- To view the customer order summary
SELECT * FROM customer_order_summary;
