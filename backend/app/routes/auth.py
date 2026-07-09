from flask import Blueprint, jsonify, request
from app.models.user import User
from app.config import Config
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    try:
        user = User.create_user(email, password, name)
        token = generate_token(user['_id'])
        return jsonify({
            "status": "success",
            "message": "User created successfully",
            "token": token,
            "user": {"id": user['_id'], "email": user['email'], "name": user['name']}
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    user = User.authenticate(email, password)
    if user:
        token = generate_token(user['_id'])
        return jsonify({
            "status": "success",
            "message": "Login successful",
            "token": token,
            "user": {"id": user['_id'], "email": user['email'], "name": user.get('name', '')}
        })
    
    return jsonify({"status": "error", "message": "Invalid email or password"}), 401
