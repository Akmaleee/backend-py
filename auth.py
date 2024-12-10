import jwt
import os
from flask import request, jsonify
from functools import wraps

SECRET_KEY = os.getenv("JWT_SECRET")

# Middleware to verify JWT
def verify_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"status": "fail", "message": "Unauthorized"}), 401

        token = auth_header.split(" ")[1]
        try:
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.auth = {"userId": decoded["userId"]}
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"status": "fail", "message": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"status": "fail", "message": "Invalid token"}), 401

    return decorated