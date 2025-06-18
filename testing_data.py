import requests
data = {
    "conversion_rate": 0.05,
    "metrics.clicks": 100,
    "metrics.impressions": 2000,
    "cost_in_pounds": 50,
    "metrics.conversions_value": 300
}
response = requests.post("http://127.0.0.1:5000/predict", json=data)
print(response.json())