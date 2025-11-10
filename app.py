from flask import Flask, request, jsonify
from flask_cors import CORS
from verifier import verify_email

app = Flask(__name__)
CORS(app)  # Allow WordPress frontend access

@app.route('/')
def home():
    return jsonify({"message": "Email Verifier API is live!"})

@app.route('/verify', methods=['POST'])
def verify():
    data = request.get_json()
    if not data or 'email' not in data:
        return jsonify({"error": "Missing 'email' field"}), 400

    email = data['email']
    valid, status = verify_email(email)
    return jsonify({"email": email, "valid": valid, "status": status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
