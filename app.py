from flask import Flask
from db import db
import os

app = Flask(__name__)

# Update the database URI if you are moving to a production DB (like PostgreSQL or Azure SQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To suppress warnings

db.init_app(app)

@app.route('/')
def home():
    return "Hello, Welcome to the To-Do List App!"

# Make sure your app listens on the port specified by Azure (using the PORT environment variable)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000 for local dev
    app.run(host="0.0.0.0", port=port)
