import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load data
data = pd.read_csv("model/credit_data.csv")

# Convert employment text to numeric
data['employment_type'] = data['employment_type'].map({
    'salaried': 3,
    'self': 2,
    'student': 1,
    'unemployed': 0
})

# Features and target
X = data[['income','debt','loan_amount','employment_type','property_value']]
y = data['default']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
print(f"\nModel Accuracy: {accuracy:.2f}")

# Save model
with open("model/risk_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\nModel saved as risk_model.pkl")
