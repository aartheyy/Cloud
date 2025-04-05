from flask import Flask, render_template
from flask_login import LoginManager
from extensions import db, bcrypt
from models import User, Task
from auth_routes import register_auth_routes
import os
import socket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Required for session cookies

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Database and sample data
@app.before_first_request
def create_tables():
    db.create_all()
    if not Task.query.first():
        sample_tasks = [
            Task(title="Learn Azure", user_id=1),
            Task(title="Build To-Do List App", user_id=1),
            Task(title="Push to GitHub & Deploy", completed=True, user_id=1)
        ]
        db.session.add_all(sample_tasks)
        db.session.commit()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/whoami")
def whoami():
    hostname = socket.gethostname()
    return f"Handled by instance: {hostname}"

# Register auth & task routes
register_auth_routes(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
