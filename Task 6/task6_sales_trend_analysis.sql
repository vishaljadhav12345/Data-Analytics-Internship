
-- TASK 6: Sales Trend Analysis Using Aggregations

-- Objective: Analyze monthly revenue and order volume from the online_sales.orders table

-- 1. Monthly revenue and order volume grouped by year and month
SELECT 
    strftime('%Y', order_date) AS year,
    strftime('%m', order_date) AS month,
    SUM(amount) AS total_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM online_sales.orders
GROUP BY year, month
ORDER BY year, month;

-- 2. Limit results to a specific year (e.g., 2023)
-- SELECT 
--     strftime('%Y', order_date) AS year,
--     strftime('%m', order_date) AS month,
--     SUM(amount) AS total_revenue,
--     COUNT(DISTINCT order_id) AS total_orders
-- FROM online_sales.orders
-- WHERE strftime('%Y', order_date) = '2023'
-- GROUP BY year, month
-- ORDER BY year, month;
