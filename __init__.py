from flask import Flask
from config import Config
from extensions import db, csrf
from routes import main
from api.product_api import product_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(product_api)

    return app
