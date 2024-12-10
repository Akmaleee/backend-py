from flask import request, jsonify
from database import get_db_connection
from auth import verify_token
import datetime

@verify_token
def add_product():
    user_id = request.auth["userId"]
    data = request.json
    required_fields = ["namaProduct", "valueProduct"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "fail", "message": "Missing fields"}), 400

    created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO products (userId, namaProduct, valueProduct, createdAt) VALUES (%s, %s, %s, %s)",
                (user_id, data["namaProduct"], data["valueProduct"], created_at),
            )
        connection.commit()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Error: {str(e)}"}), 500
    finally:
        connection.close()

@verify_token
def get_products():
    user_id = request.auth["userId"]
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE userId = %s", (user_id,))
            products = cursor.fetchall()
        return jsonify({"status": "success", "products": products}), 200
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Error: {str(e)}"}), 500
    finally:
        connection.close()