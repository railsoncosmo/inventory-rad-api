from app import app
from product_service import ProductService
from flask import jsonify, request

product_service = ProductService()

@app.route("/")
def health():
  return "Server is running"

@app.route("/products", methods=["GET"])
def get_products():
  products = product_service.find()
  return jsonify(products), 200

@app.route("/products", methods=["POST"])
def create_product():
  data = request.json
  product = product_service.insert(data)
  return jsonify(product), 201

@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
  product = product_service.findOne(id)
  return jsonify(product), 200

@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
  data = request.json
  product = product_service.update(id, data)
  return jsonify(product), 200

@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
  product = product_service.delete(id)
  return jsonify(product), 200
