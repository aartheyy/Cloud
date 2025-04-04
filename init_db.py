from app import app
from db import db
import models  # this will import your Task model

# This will create all tables defined in models (like Task)
with app.app_context():
    db.create_all()
