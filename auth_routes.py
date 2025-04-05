# auth_routes.py

from flask import request, jsonify, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from models import Task, User
from db import db
from extensions import bcrypt


def register_auth_routes(app):
    @app.route('/tasks', methods=['GET'])
    @login_required
    def get_tasks_html():
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        return render_template("tasks.html", tasks=tasks, username=current_user.username)

    @app.route('/tasks', methods=['POST'])
    @login_required
    def add_task():
        title = request.form.get('title') or (request.json and request.json.get('title'))
        if not title:
            return jsonify({'error': 'No title provided'}), 400

        new_task = Task(title=title, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()

        if request.form:
            return redirect(url_for('get_tasks_html'))
        return jsonify({'message': 'Task added'}), 201

    @app.route('/tasks/<int:task_id>', methods=['POST', 'PUT', 'DELETE'])
    @login_required
    def update_or_delete_task(task_id):
        task = Task.query.get(task_id)
        if not task or task.user_id != current_user.id:
            return jsonify({'error': 'Task not found'}), 404

        method = request.form.get('_method', '').upper() or request.method

        if method == 'PUT':
            task.completed = True
            db.session.commit()
            return redirect(url_for('get_tasks_html')) if request.form else jsonify({'message': 'Task marked completed'})

        elif method == 'DELETE':
            db.session.delete(task)
            db.session.commit()
            return redirect(url_for('get_tasks_html')) if request.form else jsonify({'message': 'Task deleted'})

        return jsonify({'error': 'Invalid method'}), 400

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
