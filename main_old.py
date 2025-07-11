from flask import Flask, request, jsonify

app = Flask(__name__)

# Store relay states
relay_state = {"relay1": 0, "relay2": 0}

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
