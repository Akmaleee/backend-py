from flask import Flask
from handlers.users import register_user, login_user
from handlers.products import add_product, get_products
from handlers.ocr import process_ocr

app = Flask(__name__)

app.route("/register", methods=["POST"])(register_user)
app.route("/login", methods=["POST"])(login_user)
app.route("/products", methods=["POST"])(add_product)
app.route("/products", methods=["GET"])(get_products)
app.route("/ocr", methods=["POST"])(process_ocr)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)