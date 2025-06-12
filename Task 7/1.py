import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Create SQLite database and connect
conn = sqlite3.connect("/mnt/data/sales_data.db")
cursor = conn.cursor()

# Step 2: Create sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Step 3: Insert sample data
sample_data = [
    ('Apple', 10, 2.0),
    ('Banana', 20, 1.0),
    ('Orange', 15, 1.5),
    ('Apple', 5, 2.0),
    ('Banana', 10, 1.0),
    ('Orange', 5, 1.5),
]

cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# Step 4: Run SQL query to get summary
query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue 
FROM sales 
GROUP BY product
"""

df = pd.read_sql_query(query, conn)

# Step 5: Print the results
print("📊 Sales Summary:")
print(df)

# Step 6: Plot bar chart for revenue per product
plt.figure(figsize=(8, 5))
df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()

# Save the plot
chart_path = "/mnt/data/sales_chart.png"
plt.savefig(chart_path)
plt.close()

# Clean up
conn.close()

chart_path
