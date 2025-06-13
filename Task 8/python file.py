import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# 1. Simulate sales data (like Superstore_Sales.csv)
data = {
    'Order Date': pd.date_range(start="2023-01-01", periods=100, freq='7D'),
    'Region': ['East', 'West', 'Central', 'South'] * 25,
    'Category': ['Furniture', 'Office Supplies', 'Technology'] * 33 + ['Furniture'],
    'Sales': [round(x, 2) for x in abs(np.random.randn(100) * 500)],
    'Profit': [round(x, 2) for x in np.random.randn(100) * 100]
}
df = pd.DataFrame(data)

# 2. Convert Order Date to Month-Year format
df['Month-Year'] = df['Order Date'].dt.to_period('M').astype(str)

# 3. Create PDF to hold the dashboard
with PdfPages("Sales_Dashboard_Report.pdf") as pdf:

    # Line Chart: Monthly Sales
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=df.groupby('Month-Year')['Sales'].sum().reset_index(), x='Month-Year', y='Sales', marker='o')
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    pdf.savefig(); plt.close()

    # Bar Chart: Sales by Region
    plt.figure(figsize=(6, 4))
    sns.barplot(data=df.groupby('Region')['Sales'].sum().reset_index(), x='Region', y='Sales', palette='Set2')
    plt.title("Sales by Region")
    plt.tight_layout()
    pdf.savefig(); plt.close()

    # Donut Chart: Sales by Category
    category_sales = df.groupby('Category')['Sales'].sum()
    plt.figure(figsize=(6, 6))
    wedges, texts, autotexts = plt.pie(category_sales, labels=category_sales.index,
                                       autopct='%1.1f%%', startangle=90)
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title("Sales Distribution by Category")
    plt.tight_layout()
    pdf.savefig(); plt.close()

print("✅ Dashboard saved as Sales_Dashboard_Report.pdf")
