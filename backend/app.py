from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows the frontend (running on a different port) to call this API

@app.route("/")
def home():
    return jsonify({"message": "AgriSense backend is running"})

@app.route("/api/ping")
def ping():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)