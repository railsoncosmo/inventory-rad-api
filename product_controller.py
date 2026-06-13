from product_service import ProductService
from flask import jsonify, request

product_service = ProductService()


def register_routes(app):
  @app.route("/")
  def health():
    return "Server is running"

  @app.route("/products", methods=["GET"])
  def get_products():
    name = request.args.get("name", "").strip()
    where = {"name": name} if name else None
    products = product_service.find(where)
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


if __name__ == "__main__":
  from flask import Flask

  app = Flask(__name__)
  register_routes(app)
  app.run(host="127.0.0.1", port=5001)
