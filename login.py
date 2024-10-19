import random

from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def UserLogin():
    try:
        # Extract request data
        body = request.get_json()  # use get_json() for Flask's request object
        uname = body.get("uname") # safely get 'uname'
        upass = body.get("upass") # safely get 'upass'

        # Database connection setup
        con = psycopg2.connect(
            database="Lemonade",
            user="postgres",
            password="123",  # Fill in your PostgreSQL password here
            host="127.0.0.1",
            port="5432"
        )

        cur = con.cursor(cursor_factory=DictCursor)

        # Query to find user by username
        cur.execute("SELECT * FROM lemonade.user WHERE name = %s and password = %s", (uname, upass))

        # Check if user exists
        if cur.rowcount > 0:
            user_data = cur.fetchone() # Fetch the user data
            uid = user_data.get("id")

            rndcode = ''.join(random.sample('0123456789', 6))

            cur.execute("UPDATE lemonade.user SET confirm_code = %s, expired_code = now() + INTERVAL '2 minutes' WHERE id = %s ", (rndcode, uid))
            con.commit()

            # Prepare successful response
            response = {
                'cd': "000",
                'sms': "Success!",
                'data': dict(user_data) # Convert the result to a dictionary
            }

        else:
            # If user not found, return failure response
            response = {
                'cd': "888",
                'sms': "User not found!",
                'data': {}
            }

        # Close the cursor and connection
        cur.close()
        con.close()

        return jsonify(response)  # Use jsonify for JSON response

    except Exception as ex:
        # Catch and return error with details
        return jsonify({
            'cd': "999",
            'sms': f"Unhandled error: {str(ex)}",
            'data': {}
        }), 500  # Return status code 500 for server error


if __name__ == '__main__':
    app.run(debug=True, port=5000)
