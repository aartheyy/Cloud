# auth_routes.py

from flask import request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from models import Task, User
from extensions import db, bcrypt

def register_auth_routes(app):

    # -------------------------------
    # ✅ CRUD Routes (JSON-based API)
    # -------------------------------

    @app.route('/tasks', methods=['GET'])
    @login_required
    def get_tasks():
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return jsonify([
            {'id': t.id, 'title': t.title, 'completed': t.completed}
            for t in tasks
        ])

    @app.route('/tasks', methods=['POST'])
    @login_required
    def add_task():
        data = request.get_json()
        title = data.get('title')
        if not title:
            return jsonify({'error': 'No title provided'}), 400
        new_task = Task(title=title, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added'}), 201

    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    @login_required
    def complete_task(task_id):
        task = Task.query.get(task_id)
        if not task or task.user_id != current_user.id:
            return jsonify({'error': 'Task not found'}), 404
        task.completed = True
        db.session.commit()
        return jsonify({'message': 'Task marked as completed'})

    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    @login_required
    def delete_task(task_id):
        task = Task.query.get(task_id)
        if not task or task.user_id != current_user.id:
            return jsonify({'error': 'Task not found'}), 404
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})

    # -------------------------------
    # ✅ Auth Routes (JSON-based API)
    # -------------------------------

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'User already exists'}), 409
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered'})

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': 'Missing credentials'}), 400
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Login successful'})
        return jsonify({'error': 'Invalid credentials'}), 401

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
