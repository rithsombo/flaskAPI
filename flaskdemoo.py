from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import string

app = Flask(__name__)
CORS(app)

# Mock user data for illustration
users = {
    "example_user": {
        "password": "password123",
        "is_active": True,
        "confirm_code": "abc123"  # Hardcoded confirmation code for example
    }
}


# Helper function to generate random confirmation code
def generate_confirm_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users.get(username)

    if user and user['password'] == password:
        confirm_code = generate_confirm_code()  # Generate or retrieve confirm code
        users[username]['confirm_code'] = confirm_code
        print(generate_confirm_code())
        # Store code for user
        return jsonify({
            "status": "success",
            "message": "Login successful! Please enter the verification code.",
            "confirm_code": confirm_code  # For now, returning the code (in real cases, send via email/SMS)
        })
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401


# Endpoint to verify confirmation code
@app.route('/verify-code', methods=['POST'])
def verify_code():
    data = request.json
    username = data.get('username')
    input_code = data.get('confirm_code')

    user = users.get(username)
    if user and user['confirm_code'] == input_code:
        return jsonify({"status": "success", "message": "Verification successful!"})
    else:
        return jsonify({"status": "fail", "message": "Invalid verification code"}), 401


if __name__ == '__main__':
    app.run(debug=True)
