from app import app
from db import db
import models  # This will import the Task model

with app.app_context():
    db.create_all()
