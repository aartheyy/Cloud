from flask import request, jsonify
from models import Task, User

from flask_login import login_user, login_required, logout_user, current_user
from app import app, db, bcrypt

def register_routes(app):
    @app.route('/tasks', methods=['GET'])
    @login_required
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([{'id': t.id, 'title': t.title, 'completed': t.completed} for t in tasks])

    @app.route('/tasks', methods=['POST'])
    @login_required
    def add_task():
        data = request.get_json()
        new_task = Task(title=data['title'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added'}), 201

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    @login_required
    def update_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        task.completed = True
        db.session.commit()
        return jsonify({'message': 'Task completed'})

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    @login_required
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            login_user(user)
            return jsonify({'message': 'Logged in'})
        return jsonify({'error': 'Invalid credentials'}), 401
    
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(username=data['username'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered'})
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return jsonify({'message': 'Logged out'})

    @app.route('/profile')
    def profile():
        if current_user.is_authenticated:
            return jsonify({'logged_in': True, 'username': current_user.username})
        return jsonify({'logged_in': False})
