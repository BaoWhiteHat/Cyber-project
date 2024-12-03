import sqlite3
from flask import Flask, request

# Initialize Flask app
app = Flask(__name__)


# Create an SQLite database and a sample table
def init_db():
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    # Create users table if not exists
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")

    # Insert sample data
    c.execute("INSERT or IGNORE INTO users (username, password) VALUES ('admin', 'password123')")
    c.execute("INSERT or IGNORE INTO users (username, password) VALUES ('user', 'userpass')")

    conn.commit()
    conn.close()


# Vulnerable endpoint
@app.route('/vulnerable', methods=['GET'])
def vulnerable():
    username = request.args.get("username", "")  # Get 'username' parameter from the request

    # Deliberately vulnerable SQL query (directly interpolates user input)
    query = f"SELECT * FROM users WHERE username = '{username}'"

    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    try:
        c.execute(query)  # Execute the query
        rows = c.fetchall()  # Fetch all results
        if rows:
            return f"Results: {rows}"  # Return the results
        else:
            return "No results found."
    except sqlite3.Error as e:
        return f"Database error: {e}"  # Return database error message
    finally:
        conn.close()  # Ensure the connection is closed


# Initialize the database
if __name__ == "__main__":
    init_db()  # Call the function to initialize the database
    app.run(debug=True, port=5000)  # Start the Flask app on port 5000
