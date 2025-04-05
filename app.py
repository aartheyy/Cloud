from flask import Flask, render_template
from models import Task
from db import db
import os
import routes  # make sure this is after Flask
from flask_login import LoginManager
from models import User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # redirect for @login_required

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
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@app.route("/")
def index():
    return render_template("index.html")  # <-- must be after `render_template` is imported

routes.register_routes(app)  # <-- must be called after `app` is created

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
