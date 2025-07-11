from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Relay control state (commanded by server/frontend)
relay_state = {
    "Breaker1": 0, "Isolator1": 0, "Breaker2": 0, "Isolator2": 0, "Breaker3": 0, "Isolator3": 0, "Breaker4": 0, "Isolator4": 0,
}

@app.route('/set_relay', methods=['POST'])
def set_relay():
    data = request.json
    if "relay" in data and "state" in data:
        relay = data["relay"]
        state = data["state"]
        if relay in relay_state and state in [0, 1]:
            relay_state[relay] = state
            return jsonify({"status": "success", "message": f"{relay} set to {state}"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/get_relay', methods=['GET'])
def get_relay():
    return jsonify(relay_state), 200

@app.route('/relay_feedback', methods=['POST'])
def post_relay_feedback():
    data = request.json
    success = False
    for relay, state in data.items():
        if relay in relay_state and state in [0, 1]:
            relay_state[relay] = state
            success = True
    if success:
        return jsonify({"status": "success", "message": "Feedback updated"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid feedback data"}), 400

@app.route('/relay_feedback', methods=['GET'])
def get_relay_feedback():
    return jsonify(relay_state), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
