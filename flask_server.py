from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"Received authorization code: {code}")
    return "Authorization successful, you can close this window."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8009)