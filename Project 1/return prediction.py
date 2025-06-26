# return_prediction.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# 1. Load datasets
orders = pd.read_csv('orders.csv')
returns = pd.read_csv('returns.csv')

# 2. Merge and prepare data
df = pd.merge(orders, returns, on='order_id', how='left')
df['is_returned'] = df['return_id'].notnull().astype(int)

# Drop unused columns
df = df.drop(columns=['order_id', 'return_id', 'customer_id'])

# Fill missing values
df['marketing_channel'] = df['marketing_channel'].fillna('Unknown')

# Encode categorical features
df = pd.get_dummies(df, drop_first=True)

# 3. Prepare for modeling
X = df.drop(columns=['is_returned'])
y = df['is_returned']

# 4. Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 5. Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 6. Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# 7. Predict on full data
df['return_probability'] = model.predict_proba(X)[:, 1]
df['predicted_return'] = model.predict(X)

# 8. Save high-risk products (prob > 0.7)
high_risk = df[df['return_probability'] > 0.7]
high_risk.to_csv('high_risk_products.csv', index=False)

print("✅ High-risk products saved to 'high_risk_products.csv'")
