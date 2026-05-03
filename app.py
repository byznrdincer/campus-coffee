from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from cosmosdb import create_order, get_all_orders, update_order_status

app = Flask(__name__)
CORS(app)

MENU = [
    {"id": 1, "name": "Espresso", "price": 25, "emoji": "☕"},
    {"id": 2, "name": "Latte", "price": 35, "emoji": "🥛"},
    {"id": 3, "name": "Cappuccino", "price": 35, "emoji": "☕"},
    {"id": 4, "name": "Americano", "price": 30, "emoji": "🖤"},
    {"id": 5, "name": "Çay", "price": 15, "emoji": "🍵"},
    {"id": 6, "name": "Sandviç", "price": 45, "emoji": "🥪"},
]

@app.route("/")
def index():
    return render_template("index.html", menu=MENU)

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    order = create_order(data["student_name"], data["items"], data.get("note", ""))
    return jsonify(order)

@app.route("/admin")
def admin():
    orders = get_all_orders()
    return render_template("admin.html", orders=orders)

@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.json
    update_order_status(data["order_id"], data["status"])
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
