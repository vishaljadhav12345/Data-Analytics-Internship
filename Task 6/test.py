# Generate SQL script for Task 6: Sales Trend Analysis Using Aggregations

task6_sql_script = """
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
"""

# Save to .sql file
task6_sql_path = "task6_sales_trend_analysis.sql"
with open(task6_sql_path, "w") as f:
    f.write(task6_sql_script)
task6_sql_path
