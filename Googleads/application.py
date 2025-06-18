import streamlit as st
import xgboost as xgb
import numpy as np
import joblib

# Load model 
model = xgb.XGBRegressor()
model.load_model('xgboost_conversion_model.json')


# Streamlit UI for inputs
st.title("Budget Prediction for Conversions")

# Input fields for user
new_clicks = st.number_input("Enter new clicks", min_value=0, value=50)
new_impressions = st.number_input("Enter new impressions", min_value=0, value=500)
new_ctr = st.number_input("Enter new CTR (e.g., 0.02)", min_value=0.0, value=0.02)
new_cost_in_pounds = st.number_input("Enter new cost in pounds", min_value=0.0, value=30.00)
new_conversion_value = st.number_input("Enter new conversion value", min_value=0.0, value=0.35)
new_conversion_rate = st.number_input("Enter new conversion rate (e.g., 0.4)", min_value=0.0, value=0.4)

# Budgets to test
budgets_to_test = [10, 15, 20, 25]

# Initialize variables
best_budget = None
max_conversions = -1

# Calculate the best budget based on model predictions
for budget in budgets_to_test:
    prediction = model.predict([[new_clicks, new_impressions, new_cost_in_pounds, new_conversion_value, new_ctr, new_conversion_rate]])
    if prediction[0] > max_conversions:
        max_conversions = prediction[0]
        best_budget = budget

# Display the result
if best_budget is not None:
    st.write(f"**Recommended budget:** {best_budget} (predicts {max_conversions:.2f} conversions)")
else:
    st.write("No prediction available.")
