from flask import Flask
from models import Task
from db import db
import os

app = Flask(__name__)

# SQLite Database URI for local development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress a warning

db.init_app(app)
@app.before_first_request
def create_tables():
    db.create_all()

    # Insert only if DB is empty
    if not Task.query.first():
        sample_tasks = [
            Task(title="Learn Azure"),
            Task(title="Build To-Do List App"),
            Task(title="Push to GitHub & Deploy", completed=True)
        ]
        db.session.add_all(sample_tasks)
        db.session.commit()
    
@app.route('/')
def home():
    return "Welcome to the To-Do List App!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
