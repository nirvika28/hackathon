from flask import Flask, request, jsonify
import joblib
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

# Load trained model
model = joblib.load('overspending_model_final.pkl')

def generate_nudge(limit, amount):
    if limit <= 0:
        return None

    percent_over = ((amount - limit) / limit) * 100
    input_features = np.array([[limit, amount, percent_over]])
    
    risk_level = model.predict(input_features)[0]

    if risk_level == 'low':
        return None
    else:
        return f"Alert: You have overspent your limit by {round(percent_over, 2)}%. Consider pausing spending this week."

@app.route('/check_spending', methods=['POST'])
def check_spending():
    data = request.json
    print("Received Data:", data)  # DEBUG PRINT

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    limit = data.get('limit')
    amount = data.get('amount')

    if limit is None or amount is None:
        return jsonify({"error": "Missing limit or amount value"}), 400

    message = generate_nudge(limit, amount)
    return jsonify({"nudge": message})

if __name__ == '__main__':
    app.run(debug=True)
