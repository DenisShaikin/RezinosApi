from flask import Flask, url_for
# from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_restful import Api, reqparse


from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
# from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()

# login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    # login_manager.init_app(app)
    # csrf = CSRFProtect()
    # csrf.init_app(app)

# def register_blueprints(app):
#     module = import_module('app.routes')
#     app.register_blueprint(module.blueprint)

def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()
    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__)  #static_folder='base/static'
    app.config.from_object(config)

    register_extensions(app)
    # register_blueprints(app)
    configure_database(app)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    api = Api(app)
    from app.api.routes import TirePrices, NewUser, GetUser, GetResource, GetAuthToken
    api.add_resource(TirePrices, '/api/<string:region>')
    api.add_resource(NewUser, '/api/users')
    api.add_resource(GetResource, '/api/resource')
    api.add_resource(GetAuthToken, '/api/token')
    api.add_resource(GetUser, '/api/users/<int:id>')

    return app

