from flask import Flask, request, jsonify
import xgboost as xgb
import numpy as np
import os

app = Flask(__name__)

# Check if model file exists
MODEL_PATH = 'xgboost_conversion_model.json'
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file '{MODEL_PATH}' not found.")

# Load the model
model = xgb.XGBRegressor()
model.load_model(MODEL_PATH)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Print data for debugging
    print('Received data:', data)
    try:
        features = np.array([
            [
                data.get('conversion_rate', 0),
                data.get('metrics.clicks', 0),
                data.get('metrics.impressions', 0),
                data.get('cost_in_pounds', 0),
                data.get('metrics.conversions_value', 0)
            ]
        ], dtype=float)
        print('Features shape:', features.shape)
        prediction = model.predict(features)
        return jsonify({'predicted_conversions': float(prediction[0])})
    except Exception as e:
        print('Prediction error:', str(e))
        return jsonify({'error': str(e)}), 400

@app.route('/', methods=['GET'])
def home():
    return 'XGBoost API is running.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)