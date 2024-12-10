import bcrypt
import jwt
import datetime
from flask import request, jsonify
from database import get_db_connection
from auth import SECRET_KEY

# Register a new user
def register_user():
    data = request.json
    required_fields = ["email", "password", "name", "age", "bb"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "fail", "message": "Missing fields"}), 400

    password = data["password"]
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    user_id = jwt.encode({"email": data["email"]}, SECRET_KEY, algorithm="HS256")
    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (id, email, password, name, age, bb, createdAt) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (user_id, data["email"], hashed_password, data["name"], data["age"], data["bb"], created_at),
            )
        connection.commit()
        return jsonify({"status": "success", "userId": user_id}), 201
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Error: {str(e)}"}), 500
    finally:
        connection.close()

# Login user
def login_user():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
                return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

            token = jwt.encode(
                {"userId": user["id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                SECRET_KEY,
                algorithm="HS256",
            )
            return jsonify({"status": "success", "token": token}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Error: {str(e)}"}), 500
    finally:
        connection.close()