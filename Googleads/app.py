import streamlit as st
import xgboost as xgb
import numpy as np
import joblib

# Load model 
model = xgb.XGBRegressor()
model.load_model('xgboost_conversion_model.json')


# Title
st.title(' Campaign Conversion Predictor ' )

# Input fields
conversion_rate = st.number_input('Conversion Rate', value=0.473823, step=0.01)
metrics_clicks = st.number_input('Metrics Clicks', value=0.473821 , step=0.01)
metrics_impressions = st.number_input('Metrics Impressions', value=0.5248 , step= 0.01)
cost_in_pounds = st.number_input('Cost in Pounds', value=0.4254 , step=0.01)
metrics_conversions_value = st.number_input('Metrics Conversions Value', value=0.224823, step=0.01)
metrics_ctr=st.number_input('Metrics CTR', value=0.024823, step=0.01)
# Predict button
if st.button('Predict Conversions'):
    features = np.array([[conversion_rate, metrics_clicks, metrics_impressions, cost_in_pounds, metrics_conversions_value,metrics_ctr]])
    prediction = model.predict(features)
    st.success(f'Predicted Conversions: {prediction[0]:.2f}')

# Run with: streamlit run app.py 