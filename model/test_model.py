import pickle
import pandas as pd

# Load trained model
with open("model/risk_model.pkl", "rb") as f:
    model = pickle.load(f)

# Sample borrower data with column names
sample_user = pd.DataFrame([{
    "income":600000,
    "debt":120000,
    "loan_amount":250000,
    "employment_type":3,
    "property_value":500000
}])

prediction = model.predict(sample_user)[0]
probability = model.predict_proba(sample_user)[0][1]

print("\nPrediction:", "RISKY" if prediction == 1 else "SAFE")
print(f"Risk Probability: {probability:.2f}")
