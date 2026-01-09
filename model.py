import numpy as np
import pandas as pd
from joblib import load
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

# Load dataset
data = pd.read_csv("Loan_default.csv")

# Categorical columns (LoanPurpose removed)
categorical_cols = [
    "Education", "EmploymentType", "MaritalStatus",
    "HasMortgage", "HasDependents", "HasCoSigner"
]

def normalize_string(s):
    return str(s).strip().lower()

data[categorical_cols] = data[categorical_cols].astype(str).applymap(normalize_string)

# Encode categorical
encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
data[categorical_cols] = encoder.fit_transform(data[categorical_cols])

# Prepare X & scale
X = data.drop(["Default", "LoanID", "LoanPurpose"], axis=1)
scaler = StandardScaler()
scaler.fit(X)

# Load decision tree model
model = load("DecisionTree.joblib")

def predict_default(user_input_dict):

    user_copy = user_input_dict.copy()

    for col in categorical_cols:
        user_copy[col] = normalize_string(user_copy[col])

    user_df = pd.DataFrame([user_copy])
    user_df[categorical_cols] = encoder.transform(user_df[categorical_cols])

    user_scaled = scaler.transform(user_df)

    return int(model.predict(user_scaled)[0])
