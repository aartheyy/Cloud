# app.py

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from models import Task, User
from db import db

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # required for session cookies

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    if not Task.query.first():
        sample_tasks = [
            Task(title="Learn Azure"),
            Task(title="Build To-Do List App"),
            Task(title="Push to GitHub & Deploy", completed=True)
        ]
        db.session.add_all(sample_tasks)
        db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

import socket

@app.route("/whoami")
def whoami():
    hostname = socket.gethostname()
    return f"Handled by instance: {hostname}"


from auth_routes import register_auth_routes
register_auth_routes(app)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
