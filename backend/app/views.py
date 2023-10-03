from flask import jsonify, request
from app import app, db
from app.models import User
from flask_login import login_user, logout_user, login_required
from flask_login import current_user

from flask import Flask, jsonify, request




# metoda e regjistrimit te userit

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify(success=False, message="Username already taken."), 400

    user = User(username=username, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(success=True, message="Registration successful!")

# metoda per logimin e userit

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify(success=True, message="Login successful!")
    else:
        return jsonify(success=False, message="Invalid username or password."), 401

# homepage
#  
@app.route('/index')
@login_required
def index():
    return jsonify(message="Hello World!")

# logout metoda
@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify(success=True, message="Logged out successfully!")

# 
# profili i userit
# 
# metoda e shikimit te informatave  te veta te userit

@app.route('/user_details', methods=['GET'])
@login_required
def get_user_details():
    print("Is authenticated:", current_user.is_authenticated)
    print("Current user:", current_user.username)
    user_data = {
        'id': current_user.id,
        'username': current_user.username,
        'role': current_user.role
    }
    return jsonify(user_data)

# metoda qe useri me ndryshu vet passwordin e vet

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify(success=False, message="Both old and new passwords are required."), 400

    # Check if the old password is correct
    if current_user.check_password(old_password):
        # Set the new password
        current_user.set_password(new_password)
        db.session.commit()
        return jsonify(success=True, message="Password successfully updated!")
    else:
        return jsonify(success=False, message="Incorrect old password."), 401
    

@app.route('/api/workers', methods=['GET'])
def get_workers():
    # Assuming you have a role or similar field in your User model to differentiate workers.
    workers = User.query.filter_by(role='worker').all()

    # Convert the workers to a format that can be returned as JSON.
    worker_list = [{'id': worker.id, 'username': worker.username} for worker in workers]
    
    return jsonify(worker_list)


@app.route('/api/workers/<int:worker_id>', methods=['PUT'])
def edit_worker(worker_id):
    worker = User.query.get(worker_id)
    if not worker:
        return jsonify({"success": False, "message": "Worker not found"}), 404

    data = request.get_json()
    new_username = data.get('username')
    if not new_username:
        return jsonify({"success": False, "message": "Username is required"}), 400

    worker.username = new_username
    db.session.commit()

    return jsonify({"success": True, "message": "Worker updated successfully"}), 200


@app.route('/api/workers/<int:worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    worker = User.query.get(worker_id)
    if not worker:
        return jsonify({"success": False, "message": "Worker not found"}), 404

    db.session.delete(worker)
    db.session.commit()

    return jsonify({"success": True, "message": "Worker deleted successfully"}), 200
