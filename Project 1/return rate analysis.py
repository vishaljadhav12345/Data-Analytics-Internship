# return_rate_analysis.py

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. Load and clean data
def load_csv_safely(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"The file '{filename}' was not found. Please ensure it is in the working directory.")
    return pd.read_csv(filename)

returns = load_csv_safely('returns.csv')
orders = load_csv_safely('orders.csv')

# Merge datasets
full_data = pd.merge(orders, returns, on='order_id', how='left')
full_data['is_returned'] = full_data['return_id'].notnull().astype(int)

# Drop columns not needed for modeling
drop_cols = ['return_id', 'order_id', 'customer_id']
full_data = full_data.drop(columns=[col for col in drop_cols if col in full_data.columns])

# Fill missing values and encode categorical features
if 'marketing_channel' in full_data.columns:
    full_data['marketing_channel'] = full_data['marketing_channel'].fillna('Unknown')
    full_data = pd.get_dummies(full_data, drop_first=True)

# 2. Analyze return % by category and supplier
if 'category' in full_data.columns:
    return_rate_category = full_data.groupby('category')['is_returned'].mean().reset_index()
    return_rate_category.to_csv('return_rate_by_category.csv', index=False)

if 'supplier' in full_data.columns:
    return_rate_supplier = full_data.groupby('supplier')['is_returned'].mean().reset_index()
    return_rate_supplier.to_csv('return_rate_by_supplier.csv', index=False)

# 3. Logistic Regression Model
X = full_data.drop(columns=['is_returned'])
y = full_data['is_returned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 4. Prediction and Risk Score
full_data['return_probability'] = model.predict_proba(X)[:, 1]
full_data['predicted_return'] = model.predict(X)

# Save high risk products (probability > 0.7)
high_risk = full_data[full_data['return_probability'] > 0.7]
high_risk.to_csv('high_risk_products.csv', index=False)

# 5. Evaluation
print(classification_report(y_test, model.predict(X_test)))
