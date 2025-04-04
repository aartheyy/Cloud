from flask import Flask
from db import db
import os

app = Flask(__name__)

# Update the database URI if you are moving to a production DB like PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress a warning

db.init_app(app)

@app.route('/')
def home():
    return "Hello, Welcome to the To-Do List App!"

# Make sure your app listens on the port specified by Azure
if __name__ == "__main__":
    # Use the environment variable for the port Azure assigns
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
