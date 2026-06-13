from flask import Flask

app = Flask(__name__)

from product_controller import register_routes

register_routes(app)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)