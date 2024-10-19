from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import psycopg2
from psycopg2.extras import DictCursor

app = Flask(__name__)
CORS(app)

@app.route('/confirmcode', methods=['POST'])
def ConfirmCode():
    try:
        # Extract request data
        body = request.get_json()  # use get_json() for Flask's request object
        uname = body.get("uname") # safely get 'uname'
        upass = body.get("upass") # safely get 'upass'
        ucode = body.get("ucode")

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
        cur.execute("SELECT * FROM lemonade.user WHERE name = %s and password = %s and confirm_code = %s and expired_code >= now()", (uname, upass, ucode))


        # Check if user exists
        if cur.rowcount > 0:
            user_data = cur.fetchone() # Fetch the user data

            # Prepare successful response
            response = {
                'cd': "000",
                'sms': "Verify Success!",
                'data': dict(user_data) # Convert the result to a dictionary
            }

        else:
            # If user not found, return failure response
            response = {
                'cd': "888",
                'sms': "Verify Failed!",
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


@app.route('/showall', methods=['GET'])
def ShowAllUser():
    try:
        con = psycopg2.connect(
            database="Lemonade",
            user="postgres",
            password="123",  # Fill in your PostgreSQL password here
            host="127.0.0.1",
            port="5432"
        )
        cur = con.cursor(cursor_factory=DictCursor)

        # Query to find user by username
        cur.execute( "SELECT id, name, password, is_active FROM lemonade.user order by id ASC")

        users = cur.fetchall()

        # Check if user exists
        if cur.rowcount > 0:
              # Fetch the user data
            users_list = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in users]

            # Prepare successful response

            response = {
                  'cd': "000",
                  'sms': "Verify Success!",
                  'users_list': users_list  # Ensure you are returning this under 'users_list'
              }
        else:
              # If no users were found, return failure response
              response = {
                  'cd': "888",
                  'sms': "No users found!",
                  'users_list': []  # Make sure to return an empty list if no users
              }

        # Close the cursor and connection
        cur.close()
        con.close()

        # Return the response as JSON
        return jsonify(response)

    except Exception as ex:
        # Log and return error with details
        return jsonify({
            'cd': "999",
            'sms': f"Unhandled error: {str(ex)}",
            'users_list': []  # Return empty list in case of error
        }), 500  # Return status code 500 for server error

if __name__ == '__main__':
    app.run(debug=True, port=5001)
